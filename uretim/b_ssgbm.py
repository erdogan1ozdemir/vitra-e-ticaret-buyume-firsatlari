# -*- coding: utf-8 -*-
"""Bolum: SSG ve BM derin talep (48 ay, urun tipi ve ozellik)."""
from ortak import *
from rapor_parca1 import T, cizgi
from b_talep import kat, kat2
A48 = SB["aylar"]; SEG = SB["seg"]; K3 = SB["k3"]; OS = SB["oz_ssg"]; OB = SB["oz_bm"]
ssg, bm = SEG["SSG"], SEG["BM"]
GRAFIK = cizgi([(x("SSG (vitrifiye ve rezervuar)", "SSG (sanitaryware and cisterns)"), "#10332F", [round(v) for v in ssg["seri"]]),
                (x("BM (banyo mobilyası)", "BM (bathroom furniture)"), "#E85F36", [round(v) for v in bm["seri"]])],
               y_etiket=x("Aylık arama hacmi · Eyl 2022 - Ağu 2026", "Monthly search volume · Sep 2022 - Aug 2026"), aylar=A48)
def k3rows(seg, lim):
    out = []
    for key, v in sorted([(k, v) for k, v in K3.items() if k.startswith(seg + "|")], key=lambda i: -i[1]["p3"])[:lim]:
        _, k2, k3 = key.split("|")
        out.append([kat2(k2), kat2(k3) if k3 != k2 else x("Genel", "General"), cell(v["p0"]), cell(v["p3"]), n(yz(v["uc"])), n(yz(v["yoy"]))])
    return out
BAS = [th("Alt kategori", "Sub-category", "VitrA kategori ağacındaki alt kategori.", "Sub-category in the VitrA category tree."),
       th("Ürün tipi", "Product type", "Alt kategorinin altındaki ürün tipi; \"Genel\" alt kategori adıyla yapılan aramalardır.", "Product type under the sub-category; \"General\" is searches made with the sub-category name."),
       th("Eyl 22 - Ağu 23", "Sep 22 - Aug 23", "Eylül 2022 - Ağustos 2023 aylık ortalama arama hacmi.", "Average monthly search volume, September 2022 - August 2023.", True),
       th("Eyl 25 - Ağu 26", "Sep 25 - Aug 26", "Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Average monthly search volume, September 2025 - August 2026.", True),
       th("3 yıllık değişim", "3-year change", "İki 12 aylık pencerenin ortalamaları arasındaki yüzde değişim.", "Percentage change between the averages of the two 12-month windows.", True),
       th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True)]
OZ_EN = {"Tip": "Type", "Ölçü": "Size", "Renk ve malzeme": "Colour and material", "Özellik": "Feature", "İhtiyaç ve bağlam": "Need and context", "Marka ve kanal": "Brand and channel",
         "Asma": "Wall-hung", "Yerden / takım": "Floor-standing / close-coupled", "Gömme": "Concealed", "Kanalsız / rimless": "Rimless", "Çanak / tezgah üstü": "Bowl / countertop", "Etajerli / ayaklı": "With shelf / pedestal",
         "Köşe": "Corner", "Alaturka": "Squat", "Lavabolu": "With basin", "Aynalı": "With mirror", "Boy / kolon": "Tall / column", "Ölçü (cm)": "Size (cm)", "Ölçüleri / boyut": "Dimensions",
         "Siyah / antrasit": "Black / anthracite", "Beyaz": "White", "Ahşap / meşe": "Wood / oak", "Gri / renkli": "Grey / coloured", "Altın / bakır": "Gold / copper", "PVC / suya dayanıklı": "PVC / water-resistant",
         "MDF / lake": "MDF / lacquer", "Akıllı / elektronik": "Smart / electronic", "Yavaş kapanan": "Soft-close", "Işıklı / ledli": "Lit / LED", "Çekmeceli / kapaklı": "With drawers / doors",
         "Duvara tam dayalı": "Back-to-wall", "Küçük / dar banyo": "Small / narrow bathroom", "Modern / tasarım": "Modern / design", "Engelli / çocuk": "Accessible / children", "Modeller": "Models",
         "Fiyat": "Price", "Tamir / parça": "Repair / parts", "VitrA": "VitrA", "Rakip marka": "Competitor brand", "Perakendeci / pazaryeri": "Retailer / marketplace"}
