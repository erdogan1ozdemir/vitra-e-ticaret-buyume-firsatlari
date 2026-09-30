# -*- coding: utf-8 -*-
"""Kaynak dokumu · H: alt kategori tamamlayici taramasi (30.09.2026, Chrome) - vitra.com.tr kategori sayfalari, Trendyol, Hepsiburada, Akakce, Cimri ve rakip magaza aramalari (57 kesit)."""
import json, os, re
from urllib.parse import quote
from kaynak_ortak import *
from kaynak_veri_a import D30
P = os.path.join(DERIN, "pazaryeri_derin2")
def L(f): return [json.loads(l) for l in open(os.path.join(P, f), encoding="utf-8")]
K = L("kesitler.jsonl"); VS = L("vitra_site_kategori.jsonl")
Y = "tarayıcı (Chrome, kullanıcı oturumu)"
MAGURL = {"koctas": ("Koçtaş", "https://www.koctas.com.tr/search?q=%s&sort=bestseller-desc", "çok satan sırası"), "bauhaus": ("Bauhaus", "https://www.bauhaus.com.tr/search?q=%s", "alaka sırası"),
          "banyomarka": ("Banyomarka", "https://www.banyomarka.com/arama?q=%s", "arama sırası"), "banyomega": ("Banyomega", "https://www.banyomega.com/arama?q=%s", "arama sırası"),
          "banyoline": ("Banyoline", "https://www.banyoline.com/Arama?1&kelime=%s", "arama sırası"), "creavit": ("Creavit (e-mağaza)", "https://shop.creavit.com.tr/search?type=product&q=%s", "arama sırası")}
def _f(o):
    f = (o or {}).get("fiyat") or {}
    return ("medyan %s TL" % format(round(f["medyan"]), ",").replace(",", ".")) if f.get("medyan") else "fiyat medyanı alınamadı"
