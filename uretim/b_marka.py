# -*- coding: utf-8 -*-
"""Bolum: Marka aramalari ve autocomplete - kullanicinin VitrA'dan bekledikleri."""
from ortak import *
import json, os
from rapor_parca1 import T
from ortak import _hacim
AU = A["auto"]; AT = A["auto_tema"]; TQ = A["gsc_top_sorgu"]
import re as _re
_GURULTU = _re.compile(r"klozetas|klozeto|dangtis|zaandam|weil am rhein|\bvitray|kayseri|schweiz|brussels|zürich|deutschland|nederland|belgique")   # yazim gurultusu ve toplama konumuna/yurt disina bagli oneriler
def _temiz(lst): return [o for o in lst if not _GURULTU.search(o)]
from niyet_kurallari import niyet as _niy
_TSINIF = {"Fiyat": "t-fiyat", "Tamir ve bakım": "t-tamir", "Montaj": "t-montaj"}
def kwt(s):
    c = _TSINIF.get(_niy(s)); h = kwv(s)
    return h.replace('<span class="kw">', '<span class="kw %s">' % c, 1) if c else h
TLEJ = '<div class="kwlej">%s</div>' % "".join('<span class="kw %s">%s</span>' % (c, x(t, e)) for t, e, c in [("Fiyat", "Price", "t-fiyat"), ("Tamir ve bakım", "Repair and maintenance", "t-tamir"), ("Montaj", "Installation", "t-montaj")])
def satir(tohum, en):
    return [kwv(tohum), '<div class="kwlist">%s</div>' % "".join(kwt(s) for s in _temiz(AU.get(tohum, []))[:10])]
TOHUM = [("vitra", "vitra"), ("vitra klozet", "vitra klozet"), ("vitra gömme rezervuar", "vitra gömme rezervuar"), ("vitra banyo dolabı", "vitra banyo dolabı"), ("vitra batarya", "vitra batarya"),
         ("vitra duşakabin", "vitra duşakabin"), ("vitra akıllı klozet", "vitra akıllı klozet"), ("vitra klozet kapağı", "vitra klozet kapağı"), ("vitra servis", "vitra servis"), ("vitra yedek parça", "vitra yedek parça"),
         ("vitra bayi", "vitra bayi"), ("vitra taksit", "vitra taksit"), ("vitra indirim", "vitra indirim"), ("vitra outlet", "vitra outlet")]
tbl = tablo([th("Kök ifade", "Seed phrase", "Google arama kutusuna yazılan ifade; öneriler bu ifadenin devamı olarak gelmektedir.", "Phrase typed into the Google search box; suggestions come as continuations of it."),
             th("Autocomplete önerileri · 2026 aylık ort. hacim", "Autocomplete suggestions · 2026 monthly avg. volume", "Google'ın Türkiye, Türkçe, masaüstü Chrome için döndürdüğü ilk 10 tamamlama önerisi; sırası Google'ın sırasıdır. Rozet: Ocak - Ağustos 2026 aylık ortalama arama hacmi (Google Ads); rozeti olmayan kelime için hacim dönmemiştir.", "First 10 completion suggestions Google returns for Turkey, Turkish, desktop Chrome; the order is Google's.")],
            [satir(t, e) for t, e in TOHUM], "uzun")
_AE = json.load(open(os.path.join(veri.V, "ham", "autocomplete_ek.json"), encoding="utf-8"))
G_EN = {"Kategori": "Category", "Montaj ve tamir": "Installation and repair", "Yenileme ve tasarım": "Renovation and design", "Fiyat ve ödeme": "Price and payment", "Rakip marka": "Competitor brand", "Perakendeci": "Retailer"}
_HARIC = {"batarya değişimi"}   # oneriler telefon bataryasina kaydigi icin tablo disi
def _hk(s_): return (_hacim(s_) or 0)
rows2 = []
for g_, lst_ in _AE["grup"].items():
    for s_ in sorted([q for q in lst_ if q not in _HARIC], key=lambda q: -_hk(q)):
        rows2.append([x(g_, G_EN[g_]), kwv(s_), '<div class="kwlist">%s</div>' % "".join(kwt(o) for o in _temiz(_AE["oneri"].get(s_, []))[:10])])
