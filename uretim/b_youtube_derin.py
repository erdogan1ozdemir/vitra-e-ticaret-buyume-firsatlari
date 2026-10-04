# -*- coding: utf-8 -*-
"""YouTube bolumu ek: 68 arama, kanal turu, yorum temalari, video firsatlari (D20)."""
from ortak import *
import json, os
D = os.path.join(veri.V, "ham", "derin", "youtube")
AN = json.load(open(os.path.join(D, "analiz.json"), encoding="utf-8"))
YT = json.load(open(os.path.join(D, "yorum_temalari.json"), encoding="utf-8"))
VF = json.load(open(os.path.join(D, "video_firsatlari.json"), encoding="utf-8"))
GEN = {"Seçim ve karşılaştırma": "Selection and comparison", "Montaj": "Installation", "Tamir ve bakım": "Repair and maintenance",
       "İlham ve tadilat": "Inspiration and renovation", "Marka ve rakip": "Brand and competitor", "Yeni kategoriler": "New categories"}
def mil(v): return x("%sM" % ("%.1f" % (v / 1e6)).replace(".", ","), "%.1fM" % (v / 1e6))
T_GR = tablo([th("Niyet grubu", "Intent group", "68 YouTube aramasının niyete göre gruplanması.", "Grouping of the 68 YouTube searches by intent."),
              th("Arama", "Searches", "Gruptaki arama ifadesi sayısı.", "Number of search phrases in the group.", True),
              th("Tekil video", "Unique videos", "İlk 20 sonuçta görünen tekil video sayısı; alakasız sonuçlar hariç.", "Unique videos in the top 20 results; irrelevant results excluded.", True),
              th("Toplam izlenme", "Total views", "Tekil videoların izlenme toplamı; bir video birden fazla aramada çıksa da bir kez sayılmıştır.", "Sum of views of unique videos; a video appearing in several searches is counted once.", True),
              th("Medyan izlenme", "Median views", "Video başına medyan izlenme; tek bir viral videonun etkisini dengelemek için verilmiştir.", "Median views per video; given to offset the effect of a single viral video.", True),
              th("VitrA / Artema kanalının göründüğü arama", "Searches with a VitrA / Artema channel", "VitrA Türkiye, VitrA Bathrooms veya Artema Türkiye (aynı grup) kanalından en az bir videonun ilk 20'de olduğu arama sayısı.", "Number of searches with at least one video from VitrA Türkiye, VitrA Bathrooms or Artema Türkiye in the top 20.", True),
              th("VitrA ort. en iyi sıra", "VitrA avg. best position", "VitrA kanalının göründüğü aramalarda en iyi sıraların ortalaması.", "Average of best positions in searches where the VitrA channel appears.", True)],
             [[etk(g, GEN[g]), cell(v["arama"]), cell(v["tekil_video"]), n(mil(v["toplam_izlenme_tekil"])), cell(v["medyan_izlenme_video"]),
               n("%d / %d" % (v["vitra_olan_arama"], v["arama"])), n(x(("%.1f" % v["vitra_ort_en_iyi_sira"]).replace(".", ","), "%.1f" % v["vitra_ort_en_iyi_sira"]) if v["vitra_ort_en_iyi_sira"] else "-")]
              for g, v in AN["grup"].items()])
TUR = {"Marka": "Brand", "Tesisatçı / usta": "Plumber / installer", "Perakendeci": "Retailer", "Dekorasyon / iç mimar": "Decoration / interior designer", "İnceleme / teknoloji": "Review / technology", "Diğer": "Other"}
tg = sum(v["gorunme"] for v in AN["tur"].values())
T_TUR = tablo([th("Kanal türü", "Channel type", "Kanal adı ve içeriğine göre yapılan sınıflandırma.", "Classification by channel name and content."),
               th("Kanal sayısı", "Channels", "Türdeki kanal sayısı.", "Number of channels of the type.", True),
               th("Görünme payı", "Share of appearances", "68 aramanın ilk 20 sonucundaki toplam görünme içindeki pay.", "Share of total appearances in the top 20 results of the 68 searches.", True)],
              [[x(t, TUR[t]), cell(v["kanal"]), n(yzd(v["gorunme"] / tg * 100))] for t, v in AN["tur"].items()], "dar")
