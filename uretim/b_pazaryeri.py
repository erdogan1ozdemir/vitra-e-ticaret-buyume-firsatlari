# -*- coding: utf-8 -*-
"""Bolum: Pazaryerlerinde banyo - kategori trafigi (Ahrefs), kategori yapisi, cok satanlar, marka payi, fiyat, satici, mıknatıs."""
from ortak import *
import json, os
from urllib.parse import unquote as _uq
D = os.path.join(veri.V, "ham", "derin")
AP = json.load(open(os.path.join(D, "ahrefs_pazaryeri", "analiz_ozet_tablolar.json"), encoding="utf-8"))
_KPV = json.load(open(os.path.join(veri.V, "ham", "kp_ahrefs_degis.json"), encoding="utf-8"))["kelimeler"]   # arama hacmi: Google Keyword Planner
def _kph(k_): return (_KPV.get(k_) or {}).get("ort12")
# banyo disi sayfalar (LED armatur, bebek kuveti, fotograf makinesi, kozmetik, terlik) banyo cekirdek trafiginden cikarilir
import re as _re2, collections as _col2
_SS = json.load(open(os.path.join(D, "ahrefs_pazaryeri", "analiz_sayfa_siniflandirma.json"), encoding="utf-8"))
_DIS = _re2.compile(r"led armatür|şerit led|fotoğraf|kodak|vajinal|terlik|bebek küvet")
_CIK = _col2.defaultdict(lambda: _col2.defaultdict(lambda: [0, 0]))
for _site, _lst in _SS.items():
    for _r in _lst:
        if _r["grup"] == "çekirdek" and _DIS.search((_r.get("top_kw") or "") + " " + _r["url"].lower()):
            _CIK[_site][_r["sinif"]][0] += _r["trafik"]; _CIK[_site][_r["sinif"]][1] += 1
for _r in AP["site_tablosu"]:
    _r["cekirdek"] -= sum(v_[0] for v_ in _CIK[_r["site"]].values())
for _site, _key in (("trendyol", "altkat_trendyol"), ("hepsiburada", "altkat_hepsiburada")):
    for _r in AP[_key]["satirlar"]:
        _c = _CIK[_site].get(_r["sinif"])
        if _c: _r["trafik"] -= _c[0]; _r["sayfa"] -= _c[1]
    _tot = sum(_r["trafik"] for _r in AP[_key]["satirlar"] if _r["grup"] == "çekirdek"); AP[_key]["cekirdek_toplam"] = _tot
    for _r in AP[_key]["satirlar"]:
        if _r["grup"] == "çekirdek": _r["pay_cekirdek"] = 100 * _r["trafik"] / _tot
SITE_DOM = {"trendyol": "trendyol.com", "hepsiburada": "hepsiburada.com", "n11": "n11.com", "amazon": "amazon.com.tr", "koctas": "koctas.com.tr", "bauhaus": "bauhaus.com.tr", "ikea": "ikea.com.tr", "tekzen": "tekzen.com.tr", "akakce": "akakce.com", "cimri": "cimri.com"}
SITE_AD = {"trendyol": "Trendyol", "hepsiburada": "Hepsiburada", "n11": "n11", "amazon": "Amazon TR", "koctas": "Koçtaş", "bauhaus": "Bauhaus", "ikea": "IKEA", "tekzen": "Tekzen", "akakce": "Akakçe", "cimri": "Cimri"}
SB_ = AP["ssg_bm"]
srows = []
for r in sorted(AP["site_tablosu"], key=lambda r: -r["cekirdek"]):
    s = r["site"]; sb = SB_.get(s, {})
    srows.append([u("https://www." + SITE_DOM[s], SITE_AD[s]), cell(r["cekirdek"]), cell(sb.get("ssg", 0)), cell(sb.get("bm", 0)), cell(r["bitisik"]), u("https://www." + SITE_DOM[s] + r["top_url"], _uq(r["top_url"])[:60])])
T_SITE = tablo([th("Site", "Site", "Pazaryeri, perakendeci veya fiyat karşılaştırma sitesi.", "Marketplace, retailer or price comparison site."),
                th("Banyo ana kategorileri", "Main bathroom categories", "Banyo, SSG, BM, armatür ve yıkanma sayfalarının Ahrefs tahmini aylık organik trafiği; değerler alt sınır olarak okunmalıdır.", "Ahrefs estimated monthly organic traffic of bathroom, SSG, BM, tap and bathing pages; values should be read as a lower bound; query row limit.", True),
                th("SSG", "SSG", "Klozet, lavabo, bide, pisuvar, rezervuar, klozet kapağı ve iç takım sayfaları.", "WC, washbasin, bidet, urinal, cistern, seat and inner-mechanism pages.", True),
                th("BM", "BM", "Banyo dolabı, lavabo dolabı, boy dolabı, ayna, çamaşır makinesi dolabı ve tezgah sayfaları.", "Bathroom cabinet, basin unit, tall cabinet, mirror, washing machine cabinet and countertop pages.", True),
                th("Bitişik", "Adjacent", "Evye, mutfak bataryası, seramik, boy aynası, şofben gibi banyoya bitişik sayfalar.", "Pages adjacent to the bathroom such as sinks, kitchen taps, tiles, full-length mirrors and water heaters.", True),
                th("En çok trafik alan sayfa", "Top page", "Banyonun ana kategorilerinde en yüksek trafikli adres.", "Highest-traffic URL in the main bathroom categories.")], srows)
