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
 "suzgec":         (("Tekzen, Banyoline, Kale", "Tekzen, Banyoline, Kale"), "Yakın", ("Duş teknesi ve kanalı sepetine tamamlayıcı", "Complement in the shower tray and channel basket")),
 "taharet_aparat": (("Kale Smartx (yalnız kendi klozetine), TOTO, Coway, medikal satıcılar", "Kale Smartx (own WC only), TOTO, Coway, medical sellers"), "Yakın", ("V-Care teknolojisinden universal kapak (uzun vade)", "Universal seat derived from V-Care technology (long term)")),
 "ticari":         (("Banyomarka, profesyonel ıslak hacim markaları", "Banyomarka, professional washroom brands"), "Orta", ("Proje kanalında temassız batarya ve pisuvarla paket", "Package with touchless taps and urinals in the project channel")),
 "yapi_kimya":     (("Kale (Kalekim), Bauhaus, Tekzen, Banyoline, Koçtaş", "Kale (Kalekim), Bauhaus, Tekzen, Banyoline, Koçtaş"), "Orta", ("Karo sepetine yapıştırıcı ve derz, iş ortağı ürünü", "Adhesive and grout in the tile basket, partner product")),
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
    rows.append([x(t["tr"], tema.META[tk]["en"]), cell(t["v12"]), n(yz(t["yoy"])), n(yz(t["uc_yil"])), '<span class="badge %s">%s</span>' % ({"Var": "b-var", "Kısmi": "b-kis", "Yok": "b-yok"}[t["durum"]], x(t["durum"], DUR_EN[t["durum"]])),
                 x(*rk), '<span class="badge %s">%s</span>' % (UY_CL[uy], x(uy, UY_EN[uy])), x(*md), '<div class="kwlist">%s</div>' % "".join(kw(w[0]) for w in t["top"][:3])])
tbl = tablo([th("Tema", "Theme", "VitrA kataloğunda bulunmayan ya da sınırlı derinlikte bulunan ürün teması.", "Product theme absent from, or thin in, the VitrA catalogue."),
             th("Aylık talep", "Monthly demand", "Eyl 2025 - Ağu 2026 aylık ortalama arama hacmi; yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 average monthly search volume; spelling variants counted once.", True),
             th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True),
             th("3 yıllık değişim", "3-year change", "Eyl 22 - Ağu 23 ile Eyl 25 - Ağu 26 ortalamaları arasındaki değişim.", "Change between the Sep 22 - Aug 23 and Sep 25 - Aug 26 averages.", True),
             th("VitrA", "VitrA", "VitrA kataloğundaki karşılık.", "Coverage in the VitrA catalogue."),
             th("Rakipte kim satıyor?", "Who sells it?", "Rakip sitelerin kategori ağaçları, Trendyol sonuçları ve Inbound'un Haziran 2026 rakip ürün analizi.", "Competitor category trees, Trendyol results and Inbound's June 2026 competitor product analysis."),
             th("VitrA'ya uyum", "Fit with VitrA", "Yakın: VitrA veya Artema üretim yetkinliğine bitişik · Orta: tamamlayıcı, iş ortağıyla sunulabilir · Uzak: marka ve kanal açısından uzak.", "Close: adjacent to VitrA or Artema manufacturing capability · Medium: complementary, can be offered with a partner · Distant: far in brand and channel terms."),
             th("Model önerisi", "Proposed model", "Temanın vitra.com.tr'de nasıl sunulabileceği; 3P = üçüncü taraf satıcı.", "How the theme could be offered on vitra.com.tr; 3P = third-party seller."),
             th("Örnek aramalar", "Example searches", "Temanın en yüksek hacimli aramaları.", "Highest-volume searches in the theme.")], rows, "uzun")