TEM = [("Ürün kalitesi / kırılma / sızıntı", "Product quality / breakage / leaks", "Kullanmaya başlayalı 8 ay oldu ve sızıntı başladı.", "https://www.youtube.com/watch?v=a1i0pneZhdw"),
       ("Fiyat", "Price", "Min 1500TL lik işi 90 TL ye çözdüm sayenizde.", "https://www.youtube.com/watch?v=eLA0UQvn-9U"),
       ("Montaj zorluğu / uygulama soruları", "Installation difficulty / application questions", "Hocam bunun sökme işlemini de bir göstersen sökemedim biz", "https://www.youtube.com/watch?v=Rcvk_z95Zxc"),
       ("Usta ücreti / usta bulma", "Installer fee / finding an installer", "Usta çağırdım yapmaya cesaret edemedi.", "https://www.youtube.com/watch?v=uiWwzjYYF0k"),
       ("Servis ve garanti", "Service and warranty", "Sayenizde 250 servis ücreti vermeden 40tl ye hallettim.", "https://www.youtube.com/watch?v=6TgHlbFCsh8"),
       ("Satın alma kanalı", "Purchase channel", "vitra conta 5 6 nalbura gittim bulamadim. Nerden bulabilirim", "https://www.youtube.com/watch?v=8aSO7T-b650"),
       ("Parça bulma / yedek parça", "Finding parts / spare parts", "parça numarasını da verebilirmisiniz o contanın aynısından", "https://www.youtube.com/watch?v=8aSO7T-b650"),
       ("Marka karşılaştırması", "Brand comparison", "banyo eviye lavabo bataryası olarak hangi marka tavsiye edersin ?", "https://www.youtube.com/watch?v=lkfdmDjQZCc")]
T_YR = tablo([th("Tema", "Theme", "Yorumun anahtar ifadelere göre atandığı tema; bir yorum birden fazla temaya girebilir.", "Theme assigned to the comment by key phrases; a comment may fall into several themes."),
              th("Yorum", "Comments", "Temaya giren yorum sayısı (2.218 geçerli yorum içinde).", "Number of comments in the theme (out of 2,218 valid comments).", True),
              th("Pay", "Share", "Geçerli yorumlar içindeki pay.", "Share of valid comments.", True),
              th("VitrA ürünlü videolarda", "On VitrA-product videos", "VitrA veya Artema ürününün tamir ya da montajını anlatan videolardaki yorum sayısı.", "Comments on videos showing the repair or installation of a VitrA or Artema product.", True),
              th("Örnek yorum", "Example comment", "Kaynaktaki yazımıyla kısaltılmış kullanıcı yorumu; bağlantı videoya gider.", "User comment shortened, spelling as in the source; the link goes to the video.")],
             [[x(a, b), cell(YT["temalar"][a]["yorum"]), n(yzd(YT["temalar"][a]["pay_gecerli"])), cell(YT["temalar"][a]["vitra_videolari_yorum"]), u(url, "“%s”" % q)] for a, b, q, url in sorted(TEM, key=lambda t_: -YT["temalar"][t_[0]]["yorum"])])
FEN = {"Klozet sifon / iç takım değiştirme, su kaçırma": "WC flush valve / inner mechanism replacement, leaks", "Rezervuar şamandıra ve su seviyesi ayarı": "Cistern float and water level adjustment",
       "Gömme rezervuar su doldurmuyor / geç doluyor": "Concealed cistern not filling / filling slowly", "Batarya damlatıyor, aç-kapa kartuş değişimi": "Dripping tap, quarter-turn cartridge replacement",
       "Lavabo sifonu tıkanıklığı ve sifon temizliği": "Basin trap blockage and trap cleaning", "Banyoda silikon çekme": "Applying silicone in the bathroom", "Batarya kireç temizliği": "Tap limescale cleaning",
       "Taharet musluğu takma": "Fitting a bidet valve", "Duşakabin kurulum, seçim ve teker değişimi": "Shower enclosure installation, selection and roller replacement",
       "Banyo tadilatı maliyeti ve öncesi-sonrası": "Bathroom renovation cost and before-after", "Küçük banyo ve kiralık ev banyo yenileme": "Small bathroom and rented-home bathroom makeover",
       "Fayans boyama ve fayans üstüne fayans": "Tile painting and tiling over tiles", "Akıllı klozet karar içeriği": "Smart toilet decision content", "Rakip gömme rezervuar karşılaştırması (Geberit)": "Competitor concealed cistern comparison (Geberit)",
       "Banyo dolabı marka ve malzeme kararı": "Bathroom cabinet brand and material decision", "Lavabo seçimi": "Washbasin selection", "Ankastre ve termostatik batarya montajı": "Concealed and thermostatic tap installation",
       "Havlupan montajı ve elektrikli havlupan": "Towel radiator installation and electric towel radiators", "Çocuk klozet adaptörü": "Children's toilet seat adapter",
       "Engelli banyo düzenlemesi": "Accessible bathroom layout", "Çamaşır makinesi dolabı montajı": "Washing machine cabinet installation"}
