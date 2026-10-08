# -*- coding: utf-8 -*-
"""Bolum: YouTube - montaj, tamir ve karar videolari."""
from ortak import *
def _sira_en(n_): return "%d%s" % (n_, "th" if 11 <= n_ % 100 <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(n_ % 10, "th"))
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
        rows.append([etk(gtr, gen), veri_m(q), cell(v["n"]), cell(v["toplam_g"]), n(x("%s" % (", ".join(str(i) for i in vr[:6]) + ("…" if len(vr) > 6 else "")) if vr else "-", "%s" % (", ".join(str(i) for i in vr[:6]) + ("…" if len(vr) > 6 else "")) if vr else "-")), vid(v["top"][0])])
tbl = tablo([th("Grup", "Group", "Aramanın niyet grubu.", "Intent group of the search."),
             th("YouTube araması", "YouTube search", "YouTube arama kutusuna yazılan ifade; Türkiye.", "Phrase typed into the YouTube search box; Turkey."),
             th("Sonuç", "Results", "Alınan video sayısı (ilk sayfa).", "Number of videos retrieved (first page).", True),
             th("Toplam izlenme", "Total views", "İlk sayfadaki videoların toplam izlenmesi; kategorideki ilgiyi gösterir.", "Total views of the first-page videos; indicates interest in the category.", True),
             th("VitrA kanalı sırası", "VitrA channel positions", "VitrA Türkiye veya VitrA Bathrooms kanalına ait videoların sonuçtaki sıraları; \"-\" hiç yok demektir.", "Positions of videos belonging to the VitrA Türkiye or VitrA Bathrooms channel; \"-\" means none.", True),
             th("1. sıradaki video", "Video ranked 1st", "İlk sonuç, kanal ve izlenme.", "First result, channel and views.")], rows, "uzun")
import json as _json, os as _os
_AH = _json.load(open(_os.path.join(veri.V, "ham", "autocomplete_hacim.json"), encoding="utf-8"))["kelime"]
prow = []
for gtr, gen, qs in GRUP:
    for q in qs:
        v = Y[q]; vr = v["vitra"]; h = (_AH.get(q) or {}).get("ort2026"); tp = v["top"][0] if v.get("top") else None
        prow.append([kw(q), etk(gtr, gen), cell(round(h)) if h else n("-"), cell(v["n"]), cell(v["toplam_g"]), n(", ".join(str(i) for i in vr[:6]) if vr else "-"),
                     veri_m(" ".join(tp[1].split()) if tp else "-"), cell(tp[2] or 0) if tp else n("-")])
_PT = tablo([th("Arama ifadesi", "Search phrase", "YouTube'da aranan ifade.", "Phrase searched on YouTube."), th("Grup", "Group", "Aramanın niyet grubu.", "Intent group of the search."),
             th("Google aylık hacim", "Google monthly volume", "Aynı ifadenin Google'daki Ocak - Ağustos 2026 aylık ortalama arama hacmi (Google Ads); \"-\" hacim dönmedi.", "Average monthly Google search volume for the same phrase, January - August 2026 (Google Ads); \"-\" no volume returned.", True),
             th("YouTube sonuç", "YouTube results", "İlk sayfadaki video sayısı.", "Videos on the first page.", True), th("Toplam izlenme", "Total views", "İlk sayfadaki videoların toplam izlenmesi.", "Total views of first-page videos.", True),
             th("VitrA kanalı sırası", "VitrA channel positions", "VitrA videolarının sonuçtaki sıraları; \"-\" yok.", "Positions of VitrA videos in the results; \"-\" none.", True),
             th("1. sıradaki kanal", "Channel ranked 1st", "İlk sonucun kanalı.", "Channel of the first result."), th("1. video izlenme", "1st video views", "İlk sonucun izlenmesi.", "Views of the first result.", True)], prow, "uzun")
