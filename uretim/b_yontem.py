# -*- coding: utf-8 -*-
"""Bolum: Yontem ve kapsam."""
from ortak import *
HTML = """
<p class="lede">%s</p>
%s
%s
""" % (
 x("Bu raporun ilk sürümü, Inbound'un erişimindeki veri kaynaklarıyla hazırlanmıştır. VitrA'dan beklenen pazaryeri performansı, GA4 dönüşüm ve site içi arama raporları, iade ve çağrı merkezi verisi geldiğinde ilgili bölümler eklenecek ve öneriler güncellenecektir.",
   "The first version of this report was prepared with the data sources available to Inbound. When the marketplace performance, GA4 conversion and site search reports, and return and call centre data expected from VitrA arrive, the related sections will be added and the proposals updated."),
 tablo([th("Veri kaynağı", "Data source", "Kullanılan kaynak.", "Source used."),
        th("Kapsam", "Scope", "Dönem, coğrafya ve örneklem.", "Period, geography and sample."),
        th("Kullanıldığı bölüm", "Used in section", "Verinin işlendiği bölüm.", "Section where the data is processed."),
        th("Not", "Note", "Ölçüm sınırı veya yöntem notu.", "Measurement limit or method note.")],
       [[x("Google Ads Keyword Planner", "Google Ads Keyword Planner"), x("2.420 kelime · Türkiye, Türkçe · aylık hacim Eyl 2024 - Ağu 2026", "2,420 keywords · Turkey, Turkish · monthly volume Sep 2024 - Aug 2026"), x("03, 04", "03, 04"), x("Google Ads benzer kelimeler için birleşik hacim döndürür; aynı hacimli yazım varyantları toplamda tekrar sayılmıştır ve toplamlar üst sınır olarak okunmalıdır", "Google Ads returns combined volume for similar keywords; spelling variants with identical volume are counted repeatedly in totals, which should be read as an upper bound")],
        [x("Google Search Console", "Google Search Console"), x("sc-domain:vitra.com.tr · 1 Haz 2025 - 25 Eyl 2026 · sayfa, sorgu, cihaz, ülke", "sc-domain:vitra.com.tr · 1 Jun 2025 - 25 Sep 2026 · page, query, device, country"), x("04, 05, 06", "04, 05, 06"), x("Sayfa ve sorgu raporları ilk 25.000 satırla sınırlıdır; sayfa×gün tablosu 100.000 satır", "Page and query reports are limited to the top 25,000 rows; the page×day table to 100,000 rows")],
        [x("Google Autocomplete", "Google Autocomplete"), x("49 tohum ifade · Türkiye, Türkçe, masaüstü Chrome · %s" % veri.TARIH, "49 seed phrases · Turkey, Turkish, desktop Chrome · %s" % veri.TARIH), x("06, 08", "06, 08"), x("Öneriler tek günlük anlık görüntüdür; sıralama Google'ın sırasıdır", "Suggestions are a single-day snapshot; the order is Google's")],
        [x("YouTube arama", "YouTube search"), x("30 ifade · Türkiye · ilk sayfa · %s" % veri.TARIH, "30 phrases · Turkey · first page · %s" % veri.TARIH), x("07", "07"), x("İzlenme sayıları video yayın tarihinden itibaren kümülatiftir", "View counts are cumulative from the video's publication date")],
        [x("Ahrefs Site Explorer", "Ahrefs Site Explorer"), x("Organik rakipler ve Batch Analysis · Türkiye · 27.09.2026", "Organic competitors and Batch Analysis · Turkey · 27.09.2026"), x("08", "08"), x("Organik ve paid trafik değerleri Ahrefs tahminidir; gerçek ziyaret sayısı değildir", "Organic and paid traffic values are Ahrefs estimates, not actual visit counts")],
        [x("TCMB EVDS", "CBRT EVDS"), x("Kart harcamaları, kartlı ödeme endeksi, tüketici eğilimi, konut, banka kredileri, hane halkı beklentileri · 2024-2026", "Card spending, card payment index, consumer tendency, housing, bank lending, household expectations · 2024-2026"), x("02", "02"), x("Kart harcamaları nominaldir; reel karşılaştırma için kartlı ödeme endeksinin reel serisi kullanılmıştır", "Card spending is nominal; the real series of the card payment index is used for real comparison")]]),
 box("BEKLENEN VERİ", "DATA EXPECTED", marks([("at", "VitrA panelinden Trendyol ve Hepsiburada ürün-kategori bazında görüntülenme, sepete ekleme, satın alma, iade ve müşteri soruları (son 12 ay)", "From the VitrA panel: Trendyol and Hepsiburada views, add-to-basket, purchases, returns and customer questions by product category (last 12 months)"),
                                             ("at", "GA4: ürün performansı, dönüşüm hunisi, site içi arama, kanal ve cihaz kırılımı, lead olayları (ayrı talep dokümanı iletilmiştir)", "GA4: product performance, conversion funnel, site search, channel and device breakdown, lead events (a separate request document has been sent)"),
                                             ("at", "Ürün listesi, iade nedenleri, çağrı merkezi konu başlıkları, kargo ve teslimat süreç bilgisi", "Product list, return reasons, call centre topics, shipping and delivery process information"),
                                             ("at", "Yapay zeka görünürlüğü: Inbound görünürlük aracındaki VitrA prompt seti (montaj ve e-ticaret prompt'ları eklenmiş, koşu birikince rapora alınacak)", "AI visibility: the VitrA prompt set in the Inbound visibility tool (installation and e-commerce prompts added, to be included once runs accumulate)")])),
)