VS = sorted([r for r in VF if r["konu"] != "Fayans boyama ve fayans üstüne fayans"], key=lambda r: -r["toplam"])[:14]
T_VF = tablo([th("Video konusu", "Video topic", "Aramaların birleştirildiği konu.", "Topic combining the searches."),
              th("YouTube araması", "YouTube search", "Konuyu temsil eden arama ifadeleri.", "Search phrases representing the topic."),
              th("Toplam izlenme", "Total views", "İlk 20 sonuçtaki tekil videoların izlenme toplamı.", "Sum of views of unique videos in the top 20 results.", True),
              th("En çok izlenen kanal", "Most-viewed channel", "Konudaki en yüksek izlenmeli videonun kanalı.", "Channel of the most-viewed video in the topic."),
              th("VitrA / Artema kanal videosu", "VitrA / Artema channel videos", "İlk 20'de VitrA veya Artema kanalına ait video sayısı.", "Number of VitrA or Artema channel videos in the top 20.", True),
              th("VitrA geçen 3. taraf video", "Third-party videos naming VitrA", "Başlığında VitrA ya da Artema geçen, marka dışı kanallara ait video sayısı.", "Videos from non-brand channels with VitrA or Artema in the title.", True)],
             [[x(r["konu"], FEN[r["konu"]]), veri_m(", ".join(r["arama"])), n(mil(r["toplam"])), veri_m(" ".join(r["en_kanal"].split())), cell(r["vitra_marka_video"]), cell(r["vitra_ucuncu_taraf"])] for r in VS], "uzun")
