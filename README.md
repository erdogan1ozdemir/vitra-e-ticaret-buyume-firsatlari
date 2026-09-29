# VitrA Türkiye · E-Ticaret Büyüme Fırsatları

VitrA'nın Türkiye e-ticaret kanalları (vitra.com.tr, Trendyol, Hepsiburada) için büyüme fırsatları çalışması. Rapor tek HTML dosyasıdır; Türkçe ve İngilizce sürüm aynı dosyada, üst bardaki EN / TR düğmesiyle değişir. Excel veri dosyası rapora gömülüdür ve üst bardan indirilebilir.

- Rapor: `VitrA_E-Ticaret_Buyume_Firsatlari.html`
- Veri dosyası: `VitrA_E-Ticaret_Buyume_Firsatlari.xlsx` (37 sekme)

## Kapsam (Sürüm 2 · 29.09.2026)

| Küme | Bölümler |
|---|---|
| Durum | Özet · Makro ortam ve ödeme gücü (TCMB EVDS) |
| Talep | Kategori talebi · SSG ve BM derin talep (48 ay, ürün tipi ve özellik) · İhtiyaç dili · Organik kanal (GSC) · Marka aramaları ve autocomplete · YouTube |
| Fırsat | Katalog ve talep eşleşmesi (vitra.com.tr ürün sitemap'i, Trendyol) · Yeni kategori ve segment fırsatları (52.973 kelimelik evren, 58 tema) · Set, komple banyo ve ürün + hizmet |
| Rekabet ve model | Rakip görünürlüğü (Ahrefs) · Benchmark: e-ticaret modelleri ve dijital deneyim · Kanal rolleri ve etkileşim modeli |
| Plan ve ek | Sonraki adımlar · Yöntem · Kaynakça · Sözlük |

Sonraki sürümde eklenecek: VitrA pazaryeri panel verisi, GA4 (talep: `talepler/GA4_veri_talebi.md`), iade ve çağrı merkezi konuları, yapay zeka görünürlüğü.

## Üretim

```
cd uretim
python3 gsc_kategori.py && python3 kelime_niyet.py && python3 evds_isle.py && python3 analiz.py
python3 yeni_kategori.py && python3 ssg_bm.py && python3 katalog.py
python3 rapor.py && python3 excel.py && python3 rapor.py
```

`veri/islenmis/` türetilmiş tabloları içerir; ham çekimler (`veri/ham/`) depoya alınmamıştır.
