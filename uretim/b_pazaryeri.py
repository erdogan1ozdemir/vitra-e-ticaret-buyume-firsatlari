# -*- coding: utf-8 -*-
"""Bolum: Pazaryerlerinde banyo - kategori trafigi (Ahrefs), kategori yapisi, cok satanlar, marka payi, fiyat, satici, mıknatıs."""
from ortak import *
import json, os
D = os.path.join(veri.V, "ham", "derin")
AP = json.load(open(os.path.join(D, "ahrefs_pazaryeri", "analiz_ozet_tablolar.json"), encoding="utf-8"))
SITE_AD = {"trendyol": "Trendyol", "hepsiburada": "Hepsiburada", "n11": "n11", "amazon": "Amazon TR", "koctas": "Koçtaş", "bauhaus": "Bauhaus", "ikea": "IKEA", "tekzen": "Tekzen", "akakce": "Akakçe", "cimri": "Cimri"}
SB_ = AP["ssg_bm"]
srows = []
for r in sorted(AP["site_tablosu"], key=lambda r: -r["cekirdek"]):
    s = r["site"]; sb = SB_.get(s, {})
    srows.append([veri_m(SITE_AD[s]), cell(r["cekirdek"]), cell(sb.get("ssg", 0)), cell(sb.get("bm", 0)), cell(r["bitisik"]), veri_m(r["top_url"][:60])])
T_SITE = tablo([th("Site", "Site", "Pazaryeri, perakendeci veya fiyat karşılaştırma sitesi.", "Marketplace, retailer or price comparison site."),
                th("Banyo ana kategorileri", "Main bathroom categories", "Banyo, SSG, BM, armatür ve yıkanma sayfalarının Ahrefs tahmini aylık organik trafiği; sorgu satır sınırı nedeniyle alt sınırdır.", "Ahrefs estimated monthly organic traffic of bathroom, SSG, BM, tap and bathing pages; a lower bound due to the query row limit.", True),
                th("SSG", "SSG", "Klozet, lavabo, bide, pisuvar, rezervuar, klozet kapağı ve iç takım sayfaları.", "WC, washbasin, bidet, urinal, cistern, seat and inner-mechanism pages.", True),
                th("BM", "BM", "Banyo dolabı, lavabo dolabı, boy dolabı, ayna, çamaşır makinesi dolabı ve tezgah sayfaları.", "Bathroom cabinet, basin unit, tall cabinet, mirror, washing machine cabinet and countertop pages.", True),
                th("Bitişik", "Adjacent", "Evye, mutfak bataryası, seramik, boy aynası, şofben gibi banyoya bitişik sayfalar.", "Pages adjacent to the bathroom such as sinks, kitchen taps, tiles, full-length mirrors and water heaters.", True),
                th("En çok trafik alan sayfa", "Top page", "Banyonun ana kategorilerinde en yüksek trafikli adres.", "Highest-traffic URL in the main bathroom categories.")], srows)
# alt kategori: TY + HB birlesik
ty = {r["sinif"]: r for r in AP["altkat_trendyol"]["satirlar"]}; hb = {r["sinif"]: r for r in AP["altkat_hepsiburada"]["satirlar"]}
SIN_EN = {"Boy aynası & genel ayna": "Full-length and general mirrors", "Çamaşır makinesi dolabı": "Washing machine cabinet", "Batarya & musluk (banyo)": "Taps and mixers (bath)", "Duşakabin & duş teknesi": "Shower enclosures and trays",
          "Banyo dolabı": "Bathroom cabinet", "Seramik & fayans": "Tiles", "Banyo aksesuarı & düzenleyici": "Bathroom accessories and organisers", "Klozet & pisuvar": "WCs and urinals", "Duş seti, başlığı & hortumu": "Shower sets, heads and hoses",
          "Evye & mutfak bataryası": "Sinks and kitchen taps", "Klozet kapağı": "Toilet seat", "Lavabo": "Washbasin", "Sifon, gider & süzgeç": "Siphons, drains and strainers", "Taharet musluğu & ara musluk": "Bidet valves and stop valves",
          "Rezervuar & iç takım": "Cisterns and inner mechanisms", "Havlupan & havluluk": "Towel radiators and rails", "Banyo aynası": "Bathroom mirrors", "Küvet & jakuzi": "Bathtubs and jacuzzis", "Banyo tekstili": "Bath textiles",
          "Şofben & termosifon": "Water heaters", "Su arıtma": "Water purifiers", "Mutfak tezgahı": "Kitchen countertops", "Banyo mobilyası (genel)": "Bathroom furniture (general)", "Tesisat & yedek parça": "Plumbing and spare parts"}
