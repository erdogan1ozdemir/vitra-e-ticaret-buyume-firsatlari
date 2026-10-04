# -*- coding: utf-8 -*-
"""Genisletilmis SERP seti (04.10.2026): A VitrA gami (her alt kategoriye en az bir bas kelime), B yakin kategori firsatlari, C marka ve karsilastirma.
Hacim: Keyword Planner ortalama (Eyl 2025 - Agu 2026); hacmi olmayan kelime alinmaz. Cikti: veri/ham/derin/serp/set_v2.json"""
import json, os, re, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import veri, dfs
from serp_kelimeler import LISTE as ESKI
K = veri.KELIME; Y = json.load(open(os.path.join(veri.V, "islenmis", "yeni_kategori.json"), encoding="utf-8"))
CAN = veri.kanonik()
MARKA = re.compile(r"(özdilek|\b(?:vitra|artema|kale|creavit|eca|e\.c\.a|serel|geberit|grohe|hansgrohe|duravit|roca|ideal standard|bien|turkuaz|bocchi|newarc|isvea|visam|turavit|franke|tema|nkp|villeroy|toto|orka|koçtaş|ikea|bauhaus|tekzen|trendyol|hepsiburada|n11|amazon|ihlas|özdilek|teka|bosch|tefal|aceser|nila|itimat|bianca|stella|isonem|skip hop|bıçaklı|çimstone)\b)")
DIS_ESKI = {"havlupan", "elektrikli havlupan", "su arıtma cihazı", "termosifon", "şofben", "banyo paspası", "mutfak tezgahı", "çamaşır sepeti", "bornoz", "derz dolgu", "bebek küveti", "seramik yapıştırıcı", "banyo lambası", "granit evye", "evye", "arıtmalı batarya", "tesisatçı"}
RAKIP_ESKI = {"geberit gömme rezervuar", "creavit klozet", "grohe batarya", "kale klozet"}
VITRA_ESKI = {"vitra klozet", "vitra banyo dolabı", "vitra gömme rezervuar", "vitra lavabo", "artema batarya"}
set_ = collections.OrderedDict()
_TRF = str.maketrans("çğıöşüâÇĞİÖŞÜ", "cgiosuaCGIOSU")
def norm(k_):
    w = k_.translate(_TRF).split()
    return " ".join(w[:-1] + [w[-1][:4]]) if w else k_
_NG = set()
def ekle(kw, grup, tema, alt=None):
    kw = CAN.get(kw, kw)
    if kw in set_ or (grup != "A" and norm(kw) in _NG): return
    set_[kw] = {"kw": kw, "grup": grup, "tema": tema, "alt": alt}; _NG.add(norm(kw))
# ---- A: VitrA gami
k2 = collections.defaultdict(list)
for r in K:
    if not r["markali"] and not MARKA.search(r["kw"]): k2[(r["k1"], r["k2"])].append(r)
tot = sum(r["a26"] for (a, _), L in k2.items() if a != "Karo Seramik Ürünleri" for r in L)
kat_es = {}
for (a, b), L in k2.items():
    for r in L: kat_es[r["kw"]] = (a, b)
HARIC_K2 = {"Eviyeler"}   # VitrA gaminda evye bulunmuyor (Bolum 12): B grubunda
for kw, t in ESKI:   # mevcut setin VitrA gamindaki kelimeleri korunur
    kw = CAN.get(kw, kw)
    if kw in DIS_ESKI or kw in RAKIP_ESKI or kw in VITRA_ESKI or kw == "tesisatçı": continue
    a, b = kat_es.get(kw, (None, None))
    if t in ("Soru", "Hizmet"): ekle(kw, "A", "Soru ve karar" if t == "Soru" else "Hizmet ve ilham", b)
    elif a: ekle(kw, "A", a, b)
    else: ekle(kw, "A", {"SSG": "Vitrifiyeler", "BM": "Banyo Mobilyaları", "Armatür-duş": "Armatürler", "Yıkanma": "Yıkanma Alanları", "Karo": "Karo Seramik Ürünleri", "Bitişik": "Vitrifiyeler"}.get(t, t), None)
