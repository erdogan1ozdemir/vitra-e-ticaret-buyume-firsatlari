# -*- coding: utf-8 -*-
"""Bolum: Ihtiyac dili - kullanici ne ariyor (niyet siniflari)."""
from ortak import *
from rapor_parca1 import T
from b_talep import kat, KAT_EN
NI = A["niyet"]; NK = A["niyet_k1"]; OR = A["niyet_ornek"]
N_EN = {"Jenerik ürün": "Generic product", "Tasarım ve fikir": "Design and ideas", "Fiyat": "Price", "Seçim ve karşılaştırma": "Selection and comparison", "Ölçü ve teknik": "Dimensions and technical",
        "Tamir ve bakım": "Repair and maintenance", "Montaj": "Installation", "Taksit ve ödeme": "Instalment and payment", "Yer ve kanal": "Where to buy"}
N_AC = {"Jenerik ürün": ("Ürün adı veya ürün adı + tip: \"banyo dolabı\", \"duşakabin\", \"klozet\"", "Product name or product name + type: \"bathroom cabinet\", \"shower enclosure\", \"WC\""),
        "Tasarım ve fikir": ("\"modelleri\", \"dekorasyon\", \"küçük banyo\" gibi ilham arayan ifadeler", "Inspiration-seeking phrases such as \"models\", \"decoration\", \"small bathroom\""),
        "Fiyat": ("\"fiyat\", \"fiyatları\", \"ucuz\", \"indirim\" içeren ifadeler", "Phrases containing \"price\", \"prices\", \"cheap\", \"discount\""),
        "Seçim ve karşılaştırma": ("\"hangisi\", \"en iyi\", \"nedir\", \"tavsiye\" gibi karar öncesi sorular", "Pre-decision questions such as \"which\", \"best\", \"what is\", \"recommendation\""),
        "Ölçü ve teknik": ("\"ölçüleri\", \"80 cm\", \"kaç litre\" gibi ölçü ve teknik ifadeler", "Dimension and technical phrases such as \"dimensions\", \"80 cm\", \"how many litres\""),
        "Tamir ve bakım": ("\"iç takımı\", \"tamiri\", \"su kaçırıyor\", \"yedek parça\"", "\"inner mechanism\", \"repair\", \"leaking\", \"spare part\""),
        "Montaj": ("\"montajı\", \"nasıl takılır\", \"montaj aparatı\"", "\"installation\", \"how to fit\", \"fitting kit\"")}
def niy(nm): return x(nm, N_EN[nm])
sira = sorted(NI, key=lambda k: -NI[k]["a26"]); tot26 = sum(NI[k]["a26"] for k in NI)
rows = []
for nm in sira:
    v = NI[nm]; ex = ", ".join(kw(kw_) for kw_, _ in OR[nm][:4])
    rows.append([niy(nm), x(*N_AC[nm]), cell(v["n"]), cell(v["a26"]), n(yzd(100 * v["a26"] / tot26)), n(yz(v["yoy"])), '<div class="kwlist">%s</div>' % ex])
