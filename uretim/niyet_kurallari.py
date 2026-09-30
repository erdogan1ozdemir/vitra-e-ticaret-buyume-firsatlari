# -*- coding: utf-8 -*-
"""Arama sorgusu ve autocomplete onerisi icin ihtiyac sinifi kurallari (analiz.py ve b_marka.py ortak)."""
import re
NIY = [("Fiyat", r"fiyat|ucuz|indirim|kampanya|outlet|kaç para|ne kadar"),
       ("Tamir ve bakım", r"tamir|arıza|su kaçır|akıtı|tıkan|temizli|değişim|değiştir|onarım|bakım|yedek|iç takım|parça|servis"),
       ("Montaj", r"montaj|nasıl takılır|nasıl yapılır|kurulum|takma"),
       ("Ölçü ve teknik", r"ölçü|boyut|\bcm\b|litre|derinlik|yükseklik|genişlik|teknik|çizim"),
       ("Seçim ve karşılaştırma", r"en iyi|hangisi|tavsiye|öneri|yorum|karşılaştır|inceleme|nedir|farkı|kaliteli"),
       ("Tasarım ve fikir", r"dekorasyon|tasarım|fikir|model|trend|renk|modern|küçük banyo|katalog"),
       ("Yer ve kanal", r"bayi|mağaza|showroom|satış nokta|nerede|iletişim|müşteri hizmet")]
def niyet(q):
    for a, rx in NIY:
        if re.search(rx, q): return a
    return "Jenerik ürün"