# alt kategori: TY + HB birlesik
ty = {r["sinif"]: r for r in AP["altkat_trendyol"]["satirlar"]}; hb = {r["sinif"]: r for r in AP["altkat_hepsiburada"]["satirlar"]}
SIN_EN = {"Boy aynası & genel ayna": "Full-length and general mirrors", "Çamaşır makinesi dolabı": "Washing machine cabinet", "Batarya & musluk (banyo)": "Taps and mixers", "Duşakabin & duş teknesi": "Shower enclosures and trays",
          "Banyo dolabı": "Bathroom cabinet", "Seramik & fayans": "Tiles", "Banyo aksesuarı & düzenleyici": "Bathroom accessories and organisers", "Klozet & pisuvar": "WCs and urinals", "Duş seti, başlığı & hortumu": "Shower sets, heads and hoses",
          "Evye & mutfak bataryası": "Sinks and kitchen taps", "Klozet kapağı": "Toilet seat", "Lavabo": "Washbasin", "Sifon, gider & süzgeç": "Siphons, drains and strainers", "Taharet musluğu & ara musluk": "Bidet valves and stop valves",
          "Rezervuar & iç takım": "Cisterns and inner mechanisms", "Havlupan & havluluk": "Towel radiators and rails", "Banyo aynası": "Bathroom mirrors", "Küvet & jakuzi": "Bathtubs and jacuzzis", "Banyo tekstili": "Bath textiles",
          "Şofben & termosifon": "Water heaters", "Sifon & gider": "Siphons and drains", "Termosifon & şofben": "Storage and instantaneous water heaters", "Banyo (genel/kök)": "Bathroom (general)", "Su arıtma": "Water purifiers", "Mutfak tezgahı": "Kitchen countertops", "Banyo mobilyası (genel)": "Bathroom furniture (general)", "Tesisat & yedek parça": "Plumbing and spare parts"}
adlar = sorted(set(ty) | set(hb), key=lambda a: -((ty.get(a) or {}).get("trafik", 0) + (hb.get(a) or {}).get("trafik", 0)))[:18]
arows = []
for a in adlar:
    t_, h_ = ty.get(a, {}), hb.get(a, {})
    grp = t_.get("grup") or h_.get("grup") or ""
    def _ord(i): return "%d%s" % (i, "th" if 10 <= i % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(i % 10, "th"))
    _h = _kph(t_.get("top_kw"))
    kwtxt = (kw(t_["top_kw"]) + " <span>" + x("(%s · %d. sıra)" % (bin(_h) if _h else "-", t_["top_sira"] or 0), "(%s · %s)" % (bin(_h) if _h else "-", _ord(t_["top_sira"] or 0))) + "</span>") if t_.get("top_kw") else "-"
    arows.append([x({"Batarya & musluk (banyo)": "Batarya & musluk"}.get(a, a), SIN_EN.get(a, a)), etk({"çekirdek": "ana", "dışı": "kapsam dışı"}.get(grp, grp), {"çekirdek": "main", "bitişik": "adjacent", "dışı": "outside"}.get(grp, grp)), cell(t_.get("trafik", 0)) if t_ else n("-"), cell(h_.get("trafik", 0)) if h_ else n("-"), kwtxt])
T_ALT = tablo([th("Alt kategori", "Sub-category", "Sayfaların URL ve en iyi kelimesine göre sınıflandığı banyo alt kategorisi.", "Bathroom sub-category into which pages were classified by URL and top keyword."),
               th("Grup", "Group", "Ana: VitrA'nın sattığı banyo kategorileri · bitişik: banyoyla birlikte alınan ama VitrA'nın sınırlı sattığı kategoriler.", "Main: bathroom categories VitrA sells · adjacent: categories bought with the bathroom that VitrA sells in a limited way."),
               th("Trendyol trafik", "Trendyol traffic", "Ahrefs tahmini aylık organik trafik.", "Ahrefs estimated monthly organic traffic.", True),
               th("Hepsiburada trafik", "Hepsiburada traffic", "Ahrefs tahmini aylık organik trafik.", "Ahrefs estimated monthly organic traffic.", True),
               th("Trendyol'da en çok trafik getiren kelime", "Top Trendyol keyword", "Kelime, aylık arama hacmi (Google Keyword Planner, Eyl 2025 - Ağu 2026 ortalaması) ve Trendyol'un sırası.", "Keyword, monthly search volume (Google Keyword Planner, Sep 2025 - Aug 2026 average) and Trendyol's position.")], arows, "uzun")
