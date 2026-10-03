# -*- coding: utf-8 -*-
"""Pazaryeri yorum ve soru-cevap kayitlarini tek semada birlestirir.
Kaynaklar:
  - Trendyol resmi magaza paneli: urun degerlendirmeleri (xlsx) ve urun sorulari (xlsx)
  - Hepsiburada ve Trendyol herkese acik urun sayfalari (Apify; veri/ham/yorum/*.jsonl)
Kisisel veri tutulmaz: yorumcu ve soru soran adi hic okunmaz; metindeki telefon, e-posta ve uzun numaralar maskelenir.
Cikti: veri/islenmis/yorum_kayit.json"""
import json, os, re, glob, datetime as dt
import openpyxl
import veri

KOK = veri.KOK
HAM = os.path.join(veri.V, "ham", "yorum")
PANEL = os.path.join(KOK, "pazaryeri-verileri", "trendyol")
RESMI_HB = {"VitrA", "VitrA Online"}

# ---------------------------------------------------------------- marka ve urun grubu
MARKA = [(r"^vitra$", "VitrA"), (r"^artema$", "Artema"), (r"^(kale|kalebodur|kale banyo)$", "Kale"), (r"^creavit$", "Creavit"),
         (r"^(e\.?c\.?a\.?|eca)$", "E.C.A."), (r"^serel$", "Serel"), (r"^grohe$", "Grohe"), (r"^(turkuaz|turkuaz seramik)$", "Turkuaz"),
         (r"^geberit$", "Geberit"), (r"^turavit$", "Turavit"), (r"^visam$", "Visam"), (r"^durul$", "Durul"), (r"^newarc$", "Newarc"),
         (r"^hansgrohe$", "Hansgrohe"), (r"^tema$", "TEMA"), (r"^berev$", "Berev"), (r"^suvia$", "Suvia"), (r"^itimat$", "İtimat"),
         (r"^hms$", "HMS"), (r"^punto$", "Punto"), (r"^seramiksan$", "Seramiksan"), (r"^ege seramik$", "Ege Seramik")]
def marka(m):
    t = (m or "").strip()
    tl = t.lower().replace("İ", "i")
    for rx, ad in MARKA:
        if re.match(rx, tl): return ad
    return t[:1].upper() + t[1:] if t else "Belirtilmemiş"

GRUP = [("Klozet kapağı", r"klozet kapa|kapak.*klozet|wc kapa|yavaş kapanan kapak"),
        ("Rezervuar ve iç takım", r"rezervuar|iç takım|şamandıra|kumanda panel|basma buton|flush"),
        ("Banyo dolabı", r"banyo dolab|lavabo dolab|aynalı dolap|dolap seti|banyo mobilya|çamaşır makinesi dolab|boy dolab"),
        ("Duşakabin", r"duşakabin|dusakabin|duş kabin|duş paravan"),
        ("Lavabo bataryası", r"lavabo batarya|lavabo musluk|lavabo armat|çanak lavabo batarya|fotoselli"),
        ("Banyo ve duş bataryası", r"banyo batarya|duş batarya|ankastre|termostatik|banyo musluk|banyo armat"),
        ("Eviye bataryası", r"eviye batarya|mutfak batarya|evye batarya|mutfak musluk"),
        ("Duş seti ve sistemi", r"duş set|duş sistem|tepe duş|el duş|duş başlı|duş kolon|duş hortum|robot duş|yağmur|mafsallı"),
        ("Klozet", r"klozet|asma klozet|wc"),
        ("Lavabo", r"lavabo|çanak|etajer"),
        ("Ara musluk ve tesisat", r"ara musluk|ara valf|sifon|süzgeç|tesisat|bağlantı|spiral|vana"),
        ("Banyo aksesuarı", r"askı|havluluk|kağıtlık|sabunluk|fırçalık|diş fırça|raf|aksesuar|tutamak|taharet|musluk başlığı|perlatör")]
def grup(ad, kat=""):
    t = ("%s %s" % (ad or "", kat or "")).lower().replace("İ", "i")
    for g, rx in GRUP:
        if re.search(rx, t): return g
    return "Diğer"

# ---------------------------------------------------------------- metin temizligi
_TEL = re.compile(r"(\+?90[\s-]?)?0?\s?5\d{2}[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}")
_EPOSTA = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_UZUN = re.compile(r"\b\d{9,}\b")
_VITRA = re.compile(r"\bvitra\b", re.I)
from kisi_ad import ADLAR, yalniz_ad
_ADSOYAD = re.compile(r"\b([A-ZÇĞİÖŞÜ][a-zçğıöşü]+)\s+([A-ZÇĞİÖŞÜ][a-zçğıöşü]+|[A-ZÇĞİÖŞÜ]{2,})\b")
def _ad_maske(s):
    return _ADSOYAD.sub(lambda m: "[ad]" if m.group(1).replace("İ", "i").lower() in ADLAR else m.group(0), s)
