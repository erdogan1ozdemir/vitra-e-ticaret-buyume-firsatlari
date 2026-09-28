# -*- coding: utf-8 -*-
"""Bolum: YouTube - montaj, tamir ve karar videolari."""
from ortak import *
from rapor_parca1 import T
Y = A["yt"]; YK = A["yt_kanal"]
GRUP = [("Marka aramaları", "Brand searches", ["vitra klozet", "vitra gömme rezervuar", "vitra akıllı klozet", "vitra v care", "vitra lavabo", "vitra banyo dolabı montajı"]),
        ("Marka + tamir", "Brand + repair", ["vitra gömme klozet su kaçırıyor", "vitra rezervuar tamiri"]),
        ("Montaj", "Installation", ["klozet montajı nasıl yapılır", "asma klozet montajı", "gömme rezervuar montajı", "klozet kapağı montajı", "klozet kapağı nasıl değiştirilir", "lavabo bataryası montajı", "banyo bataryası nasıl takılır", "banyo dolabı montajı", "duşakabin montajı", "duş seti montajı"]),
        ("Tamir", "Repair", ["gömme rezervuar tamiri", "rezervuar su kaçırıyor", "klozet su kaçırıyor", "klozet tıkanıklığı nasıl açılır"]),
        ("Karar ve ilham", "Decision and inspiration", ["en iyi klozet markası", "klozet alırken nelere dikkat", "akıllı klozet inceleme", "banyo dolabı tavsiye", "banyo dolabı inceleme", "banyo yenileme", "banyo tadilatı", "küçük banyo dekorasyonu"])]
def vid(t):
    b, kanal, g, url, yayin, sira = t
    return '%s <span class="pay">%s</span>' % (u(url, b[:60] + ("…" if len(b) > 60 else "")), veri_m("(%s · %s)" % (" ".join(kanal.split()), k(g or 0))))
rows = []
for gtr, gen, qs in GRUP:
    for q in qs:
        v = Y[q]; vr = v["vitra"]
        rows.append([x(gtr, gen), veri_m(q), cell(v["n"]), cell(v["toplam_g"]), n(x("%s" % (", ".join(str(i) for i in vr[:6]) + ("…" if len(vr) > 6 else "")) if vr else "-", "%s" % (", ".join(str(i) for i in vr[:6]) + ("…" if len(vr) > 6 else "")) if vr else "-")), vid(v["top"][0])])
tbl = tablo([th("Grup", "Group", "Aramanın niyet grubu.", "Intent group of the search."),
             th("YouTube araması", "YouTube search", "YouTube arama kutusuna yazılan ifade; Türkiye.", "Phrase typed into the YouTube search box; Turkey."),
             th("Sonuç", "Results", "Alınan video sayısı (ilk sayfa).", "Number of videos retrieved (first page).", True),
             th("Toplam izlenme", "Total views", "İlk sayfadaki videoların toplam izlenmesi; kategorideki ilgiyi gösterir.", "Total views of the first-page videos; indicates interest in the category.", True),
             th("VitrA kanalı sırası", "VitrA channel positions", "VitrA Türkiye veya VitrA Bathrooms kanalına ait videoların sonuçtaki sıraları; \"-\" hiç yok demektir.", "Positions of videos belonging to the VitrA Türkiye or VitrA Bathrooms channel; \"-\" means none.", True),
             th("1. sıradaki video", "Video ranked 1st", "İlk sonuç, kanal ve izlenme.", "First result, channel and views.")], rows, "uzun")
ktot_v = sum(v for _, _, v in YK)
rows2 = [[veri_m(kanal), cell(n_), cell(v)] for kanal, n_, v in YK[:12]]
tbl2 = tablo([th("Kanal", "Channel", "YouTube kanalı.", "YouTube channel."),
              th("Sonuçtaki video", "Videos in results", "30 aramanın ilk sayfalarında görünen video sayısı.", "Number of videos appearing on the first pages of the 30 searches.", True),
              th("Toplam izlenme", "Total views", "Bu videoların toplam izlenmesi.", "Total views of these videos.", True)], rows2, "dar")