# kategori yapisi ve VitrA listeleme payi (tarayici)
KY = [("Klozet", "WC", "1.458", "172", "%11,8", "4.095", "302", "%7,4"), ("Lavabo", "Washbasin", "5.806", "186", "%3,2", "8.956", "313", "%3,5"),
      ("Klozet kapağı", "Toilet seat", "4.384", "76", "%1,7", "10.000+", "143", "-"), ("Rezervuar ve iç takım", "Cistern and inner mechanism", "4.149", "284", "%6,8", "3.956", "-", "-"),
      ("Pisuvar", "Urinal", "260", "37", "%14,2", "412", "-", "-"), ("Banyo dolabı seti / banyo mobilyası", "Bathroom cabinet set / furniture", "25.973", "108", "%0,4", "10.000+", "263", "-"),
      ("Batarya ve musluk (VitrA + Artema)", "Taps and mixers (VitrA + Artema)", "41.057", "492 + 891", "%3,4", "10.000+", "800 + 1.223", "-"),
      ("Duş sistemi (VitrA + Artema)", "Shower systems (VitrA + Artema)", "23.213", "291 + 346", "%2,7", "10.000+", "-", "-"), ("Banyo aksesuarı", "Bathroom accessories", "63.531", "263", "%0,4", "10.000+", "-", "-"),
      ("Banyo aynası", "Bathroom mirror", "3.404", "25", "%0,7", "10.000+", "-", "-"), ("Duşakabin", "Shower enclosure", "1.982", "2", "%0,1", "2.375", "-", "-"), ("Evye", "Sink", "3.252", "4", "%0,1", "10.000+", "-", "-")]
T_KY = tablo([th("Kategori", "Category", "Pazaryerindeki kategori.", "Category on the marketplace."),
              th("Trendyol ürün", "Trendyol listings", "Kategori sayfasının gösterdiği sonuç sayısı, 29.09.2026.", "Result count shown on the category page, 29.09.2026.", True),
              th("VitrA Trendyol", "VitrA on Trendyol", "Kategori ve marka filtresiyle VitrA (ve Artema) listeleme sayısı.", "VitrA (and Artema) listing count with category and brand filters.", True),
              th("Trendyol payı", "Trendyol share", "VitrA listelemesinin kategori içindeki payı.", "VitrA's share of listings in the category.", True),
              th("Hepsiburada ürün", "Hepsiburada listings", "Kategori sonuç sayısı; 10.000 üzeri \"10.000+\" olarak gösterilir.", "Category result count; above 10,000 shown as \"10,000+\".", True),
              th("VitrA Hepsiburada", "VitrA on Hepsiburada", "Marka filtreli sonuç sayısı; Hepsiburada payı klozette %7,4, lavaboda %3,5'tir; \"-\" veri yok.", "Brand-filtered result count; the Hepsiburada share is 7.4% for WCs and 3.5% for washbasins; \"-\" no data.", True)],
             [[x(a, b), n(c), n(d), n(e), n(f), n(g)] for a, b, c, d, e, f, g, h in KY])
CS = [
 # kategori, TY lider marka, TY lider degerlendirme payi, VitrA TY urun (ilk 36), VitrA TY deg. payi, HB lider marka, HB lider deg./urun, VitrA HB urun, VitrA HB deg.
 (("Klozet", "WC"), "Turavit", "%38", "3", "%3", "Turkuaz", "536", "9", "147"),
 (("Klozet kapağı", "Toilet seat"), "Visam", "%21", "1", "%2,6", "NKP", "5.354", "8", "1.038"),
 (("Lavabo", "Washbasin"), "Turkuaz", "%56", "1", "%0,5", "Turkuaz", "1.221", "0", "-"),
 (("Rezervuar ve iç takım", "Cistern and inner mechanism"), "Visam", "%27", "9", "%16", "VitrA", "2.248", "8", "2.248"),
 (("Banyo dolabı", "Bathroom cabinet"), "KAREN BANYO", "%47", "0", "-", "Aeka", "-", "0", "-"),
 (("Lavabo dolabı", "Washbasin unit"), "-", "-", "-", "-", "Dmz Home Concept", "-", "3", "402"),
 (("Çamaşır makinesi dolabı", "Washing machine cabinet"), "Bofigo", "-", "0", "-", "Remaks", "-", "0", "-"),
 (("Banyo aynası", "Bathroom mirror"), "SUEL HOUSE", "%48", "0", "-", "ER-KA DİZAYN", "-", "1", "5"),
 (("Lavabo bataryası", "Basin tap"), "Markasız (Genel Markalar)", "%30", "0", "-", "Creavit", "-", "4", "200"),
 (("Evye bataryası", "Kitchen tap"), "KUSTAR", "%48", "0", "-", "Artema", "-", "6", "1.269"),
 (("Duşakabin", "Shower enclosure"), "Durul", "%93", "0", "-", "Durul", "-", "0", "-"),
 (("Duş sistemi / başlığı", "Shower system / head"), "NOY", "%21", "0", "-", "Berev", "-", "0", "-")]