MB = AN["marka_bahis"]["VitrA"]; VK = AN["marka_kanal"]["VitrA Türkiye"]["toplam"]
EK = """
<h3>%s</h3>
<p>%s</p>
<div class="kpis">%s%s%s%s</div>
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div>%s</div></div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Genişletilmiş tarama: 68 arama, altı niyet grubu", "Extended scan: 68 searches, six intent groups"),
 x("İlk taramaya ek olarak seçim, montaj, tamir, ilham, marka ve yeni kategori niyetlerini kapsayan 68 arama için ilk 20 sonuç, kanal türü ve 33 videonun 2.218 yorumu incelenmiştir.",
   "In addition to the first scan, the top 20 results, channel types and 2,218 comments on 33 videos were examined for 68 searches covering selection, installation, repair, inspiration, brand and new-category intents."),
 kpi_kart(k(VK["gorunme"]), "VitrA Türkiye görünmesi · %d arama, %d tekil video" % (VK["arama"], VK["tekil_video"]), "VitrA Türkiye appearances · %d searches, %d unique videos" % (VK["arama"], VK["tekil_video"]), "up"),
 kpi_kart(x("%43,7", "43.7%"), "Tesisatçı ve usta kanallarının görünme payı · 252 kanal", "Share of appearances by plumber and installer channels · 252 channels", "hi"),
 kpi_kart("0 / 16", "İlham, tadilat ve yeni kategori aramalarında VitrA kanalı", "VitrA channel in inspiration, renovation and new-category searches", "dn"),
 kpi_kart(k(MB["ucuncu_taraf_video"]), "Başlığında VitrA geçen marka dışı kanal videosu · 2,2M izlenme", "Videos from non-brand channels with VitrA in the title · 2.2M views", "hi"),
 T_GR,
 insight("VitrA ve Artema kanallarının göründüğü 4 marka aramasında ortalama en iyi sıra 2,0'dır; montaj aramalarının 15'inin 9'unda bu kanallar ilk 20'dedir. Tamir ve bakım aramaları medyan video izlenmesinde en yüksek gruptur (55.728); bu grupta VitrA 10 aramanın 2'sinde görünmektedir. İlham ve tadilat (26,2M izlenme) ile yeni kategori aramalarında (14,0M) VitrA kanalına ait video bulunmamaktadır.",
         "In the 4 brand searches where the VitrA and Artema channels appear, their average best position is 2.0; these channels are in the top 20 for 9 of 15 installation searches. Repair and maintenance searches have the highest median video views (55,728); VitrA appears in 2 of 10 searches in this group. There is no VitrA channel video in inspiration and renovation (26.2M views) or new-category searches (14.0M).", "D20"),
 x("Kanal türleri", "Channel types"), T_TUR,
 note("OKUMA", "READING", ul_b([("Görünme payı:", "Share of appearances:", "tesisatçı ve usta kanalları %43,7, marka kanalları %20,0 pay taşımaktadır.", "plumber and installer channels carry 43.7% and brand channels 20.0%."),
                                 ("Tamir ve montaj:", "Repair and installation:", "bu aramalarda bağımsız usta kanallarının görünürlüğü üretici kanallarından daha yüksektir.", "in these searches independent plumber channels are more visible than manufacturer channels."),
                                 ("35 üçüncü taraf VitrA videosunun 8'i", "8 of the 35 third-party VitrA videos", "tamir videosudur; VitrA ürünlerinin tamiri marka dışı kanallarda anlatılmaktadır.", "are repair videos; the repair of VitrA products is explained on non-brand channels.")])),
 x("Yorumlarda öne çıkan konular", "Topics in the comments"),
 T_YR,
 insight("Geçerli yorumların %51,7'si teşekkür ve genel ifadelerdir; konu belirten yorumlarda en sık konu ürün kalitesi ve sızıntıdır (tüm geçerli yorumların %11,1'i), bunu fiyat (%7,3) ve montaj soruları (%4,1) izlemektedir. Yorumlarda usta ve servis ücretinden tasarruf, parçanın nereden bulunacağı ve parça numarası sorusu tekrar etmektedir. Bu sorular, video açıklamalarında açılması önerilen yedek parça kategorisinin bağlantısı ve parça kodu verilmesiyle doğrudan karşılanabilecek ihtiyaçlardır.",
         "51.7% of valid comments are thanks and general remarks; among comments naming a topic the most frequent is product quality and leaks (11.1% of all valid comments), followed by price (7.3%) and installation questions (4.1%). Savings on installer and service fees, where to find the part and the part number recur in the comments. These questions are needs that can be met directly by giving a link to the proposed spare-parts category and the part code in video descriptions.", "D20"),
 x("Video fırsatları", "Video opportunities"),
 T_VF,
 insight("En yüksek izlenmeli 14 konunun hiçbirinde ilk 20 sonuçta VitrA kanalına ait video bulunmamaktadır. Sifon ve iç takım değişimi (6,8M), batarya damlatması ve kartuş değişimi (7,0M), şamandıra ayarı (4,9M) ve duşakabin kurulumu (4,6M) VitrA'nın ürün ve yedek parça gamıyla doğrudan örtüşmektedir. Engelli banyo düzenlemesi (5,0M) ve çocuk klozet adaptörü (2,3M; tek bir videonun ağırlıkta olduğu konu) ise katalogda sınırlı yer alan segmentlerde ilgi olduğuna işaret etmektedir. Fayans boyama konusu tek bir viral video (13,7M) nedeniyle tablo dışında tutulmuştur.",
         "None of the 14 highest-viewed topics has a VitrA channel video in the top 20 results. Flush valve and inner mechanism replacement (6.8M), dripping taps and cartridge replacement (7.0M), float adjustment (4.9M) and shower enclosure installation (4.6M) overlap directly with VitrA's product and spare-part range. Accessible bathroom layout (5.0M) and children's toilet seat adapters (2.3M; a topic dominated by a single video) point to interest in segments with limited presence in the catalogue. Tile painting was left out of the table because of a single viral video (13.7M).", "D20"),
 kaynak("YouTube arama sonuçları ve yorumlar · 68 ifade · Türkiye · ilk 20 sonuç · 29.09.2026", "YouTube search results and comments · 68 phrases · Turkey · top 20 results · 29.09.2026", "D20"),
)
