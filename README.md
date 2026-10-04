# VitrA Türkiye · E-Ticaret Büyüme Fırsatları

VitrA'nın Türkiye e-ticaret kanalları (vitra.com.tr, Trendyol, Hepsiburada) için büyüme fırsatları çalışması. Rapor tek HTML dosyasıdır; Türkçe ve İngilizce sürüm aynı dosyada, üst bardaki EN / TR düğmesiyle değişir. Excel veri dosyası rapora gömülüdür ve üst bardan indirilebilir.

- Rapor: `VitrA_E-Ticaret_Buyume_Firsatlari.html`
- Veri dosyası: `VitrA_E-Ticaret_Buyume_Firsatlari.xlsx` (88 sekme)
- Kaynak siteler dökümü: `VitrA_E-Ticaret_Kaynak_Siteler.xlsx` (1.292 satır, 75 alan adı; URL, ne için bakıldı, hangi bölüme kaynak sağladı, hangi bilgiler alındı, erişim tarihi, rapordaki kaynakça numarası; ayrıca alan adı özeti ve raporun Yöntem ve Kapsam tablosu)

## Kapsam (Sürüm 6 · 30.09.2026)

| Küme | Bölümler |
|---|---|
| Durum | Özet · Makro ortam ve ödeme gücü (TCMB EVDS) |
| Talep | Kategori talebi · SSG ve BM derin talep (48 ay, ürün tipi ve özellik) · İhtiyaç dili · Organik kanal (GSC, alan adı düzeyi) · Marka aramaları ve autocomplete · Google arama sonuçları ve AI Overview (109 kelime) · YouTube (68 arama, kanal türü, 2.218 yorum, video fırsatları) · Şikayetvar satış sonrası deneyimi (VitrA 978 / Artema 544 şikayet, son 24 ay tam metin) |
| Fırsat | Katalog ve talep eşleşmesi (vitra.com.tr ürün sitemap'i, Trendyol) · Yeni kategori ve segment fırsatları (52.973 kelimelik evren, 58 tema) · Set, komple banyo ve ürün + hizmet |
| Rekabet ve model | Rakip görünürlüğü (Ahrefs) · Marka ve uzman sitelerde kategori trafiği (24 site, 69 baş kelime) · Pazaryerleri: Trendyol ve Hepsiburada kategori yapısı, çok satanlar, fiyat ve satıcı yapısı · Fiyat ve satıcı manzarası: Google Shopping (30 kelime × 120 ilan, 24 satıcı listesi), Trendyol ve Hepsiburada çok satanları (14 kategori), 29 VitrA ürününde 4 kanal fiyat karşılaştırması · Kanal politikaları: ödeme ve taksit, kargo ve iade, garanti ve yedek parça, sosyal kanallar, Google Business Profile, Shopping blok · Benchmark: e-ticaret modelleri ve dijital deneyim · Kanal rolleri ve etkileşim modeli · Alt kategori tamamlayıcı taraması: 57 alt kesit için vitra.com.tr kategori sayfaları (ürün, fiyat aralığı, stok), pazaryeri ve fiyat karşılaştırma aramaları, rakip mağaza aramaları, aynı model kodunda fiyat eşleşmesi |
| Resmi mağaza | VitrA Trendyol ve Hepsiburada satıcı paneli verisi: çeyreklik adet, karışım, kategori ve ürün katkısı (ciro tutarı yok, pay ve oran), görüntülenme-dönüşüm, müşteri profili, Trendyol'un Enleri, değerlendirme ve soru temaları, iptal-iade, operasyon. Ham panel dosyaları depoya alınmaz; `uretim/panel_hazirla.py` yalnızca `veri/islenmis/panel.json` üretir (Resmi mağaza panel verisi) |
| Plan ve ek | Sonraki adımlar · Yöntem · Kaynakça · Sözlük |

Rapor özellikleri: TR/EN tek dosya, metin içi terim balonları, sütun başlığı açıklamaları, alan adı logoları, kendi içinde kaydırılan uzun tablolar, koyu tema, gömülü Excel indirme. Sonraki sürümde eklenecek: VitrA pazaryeri panel verisi, GA4 (talep: `talepler/GA4_veri_talebi.md`), iade ve çağrı merkezi konuları, yapay zeka görünürlüğü.

## Üretim

```
cd uretim
python3 gsc_kategori.py && python3 kelime_niyet.py && python3 evds_isle.py && python3 analiz.py
python3 yeni_kategori.py && python3 ssg_bm.py && python3 katalog.py
python3 rapor.py && python3 excel.py && python3 rapor.py
```

`veri/islenmis/` türetilmiş tabloları içerir. Büyük ham çekimler (Keyword Planner, GSC, EVDS, sitemap, Apify) depoya alınmamıştır; rapor modüllerinin doğrudan okuduğu küçük özet dosyaları `veri/ham/` altındadır (autocomplete ve YouTube ilk tarama, Ahrefs rakip özeti, VitrA hizmet sayfaları, alan adı logoları; `derin/` altında Ahrefs pazaryeri ve marka talebi, YouTube, Şikayetvar tema özetleri, Google Shopping fiyat matrisi ve satıcı listeleri, Trendyol ve Hepsiburada çok satan özetleri, kanal politikaları). Bu dosyalarla `rapor.py → excel.py → rapor.py` zinciri depodan çalışır; ilk satırdaki işleme betikleri ham çekimleri gerektirir.