CS_NOT = {"Klozet": ("2. Turkuaz %11, 3. Seramiksan %9", "2nd Turkuaz 11%, 3rd Seramiksan 9%"), "Klozet kapağı": ("ELİTRA %20, Saban %16; HB'de Visam 1.495", "ELİTRA 20%, Saban 16%; Visam 1,495 on HB"),
          "Lavabo": ("Turkuaz 13 ürün; HB'de 14 ürün", "Turkuaz 13 products; 14 products on HB"), "Rezervuar ve iç takım": ("HB'de Visam 8 ürün, 1.962 değerlendirme", "Visam 8 products and 1,962 reviews on HB"),
          "Banyo dolabı": ("ÖZCEDEN %26; HB listesi arama sonucudur (Aeka, Mowo Home)", "ÖZCEDEN 26%; HB list is a search result (Aeka, Mowo Home)"), "Lavabo dolabı": ("HB'de Dmz Home Concept 8 ürün; VitrA Mia", "Dmz Home Concept 8 products on HB; VitrA Mia"),
          "Çamaşır makinesi dolabı": ("Liste sepet ve düzenleyici ağırlıklı; HB'de Bofigo da var", "List dominated by baskets and organisers; Bofigo also on HB"), "Banyo aynası": ("-", "-"),
          "Lavabo bataryası": ("Sardıcı %16; HB'de Creavit 6, Sardıcı 6, ECA 4 ürün; Artema Trendyol ilk 36'da yok; Solid S Hepsiburada ürün sayfasında 2.313 değerlendirmeyle çok satan ilk 36 dışında", "Sardıcı 16%; Creavit 6, Sardıcı 6, ECA 4 products on HB; Artema not in Trendyol top 36; Solid S has 2,313 reviews on its Hepsiburada product page but sits outside the top 36"),
          "Evye bataryası": ("HB'de Artema 6, Sardıcı 4 ürün; Artema Trendyol ilk 36'da yok", "Artema 6, Sardıcı 4 products on HB; Artema not in Trendyol top 36"), "Duşakabin": ("HB'de Durul 27/36 ürün", "Durul 27/36 products on HB"),
          "Duş sistemi / başlığı": ("Kaşbaşı Home %16; HB'de Berev 13 ürün", "Kaşbaşı Home 16%; Berev 13 products on HB")}
def _cs(v): return n(v) if v not in ("-", "") else n("-")
T_CS = tablo([th("Kategori", "Category", "Çok satan sıralamasının okunduğu kategori veya arama.", "Category or search whose bestseller ranking was read."),
              th("Trendyol lider marka", "Trendyol leading brand", "\"En Çok Satan\" sıralamasının ilk 36 ürününde değerlendirme payı en yüksek marka.", "Brand with the highest review share among the top 36 products in the \"Best Seller\" ranking."),
              th("Lider payı (TY)", "Leader share (TY)", "Lider markanın ilk 36'daki değerlendirme payı.", "The leading brand's share of reviews in the top 36.", True),
              th("VitrA ürün (TY ilk 36)", "VitrA products (TY top 36)", "İlk 36 içindeki VitrA (Artema) ürün sayısı; 0 = listede yok.", "Number of VitrA (Artema) products in the top 36; 0 = not listed.", True),
              th("VitrA değ. payı (TY)", "VitrA review share (TY)", "VitrA ürünlerinin ilk 36'daki değerlendirme payı.", "Review share of VitrA products in the top 36.", True),
              th("Hepsiburada lider marka", "Hepsiburada leading brand", "\"Çok satanlar\" sıralamasının ilk 36 ürününde öne çıkan marka.", "Leading brand among the top 36 products in the \"Best selling\" ranking."),
              th("Lider değ. (HB)", "Leader reviews (HB)", "Lider markanın ilk 36'daki toplam değerlendirme sayısı; \"-\" veri yok.", "Total reviews of the leading brand in the top 36; \"-\" no data.", True),
              th("VitrA ürün (HB ilk 36)", "VitrA products (HB top 36)", "İlk 36 içindeki VitrA (Artema) ürün sayısı; 0 = listede yok.", "Number of VitrA (Artema) products in the top 36; 0 = not listed.", True),
              th("VitrA değ. (HB)", "VitrA reviews (HB)", "VitrA ürünlerinin ilk 36'daki toplam değerlendirme sayısı.", "Total reviews of VitrA products in the top 36.", True),
              th("Not", "Note", "İkinci ve üçüncü markalar, okuma yöntemi.", "Second and third brands, reading method.")],
             [[x(*kat_), veri_m(ty_m) if ty_m != "-" else n("-"), _cs(ty_p), _cs(vt_n), _cs(vt_p), veri_m(hb_m) if hb_m != "-" else n("-"), _cs(hb_d), _cs(vh_n), _cs(vh_d), x(*CS_NOT[kat_[0]])]
              for kat_, ty_m, ty_p, vt_n, vt_p, hb_m, hb_d, vh_n, vh_d in CS], "uzun")
