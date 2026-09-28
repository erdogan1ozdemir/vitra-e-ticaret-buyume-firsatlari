# -*- coding: utf-8 -*-
"""Rapor metinlerinin Ingilizce karsiliklari. EN[tr] = en.
Icerik modulleri x(tr, en) ile kayit yapar; burada yalnizca oldugu gibi kalan
ifadeler (marka, alan adi, arama kelimesi, kisaltma) listelenir."""
EN = {}
AYNI = """
VitrA|Inbound|Artema|Koçtaş|Bauhaus|IKEA|Tekzen|Evidea|Vivense|Creavit|Kale|Banyomarka|Trendyol
Hepsiburada|n11|Amazon|Amazon.com.tr|Akakçe|Cimri|Google|YouTube|ChatGPT|Gemini|AI Overview|GA4|GSC
DR|CTR|CPC|KD|SoV|YoY|MoM|✓|▲|TL|₺|Shopify|Ahrefs|SEOmonitor|Keyword Planner|Google Trends|TCMB|EVDS|BKM|TÜİK
vitra.com.tr|online.vitra.com.tr|koctas.com.tr|bauhaus.com.tr|ikea.com.tr|evidea.com|vivense.com|creavit.com.tr
kale.com.tr|banyomarka.com|trendyol.com|hepsiburada.com|n11.com|amazon.com.tr|akakce.com|tekzen.com.tr|artema.com.tr
yerevdekor.com|yurtbayseramik.com|turkmenleryapi.com.tr|egeseramikshop.com|yapilir.com|banyomoda.com|ngkutahyaseramik.com.tr
balneom.com|yapimanya.com|banyoline.com|roca.com.tr|egeseramik.com|turkuazseramik.com.tr|vitra.net.tr|serel.com.tr
ecebanyo.com|idealstandard.com.tr|Reuter|Victorian Plumbing|Wayfair|Home Depot|Rim-ex|V-Care|QuantumFlush|Sento|Integra
Metropole|Root|Origin|Flow|Bliss|Minimax|Aquaheat|Macit Tesisat|Tesisat Servisim|Kılıç Tadilat|Mini Tesisat|Faydası Olsun
VitrA Türkiye|Q1|Q2|Q3|Q4|2025 Q1|2025 Q2|2025 Q3|2025 Q4|2026 Q1|2026 Q2|2024|2025|2026|Ocak|Şubat
"""
for _t in AYNI.replace("\n", "|").split("|"):
    _t = _t.strip()
    if _t: EN[_t] = _t
