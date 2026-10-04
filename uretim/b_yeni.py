# -*- coding: utf-8 -*-
"""Bolum: Yeni kategori ve segment firsatlari (gam disi ve sinirli derinlik)."""
from ortak import *
from rapor_parca1 import barlar
import tema
KTT = KT["tema"]; TM = YK["tema"]
# tema: (rakipte kim, uyum, model TR, model EN)
R = {
 "yedek":          (("Koçtaş, Banyomarka, Trendyol jenerik satıcılar; Kale'de ürünsüz sayfa", "Koçtaş, Banyomarka, Trendyol generic sellers; empty page at Kale"), "Yakın", ("Orijinal VitrA-Artema parçası, ürün koduna göre parça bulucu", "Original VitrA-Artema part, part finder by product code")),
 "aritma_bat":     (("Franke, Arya, FLEKO, arıtma cihazı markaları", "Franke, Arya, FLEKO, purifier brands"), "Yakın", ("Artema 3 yollu batarya + filtre aboneliği", "Artema 3-way tap + filter subscription")),
 "evye":           (("Franke, Blanco, Teka, RealStone; Koçtaş, IKEA", "Franke, Blanco, Teka, RealStone; Koçtaş, IKEA"), "Yakın", ("Granit ve çelik evye + mutfak bataryası seti", "Granite and steel sink + kitchen tap set")),
 "havlupan":       (("Eca, Toprak, Kumtel, DG Therm; Koçtaş, Banyomarka", "Eca, Toprak, Kumtel, DG Therm; Koçtaş, Banyomarka"), "Yakın", ("Koleksiyon uyumlu havlupan derinliği (krom, siyah, elektrikli)", "Collection-matched towel radiator depth (chrome, black, electric)")),
 "aydinlatma":     (("IKEA, Kale, Banyomarka, ayna atölyeleri", "IKEA, Kale, Banyomarka, mirror workshops"), "Yakın", ("Ledli ayna ve aplik, BM setine bağlı", "LED mirror and wall lights, linked to BM sets")),
 "cocuk":          (("IKEA, Banyomarka, bebek ürünü markaları", "IKEA, Banyomarka, baby-product brands"), "Yakın", ("Sento çocuk serisi + adaptör ve basamak (3P)", "Sento kids series + adapter and step (3P)")),
 "engelli":        (("Bauhaus, Banyomarka, Banyoline, Kale", "Bauhaus, Banyomarka, Banyoline, Kale"), "Yakın", ("Conforma ve tutunma barlarıyla \"erişilebilir banyo\" seti", "\"Accessible bathroom\" set with Conforma and grab bars")),
 "suzgec":         (("Tekzen, Banyoline, Kale", "Tekzen, Banyoline, Kale"), "Yakın", ("Duş teknesi ve kanalı siparişine tamamlayıcı", "Complement to shower tray and channel orders")),
 "taharet_aparat": (("Kale Smartx (yalnız kendi klozetine), TOTO, Coway, medikal satıcılar", "Kale Smartx (own WC only), TOTO, Coway, medical sellers"), "Yakın", ("V-Care teknolojisinden universal kapak (uzun vade)", "Universal seat derived from V-Care technology (long term)")),
 "ticari":         (("Banyomarka, profesyonel ıslak hacim markaları", "Banyomarka, professional washroom brands"), "Orta", ("Proje kanalında temassız batarya ve pisuvarla paket", "Package with touchless taps and urinals in the project channel")),
 "yapi_kimya":     (("Kale (Kalekim), Bauhaus, Tekzen, Banyoline, Koçtaş", "Kale (Kalekim), Bauhaus, Tekzen, Banyoline, Koçtaş"), "Orta", ("Karo siparişine yapıştırıcı ve derz, iş ortağı ürünü", "Adhesive and grout added to tile orders, partner product")),
 "duzen":          (("IKEA, Bauhaus, Evidea", "IKEA, Bauhaus, Evidea"), "Orta", ("BM koleksiyonuna uyumlu raf ve düzenleyici (3P)", "Shelves and organisers matching BM collections (3P)")),
 "tekstil":        (("Bauhaus, Tekzen, Evidea, IKEA, Koçtaş", "Bauhaus, Tekzen, Evidea, IKEA, Koçtaş"), "Uzak", ("Yalnız \"banyo yenileme paketi\" içinde seçili iş ortağı", "Selected partner only within a \"bathroom renovation package\"")),
 "sicaksu":        (("Bauhaus, Tekzen, Koçtaş", "Bauhaus, Tekzen, Koçtaş"), "Orta", ("Tadilat paketinde iş ortağı ürünü + montaj", "Partner product + installation in the renovation package")),
 "aritma":         (("Bauhaus, Tekzen, uzman markalar", "Bauhaus, Tekzen, specialist brands"), "Orta", ("Arıtmalı bataryaya bağlı iş ortağı cihazı", "Partner device linked to the purifier tap")),
 "tesisat":        (("Bauhaus, Tekzen, Banyoline", "Bauhaus, Tekzen, Banyoline"), "Uzak", ("Montaj hizmeti kapsamında sarf malzeme olarak", "As consumables within the installation service")),
 "kaplama":        (("Koçtaş, Bauhaus, boya markaları", "Koçtaş, Bauhaus, paint brands"), "Uzak", ("Değerlendirme dışı; VitrA Karo ile rekabet eder", "Out of scope; competes with VitrA Tiles")),
 "mutfak_tezgah":  (("Kale, IKEA, Tekzen, taş ve kompozit üreticileri", "Kale, IKEA, Tekzen, stone and composite makers"), "Orta", ("VitrA Karo büyük ebat porselen ile ürün uygunluğu değerlendirilebilir", "Product fit can be assessed with VitrA Tiles large-format porcelain")),
 "bahce":          (("Bauhaus, yapı marketler", "Bauhaus, DIY retailers"), "Orta", ("Artema bahçe ve dış mekan musluğu", "Artema garden and outdoor tap")),
 "yumusatma":      (("Arıtma markaları", "Purifier brands"), "Uzak", ("Arıtmalı batarya ile birlikte izlenebilir", "Can be tracked together with the purifier tap")),
 "wellness":       (("Uzman ithalatçılar", "Specialist importers"), "Uzak", ("Kısa vadede değerlendirme dışı", "Out of scope in the short term")),
 "cop_ogutucu":    (("Franke, Teka", "Franke, Teka"), "Uzak", ("Evye setine opsiyon (3P)", "Option in the sink set (3P)")),
 "prefabrik":      (("Proje üreticileri", "Project manufacturers"), "Uzak", ("Proje kanalı konusu", "A project-channel topic")),
 "banyo_isitici":  (("Elektrikli ev aletleri markaları", "Small appliance brands"), "Uzak", ("Değerlendirme dışı", "Out of scope")),
 "tarti":          (("Elektrikli ev aletleri markaları", "Small appliance brands"), "Uzak", ("Değerlendirme dışı", "Out of scope")),
}
UY_EN = {"Yakın": "Close", "Orta": "Medium", "Uzak": "Distant"}
UY_CL = {"Yakın": "b-var", "Orta": "b-kis", "Uzak": "b-o3"}
DUR_EN = {"Var": "Available", "Kısmi": "Partial", "Yok": "Not available"}
rows = []; bar = []
for tk, (rk, uy, md) in sorted(R.items(), key=lambda i: -TM[i[0]]["v12"]):
    t = TM[tk]
    rows.append([x(t["tr"], tema.META[tk]["en"]), cellk(t["v12"]), n(yz(t["yoy"])), n(yz(t["uc_yil"])), '<span class="badge %s">%s</span>' % ({"Var": "b-var", "Kısmi": "b-kis", "Yok": "b-yok"}[t["durum"]], x(t["durum"], DUR_EN[t["durum"]])),
                 x(*rk), '<span class="badge %s">%s</span>' % (UY_CL[uy], x(uy, UY_EN[uy])), x(*md), '<div class="kwlist">%s</div>' % "".join(kw(w[0]) for w in t["top"][:3])])