FB = [("Klozet", "WC", "7.500", "15.848", "6.962", "13.910", "~2x"), ("Klozet kapağı", "Toilet seat", "619", "1.670 (Integra)", "670", "2.190", "~3x"),
      ("Lavabo", "Washbasin", "2.930", "8.134", "1.635", "6.948", "3-4x"), ("Banyo dolabı / mobilya", "Bathroom cabinet / furniture", "6.400", "15.887", "2.148", "13.100", "2,5-6x"),
      ("Rezervuar iç takım", "Inner mechanism", "281", "896-1.131", "490", "837", "~2-4x"), ("Klozet takımı (set)", "WC set", "-", "11.999-16.735", "8.000-12.000", "13.200-17.600", "~1,5x")]
T_FB = tablo([th("Kategori", "Category", "Fiyat karşılaştırılan kategori.", "Category compared on price."),
              th("Trendyol kategori medyanı", "Trendyol category median", "Çok satan ilk 36 ürünün medyan fiyatı, TL.", "Median price of the top 36 bestsellers, TL.", True),
              th("VitrA Trendyol", "VitrA on Trendyol", "VitrA marka filtresindeki çok satan ilk 36'nın medyanı, TL.", "Median of VitrA's top 36 bestsellers under the brand filter, TL.", True),
              th("Hepsiburada kategori medyanı", "Hepsiburada category median", "Çok satan ilk 36 ürünün medyan fiyatı, TL.", "Median price of the top 36 bestsellers, TL.", True),
              th("VitrA Hepsiburada", "VitrA on Hepsiburada", "VitrA marka filtreli ilk 36 medyanı, TL.", "Median of VitrA's brand-filtered top 36, TL.", True),
              th("VitrA / kategori", "VitrA / category", "VitrA ürünlerinin medyan fiyatının, kategorinin çok satan ürünlerinin medyan fiyatına oranı; iki pazaryeri aralığı, yuvarlanmıştır.", "Ratio of the median price of VitrA products to the median price of the category's best sellers; range across the two marketplaces, rounded.", True)],
             [[x(a, b), n(c), n(d), n(e), n(f), n(g)] for a, b, c, d, e, f, g in FB])
MK = AP["miknatis"]
MK_EN = {"Klozet kapağı (menteşe, adaptör dahil)": "Toilet seats (incl. hinges and adapters)", "Rezervuar iç takımı & şamandıra": "Cistern inner mechanisms and float valves", "Musluk başlığı, perlatör & uzatma": "Tap heads, aerators and extensions", "Banyo aksesuarı, raf & düzenleyici": "Bathroom accessories, shelves and organisers", "Banyo paspası, duş perdesi & tekstil": "Bath mats, shower curtains and textiles", "Taharet musluğu & ara musluk": "Bidet valves and stop valves", "Sifon, gider & süzgeç": "Siphons, drains and strainers", "Duş seti, başlığı & hortumu": "Shower sets, heads and hoses", "Klozet kapağı": "Toilet seat", "Banyo aksesuarı & düzenleyici": "Bathroom accessories and organisers",
         "Rezervuar & iç takım": "Cisterns and inner mechanisms", "Havlupan & havluluk": "Towel radiators and rails", "Silikon & yapıştırıcı": "Silicone and adhesives", "Tesisat & yedek parça": "Plumbing and spare parts", "Kartuş & perlatör": "Cartridges and aerators", "Musluk başlığı & perlatör": "Tap heads and aerators"}