def temiz(s):
    if not s: return ""
    if yalniz_ad(str(s)): return "[ad]"
    s = re.sub(r"\s+", " ", str(s)).strip().replace("\u2014", "-").replace("\u2013", "-")
    s = _EPOSTA.sub("[e-posta]", s); s = _TEL.sub("[telefon]", s); s = _UZUN.sub("[numara]", s)
    return _VITRA.sub("VitrA", _ad_maske(s))

def ad_duz(s):
    return _VITRA.sub("VitrA", re.sub(r"\s+", " ", str(s or "")).strip())

def tarih(s):
    if not s: return None
    s = str(s)
    for f in ("%d-%m-%Y %H:%M", "%d.%m.%Y %H:%M"):
        try: return dt.datetime.strptime(s, f).strftime("%Y-%m-%d")
        except ValueError: pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return m.group(1) if m else None

def _saat(a, b):
    try:
        t1 = dt.datetime.fromisoformat(a.replace("Z", "+00:00")[:26] + ("+00:00" if "+" not in a[19:] and "Z" not in a else ""))
        t2 = dt.datetime.fromisoformat(b.replace("Z", "+00:00")[:26] + ("+00:00" if "+" not in b[19:] and "Z" not in b else ""))
        return round((t2 - t1).total_seconds() / 3600, 2)
    except Exception:
        return None
