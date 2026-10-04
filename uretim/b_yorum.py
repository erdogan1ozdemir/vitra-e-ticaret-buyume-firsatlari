# -*- coding: utf-8 -*-
"""Bolum: Pazaryeri yorumlari ve soru-cevap · sentiment, pain point, rakip karsilastirmasi (Trendyol + Hepsiburada)."""
from ortak import *
from ortak import _J
from grafik2 import yigin
from yorum_tema import YAD, SAD

A = _J("islenmis", "yorum_analiz.json")
M, S, TOP = A["marka"], A["soru"], A["toplam"]
VG, RK = A["vg"], A["rakip"]
K = A["kumeler"]
RAK = [m for m in K if m not in ("VitrA", "Artema", "Diğer markalar")]
ALT = "yorum-soru-seti.html"
for _m in K: x(_m, _m if _m != "Diğer markalar" else "Other brands")
for _k, (_t, _e) in list(YAD.items()) + list(SAD.items()): x(_t, _e)


def alt_btn(tr="Pazaryeri Yorumları sayfasını görüntüle", en="View the Marketplace Reviews page", hedef=""):
    return '<a class="popb altb" href="%s%s" target="_blank" rel="noopener">%s <span aria-hidden="true">↗</span></a>' % (ALT, hedef, x(tr, en))


def tn(m, t): return M[m]["tema_neg"].get(t) or 0
def tp(prof, t): return dict((k, r) for k, _, r in prof["guclu"]).get(t) or 0
def yd(v): return yzd(v or 0)
def ye(v): return ("%.1f" % (v or 0)) + "%"
def ad(m): return m if m != "Diğer markalar" else x("Diğer markalar", "Other brands")
def tad(t): return x(*YAD[t])
def sad(t): return x(*SAD[t])

# ---------------------------------------------------------------- duygu dagilimi grafigi
_sira = ["VitrA", "Artema"] + sorted(RAK, key=lambda m: M[m]["olumsuz"] or 0) + ["Diğer markalar"]
GD = yigin([(ad(m), [M[m]["olumlu"] or 0, M[m]["notr"] or 0, M[m]["olumsuz"] or 0]) for m in _sira],
           [(x("Olumlu (4-5)", "Positive (4-5)"), "#9CCFC5"), (x("Nötr (3)", "Neutral (3)"), "#B8A48F"), (x("Olumsuz (1-2)", "Negative (1-2)"), "#E85F36")],
           x("Puana göre yorum dağılımı (%100) · marka bazında · Trendyol ve Hepsiburada", "Distribution of reviews by rating (100%) · by brand · Trendyol and Hepsiburada"), sol=120, bh=22, ara=8)

# ---------------------------------------------------------------- marka tablosu
def _mrow(m):
    p = M[m]; s = S[m]
    def _j(l):
        return x(", ".join("%s (%s)" % (YAD[t][0], yzd(r, 0)) for t, _, r in l), ", ".join("%s (%d%%)" % (YAD[t][1], round(r)) for t, _, r in l)) if l else "-"
    pain = _j(p["pain"][:2]) if p["olumsuz_metinli"] >= 15 else "-"
    guc = _j(p["guclu"][:2])
    return [("<b>%s</b>" % ad(m)) if m in ("VitrA", "Artema") else ad(m), cell(p["n"]), cell(p["metinli"]), n(f1(p["ort_puan"])),
            n(yzd(p["olumlu"])), n(yzd(p["olumsuz"])), pain, guc, cell(s["n"])]
