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
KPI = "".join([
 kpi_kart(yz(toplam_yoy), "Kategori arama talebi · Oca-Ağu 2026 / 2025, 2.420 kelime", "Category search demand · Jan-Aug 2026 / 2025, 2,420 keywords", "dn"),
 kpi_kart(yz(kloz), "Klozetler · tek büyüyen büyük alt kategori", "WCs · the only growing large sub-category", "up"),
 kpi_kart(k(son12), "Organik tık · Eyl 2025 - Ağu 2026, vitra.com.tr", "Organic clicks · Sep 2025 - Aug 2026, vitra.com.tr"),
 kpi_kart(yzd(tam_pay), "Autocomplete önerilerinde tamir ve yedek parça payı", "Share of repair and spare-part themes in autocomplete suggestions", "hi"),
])
KRITIK = marks([
 ("at", "Talep daralması makro kaynaklıdır: reel kart harcaması yatay, güven ve tamirat niyeti yükselmekte; ertelenen yenileme talebi 2026 Q4 - 2027 Q1'de geri gelebilir", "The demand contraction is macro-driven: real card spending is flat while confidence and repair intent are rising; postponed renovation demand may return in 2026 Q4 - 2027 Q1"),
 ("at", "Banyo Mobilyaları talebin %s'ini oluştururken organik tıkın %s'ini almaktadır; en büyük açık bu kategoridedir" % (yzd(bm_talep), yzd(bm_tik)), "Bathroom Furniture makes up %s of demand but takes %s of organic clicks; the widest gap is in this category" % (yzd(bm_talep).replace("%", "") + "%", yzd(bm_tik).replace("%", "") + "%")),
 ("at", "Tamir, yedek parça ve montaj ihtiyacı markadan bağımsız kategori davranışıdır; VitrA bu aramalarda YouTube'da görünmemekte, sitede bu sorgular %s CTR ile kalmaktadır" % yzd(100 * GS["Markasız · Tamir ve bakım"][0] / GS["Markasız · Tamir ve bakım"][1]), "The repair, spare-part and installation need is a category behaviour independent of brand; VitrA is absent from these searches on YouTube and these queries stay at %s CTR on the site" % (yzd(100 * GS["Markasız · Tamir ve bakım"][0] / GS["Markasız · Tamir ve bakım"][1]).replace("%", "") + "%")),
 ("up", "vitra.com.tr marka siteleri arasında organik lider (%s tahmini aylık ziyaret); kategori aramalarında asıl rakip Koçtaş (%s) ve pazaryerleridir" % (k(vit[4]), k(koc[4])), "vitra.com.tr is the organic leader among brand sites (%s estimated monthly visits); the real competitors in category searches are Koçtaş (%s) and the marketplaces" % (k(vit[4]), k(koc[4]))),
 ("up", "Kanal farklılaşması fiyatla değil set, yedek parça, montaj hizmeti ve danışmanlıkla kurulabilir; tamamlayıcı ürünlerde üçüncü taraf satıcı modeli test edilebilir", "Channel differentiation can be built not on price but on sets, spare parts, installation service and consultation; a third-party seller model can be tested for complementary products"),
])
FN = '<div class="fnotes">%s</div>' % "".join([
 fnote(1, "Talep daralıyor, klozet direniyor", "Demand contracts, the WC resists",
       [("2.420 kelimenin talebi Oca-Ağu 2026'da <b>%s</b>; sekiz kategorinin tamamı yatay veya negatif" % yz(toplam_yoy), "Demand for 2,420 keywords <b>%s</b> in Jan-Aug 2026; all eight categories flat or negative" % yz(toplam_yoy)),
        ("Klozetler <b>%s</b>, Banyo Karoları <b>%s</b>; Lavabo Dolapları <b>%s</b>, Banyo Aynaları <b>%s</b>" % (yz(kloz), yz(A["k2"]["Karo Seramik Ürünleri|Banyo Karo Seramikleri"]["yoy"]), yz(A["k2"]["Banyo Mobilyaları|Lavabo Dolapları"]["yoy"]), yz(A["k2"]["Banyo Mobilyaları|Banyo Aynaları"]["yoy"])), "WCs <b>%s</b>, Bathroom Tiles <b>%s</b>; Washbasin Units <b>%s</b>, Bathroom Mirrors <b>%s</b>" % (yz(kloz), yz(A["k2"]["Karo Seramik Ürünleri|Banyo Karo Seramikleri"]["yoy"]), yz(A["k2"]["Banyo Mobilyaları|Lavabo Dolapları"]["yoy"]), yz(A["k2"]["Banyo Mobilyaları|Banyo Aynaları"]["yoy"]))),
        ("Tasarım ve model aramaları tek büyüyen ihtiyaç sınıfı: <b>%s</b>" % yz(NI["Tasarım ve fikir"]["yoy"]), "Design and model searches are the only growing need class: <b>%s</b>" % yz(NI["Tasarım ve fikir"]["yoy"]))]),
 fnote(2, "Makro ortam: harcama nominal, niyet yükselişte", "Macro environment: nominal spending, rising intent",
       [("Mobilya ve dekorasyon kart harcaması <b>%s</b> nominal; reel kartlı ödeme endeksi <b>%s</b>" % (yz(A["kart"]["mobilya_dekorasyon"]["yoy"]), yz((sum(A["koe"]["2026-%d" % m]["genel_reel"] for m in range(1, 8)) / sum(A["koe"]["2025-%d" % m]["genel_reel"] for m in range(1, 8)) - 1) * 100)), "Furniture and decoration card spending <b>%s</b> nominal; real card payment index <b>%s</b>" % (yz(A["kart"]["mobilya_dekorasyon"]["yoy"]), yz((sum(A["koe"]["2026-%d" % m]["genel_reel"] for m in range(1, 8)) / sum(A["koe"]["2025-%d" % m]["genel_reel"] for m in range(1, 8)) - 1) * 100))),
        ("Tüketici güven endeksi Eylül 2026'da <b>%s</b>, son iki yılın en yükseği; konut tamiratına harcama ihtimali <b>%s</b>" % (("%.1f" % A["tuketici"]["2026-9"]["guven_endeksi"]).replace(".", ","), ("%.1f" % A["tuketici"]["2026-9"]["konut_tamirat_harcama_ihtimali"]).replace(".", ",")), "Consumer confidence index <b>%s</b> in September 2026, the highest in two years; probability of spending on home repairs <b>%s</b>" % ("%.1f" % A["tuketici"]["2026-9"]["guven_endeksi"], "%.1f" % A["tuketici"]["2026-9"]["konut_tamirat_harcama_ihtimali"])),
        ("Konut satışları Oca-Ağu 2026 <b>%s</b>; her el değiştiren konut yenileme adayı" % yz((sum(A["konut"]["2026-%d" % m]["toplam"] for m in range(1, 9)) / sum(A["konut"]["2025-%d" % m]["toplam"] for m in range(1, 9)) - 1) * 100), "House sales Jan-Aug 2026 <b>%s</b>; every home changing hands is a renovation candidate" % yz((sum(A["konut"]["2026-%d" % m]["toplam"] for m in range(1, 9)) / sum(A["konut"]["2025-%d" % m]["toplam"] for m in range(1, 9)) - 1) * 100))]),
 fnote(3, "Organik kanal: kategori sayfaları taşıyor", "Organic channel: category pages carry the load",
       [("Organik tıkların <b>%s</b>'i kategori sayfalarına; ürün sayfaları <b>%s</b>" % (yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot)), "<b>%s</b> of organic clicks land on category pages; product pages <b>%s</b>" % (yzd(100 * GT["kategori"][0] / ttot).replace("%", "") + "%", yzd(100 * GT["urun"][0] / ttot).replace("%", "") + "%")),
        ("Tıkların <b>%s</b>'i markalı sorgudan; \"vitra\" tek başına <b>%s</b> tık" % (yzd(100 * A["gsc_marka"]["markali"] / A["gsc_marka"]["toplam_sorgu"]), k(A["gsc_top_sorgu"][0][1])), "<b>%s</b> of clicks come from branded queries; \"vitra\" alone <b>%s</b> clicks" % (yzd(100 * A["gsc_marka"]["markali"] / A["gsc_marka"]["toplam_sorgu"]).replace("%", "") + "%", k(A["gsc_top_sorgu"][0][1]))),
        ("Aralık 2025 alan adı taşınması sonrası trafik korunmuş; Haz-Tem 2026'da taşınma öncesi seviye", "Traffic preserved after the December 2025 domain migration; pre-migration level reached in Jun-Jul 2026")]),
 fnote(4, "Kullanıcı VitrA'dan yedek parça ve montaj bekliyor", "The user expects spare parts and installation from VitrA",
       [("Autocomplete önerilerinin <b>%s</b>'i tamir ve yedek parça, <b>%s</b>'i montaj temasında" % (yzd(tam_pay), yzd(100 * AT["Montaj"] / sum(AT.values()))), "<b>%s</b> of autocomplete suggestions are in the repair and spare-part theme, <b>%s</b> in installation" % (yzd(tam_pay).replace("%", "") + "%", yzd(100 * AT["Montaj"] / sum(AT.values())).replace("%", "") + "%")),
        ("\"vitra taksit seçenekleri\", \"vitra 9 taksit\", \"vitra servis ücreti\", \"klozet montaj ücreti\" aranıyor", "\"vitra taksit seçenekleri\", \"vitra 9 taksit\", \"vitra servis ücreti\", \"klozet montaj ücreti\" are being searched"),
        ("YouTube tamir aramalarında VitrA videosu yok; Macit Tesisat'ın VitrA tamir videosu <b>%s</b> izlenme" % k(A["yt"]["vitra gömme klozet su kaçırıyor"]["top"][0][2]), "No VitrA video in YouTube repair searches; Macit Tesisat's VitrA repair video <b>%s</b> views" % k(A["yt"]["vitra gömme klozet su kaçırıyor"]["top"][0][2]))]),
 fnote(5, "Rekabet: pazaryeri ve yapı market ölçeği", "Competition: marketplace and DIY scale",
       [("Koçtaş VitrA kelimelerinin <b>%s</b>'inde birlikte sıralanıyor; organik trafiği VitrA'nın <b>%s</b> katı" % (yzd(100 * veri.AHREFS["ahrefs_organik_rakipler_tr"][0][1] / vit[2]), ("%.1f" % (koc[4] / vit[4])).replace(".", ",")), "Koçtaş ranks alongside VitrA for <b>%s</b> of its keywords; its organic traffic is <b>%s</b> times VitrA's" % (yzd(100 * veri.AHREFS["ahrefs_organik_rakipler_tr"][0][1] / vit[2]).replace("%", "") + "%", "%.1f" % (koc[4] / vit[4]))),
        ("Marka siteleri içinde VitrA lider: <b>%s</b> tahmini organik ziyaret; Kale <b>%s</b>, Creavit <b>%s</b>" % (k(vit[4]), k(next(b[4] for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "kale.com.tr")), k(next(b[4] for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "creavit.com.tr"))), "VitrA leads among brand sites: <b>%s</b> estimated organic visits; Kale <b>%s</b>, Creavit <b>%s</b>" % (k(vit[4]), k(next(b[4] for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "kale.com.tr")), k(next(b[4] for b in veri.AHREFS["ahrefs_batch_tr"] if b[0] == "creavit.com.tr")))),
        ("Bauhaus paid trafiği organik trafiğini aşıyor; VitrA'da paid, organiğin <b>%s</b>'i" % yzd(100 * vit[5] / vit[4]), "Bauhaus paid traffic exceeds its organic; at VitrA paid is <b>%s</b> of organic" % (yzd(100 * vit[5] / vit[4]).replace("%", "") + "%"))]),
 fnote(6, "Model: kanal rolü ve etkileşim", "Model: channel role and engagement",
       [("Pazaryerinde hızlı karar ürünleri ve kampanya; marka sitesinde set, yedek parça, montaj ve danışmanlık", "Quick-decision products and campaigns on marketplaces; sets, spare parts, installation and consultation on the brand site"),
        ("Hacimli üründe geri arama, keşif, lokal bayi stoğu ve montaj seçeneği; lead olayları GA4'te tanımlanmalı", "Call-back, site survey, local dealer stock and installation option for bulky products; lead events to be defined in GA4"),
        ("VitrA'nın üretmediği tamamlayıcı ürünlerde üçüncü taraf satıcı modeli montaj malzemesinde test edilebilir", "A third-party seller model for complementary products VitrA does not make can be tested in fitting materials")]),
])
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s</div>
%s
<h3>%s</h3>
%s
""" % (
 x("VitrA e-ticaret büyüme fırsatları çalışmasının ilk sürümüdür. Pazar talebi, kullanıcı ihtiyaç dili, organik kanal performansı, YouTube, rekabet ve makro ortam Inbound erişimindeki kaynaklarla incelenmiş; kanal rolleri ve etkileşim modeli için öneri çerçevesi kurulmuştur. VitrA'dan beklenen pazaryeri, GA4 ve müşteri verisiyle rapor genişletilecektir.",
   "This is the first version of the VitrA e-commerce growth opportunities study. Market demand, user need language, organic channel performance, YouTube, competition and the macro environment were examined with the sources available to Inbound; a proposal framework for channel roles and the engagement model was set up. The report will be extended with the marketplace, GA4 and customer data expected from VitrA."),
 KPI,
 box("KRİTİK TESPİT", "KEY FINDINGS", KRITIK),
 x("Öne çıkan bulgular", "Highlights"), FN,
)
