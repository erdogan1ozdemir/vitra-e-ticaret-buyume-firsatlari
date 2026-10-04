# -*- coding: utf-8 -*-
"""Kaynakca kaydi ve atif cozumleyici. [[ref:KOD]] -> <sup class="ref">."""
import re, html as _h
from urllib.parse import urlsplit, unquote
TARIH = "28.09.2026"
# kod: (baslik_tr, baslik_en, [url], tarih)
K = {
 "D1": ("Google Ads Keyword Planner · 2.299 kategori kelimesi · Türkiye, Türkçe · Oca 2023 - Ağu 2026",
        "Google Ads Keyword Planner · 2,299 category keywords · Turkey, Turkish · Jan 2023 - Aug 2026",
        ["https://ads.google.com/home/tools/keyword-planner/"]),
 "D2": ("Google Search Console · sc-domain:vitra.com.tr · sayfa, sorgu, cihaz ve ülke kırılımı · 1 Haz 2025 - 25 Eyl 2026",
        "Google Search Console · sc-domain:vitra.com.tr · page, query, device and country breakdown · 1 Jun 2025 - 25 Sep 2026",
        ["https://search.google.com/search-console"]),
 "D3": ("Google Autocomplete · 66 kök ifade (\"vitra\" ile başlayan 14; kategori, hizmet, fiyat, rakip marka ve perakendeci için 52) · Türkiye, Türkçe, masaüstü Chrome · 30.09.2026",
        "Google Autocomplete · 66 seed phrases (14 starting with \"vitra\"; 52 for categories, services, price, competitor brands and retailers) · Turkey, Turkish, desktop Chrome · 30.09.2026",
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
 "D11": ("VitrA kategori kelime araştırması · kategori eşlemesinin alındığı ilk liste, 2.420 aday kelime, 8 ana / 64 alt kategori · Inbound, 2025",
         "VitrA category keyword research · the original list for the category mapping, 2,420 candidate keywords, 8 main / 64 sub categories · Inbound, 2025",
         []),
 "Y1": ("Macit Tesisat · \"VitrA gömme klozet tamiri çok basit\" · YouTube",
        "Macit Tesisat · \"VitrA concealed WC repair is very simple\" · YouTube",
        ["https://www.youtube.com/watch?v=a1i0pneZhdw"]),
 "D12": ("Google Ads anahtar kelime önerileri · 10 kök ifade grubu, 52.973 kelime · Türkiye, Türkçe · Eyl 2022 - Ağu 2026",
         "Google Ads keyword ideas · 10 seed groups, 52,973 keywords · Turkey, Turkish · Sep 2022 - Aug 2026",
         ["https://ads.google.com/home/tools/keyword-planner/"]),
 "D13": ("vitra.com.tr ürün sitemap'i (7.804 adres), kategori, hizmet ve ürün sayfaları, Banyo Asistanı akışı",
         "vitra.com.tr product sitemap (7,804 URLs), category, service and product pages, Bathroom Assistant flow",
         ["https://www.vitra.com.tr/sitemaps/sitemap-products.xml", "https://www.vitra.com.tr/c-montaj-hizmeti", "https://www.vitra.com.tr/kesif-hizmeti/kesif-hizmeti-p-etic_kesif"]),
 "D14": ("Rakip kategori sitemap'leri · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline",
         "Competitor category sitemaps · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline",
         ["https://www.bauhaus.com.tr/google/sitemap/category", "https://www.ikea.com.tr/sitemap/kategori.sitemap.xml", "https://www.tekzen.com.tr/sitemap/categories/0.xml", "https://www.banyomarka.com/xml/sitemap/category.xml", "https://www.kale.com.tr/sitemap-category.xml", "https://www.evidea.com", "https://www.banyoline.com"]),
 "D15": ("Trendyol arama sonuçları · 13 tema, ilk 40-45 ürün (rezervuar iç takımı 150) · fiyat, marka, değerlendirme sayısı",
         "Trendyol search results · 13 themes, top 40-45 products (150 for cistern inner mechanisms) · price, brand, review count",
         ["https://www.trendyol.com"]),
 "D16": ("Inbound · VitrA sezonsallık ve banyo mobilyası fırsat çalışması, rakip analizi ve ürün fırsatları · Haziran 2026",
         "Inbound · VitrA seasonality and bathroom furniture opportunity study, competitor analysis and product opportunities · June 2026",
         []),
 "D17": ("Ahrefs Site Explorer · pazaryeri ve yapı market kategori sayfaları (Trendyol, Hepsiburada, Koçtaş, Akakçe, IKEA, Cimri, Amazon, Bauhaus, n11) · top pages ve organic keywords · Türkiye · 28.09.2026",
         "Ahrefs Site Explorer · marketplace and DIY retailer category pages (Trendyol, Hepsiburada, Koçtaş, Akakçe, IKEA, Cimri, Amazon, Bauhaus, n11) · top pages and organic keywords · Turkey · 28.09.2026",
         ["https://ahrefs.com/site-explorer"]),
 "D18": ("Ahrefs Site Explorer ve Keywords Explorer · 24 marka ve uzman e-ticaret sitesi top pages, 69 baş kelime, 18 marka araması · Türkiye · 28.09.2026",
         "Ahrefs Site Explorer and Keywords Explorer · top pages of 24 brand and specialist e-commerce sites, 69 head keywords, 18 brand searches · Turkey · 28.09.2026",
         ["https://ahrefs.com/site-explorer", "https://ahrefs.com/keywords-explorer"]),
 "D19": ("Google arama sonuçları · 322 kelime (A VitrA gamı 159, B yakın kategoriler 83, C marka ve karşılaştırma 80), ilk 20 organik sonuç, AI Overview ve SERP özellikleri, aynı gün üç gözlem; takipteki 154 kelimede sıralar SEOmonitor 03.10.2026 · Türkiye, Türkçe, mobil · 04.10.2026",
         "Google search results · 322 keywords (A VitrA range 159, B adjacent categories 83, C brand and comparison 80), top 20 organic results, AI Overview and SERP features, three observations on the same day; positions for the 154 tracked keywords from SEOmonitor 03.10.2026 · Turkey, Turkish, mobile · 04.10.2026",
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
 "D23": ("Kanal politikaları taraması · vitra.com.tr, Koçtaş, Bauhaus, IKEA, Creavit, Banyomarka, Banyoline, Hepsiburada, Trendyol, Kale, E.C.A., Geberit, Grohe yardım, ödeme, teslimat, iade, garanti ve servis sayfaları · sosyal profiller · Google Maps ve SERP · 29.09.2026",
         "Channel policy scan · help, payment, delivery, returns, warranty and service pages of vitra.com.tr, Koçtaş, Bauhaus, IKEA, Creavit, Banyomarka, Banyoline, Hepsiburada, Trendyol, Kale, E.C.A., Geberit, Grohe · social profiles · Google Maps and SERP · 29.09.2026",
         ["https://www.vitra.com.tr/odeme-rehberi", "https://www.vitra.com.tr/teslimat-rehberi", "https://www.vitra.com.tr/garanti-hizmetleri", "https://www.koctas.com.tr/taksitler", "https://www.bauhaus.com.tr/taksit-secenekleri", "https://www.ikea.com.tr/odeme-secenekleri", "https://www.banyoline.com/montaj-hizmeti", "https://www.grohe.com/tr-TR/servis-destek/garanti"]),
 "D24": ("Şikayetvar · VitrA (978) ve Artema (544) marka sayfaları, son 24 ay şikayet metinleri, Kale, Creavit, E.C.A., Bocchi ve Geberit marka göstergeleri · 29.09.2026",
         "Şikayetvar · VitrA (978) and Artema (544) brand pages, complaint texts of the last 24 months, brand indicators of Kale, Creavit, E.C.A., Bocchi and Geberit · 29.09.2026",
         ["https://www.sikayetvar.com/vitra", "https://www.sikayetvar.com/artema"]),
 "D25": ("Google Shopping ürün ve satıcı listeleri · 27 kategori + 3 marka kelimesi, ilk 120 ilan; 12 VitrA ve Artema ürünü için 24 satıcı listesi · Türkiye · 29.09.2026 · Akakçe ve Cimri sınırlı okuma",
         "Google Shopping product and seller lists · 27 category + 3 brand keywords, first 120 listings; 24 seller lists for 12 VitrA and Artema products · Turkey · 29.09.2026 · Akakçe and Cimri limited reading",
         ["https://shopping.google.com", "https://www.akakce.com", "https://www.cimri.com"]),
 "D26": ("Trendyol ve Hepsiburada çok satan listeleri (14 kategori × 36 ürün, 1.008 kayıt) · 29 VitrA ve Artema ürününde vitra.com.tr, Trendyol, Hepsiburada ve Koçtaş liste fiyatı · 29.09.2026",
         "Trendyol and Hepsiburada best-seller lists (14 categories × 36 products, 1,008 records) · list prices of 29 VitrA and Artema products on vitra.com.tr, Trendyol, Hepsiburada and Koçtaş · 29.09.2026",
         ["https://www.trendyol.com/magaza/vitra-m-144409", "https://www.hepsiburada.com", "https://www.koctas.com.tr"]),
 "D27": ("Akakçe arama, ürün ve kategori sayfaları (29 SKU, 12 kategori) · Cimri kategori ve marka sayfaları (10 kategori) · 30.09.2026",
         "Akakçe search, product and category pages (29 SKUs, 12 categories) · Cimri category and brand pages (10 categories) · 30.09.2026",
         ["https://www.akakce.com/klozet.html", "https://www.cimri.com/klozet"]),
 "D28": ("Cimri ürün sayfaları (19 ürün, 110 teklif) · Koçtaş, Trendyol, n11, Amazon TR ve Hepsiburada yardım sayfaları · Creavit, Geberit ve Duravit garanti ve servis sayfaları · Şikayetvar şikayet ve marka sayfaları · Hepsiburada çok satan 2-3. sayfa · 30.09.2026",
         "Cimri product pages (19 products, 110 offers) · Koçtaş, Trendyol, n11, Amazon TR and Hepsiburada help pages · Creavit, Geberit and Duravit warranty and service pages · Şikayetvar complaint and brand pages · Hepsiburada best-seller pages 2-3 · 30.09.2026",
         ["https://www.koctas.com.tr/myaccount/faq", "https://www.trendyol.com/yardim/iade", "https://www.n11.com/destek-merkezi", "https://www.amazon.com.tr/gp/help/customer/display.html?nodeId=GNWCU626A4NXEEGJ", "https://www.creavit.com.tr/dokumanlar/", "https://www.duravit.com.tr/servis_hizmeti/faqs.tr-tr.html"]),
 "D29": ("Pazaryeri alt kategori taraması · Trendyol (42), Hepsiburada (40), Akakçe (42 + 8 VitrA marka sayfası), Cimri (30) çok satan ve popülerlik listeleri; Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline, Creavit e-mağaza kategori sayfaları · 30.09.2026",
         "Marketplace sub-category scan · Trendyol (42), Hepsiburada (40), Akakçe (42 + 8 VitrA brand pages), Cimri (30) best-seller and popularity lists; Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline, Creavit e-store category pages · 30.09.2026",
         ["https://www.trendyol.com/sr?wc=109226&sst=BEST_SELLER", "https://www.hepsiburada.com/klozetler-c-18021930?siralama=coksatan", "https://www.akakce.com/klozet.html", "https://www.cimri.com/klozet", "https://www.koctas.com.tr/vitrifiyeler/klozet/c/103013?sort=bestseller-desc", "https://www.banyomarka.com", "https://www.banyomega.com", "https://www.banyoline.com", "https://shop.creavit.com.tr"]),
 "D30": ("Alt kategori tamamlayıcı taraması · vitra.com.tr 55 kategori ve 3 özel sayfa (ürün, fiyat aralığı, stok, kampanya etiketi); Trendyol, Hepsiburada, Akakçe ve Cimri aramaları (57 kesit, çok satan sırası); Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline ve Creavit e-mağaza aramaları; aynı model kodunda fiyat eşleşmesi · 30.09.2026",
         "Sub-category complementary scan · vitra.com.tr 55 category and 3 special pages (products, price range, stock, campaign label); Trendyol, Hepsiburada, Akakçe and Cimri searches (57 segments, best-seller order); Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline and Creavit e-store searches; price matching on the same model code · 30.09.2026",
         ["https://www.vitra.com.tr/c-canak-lavabolar", "https://www.vitra.com.tr/c-dus-uniteleri", "https://www.vitra.com.tr/c-kampanyali-urunler", "https://www.trendyol.com/sr?q=s%C3%BCrg%C3%BCl%C3%BC%20el%20du%C5%9Fu%20tak%C4%B1m%C4%B1&sst=BEST_SELLER", "https://www.hepsiburada.com/ara?q=ankastre%20stop%20valf&siralama=coksatan", "https://www.akakce.com/klozet/ayakli-klozet.html", "https://www.cimri.com/arama?q=ayakl%C4%B1%20klozet", "https://www.koctas.com.tr/search?q=%C3%A7anak%20lavabo&sort=bestseller-desc", "https://www.banyomarka.com/arama?q=s%C3%BCrg%C3%BCl%C3%BC%20el%20du%C5%9Fu%20tak%C4%B1m%C4%B1"]),
  "D31": ("VitrA resmi mağaza satıcı paneli · Trendyol: satış (2025 Q4 - 2026 Q3), sipariş dağılımı, mağaza, operasyon, favori-görüntüleme (2025, 2026), ürün ve satıcı değerlendirmeleri, ürün ve sipariş soruları, Trendyol'un Enleri (Eylül 2026) · Hepsiburada: ürün performansı, görüntülenme ve iptal (son 12 ay), değerlendirme · 30.09.2026",
         "VitrA official store seller panel · Trendyol: sales (2025 Q4 - 2026 Q3), order distribution, store, operations, favourite-views (2025, 2026), product and seller reviews, product and order questions, Trendyol Top Lists (September 2026) · Hepsiburada: product performance, views and cancellations (last 12 months), reviews · 30.09.2026",
         ["https://partner.trendyol.com", "https://merchant.hepsiburada.com"]),
  "D32": ("Banyo yenileme adedi araştırması · TÜİK ADNKS 2024, konut satışları 2023-2026, yapı izinleri, Bina ve Konut Nitelikleri 2021 · Türkiye Seramik Federasyonu, Sanayi Bakanlığı seramik notu · Eczacıbaşı basın bülteni (2022) ve faaliyet raporları · VDS-Forsa banyo araştırması (Almanya, 2017) · 30.09.2026",
         "Bathroom renovation research · TurkStat ABPRS 2024, house sales 2023-2026, building permits, Building and Dwelling Characteristics 2021 · Turkish Ceramics Federation, Ministry of Industry ceramics note · Eczacıbaşı press release (2022) and annual reports · VDS-Forsa bathroom survey (Germany, 2017) · 30.09.2026",
         ["https://www.aa.com.tr/tr/gundem/turkiyede-ortalama-hane-halki-buyuklugu-2024te-3-11-oldu/3566979", "https://www.aa.com.tr/tr/ekonomi/turkiyede-2025te-1-milyon-688-bin-910-konut-satildi/3804701", "https://www.serfed.com/uyelerimiz/sersa", "https://www.aa.com.tr/tr/ekonomi/seramik-sektorunun-2024-ihracat-hedefi-2-milyar-dolar/3139333", "https://www.newsfilecorp.com/release/130362/Leading-Ceramics-Producer-VitrA-Sets-Sights-on-Thriving-US-Market", "https://www.eczacibasi.com.tr/en/field-of-activity/building-products", "https://www.sanitaerwirtschaft.de/markt-branche/die-deutschen-und-ihre-baeder"]),
 "D33": ("Google Search Console · sc-domain:vitra.com.tr · /ilham-veren-fikirler/ sayfaları ve soru sorguları (\"nasıl\", \"su kaçır\") · 1 Eki 2025 - 25 Eyl 2026",
         "Google Search Console · sc-domain:vitra.com.tr · /ilham-veren-fikirler/ pages and question queries (\"nasıl\", \"su kaçır\") · 1 Oct 2025 - 25 Sep 2026", ["https://search.google.com/search-console"]),
 "D34": ("Wikidata ve Wikipedia · VitrA (Q7937213, Q127325081), Türkçe ve İngilizce VitrA maddeleri, Artema araması · 02.10.2026",
         "Wikidata and Wikipedia · VitrA (Q7937213, Q127325081), Turkish and English VitrA articles, Artema search · 02.10.2026",
         ["https://www.wikidata.org/wiki/Q7937213", "https://www.wikidata.org/wiki/Q127325081", "https://tr.wikipedia.org/wiki/VitrA", "https://en.wikipedia.org/wiki/VitrA_(sanitaryware)"]),
 "D35": ("vitra.com.tr · llms.txt, robots.txt, site haritaları (ilham, destek) · 02.10.2026",
         "vitra.com.tr · llms.txt, robots.txt, sitemaps (inspiration, support) · 02.10.2026",
         ["https://www.vitra.com.tr/llms.txt", "https://www.vitra.com.tr/sitemaps/sitemap-ilham.xml", "https://www.vitra.com.tr/sitemaps/sitemap-support.xml"]),
 "D36": ("VitrA resmi mağaza satıcı paneli · Hepsiburada ürün bazlı satış raporu (son 12 ay) · 02.10.2026",
         "VitrA official store seller panel · Hepsiburada product-level sales report (last 12 months) · 02.10.2026", ["https://merchant.hepsiburada.com"]),
 "D37": ("Similarweb · site trafiği, kanal kırılımı ve etkileşim · 31 alan adı · Haz - Ağu 2026 · 03.10.2026",
         "Similarweb · site traffic, channel breakdown and engagement · 31 domains · Jun - Aug 2026 · 03.10.2026", ["https://www.similarweb.com/website/vitra.com.tr/"]),
 "D38": ("Trendyol ve Hepsiburada ürün sayfaları · VitrA, Artema ve rakip markaların herkese açık değerlendirme ve soru-cevap kayıtları · 03.10.2026",
         "Trendyol and Hepsiburada product pages · public reviews and Q&A records of VitrA, Artema and competitor brands · 03.10.2026", ["https://www.trendyol.com", "https://www.hepsiburada.com"]),
 "D39": ("Yapay zeka yanıt takibi · 125 banyo ve satın alma sorusu (14'ü VitrA adıyla) · ChatGPT, Gemini ve Google AI Overview yanıtları, adı geçen markalar ve kaynak gösterilen alan adları · 4 Eyl - 3 Eki 2026",
         "AI answer tracking · 125 bathroom and purchase questions (14 naming VitrA) · ChatGPT, Gemini and Google AI Overview answers, brands named and domains cited · 4 Sep - 3 Oct 2026", ["https://chatgpt.com", "https://gemini.google.com", "https://www.google.com.tr"]),
 "D40": ("vitra.com.tr site içi arama · 38 arama, yazarken açılan anlık sonuçlar ve Enter sonrası sonuç sayfası · 04.10.2026",
         "vitra.com.tr site search · 38 searches, instant results while typing and the results page after Enter · 04.10.2026", ["https://www.vitra.com.tr/search?text={arama}"]),
 "D41": ("vitra.com.tr sepet, giriş ve üyeliksiz alışveriş ekranları · masaüstü · 04.10.2026",
         "vitra.com.tr cart, sign-in and guest checkout screens · desktop · 04.10.2026", ["https://www.vitra.com.tr/sepetim"]),
 "D43": ("Google Ads Keyword Planner · marka aramaları: 26 üretici marka ve 10 perakendeci, yalın marka adı ve marka + kategori aramaları · Türkiye, Türkçe · Eyl 2022 - Ağu 2026",
         "Google Ads Keyword Planner · brand searches: 26 manufacturer brands and 10 retailers, brand name alone and brand + category searches · Turkey, Turkish · Sep 2022 - Aug 2026",
         ["https://ads.google.com/home/tools/keyword-planner/"]),
 "D42": ("SEOmonitor · vitra.com.tr kampanyası · 2.269 takipli kelime (8 kategoride 2.140 ana kelime ve marka aramaları) · mobil sıra, SERP özellikleri, AI Overview durumu 03.10.2026 · rakiplerle tahmini click payı 19 Eyl - 3 Eki 2026",
         "SEOmonitor · vitra.com.tr campaign · 2,269 tracked keywords (2,140 main keywords in 8 categories plus brand searches) · mobile ranks, SERP features, AI Overview status 03.10.2026 · estimated click share against competitors 19 Sep - 3 Oct 2026", ["https://app.seomonitor.com"]),
 "B1": ("Koçtaş · Banyo Tadilatı sayfası", "Koçtaş · Bathroom Renovation page", ["https://www.koctas.com.tr/banyo-tadilati"]),
 "B2": ("Koçtaş · Montaj hizmetleri ve banyo kampanyası koşulları", "Koçtaş · Installation services and bathroom campaign terms", ["https://www.koctas.com.tr/hizmetlerimiz", "https://www.koctas.com.tr/banyo-kampanyasi"]),
 "B3": ("IKEA Türkiye · Banyo, montaj hizmeti ve taksit bilgisi", "IKEA Turkey · Bathroom, installation service and instalment information", ["https://www.ikea.com.tr/odalar/banyo", "https://www.ikea.com.tr/montaj-hizmeti"]),
 "B4": ("Hepsiburada · Kurulum hizmeti", "Hepsiburada · Installation service", ["https://www.hepsiburada.com/staticPage/12413"]),
 "B5": ("Kale · Montaj hizmetleri sayfası", "Kale · Installation services page", ["https://www.kale.com.tr/montaj-hizmetleri"]),
 "B6": ("BAUHAUS Almanya · Komplettbad-Service", "BAUHAUS Germany · Komplettbad-Service", ["https://www.bauhaus.info/service/leistungen/montageservice/komplettbad"]),
 "B7": ("The Home Depot · Bathroom remodeling", "The Home Depot · Bathroom remodeling", ["https://www.homedepot.com/services/c/bathroom-remodel/d9843b7cb"]),
 "B8": ("Kohler Reveal · Shower and bath remodel", "Kohler Reveal · Shower and bath remodel", ["https://reveal.kohler.com/en"]),
 "B9": ("Villeroy & Boch · 3D online bathroom planner", "Villeroy & Boch · 3D online bathroom planner", ["https://www.villeroy-boch.co.uk/r/bathroom-ideas/planning/bathroom-planner-online/"]),
 "B10": ("Duravit · Bathroom planner", "Duravit · Bathroom planner", ["https://www.duravit.com/en-us/service/bathroom-planner/"]),
 "B11": ("Hansgrohe · Spare parts search", "Hansgrohe · Spare parts search", ["https://www.hansgrohe-usa.com/service/spare-parts-search"]),
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
    tr, en, urls = K[kod]
    tarihler = re.findall(r"\b(\d{2}\.\d{2}\.\d{4})\b", tr)
    return tr, en, urls, (tarihler[-1] if tarihler else TARIH)
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
        link = " &middot; ".join((_link(u, x(_h.escape(_gorunen(u)), _h.escape(_gorunen(u)))) if "{" not in u else '<span class="kt">%s</span>' % x(_h.escape(_gorunen(u)), _h.escape(_gorunen(u)))) for u in urls)
        satir.append('<li id="kay-%d" data-kod="%s"><span class="kn">%d</span><div><span class="kb">%s</span> %s</div></li>'
                     % (i, kod, i, x(tr, en), link))
    return '<p class="h3n">%s</p><ol class="kaynakca">%s</ol>' % (
        x("Metindeki üst simge numaraları bu listeye bağlanmaktadır; bağlantılar yeni sekmede açılır.",
          "Superscript numbers in the text link to this list; links open in a new tab."), "".join(satir))
