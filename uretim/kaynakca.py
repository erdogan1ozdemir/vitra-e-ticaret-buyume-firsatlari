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
 "D3": ("Google Autocomplete · \"vitra\" ile başlayan 49 kök ifade · Türkiye, Türkçe, masaüstü Chrome",
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
 "D12": ("Google Ads keyword ideas (keywords for keywords) · 10 kök ifade grubu, 52.973 kelime · Türkiye, Türkçe · Eyl 2022 - Ağu 2026",
         "Google Ads keyword ideas (keywords for keywords) · 10 seed groups, 52,973 keywords · Turkey, Turkish · Sep 2022 - Aug 2026",
         ["https://ads.google.com/home/tools/keyword-planner/"]),
 "D13": ("vitra.com.tr ürün sitemap'i (7.804 adres), kategori, hizmet ve ürün sayfaları, Banyo Asistanı akışı",
         "vitra.com.tr product sitemap (7,804 URLs), category, service and product pages, Bathroom Assistant flow",
         ["https://www.vitra.com.tr/sitemaps/sitemap-products.xml", "https://www.vitra.com.tr/c-montaj-hizmeti", "https://www.vitra.com.tr/kesif-hizmeti/kesif-hizmeti-p-etic_kesif"]),
 "D14": ("Rakip kategori sitemap'leri · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline",
         "Competitor category sitemaps · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline",
         ["https://www.bauhaus.com.tr/google/sitemap/category", "https://www.ikea.com.tr/sitemap/kategori.sitemap.xml", "https://www.tekzen.com.tr/sitemap/categories/0.xml", "https://www.banyomarka.com/xml/sitemap/category.xml", "https://www.kale.com.tr/sitemap-category.xml"]),
 "D15": ("Trendyol arama sonuçları · 13 tema, ilk 40-45 ürün (rezervuar iç takımı 150) · fiyat, marka, değerlendirme sayısı",
         "Trendyol search results · 13 themes, top 40-45 products (150 for cistern inner mechanisms) · price, brand, review count",
         ["https://www.trendyol.com"]),
 "D16": ("Inbound · VitrA sezonsallık ve banyo mobilyası fırsat çalışması, rakip analizi ve ürün fırsatları · Haziran 2026",
         "Inbound · VitrA seasonality and bathroom furniture opportunity study, competitor analysis and product opportunities · June 2026",
         ["https://github.com/erdogan1ozdemir/vitra-sezon-tr"]),
 "D17": ("Ahrefs Site Explorer · pazaryeri ve yapı market kategori sayfaları (Trendyol, Hepsiburada, Koçtaş, Akakçe, IKEA, Cimri, Amazon, Bauhaus, n11) · top pages ve organic keywords · Türkiye · 28.09.2026",
         "Ahrefs Site Explorer · marketplace and DIY retailer category pages (Trendyol, Hepsiburada, Koçtaş, Akakçe, IKEA, Cimri, Amazon, Bauhaus, n11) · top pages and organic keywords · Turkey · 28.09.2026",
         ["https://ahrefs.com/site-explorer"]),
 "D18": ("Ahrefs Site Explorer ve Keywords Explorer · 24 marka ve uzman e-ticaret sitesi top pages, 69 baş kelime, 18 marka araması · Türkiye · 28.09.2026",
         "Ahrefs Site Explorer and Keywords Explorer · top pages of 24 brand and specialist e-commerce sites, 69 head keywords, 18 brand searches · Turkey · 28.09.2026",
         ["https://ahrefs.com/site-explorer", "https://ahrefs.com/keywords-explorer"]),
 "D19": ("Google arama sonuçları (DataForSEO SERP API) · 109 kategori kelimesi, ilk 20 organik sonuç, AI Overview ve SERP özellikleri · Türkiye, Türkçe, mobil · 29.09.2026",
         "Google search results (DataForSEO SERP API) · 109 category keywords, top 20 organic results, AI Overview and SERP features · Turkey, Turkish, mobile · 29.09.2026",
         ["https://www.google.com.tr"]),
 "D20": ("YouTube arama sonuçları ve yorumlar · 68 arama ifadesi, 560 kanal, 2.218 yorum · Türkiye · 29.09.2026",
         "YouTube search results and comments · 68 search phrases, 560 channels, 2,218 comments · Turkey · 29.09.2026",
         ["https://www.youtube.com"]),
 "D21": ("Trendyol · banyo, vitrifiye ve armatür kategori ağacı, arama önerileri, mağaza ve çok satan listeleri · 29.09.2026",
         "Trendyol · bathroom, sanitaryware and tap category tree, search suggestions, store and best-seller lists · 29.09.2026",
         ["https://www.trendyol.com/banyo-yapi-malzemeleri-x-c105718", "https://www.trendyol.com/magaza/vitra-m-144409"]),
 "D22": ("Hepsiburada · banyo kategori listeleri, marka filtreleri, satıcı ve hizmet ürünleri (ilk sayfa, 36 ürün) · 29.09.2026",
         "Hepsiburada · bathroom category listings, brand filters, sellers and service products (first page, 36 products) · 29.09.2026",
         ["https://www.hepsiburada.com"]),
 "D23": ("Kanal politikaları taraması · vitra.com.tr, Koçtaş, Bauhaus, IKEA, Creavit, Banyomarka, Banyoline, Hepsiburada, Trendyol, Kale, E.C.A., Geberit, Grohe yardım, ödeme, teslimat, iade, garanti ve servis sayfaları · sosyal profiller · Google Maps ve SERP (DataForSEO) · 29.09.2026",
         "Channel policy scan · help, payment, delivery, returns, warranty and service pages of vitra.com.tr, Koçtaş, Bauhaus, IKEA, Creavit, Banyomarka, Banyoline, Hepsiburada, Trendyol, Kale, E.C.A., Geberit, Grohe · social profiles · Google Maps and SERP (DataForSEO) · 29.09.2026",
         ["https://www.vitra.com.tr/odeme-rehberi", "https://www.vitra.com.tr/teslimat-rehberi", "https://www.vitra.com.tr/garanti-hizmetleri", "https://www.koctas.com.tr/taksitler", "https://www.bauhaus.com.tr/taksit-secenekleri", "https://www.ikea.com.tr/odeme-secenekleri", "https://www.banyoline.com/montaj-hizmeti", "https://www.grohe.com/tr-TR/servis-destek/garanti"]),
 "B1": ("Koçtaş · Banyo Tadilatı sayfası", "Koçtaş · Bathroom Renovation page", ["https://www.koctas.com.tr/banyo-tadilati"]),
 "B2": ("Koçtaş · Montaj hizmetleri ve banyo kampanyası koşulları", "Koçtaş · Installation services and bathroom campaign terms", ["https://www.koctas.com.tr/hizmetlerimiz", "https://www.koctas.com.tr/banyo-kampanyasi"]),
 "B3": ("IKEA Türkiye · Banyo, montaj hizmeti ve taksit bilgisi", "IKEA Turkey · Bathroom, installation service and instalment information", ["https://www.ikea.com.tr/odalar/banyo", "https://www.ikea.com.tr/montaj-hizmeti"]),
 "B4": ("Hepsiburada · Kurulum hizmeti", "Hepsiburada · Installation service", ["https://www.hepsiburada.com/staticPage/12413"]),
 "B5": ("Kale · Montaj hizmetleri ve yedek parça sayfaları", "Kale · Installation services and spare-parts pages", ["https://www.kale.com.tr/montaj-hizmetleri", "https://www.kale.com.tr/yedek-parcalar"]),
 "B6": ("BAUHAUS Almanya · Komplettbad-Service", "BAUHAUS Germany · Komplettbad-Service", ["https://www.bauhaus.info/service/leistungen/montageservice/komplettbad"]),
 "B7": ("The Home Depot · Bathroom remodeling", "The Home Depot · Bathroom remodeling", ["https://www.homedepot.com/services/c/bathroom-remodel/d9843b7cb"]),
 "B8": ("Reveal by KOHLER · Shower and bath remodel", "Reveal by KOHLER · Shower and bath remodel", ["https://reveal.kohler.com/en"]),
 "B9": ("Villeroy & Boch · 3D online bathroom planner", "Villeroy & Boch · 3D online bathroom planner", ["https://www.villeroy-boch.co.uk/r/bathroom-ideas/planning/bathroom-planner-online/"]),
 "B10": ("Duravit · Bathroom planner", "Duravit · Bathroom planner", ["https://www.duravit.com/en-us/service/bathroom-planner/"]),
 "B11": ("hansgrohe · Spare parts search", "hansgrohe · Spare parts search", ["https://www.hansgrohe-usa.com/service/spare-parts-search"]),
 "B12": ("GROHE · Spare Parts Finder", "GROHE · Spare Parts Finder", ["https://www.grohe.com/en-GB/service-support/spare-parts-finder"]),
 "B13": ("Geberit · AquaClean evde deneme", "Geberit · AquaClean home trial", ["https://www.geberit.de/badezimmerprodukte/wcs-urinale/dusch-wcs-geberit-aquaclean/testen/"]),
 "B14": ("Victorian Plumbing · Bathroom suites ve finansman", "Victorian Plumbing · Bathroom suites and finance", ["https://www.victorianplumbing.co.uk/bathroom-suites", "https://www.victorianplumbing.co.uk/help-and-customer-service/bathroom-finance"]),
 "B15": ("Banyomarka · Batarya ve musluk kombinleri", "Banyomarka · Tap and valve bundles", ["https://www.banyomarka.com/batarya-musluk-kombinleri"]),
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
