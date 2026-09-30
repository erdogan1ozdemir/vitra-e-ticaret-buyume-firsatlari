# -*- coding: utf-8 -*-
"""Bolum: Katalog ve talep eslesmesi + pazaryeri gorunumu (Trendyol)."""
from ortak import *
from urllib.parse import quote as _q
import tema
KTT = KT["tema"]
GR_EN = {"SSG": "SSG", "BM": "BM", "Armatür-Duş": "Taps and showers", "Yıkanma": "Bathing areas", "Karo": "Tiles", "Aksesuar": "Accessories"}
DUR_EN = {"Var": "Available", "Kısmi": "Partial", "Yok": "Not available"}
def durum(d): return '<span class="badge %s">%s</span>' % ({"Var": "b-var", "Kısmi": "b-kis", "Yok": "b-yok"}[d], x(d, DUR_EN[d]))
NOT = {
 "hela": ("Sitede 1 ürün; ürün sitemap'inde yer almıyor", "1 product on the site; not included in the product sitemap"),
 "havlupan": ("2 ürün (Artepan, Voyage)", "2 products (Artepan, Voyage)"),
 "akilli_klozet": ("7 akıllı klozet, 9 akıllı klozet seti", "7 smart WCs, 9 smart WC sets"),
 "camasir_dolap": ("29 ürün, 6 model; Trendyol ilk 40 sonuçta yok", "29 products, 6 models; not in Trendyol's top 40"),
 "yedek": ("Yedek parça kategorisi yok; eski yedek parça sayfası tek ürünlü kategoriye yönleniyor", "No spare-parts category; the old spare-parts page redirects to a one-product category"),
 "taharet_musluk": ("10 taharet el duşu", "10 bidet hand sprays"),
 "banyo_raf": ("Raf, kulp, ayak ve konsol 22 ürün", "22 shelves, handles, feet and consoles"),
 "ic_takim": ("25 ürün; Trendyol'da ilk sırada", "25 products; first place on Trendyol"),
 "rezervuar": ("9 ürün (duvar önü rezervuar)", "9 products (exposed cisterns)"),
 "lavabo_dolap": ("1.003 renk ve ölçü varyantı, 36 model", "1,003 colour and size variants, 36 models"),
 "karo": ("2.098 ürün", "2,098 products"),
 "dusakabin": ("301 ürün; ürün sayfasında montaj seçeneği yok", "301 products; no installation option on the product page"),
}
rows = []
for tk, v in sorted(KTT.items(), key=lambda i: -i[1]["v12"]):
    if v["grup"] not in GR_EN: continue
    nt = NOT.get(tk)
    rows.append([x(v["grup"], GR_EN[v["grup"]]), x(v["tr"], tema.META[tk]["en"]), cell(v["v12"]), n(yz(v["uc"])), cell(v["urun"]) if v["urun"] else n("-"), cell(v["model"]) if v["model"] else n("-"), durum(v["durum"]), x(*nt) if nt else "-"])
tbl = tablo([th("Grup", "Group", "Tema grubu.", "Theme group."),
             th("Tema", "Theme", "Genişletilmiş kelime evreninde tanımlanan ürün teması.", "Product theme defined in the expanded keyword universe."),
             th("Aylık talep", "Monthly demand", "Eyl 2025 - Ağu 2026 aylık ortalama arama hacmi; yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 average monthly search volume; spelling variants counted once.", True),
             th("3 yıllık değişim", "3-year change", "Eyl 22 - Ağu 23 ile Eyl 25 - Ağu 26 ortalamaları arasındaki değişim.", "Change between the Sep 22 - Aug 23 and Sep 25 - Aug 26 averages.", True),
             th("VitrA ürün", "VitrA products", "vitra.com.tr ürün sitemap'inde temaya eşlenen ürün adresi sayısı; renk ve ölçü varyantları ayrı sayılır.", "Number of product URLs in the vitra.com.tr product sitemap mapped to the theme; colour and size variants counted separately.", True),
             th("Model", "Models", "Renk ekleri ayıklanmış tekil ürün adı sayısı (yaklaşık).", "Approximate number of unique product names after removing colour suffixes.", True),
             th("Durum", "Status", "VitrA kataloğunda temanın karşılığı: Var, Kısmi (sınırlı derinlik), Yok.", "Coverage of the theme in the VitrA catalogue: Available, Partial (limited depth), Not available."),
             th("Not", "Note", "Katalog ve pazaryeri gözlemi.", "Catalogue and marketplace observation.")], rows, "uzun")
TY_EN = {"banyo dolabı": "bathroom cabinet", "suya dayanıklı banyo dolabı": "water-resistant bathroom cabinet", "çamaşır makinesi dolabı": "washing machine cabinet", "ledli banyo aynası": "LED bathroom mirror",
         "granit evye": "granite sink", "arıtmalı batarya": "purifier tap", "havlupan": "towel radiator", "klozet taharet aparatı": "WC bidet attachment", "çocuk klozet adaptörü": "child toilet seat adapter",
         "engelli tutunma barı": "accessible grab bar", "klozet lavabo seti": "WC and washbasin set", "rezervuar iç takımı": "cistern inner mechanism", "batarya kartuşu": "tap cartridge"}
