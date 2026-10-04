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
        out.append([kat2(k2), kat2(k3) if k3 != k2 else x("Genel", "General"), cellk(v["p0"]), cellk(v["p3"]), n(yz(v["uc"])), n(yz(v["yoy"]))])
    return out
from grafik2 import sapma as _sp, gruplu as _gr, f_deg as _fd, f_k as _fk
from b_talep import sekmeler as _sek
def k3grafik(seg, lim):
    """Iki sekme: 3 yillik degisim (yuzde, siralı) ve iki donemin aylik ortalama hacmi (yan yana cubuk)."""
    sat = sorted([(k, v) for k, v in K3.items() if k.startswith(seg + "|")], key=lambda i: -i[1]["p3"])[:lim]
    et = {kk: kat2(kk.split("|")[2]) for kk, _ in sat}
    renk = "#E85F36" if seg == "BM" else "#10332F"
    dg = sorted(sat, key=lambda i: -i[1]["uc"])
    G1 = _sp([(et[kk], v["uc"]) for kk, v in dg], x("3 yıllık değişim", "3-year change"),
             x("%s ürün tipleri · Eyl 2022 - Ağu 2023 tabanına göre Eyl 2025 - Ağu 2026 aylık ortalama arama hacmindeki değişim, en çok artandan en çok azalana" % seg,
               "%s product types · change in average monthly search volume from the Sep 2022 - Aug 2023 base to Sep 2025 - Aug 26, from the largest increase to the largest decrease" % seg),
             ek=[(x("Eyl 2022 - Ağu 2023 aylık ort.", "Sep 2022 - Aug 2023 monthly avg."), [_fk(v["p0"]) for _, v in dg]), (x("Eyl 2025 - Ağu 2026 aylık ort.", "Sep 2025 - Aug 2026 monthly avg."), [_fk(v["p3"]) for _, v in dg])])
    G2 = _gr([(et[kk], [v["p0"], v["p3"]]) for kk, v in sat],
             [(x("Eyl 2022 - Ağu 2023 aylık ort.", "Sep 2022 - Aug 2023 monthly avg."), "#B9C4C1"), (x("Eyl 2025 - Ağu 2026 aylık ort.", "Sep 2025 - Aug 2026 monthly avg."), renk)],
             x("%s ürün tipleri · iki dönemin aylık ortalama arama hacmi, hacme göre sıralı" % seg, "%s product types · average monthly search volume in the two periods, sorted by volume" % seg), bicim=_fk)
    return _sek([("3 yıllık değişim (%)", "3-year change (%)", G1), ("Arama hacmi: iki dönem", "Search volume: two periods", G2)], "gtabs")
BAS = [th("Alt kategori", "Sub-category", "VitrA kategori ağacındaki alt kategori.", "Sub-category in the VitrA category tree."),
       th("Ürün tipi", "Product type", "Alt kategorinin altındaki ürün tipi; \"Genel\" ürün tipi belirtilmeden, alt kategori ya da kategori adıyla yapılan aramalardır.", "Product type under the sub-category; \"General\" is searches made with the sub-category name."),
       th("Eyl 2022 - Ağu 2023", "Sep 2022 - Aug 2023", "Eylül 2022 - Ağustos 2023 aylık ortalama arama hacmi.", "Average monthly search volume, September 2022 - August 2023.", True),
       th("Eyl 2025 - Ağu 2026", "Sep 2025 - Aug 2026", "Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Average monthly search volume, September 2025 - August 2026.", True),
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
        out.append([x(z["grup"], OZ_EN[z["grup"]]), x(z["ad"], OZ_EN[z["ad"]]), cellk(z["v12"]), n(yzd(z["pay"])), n(yz(z["yoy"])), '<div class="kwlist">%s</div>' % "".join(kw(k_) for k_ in z["ornek"][:3])])
    return out
OBAS = [th("Boyut", "Dimension", "Arama ifadesinde geçen özellik grubu.", "Attribute group appearing in the search phrase."),
        th("Arama özelliği", "Search attribute", "İfadede geçen özellik; bir kelime birden fazla özelliğe girebilir.", "Attribute in the phrase; a keyword can fall into more than one attribute."),
        th("Aylık hacim", "Monthly volume", "Eyl 2025 - Ağu 2026 aylık ortalama; genişletilmiş kelime evreni, yazım varyantları tek sayılmıştır.", "Sep 2025 - Aug 2026 monthly average; expanded keyword universe, spelling variants counted once.", True),
        th("Pay", "Share", "Segmentin toplam arama hacmi içindeki pay.", "Share of the segment's total search volume.", True),
        th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True),
        th("Örnek", "Examples", "Özelliğin en yüksek hacimli kelimeleri.", "Highest-volume keywords for the attribute.")]
