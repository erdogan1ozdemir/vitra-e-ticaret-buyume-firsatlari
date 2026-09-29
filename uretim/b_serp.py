# -*- coding: utf-8 -*-
"""Bolum: Google arama sonuclari (SERP) ve AI Overview."""
from ortak import *
DOM = [("trendyol.com", 86, 68, "2,3", "14 / 14 / 12 / 21"), ("koctas.com.tr", 65, 30, "4,2", "9 / 13 / 8 / 15"), ("vitra.com.tr", 54, 35, "3,1", "14 / 11 / 5 / 3"), ("hepsiburada.com", 54, 16, "5,2", "8 / 11 / 8 / 18"),
       ("akakce.com", 40, 11, "5,7", "10 / 3 / 10 / 10"), ("creavit.com.tr", 35, 10, "4,8", "13 / 9 / 4 / 1"), ("pinterest.com", 28, 7, "5,3", "1 / 11 / - / 4"), ("banyomarka.com", 22, 10, "4,6", "5 / - / 4 / 1"),
       ("instagram.com", 22, 3, "7,7", "2 / 1 / 3 / 7"), ("youtube.com", 21, 5, "6,2", "3 / - / 5 / 3"), ("cimri.com", 19, 1, "7,1", "5 / - / 4 / 4"), ("kale.com.tr", 18, 6, "5,8", "7 / 2 / 2 / 1"),
       ("ikea.com.tr", 18, 5, "6,3", "1 / 8 / 2 / 3"), ("amazon.com.tr", 17, 5, "5,2", "1 / 2 / 3 / 8"), ("bauhaus.com.tr", 17, 1, "6,4", "6 / 4 / 4 / 2")]
T_DOM = tablo([th("Alan adı", "Domain", "Google TR mobil ilk 10 organik sonuçta görünen alan adı.", "Domain appearing in Google TR mobile top 10 organic results."),
               th("İlk 10 (kelime)", "Top 10 (keywords)", "109 kelimeden kaçında ilk 10'da.", "In how many of 109 keywords it is in the top 10.", True),
               th("İlk 3 (kelime)", "Top 3 (keywords)", "Kaç kelimede ilk 3'te.", "In how many keywords it is in the top 3.", True),
               th("Ort. sıra", "Avg. position", "Görüldüğü kelimelerdeki en iyi sıranın ortalaması.", "Average of the best position in the keywords where it appears.", True),
               th("SSG / BM / Armatür / Bitişik", "SSG / BM / Taps / Adjacent", "Tema bazında ilk 10'da görüldüğü kelime sayısı (tema büyüklükleri 16 / 15 / 13 / 24).", "Number of keywords in the top 10 by theme (theme sizes 16 / 15 / 13 / 24).", True)],
              [[veri_m(a), cell(b), cell(c), n(d), n(e)] for a, b, c, d, e in DOM])
VT = [("SSG", "SSG", 16, 12, 14, 2), ("BM", "BM", 15, 6, 11, 4), ("Armatür ve duş", "Taps and showers", 13, 3, 5, 8), ("Yıkanma", "Bathing areas", 6, 3, 5, 1), ("Bitişik ürünler", "Adjacent products", 24, 0, 3, 21),
      ("Hizmet ve ilham", "Services and inspiration", 14, 1, 4, 10), ("Karo", "Tiles", 5, 1, 3, 2), ("Soru ve karar", "Questions and decisions", 7, 5, 5, 1), ("Marka", "Brand", 9, 4, 4, 5)]
T_VT = tablo([th("Tema", "Theme", "Kelime grubu.", "Keyword group."), th("Kelime", "Keywords", "Temadaki kelime sayısı.", "Number of keywords in the theme.", True),
              th("VitrA ilk 3", "VitrA top 3", "vitra.com.tr'nin ilk 3'te olduğu kelime sayısı.", "Number of keywords where vitra.com.tr is in the top 3.", True),
              th("VitrA ilk 10", "VitrA top 10", "İlk 10'da olduğu kelime sayısı.", "Number of keywords in the top 10.", True),
              th("İlk 20'de yok", "Not in top 20", "vitra.com.tr'nin ilk 20'de görünmediği kelime sayısı.", "Number of keywords where vitra.com.tr is not in the top 20.", True)],
             [[x(a, b), cell(c), cell(d), cell(e), cell(f)] for a, b, c, d, e, f in VT])