N_EK = len(rows2)
tbl2 = tablo([th("Grup", "Group", "Kök ifadenin türü: kategori, montaj ve tamir, yenileme ve tasarım, fiyat ve ödeme, rakip marka, perakendeci.", "Type of seed phrase: category, installation and repair, renovation and design, price and payment, competitor brand, retailer."),
              th("Kök ifade", "Seed phrase", "Google arama kutusuna yazılan ifade; rozet Ocak - Ağustos 2026 aylık ortalama arama hacmidir (Google Ads). Grup içinde hacme göre sıralanmıştır.", "Phrase typed into the Google search box; the badge is the January - August 2026 monthly average search volume (Google Ads). Sorted by volume within each group."),
              th("Autocomplete önerileri · 2026 aylık ort. hacim", "Autocomplete suggestions · 2026 monthly avg. volume", "Google'ın Türkiye, Türkçe, masaüstü Chrome için döndürdüğü ilk 10 tamamlama önerisi (30 Eyl 2026); sırası Google'ın sırasıdır. Rozet Ocak - Ağustos 2026 aylık ortalama arama hacmidir.", "First 10 completion suggestions Google returns for Turkey, Turkish, desktop Chrome (30 Sep 2026), in Google's order. The badge is the January - August 2026 monthly average search volume.")],
             rows2, "uzun")
from niyet_kurallari import niyet as _niyet
from collections import Counter as _Counter
_ONERI = [o for t_, _ in TOHUM for o in _temiz(AU.get(t_, []))[:10]] + [o for g_, lst_ in _AE["grup"].items() for s_ in lst_ if s_ not in _HARIC for o in _temiz(_AE["oneri"].get(s_, []))[:10]]
_ONERI = list(dict.fromkeys(_ONERI))   # iki kok ifadede donen ayni oneri bir kez sayilir
AT = dict(_Counter(_niyet(o) for o in _ONERI))
N_KOK = len(TOHUM) + N_EK
_PER = [("Koçtaş", r"koçtaş|koctas"), ("IKEA", r"ikea"), ("Bauhaus", r"bauhaus"), ("Trendyol", r"trendyol"), ("Tekzen", r"tekzen"), ("Cimri", r"cimri"), ("A101", r"a101"), ("Hepsiburada", r"hepsiburada"), ("Amazon", r"amazon"), ("n11", r"\bn11\b")]
_ONERI_PK = list(dict.fromkeys([o for t_, _ in TOHUM for o in _temiz(AU.get(t_, []))[:10]] + [o for g_, lst_ in _AE["grup"].items() if g_ != "Perakendeci" for s_ in lst_ if s_ not in _HARIC for o in _temiz(_AE["oneri"].get(s_, []))[:10]]))
PER = [(ad, sum(1 for o in _ONERI_PK if _re.search(rx, o))) for ad, rx in _PER]; PER = [p_ for p_ in sorted(PER, key=lambda i: -i[1]) if p_[1]]
# perakendeci kok ifadelerinden ("ikea banyo dolabı" gibi) gelen oneriler zaten perakendeci adi tasidigindan sayima alinmaz
N_PER = sum(1 for o in _ONERI_PK if any(_re.search(rx, o) for _, rx in _PER))
T_EN = {"Jenerik ürün": "Generic product", "Fiyat": "Price", "Tamir ve bakım": "Repair and maintenance", "Tasarım ve fikir": "Design and ideas", "Montaj": "Installation", "Ölçü ve teknik": "Dimensions and technical", "Yer ve kanal": "Where to buy", "Seçim ve karşılaştırma": "Selection and comparison"}
attot = sum(AT.values())
_TL = {"Jenerik ürün": ("Ürün adı ve diğer", "Product name and other")}   # siniflanamayan oneriler
def _tl(t): return x(*_TL.get(t, (t, T_EN[t])))
from grafik2 import gruplu as _gr, f_pay as _fp
_ATS = sorted(AT.items(), key=lambda i: -i[1])
GT3 = _gr([(_tl(t), [100 * v / attot]) for t, v in _ATS], [(x("Öneri payı", "Share of suggestions"), "#E85F36")], genislik=460)
tema_rows = [[_tl(t), cell(v), n(yzd(100 * v / attot))] for t, v in sorted(AT.items(), key=lambda i: -i[1])]
tbl3 = tablo([th("Öneri teması", "Suggestion theme", "Önerinin ifade kalıbına göre sınıfı.", "Class of the suggestion by phrase pattern."),
              th("Öneri", "Suggestions", "Tablolarda yer alan 66 kök ifadeden dönen tekil öneri sayısı (kök ifade başına en fazla 10; iki kök ifadede dönen öneri bir kez sayılmıştır).", "Number of unique suggestions returned for the 66 seed phrases in the tables (up to 10 per seed; a suggestion returned for two seeds is counted once).", True),
              th("Pay", "Share", "Toplam öneri içindeki pay.", "Share of total suggestions.", True)], tema_rows, "dar")
