# -*- coding: utf-8 -*-
"""Sikayetvar verisini temalara ayirir; aylik seri, alintilar, alt kirilimlar ve rakip tablosu uretir.
Girdi : veri/ham/derin/sikayetvar/{marka_vitra,marka_artema}.json, detay_*.jsonl, rakip_ham.json, konu.json
Cikti : sikayetler.json, temalar.json, aylik.json, rakip.json, alt_kirilim.json (ayni klasor)"""
import json, os, re, collections, statistics
import sikayetvar_tema as T
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
BASLANGIC, BITIS = "2024-10-01", "2026-09-29"   # son 24 ay (Eki 2024 - Eyl 2026)

def yukle(p, varsayilan=None):
    yol = os.path.join(D, p)
    if not os.path.exists(yol): return varsayilan
    return json.load(open(yol, encoding="utf-8"))

def detaylar(slug):
    yol = os.path.join(D, "detay_%s.jsonl" % slug)
    d = {}
    if os.path.exists(yol):
        for s in open(yol, encoding="utf-8"):
            j = json.loads(s); d[j["url"]] = j["metin_tam"]
    return d

def temizle(t):
    from sikayetvar_detay import temizle as tz
    return tz(t)

def ay_listesi():
    r = []; y, m = 2024, 10
    while (y, m) <= (2026, 9):
        r.append("%04d-%02d" % (y, m)); m += 1
        if m == 13: y, m = y + 1, 1
    return r

def hazirla(slug):
    d = yukle("marka_%s.json" % slug); det = detaylar(slug)
    out = []
    for x in d["sikayetler"]:
        r = {"marka": slug, "id": x["id"], "baslik": x["baslik"], "url": x["url"], "tarih": x["tarih"], "goruntulenme": x["goruntulenme"],
             "cozuldu": x["cozuldu"], "yildiz": x["yildiz"], "yayindan_kaldirildi": x["yayindan_kaldirildi"]}
        tam = det.get(x["url"])
        r["metin_kaynagi"] = "detay" if tam else "liste"
        r["metin"] = tam if tam else temizle(x["metin"] or "")
        if x["baslik"] and r["metin"] is not None:
            e, a, s = T.etiketle(x["baslik"], r["metin"])
        else:
            e, a = set(), None
        r["etiketler"] = sorted(e); r["ana_tema"] = a
        r["pencere"] = bool(x["tarih"] and BASLANGIC <= x["tarih"] <= BITIS)
        out.append(r)
    return d["bilgi"], out

# ---- alintilar ----
CUMLE = re.compile(r"(?<=[.!?])\s+|\n+")
ISIM = re.compile(r"\b(?:ben|adım|sayın|saygılar(?:ımla)?)\b[^.]{0,30}\b[A-ZÇĞİÖŞÜ][a-zçğıöşü]+\s+[A-ZÇĞİÖŞÜ]\*|\*{3,}|\[(?:e-posta|telefon|no)\]")

def alinti_adaylari(kayit, tema):
    rx = T.DERLI[tema]
    res = []
    for c in CUMLE.split(kayit["metin"] or ""):
        c = c.strip()
        if not (55 <= len(c) <= 230): continue
        if ISIM.search(c): continue
        k = T.kucuk(c)
        s = sum(len(r.findall(k)) for r in rx)
        if s: res.append((s, c))
    return res

NEG = re.compile(r"yok|değil|rağmen|reddet|çözüm|bulunam|gelmedi|gelmiyor|karşılık|mağdur|ödeme|ücret|talep|iade|olmadı|verilmedi|sunulmadı|yapılmadı|ilgilen|pişman|kırıl|çatla|su ")

def aday_listesi(liste, tema, k=12):
    aday = []
    for r in liste:
        if tema not in r["etiketler"] or not r["url"]: continue
        for s, c in alinti_adaylari(r, tema):
            neg = len(NEG.findall(T.kucuk(c)))
            aday.append((s + neg + (2 if r["ana_tema"] == tema else 0), r["goruntulenme"] or 0, c, r))
    aday.sort(key=lambda a: (-a[0], -a[1]))
    sec, kul = [], set()
    for s, g, c, r in aday:
        if r["url"] in kul: continue
        kul.add(r["url"]); sec.append({"metin": c, "url": r["url"], "tarih": r["tarih"], "puan": s})
        if len(sec) == k: break
    return sec