BOS = [("su arıtma cihazı", 73458, "trendyol.com"), ("termosifon", 61500, "trendyol.com"), ("banyo bataryası", 39267, "trendyol.com"), ("taharet musluğu", 37417, "akakce.com"), ("tesisatçı", 36800, "armut.com"), ("şofben", 36075, "trendyol.com"),
       ("jakuzi", 28967, "jakuzicenter.com"), ("banyo paspası", 26717, "trendyol.com"), ("dolap kulpu", 24242, "trendyol.com"), ("mutfak tezgahı", 24242, "koctas.com.tr"), ("lavabo bataryası", 23833, "trendyol.com"), ("fayans fiyatları", 23425, "koctas.com.tr"),
       ("banyo seti", 23017, "trendyol.com"), ("çamaşır sepeti", 21308, "trendyol.com"), ("evye", 18783, "trendyol.com"), ("havlupan", 16642, "trendyol.com"), ("derz dolgu", 14675, "trendyol.com"), ("banyo rafı", 10708, "trendyol.com"),
       ("gömme rezervuar iç takımı", 4650, "akakce.com"), ("granit evye", 4667, "ankastredunyasi.com"), ("klozet kapağı menteşesi", 4483, "trendyol.com"), ("geberit gömme rezervuar", 3933, "trendyol.com"), ("creavit klozet", 3800, "creavit.com.tr"), ("kanalsız klozet", 2025, "bauhaus.com.tr")]
T_BOS = tablo([th("Arama kelimesi", "Search keyword", "vitra.com.tr'nin ilk 20'de görünmediği kelime.", "Keyword where vitra.com.tr does not appear in the top 20."),
               th("Aylık hacim", "Monthly volume", "Keyword Planner 12 aylık ortalama.", "Keyword Planner 12-month average.", True),
               th("SERP lideri", "SERP leader", "Organik 1. sıradaki alan adı.", "Domain in organic position 1.")], [[veri_m(a), cell(b), veri_m(c)] for a, b, c in BOS], "uzun")
OZ = [("AI Overview", "AI Overview", "31 (%28)", "5 / 3 / 2 / 8", "Soru 5/7, karo 3/5", "Questions 5/7, tiles 3/5"), ("People Also Ask", "People Also Ask", "84 (%77)", "12 / 6 / 9 / 21", "Yıkanma, karo, soru, marka %100", "Bathing, tiles, questions, brand 100%"),
      ("Video / Shorts", "Video / Shorts", "40 (%37)", "7 / 6 / 3 / 7", "Hizmet %71, soru %71", "Services 71%, questions 71%"), ("Local pack", "Local pack", "42 (%39)", "5 / 7 / 3 / 7", "Yıkanma %83, marka %67", "Bathing 83%, brand 67%"),
      ("Yer siteleri (Sahibinden, Armut)", "Place sites (Sahibinden, Armut)", "12 (%11)", "0 / 5 / 0 / 3", "Banyo dolabı, duşakabin, tesisatçı", "Bathroom cabinet, shower enclosure, plumber"), ("Shopping / ürün listeleme", "Shopping / product listings", "0", "0 / 0 / 0 / 0", "Hiçbir kelimede dönmedi", "Returned for no keyword")]
T_OZ = tablo([th("SERP özelliği", "SERP feature", "Arama sonuç sayfasında organik sonuç dışındaki blok.", "Block on the results page other than organic results."),
              th("Kelime (pay)", "Keywords (share)", "109 kelimeden kaçında görüldüğü.", "In how many of 109 keywords it appeared.", True),
              th("SSG / BM / Armatür / Bitişik", "SSG / BM / Taps / Adjacent", "Tema bazında görüldüğü kelime sayısı.", "Keywords by theme where it appeared.", True),
              th("En yoğun olduğu temalar", "Themes where most frequent", "En yüksek görülme oranı.", "Highest occurrence rate.")], [[x(a, b), n(c), n(d), x(e, f)] for a, b, c, d, e, f in OZ])
AI = [("trendyol.com", 14), ("koctas.com.tr", 9), ("vitra.com.tr", 7), ("hepsiburada.com", 7), ("banyomarka.com", 6), ("creavit.com.tr", 6), ("kale.com.tr", 5), ("banyome.com", 5), ("yapilir.com", 4), ("cimri.com", 4)]
RANK_AI = rank_list([(veri_m(a), b) for a, b in AI], 14, you=lambda e: "vitra" in e, fmt=lambda v: bin(v))
PAA = [("Fiyat", "Price", ["Klozet yaptırmak kaç TL?", "Klozet iç takım değişimi ne kadar?", "Banyo dolabı fiyatları ne kadar?", "Bir banyo tadilatı ne kadara mal olur?", "Arıtma taktırmak kaç TL?"]),
       ("Ölçü ve seçim", "Size and selection", ["Klozet kapakları standart mı?", "Banyo dolabı yüksekliği kaç santim olmalı?", "Kanallı klozet mi iyi kanalsız mı?", "Gömme rezervuar mantıklı mı?", "MDF banyo dolabı suya dayanıklı mı?"]),
       ("Montaj ve tamir", "Installation and repair", ["Klozet montajı kaç TL?", "Klozet değişimini kim yapar?", "Klozet suyu neden durmuyor?", "Taharet musluğu değişimi kaç TL?", "Banyo fayansları kırılmadan nasıl yenilenir?"]),
       ("VitrA ve marka", "VitrA and brand", ["VitrA iyi marka mı?", "VitrA ve Artema aynı marka mı?", "VitrA gömme rezervuar neden su doldurmuyor?", "Bataryada E.C.A. mı Artema mı?", "Artema hangi ülkenin markası?"])]