for (a, b), L in sorted(k2.items(), key=lambda i: -sum(r["a26"] for r in i[1])):
    if b in HARIC_K2 or a == "Karo Seramik Ürünleri": continue
    pay = sum(r["a26"] for r in L) / tot
    hedef = max(1, min(8, round(pay * 180)))
    var = sum(1 for v in set_.values() if v["grup"] == "A" and v["alt"] == b)
    for r in sorted(L, key=lambda r: -r["a26"]):
        if var >= hedef: break
        if r["a26"] < 30 or r["kw"] in set_: continue
        ekle(r["kw"], "A", a, b); var += 1
# ---- B: yakin kategori firsatlari (VitrA gaminda olmayan ya da kismi temalar)
for tk, t in sorted(Y["tema"].items(), key=lambda i: -i[1]["v12"]):
    if t["durum"] == "Var" or t["grup"] not in ("Bitişik", "Hizmet-Set", "Yıkanma", "SSG", "Armatür-Duş", "BM"): continue
    if tk in ("montaj_hiz", "ilham", "tasarim", "tadilat", "set", "yedek", "banyo_raf", "taharet_musluk", "aydinlatma", "suzgec"): continue   # VitrA'da karsiligi olan ya da A grubunda temsil edilen temalar
    n = 6 if t["v12"] > 200000 else (4 if t["v12"] > 40000 else (3 if t["v12"] > 8000 else 2))
    alin = 0
    for kw, v, _ in t["top"]:
        if alin >= n: break
        if MARKA.search(kw) or v < 50 or kw in set_: continue
        ekle(kw, "B", t["tr"], tk); alin += 1
_BT = {"havlupan": "Havlupan ve banyo radyatörü", "elektrikli havlupan": "Havlupan ve banyo radyatörü", "su arıtma cihazı": "Su arıtma cihazı", "termosifon": "Şofben, termosifon ve su ısıtıcı",
       "şofben": "Şofben, termosifon ve su ısıtıcı", "banyo paspası": "Banyo tekstili (havlu, bornoz, paspas, perde)", "bornoz": "Banyo tekstili (havlu, bornoz, paspas, perde)",
       "mutfak tezgahı": "Mutfak tezgahı", "çamaşır sepeti": "Banyo düzenleme ve depolama", "derz dolgu": "Yapıştırıcı, derz ve su yalıtımı", "seramik yapıştırıcı": "Yapıştırıcı, derz ve su yalıtımı",
       "bebek küveti": "Çocuk ve bebek banyo ürünleri", "banyo lambası": "Banyo aydınlatması ve ışıklı ayna", "granit evye": "Mutfak evyesi (granit, çelik, akıllı)", "evye": "Mutfak evyesi (granit, çelik, akıllı)",
       "arıtmalı batarya": "Arıtmalı ve filtreli batarya"}
for kw in DIS_ESKI - {"tesisatçı"}:
    if kw not in set_: ekle(kw, "B", _BT.get(kw, "Diğer"), None)
# ---- C: marka ve karsilastirma
mk = collections.defaultdict(list)
src = {r["kw"]: r["a26"] for r in K}
U = json.load(open(os.path.join(veri.V, "ham", "kfk_evren.json"), encoding="utf-8"))["kelimeler"]
for k_, d_ in U.items():
    if k_ not in src and isinstance(d_, dict) and d_.get("hacim"): src[k_] = d_["hacim"]
MK = {"VitrA": ["vitra"], "Artema": ["artema"], "E.C.A.": ["eca"], "Kale": ["kale"], "Serel": ["serel"], "Creavit": ["creavit"], "Visam": ["visam"], "Turkuaz": ["turkuaz"],
      "Grohe": ["grohe"], "Geberit": ["geberit"], "Bien": ["bien"], "Orka": ["orka"], "Bocchi": ["bocchi"], "Duravit": ["duravit"], "IKEA": ["ikea"], "Koçtaş": ["koçtaş"]}
