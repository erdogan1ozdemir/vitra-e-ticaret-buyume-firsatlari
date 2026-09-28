# -*- coding: utf-8 -*-
"""Kaynakca kaydi ve atif cozumleyici. [[ref:KOD]] -> <sup class="ref">."""
import re, html as _h
from urllib.parse import urlsplit, unquote
TARIH = "28.09.2026"
# kod: (baslik_tr, baslik_en, [url], tarih)
K = {
 "D1": ("Google Ads Keyword Planner · 2.420 kategori kelimesi · Türkiye, Türkçe · Eyl 2024 - Ağu 2026",
        "Google Ads Keyword Planner · 2,420 category keywords · Turkey, Turkish · Sep 2024 - Aug 2026",
        ["https://ads.google.com/home/tools/keyword-planner/"]),
 "D2": ("Google Search Console · sc-domain:vitra.com.tr · sayfa, sorgu, cihaz ve ülke kırılımı · 1 Haz 2025 - 25 Eyl 2026",
        "Google Search Console · sc-domain:vitra.com.tr · page, query, device and country breakdown · 1 Jun 2025 - 25 Sep 2026",
        ["https://search.google.com/search-console"]),
 "D3": ("Google Autocomplete · \"vitra\" ile başlayan 49 tohum ifade · Türkiye, Türkçe, masaüstü Chrome",
        "Google Autocomplete · 49 seed phrases starting with \"vitra\" · Turkey, Turkish, desktop Chrome",
        ["https://www.google.com.tr"]),
 "D4": ("YouTube arama sonuçları · 30 kategori, montaj ve tamir ifadesi · Türkiye · ilk 20 sonuç",
        "YouTube search results · 30 category, installation and repair phrases · Turkey · top 20 results",
        ["https://www.youtube.com"]),
 "D5": ("Ahrefs Site Explorer · organik rakipler ve toplu alan adı metrikleri · Türkiye",
        "Ahrefs Site Explorer · organic competitors and batch domain metrics · Turkey",
        ["https://ahrefs.com/site-explorer"]),
 "D6": ("TCMB EVDS · banka ve kredi kartı harcamaları, sektörel haftalık akım (BKM)",
        "CBRT EVDS · bank and credit card spending, weekly sectoral flows (BKM)",
        ["https://evds3.tcmb.gov.tr"]),
 "D7": ("TCMB EVDS · Tüketici Eğilim Anketi (TÜİK-TCMB) · aylık",
        "CBRT EVDS · Consumer Tendency Survey (TurkStat-CBRT) · monthly",
        ["https://evds3.tcmb.gov.tr"]),
 "D8": ("TCMB EVDS · konut satış istatistikleri (TÜİK) ve Konut Fiyat Endeksi",
        "CBRT EVDS · house sales statistics (TurkStat) and House Price Index",
        ["https://evds3.tcmb.gov.tr"]),
 "D9": ("TCMB EVDS · Banka Kredileri Eğilim Anketi · üç aylık, net yüzde",
        "CBRT EVDS · Bank Lending Survey · quarterly, net percentage",
        ["https://evds3.tcmb.gov.tr"]),
 "D10": ("TCMB EVDS · Kartlı Ödeme Endeksi (nominal ve reel)",
         "CBRT EVDS · Card Payment Index (nominal and real)",
         ["https://evds3.tcmb.gov.tr"]),
 "D11": ("VitrA kategori kelime araştırması · 2.420 kelime, 8 ana / 64 alt kategori · Inbound, 2025",
         "VitrA category keyword research · 2,420 keywords, 8 main / 64 sub categories · Inbound, 2025",
         ["https://github.com/erdogan1ozdemir/vitra-sezon-tr"]),
 "Y1": ("Macit Tesisat · \"VitrA gömme klozet tamiri çok basit\" · YouTube",
        "Macit Tesisat · \"VitrA concealed WC repair is very simple\" · YouTube",
        ["https://www.youtube.com/watch?v=a1i0pneZhdw"]),
}
def _gorunen(url):
    p = urlsplit(url); yol = unquote(p.path).rstrip("/")
    if p.query: yol += "?" + unquote(p.query)
    s = p.netloc.replace("www.", "") + yol
    return s if len(s) <= 90 else s[:87] + "..."
def _link(url, metin=None):
    return '<a class="u" href="%s" target="_blank" rel="noopener">%s</a>' % (_h.escape(url, quote=True), metin or _h.escape(_gorunen(url)))
def girdi(kod):
    if kod not in K: raise SystemExit("Kaynakçada bulunmayan kod: %s" % kod)
    tr, en, urls = K[kod]; return tr, en, urls, TARIH
_REF = re.compile(r"\[\[ref:([^\]]+)\]\]")
def coz(govde):
    sira, no = [], {}
    def _bir(m):
        nums = []
        for kod in [k.strip() for k in m.group(1).split(",") if k.strip()]:
            if kod not in no:
                girdi(kod); sira.append(kod); no[kod] = len(sira)
            if no[kod] not in nums: nums.append(no[kod])
        return '<sup class="ref">%s</sup>' % ",".join('<a href="#kay-%d">%d</a>' % (n, n) for n in sorted(nums))
    return _REF.sub(_bir, govde), sira
def bolum_html(sira, x):
    satir = []
    for i, kod in enumerate(sira, 1):
        tr, en, urls, tarih = girdi(kod)
        link = " &middot; ".join(_link(u, x(_h.escape(_gorunen(u)), _h.escape(_gorunen(u)))) for u in urls)
        satir.append('<li id="kay-%d"><span class="kn">%d</span><div><span class="kb">%s</span> %s<span class="kt">%s</span></div></li>'
                     % (i, i, x(tr, en), link, x("Erişim " + tarih, "Accessed " + tarih)))
    return '<p class="lede">%s</p><ol class="kaynakca">%s</ol>' % (
        x("Metindeki üst simge numaraları bu listeye bağlanmaktadır; bağlantılar yeni sekmede açılır.",
          "Superscript numbers in the text link to this list; links open in a new tab."), "".join(satir))
