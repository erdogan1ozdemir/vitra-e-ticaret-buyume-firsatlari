# -*- coding: utf-8 -*-
"""Bolum: Katalog ve talep eslesmesi + pazaryeri gorunumu (Trendyol)."""
from ortak import *
from urllib.parse import quote as _q
import json as _json
_TURL = _json.load(open(os.path.join(veri.V, "islenmis", "trendyol_ozet_url.json"), encoding="utf-8"))["url"]
import tema
KTT = KT["tema"]
GR_EN = {"SSG": "SSG", "BM": "BM", "Armatür-Duş": "Taps and showers", "Yıkanma": "Bathing areas", "Karo": "Tiles", "Aksesuar": "Accessories", "Bitişik": "Adjacent"}
_EK_TEMA = {"havlupan"}   # bitisik grupta olup katalogda urunu bulunan tema
import tema as _tema
def _durum(tk, v):
    if tk in _tema.META: return _tema.META[tk]["durum"]   # Bolum 12 ile ayni durum degerlendirmesi
    if tk == "hela": return "Kısmi"   # sitede 1 urun; urun haritasinda yok
    u_ = v["urun"] or 0
    return "Var" if u_ >= 20 else ("Kısmi" if u_ >= 1 else "Yok")
DUR_EN = {"Var": "Available", "Kısmi": "Partial", "Yok": "Not available"}
def durum(d): return '<span class="badge %s">%s</span>' % ({"Var": "b-var", "Kısmi": "b-kis", "Yok": "b-yok"}[d], x(d, DUR_EN[d]))
NOT = {
 "hela": ("Sitede 1 ürün; ürün sitemap'inde yer almıyor", "1 product on the site; not included in the product sitemap"),
 "havlupan": ("Artepan, Voyage", "Artepan, Voyage"),
 "akilli_klozet": ("7 akıllı klozet, 9 akıllı klozet seti", "7 smart WCs, 9 smart WC sets"),
 "camasir_dolap": ("Trendyol ilk 40 sonuçta yok", "Not in Trendyol's top 40"),
 "yedek": ("Yedek parça kategorisi yok; eski yedek parça sayfası tek ürünlü kategoriye yönleniyor", "No spare-parts category; the old spare-parts page redirects to a one-product category"),
 "taharet_musluk": ("Taharet el duşu", "Bidet hand sprays"),
 "banyo_raf": ("Raf, kulp, ayak ve konsol", "Shelves, handles, feet and consoles"),
 "ic_takim": ("Sitede iç takım ürünleri satılıyor", "Inner mechanisms are sold on the site"),
 "rezervuar": ("Duvar önü rezervuar", "Exposed cistern"),
 "lavabo_dolap": ("Model başına ~28 renk ve ölçü varyantı", "~28 colour and size variants per model"),
  "dusakabin": ("Ürün sayfasında montaj seçeneği yok", "No installation option on the product page"),
}
rows = []
for tk, v in sorted(KTT.items(), key=lambda i: -i[1]["v12"]):
    if v["grup"] not in GR_EN or (v["grup"] == "Bitişik" and tk not in _EK_TEMA): continue
    nt = NOT.get(tk)
    rows.append([x(v["grup"], GR_EN[v["grup"]]), x(v["tr"], tema.META[tk]["en"]), cellk(v["v12"]), n(yz(v["uc"])), cell(v["urun"]) if v["urun"] else n("-"), cell(v["model"]) if v["model"] else n("-"), durum(_durum(tk, v)), x(*nt) if nt else n("-")])
