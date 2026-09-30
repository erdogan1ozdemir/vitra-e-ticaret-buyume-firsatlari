# -*- coding: utf-8 -*-
"""Kaynak dokumu · G: pazaryeri alt kategori taramasi (30.09.2026, Chrome) - Trendyol, Hepsiburada, Akakce, Cimri, rakip magazalar."""
import json, os
from kaynak_ortak import *
from kaynak_veri_a import D30
P = os.path.join(DERIN, "pazaryeri_derin")
def L(f): return [json.loads(l) for l in open(os.path.join(P, f), encoding="utf-8")]
MAG = {"Koçtaş": "https://www.koctas.com.tr", "Bauhaus": "https://www.bauhaus.com.tr", "Banyomarka": "https://www.banyomarka.com", "Banyomega": "https://www.banyomega.com", "Banyoline": "https://www.banyoline.com", "Creavit (e-mağaza)": "https://shop.creavit.com.tr"}
Y = "tarayıcı (Chrome, kullanıcı oturumu)"
def _f(r):
    f = r.get("fiyat") or {}
    return ("medyan %s TL" % format(round(f["med"]), ",").replace(",", ".")) if f.get("med") else "fiyat bandı alınamadı"
def doldur():
    for r in L("ty_kategori.jsonl"):
        ekle("https://www.trendyol.com" + r["url"], "Trendyol %s kategorisi çok satan listesi (ilk 2 sayfa, %s)" % (r["kategori"], r["kapsam"].replace("_", " ")),
             "%d ürün okundu, kategori toplamı %s; %s; toplam değerlendirme %s; %d marka; VitrA/Artema %d ürün" % (r.get("n") or 0, r.get("toplam") or "-", _f(r), r.get("toplam_yorum") or "-", r.get("marka_sayisi") or 0, r.get("vitra_adet") or 0),
             bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], kodbolum=False)
    for r in L("hb_kategori.jsonl"):
        ekle("https://www.hepsiburada.com" + r["url"], "Hepsiburada %s kategorisi çok satan listesi (ilk 2 sayfa, %s)" % (r["kategori"], r["kapsam"].replace("_", " ")),
             "%d ürün okundu, kategori toplamı %s; %s; toplam değerlendirme %s; platform satış payı %s; VitrA/Artema %d ürün" % (r.get("n") or 0, r.get("toplam") or "-", _f(r), r.get("toplam_yorum") or "-", ("%%%s" % r["platform_pay"]) if r.get("platform_pay") is not None else "-", r.get("vitra_adet") or 0),
             bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], kodbolum=False)
    for r in L("akakce_kategori.jsonl"):
        k = r["kategori"]; url = "https://www.akakce.com/%s.html" % k
        ekle(url, "Akakçe %s kategori sayfası (popülerlik sırası, ilk 2 sayfa)" % k,
             "%d ürün okundu, kategori toplamı %s; %s; satıcı sayısı medyanı %s; VitrA/Artema %d ürün; marka filtresi ilk 15" % (r.get("n") or 0, r.get("toplam") or "-", _f(r), r.get("satici_sayisi_medyan") or "-", r.get("vitra_adet") or 0),
             bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], kodbolum=False)
    ekle("https://www.akakce.com/{kategori}.html?f=vitra", "Akakçe VitrA marka sayfaları (klozet, lavabo, klozet kapağı, banyo dolabı, rezervuar ve 3 kesit daha)", "8 marka sayfası, en popüler ilk 40 ürün (200 satır): ürün, en düşük fiyat, satıcı sayısı; klozet 309, lavabo 297, kapak 179, banyo dolabı 297, rezervuar 46 ürün", bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], adet=8, kodbolum=False)
    for r in L("cimri_kategori.jsonl"):
        k = r["kategori"]; url = "https://www.cimri.com/%s" % k
        ekle(url, "Cimri %s kategori sayfası (popülerlik sırası, ilk 2 sayfa)" % k,
             "%d ürün okundu, kategori toplamı %s; %s; satıcı sayısı medyanı %s; VitrA/Artema %d ürün; mağaza ve marka filtresi" % (r.get("n") or 0, r.get("toplam") or "-", _f(r), r.get("satici_sayisi_medyan") or "-", r.get("vitra_adet") or 0),
             bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], kodbolum=False)
    for r in L("rakip_magaza_kategori.jsonl"):
        m = r.get("magaza"); u = r.get("url")
        if m not in MAG or not u: continue
        url = u if u.startswith("http") else MAG[m] + u
        ekle(url, "%s %s kategori sayfası (%s)" % (m, r.get("kategori"), "çok satan sırası" if m == "Koçtaş" else "varsayılan sıralama, ilk sayfa"),
             "%d ürün okundu; %s; VitrA/Artema %d ürün; marka dağılımı: %s" % (r.get("n") or 0, _f(r), r.get("vitra_adet") or 0, (r.get("marka_dagilimi") or "-")[:90]),
             bolum=["derin"], yontem=Y, tarih=D30, kod=["D29"], kodbolum=False)
