# -*- coding: utf-8 -*-
"""Bolum: Marka aramalari ve autocomplete - kullanicinin VitrA'dan bekledikleri."""
from ortak import *
from rapor_parca1 import T
AU = A["auto"]; AT = A["auto_tema"]; TQ = A["gsc_top_sorgu"]
def satir(tohum, en):
    return [veri_m(tohum), '<div class="kwlist">%s</div>' % "".join(kw(s) for s in AU.get(tohum, [])[:10])]
TOHUM = [("vitra", "vitra"), ("vitra klozet", "vitra klozet"), ("vitra gömme rezervuar", "vitra gömme rezervuar"), ("vitra banyo dolabı", "vitra banyo dolabı"), ("vitra batarya", "vitra batarya"),
         ("vitra duşakabin", "vitra duşakabin"), ("vitra akıllı klozet", "vitra akıllı klozet"), ("vitra klozet kapağı", "vitra klozet kapağı"), ("vitra servis", "vitra servis"), ("vitra yedek parça", "vitra yedek parça"),
         ("vitra bayi", "vitra bayi"), ("vitra taksit", "vitra taksit"), ("vitra indirim", "vitra indirim"), ("vitra outlet", "vitra outlet")]
tbl = tablo([th("Tohum ifade", "Seed phrase", "Google arama kutusuna yazılan ifade; öneriler bu ifadenin devamı olarak gelmektedir.", "Phrase typed into the Google search box; suggestions come as continuations of it."),
             th("Autocomplete önerileri", "Autocomplete suggestions", "Google'ın Türkiye, Türkçe, masaüstü Chrome için döndürdüğü ilk 10 tamamlama önerisi; sırası Google'ın sırasıdır.", "First 10 completion suggestions Google returns for Turkey, Turkish, desktop Chrome; the order is Google's.")],
            [satir(t, e) for t, e in TOHUM], "uzun")
TOHUM2 = [("klozet", "klozet"), ("banyo dolabı", "banyo dolabı"), ("gömme rezervuar", "gömme rezervuar"), ("duşakabin", "duşakabin"), ("akıllı klozet", "akıllı klozet"), ("klozet montaj", "klozet montaj"), ("klozet tamir", "klozet tamir"),
          ("banyo dolabı montaj", "banyo dolabı montaj"), ("klozet taksit", "klozet taksit"), ("banyo yenileme", "banyo yenileme"), ("artema", "artema"), ("creavit klozet", "creavit klozet"), ("kale klozet", "kale klozet")]
tbl2 = tablo([th("Tohum ifade", "Seed phrase", "Kategori veya rakip marka ile başlayan ifade.", "Phrase starting with a category or competitor brand."),
              th("Autocomplete önerileri", "Autocomplete suggestions", "Google'ın döndürdüğü ilk 10 tamamlama önerisi.", "First 10 completion suggestions Google returns.")],
             [satir(t, e) for t, e in TOHUM2], "uzun")