def alintilar(liste, tema, n=3):
    adaylar = aday_listesi(liste, tema, 40)
    secilen = yukle("alinti_secilen.json", {}).get(tema)
    if secilen:
        out = []
        for m in secilen:
            for a in adaylar:
                if a["metin"] == m: out.append({"metin": a["metin"], "url": a["url"], "tarih": a["tarih"]}); break
        if out: return out
    return [{"metin": a["metin"], "url": a["url"], "tarih": a["tarih"]} for a in adaylar[:n]]

# ---- alt kirilimlar ----
def sayim(liste, sozluk):
    c = {}
    for ad, rx in sozluk.items():
        c[ad] = sum(1 for r in liste if re.search(rx, T.kucuk(r["baslik"] + " " + (r["metin"] or ""))))
    return c

PARCA = {"Klozet kapağı, menteşe, vida, takoz": r"menteşe|kapak(?:ı|ın)? (?:vida|takoz)|kapak vidas|yavaş (?:kapan|açıl)|klozet kapa",
         "Rezervuar, şamandıra, kumanda paneli": r"rezervuar|şamandıra|şamandra|kumanda panel|buton|flatör|flush",
         "Batarya, kartuş, musluk parçası": r"kartuş|batarya|musluk|perlatör|taharet",
         "Duş başlığı, hortum, duş seti parçası": r"duş başlığ|hortum|duş seti|tepe duş|duş kolonu|el duşu",
         "Sifon, gider, sifon parçası": r"sifon|gider|süzgeç",
         "Ayna, dolap, çekmece, kapak menteşesi (mobilya)": r"banyo dolab|aynalı|çekmece|ayna\b|dolap"}
MONTAJ = {"Vitra servisi / yetkili servis montajı": r"servis(?:i|in)? montaj|montaj hizmet|vitra montaj|montaj ekib|montajcı|montaj personel|kurulum ekib|kurulum hizmet",
          "Kendi ustası / tesisatçı montajı": r"ustam|tesisatçı|kendi usta|usta(?:ya|ma)? taktır|ustaya",
          "Montaj randevusu, erteleme, gecikme": r"randevu|ertele|gelmedi|gelmiyor|geciktir|gecik",
          "Montaj ücreti / ek ücret": r"montaj (?:ücret|bedel|fiyat)|ücret(?:li)? montaj|montaj için .{0,20}(?:tl|ücret)",
          "Montaj hatası, hasar": r"montaj hata|yanlış (?:takıl|monte)|hasar|kırdı|çizdi|yanlış montaj|hatalı montaj"}
FIYAT = {"Servis ücreti, kontrol ücreti, haksız ücret": r"kontrol ücret|servis ücret|haksız ücret|aşırı ücret|fahiş|ücret talep|ücretli servis|ücret iste",
         "Parça / ürün fiyatı, pahalılık": r"pahalı|fiyat|zam\b",
         "Kampanya, indirim, taksit": r"kampanya|indirim|taksit|kupon|fiyat fark",
         "İade / para iadesi süresi ve bedeli": r"para iade|iade bedel|ücret iade|iade tutar"}
GUVEN = {"Tekrar almama, tavsiye etmeme": r"bir daha|asla|tavsiye etmiyorum|tavsiye etmem|kimseye|almayın|almayacağım|vazgeç|başka marka|marka değiş|pişman",
         "Marka güveni ile satın alma (güvenerek, kaliteli sanıp)": r"güvenerek|güvendim|güvenip|kaliteli (?:olduğunu|sanıp|diye)|marka(?:sına)? güven|sırf marka|isminden|ismine",
         "Tüketici hakem heyeti, hukuki süreç": r"tüketici hakem|hakem heyeti|tüketici mahkeme|dava|avukat|noter|ihtarname|ticaret bakanlığı|alo 175|bilirkişi|icra"}
PLAT = T.PLATFORMLAR; PER = T.PERAKENDE
def ana_sayilar(liste):
    return dict(collections.Counter(r["ana_tema"] for r in liste))

def tema_ozeti(liste, alintili=True):
    N = len(liste)
    out = {}
    for t in T.SIRA + ["diger"]:
        etk = [r for r in liste if t in r["etiketler"]] if t != "diger" else [r for r in liste if not r["etiketler"]]
        ana = [r for r in liste if r["ana_tema"] == t]
        ad = T.TEMALAR[t][0] if t != "diger" else "Diğer / sınıflandırılamayan"
        gor = [r["goruntulenme"] for r in etk if r["goruntulenme"]]
        out[ad] = {"kod": t, "sayi": len(etk), "pay": round(len(etk) / N, 4) if N else 0,
                   "ana_tema_sayi": len(ana), "ana_tema_pay": round(len(ana) / N, 4) if N else 0,
                   "cozuldu_pay": round(sum(r["cozuldu"] for r in etk) / len(etk), 4) if etk else None,
                   "medyan_goruntulenme": statistics.median(gor) if gor else None,
                   "alintilar": alintilar(liste, t) if (alintili and t != "diger") else []}
    return out

