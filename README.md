# VitrA Türkiye · E-Ticaret Büyüme Fırsatları

VitrA'nın Türkiye e-ticaret kanalları (vitra.com.tr, Trendyol, Hepsiburada) için büyüme fırsatları çalışması. Rapor tek HTML dosyasıdır; Türkçe ve İngilizce sürüm aynı dosyada, üst bardaki EN / TR düğmesiyle değişir. Excel veri dosyası rapora gömülüdür ve üst bardan indirilebilir.

- Rapor: `VitrA_E-Ticaret_Buyume_Firsatlari.html`
- Veri dosyası: `VitrA_E-Ticaret_Buyume_Firsatlari.xlsx` (25 sekme)

## Kapsam (Sürüm 1 · 28.09.2026)

| Bölüm | Kaynak |
|---|---|
| Makro ortam ve ödeme gücü | TCMB EVDS: kart harcamaları, kartlı ödeme endeksi, tüketici eğilimi, konut, banka kredileri |
| Kategori talebi ve dönemsel değişim | Google Keyword Planner, 2.420 kelime, 8 kategori, Eyl 2024 - Ağu 2026 |
| İhtiyaç dili | Aynı kelime seti ihtiyaç sınıflarına ayrılmış; Search Console sorguları |
| Organik kanal performansı | Google Search Console, sc-domain:vitra.com.tr, Haz 2025 - Eyl 2026 |
| Marka aramaları ve autocomplete | Google Autocomplete, 49 tohum ifade |
| YouTube: montaj, tamir ve karar | YouTube arama sonuçları, 30 ifade |
| Rakip görünürlüğü ve kanal ölçeği | Ahrefs, Türkiye |
| Kanal rolleri ve etkileşim modeli | Bölüm bulgularından türetilen öneri çerçevesi |

Sonraki sürümde eklenecek: VitrA pazaryeri panel verisi, GA4 dönüşüm ve site içi arama, iade ve çağrı merkezi konuları, yapay zeka görünürlüğü.

## Üretim

```
cd uretim
python3 gsc_kategori.py && python3 kelime_niyet.py && python3 evds_isle.py && python3 analiz.py
python3 rapor.py && python3 excel.py && python3 rapor.py
```

`veri/islenmis/` türetilmiş tabloları içerir; ham çekimler (`veri/ham/`) depoya alınmamıştır.