SITES = ["trendyol", "hepsiburada", "n11", "amazon", "koctas", "bauhaus", "ikea", "tekzen", "akakce", "cimri"]
mrows = []
for m in sorted([m_ for m_ in MK if sum(m_.get(s_) or 0 for s_ in SITES) >= 5000], key=lambda m: -sum(m.get(s) or 0 for s in SITES)):
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
 x("Pazaryerleri iki kaynakla incelenmiştir: Ahrefs ile Trendyol, Hepsiburada ve sekiz perakende ve karşılaştırma sitesinin banyo kategorilerinden aldığı organik trafik; site üzerinde Trendyol ve Hepsiburada'nın kategori yapısı, çok satan sıralamaları, marka filtreleri ve arama önerileri. Değerlendirme sayısı satış adedine yaklaşık bir gösterge olarak kullanılmıştır.",
   "Marketplaces were examined with two sources: with Ahrefs, the organic traffic Trendyol, Hepsiburada and eight retail and comparison sites receive from bathroom categories; on the sites themselves, the category structure, bestseller rankings, brand filters and search suggestions of Trendyol and Hepsiburada. Review count is used as an approximate indicator of units sold."),
 kpi_kart(k(cek_ty), "Trendyol banyo kategorilerinin aylık organik trafiği (Ahrefs, alt sınır)", "Monthly organic traffic of Trendyol bathroom categories (Ahrefs, lower bound)"),
 kpi_kart("%11,8", "VitrA'nın Trendyol klozet kategorisindeki listeleme payı · lavabo %3,2, banyo dolabı %0,4", "VitrA's listing share in the Trendyol WC category · washbasin 3.2%, bathroom cabinet 0.4%", "hi"),
 kpi_kart("%69", "Hepsiburada'da VitrA ürünlerinde buybox'ın üçüncü taraf satıcıdaki payı", "Share of the buybox held by third-party sellers for VitrA products on Hepsiburada", "dn"),
 kpi_kart("1,5x-6x", "Pazaryerindeki VitrA ürünlerinin medyan fiyatının kategorinin çok satan ürünlerine oranı (takım klozet ~1,5x, klozet ~2x, lavabo 3-4x, banyo dolabı 6x'e kadar)", "Ratio of the median price of VitrA products on marketplaces to the category's best sellers (WC set ~1.5x, WC ~2x, washbasin 3-4x, bathroom cabinet up to 6x)", "dn"),
 x("Banyo trafiği hangi sitelerde?", "Which sites carry bathroom traffic?"),
 T_SITE,
 insight("Banyonun ana kategorilerinde organik trafik Trendyol (%s), Koçtaş (%s) ve Hepsiburada'da (%s) toplanmaktadır; Akakçe ve Cimri gibi fiyat karşılaştırma siteleri de toplam %s ile Amazon ve n11'in önündedir. Trendyol'da trafiğin yaklaşık %%61'i kategori, %%25'i arama ve koleksiyon sayfalarından gelmekte, ürün sayfalarının payı %%3'te kalmaktadır; bu dağılım, banyo kararının pazaryerinde kategori listesi üzerinden verildiğine işaret etmektedir. SSG, üç büyük sitede banyo trafiğinin %%21-24'ünü, BM Trendyol'da %%25'ini, IKEA'da %%60'ını oluşturmaktadır." % (k(cek_ty), k(cek_ko), k(cek_hb), k(72439 + 31886)),
         "Organic traffic in the main bathroom categories concentrates on Trendyol (%s), Koçtaş (%s) and Hepsiburada (%s); price comparison sites Akakçe and Cimri together (%s) are ahead of Amazon and n11. On Trendyol about 61%% of traffic comes from category pages and 25%% from search and collection pages, while product pages stay at 3%%; this distribution indicates that the bathroom decision on the marketplace is made through category listings. SSG makes up 21-24%% of bathroom traffic on the three large sites, BM 25%% on Trendyol and 60%% on IKEA." % (k(cek_ty), k(cek_ko), k(cek_hb), k(72439 + 31886)), "D17"),
 x("Alt kategori trafiği: Trendyol ve Hepsiburada", "Sub-category traffic: Trendyol and Hepsiburada"),
 T_ALT,
 insight("Trendyol'da banyo trafiğini en çok getiren alt kategoriler çamaşır makinesi dolabı (%s), batarya (%s), duşakabin (%s) ve banyo dolabıdır (%s); klozet (%s) ve klozet kapağı bunların gerisindedir. Hepsiburada'da ise batarya ilk sıradadır. Banyoya bitişik boy aynası, evye ve seramik sayfaları da ana kategoriler kadar trafik almaktadır. VitrA'nın pazaryerinde görünür olduğu klozet ve iç takım, pazaryeri trafiğinin küçük bir bölümünü oluşturmaktadır; trafiğin büyük kısmı VitrA'nın sınırlı göründüğü mobilya, duşakabin ve armatür kategorilerindedir." % (k(ty["Çamaşır makinesi dolabı"]["trafik"]), k(ty["Batarya & musluk (banyo)"]["trafik"]), k(ty["Duşakabin & duş teknesi"]["trafik"]), k(ty["Banyo dolabı"]["trafik"]), k(ty["Klozet & pisuvar"]["trafik"])),
         "On Trendyol the sub-categories bringing the most bathroom traffic are washing machine cabinets (%s), taps (%s), shower enclosures (%s) and bathroom cabinets (%s); WCs (%s) and toilet seats trail behind. On Hepsiburada taps rank first. Bathroom-adjacent full-length mirror, sink and tile pages receive as much traffic as the core categories. The WCs and inner mechanisms where VitrA is visible on the marketplace make up a small part of marketplace traffic; most traffic sits in furniture, shower enclosure and tap categories where VitrA has limited presence." % (k(ty["Çamaşır makinesi dolabı"]["trafik"]), k(ty["Batarya & musluk (banyo)"]["trafik"]), k(ty["Duşakabin & duş teknesi"]["trafik"]), k(ty["Banyo dolabı"]["trafik"]), k(ty["Klozet & pisuvar"]["trafik"])), "D17"),
 x("Kategori yapısı ve VitrA'nın listeleme payı", "Category structure and VitrA's listing share"),
 T_KY,
 insight("VitrA, Hepsiburada'da Banyo ve Mutfak kategorisinde 3.191 ürünle incelenen markalar içinde en geniş listelemeye sahiptir (Creavit 1.975, Artema 1.938, Kale 1.376); Trendyol'da marka filtresi 2.781 listeleme göstermektedir. Buna karşın listelemenin büyük kısmı batarya, duş, rezervuar, tesisat ve aksesuardadır; klozet, lavabo, pisuvar ve banyo dolabı Trendyol'daki VitrA listelemesinin yaklaşık %18'idir. Banyo mobilyasında (25.973 ürün) VitrA payı %0,4, duşakabinde %0,1'dir.",
         "On Hepsiburada VitrA has the widest listing among the brands examined in the Bathroom and Kitchen category with 3,191 products (Creavit 1,975, Artema 1,938, Kale 1,376); on Trendyol the brand filter shows 2,781 listings. Most listings, however, are in taps, showers, cisterns, plumbing and accessories; WCs, washbasins, urinals and bathroom cabinets make up about 18% of VitrA's Trendyol listings. In bathroom furniture (25,973 products) VitrA's share is 0.4%, and 0.1% in shower enclosures.", "D21", "D22"),
 x("Çok satanlarda kim önde?", "Who leads the bestseller lists?"),
 T_CS,
 insight("Pazaryerinde çok satan listeleri orta fiyatlı yerel markalar ve jenerik ürünler taşımaktadır: lavaboda Turkuaz, klozette Turavit ve Turkuaz, banyo dolabında KAREN BANYO ve ÖZCEDEN, duşakabinde Durul, klozet kapağında Visam, ELİTRA ve NKP. VitrA'nın çok satanlarda güçlü olduğu alan yedek parça niteliğindeki ürünlerdir: rezervuar iç takımında iki pazaryerinde de ilk sıralarda yer almakta, Hepsiburada'da klozet kapağında 8 ürünle en kalabalık marka olmaktadır; Integra universal klozet kapağı Trendyol'da 471, Hepsiburada'da 622 değerlendirmeye ulaşmıştır. Artema, Hepsiburada'da evye bataryasında (6 ürün, 1.269 değ.) ve ürün sayfasında 2.313 değerlendirmeye ulaşan Solid S lavabo bataryasında güçlüdür; Trendyol'da ise batarya çok satanlarının ilk sıralarında görünmemektedir.",
         "Bestseller lists on the marketplace are carried by mid-priced local brands and generic products: Turkuaz in washbasins, Turavit and Turkuaz in WCs, KAREN BANYO and ÖZCEDEN in bathroom cabinets, Durul in shower enclosures, Visam, ELİTRA and NKP in toilet seats. VitrA is strong in spare-part-type products: it ranks at the top for cistern inner mechanisms on both marketplaces and is the most represented brand in toilet seats on Hepsiburada with 8 products; the Integra universal toilet seat has reached 471 reviews on Trendyol and 622 on Hepsiburada. Artema is strong on Hepsiburada in kitchen taps (6 products, 1,269 reviews) and the Solid S basin tap, whose product page has reached 2,313 reviews; on Trendyol it does not appear at the top of the tap bestseller lists.", "D21", "D22"),
 x("Fiyat konumu", "Price position"),
 T_FB,
 insight("Pazaryerindeki VitrA ürünlerinin medyan fiyatı, kategorinin çok satan ürünlerinin medyanının üzerindedir: fark takım klozette ~1,5x ile en dar, banyo dolabında 6x'e kadar ile en geniştir. İç takım ve klozet kapağı gibi düşük fiyatlı ürünlerde fark 2-4x bandındadır.",
         "The median price of VitrA products on marketplaces is above the median of the category's best sellers: the gap is narrowest in WC sets at ~1.5x and widest in bathroom cabinets at up to 6x. In low-priced products such as inner mechanisms and toilet seats the gap is in the 2-4x band.", "D21", "D22"),
 x("Satıcı yapısı, hizmet ve arama önerileri", "Seller structure, services and search suggestions"),
 marks([("at", "Trendyol'da VitrA mağazasında (İNTEMA) 833 ürün bulunmakta, mağaza puanı 8,7'dir; marka filtresinde 2.781 listeleme vardır. VitrA marka filtresindeki çok satan ilk 36 ürünün 19'u 12 farklı üçüncü taraf satıcıdadır; en çok değerlendirilen Integra klozet kapağının satıcısı da üçüncü taraftır", "Trendyol: VitrA store (İNTEMA) 833 products, rating 8.7; 2,781 listings under the brand filter. 19 of the top 36 bestsellers under the VitrA brand filter are with 12 different third-party sellers; the most-reviewed Integra toilet seat is also sold by a third party"),
        ("at", "Hepsiburada'da 210 benzersiz VitrA ürününde buybox VitrA mağazasında %19, Hepsiburada'da %13, üçüncü taraf satıcılarda %69'dur (yuvarlama nedeniyle toplam %101); Artema için ayrı mağaza görünmemektedir", "Hepsiburada: across 210 unique VitrA products the buybox is with the VitrA store 19%, Hepsiburada 13%, third-party sellers 69% (101% in total due to rounding); no separate Artema store is visible"),
        ("at", "Hepsiburada'da montaj ayrı hizmet ürünü olarak satılmaktadır (Mr Usta klozet montajı 2.730 TL, batarya montajı 1.375 TL); incelenen VitrA ürün kartlarında kurulum etiketi yer almamaktadır", "On Hepsiburada installation is sold as a separate service product (Mr Usta WC installation 2,730 TL, tap installation 1,375 TL); the VitrA product cards examined carry no installation label"),
        ("up", "Set ürünler klozet, iç takım ve lavabo dolabında Hepsiburada ilk 36'nın yaklaşık yarısını oluşturmaktadır; klozet takımlarında çok satan bant 8.000-12.000 TL'dir", "Set products make up about half of Hepsiburada's top 36 in WCs, inner mechanisms and basin units; the bestselling band for WC sets is 8,000-12,000 TL")]),
 ONER,
 insight("Arama önerileri iki pazaryerinde de VitrA için yedek parça ve SSG niyetini, Artema için armatür niyetini göstermektedir. Hepsiburada'da \"vitra\" yazıldığında kategori önerisi doğrudan Rezervuar İç Takımlar'dır. Montaj hizmeti ise Hepsiburada'da ayrı bir kategoride ve üçüncü taraf hizmet satıcısı üzerinden sunulmaktadır.",
         "Search suggestions on both marketplaces show spare-part and SSG intent for VitrA and tap intent for Artema. On Hepsiburada typing \"vitra\" brings Cistern Inner Mechanisms directly as the category suggestion. Installation service is offered on Hepsiburada in a separate category and through a third-party service seller.", "D21", "D22"),
 x("Düşük fiyatlı, yüksek trafikli kategoriler", "Low-priced, high-traffic categories"),
 T_MK,
 insight("Düşük fiyatlı ve yüksek trafikli kategoriler (banyo aksesuarı, duş başlığı, sifon, klozet kapağı, iç takım, taharet musluğu) pazaryerine sürekli ziyaret getirmekte ve sepete ek ürün taşıyabilmektedir. Trendyol ve Hepsiburada'da 700 TL altı en çok değerlendirilen ürünler duş başlığı (5 fonksiyonlu, 167-450 TL, 2.800-7.400 değ.), yapışkanlı raf (199 TL, 19.877 değ.) ve gider koku önleyicidir (130 TL, 5.405 değ.); VitrA'nın bu banttaki karşılığı conta gibi küçük parçalar ve Artema filtreli ara musluktur (ara musluk 340-427 TL, 309-1.120 değ.); klozet kapağı ve iç takım bu bandın üzerindedir. vitra.com.tr'de bu ürünlerin tek sayfada, ürün koduna göre bulunabilmesi hem arama trafiği hem de ana ürün satışına geçiş için giriş kapısı olabilir.",
         "Low-priced, high-traffic categories (bathroom accessories, shower heads, siphons, toilet seats, inner mechanisms, bidet valves) bring a steady stream of visits to the marketplace and can carry add-on products into the basket. The most-reviewed products under 700 TL on Trendyol and Hepsiburada are shower heads (5-function, 167-450 TL, 2,800-7,400 reviews), adhesive shelves (199 TL, 19,877 reviews) and drain odour stoppers (130 TL, 5,405 reviews); VitrA's counterpart in this band is small parts such as gaskets and the Artema filtered stop valve (stop valve 340-427 TL, 309-1,120 reviews); toilet seats and inner mechanisms sit above this band. Making these products findable on one page by product code on vitra.com.tr can be an entry point both for search traffic and for moving to main product sales.", "D17", "D21", "D22"),
 kaynak("Ahrefs Site Explorer top pages ve organic keywords (TR, 28.09.2026) · Trendyol ve Hepsiburada kategori, çok satan, marka filtresi ve arama önerisi sayfaları (tarayıcı, 29.09.2026)", "Ahrefs Site Explorer top pages and organic keywords (TR, 28.09.2026) · Trendyol and Hepsiburada category, bestseller, brand filter and search suggestion pages (browser, 29.09.2026)", "D17", "D21", "D22"),
)