T_EN = {"Ürün": "Product", "Fiyat": "Price", "Tamir ve bakım": "Repair and maintenance", "Tasarım": "Design", "Montaj": "Installation", "Ölçü ve teknik": "Dimensions and technical", "Bayi ve mağaza": "Dealer and store", "Seçim": "Selection"}
attot = sum(AT.values())
tema_rows = [[x(t, T_EN[t]), cell(v), n(yzd(100 * v / attot))] for t, v in sorted(AT.items(), key=lambda i: -i[1])]
tbl3 = tablo([th("Öneri teması", "Suggestion theme", "Önerinin ifade kalıbına göre sınıfı.", "Class of the suggestion by phrase pattern."),
              th("Öneri", "Suggestions", "49 tohum ifadeden dönen toplam öneri sayısı.", "Total number of suggestions returned for 49 seed phrases.", True),
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
 x("Google'ın arama kutusunda önerdiği tamamlamalar, gerçek kullanıcı aramalarından türetildiği için markadan ne beklendiğini en doğrudan gösteren kaynaklardan biridir. 49 tohum ifade için Türkiye, Türkçe, masaüstü Chrome sonuçları alınmıştır.",
   "The completions Google suggests in the search box are derived from real user searches, which makes them one of the most direct sources for what is expected of the brand. Results were collected for 49 seed phrases for Turkey, Turkish, desktop Chrome."),
 metric("Tamir ve bakım önerileri", "Repair and maintenance suggestions", yzd(100 * AT["Tamir ve bakım"] / attot), "Tüm önerilerin payı; \"iç takımı\", \"şamandıra\", \"su kaçırıyor\", \"menteşe\"", "Share of all suggestions; \"inner mechanism\", \"float valve\", \"leaking\", \"hinge\""),
 metric("Fiyat önerileri", "Price suggestions", yzd(100 * AT["Fiyat"] / attot), "\"fiyatları\" ile biten ve perakendeci adı taşıyan öneriler", "Suggestions ending in \"prices\" and carrying a retailer name"),
 metric("Montaj önerileri", "Installation suggestions", yzd(100 * AT["Montaj"] / attot), "\"montajı\", \"montaj aparatı\", \"montaj ücreti\", \"taktırma\"", "\"installation\", \"fitting kit\", \"installation fee\", \"having it fitted\""),
 metric("Perakendeci adı geçen öneri", "Suggestions naming a retailer", "%d" % (kocs + tek), "Koçtaş %d, Tekzen %d: kullanıcı VitrA ürününü yapı marketten almayı da düşünmektedir" % (kocs, tek), "Koçtaş %d, Tekzen %d: the user also considers buying the VitrA product from a DIY store" % (kocs, tek)),
 x("\"vitra\" ile başlayan aramalar", "Searches starting with \"vitra\""),
 tbl,
 insight("\"vitra klozet\" önerilerinde fiyat, kapak, model ve takım aramalarının yanında \"iç takımı\", \"su kaçırıyor\", \"şamandırası\" ve \"kapağı menteşesi\" yer almaktadır; \"vitra gömme rezervuar\" önerilerinin çoğunluğu iç takım, şamandıra, conta ve boşaltma grubu gibi yedek parça ifadeleridir. Mevcut ürün sahibinin markadan beklediği ilk şey yedek parça ve çözümdür; \"vitra servis\" önerileri ise ücret, numara, en yakın ve randevu ile servis sürecine ilişkin belirsizliği göstermektedir. \"vitra taksit\" tohumu \"taksit seçenekleri\", \"kaç taksit\", \"9 taksit\" ve \"kredi kartı taksit\" önerilerini getirmektedir. Sitede üst bantta \"vade farksız 6 ay taksit\", Banyo Asistanı'nda \"9 taksit\" mesajı yer aldığından, kullanıcının aradığı taksit sayısının tek ve net bir mesajla verilmesi fayda sağlayabilir.",
         "The \"vitra klozet\" suggestions include \"inner mechanism\", \"leaking\", \"float valve\" and \"seat hinge\" alongside price, seat, model and set searches; most \"vitra gömme rezervuar\" suggestions are spare-part phrases such as inner mechanism, float valve, gasket and flush valve. The first thing the existing owner expects from the brand is a spare part and a solution; the \"vitra servis\" suggestions (fee, number, nearest, appointment) show uncertainty about the service process. The \"vitra taksit\" seed brings \"instalment options\", \"how many instalments\", \"9 instalments\" and \"credit card instalment\". Since the site shows \"6 months interest-free\" in the top banner and \"9 instalments\" in the Bathroom Assistant, giving the instalment count users search for in a single, clear message can be beneficial.", "D3"),
 x("Kategori ve rakip marka aramaları", "Category and competitor brand searches"),
 tbl2,
 insight("Kategori tohumlarında \"klozet montaj ücreti\", \"klozet taktırma fiyatı\", \"klozet montaj aparatı koçtaş\" gibi öneriler, ürünle birlikte montaj hizmetinin de arandığını göstermektedir; \"klozet taksit\" tohumu doğrudan \"taktırma\" önerisine dönüşmektedir. Rakip tohumlarında (Creavit, Kale) öneri profili VitrA ile aynıdır: kapak, menteşe, iç takım, şamandıra, montaj. Yedek parça ve montaj ihtiyacı markadan bağımsız bir kategori davranışıdır ve bu ihtiyacı ilk karşılayan marka için sadakat ve tekrar satış fırsatı taşımaktadır.",
         "In the category seeds, suggestions such as \"klozet montaj ücreti\" (WC installation fee), \"klozet taktırma fiyatı\" (price for having a WC fitted) and \"klozet montaj aparatı koçtaş\" show that the installation service is searched for together with the product; the \"klozet taksit\" seed turns directly into a \"having it fitted\" suggestion. In the competitor seeds (Creavit, Kale) the suggestion profile is the same as VitrA's: seat, hinge, inner mechanism, float valve, installation. The spare-part and installation need is a category behaviour independent of the brand and carries a loyalty and repeat-sale opportunity for the first brand that meets it.", "D3"),
 x("Öneri temaları", "Suggestion themes"), tbl3,
 x("En çok tık getiren sorgular · Search Console", "Queries bringing most clicks · Search Console"), tbl4,
 kaynak("Google Autocomplete · 49 tohum ifade · Türkiye, Türkçe, masaüstü Chrome · %s · Google Search Console sorgu raporu" % veri.TARIH,
        "Google Autocomplete · 49 seed phrases · Turkey, Turkish, desktop Chrome · %s · Google Search Console query report" % veri.TARIH, "D3", "D2"),
)