SEC_S = ["Asma", "Yerden / takım", "Gömme", "Etajerli / ayaklı", "Alaturka", "Kanalsız / rimless", "Çanak / tezgah üstü", "Ölçü (cm)", "Ölçüleri / boyut", "Gri / renkli", "Siyah / antrasit", "Akıllı / elektronik", "Yavaş kapanan", "Fiyat", "Modeller", "Tamir / parça", "Küçük / dar banyo", "Engelli / çocuk", "VitrA", "Rakip marka", "Perakendeci / pazaryeri"]
SEC_B = ["Lavabolu", "Aynalı", "Etajerli / ayaklı", "Köşe", "Ölçü (cm)", "Siyah / antrasit", "Ahşap / meşe", "Gri / renkli", "PVC / suya dayanıklı", "MDF / lake", "Işıklı / ledli", "Çekmeceli / kapaklı", "Küçük / dar banyo", "Modern / tasarım", "Modeller", "Fiyat", "VitrA", "Rakip marka", "Perakendeci / pazaryeri"]
def oz(o, ad): return next(z for z in o["ozellik"] if z["ad"] == ad)
kloz = K3["SSG|Klozetler|Klozetler"]; akil = K3["SSG|Klozetler|Akıllı Klozet Seti"]; ict = K3["SSG|Klozetler|Rezervuar ve Klozet İç Takımları"]; tak = K3["SSG|Klozetler|Takım Klozetler"]; bide = K3["SSG|Bideler|Bideler"]
bd = K3["BM|Banyo Dolapları|Banyo Dolapları"]; cm = K3["BM|Banyo Dolapları|Çamaşır Makinesi Dolapları"]; tz = K3["BM|Banyo Tezgahları|Banyo Tezgahları"]; kulp = K3["BM|Banyo Mobilya Tamamlayıcıları|Banyo Dolabı Kulpları"]; raf = K3["BM|Banyo Mobilya Tamamlayıcıları|Banyo Rafları"]
_SR = [r for r in SB["kw_ssgbm"] if r[1] == "SSG"]
def _ex(f):
    L_ = [r for r in _SR if f(r) and r[6] is not None]; return 100 * (sum(r[4] for r in L_) / sum(r[4] / (1 + r[6] / 100) for r in L_) - 1)