TM = tablo([th("Marka", "Brand", "Değerlendirme kaydı bulunan marka; rakipler arasında metinli yorumu 40 ve üzeri olanlar ayrı, diğerleri tek kümede gösterilmiştir.", "Brand with review records; competitors with 40 or more text reviews are shown separately, the rest in one cluster."),
            th("Yorum sayısı", "Reviews", "Trendyol ve Hepsiburada ürün sayfalarındaki toplam değerlendirme (puanlı).", "Total rated reviews on Trendyol and Hepsiburada product pages.", True),
            th("Metinli", "With text", "Yorum metni bulunan değerlendirme sayısı; tema analizi bu kayıtlarla yapılmıştır.", "Number of reviews with text; theme analysis uses these records.", True),
            th("Ort. puan", "Avg. rating", "1-5 puan ortalaması.", "Average of 1-5 ratings.", True),
            th("Olumlu", "Positive", "4-5 puanlı yorum payı.", "Share of 4-5 star reviews.", True),
            th("Olumsuz", "Negative", "1-2 puanlı yorum payı.", "Share of 1-2 star reviews.", True),
            th("En sık pain point", "Top pain points", "Olumsuz metinli yorumlarda en sık geçen iki tema ve bu yorumlardaki payı; olumsuz metinli yorumu 15'in altındaysa boş bırakılmıştır.", "The two themes most often mentioned in negative text reviews and their share; blank if there are fewer than 15 negative text reviews."),
            th("Öne çıkan güçlü yön", "Top strengths", "Olumlu metinli yorumlarda en sık geçen iki tema ve bu yorumlardaki payı.", "The two themes most often mentioned in positive text reviews and their share."),
            th("Soru", "Questions", "Ürün sayfalarındaki soru-cevap kaydı sayısı.", "Number of Q&A records on product pages.", True)],
           [_mrow(m) for m in _sira], "sorusut")

# ---------------------------------------------------------------- pain point profili
_tema = sorted(YAD, key=lambda t: -(VG["tema_neg"].get(t) or 0))
def _trow(t):
    v, a, r = M["VitrA"]["tema_neg"].get(t) or 0, M["Artema"]["tema_neg"].get(t) or 0, RK["tema_neg"].get(t) or 0
    fark = v - r
    fs = ("+" if fark > 0.05 else ("-" if fark < -0.05 else "")) + f1(abs(fark))
    return [tad(t), n(yzd(v)), n(yzd(a)), n(yzd(r)), n('<span class="%s">%s</span>' % ("dn" if fark > 3 else ("up" if fark < -3 else ""), fs))]
TP = tablo([th("Yorum teması", "Review theme", "Yorum metnine anahtar ifade kurallarıyla atanan konu; bir yorum birden fazla temaya girebilir.", "Topic assigned to the review text with key phrase rules; a review may fall into more than one theme."),
            th("VitrA", "VitrA", "VitrA'nın olumsuz (1-2 puan) metinli yorumlarından ilgili temaya değinenlerin payı.", "Share of VitrA's negative (1-2 star) text reviews that mention the theme.", True),
            th("Artema", "Artema", "Artema'nın olumsuz metinli yorumlarından ilgili temaya değinenlerin payı.", "Share of Artema's negative text reviews that mention the theme.", True),
            th("Rakipler", "Competitors", "VitrA ve Artema dışındaki tüm markaların olumsuz metinli yorumlarında ilgili temanın payı.", "Share of the theme in negative text reviews of all brands other than VitrA and Artema.", True),
            th("VitrA - rakip farkı", "VitrA - competitor gap", "VitrA payı ile rakip payı arasındaki fark, yüzde puan; kırmızı VitrA'nın daha sık şikayet aldığı temaları gösterir.", "Difference between the VitrA and competitor shares, in percentage points; red marks themes where VitrA receives more complaints.", True)],
           [_trow(t) for t in _tema])

# ---------------------------------------------------------------- urun grubu karsilastirmasi
def _grow(g):
    a, b = g["vitra"], g["rakip"]
    pa = tad(a["pain"][0][0]) if a["pain"] and a["olumsuz_metinli"] >= 5 else "-"
    pb = tad(b["pain"][0][0]) if b["pain"] and b["olumsuz_metinli"] >= 5 else "-"
    fark = (a["olumsuz"] or 0) - (b["olumsuz"] or 0)
    return [x(g["grup"], GEN.get(g["grup"], g["grup"])), cell(a["metinli"]), n('<span class="%s">%s</span>' % ("dn" if fark > 2 else "", yzd(a["olumsuz"]))), pa, cell(b["metinli"]), n(yzd(b["olumsuz"])), pb]