tbl = tablo([th("Grup", "Group", "Tema grubu.", "Theme group."),
             th("Tema", "Theme", "Genişletilmiş kelime evreninde tanımlanan ürün teması.", "Product theme defined in the expanded keyword universe."),
             th("Aylık talep", "Monthly demand", "Eyl 2025 - Ağu 2026 aylık ortalama arama hacmi; yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 average monthly search volume; spelling variants counted once.", True),
             th("3 yıllık değişim", "3-year change", "Eyl 2022 - Ağu 2023 ile Eyl 2025 - Ağu 2026 ortalamaları arasındaki değişim.", "Change between the Sep 2022 - Aug 2023 and Sep 2025 - Aug 2026 averages.", True),
             th("VitrA ürün", "VitrA products", "vitra.com.tr ürün sitemap'inde temaya eşlenen ürün adresi sayısı; renk ve ölçü varyantları ayrı sayılır.", "Number of product URLs in the vitra.com.tr product sitemap mapped to the theme; colour and size variants counted separately.", True),
             th("Model", "Models", "Renk ekleri ayıklanmış tekil ürün adı sayısı (yaklaşık).", "Approximate number of unique product names after removing colour suffixes.", True),
             th("Durum", "Status", "VitrA kataloğunda temanın karşılığı: Var (temada yeterli ürün derinliği), Kısmi (ürün var ama derinlik ya da kategori sayfası sınırlı), Yok (ürün yok); Yeni Kategori bölümüyle aynı değerlendirmedir.", "Coverage of the theme in the VitrA catalogue: Available (sufficient product depth), Partial (products exist but depth or a category page is limited), Not available (no products); the same assessment as the New Categories section."),
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
    vf = v.get("vitra_fiyat"); vb = v.get("vitra_fiyat_bant"); ab = v.get("artema_fiyat_bant")
    vfh = cell(vf) if vf else (n(x(vb.split(" (")[0], vb.split(" (")[0].replace(".", ","))) if vb else (n(x("Artema " + ab, "Artema " + ab.replace(".", ","))) if ab else n("-")))
    ld = "Markasız (Genel Markalar)" if lead[0] == "Genel Markalar" else lead[0]
    trows.append([veri_m(q), cell(v["n"]), cell(med) if med else n("-"), cell(vu) if vu else n("-"), vfh, u(_TURL.get(q) or ("https://www.trendyol.com/sr?q=" + _q(lead[0] + " " + q) + "&sst=MOST_RATED"), ld), cell(lead[1]), cell(lead[2]), x(v["not"], TY_NOT_EN[q])])
tbl2 = tablo([th("Trendyol araması", "Trendyol search", "Trendyol arama kutusuna yazılan ifade.", "Phrase typed into the Trendyol search box."),
              th("İncelenen ürün", "Products examined", "İncelenen ilk sonuç sayısı.", "Number of top results examined (150 for inner mechanisms).", True),
              th("Medyan fiyat (TL)", "Median price (TL)", "İncelenen ürünlerin medyan satış fiyatı; havlupanda yalnız ısıtıcılı havlupanlar, iç takımda jenerik ürünler; set listelerinde ürün kapsamı farklı olduğu için medyan hesaplanmamıştır.", "Median sale price of the products examined; heated towel rails only for towel radiators, generic products for inner mechanisms; not calculated for set lists because product scope differs.", True),
              th("VitrA / Artema ürün", "VitrA / Artema products", "İlk sonuçlarda VitrA veya Artema markalı ürün sayısı.", "Number of VitrA or Artema products in the top results.", True),
              th("VitrA fiyatı (TL)", "VitrA price (TL)", "İlk sonuçlardaki VitrA ürününün fiyatı veya fiyat bandı; VitrA yoksa Artema.", "Price or price band of the VitrA product in the top results; Artema if VitrA is absent.", True),
              th("En çok değerlendirilen marka", "Most-reviewed brand", "İlk sonuçlarda değerlendirme sayısı en yüksek ürünün markası; bağlantı ürün sayfasını yeni sekmede açar.", "Brand of the most-reviewed product among the top results; the link opens the product page in a new tab."),
              th("Fiyat (TL)", "Price (TL)", "Bu ürünün satış fiyatı, 29.09.2026.", "Sale price of this product, 29.09.2026.", True),
              th("Değerlendirme sayısı", "Reviews", "Bu ürünün değerlendirme sayısı; satış hacmi göstergesi olarak kullanılmıştır.", "Review count of this product; used as a sales volume indicator.", True),
              th("Gözlem", "Observation", "Sonuç sayfasının genel görünümü.", "General view of the results page.")], trows, "uzun")
bd, cm, ay, ic = TY["banyo dolabı"], TY["çamaşır makinesi dolabı"], TY["ledli banyo aynası"], TY["rezervuar iç takımı"]
HTML = """
<p class="lede">%s</p>
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("vitra.com.tr ürün sitemap'indeki 7.804 ürün adresi temalara eşlenerek her temadaki katalog derinliği arama talebiyle karşılaştırılmıştır. Aynı temaların Trendyol'daki fiyat bandı, öne çıkan satıcıları ve VitrA varlığı da incelenmiştir. Talep burada genişletilmiş kelime evreninde tema bazında hesaplandığı için Bölüm 03 ve 04'teki kategori değişimleriyle doğrudan karşılaştırılmamalıdır.",
   "The 7,804 product URLs in the vitra.com.tr product sitemap have been mapped to themes, and catalogue depth in each theme compared with search demand. The price band, leading sellers and VitrA presence of the same themes on Trendyol are also examined. Demand here is calculated by theme in the expanded keyword universe and should not be compared directly with the category changes in Sections 03 and 04."),
 tbl,
 insight("Katalog derinliği ile talep arasında dört belirgin uyumsuzluk dikkat çekmektedir: (1) hela taşında aylık %s arama karşısında sitede 1 ürün bulunmaktadır, (2) havlupanda %s aramaya karşılık 2 ürün yer almaktadır, (3) çamaşır ve kurutma makinesi dolabında %s arama ve 29 ürün bulunmasına rağmen Trendyol ilk 40 sonucunda VitrA ürünü yer almamaktadır, (4) yedek parçada (şamandıra, menteşe, kartuş, iç takım aramaları) tüketiciye açık bir kategori bulunmamaktadır. Eski online.vitra.com.tr'deki yedek parça kategorisi Search Console'a göre Haziran - Kasım 2025 arasında ayda ortalama 300 civarında tık almış; bu adres bugün tek ürünlü \"Yıkanma Alanı Tamamlayıcı Ürünler\" kategorisine yönlenmektedir." % (k(KTT["hela"]["v12"]), k(KTT["havlupan"]["v12"]), k(KTT["camasir_dolap"]["v12"])),
         "There are four clear mismatches between catalogue depth and demand: (1) 1 product on the site against %s monthly searches for squat toilets, (2) 2 products against %s searches for towel radiators, (3) no marketplace visibility for washing machine cabinets despite %s searches and 29 products, (4) no consumer-facing spare-parts category (searches for float valves, hinges, cartridges, inner mechanisms). The spare-parts category on the old online.vitra.com.tr received about 300 clicks per month on average between June and November 2025; that address now redirects to the one-product \"Bathing Area Complementary Products\" category." % (k(KTT["hela"]["v12"]), k(KTT["havlupan"]["v12"]), k(KTT["camasir_dolap"]["v12"])), "D12", "D13", "D2"),
 x("Pazaryerindeki görünüm: Trendyol", "Marketplace view: Trendyol"),
 tbl2,
 insight("Pazaryerinde VitrA iki farklı konumda görünmektedir. Yedek parça niteliğindeki ürünlerde (rezervuar iç takımı) listelemelerin yaklaşık beşte birini oluşturmakta ve ilk sırada yer almaktadır; jenerik iç takımlar ise %s TL civarındaki fiyatla daha fazla değerlendirme toplamaktadır. Banyo mobilyası ve ayna gibi üzerinde düşünülerek alınan ürünlerde ise VitrA ürünleri pazar medyanının birkaç katı fiyatla tek tük görünmekte (banyo dolabında medyan %s TL, VitrA %s TL; ledli aynada medyan %s TL, VitrA %s TL), en çok değerlendirme alan ürünler düz paket mobilya markalarındadır. Bu tablo, pazaryerinde BM için VitrA'nın fiyatla değil, set, montaj ve garanti bütünlüğüyle konumlanabileceğini göstermektedir." % (bin(ic["fiyat_medyan_jenerik"]), bin(bd["fiyat_medyan"]), bin(bd["vitra_fiyat"]), bin(ay["fiyat_medyan"]), bin(ay["vitra_fiyat"])),
         "On the marketplace VitrA appears in two different positions. In spare-part-type products (cistern inner mechanisms) it makes up about a fifth of listings and holds the first place, while generic mechanisms collect more reviews at around %s TL. In considered purchases such as bathroom furniture and mirrors, VitrA products appear sparsely at several times the market median (bathroom cabinet median %s TL, VitrA %s TL; LED mirror median %s TL, VitrA %s TL), and the most-reviewed products belong to flat-pack furniture brands. This shows that on the marketplace VitrA can position BM not on price but on a combined set, installation and warranty offer." % (bin(ic["fiyat_medyan_jenerik"]), bin(bd["fiyat_medyan"]), bin(bd["vitra_fiyat"]), bin(ay["fiyat_medyan"]), bin(ay["vitra_fiyat"])), "D15"),
 kaynak("vitra.com.tr ürün sitemap'i (7.804 adres) ve kategori sayfaları · Google Ads Keyword Planner genişletilmiş evren · Trendyol arama sonuçları · 29.09.2026 · %s" % veri.TARIH,
        "vitra.com.tr product sitemap (7,804 URLs) and category pages · Google Ads Keyword Planner expanded universe · Trendyol search results · 29.09.2026 · %s" % veri.TARIH, "D13", "D12", "D15"),
)