TY_NOT_EN = {
 "banyo dolabı": "Almost all of the top 45 results are flat-pack furniture brands (MOBİLİQUE, Bofigo, KZY, Montenero, FURNICI); the only VitrA product is a basin set at 14,462 TL",
 "granit evye": "RealStone makes up about half the listings; review counts are low, the category has not matured on the marketplace",
 "çocuk klozet adaptörü": "Baby-product brands and generic sellers; no WC brand",
 "rezervuar iç takımı": "VitrA holds about 22% of listings and the first place; generic mechanisms sit at 280-480 TL and collect more reviews",
 "suya dayanıklı banyo dolabı": "14 of 40 results are MOBİLİQUE and 7 Bofigo; emphasis on PVC and water-resistant bodies",
 "çamaşır makinesi dolabı": "VitrA lists 29 washing machine cabinets on its site but does not appear in Trendyol's top 40",
 "ledli banyo aynası": "Decoration and mirror workshop brands; VitrA has one product at about 8 times the market median",
 "arıtmalı batarya": "Water purifier brands and generic sellers; no tap brand (VitrA, Artema, Eca, Grohe) in the top 40",
 "havlupan": "About half the results are low-priced towel rails and hooks, not radiators; heated towel rails led by Eca, Toprak, DG Therm, Termofer",
 "batarya kartuşu": "Review counts are low (max 30); generic cartridges 120-350 TL, original Artema and Eca cartridges 465-735 TL",
 "klozet taharet aparatı": "Most results come from medical suppliers; very few reviews, the category has not settled on the marketplace",
 "engelli tutunma barı": "Stainless steel makers and generic sellers; VitrA is the only bathroom brand, with one product",
 "klozet lavabo seti": "WC + cistern + seat sets dominate; no complete set with WC, basin and cabinet in the top 40. The İDEVİT set bundles fitting parts (bidet valve, hose, inner mechanism)"}
trows = []
for q, v in TY.items():
    med = v.get("fiyat_medyan") or v.get("fiyat_medyan_jenerik") or v.get("fiyat_medyan_gercek_havlupan")
    vu = v.get("vitra_urun", 0) + v.get("artema_urun", 0)
    lead = v["one_cikan"][0]
    trows.append([veri_m(q), cell(v["n"]), cell(med) if med else n("-"), cell(vu) if vu else n("-"), u("https://www.trendyol.com/sr?q=" + _q(lead[0] + " " + q), lead[0]), cell(lead[1]), cell(lead[2]), x(v["not"], TY_NOT_EN[q])])
tbl2 = tablo([th("Trendyol araması", "Trendyol search", "Trendyol arama kutusuna yazılan ifade.", "Phrase typed into the Trendyol search box."),
              th("İncelenen ürün", "Products examined", "İncelenen ilk sonuç sayısı.", "Number of top results examined.", True),
              th("Medyan fiyat (TL)", "Median price (TL)", "İncelenen ürünlerin medyan satış fiyatı; havlupanda yalnız ısıtıcılı havlupanlar, iç takımda jenerik ürünler.", "Median sale price of the products examined; heated towel rails only for towel radiators, generic products for inner mechanisms.", True),
              th("VitrA / Artema ürün", "VitrA / Artema products", "İlk sonuçlarda VitrA veya Artema markalı ürün sayısı.", "Number of VitrA or Artema products in the top results.", True),
              th("En çok değerlendirilen marka", "Most-reviewed brand", "İlk sonuçlarda değerlendirme sayısı en yüksek ürünün markası; bağlantı Trendyol'da marka + arama ifadesiyle yapılan aramaya gider.", "Brand of the most-reviewed product among the top results; the link opens a Trendyol search for brand + phrase."),
              th("Fiyat (TL)", "Price (TL)", "Bu ürünün satış fiyatı, 29.09.2026.", "Sale price of this product, 29.09.2026.", True),
              th("Değerlendirme sayısı", "Reviews", "Bu ürünün değerlendirme sayısı; satış hacmi göstergesi olarak kullanılmıştır.", "Review count of this product; used as a sales volume indicator.", True),
              th("Gözlem", "Observation", "Sonuç sayfasının genel görünümü.", "General view of the results page.")], trows, "uzun")