adlar = sorted(set(ty) | set(hb), key=lambda a: -((ty.get(a) or {}).get("trafik", 0) + (hb.get(a) or {}).get("trafik", 0)))[:18]
arows = []
for a in adlar:
    t_, h_ = ty.get(a, {}), hb.get(a, {})
    grp = t_.get("grup") or h_.get("grup") or ""
    def _ord(i): return "%d%s" % (i, "th" if 10 <= i % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th"))
    kwtxt = (kw(t_["top_kw"]) + " <span>" + x("(%s · %d. sıra)" % (bin(t_["top_hacim"] or 0), t_["top_sira"] or 0), "(%s · %s)" % (bin(t_["top_hacim"] or 0), _ord(t_["top_sira"] or 0))) + "</span>") if t_.get("top_kw") else "-"
    arows.append([x(a, SIN_EN.get(a, a)), x({"çekirdek": "ana", "dışı": "kapsam dışı"}.get(grp, grp), {"çekirdek": "main", "bitişik": "adjacent", "dışı": "outside"}.get(grp, grp)), cell(t_.get("trafik", 0)) if t_ else n("-"), cell(h_.get("trafik", 0)) if h_ else n("-"), kwtxt])
T_ALT = tablo([th("Alt kategori", "Sub-category", "Sayfaların URL ve en iyi kelimesine göre sınıflandığı banyo alt kategorisi.", "Bathroom sub-category into which pages were classified by URL and top keyword."),
               th("Grup", "Group", "Ana: VitrA'nın sattığı banyo kategorileri · bitişik: banyoyla birlikte alınan ama VitrA'nın sınırlı sattığı kategoriler.", "Main: bathroom categories VitrA sells · adjacent: categories bought with the bathroom that VitrA sells in a limited way."),
               th("Trendyol trafik", "Trendyol traffic", "Ahrefs tahmini aylık organik trafik.", "Ahrefs estimated monthly organic traffic.", True),
               th("Hepsiburada trafik", "Hepsiburada traffic", "Ahrefs tahmini aylık organik trafik.", "Ahrefs estimated monthly organic traffic.", True),
               th("Trendyol'da en çok trafik getiren kelime", "Top Trendyol keyword", "Kelime, aylık hacim ve Trendyol'un sırası.", "Keyword, monthly volume and Trendyol's position.")], arows, "uzun")
# kategori yapisi ve VitrA listeleme payi (tarayici)
KY = [("Klozet", "WC", "1.458", "172", "%11,8", "4.095", "302", "%7,4"), ("Lavabo", "Washbasin", "5.806", "186", "%3,2", "8.956", "313", "%3,5"),
      ("Klozet kapağı", "Toilet seat", "4.384", "76", "%1,7", "10.000+", "143", "-"), ("Rezervuar ve iç takım", "Cistern and inner mechanism", "4.149", "284", "%6,8", "3.956", "-", "-"),
      ("Pisuvar", "Urinal", "260", "37", "%14,2", "412", "-", "-"), ("Banyo dolabı seti / banyo mobilyası", "Bathroom cabinet set / furniture", "25.973", "108", "%0,4", "10.000+", "263", "-"),
      ("Batarya ve musluk (VitrA + Artema)", "Taps and mixers (VitrA + Artema)", "41.057", "492 + 891", "%3,4", "10.000+", "800 + 1.223", "-"),
      ("Duş sistemi (VitrA + Artema)", "Shower systems (VitrA + Artema)", "23.213", "291 + 346", "%2,7", "10.000+", "-", "-"), ("Banyo aksesuarı", "Bathroom accessories", "63.531", "263", "%0,4", "10.000+", "-", "-"),
      ("Banyo aynası", "Bathroom mirror", "3.404", "25", "%0,7", "10.000+", "-", "-"), ("Duşakabin", "Shower enclosure", "1.982", "2", "%0,1", "2.375", "-", "-"), ("Eviye", "Sink", "3.252", "4", "%0,1", "10.000+", "-", "-")]
T_KY = tablo([th("Kategori", "Category", "Pazaryerindeki kategori.", "Category on the marketplace."),
              th("Trendyol ürün", "Trendyol listings", "Kategori sayfasının gösterdiği sonuç sayısı, 29.09.2026.", "Result count shown on the category page, 29.09.2026.", True),
              th("VitrA Trendyol", "VitrA on Trendyol", "Kategori ve marka filtresiyle VitrA (ve Artema) listeleme sayısı.", "VitrA (and Artema) listing count with category and brand filters.", True),
              th("Trendyol payı", "Trendyol share", "VitrA listelemesinin kategori içindeki payı.", "VitrA's share of listings in the category.", True),
              th("Hepsiburada ürün", "Hepsiburada listings", "Kategori sonuç sayısı; 10.000 üzeri \"10.000+\" olarak gösterilir.", "Category result count; above 10,000 shown as \"10,000+\".", True),
              th("VitrA Hepsiburada", "VitrA on Hepsiburada", "Marka filtreli sonuç sayısı; \"-\" okunmadı.", "Brand-filtered result count; \"-\" not read.", True),
              th("Hepsiburada payı", "Hepsiburada share", "VitrA listelemesinin kategori içindeki payı.", "VitrA's share of listings in the category.", True)],
             [[x(a, b), n(c), n(d), n(e), n(f), n(g), n(h)] for a, b, c, d, e, f, g, h in KY])
CS = [("Klozet", "WC", "Turavit %38, Turkuaz %11, Seramiksan %9", "Turavit 38%, Turkuaz 11%, Seramiksan 9%", "3 ürün · %3", "3 products · 3%", "Turkuaz 536, Creavit 224 değ.", "Turkuaz 536, Creavit 224 reviews", "9 ürün · 147 değ.", "9 products · 147 reviews"),
      ("Klozet kapağı", "Toilet seat", "Visam %21, ELİTRA %20, Saban %16", "Visam 21%, ELİTRA 20%, Saban 16%", "1 ürün · %2,6", "1 product · 2.6%", "NKP 5.354, Visam 1.495 değ.", "NKP 5,354, Visam 1,495 reviews", "8 ürün · 1.038 değ.", "8 products · 1,038 reviews"),
      ("Lavabo", "Washbasin", "Turkuaz %56 (13 ürün)", "Turkuaz 56% (13 products)", "1 ürün · %0,5", "1 product · 0.5%", "Turkuaz 14 ürün, 1.221 değ.", "Turkuaz 14 products, 1,221 reviews", "ilk 36'da yok", "not in top 36"),
      ("Rezervuar ve iç takım", "Cistern and inner mechanism", "Visam %27", "Visam 27%", "9 ürün · %16", "9 products · 16%", "Visam 8 ürün, 1.962 değ.", "Visam 8 products, 1,962 reviews", "8 ürün · 2.248 değ.", "8 products · 2,248 reviews"),
      ("Banyo dolabı", "Bathroom cabinet", "KAREN BANYO %47, ÖZCEDEN %26", "KAREN BANYO 47%, ÖZCEDEN 26%", "ilk 24'te yok", "not in top 24", "Aeka, Mowo Home (arama)", "Aeka, Mowo Home (search)", "ilk 36'da yok", "not in top 36"),
      ("Lavabo dolabı", "Washbasin unit", "-", "-", "-", "-", "Dmz Home Concept 8 ürün", "Dmz Home Concept 8 products", "Mia 3 ürün · 402 değ.", "Mia 3 products · 402 reviews"),
      ("Çamaşır makinesi dolabı", "Washing machine cabinet", "sepet ve organizer ağırlıklı (Bofigo)", "mostly baskets and organisers (Bofigo)", "yok", "none", "Remaks, Bofigo", "Remaks, Bofigo", "yok", "none"),
      ("Banyo aynası", "Bathroom mirror", "SUEL HOUSE %48", "SUEL HOUSE 48%", "yok", "none", "ER-KA DİZAYN", "ER-KA DİZAYN", "1 ürün · 5 değ.", "1 product · 5 reviews"),
      ("Lavabo bataryası", "Basin tap", "Genel Markalar %30, Sardıcı %16", "Generic brands 30%, Sardıcı 16%", "Artema ilk 10'da yok", "Artema not in top 10", "Creavit 6, Sardıcı 6, ECA 4 ürün", "Creavit 6, Sardıcı 6, ECA 4 products", "Artema 4 ürün · 200 değ.", "Artema 4 products · 200 reviews"),
      ("Eviye bataryası", "Kitchen tap", "KUSTAR %48", "KUSTAR 48%", "Artema ilk 10'da yok", "Artema not in top 10", "Artema 6, Sardıcı 4 ürün", "Artema 6, Sardıcı 4 products", "Artema 6 ürün · 1.269 değ.", "Artema 6 products · 1,269 reviews"),
      ("Duşakabin", "Shower enclosure", "Durul %93", "Durul 93%", "yok", "none", "Durul 27/36 ürün", "Durul 27/36 products", "yok", "none"),
      ("Duş sistemi / başlığı", "Shower system / head", "NOY %21, Kaşbaşı Home %16", "NOY 21%, Kaşbaşı Home 16%", "yok", "none", "Berev 13 ürün", "Berev 13 products", "yok", "none")]
T_CS = tablo([th("Kategori", "Category", "Çok satan sıralamasının okunduğu kategori veya arama.", "Category or search whose bestseller ranking was read."),
              th("Trendyol: çok satanlarda öne çıkan", "Trendyol: leading bestsellers", "\"En Çok Satan\" sıralamasının ilk 36 ürününde değerlendirme payı en yüksek markalar.", "Brands with the highest review share among the top 36 products in the \"Best Selling\" ranking."),
              th("VitrA Trendyol", "VitrA on Trendyol", "İlk 36 içindeki VitrA ürün sayısı ve değerlendirme payı.", "Number of VitrA products in the top 36 and review share."),
              th("Hepsiburada: çok satanlarda öne çıkan", "Hepsiburada: leading bestsellers", "\"Çok satanlar\" sıralamasının ilk 36 ürününde öne çıkan markalar.", "Leading brands among the top 36 products in the \"Best selling\" ranking."),
              th("VitrA Hepsiburada", "VitrA on Hepsiburada", "İlk 36 içindeki VitrA (Artema) ürün sayısı ve değerlendirme toplamı.", "Number of VitrA (Artema) products in the top 36 and total reviews.")],
             [[x(a, b), x(c, d), x(e, f), x(g, h), x(i, j)] for a, b, c, d, e, f, g, h, i, j in CS], "uzun")
FB = [("Klozet", "WC", "7.500", "15.848", "6.962", "13.910", "2,0-2,1x"), ("Klozet kapağı", "Toilet seat", "619", "1.670 (Integra)", "670", "2.190", "2,7-3,3x"),
      ("Lavabo", "Washbasin", "2.930", "8.134", "1.635", "6.948", "2,8-4,2x"), ("Banyo dolabı / mobilya", "Bathroom cabinet / furniture", "6.400", "15.887", "2.148", "13.100", "2,5-6,1x"),
      ("Rezervuar iç takım", "Inner mechanism", "281", "896-1.131", "490", "837", "1,7-3,2x"), ("Klozet takımı (set)", "WC set", "-", "11.999-16.735", "8.000-12.000", "13.200-17.600", "1,4-1,5x")]
T_FB = tablo([th("Kategori", "Category", "Fiyat karşılaştırılan kategori.", "Category compared on price."),
              th("Trendyol kategori medyanı", "Trendyol category median", "Çok satan ilk 36 ürünün medyan fiyatı, TL.", "Median price of the top 36 bestsellers, TL.", True),
              th("VitrA Trendyol", "VitrA on Trendyol", "VitrA marka filtresindeki çok satan ilk 36'nın medyanı, TL.", "Median of VitrA's top 36 bestsellers under the brand filter, TL.", True),
              th("Hepsiburada kategori medyanı", "Hepsiburada category median", "Çok satan ilk 36 ürünün medyan fiyatı, TL.", "Median price of the top 36 bestsellers, TL.", True),
              th("VitrA Hepsiburada", "VitrA on Hepsiburada", "VitrA marka filtreli ilk 36 medyanı, TL.", "Median of VitrA's brand-filtered top 36, TL.", True),
              th("VitrA / kategori", "VitrA / category", "VitrA medyanının kategori medyanına oranı (iki pazaryeri aralığı).", "Ratio of VitrA's median to the category median (range across the two marketplaces).", True)],
             [[x(a, b), n(c), n(d), n(e), n(f), n(g)] for a, b, c, d, e, f, g in FB])
MK = AP["miknatis"]
MK_EN = {"Taharet musluğu & ara musluk": "Bidet valves and stop valves", "Sifon, gider & süzgeç": "Siphons, drains and strainers", "Duş seti, başlığı & hortumu": "Shower sets, heads and hoses", "Klozet kapağı": "Toilet seat", "Banyo aksesuarı & düzenleyici": "Bathroom accessories and organisers",
         "Rezervuar & iç takım": "Cisterns and inner mechanisms", "Havlupan & havluluk": "Towel radiators and rails", "Silikon & yapıştırıcı": "Silicone and adhesives", "Tesisat & yedek parça": "Plumbing and spare parts", "Kartuş & perlatör": "Cartridges and aerators", "Musluk başlığı & perlatör": "Tap heads and aerators"}
SITES = ["trendyol", "hepsiburada", "n11", "amazon", "koctas", "bauhaus", "ikea", "tekzen", "akakce", "cimri"]
mrows = []
for m in sorted(MK, key=lambda m: -sum(m.get(s) or 0 for s in SITES)):
    tot = sum(m.get(s) or 0 for s in SITES)
    mrows.append([x(m["kategori"], MK_EN.get(m["kategori"], m["kategori"])), cell(tot), cell(m.get("trendyol") or 0), cell(m.get("hepsiburada") or 0), cell(m.get("koctas") or 0)])
T_MK = tablo([th("Kategori", "Category", "Düşük fiyatlı, trafik getiren ve çapraz satışa uygun kategori.", "Low-priced category that brings traffic and suits cross-selling."),
              th("10 site toplamı", "Total across 10 sites", "Trendyol, Hepsiburada, n11, Amazon, Koçtaş, Bauhaus, IKEA, Tekzen, Akakçe ve Cimri'de Ahrefs tahmini aylık organik trafik toplamı.", "Sum of Ahrefs estimated monthly organic traffic across Trendyol, Hepsiburada, n11, Amazon, Koçtaş, Bauhaus, IKEA, Tekzen, Akakçe and Cimri.", True),
              th("Trendyol", "Trendyol", "Aylık tahmini organik trafik.", "Estimated monthly organic traffic.", True),
              th("Hepsiburada", "Hepsiburada", "Aylık tahmini organik trafik.", "Estimated monthly organic traffic.", True),
              th("Koçtaş", "Koçtaş", "Aylık tahmini organik trafik.", "Estimated monthly organic traffic.", True)], mrows)
ONER = tablo([th("Kök", "Seed", "Arama kutusuna yazılan ifade.", "Phrase typed into the search box."),
              th("Trendyol önerileri", "Trendyol suggestions", "Arama kutusunun sıraladığı öneriler (kategori ve marka önerileri dahil).", "Suggestions listed by the search box (including category and brand suggestions)."),
              th("Hepsiburada önerileri", "Hepsiburada suggestions", "Arama kutusunun öneri servisi; marka sayacı parantez içinde.", "The search box suggestion service; brand counter in brackets.")],
             [[veri_m("vitra"), veri_m("vitra klozet · vitra klozet kapağı · vitra gömme rezervuar · vitra gömme rezervuar iç takım · mağaza: VitrA"), veri_m("vitra gömme rezervuar · vitra gömme rezervuar seti · vitra klozet · vitra klozet kapağı · vitra banyo dolabı · vitra duş seti · vitra asma klozet (VitrA 3.734)")],
              [veri_m("artema"), veri_m("artema mutfak bataryası · artema banyo bataryası · artema lavabo bataryası · artema duş seti · artema taharet musluğu · arıtmalı mutfak bataryası artema"), veri_m("artema mutfak bataryası · artema banyo bataryası · artema duş seti · artema ara musluk · artema taharet musluğu (Artema 2.049)")],
              [veri_m("banyo dolabı"), veri_m("banyo lavabo dolabı · banyo kirli çamaşır sepeti dolabı · aynalı banyo dolabı · lavabolu banyo dolabı · mağaza: ROOMART, VitrA"), veri_m("lavabolu banyo dolabı · lavabo altı banyo dolabı · tekerlekli banyo dolabı · aynalı banyo dolabı · plastik banyo dolabı")],
              [veri_m("klozet"), veri_m("klozet kapağı · klozet takımı · klozet üstü raf · klozet üstü dolap · klozet taburesi"), veri_m("klozet kapağı · klozet taburesi · klozet takımı · çocuk adaptörlü klozet kapağı · marka önerisi: Klozet Montaj")],
              [veri_m("montaj hizmeti"), "-", veri_m("mr usta tesisat montaj hizmeti · mr usta batarya montaj hizmeti · mobilya montaj hizmeti (kategori: Hizmetler)")]])
x("mağaza: VitrA", "store: VitrA")
cek_ty = next(r for r in AP["site_tablosu"] if r["site"] == "trendyol")["cekirdek"]; cek_hb = next(r for r in AP["site_tablosu"] if r["site"] == "hepsiburada")["cekirdek"]; cek_ko = next(r for r in AP["site_tablosu"] if r["site"] == "koctas")["cekirdek"]
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Pazaryerleri üç kaynakla incelenmiştir: Ahrefs ile Trendyol, Hepsiburada ve sekiz perakende ve karşılaştırma sitesinin banyo kategorilerinden aldığı organik trafik; tarayıcı ile Trendyol ve Hepsiburada'nın kategori yapısı, çok satan sıralamaları, marka filtreleri ve arama önerileri. Değerlendirme sayısı satış adedine yaklaşık bir gösterge olarak kullanılmıştır.",
   "Marketplaces were examined with three sources: with Ahrefs, the organic traffic Trendyol, Hepsiburada and eight retail and comparison sites receive from bathroom categories; with the browser, the category structure, bestseller rankings, brand filters and search suggestions of Trendyol and Hepsiburada. Review count is used as an approximate indicator of units sold."),
 kpi_kart(k(cek_ty), "Trendyol banyo kategorilerinin aylık organik trafiği (Ahrefs, alt sınır)", "Monthly organic traffic of Trendyol bathroom categories (Ahrefs, lower bound)"),
 kpi_kart("%11,8", "VitrA'nın Trendyol klozet kategorisindeki listeleme payı · lavabo %3,2, banyo dolabı %0,4", "VitrA's listing share in the Trendyol WC category · washbasin 3.2%, bathroom cabinet 0.4%", "hi"),
 kpi_kart("%69", "Hepsiburada'da VitrA ürünlerinin üçüncü taraf satıcıdan sunulan payı", "Share of VitrA products offered by third-party sellers on Hepsiburada", "dn"),
 kpi_kart("2,0-6,1x", "VitrA medyan fiyatının çok satan kategori medyanına oranı (klozet, lavabo, dolap)", "Ratio of VitrA's median price to the bestseller category median (WC, washbasin, cabinet)", "dn"),
 x("Banyo trafiği hangi sitelerde?", "Which sites carry bathroom traffic?"),
 T_SITE,
 insight("Banyonun ana kategorilerinde organik trafik Trendyol (%s), Koçtaş (%s) ve Hepsiburada'da (%s) toplanmaktadır; Akakçe ve Cimri gibi fiyat karşılaştırma siteleri de toplam %s ile Amazon ve n11'in önündedir. Trendyol'da trafiğin yaklaşık %%61'i kategori, %%25'i arama ve koleksiyon sayfalarından gelmekte, ürün sayfalarının payı %%3'te kalmaktadır; banyo kararı pazaryerinde kategori listesi üzerinden verilmektedir. SSG, üç büyük sitede banyo trafiğinin %%21-24'ünü, BM Trendyol'da %%25'ini, IKEA'da %%60'ını oluşturmaktadır." % (k(cek_ty), k(cek_ko), k(cek_hb), k(72439 + 31886)),
         "Organic traffic in the main bathroom categories concentrates on Trendyol (%s), Koçtaş (%s) and Hepsiburada (%s); price comparison sites Akakçe and Cimri together (%s) are ahead of Amazon and n11. On Trendyol about 61%% of traffic comes from category pages and 25%% from search and collection pages, while product pages stay at 3%%; the bathroom decision on the marketplace is made through category listings. SSG makes up 21-24%% of bathroom traffic on the three large sites, BM 25%% on Trendyol and 60%% on IKEA." % (k(cek_ty), k(cek_ko), k(cek_hb), k(72439 + 31886)), "D17"),
 x("Alt kategori trafiği: Trendyol ve Hepsiburada", "Sub-category traffic: Trendyol and Hepsiburada"),
 T_ALT,
 insight("Trendyol'da banyo trafiğini en çok getiren alt kategoriler çamaşır makinesi dolabı (%s), batarya (%s), duşakabin (%s) ve banyo dolabıdır (%s); klozet (%s) ve klozet kapağı bunların gerisindedir. Hepsiburada'da ise batarya ilk sıradadır. Banyoya bitişik boy aynası, evye ve seramik sayfaları da ana kategoriler kadar trafik almaktadır. VitrA'nın pazaryerinde görünür olduğu klozet ve iç takım, pazaryeri trafiğinin küçük bir bölümünü oluşturmaktadır; trafiğin büyük kısmı VitrA'nın sınırlı göründüğü mobilya, duşakabin ve armatür kategorilerindedir." % (k(ty["Çamaşır makinesi dolabı"]["trafik"]), k(ty["Batarya & musluk (banyo)"]["trafik"]), k(ty["Duşakabin & duş teknesi"]["trafik"]), k(ty["Banyo dolabı"]["trafik"]), k(ty["Klozet & pisuvar"]["trafik"])),
         "On Trendyol the sub-categories bringing the most bathroom traffic are washing machine cabinets (%s), taps (%s), shower enclosures (%s) and bathroom cabinets (%s); WCs (%s) and toilet seats trail behind. On Hepsiburada taps rank first. Bathroom-adjacent full-length mirror, sink and tile pages receive as much traffic as the core categories. The WCs and inner mechanisms where VitrA is visible on the marketplace make up a small part of marketplace traffic; most traffic sits in furniture, shower enclosure and tap categories where VitrA appears weak." % (k(ty["Çamaşır makinesi dolabı"]["trafik"]), k(ty["Batarya & musluk (banyo)"]["trafik"]), k(ty["Duşakabin & duş teknesi"]["trafik"]), k(ty["Banyo dolabı"]["trafik"]), k(ty["Klozet & pisuvar"]["trafik"])), "D17"),
 x("Kategori yapısı ve VitrA'nın listeleme payı", "Category structure and VitrA's listing share"),
 T_KY,
 insight("VitrA, Hepsiburada'da Banyo ve Mutfak kategorisinde 3.191 ürünle incelenen markalar içinde en geniş listelemeye sahiptir (Creavit 1.975, Artema 1.938, Kale 1.376); Trendyol'da marka filtresi 2.781 listeleme göstermektedir. Buna karşın listelemenin büyük kısmı batarya, duş, rezervuar, tesisat ve aksesuardadır; klozet, lavabo, pisuvar ve banyo dolabı Trendyol'daki VitrA listelemesinin yaklaşık %18'idir. Banyo mobilyasında (25.973 ürün) VitrA payı %0,4, duşakabinde %0,1'dir.",
         "On Hepsiburada VitrA has the widest listing among the brands examined in the Bathroom and Kitchen category with 3,191 products (Creavit 1,975, Artema 1,938, Kale 1,376); on Trendyol the brand filter shows 2,781 listings. Most listings, however, are in taps, showers, cisterns, plumbing and accessories; WCs, washbasins, urinals and bathroom cabinets make up about 18% of VitrA's Trendyol listings. In bathroom furniture (25,973 products) VitrA's share is 0.4%, and 0.1% in shower enclosures.", "D21", "D22"),
 x("Çok satanlarda kim önde?", "Who leads the bestseller lists?"),
 T_CS,
 insight("Pazaryerinde çok satan listeleri orta fiyatlı yerel markalar ve jenerik ürünler taşımaktadır: lavaboda Turkuaz, klozette Turavit ve Turkuaz, banyo dolabında KAREN BANYO ve ÖZCEDEN, duşakabinde Durul, klozet kapağında Visam, ELİTRA ve NKP. VitrA'nın çok satanlarda güçlü olduğu alan yedek parçaya yakın ürünlerdir: rezervuar iç takımında iki pazaryerinde de ilk sıralarda, Hepsiburada'da klozet kapağında 8 ürünle en kalabalık markadır; Integra universal klozet kapağı Trendyol'da 471, Hepsiburada'da 622 değerlendirmeye ulaşmıştır. Artema, Hepsiburada'da eviye bataryasında (6 ürün, 1.269 değ.) ve Solid S lavabo bataryasında (2.313 değ.) güçlüdür; Trendyol'da ise batarya çok satanlarının ilk sıralarında görünmemektedir.",
         "Bestseller lists on the marketplace are carried by mid-priced local brands and generic products: Turkuaz in washbasins, Turavit and Turkuaz in WCs, KAREN BANYO and ÖZCEDEN in bathroom cabinets, Durul in shower enclosures, Visam, ELİTRA and NKP in toilet seats. VitrA is strong in near-spare-part products: it ranks at the top for cistern inner mechanisms on both marketplaces and is the most represented brand in toilet seats on Hepsiburada with 8 products; the Integra universal toilet seat has reached 471 reviews on Trendyol and 622 on Hepsiburada. Artema is strong on Hepsiburada in kitchen taps (6 products, 1,269 reviews) and the Solid S basin tap (2,313 reviews); on Trendyol it does not appear at the top of the tap bestseller lists.", "D21", "D22"),
 x("Fiyat konumu", "Price position"),
 T_FB,
 x("Satıcı yapısı, hizmet ve arama önerileri", "Seller structure, services and search suggestions"),
 marks([("at", "Trendyol: VitrA mağazası (İNTEMA) 833 ürün, puan 8,7; marka filtresinde 2.781 listeleme. Çok satan ilk 36'nın 19'u 12 farklı üçüncü taraf satıcıda; en çok değerlendirilen Integra klozet kapağının satıcısı da üçüncü taraf", "Trendyol: VitrA store (İNTEMA) 833 products, rating 8.7; 2,781 listings under the brand filter. 19 of the top 36 bestsellers are with 12 different third-party sellers; the most-reviewed Integra toilet seat is also sold by a third party"),
        ("at", "Hepsiburada: 210 benzersiz VitrA ürününde buybox VitrA mağazasında %19, Hepsiburada'da %13, üçüncü taraf satıcılarda %69; Artema için ayrı mağaza görünmüyor", "Hepsiburada: across 210 unique VitrA products the buybox is with the VitrA store 19%, Hepsiburada 13%, third-party sellers 69%; no separate Artema store is visible"),
        ("at", "Hepsiburada'da montaj ayrı hizmet ürünü olarak satılıyor (Mr Usta klozet montajı 2.730 TL, batarya montajı 1.375 TL); okunan VitrA ürün kartlarında kurulum etiketi görünmedi", "On Hepsiburada installation is sold as a separate service product (Mr Usta WC installation 2,730 TL, tap installation 1,375 TL); no installation label was seen on the VitrA product cards read"),
        ("up", "Set ürünler klozet, iç takım ve lavabo dolabında Hepsiburada ilk 36'nın yaklaşık yarısı; klozet takımlarında çok satan bant 8.000-12.000 TL", "Set products make up about half of Hepsiburada's top 36 in WCs, inner mechanisms and basin units; the bestselling band for WC sets is 8,000-12,000 TL")]),
 ONER,
 insight("Arama önerileri iki pazaryerinde de VitrA için yedek parça ve SSG niyetini, Artema için armatür niyetini göstermektedir. Hepsiburada'da \"vitra\" yazıldığında kategori önerisi doğrudan Rezervuar İç Takımlar'dır. Montaj hizmeti ise Hepsiburada'da ayrı bir kategori ve üçüncü taraf hizmet satıcısıyla aranmaktadır.",
         "Search suggestions on both marketplaces show spare-part and SSG intent for VitrA and tap intent for Artema. On Hepsiburada typing \"vitra\" brings Cistern Inner Mechanisms directly as the category suggestion. Installation service is searched on Hepsiburada through a separate category and a third-party service seller.", "D21", "D22"),
 x("Trafik mıknatısı kategoriler", "Traffic magnet categories"),
 T_MK,
 insight("Düşük fiyatlı ve yüksek trafikli kategoriler (banyo aksesuarı, duş başlığı, sifon, klozet kapağı, iç takım, taharet musluğu) pazaryerine sürekli ziyaret getirmekte ve ardından sepete ek ürün taşımaktadır. Trendyol ve Hepsiburada'da 700 TL altı en çok değerlendirilen ürünler duş başlığı (5 fonksiyonlu, 167-450 TL, 2.800-7.400 değ.), yapışkanlı raf (199 TL, 19.877 değ.) ve gider koku önleyicidir (130 TL, 5.405 değ.); VitrA'nın bu banttaki karşılığı klozet kapağı, iç takım, conta ve Artema filtreli ara musluktur (340-427 TL, 309-1.120 değ.). vitra.com.tr'de bu ürünlerin tek sayfada, ürün koduna göre bulunabilmesi hem arama trafiği hem de ana ürün satışına geçiş için giriş kapısı olabilir.",
         "Low-priced, high-traffic categories (bathroom accessories, shower heads, siphons, toilet seats, inner mechanisms, bidet valves) bring a steady stream of visits to the marketplace and then carry add-on products into the basket. The most-reviewed products under 700 TL on Trendyol and Hepsiburada are shower heads (5-function, 167-450 TL, 2,800-7,400 reviews), adhesive shelves (199 TL, 19,877 reviews) and drain odour stoppers (130 TL, 5,405 reviews); VitrA's counterpart in this band is toilet seats, inner mechanisms, gaskets and the Artema filtered stop valve (340-427 TL, 309-1,120 reviews). Making these products findable on one page by product code on vitra.com.tr can be an entry point both for search traffic and for moving to main product sales.", "D17", "D21", "D22"),
 kaynak("Ahrefs Site Explorer top pages ve organic keywords (TR, 28.09.2026) · Trendyol ve Hepsiburada kategori, çok satan, marka filtresi ve arama önerisi sayfaları (tarayıcı, 29.09.2026)", "Ahrefs Site Explorer top pages and organic keywords (TR, 28.09.2026) · Trendyol and Hepsiburada category, bestseller, brand filter and search suggestion pages (browser, 29.09.2026)", "D17", "D21", "D22"),
)