def ozrows(o, secim):
    out = []
    for z in o["ozellik"]:
        if z["ad"] not in secim or not z["v12"]: continue
        out.append([x(z["grup"], OZ_EN[z["grup"]]), x(z["ad"], OZ_EN[z["ad"]]), cell(z["v12"]), n(yzd(z["pay"])), n(yz(z["yoy"])), '<div class="kwlist">%s</div>' % "".join(kw(k_) for k_ in z["ornek"][:3])])
    return out
OBAS = [th("Boyut", "Dimension", "Arama ifadesinde geçen özellik grubu.", "Attribute group appearing in the search phrase."),
        th("Arama özelliği", "Search attribute", "İfadede geçen özellik; bir kelime birden fazla özelliğe girebilir.", "Attribute in the phrase; a keyword can fall into more than one attribute."),
        th("Aylık hacim", "Monthly volume", "Eyl 2025 - Ağu 2026 aylık ortalama; genişletilmiş kelime evreni, yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 monthly average; expanded keyword universe, spelling variants counted once.", True),
        th("Pay", "Share", "Segmentin toplam arama hacmi içindeki pay.", "Share of the segment's total search volume.", True),
        th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True),
        th("Örnek", "Examples", "Özelliğin en yüksek hacimli kelimeleri.", "Highest-volume keywords for the attribute.")]