def _v(o): return (o or {}).get("vitra_adet")
def doldur():
    for r in VS:
        yol = r["yol"]; url = "https://www.vitra.com.tr" + yol
        if r.get("urun") is None:
            ekle(url, "vitra.com.tr %s sayfası" % yol, "sayfa yönlendirme döngüsü verdi (ERR_TOO_MANY_REDIRECTS); sitemap'te listeleniyor", bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False); continue
        if "kesit" in r:
            ekle(url, "vitra.com.tr %s kategori sayfası (%s)" % (r.get("baslik") or yol, r["kesit"]),
                 "%d varyant kartı; liste fiyatı %s - %s TL; stoklu %s, stokta yok %s; ilk sayfada Sepette indirim etiketi %s/%s; ücretsiz montaj listesinde %s ürün" % (r["urun"], format(r.get("fiyat_min") or 0, ",").replace(",", "."), format(r.get("fiyat_max") or 0, ",").replace(",", "."), r.get("stoklu") or 0, r.get("stokta_yok") or 0, r.get("ilk_sayfa_sepet_indirimli") or 0, r.get("ilk_sayfa_n") or 0, r.get("ucretsiz_montaj_liste") or 0),
                 bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
        else:
            ekle(url, "vitra.com.tr %s özel listesi" % yol, "%d varyant; kategori dağılımı ve kampanya etiketi oranları okundu" % r["urun"], bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
    for k in K:
        a = k["alt_kategori"]; q = k["arama_ifadesi"]
        t = k.get("ty")
        if t and t.get("okunan"):
            ekle("https://www.trendyol.com" + t["u"], "Trendyol \"%s\" araması, çok satan sıralı ilk sayfa (%s)" % (q, a), "%d ürün okundu, %d eşleşen; toplam %s; %s; VitrA/Artema %s ürün" % (t["okunan"], t.get("eslesen") or 0, t.get("total") or "-", _f(t), _v(t) or 0), bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
        hb = k.get("hb")
        if hb and hb.get("okunan"):
            ekle("https://www.hepsiburada.com" + hb["u"], "Hepsiburada \"%s\" araması, çok satan sıralı ilk sayfa (%s)" % (q, a), "%d ürün okundu, %d eşleşen; toplam %s; %s; VitrA/Artema %s ürün; satıcı sayısı %s" % (hb["okunan"], hb.get("eslesen") or 0, hb.get("total") or "-", _f(hb), _v(hb) or 0, hb.get("satici_sayisi") or "-"), bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
        ak = k.get("akakce")
        if ak and ak.get("okunan") and ak.get("url"):
            ekle("https://www.akakce.com" + ak["url"], "Akakçe \"%s\" %s (%s)" % (q, "kategori sayfası" if not ak["url"].startswith("/arama") else "araması", a), "%d ürün okundu, %d eşleşen; %s; satıcı sayısı medyanı %s; VitrA/Artema %s ürün" % (ak["okunan"], ak.get("eslesen") or 0, _f(ak), ak.get("satici_medyan") or "-", _v(ak) or 0), bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
        ci = k.get("cimri")
        if ci and ci.get("okunan") and ci.get("url"):
            ekle("https://www.cimri.com" + ci["url"], "Cimri \"%s\" araması (%s)" % (q, a), "%d ürün okundu, %d eşleşen; %s; satıcı sayısı medyanı %s; VitrA/Artema %s ürün" % (ci["okunan"], ci.get("eslesen") or 0, _f(ci), ci.get("satici_medyan") or "-", _v(ci) or 0), bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
        for c, o in (k.get("magazalar") or {}).items():
            if c not in MAGURL or not o or not o.get("okunan"): continue
            ad, tpl, sira = MAGURL[c]
            ekle(tpl % quote(q), "%s \"%s\" araması (%s, %s)" % (ad, q, a, sira), "%d ürün okundu, %d eşleşen; %s; VitrA/Artema %s ürün; marka dağılımı: %s" % (o["okunan"], o.get("eslesen") or 0, _f(o), _v(o) if _v(o) is not None else "-", (o.get("marka_str") or "-")[:90]), bolum=["derin"], yontem=Y, tarih=D30, kod=["D30"], kodbolum=False)
    Y2 = "satıcı paneli dışa aktarımı (kullanıcı tarafından iletildi)"
    ekle("https://partner.trendyol.com", "Trendyol satıcı paneli (VitrA resmi mağazası): satış, sipariş dağılımı, mağaza, operasyon, favori-görüntüleme, ürün ve satıcı değerlendirmeleri, ürün ve sipariş soruları, Trendyol'un Enleri",
         "Çeyreklik net adet, iptal, iade, indirim ve komisyon oranları; müşteri profili; ürün görüntülenme ve dönüşüm; 1.023 ürün ve 149 satıcı değerlendirmesi; 352 ürün sorusu; 9 kategori × 5 liste Enleri (Eylül 2026). Ciro tutarı rapora alınmadı",
         bolum=["panel"], yontem=Y2, tarih=D30, kod=["D31"], kodbolum=False)
    ekle("https://merchant.hepsiburada.com", "Hepsiburada satıcı paneli: ürün performansı (hak ediş), görüntülenme, iptal ve değerlendirme raporları",
         "Komisyon, kargo, hizmet bedeli ve kampanya indirimi oranları; 949 SKU görüntülenme ve dönüşüm; 369 iptal nedeni; 204 SKU değerlendirme",
         bolum=["panel"], yontem=Y2, tarih=D30, kod=["D31"], kodbolum=False)
    Y3 = "web araştırması (sayfa okuma)"
    for url_, amac_, bilgi_ in [
        ("https://www.aa.com.tr/tr/gundem/turkiyede-ortalama-hane-halki-buyuklugu-2024te-3-11-oldu/3566979", "TÜİK ADNKS hane sayısı (banyo yenileme tahmini)", "2024 hane sayısı 26.599.261, ortalama hane büyüklüğü 3,11"),
        ("https://www.aa.com.tr/tr/ekonomi/turkiyede-2025te-1-milyon-688-bin-910-konut-satildi/3804701", "TÜİK 2025 konut satışları", "1.688.910 konut; ilk el 540.786, ikinci el 1.148.124"),
        ("https://www.serfed.com/uyelerimiz/sersa", "Seramik sağlık gereçleri üretim ve kapasite (SERSA)", "2021-2023 üretim 22-25-21 milyon adet, kapasite 35-37,8 milyon, ihracat adetleri"),
        ("https://www.aa.com.tr/tr/ekonomi/seramik-sektorunun-2024-ihracat-hedefi-2-milyar-dolar/3139333", "Seramik sektörü 2023 ihracatı", "Seramik sağlık gereci ihracatı 7,7 milyon adet, 312 milyon dolar"),
        ("https://www.newsfilecorp.com/release/130362/Leading-Ceramics-Producer-VitrA-Sets-Sights-on-Thriving-US-Market", "VitrA pazar payı beyanı", "Türkiye seramik sağlık gereçleri pazarında %30 pay (2022; tanım belirtilmemiş)"),
        ("https://www.eczacibasi.com.tr/en/field-of-activity/building-products", "Eczacıbaşı Yapı Ürünleri kapasitesi", "Seramik sağlık gereci 6,7 milyon, armatür 2 milyon, banyo mobilyası 795 bin adet/yıl"),
        ("https://www.sanitaerwirtschaft.de/markt-branche/die-deutschen-und-ihre-baeder", "Almanya banyo yenileme benchmark (VDS-Forsa)", "46,2 milyon banyo; yenilenmemiş banyoların ortalama yaşı 19,5 yıl")]:
        ekle(url_, amac_, bilgi_, bolum=["makro"], yontem=Y3, tarih=D30, kod=["D32"], kodbolum=False)
