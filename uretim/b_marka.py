# -*- coding: utf-8 -*-
"""Bolum: Marka aramalari ve autocomplete - kullanicinin VitrA'dan bekledikleri."""
from ortak import *
import json, os
from rapor_parca1 import T
from ortak import _hacim
AU = A["auto"]; AT = A["auto_tema"]; TQ = A["gsc_top_sorgu"]
def satir(tohum, en):
    return [kwv(tohum), '<div class="kwlist">%s</div>' % "".join(kwv(s) for s in AU.get(tohum, [])[:10])]
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
        rows2.append([x(g_, G_EN[g_]), kwv(s_), '<div class="kwlist">%s</div>' % "".join(kwv(o) for o in _AE["oneri"].get(s_, [])[:10])])
N_EK = len(rows2)
tbl2 = tablo([th("Grup", "Group", "Kök ifadenin türü: kategori, montaj ve tamir, yenileme ve tasarım, fiyat ve ödeme, rakip marka, perakendeci.", "Type of seed phrase: category, installation and repair, renovation and design, price and payment, competitor brand, retailer."),
              th("Kök ifade", "Seed phrase", "Google arama kutusuna yazılan ifade; rozet Ocak - Ağustos 2026 aylık ortalama arama hacmidir (Google Ads). Grup içinde hacme göre sıralanmıştır.", "Phrase typed into the Google search box; the badge is the January - August 2026 monthly average search volume (Google Ads). Sorted by volume within each group."),
              th("Autocomplete önerileri · 2026 aylık ort. hacim", "Autocomplete suggestions · 2026 monthly avg. volume", "Google'ın Türkiye, Türkçe, Chrome için döndürdüğü ilk 10 tamamlama önerisi (30 Eyl 2026); sırası Google'ın sırasıdır. Rozet Ocak - Ağustos 2026 aylık ortalama arama hacmidir.", "First 10 completion suggestions Google returns for Turkey, Turkish, Chrome (30 Sep 2026), in Google's order. The badge is the January - August 2026 monthly average search volume.")],
             rows2, "uzun")
T_EN = {"Ürün": "Product", "Fiyat": "Price", "Tamir ve bakım": "Repair and maintenance", "Tasarım": "Design", "Montaj": "Installation", "Ölçü ve teknik": "Dimensions and technical", "Bayi ve mağaza": "Dealer and store", "Seçim": "Selection"}
attot = sum(AT.values())
tema_rows = [[x(t, T_EN[t]), cell(v), n(yzd(100 * v / attot))] for t, v in sorted(AT.items(), key=lambda i: -i[1])]
tbl3 = tablo([th("Öneri teması", "Suggestion theme", "Önerinin ifade kalıbına göre sınıfı.", "Class of the suggestion by phrase pattern."),
              th("Öneri", "Suggestions", "49 kök ifadeden dönen toplam öneri sayısı.", "Total number of suggestions returned for 49 seed phrases.", True),
              th("Pay", "Share", "Toplam öneri içindeki pay.", "Share of total suggestions.", True)], tema_rows, "dar")
rows4 = [[veri_m(q), cell(c), cell(i), n(yzd(ctr)), n(("%.1f" % pos).replace(".", ","))] for q, c, i, ctr, pos in TQ[:20]]
tbl4 = tablo([th("Sorgu", "Query", "Kullanıcının Google'a yazdığı ifade.", "Phrase the user typed into Google."),
              th("Tık", "Clicks", "1 Haz 2025 - 25 Eyl 2026.", "1 Jun 2025 - 25 Sep 2026.", True),
              th("Gösterim", "Impressions", "Aynı dönem.", "Same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Sıra", "Position", "Ortalama sıra.", "Average position.", True)], rows4, "uzun")