_SSG_EXWC = _ex(lambda r: r[0] != "wc"); _KL_EXWC = _ex(lambda r: r[0] != "wc" and r[2] == "Klozetler" and r[3] == "Klozetler"); _WC = next(r for r in _SR if r[0] == "wc")
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
 x("Seramik sağlık gereçleri (SSG: klozet, klozet kapağı, lavabo, bide, pisuvar, evye, rezervuar) ve banyo mobilyası (BM) için talep dört yıllık aylık seriyle, ürün tipi düzeyinde incelenmiştir. Genişletilmiş kelime evreninde kullanıcının hangi <b>tip, ölçü, renk, özellik ve bağlamla</b> aradığı da ölçülmüştür.",
   "Demand for sanitaryware (SSG: WCs, toilet seats, washbasins, bidets, urinals, sinks, cisterns) and bathroom furniture (BM) has been examined at product-type level with a four-year monthly series. The expanded keyword universe also measures which <b>type, size, colour, feature and context</b> the user searches with."),
 kpi_kart(yz(ssg["uc"]), "SSG talebi · 3 yıllık değişim (Eyl 2022 - Ağu 2023 → Eyl 2025 - Ağu 2026)", "SSG demand · 3-year change (Sep 2022 - Aug 2023 → Sep 2025 - Aug 2026)", "dn" if ssg["uc"] < 0 else "up"),
 kpi_kart(yz(bm["uc"]), "BM talebi · 3 yıllık değişim", "BM demand · 3-year change", "dn"),
 kpi_kart(yz(akil["uc"]), "Akıllı klozet seti · 3 yıllık değişim, düşük tabandan (%s → %s)" % (k(akil["p0"]), k(akil["p3"])), "Smart WC sets · 3-year change, from a low base (%s → %s)" % (k(akil["p0"]).replace(",", "."), k(akil["p3"]).replace(",", ".")), "up"),
 kpi_kart(yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]), "BM aramalarında perakendeci adı geçen pay · VitrA adı %s" % yzd(oz(OB, "VitrA")["pay"]), "Share of BM searches naming a retailer · VitrA named %s" % (yzd(oz(OB, "VitrA")["pay"]).replace("%", "") + "%"), "hi"),
 GRAFIK,
 insight("İki segment dört yılda ayrışmıştır. SSG talebi Eyl 2025 - Ağu 2026 döneminde aylık %s seviyesinde ve Eyl 2022 - Ağu 2023 tabanına göre %s değişmiştir; BM talebi ise aynı tabandaki %s seviyesinden %s seviyesine gerilemiş, üç yıllık değişim %s olmuştur. SSG sonucu tek bir kelimeye duyarlıdır: \"wc\" aramaları üç yılda %s artmıştır (Google Trends de belirgin bir artış göstermektedir); bu kelime hariç SSG değişimi %s, genel klozet aramalarınınki %s'tir. SSG'deki gerilemenin sınırlı kalmasının klozetin arıza ve değişimle talebi süren bir ürün olmasıyla, BM'deki gerilemenin ise mobilya kararının ertelenebilir olmasıyla ilişkili olduğu değerlendirilebilir." % (k(ssg["p3"]), yz(ssg["uc"]), k(bm["p0"]), k(bm["p3"]), yz(bm["uc"]), yzd(_WC[6], 0), yz(_SSG_EXWC), yz(_KL_EXWC)),
         "The two segments have diverged over four years. SSG demand stood at %s per month in Sep 2025 - Aug 2026 and changed %s against the Sep 2022 - Aug 2023 base; BM demand fell from %s in the same base to %s, a three-year change of %s. The SSG result is sensitive to a single keyword: searches for \"wc\" grew %s over three years (Google Trends also shows a clear increase); excluding it, the SSG change is %s and generic WC searches %s. The limited decline in SSG can be linked to the WC being a product whose demand continues through breakdown and replacement, and the decline in BM to the furniture decision being deferrable." % (k(ssg["p3"]), yz(ssg["uc"]), k(bm["p0"]), k(bm["p3"]), yz(bm["uc"]), ("%.0f" % _WC[6]) + "%", yz(_SSG_EXWC), yz(_KL_EXWC)), "D1"),
 x("SSG: ürün tipi düzeyinde değişim", "SSG: change by product type"),
 k3grafik("SSG", 16) + tablo(BAS, k3rows("SSG", 16), "uzun"),
 insight("SSG içinde büyüme jenerik klozet aramaları (%s, 3 yılda %s), rezervuar ve klozet iç takımları (%s, %s) ve akıllı klozet setleri (%s, %s) olmak üzere üç tipte toplanmaktadır. Takım klozet (%s) ve bide (%s) aramaları ise belirgin biçimde daralmıştır; bide talebinin bir kısmının taharet fonksiyonlu klozete ve taharet musluğuna kaydığı değerlendirilebilir. İç takım talebinin üç yıllık dönemde büyümesi, mevcut ürün sahibinin yedek parça ihtiyacının arttığı şeklinde okunabilir; bu aramaların bir kısmı rakip marka adı taşımaktadır. Akıllı klozet setlerindeki üç yıllık artış düşük bir tabandan gelmektedir; son yılda değişim %s düzeyindedir." % (k(kloz["p3"]), yz(kloz["uc"]), k(ict["p3"]), yz(ict["uc"]), k(akil["p3"]), yz(akil["uc"]), yz(tak["uc"]), yz(bide["uc"]), yz(akil["yoy"])),
         "Within SSG, growth is concentrated in three types: generic WC searches (%s, %s over 3 years), cistern and WC inner mechanisms (%s, %s) and smart WC sets (%s, %s). Close-coupled WC (%s) and bidet (%s) searches have contracted markedly; part of bidet demand can be considered to have shifted to WCs with a bidet function and to bidet valves. Growth in inner-mechanism demand points to rising spare-part needs among existing owners. The three-year rise in smart WC sets comes from a low base; the change over the last year is %s." % (k(kloz["p3"]), yz(kloz["uc"]), k(ict["p3"]), yz(ict["uc"]), k(akil["p3"]), yz(akil["uc"]), yz(tak["uc"]), yz(bide["uc"]), yz(akil["yoy"])), "D1"),
 x("BM: ürün tipi düzeyinde değişim", "BM: change by product type"),
 k3grafik("BM", 13) + tablo(BAS, k3rows("BM", 13), "uzun"),
 insight("BM'de yalnızca çamaşır makinesi dolapları (%s) üç yıllık dönemde talebini korumuştur; banyo tezgahı aramaları %s, jenerik banyo dolabı aramaları %s, kulp %s ve raf %s daralmıştır. Çamaşır makinesi dolabının, banyo mobilyasının \"fonksiyonel\" ucunda duran ve küçük konutlarda önem kazanabilen bir tip olduğu değerlendirilebilir; VitrA'nın bu tipte 29 ürünü bulunmakta, ancak Trendyol'un ilk 40 sonucunda görünmemektedir (Bölüm [[b:katalog]])." % (yz(cm["uc"]), yz(tz["uc"]), yz(bd["uc"]), yz(kulp["uc"]), yz(raf["uc"])),
         "In BM only washing machine cabinets (%s) held their demand over three years; bathroom countertop searches contracted %s, generic bathroom cabinet searches %s, handles %s and shelves %s. The washing machine cabinet can be seen as a type at the \"functional\" end of bathroom furniture that may gain importance in smaller homes; VitrA has 29 products of this type but does not appear in Trendyol's top 40 results (Section [[b:katalog]])." % (yz(cm["uc"]), yz(tz["uc"]), yz(bd["uc"]), yz(kulp["uc"]), yz(raf["uc"])), "D1", "D15"),
 x("Kullanıcı hangi özellikle arıyor? SSG", "Which attributes does the user search with? SSG"),
 tablo(OBAS, ozrows(OS, SEC_S), "uzun"),
 x("Kullanıcı hangi özellikle arıyor? BM", "Which attributes does the user search with? BM"),
 tablo(OBAS, ozrows(OB, SEC_B), "uzun"),
 insight("SSG'de aramaların %s'i fiyat, %s'i tamir ve parça, %s'i \"modeller\" ifadesi taşımaktadır; marka adı geçen aramalarda VitrA tek başına en sık aranan markadır (%s); 19 rakip markanın toplamı %s'dir ve Serel, Geberit, Visam ile Creavit gömme rezervuar ve iç takım aramalarında öne çıkmaktadır. BM'de ise en belirgin sinyal kanal tarafındadır: aramaların %s'i Koçtaş, IKEA veya Trendyol gibi perakendeci adıyla yapılmakta, VitrA adıyla yapılanlar %s'te kalmaktadır. BM aramalarında \"modeller\" ifadesinin yanında ölçü (%s), lavabolu set (%s) ve aydınlatmalı ayna (%s) öne çıkmakta; PVC ve suya dayanıklı gövde aramaları %s ile malzeme ve renk özellikleri arasında en hızlı büyüyendir." % (yzd(oz(OS, "Fiyat")["pay"]), yzd(oz(OS, "Tamir / parça")["pay"]), yzd(oz(OS, "Modeller")["pay"]), yzd(oz(OS, "VitrA")["pay"]), yzd(oz(OS, "Rakip marka")["pay"]), yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]), yzd(oz(OB, "VitrA")["pay"]), yzd(oz(OB, "Ölçü (cm)")["pay"]), yzd(oz(OB, "Lavabolu")["pay"]), yzd(oz(OB, "Işıklı / ledli")["pay"]), yz(oz(OB, "PVC / suya dayanıklı")["yoy"])),
         "In SSG, %s of searches carry price, %s repair and parts, and %s the word \"models\"; among searches naming a brand VitrA alone is the most searched (%s); 19 competitor brands together account for %s, with Serel, Geberit, Visam and Creavit prominent in concealed cistern and inner-mechanism searches. In BM the clearest signal is on the channel side: %s of searches are made with a retailer name such as Koçtaş, IKEA or Trendyol, while those with the VitrA name stay at %s. In BM searches, besides the word \"models\", size (%s), basin-included sets (%s) and lit mirrors (%s) stand out; PVC and water-resistant body searches are the fastest-growing material and colour attribute at %s." % (yzd(oz(OS, "Fiyat")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Tamir / parça")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Modeller")["pay"]).replace("%", "") + "%", yzd(oz(OS, "VitrA")["pay"]).replace("%", "") + "%", yzd(oz(OS, "Rakip marka")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Perakendeci / pazaryeri")["pay"]).replace("%", "") + "%", yzd(oz(OB, "VitrA")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Ölçü (cm)")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Lavabolu")["pay"]).replace("%", "") + "%", yzd(oz(OB, "Işıklı / ledli")["pay"]).replace("%", "") + "%", yz(oz(OB, "PVC / suya dayanıklı")["yoy"])), "D12"),
 kaynak("Google Ads Keyword Planner · temel set 2.299 kelime 48 ay (Eyl 2022 - Ağu 2026) · genişletilmiş kelime evreni (Google Ads anahtar kelime önerileri, 52.973 kelime) · Türkiye, Türkçe · %s" % veri.TARIH,
        "Google Ads Keyword Planner · base set 2,299 keywords over 48 months (Sep 2022 - Aug 2026) · expanded keyword universe (Google Ads keyword suggestions, 52,973 keywords) · Turkey, Turkish · %s" % veri.TARIH, "D1", "D12"),
)