bd, cm, ay, ic = TY["banyo dolabı"], TY["çamaşır makinesi dolabı"], TY["ledli banyo aynası"], TY["rezervuar iç takımı"]
HTML = """
<p class="lede">%s</p>
%s
%s
<h3>%s</h3>
<p>%s</p>
%s
%s
%s
""" % (
 x("vitra.com.tr ürün sitemap'indeki 7.804 ürün adresi temalara eşlenerek her temadaki katalog derinliği arama talebiyle karşılaştırılmıştır. İkinci bölümde aynı temaların Trendyol'daki görünümü (fiyat bandı, öne çıkan satıcılar, VitrA varlığı) incelenmiştir.",
   "The 7,804 product URLs in the vitra.com.tr product sitemap have been mapped to themes, and catalogue depth in each theme compared with search demand. The second part examines how the same themes appear on Trendyol (price band, leading sellers, VitrA presence)."),
 tbl,
 insight("Katalog derinliği ile talep arasında dört belirgin uyumsuzluk bulunmaktadır: (1) hela taşında aylık %s arama karşısında sitede 1 ürün, (2) havlupanda %s aramaya karşılık 2 ürün, (3) çamaşır makinesi dolabında %s arama ve 29 ürün bulunmasına rağmen pazaryerinde görünmeme, (4) yedek parçada (şamandıra, menteşe, kartuş, iç takım aramaları) tüketiciye açık bir kategori bulunmaması. Eski online.vitra.com.tr'deki yedek parça kategorisi Haziran - Kasım 2025 arasında ayda ortalama 300 civarında tık almış; bu adres bugün tek ürünlü \"Yıkanma Alanı Tamamlayıcı Ürünler\" kategorisine yönlenmektedir." % (k(KTT["hela"]["v12"]), k(KTT["havlupan"]["v12"]), k(KTT["camasir_dolap"]["v12"])),
         "There are four clear mismatches between catalogue depth and demand: (1) 1 product on the site against %s monthly searches for squat toilets, (2) 2 products against %s searches for towel radiators, (3) no marketplace visibility for washing machine cabinets despite %s searches and 29 products, (4) no consumer-facing spare-parts category (searches for float valves, hinges, cartridges, inner mechanisms). The spare-parts category on the old online.vitra.com.tr received about 300 clicks per month on average between June and November 2025; that address now redirects to the one-product \"Bathing Area Complementary Products\" category." % (k(KTT["hela"]["v12"]), k(KTT["havlupan"]["v12"]), k(KTT["camasir_dolap"]["v12"])), "D12", "D13", "D2"),
 x("Pazaryerindeki görünüm: Trendyol", "Marketplace view: Trendyol"),
 x("13 tema için Trendyol arama sonuçlarının ilk 40-45 ürünü 29 Eylül 2026 tarihinde incelenmiştir. Değerlendirme sayısı, pazaryerinde satış hacmine yaklaşık bir gösterge olarak kullanılmıştır.",
   "For 13 themes, the top 40-45 products in Trendyol search results were examined on 29 September 2026. Review count is used as an approximate indicator of sales volume on the marketplace."),
 tbl2,
 insight("Pazaryerinde VitrA iki farklı konumda görünmektedir. Yedek parçaya yakın ürünlerde (rezervuar iç takımı) listelemelerin yaklaşık beşte birini oluşturmakta ve ilk sırada yer almaktadır; jenerik iç takımlar ise %s TL civarındaki fiyatla daha fazla değerlendirme toplamaktadır. Banyo mobilyası ve ayna gibi karar ürünlerinde ise VitrA ürünleri pazar medyanının birkaç katı fiyatla tek tük görünmekte (banyo dolabında medyan %s TL, VitrA %s TL; ledli aynada medyan %s TL, VitrA %s TL), en çok değerlendirme alan ürünler düz paket mobilya markalarındadır. Bu tablo, pazaryerinde BM için VitrA'nın fiyatla değil, set, montaj ve garanti bütünlüğüyle konumlanabileceğini göstermektedir." % (bin(ic["fiyat_medyan_jenerik"]), bin(bd["fiyat_medyan"]), bin(bd["vitra_fiyat"]), bin(ay["fiyat_medyan"]), bin(ay["vitra_fiyat"])),
         "On the marketplace VitrA appears in two different positions. In near-spare-part products (cistern inner mechanisms) it makes up about a fifth of listings and holds the first place, while generic mechanisms collect more reviews at around %s TL. In decision products such as bathroom furniture and mirrors, VitrA products appear sparsely at several times the market median (bathroom cabinet median %s TL, VitrA %s TL; LED mirror median %s TL, VitrA %s TL), and the most-reviewed products belong to flat-pack furniture brands. This shows that on the marketplace VitrA can position BM not on price but on set, installation and warranty integrity." % (bin(ic["fiyat_medyan_jenerik"]), bin(bd["fiyat_medyan"]), bin(bd["vitra_fiyat"]), bin(ay["fiyat_medyan"]), bin(ay["vitra_fiyat"])), "D15"),
 kaynak("vitra.com.tr ürün sitemap'i (7.804 adres) ve kategori sayfaları · Google Ads Keyword Planner genişletilmiş evren · Trendyol arama sonuçları (Apify) · %s" % veri.TARIH,
        "vitra.com.tr product sitemap (7,804 URLs) and category pages · Google Ads Keyword Planner expanded universe · Trendyol search results (Apify) · %s" % veri.TARIH, "D13", "D12", "D15"),
)