kocs = sum(1 for v in AU.values() for s in v if "koçtaş" in s or "koctas" in s); tek = sum(1 for v in AU.values() for s in v if "tekzen" in s); kays = sum(1 for v in AU.values() for s in v if "kayseri" in s)
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
""" % (
 x("Google'ın arama kutusunda önerdiği tamamlamalar, gerçek kullanıcı aramalarından türetildiği için markadan ne beklendiğini en doğrudan gösteren kaynaklardan biridir. 49 kök ifade için Türkiye, Türkçe, masaüstü Chrome sonuçları alınmıştır.",
   "The completions Google suggests in the search box are derived from real user searches, which makes them one of the most direct sources for what is expected of the brand. Results were collected for 49 seed phrases for Turkey, Turkish, desktop Chrome."),
 metric("Tamir ve bakım önerileri", "Repair and maintenance suggestions", yzd(100 * AT["Tamir ve bakım"] / attot), "Tüm önerilerin payı; \"iç takımı\", \"şamandıra\", \"su kaçırıyor\", \"menteşe\"", "Share of all suggestions; \"inner mechanism\", \"float valve\", \"leaking\", \"hinge\""),
 metric("Fiyat önerileri", "Price suggestions", yzd(100 * AT["Fiyat"] / attot), "\"fiyatları\" ile biten ve perakendeci adı taşıyan öneriler", "Suggestions ending in \"prices\" and carrying a retailer name"),
 metric("Montaj önerileri", "Installation suggestions", yzd(100 * AT["Montaj"] / attot), "\"montajı\", \"montaj aparatı\", \"montaj ücreti\", \"taktırma\"", "\"installation\", \"fitting kit\", \"installation fee\", \"having it fitted\""),
 metric("Perakendeci adı geçen öneri", "Suggestions naming a retailer", "%d" % (kocs + tek), "Koçtaş %d, Tekzen %d: kullanıcı VitrA ürününü yapı marketten almayı da düşünmektedir" % (kocs, tek), "Koçtaş %d, Tekzen %d: the user also considers buying the VitrA product from a DIY store" % (kocs, tek)),
 x("\"vitra\" ile başlayan aramalar", "Searches starting with \"vitra\""),
 tbl,
 insight("\"vitra klozet\" önerilerinde fiyat, kapak, model ve takım aramalarının yanında \"iç takımı\", \"su kaçırıyor\", \"şamandırası\" ve \"kapağı menteşesi\" yer almaktadır; \"vitra gömme rezervuar\" önerilerinin çoğunluğu iç takım, şamandıra, conta ve boşaltma grubu gibi yedek parça ifadeleridir. Mevcut ürün sahibinin markadan beklediği ilk şey yedek parça ve çözümdür; \"vitra servis\" önerileri ise ücret, numara, en yakın ve randevu ile servis sürecine ilişkin belirsizliği göstermektedir. \"vitra taksit\" kök ifadeu \"taksit seçenekleri\", \"kaç taksit\", \"9 taksit\" ve \"kredi kartı taksit\" önerilerini getirmektedir. Sitede üst bantta \"vade farksız 6 ay taksit\", Banyo Asistanı'nda \"9 taksit\" mesajı yer aldığından, kullanıcının aradığı taksit sayısının tek ve net bir mesajla verilmesi fayda sağlayabilir.",
         "The \"vitra klozet\" suggestions include \"inner mechanism\", \"leaking\", \"float valve\" and \"seat hinge\" alongside price, seat, model and set searches; most \"vitra gömme rezervuar\" suggestions are spare-part phrases such as inner mechanism, float valve, gasket and flush valve. The first thing the existing owner expects from the brand is a spare part and a solution; the \"vitra servis\" suggestions (fee, number, nearest, appointment) show uncertainty about the service process. The \"vitra taksit\" seed brings \"instalment options\", \"how many instalments\", \"9 instalments\" and \"credit card instalment\". Since the site shows \"6 months interest-free\" in the top banner and \"9 instalments\" in the Bathroom Assistant, giving the instalment count users search for in a single, clear message can be beneficial.", "D3"),
 x("Kategori ve rakip marka aramaları", "Category and competitor brand searches"),
 tbl2,
 insight("Kategori kök ifadelerinde öneriler fiyat, ölçü ve yedek parça (şamandıra, iç takım, menteşe) ekseninde toplanmaktadır; \"akıllı klozet\" ve \"gömme rezervuar tamiri\" önerilerinde marka olarak VitrA yer almaktadır. Rakip kök ifadelerinde klozet markalarının önerileri kapak, menteşe ve iç takım; batarya markalarının önerileri kartuş ve yedek parça; banyo dolabı markalarının önerileri ise ölçü (60, 80, 100 cm), katalog ve satış noktası üzerinde yoğunlaşmaktadır. Perakendeci kök ifadeleri arasında en yüksek hacim \"ikea banyo dolabı\" ifadesindedir (7,9K); fiyat önerilerinde Koçtaş, Bauhaus, Trendyol ve Cimri adları geçmektedir. Yenileme ifadelerinde \"maliyeti 2026\" ve \"ne kadar tutar\" önerileri, bütçe sorusunun ürün seçiminden önce geldiğine işaret etmektedir.",
         "In the category seeds, suggestions cluster around price, dimensions and spare parts (float valve, inner mechanism, hinge); VitrA appears as the brand in the \"akıllı klozet\" (smart WC) and \"gömme rezervuar tamiri\" (concealed cistern repair) suggestions. In the competitor seeds, WC brands draw seat, hinge and inner-mechanism suggestions; tap brands draw cartridge and spare-part suggestions; bathroom-cabinet brands draw size (60, 80, 100 cm), catalogue and point-of-sale suggestions. Among the retailer seeds, the highest volume is for \"ikea banyo dolabı\" (7.9K); price suggestions name Koçtaş, Bauhaus, Trendyol and Cimri. In the renovation phrases, \"maliyeti 2026\" (cost 2026) and \"ne kadar tutar\" (how much does it cost) suggestions indicate that the budget question comes before product choice."),
 x("Öneri temaları", "Suggestion themes"), tbl3,
 x("En çok tık getiren sorgular · Search Console", "Queries bringing most clicks · Search Console"), tbl4,
 kaynak("Google Autocomplete · 49 kök ifade (%s) ve %d kategori, hizmet, fiyat, rakip marka ve perakendeci kök ifadesi (30 Eyl 2026) · Türkiye, Türkçe, Chrome · Google Ads hacim · Google Search Console sorgu raporu" % (veri.TARIH, N_EK),
        "Google Autocomplete · 49 seed phrases (%s) and %d category, service, price, competitor brand and retailer seed phrases (30 Sep 2026) · Turkey, Turkish, Chrome · Google Ads volume · Google Search Console query report" % (veri.TARIH, N_EK), "D3", "D2"),
)