rows4 = [[veri_m(q), cell(c), cell(i), n(yzd(ctr)), n(("%.1f" % pos).replace(".", ","))] for q, c, i, ctr, pos in TQ[:20]]
tbl4 = tablo([th("Sorgu", "Query", "Kullanıcının Google'a yazdığı ifade.", "Phrase the user typed into Google."),
              th("Click", "Clicks", "1 Haz 2025 - 25 Eyl 2026.", "1 Jun 2025 - 25 Sep 2026.", True),
              th("Gösterim", "Impressions", "Aynı dönem.", "Same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Sıra", "Position", "Ortalama sıra.", "Average position.", True)], rows4, "uzun")
def _gq(q_, alan, en=False):
    r_ = next(t_ for t_ in TQ if t_[0] == q_)
    v_ = r_[alan]
    if alan == 2: return k(v_).replace(",", ".") if en else k(v_)
    if alan == 3: return ("%.1f%%" % v_) if en else yzd(v_)
    return ("%.1f" % v_) if en else ("%.1f" % v_).replace(".", ",")
HTML = """
<p class="lede">%s</p>
<div class="metrics">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div><h3>%s</h3>%s</div></div>
%s
%s
""" % (
 x("Google'ın arama kutusunda önerdiği tamamlamalar, gerçek kullanıcı aramalarından türetildiği için markadan ne beklendiğini en doğrudan gösteren kaynaklardan biridir. %d kök ifade için Türkiye, Türkçe, masaüstü Chrome önerileri alınmıştır; bunların %d'i \"vitra\" ile başlayan kök ifadeler (28 Eylül 2026), %d'si kategori, hizmet, fiyat, rakip marka ve perakendeci kök ifadeleridir (30 Eylül 2026). Üstteki dört gösterge ve tema dağılımı bu iki setteki %d öneriye dayanmaktadır; yazım hatalı ve toplama konumuna bağlı (il adı, yurt dışı) öneriler çıkarılmıştır." % (N_KOK, len(TOHUM), N_EK, len(_ONERI)),
   "The completions Google suggests in the search box are derived from real user searches, which makes them one of the most direct sources for what is expected of the brand. Suggestions were collected for %d seed phrases for Turkey, Turkish, desktop Chrome: %d seed phrases starting with \"vitra\" (28 September 2026) and %d seed phrases for categories, services, price, competitor brands and retailers (30 September 2026). The four indicators above and the theme distribution are based on the %d suggestions in these two sets; misspelt suggestions and those tied to the collection location (city names, abroad) were removed." % (N_KOK, len(TOHUM), N_EK, len(_ONERI))),
 metric("Tamir ve bakım önerileri", "Repair and maintenance suggestions", yzd(100 * AT["Tamir ve bakım"] / attot), "Tüm önerilerin payı; \"iç takımı\", \"şamandıra\", \"su kaçırıyor\", \"menteşe\"", "Share of all suggestions; \"iç takımı\", \"şamandıra\", \"su kaçırıyor\", \"menteşe\""),
 metric("Fiyat önerileri", "Price suggestions", yzd(100 * AT["Fiyat"] / attot), "\"fiyat\", \"indirim\", \"kampanya\" ve \"ne kadar\" içeren öneriler; paylar kök ifade seçimini de yansıtır", "Suggestions containing \"price\", \"discount\", \"campaign\" and \"how much\"; shares also reflect the choice of seed phrases"),
 metric("Montaj önerileri", "Installation suggestions", yzd(100 * AT["Montaj"] / attot), "\"montajı\", \"montaj aparatı\", \"montaj ücreti\", \"taktırma\"", "\"montajı\", \"montaj aparatı\", \"montaj ücreti\", \"taktırma\""),
 metric("Perakendeci adı geçen öneri · perakendeci kök ifadeleri hariç", "Suggestions naming a retailer · excluding retailer seed phrases", "%d" % N_PER, ", ".join("%s %d" % p_ for p_ in PER[:5]), ", ".join("%s %d" % p_ for p_ in PER[:5])),
 x("\"vitra\" ile başlayan aramalar", "Searches starting with \"vitra\""),
 TLEJ + tbl,
 insight("\"vitra klozet\" önerilerinde fiyat, kapak, model ve takım aramalarının yanında \"iç takımı\", \"su kaçırıyor\", \"şamandırası\" ve \"kapağı menteşesi\" yer almaktadır; \"vitra gömme rezervuar\" önerilerinin çoğunluğu iç takım, şamandıra, conta ve boşaltma grubu gibi yedek parça ifadeleridir. Bu dağılım, mevcut ürün sahibinin markadan yedek parça ve çözüm beklentisinin öne çıktığına işaret etmektedir; \"vitra servis\" önerileri ise ücret, numara, en yakın ve randevu ile servis sürecine ilişkin bilgi ihtiyacını göstermektedir. \"vitra taksit\" kök ifadesi \"taksit seçenekleri\", \"kaç taksit\", \"9 taksit\" ve \"kredi kartı taksit\" önerilerini getirmektedir. Sitede üst bantta \"vade farksız 6 ay\", Banyo Asistanı kampanya sayfasında \"9 taksit\", ürün sayfasındaki taksit tablosunda 12 taksite kadar seçenek yer aldığından, taksit bilgisinin tek ve net bir mesajla verilmesi fayda sağlayabilir.",
         "The \"vitra klozet\" suggestions include \"iç takımı\" (inner mechanism), \"su kaçırıyor\" (leaking), \"şamandırası\" (float valve) and \"kapağı menteşesi\" (seat hinge) alongside price, seat, model and set searches; most \"vitra gömme rezervuar\" suggestions are spare-part phrases such as inner mechanism, float valve, gasket and flush valve. This distribution indicates that existing owners' expectation of spare parts and solutions from the brand stands out; the \"vitra servis\" suggestions (fee, number, nearest, appointment) show an information need about the service process. The \"vitra taksit\" seed phrase brings \"taksit seçenekleri\" (instalment options), \"kaç taksit\" (how many instalments), \"9 taksit\" and \"kredi kartı taksit\" (credit card instalments). Since the site shows \"6 months interest-free\" in the top banner, \"9 instalments\" on the Bathroom Assistant campaign page and up to 12 instalments in the product page table, a single, clear instalment message can be beneficial.", "D3"),
 x("Kategori ve rakip marka aramaları", "Category and competitor brand searches"),
 TLEJ + tbl2,
 insight("Kategori kök ifadelerinde öneriler fiyat, ölçü ve yedek parça (şamandıra, iç takım, menteşe) ekseninde toplanmaktadır; \"akıllı klozet\" ve \"gömme rezervuar tamiri\" önerilerinde marka olarak VitrA yer almaktadır. Rakip kök ifadelerinde klozet markalarının önerileri kapak, menteşe ve iç takım; batarya markalarının önerileri kartuş ve yedek parça; banyo dolabı markalarının önerileri ise ölçü (60, 80, 100 cm), katalog ve satış noktası üzerinde yoğunlaşmaktadır. Perakendeci kök ifadeleri arasında en yüksek hacim \"ikea banyo dolabı\" ifadesindedir (7,9K); fiyat önerilerinde Koçtaş, Bauhaus, Trendyol ve Cimri adları geçmektedir. Yenileme ifadelerinde \"maliyeti 2026\" ve \"ne kadar tutar\" önerileri, bütçe sorusunun yenileme kararında öne çıktığına işaret etmektedir.",
         "In the category seeds, suggestions cluster around price, dimensions and spare parts (float valve, inner mechanism, hinge); VitrA appears as the brand in the \"akıllı klozet\" (smart WC) and \"gömme rezervuar tamiri\" (concealed cistern repair) suggestions. In the competitor seeds, WC brands draw seat, hinge and inner-mechanism suggestions; tap brands draw cartridge and spare-part suggestions; bathroom-cabinet brands draw size (60, 80, 100 cm), catalogue and point-of-sale suggestions. Among the retailer seeds, the highest volume is for \"ikea banyo dolabı\" (7.9K); price suggestions name Koçtaş, Bauhaus, Trendyol and Cimri. In the renovation phrases, \"maliyeti 2026\" (cost 2026) and \"ne kadar tutar\" (how much does it cost) suggestions indicate that the budget question stands out in the renovation decision."),
 x("Autocomplete önerilerinin tema oranı", "Theme share of autocomplete suggestions"), GT3 + tbl3,
 x("En çok tık getiren sorgular · Search Console", "Queries bringing most clicks · Search Console"), tbl4,
 insight("Search Console'da en çok tık getiren sorgular marka ve kategori adıdır. \"lavabo\" %s gösterimde %s ortalama sırada yalnızca %s CTR üretmekte, \"vitra gömme rezervuar\" ise %s ortalama sırada %s CTR ile kalmaktadır: bu sorgularda AI Overview ve kelimenin farklı anlamları (\"lavabo\" tuvalet anlamında ve \"lavabo açıcı\" olarak da aranmaktadır) tık payını sınırlamaktadır; başlık ve açıklama metinlerinin test edilmesi değerlendirilebilir." % (_gq("lavabo", 2), _gq("lavabo", 4), _gq("lavabo", 3), _gq("vitra gömme rezervuar", 4), _gq("vitra gömme rezervuar", 3)),
         "In Search Console the queries bringing the most clicks are the brand and category names. \"lavabo\" produces only %s CTR on %s impressions at an average position of %s, and \"vitra gömme rezervuar\" stays at %s CTR at an average position of %s: in these queries AI Overview and other meanings of the word (\"lavabo\" is also searched in the sense of toilet and as \"lavabo açıcı\", drain opener) limit the click share; testing titles and descriptions can be considered." % (_gq("lavabo", 3, True), _gq("lavabo", 2, True), _gq("lavabo", 4, True), _gq("vitra gömme rezervuar", 3, True), _gq("vitra gömme rezervuar", 4, True)), "D2"),
 kaynak("Google Autocomplete · \"vitra\" ile başlayan %d kök ifade (%s) ve %d kategori, hizmet, fiyat, rakip marka ve perakendeci kök ifadesi (30 Eyl 2026) · Türkiye, Türkçe, masaüstü Chrome · Google Ads hacim · Google Search Console sorgu raporu" % (len(TOHUM), veri.TARIH, N_EK),
        "Google Autocomplete · %d seed phrases starting with \"vitra\" (%s) and %d category, service, price, competitor brand and retailer seed phrases (30 Sep 2026) · Turkey, Turkish, desktop Chrome · Google Ads volume · Google Search Console query report" % (len(TOHUM), veri.TARIH, N_EK), "D3", "D2"),
)