PAA_H = '<div class="fnotes">%s</div>' % "".join('<article class="fnote"><span class="fc">%s</span><ul>%s</ul></article>' % (x(a, b), "".join("<li>%s</li>" % veri_m(q) for q in qs)) for a, b, qs in PAA)
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
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
<h3>%s</h3>
<div class="split"><div>%s</div>%s</div>
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Kategori, ürün, bitişik ürün, hizmet, soru ve marka kelimelerinden oluşan 109 kelime için Google Türkiye mobil arama sonuçlarının ilk 20 organik sonucu ve SERP özellikleri incelenmiştir. Sonuçlar 29 Eylül 2026 tarihli tek gözlemdir; 19 kelimede ilk çekim eksik sonuç döndürdüğü için bu kelimeler yeniden çekilmiştir.",
   "For 109 keywords made up of category, product, adjacent product, service, question and brand terms, the top 20 organic results and SERP features of Google Turkey mobile results were examined. The results are a single observation dated 29 September 2026; 19 keywords returned incomplete results on the first pull and were re-pulled."),
 kpi_kart("%79", "Trendyol'un ilk 10'da olduğu kelime payı · 48 kelimede 1. sıra", "Share of keywords with Trendyol in the top 10 · first place in 48 keywords", "hi"),
 kpi_kart("%41", "Pazaryeri ve perakendecilerin ilk 3 sıralardaki payı (327 yuvanın 134'ü)", "Share of top-3 slots held by marketplaces and retailers (134 of 327 slots)"),
 kpi_kart("54 / 109", "VitrA'nın ilk 10'da olduğu kelime · 19 kelimede 1. sıra", "Keywords with VitrA in the top 10 · first place in 19", "up"),
 kpi_kart("7 / 24", "VitrA'nın referans verildiği AI Overview (içeriği alınan 24 blok)", "AI Overviews citing VitrA (of 24 blocks with content)"),
 x("Kim sıralanıyor?", "Who ranks?"),
 T_DOM,
 insight("Arama sonuçlarında pazaryerleri ve perakendeciler belirleyicidir: Trendyol 109 kelimenin 86'sında ilk 10'da ve 48'inde 1. sıradadır; Koçtaş, Hepsiburada ve Akakçe onu izlemektedir. Banyo mobilyası, armatür ve bitişik ürün kelimelerinin %92-93'ünde en az bir pazaryeri veya perakendeci ilk 3'tedir. İlk 10 sonuçların %49'u kategori, %26'sı pazaryeri arama ve liste sayfasıdır; ürün sayfalarının payı %3'ün altındadır. Hizmet ve soru kelimelerinde ise tablo değişmekte; Armut, Pinterest, YouTube ve rehber içerikleri öne çıkmaktadır.",
         "Marketplaces and retailers are decisive in search results: Trendyol is in the top 10 for 86 of 109 keywords and first for 48; Koçtaş, Hepsiburada and Akakçe follow. In 92-93% of bathroom furniture, tap and adjacent product keywords at least one marketplace or retailer is in the top 3. 49% of top-10 results are category pages and 26% marketplace search and listing pages; product pages are under 3%. For service and question keywords the picture changes, with Armut, Pinterest, YouTube and guide content coming to the fore.", "D19"),
 x("VitrA nerede?", "Where is VitrA?"),
 T_VT,
 insight("VitrA SSG'de güçlüdür: 16 kelimenin 12'sinde ilk 3'te; klozet, asma klozet, akıllı klozet, lavabo, bide ve lavabo dolabında 1. sıradadır. Sıralanan 55 sonucun 53'ü kategori sayfasıdır. Boşluk bitişik ürünlerde (24 kelimenin 21'i), armatürde (13'ün 8'i: banyo bataryası, lavabo bataryası, taharet musluğu, robot duş seti, sifon dahil) ve hizmette (14'ün 10'u) yoğunlaşmaktadır. artema.com.tr ilk 10'da yalnızca 3 kelimede görünmekte; armatür aramalarında VitrA grubunun ağırlığı sınırlı kalmaktadır. Rakip marka kelimelerinde (kale klozet, creavit klozet, geberit gömme rezervuar, grohe batarya) VitrA ilk 20'de yer almamaktadır.",
         "VitrA is strong in SSG: in the top 3 for 12 of 16 keywords and first for WC, wall-hung WC, smart WC, washbasin, bidet and basin unit. 53 of the 55 ranking results are category pages. The gap concentrates in adjacent products (21 of 24 keywords), taps (8 of 13: including bath tap, basin tap, bidet valve, rain shower set and siphon) and services (10 of 14). artema.com.tr appears in the top 10 for only 3 keywords; the VitrA group's weight in tap searches remains limited. For competitor brand keywords (kale klozet, creavit klozet, geberit gömme rezervuar, grohe batarya) VitrA is not in the top 20.", "D19"),
 x("VitrA'nın görünmediği yüksek hacimli kelimeler", "High-volume keywords where VitrA is absent"),
 T_BOS,
 x("SERP özellikleri ve AI Overview", "SERP features and AI Overview"),
 T_OZ,
 insight("AI Overview 31 kelimede çıkmıştır ve en yoğun olduğu yer soru kelimeleridir (7'nin 5'i). VitrA 7 AI Overview'da kaynak gösterilmektedir: pisuvar, duş kanalı, porselen karo, klozet ölçüleri, en iyi klozet markası, hangi klozet alınmalı ve akıllı klozet nedir. Bu kelimelerin çoğunda VitrA organik olarak da 1. sıradadır. Bitişik ürünlerde (elektrikli havlupan, derz dolgu, ısıtmalı klozet kapağı, şamandıra) ve \"gömme rezervuar mı dış rezervuar mı\" sorusunda AI Overview çıkmakta, VitrA kaynak gösterilmemektedir. Arama sonuçlarında Shopping bloğu hiçbir kelimede dönmemiştir; ürün listeleme organik sonuç olarak pazaryeri ve karşılaştırma sayfalarında görünmektedir.",
         "AI Overview appeared for 31 keywords and is most frequent for question keywords (5 of 7). VitrA is cited in 7 AI Overviews: urinal, shower channel, porcelain tile, WC dimensions, best WC brand, which WC to buy and what is a smart WC. VitrA also ranks first organically for most of these keywords. For adjacent products (electric towel radiator, grout, heated toilet seat, float valve) and the question \"concealed or exposed cistern\", AI Overview appears without citing VitrA. No Shopping block was returned for any keyword; product listings appear as organic results on marketplace and comparison pages.", "D19"),
 x("AI Overview'da en çok kaynak gösterilen alan adları (24 blok)", "Domains cited most in AI Overview (24 blocks)"), RANK_AI,
 box("PEOPLE ALSO ASK", "PEOPLE ALSO ASK", "<p>%s</p>" % x("84 kelimede toplam 308 benzersiz soru döndü; 112'si fiyat, 73'ü \"nedir / nasıl\" niyetinde, 8'i VitrA'yı adıyla soruyor.", "308 unique questions were returned across 84 keywords; 112 carry price intent, 73 \"what / how\" intent, and 8 ask about VitrA by name.")),
 x("Kullanıcının Google'da sorduğu sorular", "Questions users ask on Google"),
 PAA_H,
 insight("Sorular üç ihtiyacı açıkça göstermektedir: işçilik dahil toplam maliyet (\"klozet yaptırmak kaç TL\", \"iç takım değişimi ne kadar\"), ölçü ve uyumluluk (\"klozet kapakları standart mı\", \"banyo dolabı yüksekliği\") ve marka güveni (\"VitrA iyi marka mı\", \"VitrA ve Artema aynı marka mı\"). Bu soruların cevaplarının kategori ve ürün sayfalarında kısa soru-cevap bloklarıyla verilmesi hem organik sıralamayı hem de AI Overview'da kaynak gösterilme olasılığını destekleyebilir.",
         "The questions clearly show three needs: total cost including labour (\"how much to have a WC fitted\", \"how much is an inner mechanism replacement\"), size and compatibility (\"are toilet seats standard\", \"bathroom cabinet height\") and brand trust (\"is VitrA a good brand\", \"are VitrA and Artema the same brand\"). Answering these questions with short Q&A blocks on category and product pages can support both organic rankings and the likelihood of being cited in AI Overview.", "D19"),
 kaynak("Google TR mobil SERP · DataForSEO · 109 kelime · ilk 20 organik sonuç · 29.09.2026 · hacim Keyword Planner", "Google TR mobile SERP · DataForSEO · 109 keywords · top 20 organic results · 29.09.2026 · volume Keyword Planner", "D19", "D12"),
)