macit = Y["vitra gömme klozet su kaçırıyor"]["top"][0]
HTML = """
<p class="lede">%s</p>
<div class="metrics">%s%s%s%s</div>
%s
<h3>%s</h3>
%s
%s
<div class="split">
<div>%s%s</div>
%s
</div>
%s
""" % (
 x("YouTube, montaj ve tamir gibi \"nasıl yapılır\" ihtiyaçlarında Google aramasının önüne geçen bir kanaldır. 30 arama ifadesi için Türkiye sonuçlarının ilk sayfası alınmış; VitrA kanalının hangi aramalarda görünür olduğu ve kimlerin görünür olduğu incelenmiştir.",
   "YouTube is a channel that overtakes Google search for \"how to\" needs such as installation and repair. The first page of Turkey results was collected for 30 search phrases; which searches the VitrA channel is visible in, and who else is visible, were examined."),
 metric("VitrA Türkiye kanalı", "VitrA Türkiye channel", "%d" % YK[0][1], "30 aramanın ilk sayfalarında %d video, %s izlenme; kategoride en görünür kanal" % (YK[0][1], k(YK[0][2])), "%d videos on the first pages of 30 searches, %s views; the most visible channel in the category" % (YK[0][1], k(YK[0][2]))),
 metric("Tamir aramalarında VitrA", "VitrA in repair searches", "0", "\"rezervuar su kaçırıyor\", \"klozet su kaçırıyor\", \"gömme rezervuar tamiri\", \"klozet tıkanıklığı\": VitrA videosu yok", "\"cistern leaking\", \"WC leaking\", \"concealed cistern repair\", \"WC blockage\": no VitrA video"),
 metric("Tamir aramalarının toplam izlenmesi", "Total views of repair searches", k(sum(Y[q]["toplam_g"] for q in GRUP[3][2] + GRUP[1][2])), "Altı tamir aramasının ilk sayfalarındaki videoların toplam izlenmesi", "Total views of first-page videos across six repair searches"),
 metric("\"vitra gömme klozet su kaçırıyor\"", "\"vitra gömme klozet su kaçırıyor\"", k(macit[2]), "1. sıra %s; VitrA kanalı 20. sırada" % macit[1], "1st place %s; VitrA channel at 20th" % macit[1]),
 tbl,
 x("Kimler görünür?", "Who is visible?"),
 tbl2,
 insight("VitrA Türkiye, marka ve montaj aramalarında güçlü konumdadır: \"vitra klozet\" sonuçlarının 12'si, \"vitra v care\" sonuçlarının 11'i, \"klozet kapağı montajı\" ve \"lavabo bataryası montajı\" aramalarının ilk sırası VitrA kanalına aittir. Tamir aramalarında ise tablo tersine dönmektedir: dört jenerik tamir aramasında VitrA videosu bulunmamakta, \"vitra rezervuar tamiri\" gibi marka + tamir aramasında bile ilk sayfada VitrA yer almamaktadır. Bu aramaları Macit Tesisat, Tesisat Servisim, Tesisatçı Genç ve Yaşar Alanoğlu gibi bağımsız tesisatçı kanalları karşılamaktadır.",
         "VitrA Türkiye holds a strong position in brand and installation searches: 12 of the \"vitra klozet\" results, 11 of the \"vitra v care\" results, and first place for \"klozet kapağı montajı\" and \"lavabo bataryası montajı\" belong to the VitrA channel. In repair searches the picture reverses: there is no VitrA video in four generic repair searches, and even in a brand + repair search such as \"vitra rezervuar tamiri\" VitrA is absent from the first page. Independent installer channels such as Macit Tesisat, Tesisat Servisim, Tesisatçı Genç and Yaşar Alanoğlu answer these searches.", "D4"),
 h3("Macit Tesisat örneği", "The Macit Tesisat example"),
 p("\"vitra gömme klozet su kaçırıyor\" aramasında ilk sırada yer alan \"%s\" videosu %s izlenmeye ulaşmıştır; aynı ifade Search Console'da \"gömme klozet su kaçırıyorsa çok basit tamiri\" sorgusu olarak vitra.com.tr'ye de tık getirmektedir. Video, bir VitrA ürününün tamirini anlatmakta ve markanın kendi kanalında karşılığı bulunmamaktadır. Bu tür kanallarla iş birliği (ürün sağlama, yedek parça bağlantısı, açıklamaya vitra.com.tr yedek parça sayfası eklenmesi) ve markanın kendi tamir serisini üretmesi birlikte değerlendirilebilir." % (macit[0], k(macit[2])),
   "The video \"%s\", ranked first for \"vitra gömme klozet su kaçırıyor\", has reached %s views; the same phrase also brings clicks to vitra.com.tr in Search Console as the query \"gömme klozet su kaçırıyorsa çok basit tamiri\". The video explains the repair of a VitrA product and has no counterpart on the brand's own channel. Collaboration with such channels (supplying products, spare-part links, adding the vitra.com.tr spare-part page to the description) and the brand producing its own repair series can be considered together." % (macit[0], k(macit[2])), "Y1", "D2"),
 box("ÖNERİ", "RECOMMENDATION", marks([("up", "Tamir serisi: rezervuar, iç takım, şamandıra, klozet kapağı, sifon için 3-5 dakikalık kısa videolar; her video açıklamasında yedek parça sayfası bağlantısı", "Repair series: 3-5 minute short videos for cistern, inner mechanism, float valve, WC seat, siphon; a spare-part page link in every description"),
                                       ("up", "Tesisatçı kanallarıyla iş birliği: ürün ve parça sağlama, video açıklamasında satın alma bağlantısı", "Collaboration with installer channels: supplying products and parts, purchase link in the video description"),
                                       ("at", "Montaj videolarında ürün sayfasına yönlendirme eksik; mevcut 71 videonun açıklamaları gözden geçirilebilir", "Redirection to the product page is missing in installation videos; the descriptions of the existing 71 videos can be reviewed"),
                                       ("at", "\"en iyi klozet markası\" aramasında VitrA 1. sırada (%s izlenme); bu videonun satın alma sayfasına bağlanması değerlendirilebilir" % k(Y["en iyi klozet markası"]["top"][0][2]), "VitrA ranks 1st for \"en iyi klozet markası\" (%s views); linking this video to the purchase page can be considered" % k(Y["en iyi klozet markası"]["top"][0][2]))])),
 kaynak("YouTube arama sonuçları · 30 ifade · Türkiye · ilk sayfa · %s" % veri.TARIH, "YouTube search results · 30 phrases · Turkey · first page · %s" % veri.TARIH, "D4"),
)