tbl = tablo([th("Tema", "Theme", "VitrA kataloğunda bulunmayan ya da sınırlı derinlikte bulunan ürün teması.", "Product theme absent from, or thin in, the VitrA catalogue."),
             th("Aylık talep", "Monthly demand", "Eyl 2025 - Ağu 2026 aylık ortalama arama hacmi; yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 average monthly search volume; spelling variants counted once.", True),
             th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True),
             th("3 yıllık değişim", "3-year change", "Eyl 2022 - Ağu 2023 ile Eyl 2025 - Ağu 2026 ortalamaları arasındaki değişim.", "Change between the Sep 2022 - Aug 2023 and Sep 2025 - Aug 2026 averages.", True),
             th("VitrA", "VitrA", "VitrA kataloğundaki karşılık.", "Coverage in the VitrA catalogue."),
             th("Rakipte kim satıyor?", "Who sells it?", "Rakip sitelerin kategori ağaçları, Trendyol sonuçları ve Inbound'un Haziran 2026 rakip ürün analizi.", "Competitor category trees, Trendyol results and Inbound's June 2026 competitor product analysis."),
             th("VitrA'ya uyum", "Fit with VitrA", "Yakın: VitrA veya Artema üretim yetkinliğine bitişik · Orta: tamamlayıcı, iş ortağıyla sunulabilir · Uzak: marka ve kanal açısından uzak.", "Close: adjacent to VitrA or Artema manufacturing capability · Medium: complementary, can be offered with a partner · Distant: far in brand and channel terms."),
             th("Model önerisi", "Proposed model", "Temanın vitra.com.tr'de nasıl sunulabileceği; 3P = üçüncü taraf satıcı.", "How the theme could be offered on vitra.com.tr; 3P = third-party seller."),
             th("Örnek aramalar", "Example searches", "Temanın en yüksek hacimli aramaları.", "Highest-volume searches in the theme.")], rows, "uzun")