tbl = tablo([th("İhtiyaç sınıfı", "Need class", "Kelimenin taşıdığı ihtiyaç; ifade kalıplarına göre sınıflandırılmıştır, markalı kelimeler dışarıda tutulmuştur.", "The need carried by the keyword; classified by phrase patterns, branded keywords excluded."),
             th("Tanım", "Definition", "Sınıfa giren ifade kalıpları.", "Phrase patterns included in the class."),
             th("Kelime", "Keywords", "Sınıftaki kelime sayısı.", "Number of keywords in the class.", True),
             th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi (sınıftaki kelimelerin toplamı).", "Average monthly search volume, January - August 2026 (sum of the class's keywords).", True),
             th("Pay", "Share", "Sınıfın toplam markasız hacim içindeki payı.", "The class's share of total non-brand volume.", True),
             th("YoY", "YoY", "Oca-Ağu 2026 / Oca-Ağu 2025 yüzde değişimi.", "Percentage change, Jan-Aug 2026 / Jan-Aug 2025.", True),
             th("Örnek", "Examples", "Sınıfın en yüksek hacimli kelimeleri.", "Highest-volume keywords in the class.")], rows)
kats = ["Vitrifiyeler", "Banyo Mobilyaları", "Yıkanma Alanları", "Rezervuarlar", "Armatürler", "Karo Seramik Ürünleri", "Duşlar", "Banyo Aksesuarları"]
cols = ["Fiyat", "Tasarım ve fikir", "Seçim ve karşılaştırma", "Ölçü ve teknik", "Montaj", "Tamir ve bakım"]
rows2 = []
for kk in kats:
    tk = sum(v["a26"] for key, v in NK.items() if key.startswith(kk + "|"))
    r = [kat(kk), cell(tk)]
    for c in cols:
        v = NK.get(kk + "|" + c, {"a26": 0})["a26"]
        r.append(n(yzd(100 * v / tk) if v else "-"))
    rows2.append(r)
tbl2 = tablo([th("Kategori", "Category", "Ana kategori.", "Main category."),
              th("Markasız hacim · 2026 aylık ort.", "Non-brand volume · 2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama, markalı kelimeler hariç.", "January - August 2026 monthly average, branded keywords excluded.", True)] +
             [th(c, N_EN[c], "Sınıfın kategori hacmi içindeki payı, Oca-Ağu 2026.", "The class's share of the category's volume, Jan-Aug 2026.", True) for c in cols], rows2, "dar")
GS = A["gsc_sorgu_niyet"]; GE = A["gsc_sorgu_ornek"]
G_EN = {"Ürün": "Product", "Fiyat": "Price", "Tasarım": "Design", "Tamir ve bakım": "Repair and maintenance", "Ölçü ve teknik": "Dimensions and technical", "Seçim": "Selection", "Montaj": "Installation", "Bayi ve mağaza": "Dealer and store"}
gtot = sum(v[0] for v in GS.values())
rows3 = []
for key, v in GS.items():
    m, nm = key.split(" · "); ex = ", ".join(kw(q) for q, _ in GE[key][:3])
    rows3.append([x(m, "Branded" if m == "Markalı" else "Non-brand"), x(nm, G_EN[nm]), cell(v[0]), n(yzd(100 * v[0] / gtot)), cell(v[1]), n(yzd(100 * v[0] / v[1]) if v[1] else "-"), '<div class="kwlist">%s</div>' % ex])
tbl3 = tablo([th("Marka", "Brand", "Sorgunun \"vitra\" veya \"artema\" içerip içermediği.", "Whether the query contains \"vitra\" or \"artema\"."),
              th("İhtiyaç sınıfı", "Need class", "Sorgunun ifade kalıbına göre sınıfı.", "Class of the query by phrase pattern."),
              th("Tık", "Clicks", "Google Search Console, 1 Haz 2025 - 25 Eyl 2026, ilk 25.000 sorgu.", "Google Search Console, 1 Jun 2025 - 25 Sep 2026, top 25,000 queries.", True),
              th("Pay", "Share", "Sınıfın toplam tık içindeki payı.", "The class's share of total clicks.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Örnek", "Examples", "Sınıfın en çok tık alan sorguları.", "Queries with most clicks in the class.")], rows3, "uzun")
fiyat = NI["Fiyat"]; tas = NI["Tasarım ve fikir"]; tam = NI["Tamir ve bakım"]; mon = NI["Montaj"]
HTML = """
<p class="lede">%s</p>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Aynı kelime seti, kullanıcının hangi ihtiyaçla aradığına göre yeniden sınıflandırılmıştır. Kategori adıyla yapılan jenerik aramaların dışında kalan altı ihtiyaç sınıfı, e-ticaret sayfalarının hangi soruya cevap vermesi gerektiğini göstermektedir.",
   "The same keyword set has been reclassified by the need the user is searching with. The six need classes outside generic category-name searches show which question the e-commerce pages need to answer."),
 tbl,
 insight("Markasız talebin %s'i yalnızca ürün adıyla yapılan jenerik aramalardır; ihtiyacı belirgin altı sınıf toplamın yaklaşık %s'ini oluşturmaktadır. Bu sınıflar içinde Tasarım ve fikir aramaları (%s) tek büyüyen grup olarak %s artmış, Fiyat aramaları (%s) %s daralmıştır. Tamir ve bakım (%s) ile Montaj (%s) hacim olarak küçük görünse de bu ifadeler karar sonrası, yüksek niyetli ve mevcut ürün sahibinden gelen aramalardır; e-ticaret sayfalarında bu iki sınıfa karşılık gelen içerik ve yedek parça akışı sınırlıdır." % (yzd(100 * NI["Jenerik ürün"]["a26"] / tot26), yzd(100 * (tot26 - NI["Jenerik ürün"]["a26"]) / tot26), k(tas["a26"]), yz(tas["yoy"]), k(fiyat["a26"]), yz(fiyat["yoy"]), k(tam["a26"]), k(mon["a26"])),
         "%s of non-brand demand consists of generic searches made with the product name only; the six classes with an explicit need make up about %s of the total. Among them, Design and ideas searches (%s) grew %s as the only rising group, while Price searches (%s) contracted %s. Repair and maintenance (%s) and Installation (%s) look small in volume, but these are post-decision, high-intent searches from existing product owners; the content and spare-part flow corresponding to these two classes on the e-commerce pages is limited." % (yzd(100 * NI["Jenerik ürün"]["a26"] / tot26), yzd(100 * (tot26 - NI["Jenerik ürün"]["a26"]) / tot26), k(tas["a26"]), yz(tas["yoy"]), k(fiyat["a26"]), yz(fiyat["yoy"]), k(tam["a26"]), k(mon["a26"])), "D1"),
 x("Kategori bazında ihtiyaç dağılımı", "Need distribution by category"),
 tbl2,
 insight("İhtiyaç profili kategoriye göre belirgin biçimde farklılaşmaktadır. Vitrifiyeler ve Yıkanma Alanlarında fiyat aramalarının payı yüksektir (\"klozet fiyat\", \"duşakabin fiyatları\"); Karo Seramik ve Banyo Mobilyalarında ise tasarım ve model aramaları öne çıkmaktadır (\"banyo dolabı modelleri\", \"banyo fayans modelleri\"). Tamir ve montaj aramaları neredeyse tamamen Vitrifiyeler ve Rezervuarlar altında toplanmaktadır (\"klozet iç takımı\", \"gömme rezervuar tamiri\"). Bu dağılım, ürün sayfası şablonunun kategoriye göre farklı önceliklerle kurgulanmasını gerektirmektedir: klozet ve rezervuar sayfasında fiyat, teslimat ve yedek parça; mobilya ve karo sayfasında görsel, ölçü ve kombinasyon.",
         "The need profile differs markedly by category. In Sanitaryware and Bathing Areas the share of price searches is high (\"klozet fiyat\", \"duşakabin fiyatları\"); in Ceramic Tiles and Bathroom Furniture design and model searches come to the fore (\"banyo dolabı modelleri\", \"banyo fayans modelleri\"). Repair and installation searches are concentrated almost entirely under Sanitaryware and Cisterns (\"klozet iç takımı\", \"gömme rezervuar tamiri\"). This distribution requires the product page template to be built with different priorities per category: price, delivery and spare parts on WC and cistern pages; visuals, dimensions and combinations on furniture and tile pages.", "D1"),
 x("Sitenin fiilen aldığı trafik: Search Console sorguları", "Traffic the site actually receives: Search Console queries"),
 tbl3,
 insight("vitra.com.tr'nin aldığı organik tıkların %s'i markalı sorgulardan gelmektedir (\"vitra\" tek başına %s tık). Markasız tarafta jenerik ürün sorguları toplam tıkların %s'ini oluştururken fiyat sorguları (%s) ve tasarım sorguları (%s) sınırlı kalmaktadır. Dikkat çeken nokta tamir ve montaj tarafındadır: markasız tamir sorguları %s gösterim almasına rağmen yalnızca %s tık üretmekte, CTR %s seviyesinde kalmaktadır. Talep görünmekte ancak site bu soruların cevabı olarak algılanmamaktadır; bu alan içerik ve yedek parça e-ticareti için fırsat taşımaktadır." % (yzd(100 * A["gsc_marka"]["markali"] / A["gsc_marka"]["toplam_sorgu"]), bin(A["gsc_top_sorgu"][0][1]), yzd(100 * GS["Markasız · Ürün"][0] / gtot), yzd(100 * GS["Markasız · Fiyat"][0] / gtot), yzd(100 * GS["Markasız · Tasarım"][0] / gtot), k(GS["Markasız · Tamir ve bakım"][1]), bin(GS["Markasız · Tamir ve bakım"][0]), yzd(100 * GS["Markasız · Tamir ve bakım"][0] / GS["Markasız · Tamir ve bakım"][1])),
         "%s of the organic clicks vitra.com.tr receives come from branded queries (\"vitra\" alone %s clicks). On the non-brand side, generic product queries make up %s of total clicks while price queries (%s) and design queries (%s) stay limited. The notable point is on the repair and installation side: non-brand repair queries generate only %s clicks despite %s impressions, with CTR at %s. Demand is visible but the site is not perceived as the answer to these questions; this area holds opportunity for content and spare-part e-commerce." % (yzd(100 * A["gsc_marka"]["markali"] / A["gsc_marka"]["toplam_sorgu"]), bin(A["gsc_top_sorgu"][0][1]), yzd(100 * GS["Markasız · Ürün"][0] / gtot), yzd(100 * GS["Markasız · Fiyat"][0] / gtot), yzd(100 * GS["Markasız · Tasarım"][0] / gtot), bin(GS["Markasız · Tamir ve bakım"][0]), k(GS["Markasız · Tamir ve bakım"][1]), yzd(100 * GS["Markasız · Tamir ve bakım"][0] / GS["Markasız · Tamir ve bakım"][1])), "D2"),
 kaynak("Google Ads Keyword Planner (ihtiyaç sınıfları, Oca-Ağu 2025 ve 2026) · Google Search Console, sc-domain:vitra.com.tr, 1 Haz 2025 - 25 Eyl 2026, ilk 25.000 sorgu",
        "Google Ads Keyword Planner (need classes, Jan-Aug 2025 and 2026) · Google Search Console, sc-domain:vitra.com.tr, 1 Jun 2025 - 25 Sep 2026, top 25,000 queries", "D1", "D2"),
)
