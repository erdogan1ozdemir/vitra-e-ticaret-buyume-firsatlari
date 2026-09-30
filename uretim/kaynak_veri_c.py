# -*- coding: utf-8 -*-
"""Kaynak dokumu · C: benchmark siteleri, Ahrefs ile olculen alan adlari (rakip, marka siteleri, pazaryerleri)."""
import os, json, csv, html
from urllib.parse import urlsplit
from kaynak_ortak import *
from kaynak_veri_a import D28, D29, D30

def fs(x):
    """TR sayi bicimi: binlik nokta, ondalik virgul."""
    if isinstance(x, float) and not x.is_integer():
        return ("%.1f" % x).replace(".", ",")
    return sayi(x)

def doldur():
    # ------------------------------------------------------------ benchmark (B1-B15)
    ekle("https://www.koctas.com.tr/banyo-tadilati", "Koçtaş banyo tadilatı sayfası: banyo yenilemesini proje olarak kurgulama modeli",
         "Tüm banyo ve bitişik kategoriler tek tadilat sayfasında; montaj sepette ücretli; anahtar teslim tadilat mağazada; kampanyalar mağazaya özel",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B1"])
    ekle("https://www.ikea.com.tr/odalar/banyo", "IKEA TR banyo oda sayfası: oda bazlı gezinme ve hazır banyo setleri",
         "Oda bazlı gezinme, hazır banyo setleri, ücretsiz planlayıcı, ücretli montaj, uzun vadeli alışveriş kredisi",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B3"])
    ekle("https://www.hepsiburada.com/staticPage/12413", "Hepsiburada kurulum hizmeti sayfası: ürünle birlikte kurulum hizmeti modeli",
         "Ürünle birlikte kurulum hizmeti sepete ekleniyor; iş ortağı firma randevu veriyor",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B4"])
    ekle("https://www.bauhaus.info/service/leistungen/montageservice/komplettbad", "BAUHAUS Almanya Komplettbad servisi: sabit fiyatlı komple banyo modeli",
         "Komple banyo sabit fiyatla: planlama, söküm, tesisat, seramik, montaj; proje koordinatörü",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B6"])
    ekle("https://www.homedepot.com/services/c/bathroom-remodel/d9843b7cb", "The Home Depot banyo yenileme hizmeti: ücretsiz keşif ve proje kredisi modeli",
         "Ücretsiz evde keşif, lisanslı yerel uygulayıcı, proje kredisi",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B7"])
    ekle("https://reveal.kohler.com/en", "Reveal by KOHLER: üretici markanın bayi ağıyla paket hizmet modeli",
         "Yetkili bayilerle duş ve küvet dönüşümü, bir günde kurulum, ömür boyu sınırlı garanti",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B8"])
    ekle("https://www.villeroy-boch.co.uk/r/bathroom-ideas/planning/bathroom-planner-online/", "Villeroy & Boch 3D online banyo planlayıcı (dijital deneyim aracı)",
         "Banyo ölçüsüne göre ürün yerleştirme, planın PDF olarak bayiye iletilmesi",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B9"])
    ekle("https://www.duravit.com/en-us/service/bathroom-planner/", "Duravit banyo planlayıcı (dijital deneyim aracı)",
         "Banyo ölçüsüne göre ürün yerleştirme ve plan çıktısı",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B10"])
    ekle("https://www.hansgrohe-usa.com/service/spare-parts-search", "hansgrohe yedek parça arama (yedek parça bulucu örneği)",
         "Patlatılmış çizim, parça numarası ve montaj videosu ile yedek parça bulma; uyumluluk bilgisi",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B11"])
    ekle("https://www.grohe.com/en-GB/service-support/spare-parts-finder", "GROHE Spare Parts Finder (yedek parça bulucu örneği)",
         "Patlatılmış çizim, parça numarası, montaj videosu; kamera ile ürün tanıma; üretimden kalkan ürünlerde 10 yıl parça güvencesi",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B12"])
    ekle("https://www.geberit.de/badezimmerprodukte/wcs-urinale/dusch-wcs-geberit-aquaclean/testen/", "Geberit AquaClean evde deneme programı (Almanya)",
         "Dusch-WC'nin 4 hafta ücretsiz evde denenmesi, kurulum videosu ile",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B13"])
    ekle("https://www.victorianplumbing.co.uk/bathroom-suites", "Victorian Plumbing komple banyo takımları (koleksiyon bazlı set modeli)",
         "Komple banyo takımları (klozet + lavabo, genişletilmiş setlerde küvet, duşakabin ve dolap); koleksiyon bazlı sunum",
         bolum=["set", "benchmark"], yontem="tarayıcı", tarih=D29, kod=["B14"])
    ekle("https://www.victorianplumbing.co.uk/help-and-customer-service/bathroom-finance", "Victorian Plumbing banyo finansmanı",
         "250 GBP üzeri siparişte %0 faizli finansman; sepet tutarına bağlı finansman modeli",
         bolum=["benchmark"], yontem="tarayıcı", tarih=D29, kod=["B14"])
    ekle("https://www.vitra.com.tr/banyonu-tasarla", "VitrA V-Design (banyoyu tasarla) adresi: 3D planlayıcı durumu",
         "V-Design (2018) 750 banyo ve 300 karo ürünüyle tanıtılmıştı; adres bugün ana sayfaya yönleniyor",
         bolum=["benchmark", "adimlar"], yontem="tarayıcı", tarih=D29)

    # ------------------------------------------------------------ Ahrefs: rakip ve batch (bolum 14)
    oz = json.load(open(os.path.join(HAM, "ahrefs_rakip_ozet.json"), encoding="utf-8"))
    OR = {r[0]: r for r in oz["ahrefs_organik_rakipler_tr"]}
    BT = {r[0]: r for r in oz["ahrefs_batch_tr"]}
    sec = re.search(r'<section id="rakip">(.*?)</section>', H, re.S).group(1)
    linkler = []
    for u in re.findall(r'href="(https?://[^"]+)"', sec):
        if u not in linkler:
            linkler.append(u)
    for u in linkler:
        d = host(u).replace("www.", "")
        parca = []
        if d in OR:
            r = OR[d]
            parca.append("Organik rakipler raporu: vitra.com.tr ile %s ortak kelime, rakibin %s kelimesi, %s aylık organik trafik, DR %s" % (fs(r[1]), fs(r[2]), fs(r[3]), fs(r[4])))
        if d in BT:
            r = BT[d]
            parca.append("Batch Analysis: DR %s, %s organik kelime, ilk 3'te %s kelime, %s organik ve %s paid trafik" % (fs(r[1]), fs(r[2]), fs(r[3]), fs(r[4]), fs(r[5])))
        if not parca:
            parca.append("Rakip listesinde yer aldı")
        ekle(u, "Rakip görünürlüğü ve kanal ölçeği: %s alan adı metrikleri (Ahrefs, Türkiye)" % d, "; ".join(parca) + " (Ahrefs tahmini, 27.09.2026)",
             bolum=["rakip"], yontem="MCP (Ahrefs)", tarih="27.09.2026", kod=["D5"])

    # ------------------------------------------------------------ Ahrefs: marka ve uzman siteler (bolum 15)
    d18 = os.path.join(DERIN, "ahrefs_markalar")
    st = json.load(open(os.path.join(d18, "site_toplam.json"), encoding="utf-8"))["siteler"]
    tp = os.path.join(d18, "top_pages")
    sayfa = {}
    for f in os.listdir(tp):
        if f.endswith(".csv"):
            sayfa[f[:-4]] = sum(1 for _ in open(os.path.join(tp, f), encoding="utf-8")) - 1
    ozel = {"creavit_blog", "vitra_rehber"}
    for d, v in st.items():
        kdom = d
        n = sayfa.get(d)
        if "dr" in v:
            parca = ["Ahrefs site toplamı: DR %s, %s organik kelime, %s aylık organik trafik" % (fs(v["dr"]), fs(v["org_keywords"]), fs(v["org_traffic"]))]
        else:
            parca = ["Ahrefs site toplamı: organik trafik görünmedi (kalekim.com gerçek alan adı olarak ayrıca sorgulandı)"]
        if n:
            parca.append("top pages: %d sayfa 40'tan fazla temaya eşlendi" % n)
        if v["org_traffic"] == 0 and "dr" in v:
            parca.append("Ahrefs'te organik trafik görünmedi (gerçek alan adı ayrı sorgulandı)")
        if d == "eca.com.tr":
            parca.append("trafiğin büyük bölümü kombi, klima ve servis sayfalarından")
        ekle("https://www." + kdom, "Marka ve uzman sitelerde kategori trafiği: %s tema × trafik matrisi (Ahrefs, Türkiye)" % kdom, "; ".join(parca) + " (28.09.2026)",
             bolum=["trafik"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D18"])
    ekle("https://www.vitra.com.tr/ilham-veren-fikirler", "VitrA rehber dizini (ilham veren fikirler): rehber ve blog sayfalarının trafiği ve rehber boşlukları",
         "Ahrefs top pages: rehber dizininde %d sayfa (ör. en kullanışlı evye hangisi 2.888, klozet kapağı montajı nasıl yapılır 1.265 aylık tahmini organik ziyaret)" % sayfa.get("vitra_rehber", 0),
         bolum=["trafik"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D18"])
    ekle("https://www.creavit.com.tr/blog", "Creavit blog dizini: rehber içeriklerin trafiği",
         "Ahrefs top pages: blog dizininde %d sayfa (ör. tıkalı mutfak lavabosu nasıl açılır 1.416 aylık tahmini organik ziyaret)" % sayfa.get("creavit_blog", 0),
         bolum=["trafik"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D18"])

    # ------------------------------------------------------------ Ahrefs: pazaryeri ve yapi market (bolum 16)
    d17 = os.path.join(DERIN, "ahrefs_pazaryeri")
    ot = json.load(open(os.path.join(d17, "analiz_ozet_tablolar.json"), encoding="utf-8"))
    kok = {"trendyol": "https://www.trendyol.com", "hepsiburada": "https://www.hepsiburada.com", "n11": "https://www.n11.com", "amazon": "https://www.amazon.com.tr",
           "koctas": "https://www.koctas.com.tr", "bauhaus": "https://www.bauhaus.com.tr", "ikea": "https://www.ikea.com.tr", "tekzen": "https://www.tekzen.com.tr",
           "akakce": "https://www.akakce.com", "cimri": "https://www.cimri.com"}
    ad = {"trendyol": "Trendyol", "hepsiburada": "Hepsiburada", "n11": "n11", "amazon": "Amazon TR", "koctas": "Koçtaş", "bauhaus": "Bauhaus", "ikea": "IKEA TR", "tekzen": "Tekzen", "akakce": "Akakçe", "cimri": "Cimri"}
    tab = {r["site"]: r for r in ot["site_tablosu"]}
    hostkey = {"trendyol.com": "trendyol", "hepsiburada.com": "hepsiburada", "n11.com": "n11", "amazon.com.tr": "amazon", "koctas.com.tr": "koctas", "bauhaus.com.tr": "bauhaus",
               "ikea.com.tr": "ikea", "tekzen.com.tr": "tekzen", "akakce.com": "akakce", "cimri.com": "cimri"}
    sec16 = re.search(r'<section id="pazaryeri">(.*?)</section>', H, re.S).group(1)
    l16 = []
    for u in re.findall(r'href="(https?://[^"]+)"', sec16):
        u = html.unescape(u)
        if u not in l16:
            l16.append(u)
    for u in l16:
        sp = urlsplit(u)
        s_ = hostkey.get(sp.netloc.replace("www.", ""))
        if not s_:
            continue
        r = tab[s_]
        if not sp.path.strip("/") and not sp.query:
            ekle(u, "Pazaryerleri ve yapı marketlerde banyo kategori trafiği: %s (Ahrefs Site Explorer)" % ad[s_],
                 "Top pages sorgusu %d satır (alt sınır, pencere tabanı %s aylık ziyaret); banyo çekirdeği %s, banyo-bitişik %s aylık tahmini organik ziyaret; banyo çekirdeğinde %d sayfa" % (r["satir"], fs(r["pencere_min"]), fs(r["cekirdek"]), fs(r["bitisik"]), r["cekirdek_sayfa"]),
                 bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
        else:
            ekle(u, "%s: banyo çekirdeğinde en çok trafik alan sayfa" % ad[s_],
                 "Aylık %s tahmini organik ziyaret (banyo çekirdeğinin en büyük sayfası)" % fs(r["top_trafik"]),
                 bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
    for r_, k_ in (("trendyol", "https://www.trendyol.com"), ("hepsiburada", "https://www.hepsiburada.com")):
        ekle(k_, "", "Organic keywords sorgusu: 300 kelime (hacim, en iyi sıra, tahmini trafik)", bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
    # marka gorunurlugu: Trendyol / Hepsiburada / Koctas / Amazon marka sayfa sorgulari
    ekle("https://www.trendyol.com/vitra-klozet-x-b109184-c109226", "Trendyol'da VitrA marka + kategori sayfası (marka sayfası trafiği)",
         "VitrA'nın Trendyol'daki 38 sayfası (18'i marka veya marka+kategori) toplam aylık 9.174 tahmini organik ziyaret; bu sayfa 2.775 ile en büyüğü, top keyword \"vitra klozet\" (sıra 2)",
         bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
    ekle("https://www.hepsiburada.com/vitra-klozetler-xc-18021930-b8646", "Hepsiburada'da VitrA klozet marka + kategori sayfası (marka sayfası trafiği)",
         "VitrA'nın Hepsiburada'daki 53 sayfası toplam aylık 2.154 tahmini organik ziyaret; bu sayfa en büyüğü; sayfa ayrıca marka filtreli çok satanlar okumasında (302 klozet ürünü) kullanıldı",
         bolum=["pazaryeri"], yontem=["MCP (Ahrefs)", "tarayıcı"], tarih=[D28, D29], kod=["D17", "D22"])
    ekle("https://www.koctas.com.tr/vitra/klozet/bc/103013", "Koçtaş'ta VitrA klozet marka sayfası (marka sayfası trafiği)",
         "VitrA'nın Koçtaş'taki 45 sayfası toplam aylık 4.255 tahmini organik ziyaret; bu sayfa en büyüğü",
         bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
    ekle("https://www.trendyol.com/artema-dus-sistemi-x-b109152-c105724", "Trendyol'da Artema duş sistemi marka + kategori sayfası (marka sayfası trafiği)",
         "Artema'nın Trendyol'daki 15 sayfası toplam aylık 3.568 tahmini organik ziyaret; bu sayfa en büyüğü",
         bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
    ekle("https://www.koctas.com.tr/artema/banyo-bataryalari/bc/103010?page=6", "Koçtaş'ta Artema banyo bataryaları marka sayfası (marka sayfası trafiği)",
         "Artema'nın Koçtaş'taki 10 sayfası toplam aylık 4.072 tahmini organik ziyaret; bu sayfa en büyüğü",
         bolum=["pazaryeri"], yontem="MCP (Ahrefs)", tarih=D28, kod=["D17"])