URUN = re.compile(r"klozet|lavabo|rezervuar|batarya|duş|banyo dolab|iç takım|kapağ|musluk|seramik|fayans|vitrifiye|küvet|duşakabin|akıllı")
for m, al in MK.items():
    L = sorted([(v, k_) for k_, v in src.items() if any(re.search(r"(?<![a-zçğıöşü])" + a + r"(?![a-zçğıöşü])", k_) for a in al) and URUN.search(k_) and v], reverse=True)
    n = 16 if m == "VitrA" else (5 if m == "Artema" else (2 if m in ("IKEA", "Koçtaş") else 3))
    gor = set()
    for v, k_ in L:
        if len(gor) >= n: break
        k_ = CAN.get(k_, k_); kok = re.sub(r"\s+(fiyatları|fiyat|modelleri|fiyatı)$", "", k_)
        if kok in gor or k_ in set_ or norm(k_) in _NG or "mutfak dolab" in k_: continue
        gor.add(kok); ekle(k_, "C", "VitrA ve Artema" if m in ("VitrA", "Artema") else ("Perakendeci adıyla" if m in ("IKEA", "Koçtaş") else "Rakip marka"), m)
KARS = ["vitra mı eca mı", "vitra mı artema mı", "kale mi vitra mı", "vitra mı serel mi", "vitra mı creavit mi", "vitra mı geberit mi", "vitra mı turkuaz mı", "vitra mı duravit mi",
        "grohe mi vitra mı", "vitra ve artema aynı mı", "vitra ile artema arasındaki fark", "artema mı eca mı", "artema mı grohe mi", "eca mı creavit mi", "serel mi creavit mi",
        "en iyi klozet markası", "en iyi asma klozet markası", "en iyi klozet kapağı markası", "en iyi banyo dolabı markaları", "en iyi banyo batarya markası", "en iyi musluk batarya markası",
        "en iyi gömme rezervuar markaları", "en iyi vitrifiye markaları", "en kaliteli vitrifiye markaları", "hangi klozet markası iyi", "klozet markaları", "kaliteli klozet markaları",
        "banyo batarya markaları", "kaliteli banyo dolabı markaları", "banyo dolabı markaları", "türk vitrifiye markaları", "vitrifiye markaları", "artema türk malı mı",
        "vitra artema yedek parça", "vitra artema yetkili servis"]
for k_ in KARS: ekle(k_, "C", "Karşılaştırma ve marka seçimi", None)
# ---- hacim: Keyword Planner (Eyl 2025 - Agu 2026 ortalamasi), hacmi olmayan cikarilir
kws = list(set_)
H = {}
for i in range(0, len(kws), 700):
    r = dfs.post("/v3/keywords_data/google_ads/search_volume/live", [{"location_code": 2792, "language_code": "tr", "date_from": "2025-09-01", "date_to": "2026-08-31", "keywords": kws[i:i + 700], "search_partners": False}])
    t = r["tasks"][0]; print("KP", t["status_message"], t.get("cost"))
    for res in t.get("result") or []:
        ms = [m["search_volume"] for m in (res.get("monthly_searches") or []) if m.get("search_volume") is not None]
        H[res["keyword"]] = {"hacim": res.get("search_volume"), "ort12": round(sum(ms) / len(ms)) if ms else None}
cikan = [k_ for k_ in kws if not (H.get(k_) or {}).get("ort12")]
for k_ in cikan: set_.pop(k_)
for k_, v in set_.items(): v["hacim"] = H[k_]["ort12"]
json.dump({"tarih": "2026-10-04", "kelimeler": list(set_.values()), "hacimsiz_cikan": cikan}, open(os.path.join(veri.V, "ham", "derin", "serp", "set_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
c = collections.Counter(v["grup"] for v in set_.values()); print(c, "hacimsiz cikan", len(cikan), cikan[:30])