def aylik(tum):
    c = collections.Counter(r["tarih"][:7] for r in tum if r["tarih"])
    return {a: c.get(a, 0) for a in ay_listesi()}

if __name__ == "__main__":
    bv, V = hazirla("vitra"); ba, A = hazirla("artema")
    Vp = [r for r in V if r["pencere"]]; Ap = [r for r in A if r["pencere"]]
    Vm = [r for r in Vp if r["baslik"]]   # metni/basligi olan (yayindan kaldirilmayan)
    Am = [r for r in Ap if r["baslik"]]
    json.dump(V + A, open(os.path.join(D, "sikayetler.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    temalar = {"VitrA": {"kapsam": "Şikayetvar /vitra, %s - %s" % (BASLANGIC, BITIS), "toplam_pencere": len(Vp), "metinli": len(Vm),
                          "yayindan_kaldirilan": len(Vp) - len(Vm), "detay_metinli": sum(1 for r in Vm if r["metin_kaynagi"] == "detay"),
                          "temalar": tema_ozeti(Vm)},
               "Artema": {"kapsam": "Şikayetvar /artema, %s - %s" % (BASLANGIC, BITIS), "toplam_pencere": len(Ap), "metinli": len(Am),
                           "yayindan_kaldirilan": len(Ap) - len(Am), "detay_metinli": sum(1 for r in Am if r["metin_kaynagi"] == "detay"),
                           "temalar": tema_ozeti(Am)}}
    json.dump(temalar, open(os.path.join(D, "temalar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ay = {"VitrA": aylik(V), "Artema": aylik(A)}
    ay_tum = {"VitrA_tum_donem": dict(sorted(collections.Counter(r["tarih"][:7] for r in V if r["tarih"]).items())),
              "Artema_tum_donem": dict(sorted(collections.Counter(r["tarih"][:7] for r in A if r["tarih"]).items()))}
    json.dump(ay["VitrA"], open(os.path.join(D, "aylik.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({**ay, **ay_tum}, open(os.path.join(D, "aylik_ek.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    def alt(L):
        ec = [r for r in L if "pazaryeri" in r["etiketler"] or "vitra_online" in r["etiketler"]]
        return {"n": len(L),
                "pazaryeri_platform": sayim(L, PLAT), "perakende_zincir": sayim(L, PER),
                "yedek_parca_parca_tipi": sayim([r for r in L if "yedek_parca" in r["etiketler"]], PARCA),
                "yedek_parca_n": sum(1 for r in L if "yedek_parca" in r["etiketler"]),
                "parca_tipi_tum_sikayet": sayim(L, PARCA),
                "montaj_alt": sayim([r for r in L if "montaj" in r["etiketler"]], MONTAJ), "montaj_n": sum(1 for r in L if "montaj" in r["etiketler"]),
                "fiyat_alt": sayim(L, FIYAT), "guven_tekrar_alim": sayim(L, GUVEN),
                "eticaret_kanali_n": len(ec),
                "siparis_teslimat_iade_genel": sum(1 for r in L if T.SIPARIS.search(T.kucuk(r["baslik"] + " " + r["metin"]))),
                "satis_sonrasi_birlesim_n": sum(1 for r in L if set(r["etiketler"]) & {"servis_garanti", "yedek_parca", "montaj", "iletisim"}),
                "cozuldu_n": sum(r["cozuldu"] for r in L)}
    json.dump({"VitrA": alt(Vm), "Artema": alt(Am)}, open(os.path.join(D, "alt_kirilim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({t: aday_listesi(Vm, t, 12) for t in T.SIRA}, open(os.path.join(D, "alinti_adaylari.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("VitrA pencere", len(Vp), "metinli", len(Vm), "detay", temalar["VitrA"]["detay_metinli"])
    for k, v in temalar["VitrA"]["temalar"].items(): print("  %-45s %4d %5.1f%%  ana %4d %5.1f%%" % (k, v["sayi"], 100 * v["pay"], v["ana_tema_sayi"], 100 * v["ana_tema_pay"]))
    print("Artema pencere", len(Ap), "metinli", len(Am))
    for k, v in temalar["Artema"]["temalar"].items(): print("  %-45s %4d %5.1f%%  ana %4d %5.1f%%" % (k, v["sayi"], 100 * v["pay"], v["ana_tema_sayi"], 100 * v["ana_tema_pay"]))
