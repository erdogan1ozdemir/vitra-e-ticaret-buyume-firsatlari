# -*- coding: utf-8 -*-
"""Kaynak dokumu · A: arac ve API kaynaklari, kamu verisi, dahili repo, vitra.com.tr ve rakip sitemap'leri."""
import os, json, re, csv
from kaynak_ortak import *

D28 = "28.09.2026"; D29 = "29.09.2026"; D30 = "30.09.2026"
BR = "Google Ads Keyword Planner"

def doldur():
    # ------------------------------------------------------------ Keyword Planner (DataForSEO Google Ads uc noktalari)
    ekle("https://ads.google.com/home/tools/keyword-planner/",
         "Kategori kelimelerinin aylık arama hacmi ve kelime evreni (kategori talebi, SSG ve BM incelemesi, yeni kategori fırsatları)",
         "2.420 kategori kelimesi için aylık hacim (Eyl 2022 - Ağu 2026 ve Eyl 2024 - Ağu 2026 pencereleri); 10 kök ifade grubundan 52.973 kelimelik evren, 48 aylık seri; hacimler Türkiye, Türkçe",
         yontem="API (DataForSEO, Google Ads uç noktaları)", tarih=[D28, D29], kod=["D1", "D12"], tur="API")
    ekle("https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live",
         "Sezon reposundaki 2.420 kelime için Keyword Planner aylık hacmi (talep, ihtiyaç dili ve organik kanal bölümlerinin hacim tabanı)",
         "2.420 kelime, 1.000'erli partiler; Türkiye (location 2792), Türkçe; aylık seri Eyl 2024 - Ağu 2026 ve 48 aya uzatılmış Eyl 2022 - Ağu 2026",
         yontem="API (DataForSEO)", tarih=[D28, D29], kod=["D1"], tur="API")
    ekle("https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live",
         "Kelime evrenini genişletme: SSG, BM, bitişik kategoriler, hizmet ve set, dış mekan gruplarında kök ifadeden kelime önerisi",
         "10 kök ifade grubu (ssg, bm, yeni_isitma_su, yeni_tekstil_aksesuar, yeni_ozel, yeni_yapi, yeni_mutfak, yeni_wellness, hizmet_set, dis_mekan_diger); 52.973 kelime, 48 aylık hacim serisi",
         yontem="API (DataForSEO)", tarih=D29, kod=["D12"], tur="API")

    # ------------------------------------------------------------ Search Console
    ekle("https://search.google.com/search-console",
         "vitra.com.tr organik performansı: sayfa, sorgu, cihaz ve ülke kırılımı (organik kanal, marka aramaları, YouTube ve katalog karşılaştırmaları)",
         "sc-domain:vitra.com.tr, 1 Haz 2025 - 25 Eyl 2026; sayfa raporu (ilk 25.000 satır), sorgu raporu (ilk 25.000), sorgu × sayfa, gün × cihaz, ülke; kategori sayfalarına giden tıkların payı ve markalı sorgu payı",
         yontem="API (Search Console, OAuth kullanıcı hesabı)", tarih=D28, kod=["D2"], tur="API")

    # ------------------------------------------------------------ Google (autocomplete + SERP)
    ekle("https://www.google.com.tr",
         "Marka autocomplete önerileri ve kategori arama sonuçları (marka aramaları, SERP ve AI Overview incelemesi)",
         "\"vitra\" ile başlayan 49 kök ifade için autocomplete önerileri (masaüstü Chrome, Türkiye, Türkçe; 28.09.2026); 109 kategori kelimesi için mobil SERP (ilk 20 organik sonuç, AI Overview, PAA; 29.09.2026)",
         yontem="API (DataForSEO SERP)", tarih=[D28, D29], kod=["D3", "D19"], adet=158, tur="arama motoru")
    ekle("https://api.dataforseo.com/v3/serp/google/autocomplete/live/advanced",
         "Marka autocomplete önerileri: \"vitra\" ile başlayan kök ifadeler",
         "49 kök ifade, Türkiye, Türkçe, client=chrome; ilk çekimde 46'sı boş dönen kök ifadeler cursor_pointer ile tek tek yeniden çekildi (49/49 dolu); önerilerin %18'i tamir ve yedek parça, %10'u montaj niyetli",
         yontem="API (DataForSEO)", tarih=D28, kod=["D3"], tur="API")
    ekle("https://api.dataforseo.com/v3/serp/google/organic/live/advanced",
         "Google mobil SERP: 109 kategori kelimesi; ayrıca Shopping/ürün bloğu kontrolü ve sosyal profil sayıları için SERP özetleri",
         "109 kelime, Türkiye, Türkçe, mobil Android, depth 20 (ilk 20 organik sonuç), AI Overview (31 blokta görüldü, 24'ünde içerik alındı), PAA; Trendyol 86 kelimede, VitrA 54 kelimede ilk 10'da. Kanal politikaları için 18 kelime × mobil ve masaüstü Shopping blok kontrolü (0 blok) ve Instagram/TikTok sayı özetleri",
         bolum=["serp", "trafik", "politika"], yontem="API (DataForSEO)", tarih=[D29], kod=["D19", "D23"], tur="API")
    ekle("https://api.dataforseo.com/v3/serp/google/organic/live/regular",
         "Google SERP özetleri: site:sikayetvar.com sorguları ve Akakçe/Cimri erişilemediğinde yedek okuma",
         "Şikayetvar için 15 site: sorgusu (3'ü boş döndü; marka sayfası adreslerini doğrulama ve vitra-karo sayfasının varlığı); Akakçe ve Cimri için kategori ve VitrA ürün kodu sorguları (başlık, en düşük fiyat, seçenek sayısı)",
         bolum=["sikayet", "fiyat"], yontem="API (DataForSEO)", tarih=D29, kod=["D24", "D25"], tur="API")
    ekle("https://www.google.com.tr/search?q=site:pinterest.com+{banyo+teması}",
         "Pinterest'te banyo temalı markasız görünürlük ve VitrA/Artema pin sayısı",
         "9 sorgu (8'i site:pinterest.com, 1'i doğal arama; \"vitra banyo pinterest\"); sonuç başlığı ve açıklamasında marka adı geçen pin sayıları: VitrA marka adlı dört sorguda 37, Artema 6 pin; markasız 5 sorguda yalnızca Ideal Standard 1",
         bolum=["politika"], yontem="API (DataForSEO SERP)", tarih=D29, kod=["D23"], adet=9, href="https://www.google.com.tr/search?q=site:pinterest.com+vitra+banyo", tur="arama motoru")
    ekle("https://www.google.com.tr/search?q=site:sikayetvar.com+{ifade}",
         "Şikayetvar marka sayfası adreslerinin doğrulanması",
         "15 site:sikayetvar.com sorgusu (3'ü yanıt vermedi); marka sayfası adresleri ve ayrı vitra-karo sayfasının varlığı görüldü",
         bolum=["sikayet"], yontem="API (DataForSEO SERP)", tarih=D29, kod=["D24"], adet=15, href="https://www.google.com.tr/search?q=site:sikayetvar.com+vitra", tur="arama motoru")
    ekle("https://www.google.com.tr/search?q=site:akakce.com+{ürün+kodu}",
         "Akakçe ve Cimri sonuçlarının Google SERP özetlerinden okunması (doğrudan erişim sınırlı kaldığında yedek yol)",
         "Kategori site: sorguları, kategori liste sorguları ve VitrA/Artema ürün kodu sorguları; başlık, en düşük fiyat ve seçenek sayısı",
         bolum=["fiyat"], yontem="API (DataForSEO SERP)", tarih=D29, kod=["D25"], href="https://www.google.com.tr/search?q=site:akakce.com+klozet", tur="arama motoru")

    # ------------------------------------------------------------ YouTube (DataForSEO)
    ekle("https://www.youtube.com",
         "YouTube arama sonuçları, kanal ve yorum analizi (montaj, tamir ve karar videoları)",
         "30 kategori, montaj ve tamir ifadesi (ilk 20 sonuç; 28.09.2026) ve 68 genişletilmiş arama (1.284 video satırı, 1.076 tekil video, 560 kanal); 33 videonun yorumları; VitrA ve Artema kanal sayıları (VitrA 1,58 Mn abone, 402 video)",
         yontem=["API (DataForSEO YouTube)", "curl"], tarih=[D28, D29], kod=["D4", "D20"], tur="sosyal")
    ekle("https://api.dataforseo.com/v3/serp/youtube/organic/live/advanced",
         "YouTube arama sonuçları: ifade bazında ilk 20 video, kanal ve izlenme",
         "30 ifade (28.09.2026) + 68 ifade (29.09.2026), Türkiye, Türkçe; video başlığı, kanal, izlenme, yayın zamanı, süre; kanal türü (tesisatçı, marka, mağaza) anahtar ifadeyle atandı",
         yontem="API (DataForSEO)", tarih=[D28, D29], kod=["D4", "D20"], tur="API")
    ekle("https://api.dataforseo.com/v3/serp/youtube/video_comments/live/advanced",
         "YouTube yorum madenciliği: tamir, montaj ve karar videolarında kullanıcı soruları",
         "33 video için yorumlar (video başına depth 100; 2.240 yorum çekildi, 2.218'i analizde); tema dağılımı: kalite ve sızıntı %11,1, fiyat %7,3, parça bulma ve parça numarası soruları",
         bolum=["youtube"], yontem="API (DataForSEO)", tarih=D29, kod=["D20"], adet=33, tur="API")
    ekle("https://www.youtube.com/results?search_query={arama+ifadesi}",
         "YouTube'da montaj, tamir, seçim ve ilham ifadeleri için görünen videolar",
         "68 arama ifadesi × ilk 20 sonuç, 6 grup (seçim ve karşılaştırma 11, montaj 15, tamir ve bakım 10, ilham ve tadilat 8, marka ve rakip 16, yeni kategoriler 8); en çok izlenen 14 tamir ve kurulum konusunun hiçbirinde VitrA kanal videosu yok",
         bolum=["youtube"], yontem="API (DataForSEO YouTube)", tarih=D29, kod=["D20"], adet=68,
         href="https://www.youtube.com/results?search_query=vitra+g%C3%B6mme+klozet+tamiri", tur="sosyal")
    ekle("https://www.youtube.com/results?search_query={kategori+montaj+tamir+ifadesi}",
         "YouTube'da 30 kategori, montaj ve tamir ifadesinin ilk sonuçları (ilk tur)",
         "30 ifade × ilk 20 sonuç; tamir aramalarında VitrA videosu bulunmaması ve Macit Tesisat videosunun (447K izlenme) öne çıkması",
         bolum=["youtube"], yontem="API (DataForSEO YouTube)", tarih=D28, kod=["D4"], adet=30,
         href="https://www.youtube.com/results?search_query=vitra+g%C3%B6mme+klozet+tamiri", tur="sosyal")

    # ------------------------------------------------------------ Google Maps (Business Profile)
    ekle("https://www.google.com/maps/search/vitra+banyo+mağazası+{il}",
         "VitrA etiketli satış noktası ve servis profillerinin Google Maps görünürlüğü ve puanı",
         "103 sorgu (81 il + 22 İstanbul ilçesi), sorgu başına ilk 20 sonuç; 262 VitrA etiketli satış noktası profili (8.451 yorum, ortalama 4,48) ve 76 servis profili (2.007 yorum); resmi mağaza bulucuda 161 satış + 76 servis noktası",
         bolum=["politika"], yontem="API (DataForSEO Maps)", tarih=D29, kod=["D23"], adet=103, href="https://www.google.com/maps/search/vitra+banyo+ma%C4%9Fazas%C4%B1+%C4%B0stanbul", tur="arama motoru")
    ekle("https://api.dataforseo.com/v3/serp/google/maps/live/advanced",
         "Google Maps sonuçları: VitrA etiketli profillerin puanı, yorum sayısı ve il dağılımı",
         "103 sorgu, Türkiye, Türkçe, depth 20; kayıtlar cid ile tekilleştirildi; İstanbul 64, Ankara ve İzmir 16'şar, Muğla ve Mersin 11'er satış noktası profili",
         bolum=["politika"], yontem="API (DataForSEO)", tarih=D29, kod=["D23"], tur="API")

    # ------------------------------------------------------------ Google Shopping (DataForSEO merchant)
    ekle("https://shopping.google.com",
         "Google Shopping ilanları: kategori bazında fiyat, mecra ve satıcı dağılımı; VitrA ve Artema ürünlerinin satıcı listeleri",
         "27 kategori + 3 marka kelimesi × ilk 120 ilan; 12 VitrA ve Artema ürünü için 24 satıcı listesi; VitrA Online genel 27 kelimenin 12'sinde yer alıyor; Türkiye, masaüstü",
         yontem="API (DataForSEO merchant)", tarih=D29, kod=["D25"], tur="arama motoru")
    ekle("https://api.dataforseo.com/v3/merchant/google/products/task_post",
         "Google Shopping ürün ve satıcı verisi (merchant/google/products ve sellers)",
         "30 kelime × 120 listeleme; 12 ürün için 24 satıcı listesi; asenkron task_post ve task_get/advanced",
         bolum=["fiyat"], yontem="API (DataForSEO)", tarih=D29, kod=["D25"], tur="API")

    # ------------------------------------------------------------ Ahrefs
    ekle("https://ahrefs.com/site-explorer",
         "Organik rakipler, alan adı metrikleri, marka ve uzman sitelerin ve pazaryerlerinin kategori sayfası trafiği",
         "vitra.com.tr'nin organik rakipleri (ilk 20) ve Batch Analysis (25 alan adı: DR, organik kelime, ilk 3, organik ve paid trafik; 27.09.2026); marka ve uzman siteler için top pages (26 hedef); pazaryeri ve yapı market için top pages ve organic keywords (10 site, Trendyol ve Hepsiburada 300'er kelime); Türkiye, 28.09.2026",
         yontem="MCP (Ahrefs)", tarih=["27.09.2026", D28], kod=["D5", "D17", "D18"], tur="API")
    ekle("https://ahrefs.com/keywords-explorer",
         "Baş kelimelerin hacmi, zorluğu ve marka aramalarının aylık serisi",
         "69 baş kelime için overview (hacim, KD, traffic potential, parent topic, CPC); 18 marka araması için 25 noktalık aylık hacim (Eyl 2024 - Eyl 2026); 30 baş kelime için SERP overview (ilk 10 alan adı ve DR); Türkiye",
         bolum=["trafik"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D18"], adet=69, tur="API")

    # ------------------------------------------------------------ TCMB EVDS
    ekle("https://evds3.tcmb.gov.tr",
         "Makro ortam ve ödeme gücü: kart harcamaları, tüketici eğilimi, konut, banka kredileri ve kartlı ödeme endeksi",
         "Beş veri grubu (kart harcamaları BKM haftalık akım, Tüketici Eğilim Anketi, konut satış ve fiyat, Banka Kredileri Eğilim Anketi, Kartlı Ödeme Endeksi); mobilya ve dekorasyon kart harcaması nominal +%33,7 (reel KÖE +%4,4), tüketici güveni Eyl 2026 91,9",
         yontem="API (EVDS)", tarih=D28, kod=["D6", "D7", "D8", "D9", "D10"], tur="kamu verisi")
    evds = [
        ("bie_kkhartut", "D6", "Kredi kartı harcamaları, sektörel haftalık akım (BKM)", "Sektör kırılımlı haftalık harcama tutarı (mobilya ve dekorasyon dahil), 403 haftalık seri (2019'dan itibaren); aylık toplama indirgenerek 2024-2026 karşılaştırması"),
        ("bie_kkislade", "D6", "Kredi kartı işlem adedi, sektörel haftalık akım (BKM)", "Sektör kırılımlı haftalık işlem adedi, 403 haftalık seri; harcama serisiyle birlikte ortalama işlem tutarı okuması"),
        ("bie_kartmetre", "D10", "Kartlı Ödeme Endeksi (nominal ve reel)", "Genel ve sektörel kartlı ödeme endeksi, nominal ve reel seriler (4 seri), 91 aylık; nominal harcamanın reel karşılaştırması için kullanıldı"),
        ("bie_mbgven2", "D7", "Tüketici Eğilim Anketi (TÜİK-TCMB) tüketici güven endeksi ve alt kalemler", "Tüketici Güven Endeksi ve alt kalemleri, 93 aylık seri; Eyl 2026 değeri 91,9"),
        ("bie_hanebek", "D7", "Hane halkı beklenti anketi", "Enflasyon beklentisi ve hane halkı soruları, 2026 ilk 9 ay"),
        ("bie_akonutsat1", "D8", "Konut satış istatistikleri: toplam (TÜİK)", "Türkiye toplam konut satışı, 92 aylık seri"),
        ("bie_akonutsat3", "D8", "Konut satış istatistikleri: ilk el (TÜİK)", "Türkiye ilk el konut satışı, aylık seri"),
        ("bie_akonutsat4", "D8", "Konut satış istatistikleri: ikinci el (TÜİK)", "Türkiye ikinci el konut satışı, aylık seri"),
        ("bie_kfe", "D8", "Konut Fiyat Endeksi (KFE)", "Konut Fiyat Endeksi ve yıllık değişim (TP.KFE.TR, TP.YKFE.TR), 92 aylık seri"),
        ("bie_bkea", "D9", "Banka Kredileri Eğilim Anketi", "Kredi standartları ve talep soruları, üç aylık net yüzde, 30 dönem (2019 Q1'den itibaren)"),
    ]
    for kod_, d, amac, bilgi in evds:
        ekle("https://evds3.tcmb.gov.tr/igmevdsms-dis/serieList/type=json&code=" + kod_, amac, bilgi, bolum=["makro"], yontem="API (EVDS)", tarih=D28, kod=[d], tur="kamu verisi")

    # ------------------------------------------------------------ Inbound dahili repo
    ekle("https://github.com/erdogan1ozdemir/vitra-sezon-tr",
         "Inbound'un önceki VitrA çalışması: kategori kelime araştırması ve sezonsallık, rakip analizi ve ürün fırsatları (talep tabanı ve yeni fırsat kümeleri)",
         "2.420 kelime, 8 ana / 64 alt kategori (2024-2025 hacim ve sezonsallık); Haziran 2026 sezonsallık ve banyo mobilyası fırsat çalışması, Ahrefs content gap (4.202 kelime, 7 rakip), dört ürün kümesi (yedek parça, granit/çelik/akıllı evye, arıtmalı batarya, universal akıllı kapak)",
         yontem="dahili repo (dosya okuma)", tarih=D28, kod=["D11", "D16"], tur="dahili")

    # ------------------------------------------------------------ Apify
    ekle("https://apify.com/automation-lab/trendyol-scraper",
         "Trendyol arama ve çok satan listelerinin ürün düzeyinde okunması",
         "13 tema, ilk 40-45 ürün (~1.200 ürün; rezervuar iç takımı için 150); ardından 14 kategori × 36 ürün çok satan listesi (504 kayıt); fiyat, marka, satıcı, değerlendirme sayısı; satıcı numaraları 180 mağaza sayfasıyla adlandırıldı",
         bolum=["fiyat", "ssgbm", "katalog", "yeni"], yontem="API (Apify)", tarih=[D29], kod=["D15", "D26"], adet=14, tur="API")
    ekle("https://apify.com/apify/rag-web-browser",
         "Doğrudan erişimde 403 dönen sayfaların (Koçtaş, Bauhaus ve bazı Hepsiburada sayfaları) metin olarak okunması",
         "Koçtaş taksit, nakliye ve montaj sayfaları ve ana sayfa; Hepsiburada mobilya ve büyük ürün sayfası; yaklaşık 16 çağrı",
         bolum=["politika"], yontem="API (Apify)", tarih=D29, kod=["D23"], adet=16, tur="API")

    # ------------------------------------------------------------ vitra.com.tr
    ekle("https://www.vitra.com.tr/sitemaps/sitemap-products.xml",
         "VitrA ürün kataloğunun ölçeği ve tema bazında ürün sayısı (katalog ve talep eşleşmesi, yeni kategori karşılaştırması)",
         "7.804 ürün adresi, 101 dizin; renk ve ölçü varyantları ayrı sayılmıştır, model sayısı renk ekleri ayıklanarak yaklaşık hesaplanmıştır; ürün seçimi için SKU aday listesi",
         yontem="curl", tarih=D29, kod=["D13"], tur="marka sitesi")
    ekle("https://www.vitra.com.tr/sitemaps/sitemap-categories.xml",
         "VitrA kategori sayfası yapısı (eski /c-... ve yeni dizin yapısı)",
         "Kategori adresleri; iki adres yapısı (eski /c-klozetler, yeni /vitrifiyeler/klozetler/) ve kategori varlığı karşılaştırması",
         bolum=["katalog", "yeni"], yontem="curl", tarih=D29, kod=["D13"], tur="marka sitesi")
    ekle("https://www.vitra.com.tr/sitemaps/sitemap-collections.xml",
         "VitrA koleksiyon sayfaları (set ve koleksiyon bazlı komple banyo değerlendirmesi)",
         "Koleksiyon adresleri; koleksiyon bazlı komple banyo takımı bulunup bulunmadığının kontrolü",
         bolum=["set", "benchmark"], yontem="curl", tarih=D29, kod=["D13"], tur="marka sitesi")
    ekle("https://www.vitra.com.tr/c-montaj-hizmeti",
         "VitrA montaj hizmeti kategorisi ve kalemleri (ürün + hizmet, set ve keşif boşluğu)",
         "11 montaj kalemi ve fiyatı: klozet 2.750 TL, gömme rezervuar 3.900, banyo mobilyası seti 4.000, lavabo 2.300, armatür ve duş 2.350, büyük 5.300 TL; 1 yıl servis garantisi; 40.000 TL üzeri kampanyada ücretsiz montaj",
         bolum=["set", "politika", "model", "benchmark"], yontem=["curl", "tarayıcı"], tarih=[D29], kod=["D13", "D23"], tur="marka sitesi")
    ekle("https://www.vitra.com.tr/kesif-hizmeti/kesif-hizmeti-p-etic_kesif",
         "VitrA keşif hizmeti ürün sayfası (ürün + hizmet, keşif boşluğu)",
         "Keşif hizmeti 1.400 TL (2 banyo, rölöve ve kırım hariç); kapsam ve koşul metni",
         bolum=["set", "politika", "model", "benchmark"], yontem=["curl", "tarayıcı"], tarih=D29, kod=["D13"], tur="marka sitesi")
    # hizmet sayfalari (vitra_hizmetler.json)
    try:
        h = json.load(open(os.path.join(HAM, "hizmet", "vitra_hizmetler.json"), encoding="utf-8"))
    except Exception:
        h = {}
    for ad, v in h.items():
        f = v.get("fiyat")
        fs = ("%s TL" % sayi(f)) if f else "fiyat yok"
        ekle(v["url"], "VitrA hizmet sayfası: %s (kapsam ve fiyat)" % ad.split(" ETIC")[0].strip(),
             "Hizmet kapsamı ve koşul maddeleri; fiyat %s; 1 yıl servis garantisi ve servis formu koşulu" % fs,
             bolum=["set", "benchmark", "model"], yontem="curl", tarih=D29, kod=["D13"], tur="marka sitesi")

    # ------------------------------------------------------------ rakip kategori sitemap'leri (D14)
    sm = [
        ("https://www.bauhaus.com.tr/google/sitemap/category", "Bauhaus", "1.007 kategori adresi"),
        ("https://www.ikea.com.tr/sitemap/kategori.sitemap.xml", "IKEA", "5.832 kategori adresi"),
        ("https://www.tekzen.com.tr/sitemap/categories/0.xml", "Tekzen", "529 kategori adresi"),
        ("https://www.banyomarka.com/xml/sitemap/category.xml", "Banyomarka", "290 kategori adresi"),
        ("https://www.kale.com.tr/sitemap-category.xml", "Kale", "142 kategori adresi"),
    ]
    for u, ad, n in sm:
        ekle(u, "%s kategori yapısı (rakipte olup VitrA'da bulunmayan kategori ve segmentlerin belirlenmesi)" % ad,
             "%s; banyo ve bitişik kategorilerin varlığı ve adlandırması (kategori varlığı gözlemidir, ürün derinliği ölçülmemiştir)" % n,
             bolum=["yeni", "benchmark"], yontem="curl", tarih=D29, kod=["D14"], tur="perakendeci")
    ekle("https://www.banyomarka.com/batarya-musluk-kombinleri",
         "Banyomarka kombin sayfası (set ve kombin modeli)",
         "Batarya ve musluk kombin sayfası; kombin sitemap kaydı; çocuk, engelli ve genel kullanım alanı kategorileri; WhatsApp destek",
         bolum=["set", "benchmark"], yontem=["curl", "tarayıcı"], tarih=D29, kod=["B15"], tur="perakendeci")
    ekle("https://www.evidea.com", "Evidea kategori yapısı (rakip kategori karşılaştırması)", "Kategori sitemap'i, 504 adres; banyo ve bitişik kategorilerin varlığı", bolum=["yeni", "benchmark"], yontem="curl", tarih=D29, tur="perakendeci")
    ekle("https://www.banyoline.com", "Banyoline kategori yapısı (rakip kategori karşılaştırması)", "Kategori sitemap'i, 80 adres; banyo ve bitişik kategorilerin varlığı", bolum=["yeni", "benchmark"], yontem="curl", tarih=D29, tur="perakendeci")