GEN = {"Klozet kapağı": "Toilet seat", "Rezervuar ve iç takım": "Cistern and inner mechanism", "Banyo dolabı": "Bathroom cabinet", "Duşakabin": "Shower enclosure", "Lavabo bataryası": "Basin tap",
       "Banyo ve duş bataryası": "Bath and shower mixer", "Eviye bataryası": "Kitchen sink mixer", "Duş seti ve sistemi": "Shower set and system", "Klozet": "WC", "Lavabo": "Washbasin",
       "Ara musluk ve tesisat": "Angle valve and plumbing", "Banyo aksesuarı": "Bathroom accessories", "Diğer": "Other"}
for _g, _e in GEN.items(): x(_g, _e)
GRP = sorted(A["grup"], key=lambda g: -((g["vitra"]["olumsuz"] or 0) - (g["rakip"]["olumsuz"] or 0)))
TG = tablo([th("Ürün grubu", "Product group", "Ürün adından atanan grup; yalnız iki tarafta da en az 25 metinli yorum bulunan gruplar gösterilmiştir.", "Group assigned from the product name; only groups with at least 25 text reviews on both sides are shown."),
            th("VitrA ve Artema metinli yorum", "VitrA and Artema text reviews", "Gruptaki VitrA ve Artema ürünlerinin metinli yorum sayısı.", "Number of text reviews on VitrA and Artema products in the group.", True),
            th("VitrA ve Artema olumsuz", "VitrA and Artema negative", "Gruptaki VitrA ve Artema yorumlarında 1-2 puan payı; rakipten 2 puandan fazla yüksekse kırmızı.", "Share of 1-2 star VitrA and Artema reviews in the group; red if more than 2 points above competitors.", True),
            th("VitrA ve Artema ilk pain point", "VitrA and Artema top pain point", "Gruptaki VitrA ve Artema olumsuz metinli yorumlarında en sık tema.", "Most frequent theme in negative VitrA and Artema text reviews in the group."),
            th("Rakip metinli yorum", "Competitor text reviews", "Gruptaki rakip ürünlerin metinli yorum sayısı.", "Number of text reviews on competitor products in the group.", True),
            th("Rakip olumsuz", "Competitor negative", "Gruptaki rakip yorumlarında 1-2 puan payı.", "Share of 1-2 star competitor reviews in the group.", True),
            th("Rakip ilk pain point", "Competitor top pain point", "Gruptaki rakip olumsuz metinli yorumlarında en sık tema.", "Most frequent theme in negative competitor text reviews in the group.")],
           [_grow(g) for g in GRP])
_ust = [g for g in GRP if (g["vitra"]["olumsuz"] or 0) - (g["rakip"]["olumsuz"] or 0) > 2]
_alt = [g for g in GRP if (g["vitra"]["olumsuz"] or 0) < (g["rakip"]["olumsuz"] or 0)]

# ---------------------------------------------------------------- rakip kartlari
def _kart(m):
    p = M[m]; s = S[m]
    mk = []
    for t, _, r in p["guclu"][:2]:
        if r and r >= 12: mk.append(("up", "%s: olumlu yorumların %s'inde" % (YAD[t][0], yzd(r, 0)), "%s: in %d%% of positive reviews" % (YAD[t][1], round(r))))
    if p["olumsuz_metinli"] >= 15:
        for t, _, r in p["pain"][:2]:
            if r and r >= 12: mk.append(("at", "%s: olumsuz yorumların %s'inde" % (YAD[t][0], yzd(r, 0)), "%s: in %d%% of negative reviews" % (YAD[t][1], round(r))))
    return ('<article class="fnote"><span class="fc">%s</span><h4 class="kh4">%s</h4>%s</article>'
            % (x("%s yorum · ort. %s · olumsuz %s" % (bin(p["n"]), f1(p["ort_puan"]), yzd(p["olumsuz"])), "%s reviews · avg. %s · negative %s" % (f"{p['n']:,}", ("%.1f" % p["ort_puan"]), ye(p["olumsuz"]))),
               m, marks(mk)))
