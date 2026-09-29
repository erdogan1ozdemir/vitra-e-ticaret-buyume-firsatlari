# -*- coding: utf-8 -*-
"""Bolum: Ozet - KPI, kritik tespit, one cikan bulgular."""
from ortak import *
K1 = A["k1"]; TOP = A["toplam"]; NI = A["niyet"]; GT = A["gsc_tur"]; GS = A["gsc_sorgu_niyet"]; AT = A["auto_tema"]
toplam_yoy = (TOP["a26"] / TOP["a25"] - 1) * 100; kloz = A["k2"]["Vitrifiyeler|Klozetler"]["yoy"]; bm = K1["Banyo Mobilyaları"]["yoy"]
ttot = sum(v[0] for v in GT.values()); ktot = sum(v[0] for v in A["gsc_kat"].values())
bm_tik = 100 * sum(v[0] for kk, v in A["gsc_kat"].items() if kk.startswith("Banyo Mobilyaları")) / ktot; bm_talep = 100 * K1["Banyo Mobilyaları"]["a26"] / TOP["a26"]
tam_pay = 100 * AT["Tamir ve bakım"] / sum(AT.values())
vit = next(b for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "vitra.com.tr"); koc = next(b for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "koctas.com.tr")
son12 = sum(A["gsc_ay_toplam"][m][0] for m in A["gsc_aylar"][-13:-1])
TM = YK["tema"]; SEG = SB["seg"]; OB = SB["oz_bm"]; OSS = SB["oz_ssg"]
def oz(o, ad): return next(z for z in o["ozellik"] if z["ad"] == ad)
yed = TM["yedek"]["v12"] + TM["ic_takim"]["v12"]
KPI = "".join([
 kpi_kart(yz(toplam_yoy), "Kategori arama talebi · Oca-Ağu 2026 / 2025, 2.420 kelime", "Category search demand · Jan-Aug 2026 / 2025, 2,420 keywords", "dn"),
 kpi_kart(yz(SEG["SSG"]["uc"]), "SSG talebi · 3 yıllık değişim; BM %s" % yz(SEG["BM"]["uc"]), "SSG demand · 3-year change; BM %s" % yz(SEG["BM"]["uc"]), "up"),
 kpi_kart(k(yed), "Aylık iç takım ve yedek parça araması · sitede yedek parça kategorisi yok", "Monthly inner-mechanism and spare-part searches · no spare-parts category on the site", "hi"),
 kpi_kart(yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]), "BM aramalarında perakendeci adı geçen pay · VitrA %s" % yzd(oz(OB, "VitrA")["pay"]), "Share of BM searches naming a retailer · VitrA %s" % (yzd(oz(OB, "VitrA")["pay"]).replace("%", "") + "%"), "hi"),
])
KRITIK = marks([
 ("at", "Talep daralması makro kaynaklıdır ve segmentler ayrışmaktadır: SSG üç yılda %s ile yatay, BM %s; ertelenen yenileme talebi 2026 Q4 - 2027 Q1'de geri gelebilir" % (yz(SEG["SSG"]["uc"]), yz(SEG["BM"]["uc"])), "The demand contraction is macro-driven and the segments diverge: SSG flat at %s over three years, BM %s; postponed renovation demand may return in 2026 Q4 - 2027 Q1" % (yz(SEG["SSG"]["uc"]), yz(SEG["BM"]["uc"]))),
 ("at", "Kullanıcı VitrA'dan yedek parça bekliyor: iç takım ve parça aramaları aylık %s, eski yedek parça sayfası bugün tek ürünlü kategoriye yönleniyor" % k(yed), "Users expect spare parts from VitrA: inner-mechanism and part searches total %s per month, and the old spare-parts page now redirects to a one-product category" % k(yed)),
 ("at", "Ürün + hizmet modelinin parçaları mevcut (11 montaj kalemi, keşif, Banyo Asistanı, ücretsiz montajlı mobilya), ancak tek bir teklif altında birleşmiyor; duşakabin gibi ölçüye bağlı ürünlerde montaj ve keşif seçeneği görünmüyor", "The pieces of a product + service model exist (11 installation items, survey, Bathroom Assistant, free-installation furniture) but are not combined into a single offer; installation and survey options are not visible on dimension-dependent products such as shower enclosures"),
 ("up", "Gam dışında VitrA'ya yakın fırsatlar: granit ve çelik evye (%s), arıtmalı batarya, erişilebilir ve çocuk banyosu, havlupan ve ledli ayna derinliği" % k(TM["evye"]["v12"]), "Out-of-range opportunities close to VitrA: granite and steel sinks (%s), purifier taps, accessible and children's bathrooms, depth in towel radiators and LED mirrors" % k(TM["evye"]["v12"])),
 ("up", "BM'de pazaryeri fiyatla değil set, montaj ve garanti bütünlüğüyle kazanılabilir: Trendyol banyo dolabı medyanı %s TL, en çok değerlendirme alanlar düz paket mobilya markaları" % bin(TY["banyo dolabı"]["fiyat_medyan"]), "On the marketplace BM can be won through set, installation and warranty integrity rather than price: Trendyol bathroom cabinet median %s TL, the most-reviewed products are flat-pack furniture brands" % bin(TY["banyo dolabı"]["fiyat_medyan"])),
])
FN = '<div class="fnotes">%s</div>' % "".join([
 fnote(1, "SSG dayanıklı, BM daralıyor", "SSG resilient, BM contracting",
       [("SSG üç yılda <b>%s</b>; klozet <b>%s</b>, akıllı klozet seti <b>%s</b>, bide <b>%s</b>" % (yz(SEG["SSG"]["uc"]), yz(SB["k3"]["SSG|Klozetler|Klozetler"]["uc"]), yz(SB["k3"]["SSG|Klozetler|Akıllı Klozet Seti"]["uc"]), yz(SB["k3"]["SSG|Bideler|Bideler"]["uc"])), "SSG <b>%s</b> over three years; WCs <b>%s</b>, smart WC sets <b>%s</b>, bidets <b>%s</b>" % (yz(SEG["SSG"]["uc"]), yz(SB["k3"]["SSG|Klozetler|Klozetler"]["uc"]), yz(SB["k3"]["SSG|Klozetler|Akıllı Klozet Seti"]["uc"]), yz(SB["k3"]["SSG|Bideler|Bideler"]["uc"]))),
        ("BM üç yılda <b>%s</b>; yalnız tezgah (<b>%s</b>) ve çamaşır makinesi dolabı (<b>%s</b>) talebini koruyor" % (yz(SEG["BM"]["uc"]), yz(SB["k3"]["BM|Banyo Tezgahları|Banyo Tezgahları"]["uc"]), yz(SB["k3"]["BM|Banyo Dolapları|Çamaşır Makinesi Dolapları"]["uc"])), "BM <b>%s</b> over three years; only countertops (<b>%s</b>) and washing machine cabinets (<b>%s</b>) hold demand" % (yz(SEG["BM"]["uc"]), yz(SB["k3"]["BM|Banyo Tezgahları|Banyo Tezgahları"]["uc"]), yz(SB["k3"]["BM|Banyo Dolapları|Çamaşır Makinesi Dolapları"]["uc"]))),
        ("Oca-Ağu 2026'da toplam talep <b>%s</b>; tasarım ve model aramaları <b>%s</b>" % (yz(toplam_yoy), yz(NI["Tasarım ve fikir"]["yoy"])), "Total demand <b>%s</b> in Jan-Aug 2026; design and model searches <b>%s</b>" % (yz(toplam_yoy), yz(NI["Tasarım ve fikir"]["yoy"])))]),
 fnote(2, "Makro ortam: harcama nominal, niyet yükselişte", "Macro environment: nominal spending, rising intent",
       [("Mobilya ve dekorasyon kart harcaması <b>%s</b> nominal; reel kartlı ödeme endeksi <b>%s</b>" % (yz(A["kart"]["mobilya_dekorasyon"]["yoy"]), yz((sum(A["koe"]["2026-%d" % m]["genel_reel"] for m in range(1, 8)) / sum(A["koe"]["2025-%d" % m]["genel_reel"] for m in range(1, 8)) - 1) * 100)), "Furniture and decoration card spending <b>%s</b> nominal; real card payment index <b>%s</b>" % (yz(A["kart"]["mobilya_dekorasyon"]["yoy"]), yz((sum(A["koe"]["2026-%d" % m]["genel_reel"] for m in range(1, 8)) / sum(A["koe"]["2025-%d" % m]["genel_reel"] for m in range(1, 8)) - 1) * 100))),
        ("Tüketici güveni Eylül 2026'da <b>%s</b>; konut tamiratına harcama ihtimali <b>%s</b>" % (("%.1f" % A["tuketici"]["2026-9"]["guven_endeksi"]).replace(".", ","), ("%.1f" % A["tuketici"]["2026-9"]["konut_tamirat_harcama_ihtimali"]).replace(".", ",")), "Consumer confidence <b>%s</b> in September 2026; probability of spending on home repairs <b>%s</b>" % ("%.1f" % A["tuketici"]["2026-9"]["guven_endeksi"], "%.1f" % A["tuketici"]["2026-9"]["konut_tamirat_harcama_ihtimali"])),
        ("Konut satışları Oca-Ağu 2026 <b>%s</b>" % yz((sum(A["konut"]["2026-%d" % m]["toplam"] for m in range(1, 9)) / sum(A["konut"]["2025-%d" % m]["toplam"] for m in range(1, 9)) - 1) * 100), "House sales Jan-Aug 2026 <b>%s</b>" % yz((sum(A["konut"]["2026-%d" % m]["toplam"] for m in range(1, 9)) / sum(A["konut"]["2025-%d" % m]["toplam"] for m in range(1, 9)) - 1) * 100))]),
 fnote(3, "Kullanıcı ne arıyor?", "What does the user search for?",
       [("SSG aramalarının <b>%s</b>'i fiyat, <b>%s</b>'i tamir ve parça; rakip marka adı (<b>%s</b>) VitrA adından (<b>%s</b>) fazla" % (yzd(oz(OSS, "Fiyat")["pay"]), yzd(oz(OSS, "Tamir / parça")["pay"]), yzd(oz(OSS, "Rakip marka")["pay"]), yzd(oz(OSS, "VitrA")["pay"])), "<b>%s</b> of SSG searches carry price, <b>%s</b> repair and parts; competitor brand names (<b>%s</b>) exceed VitrA (<b>%s</b>)" % tuple(yzd(v).replace("%", "") + "%" for v in (oz(OSS, "Fiyat")["pay"], oz(OSS, "Tamir / parça")["pay"], oz(OSS, "Rakip marka")["pay"], oz(OSS, "VitrA")["pay"]))),
        ("BM'de PVC ve suya dayanıklı gövde <b>%s</b>, küçük banyo <b>%s</b>" % (yz(oz(OB, "PVC / suya dayanıklı")["yoy"]), yz(oz(OB, "Küçük / dar banyo")["yoy"])), "In BM, PVC and water-resistant bodies <b>%s</b>, small bathroom <b>%s</b>" % (yz(oz(OB, "PVC / suya dayanıklı")["yoy"]), yz(oz(OB, "Küçük / dar banyo")["yoy"]))),
        ("Autocomplete önerilerinin <b>%s</b>'i tamir ve yedek parça; YouTube tamir aramalarında VitrA videosu yok" % yzd(tam_pay), "<b>%s</b> of autocomplete suggestions are repair and spare parts; no VitrA video in YouTube repair searches" % (yzd(tam_pay).replace("%", "") + "%"))]),
 fnote(4, "Katalog boşlukları ve yakın fırsatlar", "Catalogue gaps and nearby opportunities",
       [("Hela taşı <b>%s</b> arama / 1 ürün; havlupan <b>%s</b> / 2 ürün" % (k(TM["hela"]["v12"]), k(TM["havlupan"]["v12"])), "Squat toilet <b>%s</b> searches / 1 product; towel radiators <b>%s</b> / 2 products" % (k(TM["hela"]["v12"]), k(TM["havlupan"]["v12"]))),
        ("Evye <b>%s</b> (VitrA yalnız seramik), arıtmalı batarya üç yılda <b>%s</b>, erişilebilir ürünler YoY <b>%s</b>" % (k(TM["evye"]["v12"]), yz(TM["aritma_bat"]["uc_yil"]), yz(TM["engelli"]["yoy"])), "Sinks <b>%s</b> (VitrA ceramic only), purifier taps <b>%s</b> over three years, accessible products YoY <b>%s</b>" % (k(TM["evye"]["v12"]), yz(TM["aritma_bat"]["uc_yil"]), yz(TM["engelli"]["yoy"]))),
        ("Gam dışı büyük hacimler (arıtma, şofben, tekstil) yalnız tadilat paketinde iş ortağı ürünü olarak uygun", "Large out-of-range volumes (purifiers, water heaters, textiles) fit only as partner products in a renovation package")]),
 fnote(5, "Ürün + hizmet: parçalar var, paket yok", "Product + service: the pieces exist, the package does not",
       [("11 montaj kalemi (klozet 2.750 TL, BM seti 4.000 TL), keşif 1.400 TL, 92 üründe ücretsiz montaj", "11 installation items (WC 2,750 TL, BM set 4,000 TL), survey 1,400 TL, free installation on 92 products"),
        ("Banyo Asistanı: 4 adım, telefon / mağaza / görüntülü görüşme, 5 VitrA mağazası", "Bathroom Assistant: 4 steps, phone / store / video call, 5 VitrA stores"),
        ("Koçtaş, BAUHAUS ve Kohler banyoyu \"proje\" olarak satıyor; VitrA'da tadilat girişi ve planlayıcı yok", "Koçtaş, BAUHAUS and Kohler sell the bathroom as a \"project\"; VitrA has no renovation entry page or planner")]),
 fnote(6, "Rekabet: pazaryeri ve yapı market ölçeği", "Competition: marketplace and DIY scale",
       [("Koçtaş VitrA kelimelerinin <b>%s</b>'inde birlikte sıralanıyor; organik trafiği VitrA'nın <b>%s</b> katı" % (yzd(100 * veri.AHREFS["ahrefs_organik_rakipler_tr"][0][1] / vit[2]), ("%.1f" % (koc[4] / vit[4])).replace(".", ",")), "Koçtaş ranks alongside VitrA for <b>%s</b> of its keywords; organic traffic <b>%s</b> times VitrA's" % (yzd(100 * veri.AHREFS["ahrefs_organik_rakipler_tr"][0][1] / vit[2]).replace("%", "") + "%", "%.1f" % (koc[4] / vit[4]))),
        ("Trendyol'da BM ve aynada VitrA pazar medyanının birkaç katı fiyatta tek tük; iç takımda ilk sırada", "On Trendyol VitrA appears sparsely in BM and mirrors at several times the market median; first place in inner mechanisms"),
        ("Marka siteleri içinde VitrA organik lider: <b>%s</b> tahmini ziyaret" % k(vit[4]), "VitrA is the organic leader among brand sites: <b>%s</b> estimated visits" % k(vit[4]))]),
])
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s</div>
%s
<h3>%s</h3>
%s
""" % (
 x("VitrA e-ticaret büyüme fırsatları çalışmasıdır. Pazar talebi (SSG ve BM derin inceleme dahil), kullanıcı ihtiyaç dili, organik kanal, YouTube, katalog ve talep eşleşmesi, yeni kategori ve segmentler, set ve ürün + hizmet modelleri, rekabet, benchmark ve makro ortam Inbound erişimindeki kaynaklarla incelenmiştir. VitrA'dan beklenen pazaryeri, GA4 ve müşteri verisiyle rapor genişletilecektir.",
   "This is the VitrA e-commerce growth opportunities study. Market demand (including an in-depth look at SSG and BM), user need language, organic channel, YouTube, catalogue-demand fit, new categories and segments, set and product + service models, competition, benchmarks and the macro environment have been examined with the sources available to Inbound. The report will be extended with the marketplace, GA4 and customer data expected from VitrA."),
 KPI,
 box("KRİTİK TESPİT", "KEY FINDINGS", KRITIK),
 x("Öne çıkan bulgular", "Highlights"), FN,
)