def t(k_): return TM[k_]
HTML = """
<p class="lede">%s</p>
%s
%s
<h3>%s</h3>
<div class="steps">%s%s%s%s</div>
%s
%s
""" % (
 x("Genişletilmiş kelime evreni (52.973 kelime) VitrA'nın bugünkü kategori ağacının dışına taşan temaları da kapsayacak şekilde sınıflandırılmıştır. VitrA kataloğunda bulunmayan ya da sınırlı derinlikte bulunan temalar için talep, rakipte kimin sattığı, VitrA'ya uyum ve olası satış modeli birlikte değerlendirilmiştir; Haziran 2026 sezonsallık çalışmasındaki dört ürün kümesi (<b>yedek parça, evye, arıtmalı batarya, universal akıllı kapak</b>) güncel veriyle yeniden ölçülmüştür.",
   "The expanded keyword universe (52,973 keywords) has been classified to include themes beyond VitrA's current category tree. For themes absent from, or thin in, the VitrA catalogue, demand, who sells them, fit with VitrA and a possible sales model are assessed together; the four product clusters from the June 2026 seasonality study (<b>spare parts, sinks, purifier taps, universal smart seat</b>) have been re-measured with current data."),
 tbl,
 insight("Gam dışı talebin büyük bölümü VitrA'ya uzak ya da orta uyumdaki temalarda toplanmaktadır: su arıtma cihazı (%s), şofben ve termosifon (%s), banyo tekstili (%s) ve mutfak tezgahı (%s). Bu temalar hacimli olsa da marka ve kanal açısından VitrA'nın doğal alanı değildir; ancak Koçtaş'ın \"Banyo Tadilatı\" sayfası bu ürünlerin tamamını tek sayfada topladığı için, tadilat paketinde iş ortağı ürünü olarak yer alabilirler. VitrA'ya yakın temalarda talep daha küçük ama ürün üretimi ve marka güveni açısından daha uygundur: evye (%s), yedek parça (%s), havlupan (%s), ledli ayna ve aydınlatma (%s, üç yılda %s), yaşlı ve engelli ürünleri (%s, YoY %s) ve arıtmalı batarya (%s, üç yılda %s). Yapıştırıcı, derz ve su yalıtımı %s ile gam dışında en hızlı büyüyen temadır." % (k(t("aritma")["v12"]), k(t("sicaksu")["v12"]), k(t("tekstil")["v12"]), k(t("mutfak_tezgah")["v12"]), k(t("evye")["v12"]), k(t("yedek")["v12"]), k(t("havlupan")["v12"]), k(t("aydinlatma")["v12"]), yz(t("aydinlatma")["uc_yil"]), k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("aritma_bat")["v12"]), yz(t("aritma_bat")["uc_yil"]), yz(t("yapi_kimya")["yoy"])),
         "Most out-of-range demand sits in themes with distant or medium fit to VitrA: water purifiers (%s), water heaters (%s), bath textiles (%s) and kitchen countertops (%s). These themes are large but not VitrA's natural territory in brand and channel terms; however, since Koçtaş's \"Bathroom Renovation\" page gathers all of them on a single page, they could appear as partner products in a renovation package. Themes close to VitrA have smaller demand but are better suited in terms of manufacturing and brand trust: sinks (%s), spare parts (%s), towel radiators (%s), LED mirrors and lighting (%s, %s over three years), accessible products (%s, YoY %s) and purifier taps (%s, %s over three years). Adhesives, grout and waterproofing is the fastest-growing out-of-range theme at %s." % (k(t("aritma")["v12"]), k(t("sicaksu")["v12"]), k(t("tekstil")["v12"]), k(t("mutfak_tezgah")["v12"]), k(t("evye")["v12"]), k(t("yedek")["v12"]), k(t("havlupan")["v12"]), k(t("aydinlatma")["v12"]), yz(t("aydinlatma")["uc_yil"]), k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("aritma_bat")["v12"]), yz(t("aritma_bat")["uc_yil"]), yz(t("yapi_kimya")["yoy"])), "D12", "D14", "D16"),
 x("Öncelikli dört fırsat", "Four priority opportunities"),
 step(1, "Yedek parça kategorisi ve parça bulucu", "Spare-parts category and part finder",
      "İç takım, şamandıra, menteşe, kartuş ve conta aramaları aylık %s; autocomplete önerilerinin yaklaşık beşte biri bu temada. VitrA parçaları üretiyor; Trendyol'da iç takımda ilk sırada. Eksik olan tüketiciye açık kategori ve ürün koduna göre parça bulucu (Hansgrohe, Grohe örneği)." % k(t("yedek")["v12"] + t("ic_takim")["v12"]),
      "Searches for inner mechanisms, float valves, hinges, cartridges and gaskets total %s per month; about a fifth of autocomplete suggestions fall in this theme. VitrA makes the parts and ranks first on Trendyol for inner mechanisms. What is missing is a consumer-facing category and a part finder by product code (as at Hansgrohe and Grohe)." % k(t("yedek")["v12"] + t("ic_takim")["v12"])),
 step(2, "Granit ve çelik evye + batarya seti", "Granite and steel sink + tap set",
      "Evye talebi aylık %s; VitrA'nın evye hattı seramikle sınırlı. Trendyol'da granit evye medyanı %s TL ve değerlendirmeler düşük, kategori henüz olgunlaşmamış. Artema mutfak bataryasıyla set satışı mümkün." % (k(t("evye")["v12"]), bin(TY["granit evye"]["fiyat_medyan"])),
      "Sink demand is %s per month; VitrA's sink range is limited to ceramic. On Trendyol the granite sink median is %s TL with low review counts; the category has not matured. A set sale with the Artema kitchen tap is possible." % (k(t("evye")["v12"]), bin(TY["granit evye"]["fiyat_medyan"]))),
 step(3, "Arıtmalı batarya ve filtre aboneliği", "Purifier tap and filter subscription",
      "Arıtmalı batarya aramaları üç yılda %s; su arıtma cihazı talebi aylık %s. Trendyol ilk 40 sonucunda armatür markası yok. Franke'nin kapsül filtre modeli tekrarlı gelir için örnek alınabilir." % (yz(t("aritma_bat")["uc_yil"]), k(t("aritma")["v12"])),
      "Purifier tap searches grew %s over three years; water purifier demand is %s per month. No tap brand appears in Trendyol's top 40. Franke's capsule filter model can serve as an example for recurring revenue." % (yz(t("aritma_bat")["uc_yil"]), k(t("aritma")["v12"]))),
 step(4, "Erişilebilir banyo ve çocuk banyosu setleri", "Accessible and children's bathroom sets",
      "Yaşlı ve engelli ürünleri aylık %s (YoY %s), çocuk ve bebek ürünleri %s. VitrA'da Conforma serisi, tutunma barları ve Sento çocuk ürünleri mevcut ancak ayrı bir sayfada toplanmıyor; çocuk klozeti aramasında Trendyol 2.238 ve Hepsiburada 1.659 sonuç, engelli klozeti Trendyol'da 43 ürünlük ayrı kategori olarak listeleniyor." % (k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("cocuk")["v12"])),
      "Accessible products total %s per month (YoY %s), children's and baby products %s. VitrA has the Conforma series, grab bars and Sento kids products, but they are not gathered on a dedicated page; the children's WC search returns 2,238 results on Trendyol and 1,659 on Hepsiburada, and accessible WCs are listed as a separate 43-product category on Trendyol." % (k(t("engelli")["v12"]), yz(t("engelli")["yoy"]), k(t("cocuk")["v12"]))),
 note("NOT", "NOTE", ul_b([("Universal akıllı klozet kapağı:", "Universal smart WC seat:", "aylık %s aramayla küçük kalmakta, üç yılda %s büyümektedir; kısa vadede öncelik değil, V-Care teknolojisinin uzun vadeli türevi olarak izlenebilir." % (bin(t("taharet_aparat")["v12"]), yz(t("taharet_aparat")["uc_yil"])), "stays small at %s monthly searches but grows %s over three years; not a short-term priority, can be tracked as a long-term derivative of V-Care technology." % (bin(t("taharet_aparat")["v12"]), yz(t("taharet_aparat")["uc_yil"]))),
                             ("Havlupan:", "Towel radiators:", "Haziran çalışmasında \"ürün var\" gerekçesiyle kapsam dışı bırakılmıştı; güncel katalogda 2 ürün bulunduğundan derinlik fırsatı olarak değerlendirilmektedir.", "left out of the June study on the grounds that \"the product exists\"; with 2 products in the current catalogue it is treated here as a depth opportunity.")])),
 kaynak("Google Ads Keyword Planner genişletilmiş evren (48 ay) · vitra.com.tr ürün sitemap'i · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline kategori sitemap'leri · Trendyol arama sonuçları · Inbound VitrA sezonsallık ve rakip ürün analizi (Haziran 2026) · %s" % veri.TARIH,
        "Google Ads Keyword Planner expanded universe (48 months) · vitra.com.tr product sitemap · Bauhaus, IKEA, Tekzen, Evidea, Banyomarka, Kale, Banyoline category sitemaps · Trendyol search results · Inbound VitrA seasonality and competitor product analysis (June 2026) · %s" % veri.TARIH, "D12", "D13", "D14", "D15", "D16"),
)