_kartlar = [m for m in RAK if M[m]["metinli"] >= 60][:9]
KARTLAR = '<div class="fnotes">%s</div>' % "".join(_kart(m) for m in _kartlar)

# ---------------------------------------------------------------- rakip pain point'lerinden VitrA'ya
def _en_yuksek(t):
    l = [(m, tn(m, t)) for m in RAK if M[m]["olumsuz_metinli"] >= 20]
    return max(l, key=lambda z: z[1]) if l else (None, 0)
_km, _kv = _en_yuksek("kirik"); _mm, _mv = _en_yuksek("montaj"); _sm, _sv = _en_yuksek("satis_sonrasi")
_bd = next((g for g in A["grup"] if g["grup"] == "Banyo dolabı"), None)
_vs = dict((t, r) for t, _, r in S["VitrA"]["tema"]); _rs = dict((t, r) for t, _, r in A["soru_rakip"]["tema"])
_hbr = S["VitrA"]["kanal_profil"]["Hepsiburada"]["resmi_cevap"] or 0
_ar_hbr = S["Artema"]["kanal_profil"]["Hepsiburada"]["resmi_cevap"] or 0

GELISIM = marks([
    ("at", "Banyo dolabı teslimatı: VitrA ve Artema banyo dolabı yorumlarında olumsuz pay %s, rakiplerde %s'tir; olumsuz yorumların %s'i kırık veya hasarlı ürüne, %s'i iade ve değişim sürecine değinmektedir. Lavabo ve ayna içeren setlerde koruyucu ambalajın güçlendirilmesi ve hasarlı teslimatta değişim sürecinin kısaltılması değerlendirilebilir." % (yd(_bd["vitra"]["olumsuz"]), yd(_bd["rakip"]["olumsuz"]), yd(_bd["vitra"]["tema_neg"].get("kirik")), yd(_bd["vitra"]["tema_neg"].get("satis_sonrasi"))) if _bd else "",
           "Bathroom cabinet delivery: the negative share is %s in VitrA and Artema bathroom cabinet reviews and %s for competitors; %s of negative reviews mention broken or damaged products and %s the return and exchange process. Reinforcing protective packaging for sets containing a washbasin and mirror and shortening the exchange process for damaged deliveries may be considered." % (ye(_bd["vitra"]["olumsuz"]), ye(_bd["rakip"]["olumsuz"]), ye(_bd["vitra"]["tema_neg"].get("kirik")), ye(_bd["vitra"]["tema_neg"].get("satis_sonrasi"))) if _bd else ""),
    ("at", "Uyumluluk bilgisi: VitrA sorularının %s'i uyumluluk ve kullanım yeri, %s'i kutu içeriği, %s'i ölçü üzerinedir. Ürün sayfalarına uyumlu model listesi, ölçü çizimi ve set içeriği tablosu eklenmesi soru yükünü azaltabilir ve karar aşamasını kısaltabilir." % (yd(_vs.get("uyum")), yd(_vs.get("icerik")), yd(_vs.get("olcu"))),
           "Compatibility information: %s of VitrA questions are about compatibility and place of use, %s about box contents and %s about size. Adding a compatible model list, a dimension drawing and a set contents table to product pages may reduce the question load and shorten the decision stage." % (ye(_vs.get("uyum")), ye(_vs.get("icerik")), ye(_vs.get("olcu")))),
    ("at", "Resmi mağaza cevabı: Hepsiburada'da VitrA ürünlerine gelen soruların %s'i, Artema ürünlerine gelenlerin %s'i resmi mağaza tarafından cevaplanmıştır; kalan sorular aynı ürünü satan diğer satıcılarca yanıtlanmaktadır. Resmi mağazanın soru takibini tüm VitrA ve Artema listelerine genişletmesi, ürün bilgisinin tek kaynaktan verilmesini sağlayabilir." % (yd(_hbr), yd(_ar_hbr)),
           "Official store answers: on Hepsiburada, %s of questions on VitrA products and %s on Artema products were answered by the official store; the rest are answered by other sellers of the same product. Extending the official store's question follow-up to all VitrA and Artema listings may ensure product information comes from a single source." % (ye(_hbr), ye(_ar_hbr))),
    ("up", "Montaj desteği: montaj ve kurulum rakiplerde en sık pain point'ler arasındadır (%s'de olumsuz yorumların %s); VitrA'da montaj olumsuz yorumların %s geçmektedir (rakiplerde %s). Montaj videoları ve kurulum kılavuzunun ürün sayfasında görünür kılınması bu konudaki soruları azaltabilir." % (_mm, yzd_ek(_mv or 0, 1, "i"), yzd_ek(M["VitrA"]["tema_neg"].get("montaj") or 0, 1, "inde"), yd(RK["tema_neg"].get("montaj"))),
           "Installation support: installation is among the most frequent pain points at competitors (%s of negative reviews at %s); at VitrA installation appears in %s of negative reviews (competitors %s). Making installation videos and the setup guide visible on the product page can reduce questions on this topic." % (ye(_mv), _mm, ye(M["VitrA"]["tema_neg"].get("montaj")), ye(RK["tema_neg"].get("montaj")))),
    ("at", "Satış sonrası iletişim: iade, değişim ve satıcı iletişimi VitrA'nın olumsuz yorumlarının %s geçmektedir (rakiplerde %s, en yüksek %s'de %s). Resmi mağazada iade ve değişim adımlarının ürün sayfasında açık yazılması ve hasarlı teslimatta hızlı değişim süreci bu payı azaltabilir." % (yzd_ek(M["VitrA"]["tema_neg"].get("satis_sonrasi") or 0, 1, "inde"), yd(RK["tema_neg"].get("satis_sonrasi")), _sm, yd(_sv)),
           "After-sales contact: returns, exchanges and seller contact appear in %s of VitrA's negative reviews (%s at competitors, highest at %s with %s). Stating return and exchange steps clearly on official store product pages and a fast exchange process for damaged deliveries can reduce this share." % (ye(M["VitrA"]["tema_neg"].get("satis_sonrasi")), ye(RK["tema_neg"].get("satis_sonrasi")), _sm, ye(_sv))),
])