SEC_S = ["Asma", "Gömme", "Alaturka", "Kanalsız / rimless", "Çanak / tezgah üstü", "Ölçü (cm)", "Ölçüleri / boyut", "Renkli", "Gri / renkli", "Siyah / antrasit", "Akıllı / elektronik", "Yavaş kapanan", "Fiyat", "Modeller", "Tamir / parça", "Küçük / dar banyo", "Engelli / çocuk", "VitrA", "Rakip marka", "Perakendeci / pazaryeri"]
SEC_B = ["Lavabolu", "Aynalı", "Etajerli / ayaklı", "Köşe", "Ölçü (cm)", "Siyah / antrasit", "Ahşap / meşe", "Gri / renkli", "PVC / suya dayanıklı", "MDF / lake", "Işıklı / ledli", "Çekmeceli / kapaklı", "Küçük / dar banyo", "Modern / tasarım", "Modeller", "Fiyat", "VitrA", "Rakip marka", "Perakendeci / pazaryeri"]
def oz(o, ad): return next(z for z in o["ozellik"] if z["ad"] == ad)
kloz = K3["SSG|Klozetler|Klozetler"]; akil = K3["SSG|Klozetler|Akıllı Klozet Seti"]; ict = K3["SSG|Klozetler|Rezervuar ve Klozet İç Takımları"]; tak = K3["SSG|Klozetler|Takım Klozetler"]; bide = K3["SSG|Bideler|Bideler"]
bd = K3["BM|Banyo Dolapları|Banyo Dolapları"]; cm = K3["BM|Banyo Dolapları|Çamaşır Makinesi Dolapları"]; tz = K3["BM|Banyo Tezgahları|Banyo Tezgahları"]; kulp = K3["BM|Banyo Mobilya Tamamlayıcıları|Banyo Dolabı Kulpları"]; raf = K3["BM|Banyo Mobilya Tamamlayıcıları|Banyo Rafları"]
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
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
""" % (
 x("Seramik sağlık gereçleri (SSG: klozet, lavabo, bide, pisuvar, rezervuar) ve banyo mobilyası (BM) için talep dört yıllık aylık seriyle, ürün tipi düzeyinde incelenmiştir. İkinci bölümde aynı segmentlerin genişletilmiş kelime evreninde kullanıcının hangi tip, ölçü, renk, özellik ve bağlamla aradığı ölçülmüştür.",
   "Demand for sanitaryware (SSG: WCs, washbasins, bidets, urinals, cisterns) and bathroom furniture (BM) has been examined at product-type level with a four-year monthly series. The second part measures, in the expanded keyword universe for the same segments, which type, size, colour, feature and context the user searches with."),
 kpi_kart(yz(ssg["uc"]), "SSG talebi · 3 yıllık değişim (Eyl 22 - Ağu 23 → Eyl 25 - Ağu 26)", "SSG demand · 3-year change (Sep 22 - Aug 23 → Sep 25 - Aug 26)", "up"),
 kpi_kart(yz(bm["uc"]), "BM talebi · 3 yıllık değişim", "BM demand · 3-year change", "dn"),
 kpi_kart(yz(akil["uc"]), "Akıllı klozet seti · 3 yıllık değişim", "Smart WC sets · 3-year change", "up"),
 kpi_kart(yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]), "BM aramalarında perakendeci adı geçen pay · VitrA adı %s" % yzd(oz(OB, "VitrA")["pay"]), "Share of BM searches naming a retailer · VitrA named %s" % (yzd(oz(OB, "VitrA")["pay"]).replace("%", "") + "%"), "hi"),
 GRAFIK,
 insight("İki segment dört yılda ayrışmıştır. SSG talebi aylık %s civarında dengede kalmış ve üç yılda %s değişmiştir; BM talebi ise 2023-2024'teki %s seviyesinden %s seviyesine gerilemiş, üç yıllık değişim %s olmuştur. SSG'nin dayanıklılığı klozetin \"zorunlu değişim\" ürünü olmasından, BM'deki gerileme ise mobilya kararının ertelenebilir olmasından kaynaklanıyor olarak okunabilir." % (k(ssg["p3"]), yz(ssg["uc"]), k(bm["p1"]), k(bm["p3"]), yz(bm["uc"])),
         "The two segments have diverged over four years. SSG demand stayed balanced at around %s per month and changed %s over three years; BM demand fell from %s in 2023-2024 to %s, a three-year change of %s. SSG's resilience can be read as stemming from the WC being a \"must-replace\" product, and the BM decline from the furniture decision being deferrable." % (k(ssg["p3"]), yz(ssg["uc"]), k(bm["p1"]), k(bm["p3"]), yz(bm["uc"])), "D1"),
 x("SSG: ürün tipi düzeyinde değişim", "SSG: change by product type"),
 tablo(BAS, k3rows("SSG", 16), "uzun"),
 insight("SSG içinde büyüme üç tipte toplanmaktadır: jenerik klozet aramaları (%s, 3 yılda %s), rezervuar ve klozet iç takımları (%s, %s) ve akıllı klozet setleri (%s, %s). Takım klozet (%s) ve bide (%s) aramaları ise belirgin biçimde daralmıştır; bide talebinin bir kısmının taharet fonksiyonlu klozete ve taharet musluğuna kaydığı değerlendirilebilir. İç takım talebinin büyümesi, mevcut ürün sahibinin yedek parça ihtiyacının arttığına işaret etmektedir." % (k(kloz["p3"]), yz(kloz["uc"]), k(ict["p3"]), yz(ict["uc"]), k(akil["p3"]), yz(akil["uc"]), yz(tak["uc"]), yz(bide["uc"])),
         "Within SSG, growth is concentrated in three types: generic WC searches (%s, %s over 3 years), cistern and WC inner mechanisms (%s, %s) and smart WC sets (%s, %s). Close-coupled WC (%s) and bidet (%s) searches have contracted markedly; part of bidet demand can be considered to have shifted to WCs with a bidet function and to bidet valves. Growth in inner-mechanism demand points to rising spare-part needs among existing owners." % (k(kloz["p3"]), yz(kloz["uc"]), k(ict["p3"]), yz(ict["uc"]), k(akil["p3"]), yz(akil["uc"]), yz(tak["uc"]), yz(bide["uc"])), "D1"),
 x("BM: ürün tipi düzeyinde değişim", "BM: change by product type"),
 tablo(BAS, k3rows("BM", 13), "uzun"),
 insight("BM'de yalnızca iki tip talebini korumuştur: banyo tezgahları (%s) ve çamaşır makinesi dolapları (%s). Jenerik banyo dolabı aramaları %s, kulp %s ve raf %s daralmıştır. Çamaşır makinesi dolabı, banyo mobilyasının \"fonksiyonel\" ucunda duran ve konut küçüldükçe önemi artan bir tiptir; VitrA'nın bu tipte 29 ürünü bulunmakta, ancak Trendyol'un ilk 40 sonucunda görünmemektedir (Bölüm 09)." % (yz(tz["uc"]), yz(cm["uc"]), yz(bd["uc"]), yz(kulp["uc"]), yz(raf["uc"])),
         "In BM only two types have held their demand: bathroom countertops (%s) and washing machine cabinets (%s). Generic bathroom cabinet searches have contracted %s, handles %s and shelves %s. The washing machine cabinet sits at the \"functional\" end of bathroom furniture and gains importance as homes get smaller; VitrA has 29 products of this type but does not appear in Trendyol's top 40 results (Section 09)." % (yz(tz["uc"]), yz(cm["uc"]), yz(bd["uc"]), yz(kulp["uc"]), yz(raf["uc"])), "D1", "D15"),
 x("Kullanıcı hangi özellikle arıyor? SSG", "Which attributes does the user search with? SSG"),
 tablo(OBAS, ozrows(OS, SEC_S), "uzun"),
 x("Kullanıcı hangi özellikle arıyor? BM", "Which attributes does the user search with? BM"),
 tablo(OBAS, ozrows(OB, SEC_B), "uzun"),
 insight("SSG'de aramaların %s'i fiyat, %s'i tamir ve parça, %s'i \"modeller\" ifadesi taşımaktadır; rakip marka adı geçen aramalar (%s) VitrA adı geçen aramalardan (%s) fazladır ve Serel, Geberit, Visam ile Creavit gömme rezervuar ve iç takım aramalarında öne çıkmaktadır. BM'de ise en belirgin sinyal kanal tarafındadır: aramaların %s'i Koçtaş, IKEA veya Trendyol gibi perakendeci adıyla yapılmakta, VitrA adıyla yapılanlar %s'te kalmaktadır. BM kullanıcısı ürün tipinden çok ölçü (%s), lavabolu set (%s) ve aydınlatmalı ayna (%s) üzerinden aramakta; PVC ve suya dayanıklı gövde aramaları %s ile en hızlı büyüyen özelliktir." % (yzd(oz(OS, "Fiyat")["pay"]), yzd(oz(OS, "Tamir / parça")["pay"]), yzd(oz(OS, "Modeller")["pay"]), yzd(oz(OS, "Rakip marka")["pay"]), yzd(oz(OS, "VitrA")["pay"]), yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]), yzd(oz(OB, "VitrA")["pay"]), yzd(oz(OB, "Ölçü (cm)")["pay"]), yzd(oz(OB, "Lavabolu")["pay"]), yzd(oz(OB, "Işıklı / ledli")["pay"]), yz(oz(OB, "PVC / suya dayanıklı")["yoy"])),
         "In SSG, %s of searches carry price, %s repair and parts, and %s the word \"models\"; searches naming a competitor brand (%s) exceed those naming VitrA (%s), with Serel, Geberit, Visam and Creavit prominent in concealed cistern and inner-mechanism searches. In BM the clearest signal is on the channel side: %s of searches are made with a retailer name such as Koçtaş, IKEA or Trendyol, while those with the VitrA name stay at %s. The BM user searches less by product type than by size (%s), basin-included set (%s) and lit mirror (%s); PVC and water-resistant body searches are the fastest-growing attribute at %s." % (yzd(oz(OS, "Fiyat")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Tamir / parça")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Modeller")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Rakip marka")["pay"]).replace("%", "") + "%", yzd(oz(OS, "VitrA")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]).replace("%", "") + "%", yzd(oz(OB, "VitrA")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Ölçü (cm)")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Lavabolu")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Işıklı / ledli")["pay"]).replace("%", "") + "%", yz(oz(OB, "PVC / suya dayanıklı")["yoy"])), "D12"),
 kaynak("Google Ads Keyword Planner · çekirdek 2.420 kelime 48 ay (Eyl 2022 - Ağu 2026) · genişletilmiş kelime evreni (keywords for keywords, 52.973 kelime) · Türkiye, Türkçe · %s" % veri.TARIH,
        "Google Ads Keyword Planner · core 2,420 keywords over 48 months (Sep 2022 - Aug 2026) · expanded keyword universe (keywords for keywords, 52,973 keywords) · Turkey, Turkish · %s" % veri.TARIH, "D1", "D12"),
)