_POP30, _DIA30 = pop("30 YouTube arama ifadesi: Google hacmi, izlenme ve VitrA'nın yeri", "30 YouTube search phrases: Google volume, views and VitrA's place", _PT, "30 arama ifadesini gör", "See the 30 search phrases")
ktot_v = sum(v for _, _, v in YK)
rows2 = [[veri_m(kanal), cell(n_), cell(v)] for kanal, n_, v in YK[:12]]
tbl2 = tablo([th("Kanal", "Channel", "YouTube kanalı.", "YouTube channel."),
              th("Sonuçtaki video", "Videos in results", "30 aramanın ilk sayfalarında görünen tekil video sayısı; birden fazla aramada çıkan video bir kez sayılmıştır.", "Number of unique videos on the first pages of the 30 searches; a video appearing in several searches is counted once.", True),
              th("Toplam izlenme", "Total views", "Bu tekil videoların toplam izlenmesi.", "Total views of these unique videos.", True)], rows2, "dar")
macit = Y["vitra gömme klozet su kaçırıyor"]["top"][0]
_VT = next(t for t in YK if t[0] == "VitrA Türkiye"); _VB = next((t for t in YK if t[0] == "VitrA Bathrooms"), ("", 0, 0))
_TG = {}
for q in GRUP[3][2]: _TG.update(Y[q]["g"])
_tamir_g = sum(_TG.values())
_vk, _vv = len(Y["vitra klozet"]["vitra"]), len(Y["vitra v care"]["vitra"])
HTML = """
<p class="lede">%s</p>
<p class="popl">%s</p>
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
 x("YouTube, montaj ve tamir gibi \"nasıl yapılır\" ihtiyaçlarında sık başvurulan bir kanaldır. 30 arama ifadesi için Türkiye sonuçlarının ilk sayfası alınmış; VitrA kanalının hangi aramalarda görünür olduğu ve kimlerin görünür olduğu incelenmiştir.",
   "YouTube is a frequently used channel for \"how to\" needs such as installation and repair. The first page of Turkey results was collected for 30 search phrases; which searches the VitrA channel is visible in, and who else is visible, were examined."),
 _POP30,
 metric("VitrA Türkiye kanalı", "VitrA Türkiye channel", "%d" % _VT[1], "30 aramanın ilk sayfalarında %d tekil video, %s izlenme; kategoride en görünür kanal" % (_VT[1], k(_VT[2])), "%d unique videos on the first pages of 30 searches, %s views; the most visible channel in the category" % (_VT[1], k(_VT[2]))),
 metric("Tamir aramalarında VitrA", "VitrA in repair searches", "0", "\"rezervuar su kaçırıyor\", \"klozet su kaçırıyor\", \"gömme rezervuar tamiri\", \"klozet tıkanıklığı\": VitrA videosu yok", "\"cistern leaking\", \"WC leaking\", \"concealed cistern repair\", \"WC blockage\": no VitrA video"),
 metric("Tamir aramalarının toplam izlenmesi", "Total views of repair searches", k(_tamir_g), "Aynı dört jenerik tamir aramasının ilk sayfalarındaki %d tekil videonun toplam izlenmesi" % len(_TG), "Total views of the %d unique first-page videos across the same four generic repair searches" % len(_TG)),
 metric("\"vitra gömme klozet su kaçırıyor\"", "\"vitra gömme klozet su kaçırıyor\"", k(macit[2]), "1. sıra %s; VitrA kanalı %d. sırada (%d video içinde)" % (macit[1], Y["vitra gömme klozet su kaçırıyor"]["vitra"][0], Y["vitra gömme klozet su kaçırıyor"]["n"]), "1st place %s; VitrA channel %s of %d videos" % (macit[1], _sira_en(Y["vitra gömme klozet su kaçırıyor"]["vitra"][0]), Y["vitra gömme klozet su kaçırıyor"]["n"])),
 tbl,
 x("Kimler görünür?", "Who is visible?"),
 tbl2,
 insight("VitrA kanalları (VitrA Türkiye ve VitrA Bathrooms) marka ve montaj aramalarında güçlü konumdadır: \"vitra klozet\" sonuçlarının %d'si, \"vitra v care\" sonuçlarının %d'i, \"klozet kapağı montajı\" ve \"lavabo bataryası montajı\" aramalarının ilk sırası VitrA kanalına aittir. Tamir aramalarında ise tablo tersine dönmektedir: dört jenerik tamir aramasında VitrA videosu bulunmamakta, \"vitra rezervuar tamiri\" gibi marka + tamir aramasında bile ilk sayfada VitrA yer almamaktadır. Bu aramaları Macit Tesisat, Tesisat Servisim, Tesisatçı Genç ve Yaşar Alanoğlu gibi bağımsız tesisatçı kanalları karşılamaktadır." % (_vk, _vv),
         "The VitrA channels (VitrA Türkiye and VitrA Bathrooms) hold a strong position in brand and installation searches: %d of the \"vitra klozet\" results, %d of the \"vitra v care\" results, and first place for \"klozet kapağı montajı\" and \"lavabo bataryası montajı\" belong to the VitrA channel. In repair searches the picture reverses: there is no VitrA video in four generic repair searches, and even in a brand + repair search such as \"vitra rezervuar tamiri\" VitrA is absent from the first page. Independent installer channels such as Macit Tesisat, Tesisat Servisim, Tesisatçı Genç and Yaşar Alanoğlu answer these searches." % (_vk, _vv), "D4"),
 h3("Macit Tesisat örneği", "The Macit Tesisat example"),
 p("\"vitra gömme klozet su kaçırıyor\" aramasında ilk sırada yer alan \"%s\" videosu %s izlenmeye ulaşmıştır; benzer bir ifade Search Console'da \"gömme klozet su kaçırıyorsa çok basit tamiri\" sorgusu olarak vitra.com.tr'ye de tık getirmektedir. Video, bir VitrA ürününün tamirini anlatmakta ve markanın kendi kanalında karşılığı bulunmamaktadır. Bu tür kanallarla iş birliği (ürün sağlama, yedek parça bağlantısı, açıklamaya açılması önerilen yedek parça kategorisinin bağlantısının eklenmesi) ve markanın kendi tamir serisini üretmesi birlikte değerlendirilebilir." % (macit[0], k(macit[2])),
   "The video \"%s\", ranked first for \"vitra gömme klozet su kaçırıyor\", has reached %s views; a similar phrase also brings clicks to vitra.com.tr in Search Console as the query \"gömme klozet su kaçırıyorsa çok basit tamiri\". The video explains the repair of a VitrA product and has no counterpart on the brand's own channel. Collaboration with such channels (supplying products, spare-part links, adding a link to the proposed spare-parts category to the description) and the brand producing its own repair series can be considered together." % (macit[0], k(macit[2])), "Y1", "D2"),
 box("ÖNERİ", "RECOMMENDATION", marks([("up", "Tamir serisi: rezervuar, iç takım, şamandıra, klozet kapağı, sifon için 3-5 dakikalık kısa videolar; her video açıklamasında açılması önerilen yedek parça kategorisine bağlantı (Bölüm [[b:adimlar]])", "Repair series: 3-5 minute short videos for cistern, inner mechanism, float valve, WC seat, siphon; a link to the proposed spare-parts category in every description (Section [[b:adimlar]])"),
                                       ("up", "Tesisatçı kanallarıyla iş birliği: ürün ve parça sağlama, video açıklamasında satın alma bağlantısı", "Collaboration with installer channels: supplying products and parts, purchase link in the video description"),
                                       ("up", "Sonuçlarda görünen %d VitrA videosunun açıklamalarında ürün, montaj hizmeti ve yedek parça bağlantısı bulunup bulunmadığı gözden geçirilebilir" % (_VT[1] + _VB[1]), "The descriptions of the %d VitrA videos appearing in the results can be reviewed for product, installation service and spare-part links" % (_VT[1] + _VB[1])),
                                       ("up", "\"en iyi klozet markası\" aramasında VitrA 1. sırada (%s izlenme); bu videonun satın alma sayfasına bağlanması değerlendirilebilir" % k(Y["en iyi klozet markası"]["top"][0][2]), "VitrA ranks 1st for \"en iyi klozet markası\" (%s views); linking this video to the purchase page can be considered" % k(Y["en iyi klozet markası"]["top"][0][2]))])),
 kaynak("YouTube arama sonuçları · 30 ifade · Türkiye · ilk sayfa · %s" % veri.TARIH, "YouTube search results · 30 phrases · Turkey · first page · %s" % veri.TARIH, "D4"),
) + _DIA30

from b_youtube_derin import EK as _EK
HTML = HTML + _EK