# ---------------------------------------------------------------- soru kumeleri
_stema = [k for k in SAD if k != "diger"]
def _srow(t):
    return [sad(t), n(yzd(_vs.get(t))), n(yzd(dict((k, r) for k, _, r in S["Artema"]["tema"]).get(t))), n(yzd(_rs.get(t)))]
TS = tablo([th("Soru teması", "Question theme", "Soru metnine anahtar ifade kurallarıyla atanan konu; bir soru birden fazla temaya girebilir.", "Topic assigned to the question text with key phrase rules; a question may fall into more than one theme."),
            th("VitrA", "VitrA", "VitrA ürünlerine gelen soruların ilgili temaya giren payı.", "Share of questions on VitrA products falling into the theme.", True),
            th("Artema", "Artema", "Artema ürünlerine gelen soruların ilgili temaya giren payı.", "Share of questions on Artema products falling into the theme.", True),
            th("Rakipler", "Competitors", "Rakip ürünlere gelen soruların ilgili temaya giren payı.", "Share of questions on competitor products falling into the theme.", True)],
           [_srow(t) for t in sorted(_stema, key=lambda t: -(_vs.get(t) or 0))], "sorular")

_d0, _d1 = TOP["donem"]
_k_neg = M["VitrA"]["tema_neg"].get("kirik") or 0; _r_neg = RK["tema_neg"].get("kirik") or 0
HTML = """
<p class="lede">%s %s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
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
<p>%s</p>
%s
""" % (
 x("Trendyol ve Hepsiburada'da VitrA, Artema ve rakip markaların ürün sayfalarındaki %s yorum ve %s soru-cevap kaydı incelenmiştir. Yorumlar puana göre olumlu, nötr ve olumsuz olarak ayrılmış, metinler pain point ve güçlü yön temalarına kümelenmiştir. Rakip örneklemi iki pazaryerinde çok satan ve en çok değerlendirilen ürünlerden seçilmiştir; VitrA resmi mağazasının Trendyol panel kayıtları da kapsama dahildir; yorumların %s'i son 12 aya aittir."
   % (bin(TOP["yorum"]), bin(TOP["soru"]), yzd(TOP["son12"], 0)),
   "%s reviews and %s Q&A records on the product pages of VitrA, Artema and competitor brands on Trendyol and Hepsiburada were reviewed. Reviews are split into positive, neutral and negative by rating, and texts are clustered into pain point and strength themes. The competitor sample was selected from best-selling and most-reviewed products on both marketplaces; Trendyol panel records of the VitrA official store are also included; %s of reviews are from the last 12 months."
   % (f"{TOP['yorum']:,}", f"{TOP['soru']:,}", "%d%%" % round(TOP["son12"]))),
 alt_btn(),
 kpi_kart(yzd(M["VitrA"]["olumsuz"]), "VitrA yorumlarında olumsuz pay · Artema %s, rakipler %s" % (yzd(M["Artema"]["olumsuz"]), yzd(RK["olumsuz"])), "Negative share in VitrA reviews · Artema %s, competitors %s" % (ye(M["Artema"]["olumsuz"]), ye(RK["olumsuz"]))),
 kpi_kart(f1(M["VitrA"]["ort_puan"]), "VitrA ortalama puanı · Artema %s · %s yorum" % (f1(M["Artema"]["ort_puan"]), bin(M["VitrA"]["n"])), "VitrA average rating · Artema %s · %s reviews" % ("%.1f" % M["Artema"]["ort_puan"], f"{M['VitrA']['n']:,}")),
 kpi_kart(yzd(_bd["vitra"]["olumsuz"]) if _bd else "-", "Banyo dolabında VitrA ve Artema olumsuz payı · rakipler %s" % (yzd(_bd["rakip"]["olumsuz"]) if _bd else "-"), "VitrA and Artema negative share in bathroom cabinets · competitors %s" % (ye(_bd["rakip"]["olumsuz"]) if _bd else "-")),
 kpi_kart(yzd(_vs.get("uyum")), "VitrA sorularında uyumluluk ve kullanım yeri payı", "Share of compatibility and place of use in VitrA questions"),
 x("Duygu dağılımı: marka bazında", "Sentiment split by brand"),
 GD, TM,
 insight("Olumsuz yorum payı VitrA'da %s, Artema'da %s, rakiplerde %s düzeyindedir (iki marka birlikte %s ile rakip düzeyindedir); ortalama puan VitrA'da %s, Artema'da %s düzeyindedir. Olumlu yorumlarda en sık geçen tema malzeme ve sağlamlıktır (VitrA %s, Artema %s). Rakipler arasında olumsuz payın en yüksek olduğu markalar %s olarak öne çıkmaktadır."
         % (yzd(M["VitrA"]["olumsuz"]), yzd(M["Artema"]["olumsuz"]), yzd(RK["olumsuz"]), yzd(VG["olumsuz"]), f1(M["VitrA"]["ort_puan"]), f1(M["Artema"]["ort_puan"]), yzd(tp(M["VitrA"], "kalite")), yzd(tp(M["Artema"], "kalite")),
            " ve ".join("%s (%s)" % (m, yzd(M[m]["olumsuz"])) for m in sorted(RAK, key=lambda m: -(M[m]["olumsuz"] or 0))[:2])),
         "The negative review share is %s at VitrA, %s at Artema and %s at competitors (the two brands together are in line with competitors at %s); the average rating is %s for VitrA and %s for Artema. The most frequent theme in positive reviews is material and sturdiness (VitrA %s, Artema %s). Among competitors, the brands with the highest negative share: %s."
         % (ye(M["VitrA"]["olumsuz"]), ye(M["Artema"]["olumsuz"]), ye(RK["olumsuz"]), ye(VG["olumsuz"]), "%.1f" % M["VitrA"]["ort_puan"], "%.1f" % M["Artema"]["ort_puan"], ye(tp(M["VitrA"], "kalite")), ye(tp(M["Artema"], "kalite")),
            " and ".join("%s (%s)" % (m, ye(M[m]["olumsuz"])) for m in sorted(RAK, key=lambda m: -(M[m]["olumsuz"] or 0))[:2])), "D38", "D31"),
 x("Pain point profili: kategori geneli mi, markaya özgü mü?", "Pain point profile: category-wide or brand-specific?"),
 TP,
 insight("Olumsuz yorumlarda iade, değişim ve satıcı iletişimi, malzeme ve sağlamlık ile kırık veya hasarlı ürün, VitrA'da da rakiplerde de ilk sıralardadır; bu temalar kategori genelindeki ortak pain point'ler olarak okunabilir. VitrA'da kırık, hasarlı veya kusurlu ürün payı %s ile rakip payının (%s) %s. İade ve satıcı iletişimi teması VitrA ve Artema'da daha sık geçmektedir; olumsuz deneyimin önemli bölümü üründen çok teslimat ve satış sonrası süreçte oluşmaktadır."
         % (yzd(_k_neg), yzd(_r_neg), "üzerindedir" if _k_neg > _r_neg + 2 else "yakınındadır"),
         "Returns, exchange and seller contact, material and sturdiness, and broken or damaged products rank first in negative reviews at both VitrA and competitors; these themes can be read as category-wide pain points. At VitrA the broken, damaged or defective product share is %s, %s the competitor share (%s). The returns and seller contact theme appears more often at VitrA and Artema; a significant part of the negative experience arises in delivery and after-sales rather than in the product itself."
         % (ye(_k_neg), "above" if _k_neg > _r_neg + 2 else "close to", ye(_r_neg)), "D38"),
 x("Ürün grubu karşılaştırması", "Product group comparison"),
 TG,
 insight("VitrA ve Artema olumsuz payının rakiplerin belirgin biçimde üzerinde kaldığı grup %s olarak görülmektedir. %s gruplarında VitrA ve Artema olumsuz payı rakiplerin altındadır. Bu dağılım, VitrA'nın olumsuz deneyiminin ürün geneline yayılmadığına, belirli bir ürün grubunda yoğunlaştığına işaret etmektedir."
         % ("; ".join("%s (%s, rakipler %s)" % (g["grup"].lower(), yzd(g["vitra"]["olumsuz"]), yzd(g["rakip"]["olumsuz"])) for g in _ust) or "-", (", ".join(g["grup"].lower() for g in _alt) or "-").capitalize()),
         "The group where the VitrA and Artema negative share stays clearly above competitors: %s. In the %s groups the VitrA and Artema negative share is below competitors. This distribution indicates that VitrA's negative experience is not spread across the range but concentrated in a specific product group."
         % ("; ".join("%s (%s, competitors %s)" % (GEN.get(g["grup"], g["grup"]).lower(), ye(g["vitra"]["olumsuz"]), ye(g["rakip"]["olumsuz"])) for g in _ust) or "-", ", ".join(GEN.get(g["grup"], g["grup"]).lower() for g in _alt) or "-"), "D38"),
 x("Rakiplerin öne çıktığı ve zorlandığı alanlar", "Where competitors stand out and struggle"),
 KARTLAR,
 insight("Rakiplerde %s'de kırık veya hasarlı ürün (olumsuz yorumların %s'i), %s'de montaj (%s), %s'de iade ve satıcı iletişimi (%s) öne çıkan pain point'lerdir. Bu alanlar kategori genelinde ortak pain point'lerdir; VitrA'da da kırık, hasarlı veya kusurlu ürün (%s) ve iade-satıcı iletişimi (%s) payı rakip ortalamasının (%s ve %s) üzerindedir."
         % (_km, yzd(_kv), _mm, yzd(_mv), _sm, yzd(_sv), yzd(M["VitrA"]["tema_neg"].get("kirik")), yzd(M["VitrA"]["tema_neg"].get("satis_sonrasi")), yzd(RK["tema_neg"].get("kirik")), yzd(RK["tema_neg"].get("satis_sonrasi"))),
         "At competitors, broken or damaged products at %s (%s of negative reviews), installation at %s (%s) and returns and seller contact at %s (%s) are the leading pain points. These are category-wide pain points; at VitrA too the shares of broken, damaged or defective products (%s) and returns and seller contact (%s) are above the competitor average (%s and %s)."
         % (_km, ye(_kv), _mm, ye(_mv), _sm, ye(_sv), ye(M["VitrA"]["tema_neg"].get("kirik")), ye(M["VitrA"]["tema_neg"].get("satis_sonrasi")), ye(RK["tema_neg"].get("kirik")), ye(RK["tema_neg"].get("satis_sonrasi"))), "D38"),
 x("VitrA için gelişim alanları", "Development areas for VitrA"),
 GELISIM,
 x("Soru-cevap kümeleri", "Q&A clusters"),
 TS,
 insight("VitrA ürünlerine gelen sorular uyumluluk ve kullanım yeri (%s), kutu içeriği (%s) ve ölçü (%s) etrafında toplanmaktadır; rakiplerde ölçü (%s) ilk sıradadır. VitrA ve Artema sorularında medyan cevap süresi sırasıyla %s ve %s saattir. Soruların ağırlığı, karar anında eksik kalan bilginin ürün sayfasında uyumluluk ve set kapsamı tarafında olduğuna işaret etmektedir."
         % (yzd(_vs.get("uyum")), yzd(_vs.get("icerik")), yzd(_vs.get("olcu")), yzd(_rs.get("olcu")), f1(S["VitrA"]["medyan_saat"] or 0), f1(S["Artema"]["medyan_saat"] or 0)),
         "Questions on VitrA products cluster around compatibility and place of use (%s), box contents (%s) and size (%s); at competitors size (%s) ranks first. The median answer time is %s and %s hours for VitrA and Artema questions respectively. The weight of questions indicates that the information missing at the decision point concerns compatibility and set scope on the product page."
         % (ye(_vs.get("uyum")), ye(_vs.get("icerik")), ye(_vs.get("olcu")), ye(_rs.get("olcu")), "%.1f" % (S["VitrA"]["medyan_saat"] or 0), "%.1f" % (S["Artema"]["medyan_saat"] or 0)), "D38", "D31"),
 x("Tüm yorumlar ve sorular; marka ve pazaryeri kırılımında pain point kümeleri, marka notları ve filtrelenebilir kayıtlarla birlikte ayrı sayfada yer almaktadır.",
   "All reviews and questions are on a separate page, with pain point clusters by brand and marketplace, brand notes and filterable records.") + " " + alt_btn(),
 kaynak("Trendyol ve Hepsiburada ürün sayfaları · herkese açık değerlendirme ve soru-cevap kayıtları · VitrA resmi mağaza Trendyol paneli · %s - %s · 03.10.2026" % (_d0[:7], _d1[:7]),
        "Trendyol and Hepsiburada product pages · public reviews and Q&A records · VitrA official store Trendyol panel · %s - %s · 03.10.2026" % (_d0[:7], _d1[:7]), "D38", "D31"),
)

# ---------------------------------------------------------------- diger bolumlerden alt sayfaya kopru
def kopru(tr, en):
    return '<p class="kopru">%s %s</p>' % (x(tr, en), alt_btn())
KOPRU_SIKAYET = kopru("Pazaryeri ürün sayfalarındaki yorum ve sorular, marka ve pazaryeri kırılımında pain point kümeleriyle ayrı sayfada incelenebilir.",
                      "Reviews and questions on marketplace product pages can be examined on a separate page with pain point clusters by brand and marketplace.")
KOPRU_PANEL = kopru("Resmi mağaza ve diğer satıcılardaki VitrA ve Artema yorumları, rakip markalarla karşılaştırmalı olarak ayrı sayfada yer almaktadır.",
                    "VitrA and Artema reviews at the official store and other sellers are on a separate page, compared with competitor brands.")
