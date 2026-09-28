# -*- coding: utf-8 -*-
"""Bolum: Sonraki adimlar (oncelik tablosu). Excel ile ortak kaynak."""
from ortak import *
ADIMLAR = [
 ("Öncelik 1", ("Ürün sayfasında fiyat, taksit tablosu ve teslim aralığının birlikte gösterilmesi", "Showing price, instalment table and delivery window together on the product page"),
  ("\"vitra taksit seçenekleri\", \"vitra 9 taksit\" aramaları; hacimli üründe ilk belirsizlik fiyat ve teslim", "Searches for \"vitra taksit seçenekleri\", \"vitra 9 taksit\"; the first uncertainty for a bulky product is price and delivery"),
  ("Karar öncesi belirsizliğin azaltılması", "Reducing pre-decision uncertainty"), ("D3",)),
 ("Öncelik 1", ("Yedek parça sayfasının ürün koduna göre kurulması ve montaj videosuyla birleştirilmesi", "Building the spare-part page by product code and combining it with the installation video"),
  ("Tamir aramaları aylık %s; autocomplete önerilerinin %s'i tamir temasında; tamir aramalarında VitrA videosu yok" % (k(A["niyet"]["Tamir ve bakım"]["a26"]), yzd(100 * A["auto_tema"]["Tamir ve bakım"] / sum(A["auto_tema"].values()))), "Repair searches %s per month; %s of autocomplete suggestions are in the repair theme; no VitrA video in repair searches" % (k(A["niyet"]["Tamir ve bakım"]["a26"]), yzd(100 * A["auto_tema"]["Tamir ve bakım"] / sum(A["auto_tema"].values())).replace("%", "") + "%")),
  ("Mevcut müşteriden tekrar satış ve sadakat", "Repeat sales and loyalty from existing customers"), ("D1", "D3", "D4")),
 ("Öncelik 1", ("Sepette montaj hizmeti seçeneğinin sabit ücretle tanımlanması", "Defining an installation service option with a fixed fee in the basket"),
  ("\"klozet montaj ücreti\", \"klozet taktırma fiyatı\", \"klozet montaj aparatı koçtaş\" önerileri", "Suggestions for \"klozet montaj ücreti\", \"klozet taktırma fiyatı\", \"klozet montaj aparatı koçtaş\""),
  ("Ürün + hizmet paketiyle kanal farklılaşması", "Channel differentiation through product + service bundles"), ("D3",)),
 ("Öncelik 1", ("Geri arama ve keşif formunun mobilya, duşakabin ve küvet sayfalarına eklenmesi; lead olaylarının GA4'te tanımlanması", "Adding call-back and site survey forms to furniture, shower enclosure and bathtub pages; defining lead events in GA4"),
  ("Banyo Mobilyaları talebin %s'ini oluştururken organik tıkın %s'ini almakta" % (yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]), yzd(100 * sum(v[0] for kk, v in A["gsc_kat"].items() if kk.startswith("Banyo Mobilyaları")) / sum(v[0] for v in A["gsc_kat"].values()))), "Bathroom Furniture makes up %s of demand but takes %s of organic clicks" % (yzd(100 * A["k1"]["Banyo Mobilyaları"]["a26"] / A["toplam"]["a26"]).replace("%", "") + "%", yzd(100 * sum(v[0] for kk, v in A["gsc_kat"].items() if kk.startswith("Banyo Mobilyaları")) / sum(v[0] for v in A["gsc_kat"].values())).replace("%", "") + "%")),
  ("Düşük dönüşümlü hacimli üründe ölçülebilir lead", "Measurable leads for low-conversion bulky products"), ("D1", "D2")),
 ("Öncelik 1", ("Kanal rollerinin belirlenmesi: pazaryerinde hızlı karar ürünleri, marka sitesinde set, yedek parça ve hizmet; fiyat tutarlılığı", "Setting channel roles: quick-decision products on marketplaces, sets, spare parts and services on the brand site; price consistency"),
  ("Trendyol ve Hepsiburada organik ölçeği marka sitesinin yüzlerce katı; aynı ürün aynı fiyatla üç kanalda", "Trendyol and Hepsiburada organic scale is hundreds of times the brand site; the same product at the same price on three channels"),
  ("Kanal başına net değer önerisi", "A clear value proposition per channel"), ("D5",)),
 ("Öncelik 2", ("YouTube tamir serisinin üretilmesi ve tesisatçı kanallarıyla iş birliği", "Producing a YouTube repair series and collaborating with installer channels"),
  ("Altı tamir aramasının ilk sayfaları toplam %s izlenme; Macit Tesisat videosu %s" % (k(sum(A["yt"][q]["toplam_g"] for q in ["gömme rezervuar tamiri", "rezervuar su kaçırıyor", "klozet su kaçırıyor", "klozet tıkanıklığı nasıl açılır", "vitra gömme klozet su kaçırıyor", "vitra rezervuar tamiri"])), k(A["yt"]["vitra gömme klozet su kaçırıyor"]["top"][0][2])), "First pages of six repair searches total %s views; the Macit Tesisat video %s" % (k(sum(A["yt"][q]["toplam_g"] for q in ["gömme rezervuar tamiri", "rezervuar su kaçırıyor", "klozet su kaçırıyor", "klozet tıkanıklığı nasıl açılır", "vitra gömme klozet su kaçırıyor", "vitra rezervuar tamiri"])), k(A["yt"]["vitra gömme klozet su kaçırıyor"]["top"][0][2]))),
  ("Tamir anında marka görünürlüğü ve yedek parça satışı", "Brand visibility at the moment of repair and spare-part sales"), ("D4", "Y1")),
 ("Öncelik 2", ("Klozet ve rezervuar sepetine tamamlayıcı ürün önerisinin eklenmesi; üçüncü taraf satıcı modelinin montaj malzemesinde test edilmesi", "Adding complementary product suggestions to the WC and cistern basket; testing the third-party seller model in fitting materials"),
  ("\"klozet montaj aparatı\", \"klozet bağlantı borusu\", \"taharet musluğu\" aramaları; sepet yapı markette tamamlanmakta", "Searches for \"klozet montaj aparatı\", \"klozet bağlantı borusu\", \"taharet musluğu\"; the basket is completed at DIY stores"),
  ("Sepet bütünlüğü ve tek durak konumu", "Basket integrity and one-stop position"), ("D3",)),
 ("Öncelik 2", ("Kategori sayfası şablonunun kategoriye göre ayrıştırılması: klozet ve rezervuarda fiyat, teslimat, yedek parça; mobilya ve karoda görsel, ölçü, kombinasyon", "Differentiating the category page template by category: price, delivery, spare parts for WC and cistern; visuals, dimensions, combinations for furniture and tiles"),
  ("Fiyat aramaları Vitrifiyelerde, tasarım aramaları Mobilya ve Karoda yoğunlaşmakta", "Price searches concentrate in Sanitaryware, design searches in Furniture and Tiles"),
  ("Kategoriye özgü dönüşüm", "Category-specific conversion"), ("D1", "D2")),
 ("Öncelik 2", ("Servis sayfasında ücret, randevu ve en yakın servis bilgisinin açıkça verilmesi", "Giving fee, appointment and nearest service information clearly on the service page"),
  ("\"vitra servis ücreti\", \"vitra servis randevu\", \"vitra servis en yakın\" önerileri", "Suggestions for \"vitra servis ücreti\", \"vitra servis randevu\", \"vitra servis en yakın\""),
  ("Servis belirsizliğinin azaltılması", "Reducing service uncertainty"), ("D3",)),
 ("Öncelik 3", ("Yenileme paketi: banyo mobilyası + lavabo + batarya + ayna seti; keşif ve montaj dahil tek fiyat", "Renovation package: bathroom furniture + washbasin + tap + mirror set; single price including survey and installation"),
  ("Mobilya talebi %s daralırken tasarım ve model aramaları %s büyümekte; ertelenen talep 2026 Q4'te geri gelebilir" % (yz(A["k1"]["Banyo Mobilyaları"]["yoy"]), yz(A["niyet"]["Tasarım ve fikir"]["yoy"])), "Furniture demand contracts %s while design and model searches grow %s; postponed demand may return in 2026 Q4" % (yz(A["k1"]["Banyo Mobilyaları"]["yoy"]), yz(A["niyet"]["Tasarım ve fikir"]["yoy"]))),
  ("Talep geri geldiğinde hazır teklif", "A ready offer when demand returns"), ("D1", "D7")),
 ("Öncelik 3", ("Satın alan müşteriye 5 yıl sonra yenileme ve yedek parça hatırlatması; olumsuz deneyim sonrası tekrar sipariş oranının izlenmesi", "Renewal and spare-part reminder to buyers five years later; tracking the repeat-order rate after a poor experience"),
  ("Konut satışları ve tamirat niyeti yükselmekte; mevcut müşteri tabanı yenileme adayı", "House sales and repair intent are rising; the existing customer base is a renewal candidate"),
  ("Yaşam boyu değer", "Lifetime value"), ("D7", "D8")),
]
OC = {"Öncelik 1": "b-o1", "Öncelik 2": "b-o2", "Öncelik 3": "b-o3"}; OE = {"Öncelik 1": "Priority 1", "Öncelik 2": "Priority 2", "Öncelik 3": "Priority 3"}
rows = [['<span class="badge %s">%s</span>' % (OC[o], x(o, OE[o])), "<b>%s</b>" % x(*a), x(*d) + R(*kod), x(*e)] for o, a, d, e, kod in ADIMLAR]
HTML = """
<p class="lede">%s</p>
%s
%s
""" % (
 x("Aksiyonlar üç öncelik kademesinde verilmiştir; sıralama VitrA ekibinin stratejik tercihleri ve panel verisiyle güncellenebilir. Öncelik 1 maddeleri mevcut trafik ve talep üzerinde kısa vadede etki üretebilecek düzenlemelerdir.",
   "Actions are given in three priority tiers; the order can be updated with the VitrA team's strategic preferences and panel data. Priority 1 items are adjustments that can produce a short-term effect on existing traffic and demand."),
 tablo([th("Öncelik", "Priority", "Etki ve uygulanabilirlik birlikte değerlendirilerek verilen sıra.", "Order given by assessing impact and feasibility together."),
        th("Aksiyon", "Action", "Önerilen düzenleme.", "Proposed adjustment."),
        th("Dayanak", "Basis", "Öneriyi destekleyen bulgu ve kaynak.", "Finding and source supporting the proposal."),
        th("Beklenen etki", "Expected effect", "Düzenlemenin hedeflediği sonuç.", "The outcome the adjustment targets.")], rows),
 insight("Bu sunumdan sonra ilk adım olarak üç nokta değerlendirilebilir: (1) ürün sayfasında fiyat, taksit ve teslim aralığının birlikte gösterilmesi, (2) yedek parça sayfasının kurulması ve tamir videolarıyla birleştirilmesi, (3) pazaryeri ve GA4 verisinin gelmesiyle kanal rollerinin ürün grubu bazında netleştirilmesi.",
         "Three points can be considered as the first step after this presentation: (1) showing price, instalment and delivery window together on the product page, (2) building the spare-part page and combining it with repair videos, (3) clarifying channel roles by product group once marketplace and GA4 data arrive."),
)
