# -*- coding: utf-8 -*-
"""Kaynak dokumu · E: fiyat ve satici manzarasi (vitra.com.tr urun sayfalari, Koctas, Akakce, Cimri)."""
import os, json, csv
from kaynak_ortak import *
from kaynak_veri_a import D28, D29, D30
from kaynak_veri_c import fs

CHR = "tarayıcı (Chrome, kullanıcı oturumu)"

KAT = {"banyo-aynasi": "banyo aynası", "banyo-bataryasi": "banyo bataryası", "banyo-dolabi": "banyo dolabı", "dus-seti": "duş seti", "dusakabin": "duşakabin", "klozet-kapagi": "klozet kapağı",
       "lavabo-bataryasi": "lavabo bataryası", "rezervuar-aksesuari": "rezervuar aksesuarı", "gomme-rezervuar": "gömme rezervuar", "klozet": "klozet", "lavabo": "lavabo", "rezervuar": "rezervuar", "musluk": "musluk"}

def tl(x):
    return "%s TL" % fs(round(x, 2) if isinstance(x, float) and not float(x).is_integer() else int(x)) if x is not None else "-"

def doldur():
    pf = os.path.join(DERIN, "pazaryeri_fiyat")
    urun = json.load(open(os.path.join(pf, "urun_fiyat.json"), encoding="utf-8"))
    for r in urun:
        ozet = ["kod %s" % r["kod"], "liste fiyatı %s" % tl(r["vitra_com_tr"])]
        if r.get("vitra_sepette"):
            ozet.append("sepette %s" % tl(r["vitra_sepette"]))
        ozet.append(r["vitra_stok"])
        if r.get("en_ucuz_kanal"):
            ozet.append("en düşük liste fiyatı %s (%s)" % (tl(r["en_ucuz_fiyat"]), r["en_ucuz_kanal"]))
        ekle(r["vitra_url"], "VitrA ürün sayfası: %s (kanal fiyat karşılaştırması için vitra.com.tr liste ve sepet fiyatı, stok)" % r["urun"],
             "; ".join(ozet) + "; Trendyol, Hepsiburada ve Koçtaş liste fiyatlarıyla 4 kanalda karşılaştırıldı",
             bolum=["fiyat"], yontem=["curl", "tarayıcı (Playwright)"], tarih=D29, kod=["D26"])
        if r.get("koctas_url"):
            ekle(r["koctas_url"], "Koçtaş ürün sayfası: %s (kanal fiyat karşılaştırması için Koçtaş liste ve sepet fiyatı)" % r["urun"],
                 "Koçtaş liste fiyatı %s%s; satıcı: %s%s" % (tl(r["koctas"]), (", sepette %s" % tl(r["koctas_sepette"])) if r.get("koctas_sepette") else "", r.get("koctas_satici") or "-",
                                                         "; ürün sayfasında montaj hizmeti satın alınabiliyor" if r.get("koctas_montaj_satin_al") else ""),
                 bolum=["fiyat"], yontem="tarayıcı (Playwright)", tarih=D29, kod=["D26"])
    ekle("https://www.hepsiburada.com/{ürün-adı}-pm-{HBC-kodu}", "Hepsiburada ürün sayfaları: 29 VitrA ve Artema SKU'sunun buybox, satıcı ve kampanya fiyatı",
         "29 SKU için arama ve satıcı listesi (6 parti); buybox satıcısı, VitrA mağazası, en düşük diğer satıcı, kampanya fiyatı",
         bolum=["fiyat"], yontem="tarayıcı (Playwright)", tarih=D29, kod=["D26"], adet=29, href="https://www.hepsiburada.com/vitra-integra-7041b003-0090-rim-ex-asma-klozet-54-cm-beyaz-pm-HBC00003RQ1FQ")

    # ------------------------------------------------------------ Akakce
    fm = os.path.join(DERIN, "fiyat_manzarasi", "chrome")
    ekle("https://www.akakce.com", "Akakçe fiyat karşılaştırma: arama, ürün ve kategori sayfaları (satıcı listesi ve kategori fiyat bandı)",
         "29 SKU'nun 24'ü eşleşti (arama, kod eşleşen ürün sayfası, satıcı listesi); 12 kategori sayfası; satıcı medyanı 8 (1-68); en düşük fiyat 19 üründe vitra.com.tr listesinin altında (fark medyanı %21,3; armatürde %36-50), 5 üründe vitra.com.tr daha düşük ya da eşit; Trendyol yalnız 1 üründe listeli",
         bolum=["fiyat"], yontem=["API (DataForSEO SERP özeti)", CHR], tarih=[D29, D30], kod=["D25", "D27"])
    ak = [json.loads(l) for l in open(os.path.join(fm, "akakce_urun.jsonl"), encoding="utf-8") if l.strip()]
    ekle("https://www.akakce.com/{kategori}/en-ucuz-{ürün-adı},{ürün-no}.html", "Akakçe ürün sayfaları: VitrA ve Artema SKU'ları için satıcı listesi ve en düşük fiyat",
         "24 ürün sayfası (29 SKU'dan eşleşen); satıcı, mecra, fiyat, kargo ve stok bilgisi (liste ilk 16 satıcıyla sınırlı); eşleşme doğruluğu için eşleşme ürün adresi slug'ından yapıldı",
         bolum=["fiyat"], yontem=CHR, tarih=D30, kod=["D27"], adet=len(ak), href=ak[0]["url"])
    for l in open(os.path.join(fm, "akakce_kategori.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if not r.get("url"):
            continue
        toplam = ("Kategoride %s ürün; " % fs(r["toplam"])) if r.get("toplam") else ""
        ekle(r["url"], "Akakçe %s kategori sayfası: ilk %d ürünün fiyat bandı ve marka dağılımı" % (KAT.get(r["kat"], r["kat"]), r["n"]),
             "%silk %d ürünün fiyatı en düşük %s, medyan %s, en yüksek %s TL; VitrA ilk %d ürünün %d'inde; markalar: %s" % (
                 toplam, r["n"], fs(round(r["min"])), fs(round(r["medyan"])), fs(round(r["maks"])), r["n"], r.get("vitra_n", 0), ", ".join(r.get("markalar", [])[:5])),
             bolum=["fiyat"], yontem=CHR, tarih=D30, kod=["D27"])

    # ------------------------------------------------------------ Cimri
    ct = [json.loads(l) for l in open(os.path.join(DERIN, "chrome_tur2", "cimri_teklif.jsonl"), encoding="utf-8") if l.strip()]
    ct = [r for r in ct if r.get("s")]
    ekle("https://www.cimri.com", "Cimri fiyat karşılaştırma: kategori, marka ve ürün sayfaları (satıcı teklifleri)",
         "Arama sayfası doğrulama katmanı nedeniyle açılamadı; kategori ve marka sayfaları okundu; 19 SKU için 110 teklif (idefix 39, PttAVM 27, Hepsiburada 21, Koçtaş 10, n11 5, Trendyol 4, Amazon 3); vitra.com.tr liste fiyatına göre en düşük teklif farkı medyanı -%14,8 (17 SKU); 10 SKU eşleşmedi",
         bolum=["fiyat"], yontem=["API (DataForSEO SERP özeti)", CHR], tarih=[D29, D30], kod=["D25", "D27", "D28"])
    ekle("https://www.cimri.com/{kategori}/en-ucuz-{ürün-adı}-fiyatlari,{ürün-no}", "Cimri ürün sayfaları: VitrA ve Artema SKU'ları için satıcı teklif listesi",
         "%d ürün sayfası, 110 teklif; mecra, satıcı, fiyat, kargo ve kupon kodlu fiyat; 10'dan fazla teklifte 'fiyat teklifini gör' düğmesiyle liste genişletildi" % len(ct),
         bolum=["fiyat"], yontem=CHR, tarih=D30, kod=["D28"], adet=len(ct), href=ct[0]["url"])
    ekle("https://www.cimri.com/{marka}-{kategori}?page={n}", "Cimri marka ve kategori liste sayfaları: SKU eşleştirme için derin sayfa taraması",
         "46 liste sayfası: VitrA klozet ve asma klozet 1-3, lavabo 1-7, banyo dolabı 1-6, rezervuar 1-4; Artema lavabo bataryası 1-8, banyo bataryası 1-5, ankastre banyo bataryası 1-3, duş seti 1-4, ara musluk 1-2; bu sayfalardan 9 SKU daha eşleşti",
         bolum=["fiyat"], yontem=CHR, tarih=D30, kod=["D28"], adet=46, href="https://www.cimri.com/klozet")
    for l in open(os.path.join(fm, "cimri_kategori.jsonl"), encoding="utf-8"):
        r = json.loads(l)
        if not r.get("url"):
            continue
        ekle(r["url"], "Cimri %s kategori sayfası: ilk %d ürünün fiyat bandı, marka ve mağaza sırası" % (KAT.get(r["kat"], r["kat"]), r["n"]),
             "Kategoride %s ürün; ilk %d ürünün fiyatı en düşük %s, medyan %s, en yüksek %s TL; marka sırası: %s; mağaza sırası: %s" % (
                 fs(r["toplam"]), r["n"], fs(round(r["min"])), fs(round(r["medyan"])), fs(round(r["maks"])), r.get("markalar_sira", "-"), ", ".join((r.get("magazalar_sira") or "").split(", ")[:5])),
             bolum=["fiyat"], yontem=CHR, tarih=D30, kod=["D27"])