def t(k_): return TM[k_]
from b_marka import AT as _MAT
_TAMP = 100 * _MAT["Tamir ve bakım"] / sum(_MAT.values())
HTML = """
<p class="lede">%s</p>
%s
%s
<h3>%s</h3>
<div class="steps">%s%s%s%s</div>
%s
%s
""" % (
 x("Genişletilmiş kelime evreninden (52.973 kelime) %s tekil kelime, VitrA'nın bugünkü kategori ağacının dışına taşan temaları da kapsayacak şekilde temalara atanmıştır." % bin(len(YK["kelime"])) + " VitrA kataloğunda bulunmayan ya da sınırlı derinlikte bulunan temalar için talep, rakipte kimin sattığı, VitrA'ya uyum ve olası satış modeli birlikte değerlendirilmiştir; Haziran 2026 sezonsallık çalışmasındaki dört ürün kümesi (<b>yedek parça; evye; arıtmalı batarya; taharet aparatı ve universal akıllı kapak</b>) güncel veriyle yeniden ölçülmüştür.",
   "From the expanded keyword universe (52,973 keywords), %s unique keywords have been assigned to themes, including themes beyond VitrA's current category tree." % f"{len(YK['kelime']):,}" + " For themes absent from, or thin in, the VitrA catalogue, demand, who sells them, fit with VitrA and a possible sales model are assessed together; the four product clusters from the June 2026 seasonality study (<b>spare parts; sinks; purifier taps; bidet attachments and universal smart seats</b>) have been re-measured with current data."),
 tbl,
 insight("Gam dışı talebin büyük bölümü VitrA'ya uzak ya da orta uyumdaki temalarda toplanmaktadır: su arıtma cihazı (%s), şofben ve termosifon (%s), banyo tekstili (%s) ve mutfak tezgahı (%s). Bu temalar hacimli olsa da marka ve kanal açısından VitrA'nın doğal alanı değildir; ancak Koçtaş'ın \"Banyo Tadilatı\" sayfasında olduğu gibi, tadilat paketinde iş ortağı ürünü olarak yer alabilirler. VitrA'ya yakın temalarda talep daha küçük ama ürün üretimi ve marka güveni açısından daha uygundur: evye (%s), yedek parça (%s), havlupan (%s), ledli ayna ve aydınlatma (%s, üç yılda %s), yaşlı ve engelli ürünleri (%s, YoY %s) ve arıtmalı batarya (%s, üç yılda %s, son yılda %s). Aylık 50K üzeri talebi olan gam dışı temalar içinde en hızlı büyüyen yapıştırıcı, derz ve su yalıtımıdır (YoY %s)." % (k(t("aritma")["v12"]), k(t("sicaksu")["v12"]), k(t("tekstil")["v12"]), k(t("mutfak_tezgah")["v12"]), k(t("evye")["v12"]), k(t("yedek")["v12"]), k(t("havlupan")["v12"]), k(t("aydinlatma")["v12"]), yz(t("aydinlatma")["uc_yil"]), k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("aritma_bat")["v12"]), yz(t("aritma_bat")["uc_yil"]), yz(t("aritma_bat")["yoy"]), yz(t("yapi_kimya")["yoy"])),
         "Most demand outside VitrA's range sits in themes with distant or medium fit to VitrA: water purifiers (%s), water heaters (%s), bath textiles (%s) and kitchen countertops (%s). These themes are large but not VitrA's natural territory in brand and channel terms; however, as on Koçtaş's \"Bathroom Renovation\" page, they could appear as partner products in a renovation package. Themes close to VitrA have smaller demand but are better suited in terms of manufacturing and brand trust: sinks (%s), spare parts (%s), towel radiators (%s), LED mirrors and lighting (%s, %s over three years), accessible products (%s, YoY %s) and purifier taps (%s, %s over three years, %s in the last year). Among themes outside VitrA's range with monthly demand above 50K, the fastest-growing is adhesives, grout and waterproofing (YoY %s)." % (k(t("aritma")["v12"]), k(t("sicaksu")["v12"]), k(t("tekstil")["v12"]), k(t("mutfak_tezgah")["v12"]), k(t("evye")["v12"]), k(t("yedek")["v12"]), k(t("havlupan")["v12"]), k(t("aydinlatma")["v12"]), yz(t("aydinlatma")["uc_yil"]), k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("aritma_bat")["v12"]), yz(t("aritma_bat")["uc_yil"]), yz(t("aritma_bat")["yoy"]), yz(t("yapi_kimya")["yoy"])), "D12", "D14", "D16"),
 x("Öncelikli dört fırsat", "Four priority opportunities"),
 step(1, "Yedek parça kategorisi ve parça bulucu", "Spare-parts category and part finder",
      "Rezervuar iç takımı (%s) ve kartuş, başlık, perlatör gibi yedek parça (%s) aramaları toplam aylık %s seviyesindedir; tamir ve bakım ifadeleri incelenen autocomplete önerilerinin %s oluşturmaktadır. VitrA bu parçaları üretmekte ve sitede iç takım ürünleri satılmaktadır. Tüketiciye açık bir yedek parça kategorisi ve ürün koduna göre parça bulucu (Hansgrohe, Grohe örneği) henüz bulunmamaktadır." % (k(t("ic_takim")["v12"]), k(t("yedek")["v12"]), k(t("yedek")["v12"] + t("ic_takim")["v12"]), yzd_ek(_TAMP, 1, "ini")),
      "Searches for cistern inner mechanisms (%s) and spare parts such as cartridges, heads and aerators (%s) total %s per month; repair and maintenance phrases make up %s of the autocomplete suggestions reviewed. VitrA makes these parts and inner mechanisms are sold on the site. A consumer-facing spare-parts category and a part finder by product code (as at Hansgrohe and Grohe) do not yet exist." % (k(t("ic_takim")["v12"]), k(t("yedek")["v12"]), k(t("yedek")["v12"] + t("ic_takim")["v12"]), ("%.1f" % _TAMP) + "%")),
 step(2, "Granit ve çelik evye + batarya seti", "Granite and steel sink + tap set",
      "Evye talebi aylık %s seviyesindedir; VitrA'nın evye hattı seramikle sınırlıdır. Trendyol'da granit evye medyanı %s TL'dir ve değerlendirme sayıları düşüktür; kategori pazaryerinde henüz olgunlaşmamıştır. Artema mutfak bataryasıyla set satışı değerlendirilebilir." % (k(t("evye")["v12"]), bin(TY["granit evye"]["fiyat_medyan"])),
      "Sink demand is %s per month; VitrA's sink range is limited to ceramic. On Trendyol the granite sink median is %s TL with low review counts; the category has not matured. A set sale with the Artema kitchen tap can be considered." % (k(t("evye")["v12"]), bin(TY["granit evye"]["fiyat_medyan"]))),
 step(3, "Arıtmalı batarya ve filtre aboneliği", "Purifier tap and filter subscription",
      "Arıtmalı batarya aramaları üç yılda %s artmış, son yılda %s değişmiştir; su arıtma cihazı talebi aylık %s seviyesindedir. Trendyol'da arıtmalı batarya aramasının ilk 40 sonucunda armatür markası bulunmamaktadır. Franke'nin kapsül filtre modeli tekrarlı gelir için örnek alınabilir." % (yz(t("aritma_bat")["uc_yil"]), yz(t("aritma_bat")["yoy"]), k(t("aritma")["v12"])),
      "Purifier tap searches grew %s over three years and changed %s in the last year; water purifier demand is %s per month. No tap brand appears in the top 40 Trendyol results for purifier taps. Franke's capsule filter model can serve as an example for recurring revenue." % (yz(t("aritma_bat")["uc_yil"]), yz(t("aritma_bat")["yoy"]), k(t("aritma")["v12"]))),
 step(4, "Erişilebilir banyo ve çocuk banyosu setleri", "Accessible and children's bathroom sets",
      "Yaşlı ve engelli ürünleri aylık %s (YoY %s), çocuk ve bebek ürünleri %s (YoY %s) seviyesindedir. VitrA'da Conforma serisi, tutunma barları ve Sento çocuk ürünleri mevcuttur ancak ayrı bir sayfada toplanmamaktadır; çocuk klozeti aramasında Trendyol 2.238 ve Hepsiburada 1.659 sonuç vermekte, engelli klozeti Trendyol'da 43 ürünlük ayrı kategori olarak listelenmektedir." % (k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("cocuk")["v12"]), yz(t("cocuk")["yoy"])),
      "Accessible products total %s per month (YoY %s), children's and baby products %s (YoY %s). VitrA has the Conforma series, grab bars and Sento kids products, but they are not gathered on a dedicated page; the children's WC search returns 2,238 results on Trendyol and 1,659 on Hepsiburada, and accessible WCs are listed as a separate 43-product category on Trendyol." % (k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("cocuk")["v12"]), yz(t("cocuk")["yoy"]))),
 note("NOT", "NOTE", ul_b([("Taharet aparatı ve bide kapağı (universal akıllı kapak):", "Bidet attachments and seats (universal smart seat):", "aylık %s aramayla küçük kalmakta, üç yılda %s büyümektedir; kısa vadede öncelik değil, V-Care teknolojisinin uzun vadeli türevi olarak izlenebilir." % (bin(t("taharet_aparat")["v12"]), yz(t("taharet_aparat")["uc_yil"])), "stays small at %s monthly searches but grows %s over three years; not a short-term priority, can be tracked as a long-term derivative of V-Care technology." % (bin(t("taharet_aparat")["v12"]), yz(t("taharet_aparat")["uc_yil"]))),
                             ("Havlupan:", "Towel radiators:", "Haziran çalışmasında \"ürün var\" gerekçesiyle kapsam dışı bırakılmıştı; güncel katalogda 2 ürün bulunduğundan derinlik fırsatı olarak değerlendirilmektedir.", "left out of the June study on the grounds that \"the product exists\"; with 2 products in the current catalogue it is treated here as a depth opportunity.")])),
 kaynak("Google Ads Keyword Planner genişletilmiş evren (48 ay) · vitra.com.tr ürün sitemap'i · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline kategori sitemap'leri · Trendyol arama sonuçları · Inbound VitrA sezonsallık ve rakip ürün analizi (Haziran 2026) · %s" % veri.TARIH,
        "Google Ads Keyword Planner expanded universe (48 months) · vitra.com.tr product sitemap · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline category sitemaps · Trendyol search results · Inbound VitrA seasonality and competitor product analysis (June 2026) · %s" % veri.TARIH, "D12", "D13", "D14", "D15", "D16"),
)