def _iso(s):
    """ISO zaman damgasini saniye hassasiyetine indirip ofsetle dondurur."""
    m = re.match(r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", s or "")
    return dt.datetime.fromisoformat(m.group(1)) if m else None
def sure_saat(a, b):
    t1, t2 = _iso(a), _iso(b)
    return round((t2 - t1).total_seconds() / 3600, 2) if t1 and t2 and t2 >= t1 else None
_GORELI = re.compile(r"(\d+)\s*(dakika|saat|gün|hafta|ay)\s*içinde", re.I)
def goreli_saat(s):
    m = _GORELI.search(s or "")
    if not m: return None
    v = int(m.group(1)); b = m.group(2).lower()
    return round(v * {"dakika": 1 / 60, "saat": 1, "gün": 24, "hafta": 168, "ay": 720}[b], 2)

# ---------------------------------------------------------------- kaynaklar
def jsonl(desen):
    out = []
    for f in sorted(glob.glob(os.path.join(HAM, desen))):
        out += [json.loads(l) for l in open(f, encoding="utf-8") if l.strip()]
    return out

def ty_panel():
    yor, soru = {}, []
    for f in sorted(glob.glob(os.path.join(PANEL, "seller-144409-urun-degerlendirmeleri-*.xlsx"))):
        for r in list(openpyxl.load_workbook(f, read_only=True).worksheets[0].iter_rows(values_only=True))[1:]:
            ad, kat, mk, kod, tar, _, puan, metin = r[:8]
            anahtar = (kod, tar, puan, metin)
            if anahtar in yor: continue
            yor[anahtar] = {"kanal": "Trendyol", "kaynak": "panel", "tur": "yorum", "marka": marka(mk), "urun": ad_duz(ad), "urun_id": str(kod),
                            "grup": grup(ad, kat), "kategori": kat, "satici": "VitrA resmi mağaza", "resmi": True,
                            "puan": int(float(puan)) if puan else None, "metin": temiz(metin), "tarih": tarih(tar), "dogrulanmis": True}
    f = glob.glob(os.path.join(PANEL, "UrunSorulariniz_*.xlsx"))[0]
    for r in list(openpyxl.load_workbook(f, read_only=True).worksheets[0].iter_rows(values_only=True))[1:]:
        ad, mk, kod, statu, s, st, cvp, ct, dk = r[:9]
        soru.append({"kanal": "Trendyol", "kaynak": "panel", "tur": "soru", "marka": marka(mk), "urun": ad_duz(ad), "urun_id": str(kod), "grup": grup(ad),
                     "satici": "VitrA resmi mağaza", "resmi": True, "soru": temiz(s), "tarih": tarih(st), "cevap": temiz(cvp),
                     "cevaplayan": "VitrA resmi mağaza" if cvp else None, "cevap_saat": round(float(dk) / 60, 2) if dk not in (None, "") else None})
    return list(yor.values()), soru

def hb(desen, kaynak_ad):
    L = jsonl(desen)
    urun = {}
    for r in L:
        if not r.get("record_type") and r.get("sku"):
            urun[r["sku"]] = r
    yor, soru, gor = [], [], set()
    for r in L:
        t = r.get("record_type")
        if t not in ("review", "qna"): continue
        p = r.get("product") or {}
        u = urun.get(p.get("sku")) or {}
        mk = marka(p.get("brand") or u.get("brand"))
        ad = ad_duz(p.get("title") or u.get("title") or "")
        kat = (u.get("category") or "").split(">")[-1].strip()
        if t == "review":
            rv = r.get("review") or {}
            anahtar = (p.get("sku"), rv.get("created_at"), rv.get("content"))
            if anahtar in gor: continue
            gor.add(anahtar)
            sat = (r.get("merchant") or {}).get("name") or ""
            yor.append({"kanal": "Hepsiburada", "kaynak": kaynak_ad, "tur": "yorum", "marka": mk, "urun": ad, "urun_id": p.get("sku"), "url": p.get("url"),
                        "grup": grup(ad, kat), "kategori": kat, "satici": "VitrA resmi mağaza" if sat in RESMI_HB else sat, "resmi": sat in RESMI_HB,
                        "puan": rv.get("rating"), "metin": temiz(rv.get("content")), "tarih": tarih(rv.get("created_at")), "dogrulanmis": bool(rv.get("is_purchase_verified"))})
        else:
            q = r.get("question") or {}
            anahtar = (p.get("sku"), q.get("created_at"), q.get("content"))
            if anahtar in gor: continue
            gor.add(anahtar)
            cv = (r.get("answers") or [None])[0] or {}
            cvy = cv.get("merchant_name")
            soru.append({"kanal": "Hepsiburada", "kaynak": kaynak_ad, "tur": "soru", "marka": mk, "urun": ad, "urun_id": p.get("sku"), "url": p.get("url"),
                         "grup": grup(ad, kat), "soru": temiz(q.get("content")), "tarih": tarih(q.get("created_at")), "cevap": temiz(cv.get("answer")),
                         "cevaplayan": ("VitrA resmi mağaza" if cvy in RESMI_HB else cvy) if cv else None, "resmi": cvy in RESMI_HB,
                         "cevap_saat": sure_saat(cv.get("asked_at"), cv.get("answered_at")) if cv else None})
    return yor, soru

def ty(desen, kaynak_ad):
    L = jsonl(desen)
    urun = {r["productId"]: r for r in L if r.get("recordType") == "product"}
    yor, soru, gor = [], [], set()
    for r in L:
        t = r.get("recordType")
        if t not in ("review", "qna"): continue
        u = urun.get(r.get("productId")) or {}
        ad = ad_duz(r.get("productName") or u.get("name") or "")
        mk = marka(u.get("brand"))
        kid = r.get("reviewId") if t == "review" else r.get("qnaId")
        if (t, kid) in gor: continue
        gor.add((t, kid))
        ortak = {"kanal": "Trendyol", "kaynak": kaynak_ad, "marka": mk, "urun": ad, "urun_id": r.get("productId"), "url": r.get("productUrl"),
                 "grup": grup(ad, u.get("categoryName")), "kategori": u.get("categoryName")}
        if t == "review":
            yor.append(dict(ortak, tur="yorum", satici=u.get("sellerName"), resmi=False, puan=r.get("rating"), metin=temiz(r.get("text")),
                            tarih=tarih(r.get("reviewDate")), dogrulanmis=bool(r.get("verifiedPurchase"))))
        else:
            soru.append(dict(ortak, tur="soru", satici=r.get("sellerName") or u.get("sellerName"), resmi=False, soru=temiz(r.get("questionText")),
                             tarih=tarih(r.get("questionDate")), cevap=temiz(r.get("answerText")), cevaplayan=r.get("sellerName") or u.get("sellerName") if r.get("answerText") else None,
                             cevap_saat=goreli_saat(r.get("answerDate"))))
    return yor, soru

def main():
    Y, S = [], []
    for y_, s_ in (ty_panel(), hb("hb_vitra.jsonl", "sayfa"), hb("hb_rakip*.jsonl", "sayfa"),
                   ty("ty_rakip_*.jsonl", "sayfa"), ty("ty_marka_ek_*.jsonl", "sayfa"), ty("ty_vitra_qna_*.jsonl", "sayfa")):
        Y += y_; S += s_
    # Trendyol VitrA/Artema sorulari: panel kaydi varken ayni soru sayfadan da gelirse panel kaydi tutulur
    pk = {(s["soru"], s["tarih"]) for s in S if s["kaynak"] == "panel"}
    S = [s for s in S if s["kaynak"] == "panel" or (s["soru"], s["tarih"]) not in pk]
    # ayni yorum farkli dosyalardan gelirse tekillestir
    gor, Y2 = set(), []
    for y in Y:
        a = (y["kanal"], y["urun_id"], y["tarih"], y["metin"], y["puan"])
        if a in gor: continue
        gor.add(a); Y2.append(y)
    yol = os.path.join(veri.V, "islenmis", "yorum_kayit.json")
    json.dump({"yorum": Y2, "soru": S}, open(yol, "w", encoding="utf-8"), ensure_ascii=False)
    from collections import Counter
    print("kaydedildi:", yol, len(Y2), "yorum,", len(S), "soru")
    print(Counter((y["kanal"], y["marka"]) for y in Y2).most_common(25))
    print(Counter((s["kanal"], s["marka"]) for s in S).most_common(15))
    print("grup:", Counter(y["grup"] for y in Y2).most_common())

if __name__ == "__main__":
    main()
