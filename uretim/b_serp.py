# -*- coding: utf-8 -*-
"""Bolum: Google arama sonuclari (SERP) ve AI Overview · uc grup: A VitrA gami, B yakin kategori firsatlari, C marka ve karsilastirma (04.10.2026)."""
from ortak import *
import serp_ozet as S
import json as _json, os as _os, collections as _col
_Y = _json.load(open(_os.path.join(veri.V, "islenmis", "yeni_kategori.json"), encoding="utf-8"))["tema"]
TEMA_EN = {"Vitrifiyeler": "Sanitaryware", "Banyo Mobilyaları": "Bathroom Furniture", "Armatürler": "Taps and Mixers", "Duşlar": "Showers", "Yıkanma Alanları": "Bathing Areas",
           "Rezervuarlar": "Cisterns", "Banyo Aksesuarları": "Bathroom Accessories", "Karo Seramik Ürünleri": "Ceramic Tiles", "Soru ve karar": "Questions and decisions",
           "Hizmet ve ilham": "Services and inspiration", "VitrA ve Artema": "VitrA and Artema", "Rakip marka": "Competitor brand", "Perakendeci adıyla": "With retailer name",
           "Karşılaştırma ve marka seçimi": "Comparison and brand choice"}
TEMA_EN.update({t["tr"]: t["en"] for t in _Y.values()})
def TA(t): return x(t, TEMA_EN.get(t, t))
def _ilk3(r):
    ds = []
    for t_ in sorted(r.get("top10") or [], key=lambda z: z["sira"]):
        if t_["alan"] not in ds: ds.append(t_["alan"])
    return " · ".join(ds[:3])
def _bir(r):
    t_ = sorted(r.get("top10") or [], key=lambda z: z["sira"]); return t_[0]["alan"] if t_ else None
def _sira(v): return n(("%.1f" % v).replace(".", ",")) if v is not None else n("-")
def _kw_tablo(lst):
    rows_ = []
    for r in sorted(lst, key=lambda z: -(z["hacim"] or 0)):
        g = r.get("gsc")
        rows_.append([kw(r["kelime"]), TA(r["tema"]), cell(r["hacim"]), n(str(r["vitra_sira"]) if r.get("vitra_sira") else "-"),
                      _sira(g["sira"]) if g else n("-"), cell(g["tik"]) if g else n("-"), veri_m(_ilk3(r) or "-")])
    return tablo([th("Arama kelimesi", "Search keyword", "Arama kelimesi.", "Search keyword."), th("Tema", "Theme", "Kelimenin ait olduğu kategori ya da tema.", "Category or theme of the keyword."),
                  th("Aylık hacim", "Monthly volume", "Google Keyword Planner, Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Google Keyword Planner, average monthly search volume, September 2025 - August 2026.", True),
                  th("VitrA sırası (mobil)", "VitrA position (mobile)", "vitra.com.tr'nin mobil sırası: SEOmonitor takibindeki kelimelerde 03.10.2026 günlük takip, diğerlerinde %s tarihli üç Google gözleminin medyanı; \"-\" ilk 20'de yok." % _tr(S.TARIH), "vitra.com.tr mobile position: SEOmonitor daily tracking, 03.10.2026; for untracked keywords the median of the SERP observations of %s; \"-\" not in the top 20." % _tr(S.TARIH), True),
                  th("Search Console ort. sıra", "Search Console avg. position", "1 Tem - 30 Eyl 2026 ortalama sıra, tüm cihazlar; \"-\" gösterim yok.", "Average position 1 Jul - 30 Sep 2026, all devices; \"-\" no impressions.", True),
                  th("Search Console click", "Search Console clicks", "Aynı dönemde bu kelimeden vitra.com.tr'ye gelen click.", "Clicks from this keyword to vitra.com.tr in the same period.", True),
                  th("İlk 3 alan adı", "Top 3 domains", "İlk üç organik sonucun alan adı; sıra kaynağı VitrA sırasıyla aynıdır.", "Domains of the first three organic results; the position source is the same as for VitrA's position.")], rows_, "uzun")
def _tr(t): y, m, d = t.split("-"); return "%s.%s.%s" % (d, m, y)
_DIALAR = []
def _pop_kw(lst, tr_, en_, ikon=True, etk_tr=None, etk_en=None):
    b_, d_ = pop(tr_, en_, _kw_tablo(lst), etk_tr, etk_en, ikon=ikon); _DIALAR.append(d_); return b_
# ---------------------------------------------------------------- A: kategori tablosu
A = S.SK; ATEMA = [t for t, _ in _col.Counter(r["tema"] for r in A).most_common()]
ATEMA.sort(key=lambda t: -sum(r["hacim"] for r in A if r["tema"] == t))
KAT = []
for t in ATEMA:
    L = [r for r in A if r["tema"] == t]; v = S.vitra(L)
    bir = _col.Counter(_bir(r) for r in L if _bir(r)).most_common(1)
    KAT.append((t, L, v, bir[0] if bir else ("-", 0)))
T_KAT = tablo([th("Kategori", "Category", "VitrA kategori ağacındaki ana kategori; Hizmet ve ilham ile Soru ve karar satırları ürün dışı arama türleridir. Ok simgesi kategorideki kelimeleri ve metriklerini açar.", "Main category in VitrA's category tree; the Services and inspiration and Questions and decisions rows are non-product search types. The arrow opens the category's keywords and metrics."),
               th("Kelime", "Keywords", "Kategoriden seçilen kelime sayısı; her alt kategoriden en az bir baş kelime alınmıştır.", "Keywords chosen from the category; at least one head keyword was taken from each subcategory.", True),
               th("Aylık hacim", "Monthly volume", "Kelimelerin toplam aylık ortalama arama hacmi, Keyword Planner, Eyl 2025 - Ağu 2026.", "Total average monthly search volume of the keywords, Keyword Planner, Sep 2025 - Aug 2026.", True),
               th("VitrA ilk 3", "VitrA top 3", "vitra.com.tr'nin mobilde ilk 3'te olduğu kelime sayısı (takipteki kelimelerde SEOmonitor günlük takip, 03.10.2026; diğerlerinde üç Google gözleminin medyanı).", "Keywords where vitra.com.tr is in the mobile top 3 (SEOmonitor daily tracking, 03.10.2026, for tracked keywords; median of three Google observations for the others).", True),
               th("VitrA ilk 10", "VitrA top 10", "vitra.com.tr'nin ilk 10'da olduğu kelime sayısı.", "Keywords where vitra.com.tr is in the top 10.", True),
               th("Hacim ağırlıklı ilk 10 payı", "Volume-weighted top-10 share", "VitrA'nın ilk 10'da olduğu kelimelerin kategori arama hacmi içindeki payı; büyük kelimelerdeki görünürlüğü öne çıkarır.", "Share of the category's search volume coming from keywords where VitrA is in the top 10; highlights visibility in large keywords.", True),
               th("Search Console ilk 10", "Search Console top 10", "Search Console'da 1 Tem - 30 Eyl 2026 ortalama sırası 10 ve altında olan kelime sayısı.", "Keywords with an average Search Console position of 10 or better, 1 Jul - 30 Sep 2026.", True),
               th("1. sırada en sık", "Most often in 1st place", "Kategorideki kelimelerde 1. sırada en sık görülen alan adı ve kelime sayısı.", "Domain most often in 1st place in the category's keywords, and its keyword count.")],
              [[TA(t) + _pop_kw(L, "%s: kelimeler ve metrikler" % t, "%s: keywords and metrics" % TEMA_EN.get(t, t)), cell(len(L)), cellk(sum(r["hacim"] for r in L)), cell(v["ilk3"]), cell(v["ilk10"]),
                n(yzd(v["hacim10"], 0)), cell(v["gsc10"]), veri_m("%s (%d)" % b)] for t, L, v, b in KAT])
_kg = [(t, v) for t, L, v, b in KAT if t not in ("Soru ve karar", "Hizmet ve ilham") and len(L) >= 4]
_iyi = sorted(_kg, key=lambda i: -i[1]["hacim10"])[:3]; _zay = sorted(_kg, key=lambda i: i[1]["hacim10"])[:3]
# ---------------------------------------------------------------- A: alan adlari
DOM = []
for a_, _ in S.D10.most_common(15):
    tm = S.TEMA_D[a_].most_common(3)
    DOM.append((a_, S.D10[a_], S.D3[a_], S.D1[a_], f1(S.ort_sira(a_)), ", ".join("%s %d" % (t_, c_) for t_, c_ in tm), ", ".join("%s %d" % (TEMA_EN.get(t_, t_), c_) for t_, c_ in tm)))
T_DOM = tablo([th("Alan adı", "Domain", "VitrA gamındaki aramalarda Google TR mobil ilk 10 organik sonuçta görünen alan adı.", "Domain appearing in Google TR mobile top 10 organic results for searches in VitrA's range."),
               th("İlk 10 (kelime)", "Top 10 (keywords)", "%d kelimeden kaçında ilk 10'da." % S.N, "In how many of %d keywords it is in the top 10." % S.N, True),
               th("İlk 3 (kelime)", "Top 3 (keywords)", "Kaç kelimede ilk 3'te.", "In how many keywords it is in the top 3.", True),
               th("1. sıra", "1st place", "Kaç kelimede 1. sırada.", "In how many keywords it is in 1st place.", True),
               th("Ort. sıra", "Avg. position", "Görüldüğü kelimelerdeki sıranın ortalaması (takipteki kelimelerde SEOmonitor sırası, diğerlerinde üç gözlemin medyanı).", "Average position in the keywords where it appears (SEOmonitor position for tracked keywords, median of three observations for the others).", True),
               th("En çok görüldüğü kategoriler", "Categories where seen most", "İlk 10'da en çok görüldüğü üç kategori ve kelime sayısı.", "The three categories where it is most often in the top 10, with keyword counts.")],
              [[veri_m(a), cell(b), cell(c), cell(d), n(e), x(f, g)] for a, b, c, d, e, f, g in DOM])
_T3, _P3 = S.ILK3["yuva"], S.ILK3["pz"]
# ---------------------------------------------------------------- A: VitrA'nin ilk 20'de olmadigi kelimeler
BOS = sorted([r for r in A if not r.get("vitra_sira")], key=lambda r: -r["hacim"])
T_BOS = tablo([th("Arama kelimesi", "Search keyword", "VitrA gamındaki, vitra.com.tr'nin mobilde ilk 20'de görünmediği kelime (SEOmonitor 03.10.2026 ya da %s tarihli üç Google gözleminin medyanı)." % _tr(S.TARIH), "Keyword in VitrA's range where vitra.com.tr does not appear in the mobile top 20 (SEOmonitor 03.10.2026 or the SERP observation of %s)." % _tr(S.TARIH)),
               th("Kategori", "Category", "Kelimenin kategorisi.", "Category of the keyword."),
               th("Aylık hacim", "Monthly volume", "Keyword Planner, Eyl 2025 - Ağu 2026 aylık ortalama.", "Keyword Planner, monthly average Sep 2025 - Aug 2026.", True),
               th("Search Console ort. sıra", "Search Console avg. position", "vitra.com.tr'nin bu sorgudaki 1 Tem - 30 Eyl 2026 ortalama sırası (tüm cihazlar); \"-\" sorgu raporda yok.", "vitra.com.tr average position for this query, 1 Jul - 30 Sep 2026 (all devices); \"-\" query not in the report.", True),
               th("Search Console click", "Search Console clicks", "Aynı dönemde bu sorgudan gelen click.", "Clicks from this query in the same period.", True),
               th("İlk 3 alan adı", "Top 3 domains", "İlk üç organik sonucun alan adı (mobil).", "Domains of the first three organic results (mobile).")],
              [[kw(r["kelime"]), TA(r["tema"]), cell(r["hacim"]), _sira(r["gsc"]["sira"]) if r.get("gsc") else n("-"), cell(r["gsc"]["tik"]) if r.get("gsc") else n("-"), veri_m(_ilk3(r) or "-")] for r in BOS[:25]], "uzun")
_BOS_GSC = [r for r in BOS if r.get("gsc") and r["gsc"]["sira"] <= 10]
# ---------------------------------------------------------------- B: yakin kategori firsatlari
B = S.GRUP["B"]
BT = []
for t in sorted({r["tema"] for r in B}, key=lambda t: -sum(r["hacim"] for r in B if r["tema"] == t)):
    L = [r for r in B if r["tema"] == t]; slot = [z for r in L for z in r["top10"]]
    pz = 100 * sum(1 for z in slot if z["alan"] in S.PZ) / (len(slot) or 1)
    rh = 100 * sum(1 for z in slot if z["tip"] in ("blog/rehber", "video", "sosyal/görsel", "forum/şikayet")) / (len(slot) or 1)
    bir = _col.Counter(_bir(r) for r in L if _bir(r)).most_common(1)
    BT.append((t, L, pz, rh, bir[0] if bir else ("-", 0), sum(1 for r in L if r.get("vitra_sira")), sum(1 for r in L if r.get("ai_ilk_cekim"))))
T_B = tablo([th("Tema", "Theme", "VitrA gamında bulunmayan ya da kısmen bulunan, banyo yenilemede birlikte aranan ürün ve hizmet teması; ok simgesi kelimeleri açar.", "Product or service theme searched together with bathroom renovation that VitrA does not carry or carries only partly; the arrow opens the keywords."),
             th("Kelime", "Keywords", "Temadan seçilen kelime sayısı.", "Keywords chosen from the theme.", True),
             th("Aylık hacim", "Monthly volume", "Kelimelerin toplam aylık ortalama arama hacmi, Keyword Planner.", "Total average monthly search volume of the keywords, Keyword Planner.", True),
             th("İlk 10'da pazaryeri payı", "Marketplace share of top 10", "İlk 10 organik sonucun pazaryeri, yapı market ve fiyat karşılaştırma sitelerine ait payı.", "Share of top-10 organic results held by marketplaces, DIY retailers and price comparison sites.", True),
             th("İlk 10'da içerik payı", "Content share of top 10", "İlk 10 sonucun rehber, video, sosyal ve forum sayfalarına ait payı; bilgi arayan kullanıcıyı gösterir.", "Share of top-10 results held by guide, video, social and forum pages; indicates users looking for information.", True),
             th("1. sırada en sık", "Most often in 1st place", "Temadaki kelimelerde 1. sırada en sık görülen alan adı.", "Domain most often in 1st place in the theme's keywords."),
             th("VitrA ilk 20'de", "VitrA in top 20", "vitra.com.tr'nin ilk 20'de göründüğü kelime sayısı.", "Keywords where vitra.com.tr appears in the top 20.", True),
             th("AI Overview", "AI Overview", "AI Overview çıkan kelime sayısı.", "Keywords with an AI Overview.", True)],
            [[TA(t) + _pop_kw(L, "%s: kelimeler" % t, "%s: keywords" % TEMA_EN.get(t, t)), cell(len(L)), cellk(sum(r["hacim"] for r in L)), n(yzd(pz, 0)), n(yzd(rh, 0)), veri_m("%s (%d)" % b), cell(v), cell(ai)]
             for t, L, pz, rh, b, v, ai in BT])
_Bh = sum(r["hacim"] for r in B); _Bpz = 100 * sum(1 for r in B for z in r["top10"] if z["alan"] in S.PZ) / (sum(len(r["top10"]) for r in B) or 1)
_Bv = sum(1 for r in B if r.get("vitra_sira"))
# ---------------------------------------------------------------- C: marka ve karsilastirma
C = S.GRUP["C"]
SITE = {"VitrA": "vitra.com.tr", "Artema": "artema.com.tr", "E.C.A.": "eca.com.tr", "Kale": "kale.com.tr", "Serel": "serel.com.tr", "Creavit": "creavit.com.tr", "Visam": "visam.com.tr",
        "Turkuaz": "turkuazseramik.com", "Grohe": "grohe.com.tr", "Geberit": "geberit.com.tr", "Bien": "bien.com.tr", "Orka": "orkabanyo.com", "Bocchi": "bocchi.com.tr", "Duravit": "duravit.com.tr"}
def _kendi(r, m):
    s_ = SITE.get(m); b_ = _bir(r) or ""
    return bool(s_) and (b_ == s_ or b_.endswith("." + s_) or (m == "Creavit" and "creavit" in b_) or (m == "Grohe" and "grohe" in b_) or (m == "Turkuaz" and "turkuaz" in b_) or (m == "Orka" and "orka" in b_))
CT = []
for alt in ["VitrA", "Artema"] + [m for m in SITE if m not in ("VitrA", "Artema")] + ["IKEA", "Koçtaş", None]:
    L = [r for r in C if r.get("alt") == alt] if alt else [r for r in C if r["tema"] == "Karşılaştırma ve marka seçimi"]
    if not L: continue
    ad_ = alt or "Karşılaştırma ve marka seçimi"
    bir = _col.Counter(_bir(r) for r in L if _bir(r)).most_common(1)
    CT.append((ad_, L, sum(1 for r in L if _kendi(r, alt)) if alt in SITE else None, sum(1 for r in L if (r.get("vitra_sira") or 99) <= 10), bir[0] if bir else ("-", 0), sum(1 for r in L if r.get("ai_ilk_cekim"))))
T_C = tablo([th("Marka / arama türü", "Brand / search type", "Aramada geçen marka ya da karşılaştırma araması; ok simgesi kelimeleri açar.", "Brand in the search or comparison search; the arrow opens the keywords."),
             th("Kelime", "Keywords", "Kelime sayısı.", "Number of keywords.", True),
             th("Aylık hacim", "Monthly volume", "Toplam aylık ortalama arama hacmi, Keyword Planner.", "Total average monthly search volume, Keyword Planner.", True),
             th("Markanın sitesi 1. sırada", "Brand's own site in 1st place", "Markanın kendi sitesinin 1. sırada olduğu kelime sayısı.", "Keywords where the brand's own site is in 1st place.", True),
             th("vitra.com.tr ilk 10'da", "vitra.com.tr in top 10", "vitra.com.tr'nin ilk 10'da olduğu kelime sayısı.", "Keywords where vitra.com.tr is in the top 10.", True),
             th("1. sırada en sık", "Most often in 1st place", "Bu aramalarda 1. sırada en sık görülen alan adı.", "Domain most often in 1st place in these searches."),
             th("AI Overview", "AI Overview", "AI Overview çıkan kelime sayısı.", "Keywords with an AI Overview.", True)],
            [[x(a, TEMA_EN.get(a, a)) + _pop_kw(L, "%s: kelimeler" % a, "%s: keywords" % TEMA_EN.get(a, a)), cell(len(L)), cellk(sum(r["hacim"] for r in L)), cell(k_) if k_ is not None else n("-"), cell(v), veri_m("%s (%d)" % b), cell(ai)]
             for a, L, k_, v, b, ai in CT])
_CV = [r for r in C if r.get("alt") == "VitrA"]; _CVk = sum(1 for r in _CV if _kendi(r, "VitrA"))
_CVar = _col.Counter(_bir(r) for r in _CV if not _kendi(r, "VitrA"))
_CR = [r for r in C if r["tema"] == "Rakip marka"]; _CRv = sum(1 for r in _CR if (r.get("vitra_sira") or 99) <= 10); _CRk = sum(1 for r in _CR if _kendi(r, r["alt"]))
_CK = [r for r in C if r["tema"] == "Karşılaştırma ve marka seçimi"]; _CKv = sum(1 for r in _CK if (r.get("vitra_sira") or 99) <= 10)
_CKt = _col.Counter(z["tip"] for r in _CK for z in r["top10"]); _CKtt = sum(_CKt.values()) or 1
# ---------------------------------------------------------------- SERP ozellikleri (gruplara gore)
def _oz(k_, tr_, en_):
    hs = []
    for g in "ABC":
        L = S.GRUP[g]; n_, _ = S.ozellik(k_, L); hs.append("%d (%s)" % (n_, yzd(100 * n_ / len(L), 0)))
    tn, _ = S.ozellik(k_, S.TUM)
    return [x(tr_, en_), n(hs[0]), n(hs[1]), n(hs[2]), n("%d (%s)" % (tn, yzd(100 * tn / S.NT, 0)))]
T_OZ = tablo([th("SERP özelliği", "SERP feature", "Arama sonuç sayfasında organik sonuç dışındaki blok.", "Block on the results page other than organic results."),
              th("A · VitrA gamı", "A · VitrA range", "%d kelimeden kaçında görüldüğü." % len(S.GRUP["A"]), "In how many of %d keywords it appeared." % len(S.GRUP["A"]), True),
              th("B · Yakın kategoriler", "B · Adjacent categories", "%d kelimeden kaçında görüldüğü." % len(S.GRUP["B"]), "In how many of %d keywords it appeared." % len(S.GRUP["B"]), True),
              th("C · Marka ve karşılaştırma", "C · Brand and comparison", "%d kelimeden kaçında görüldüğü." % len(S.GRUP["C"]), "In how many of %d keywords it appeared." % len(S.GRUP["C"]), True),
              th("Toplam", "Total", "%d kelimenin tamamında." % S.NT, "Across all %d keywords." % S.NT, True)],
             [_oz("ai", "AI Overview", "AI Overview"), _oz("paa", "People Also Ask", "People Also Ask"), _oz("video", "Video / Shorts", "Video / Shorts"),
              _oz("yerel", "Yerel sonuçlar (Local pack)", "Local results (Local pack)"), _oz("ilan", "İlan ve hizmet platformları", "Listing and service platforms")])
_AIG = {g: S.ai_grup(g) for g in "ABC"}
_AIV = [r for r in S.TUM if r["kelime"] in S.AI_VITRA]
_AI1 = sum(1 for r in _AIV if r.get("vitra_sira") == 1)
AI = sorted(S.AI_ALAN.items(), key=lambda t_: (-t_[1], t_[0]))[:12]
RANK_AI = rank_list([(veri_m(a), b) for a, b in AI], max(b_ for _, b_ in AI), you=lambda e: "vitra" in e, fmt=lambda v: bin(v))
PAA = [("Fiyat", "Price", ["Klozet iç takım değişimi ne kadar?", "Akıllı klozet fiyatları ne kadar?", "60 cm banyo dolabı fiyatları ne kadar?", "komple banyo yenileme fiyatları ne kadar?", "Arıtma taktırmak kaç TL?"]),
       ("Ölçü ve seçim", "Size and selection", ["Klozet kapakları her klozete uyar mı?", "Banyo dolabı kaç cm olur?", "Duşakabin tekerleği standart mı?", "Banyo dolabı için en iyi malzeme hangisidir?", "En iyi gömme rezervuar hangisi?"]),
       ("Montaj ve tamir", "Installation and repair", ["Gömme rezervuar montaj ücreti ne kadar?", "Gömme rezervuar neden su doldurmaz?", "Şamandıra suyu neden kesmez?", "Klozet taharet musluğu neden akıtır?", "Banyo fayanslarını kırmadan yenileme nasıl yapılır?"]),
       ("VitrA ve marka", "VitrA and brand", ["VitrA ve Artema aynı marka mı?", "VitrA klozet iç takımının fiyatı nedir?", "Mersin'de VitrA servisi var mı?", "Batarya eca mı artema mı?", "En iyi klozet markası hangisidir?"])]
_PAA_YOK = [q for _, _, qs in PAA for q in qs if q not in set(S.PAA_SORU)]
if _PAA_YOK: raise SystemExit("PAA ornegi guncel listede yok: %s" % _PAA_YOK)
PAA_H = '<div class="fnotes">%s</div>' % "".join('<article class="fnote"><span class="fc">%s</span><ul>%s</ul></article>' % (x(a, b), "".join("<li>%s</li>" % veri_m(q) for q in qs)) for a, b, qs in PAA)
_vs = sorted(_AIV, key=lambda r: -r["hacim"])[:8]
_ADN = {"koctas.com.tr": "Koçtaş", "hepsiburada.com": "Hepsiburada", "akakce.com": "Akakçe", "amazon.com.tr": "Amazon", "n11.com": "n11", "cimri.com": "Cimri",
        "bauhaus.com.tr": "Bauhaus", "ikea.com.tr": "IKEA", "tekzen.com.tr": "Tekzen", "pttavm.com": "PttAVM", "ciceksepeti.com": "Çiçeksepeti"}
def _izl(ve):
    L = [(a, c) for a, c in S.D10.most_common(6) if a != "trendyol.com"][:4]
    p = ["%s (%d)" % (_ADN.get(a, a), c) for a, c in L]
    return ", ".join(p[:-1]) + " " + ve + " " + p[-1]

HTML = """
<p class="lede">%s</p>
%s
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
<p class="popl">%s</p>
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
%s
""" % (
 x("%s tarihinde Google Türkiye mobil sonuçlarında %d kelimenin ilk 20 organik sonucu ve arama sonuç sayfası (SERP) özellikleri incelenmiştir; amaç, kullanıcının bir banyo ürününü aradığında hangi sitelerle karşılaştığını ve VitrA'nın bu ilk temasta nerede durduğunu görmektir." % (_tr(S.TARIH), S.NT),
   "On %s, the top 20 organic results and search engine results page (SERP) features of Google Turkey mobile results were examined for %d keywords, to see which sites users meet when searching for a bathroom product and where VitrA stands at this first touchpoint." % (_tr(S.TARIH), S.NT)),
 note("GRUPLAR VE YÖNTEM", "GROUPS AND METHOD", ul_b([
   ("A · VitrA gamı (%d kelime):" % S.N, "A · VitrA range (%d keywords):" % S.N, "VitrA'nın sattığı ürünlerin aramaları; her alt kategoriden en az bir baş kelime, büyük kategorilerde birkaç kelime, karo sınırlı tutulmuştur. Hizmet ve ilham ile soru aramaları da bu gruptadır.", "Searches for products VitrA sells; at least one head keyword from each sub-category, several in large categories, with tiles kept limited. Service, inspiration and question searches are also in this group."),
   ("B · Yakın kategoriler (%d kelime):" % len(S.GRUP["B"]), "B · Adjacent categories (%d keywords):" % len(S.GRUP["B"]), "VitrA'nın satmadığı ya da yalnız bir kısmını sattığı, banyo yenilemede birlikte aranan ürünleri kapsar (ör. şofben, su arıtma, granit evye, havlupan).", "Products searched together with bathroom renovation that VitrA does not sell or sells only in part (e.g. water heaters, water purifiers, granite sinks, towel radiators)."),
   ("C · Marka ve karşılaştırma (%d kelime):" % len(S.GRUP["C"]), "C · Brand and comparison (%d keywords):" % len(S.GRUP["C"]), "VitrA, Artema, 12 rakip marka, IKEA ve Koçtaş adıyla yapılan aramalar ile \"vitra mı eca mı\" türü karşılaştırma aramalarını kapsar.", "Searches with the VitrA, Artema, 12 competitor brand, IKEA and Koçtaş names and comparison searches such as \"vitra mı eca mı\"."),
   ("Yöntem:", "Method:", "SEOmonitor'de günlük takip edilen %d kelimede tüm sıralar (VitrA ve rakipler) 03.10.2026 mobil takip verisinden, diğer kelimelerde aynı gün yapılan üç Google gözleminin medyanından alınmıştır. İlk üç gösterge ve ilk dört alt başlık A grubundan, AI Overview ve soru göstergeleri üç gruptan hesaplanmıştır. Keyword Planner'da hacmi olmayan kelimeler ile Google sonuçlarında banyo dışı ürünlere yönelen genel kelimeler çıkarılmıştır: tek başına aranan \"kartuş\" ve \"şamandıra\" yazıcı kartuşu ve olta şamandırası, \"banyo seti\" ve \"banyo takımı\" tekstil seti, \"dolap kulpu\" mobilya kulpu, \"çöp kovası\" genel ev kovası sonuçları göstermektedir. Bu ürünlerin banyo bağlamlı aramaları (batarya kartuşu, klozet şamandırası, banyo dolabı kulpu, banyo çöp kovası) kelime evreninde yer almaktadır." % sum(1 for r in S.TUM if r.get("sira_kaynak") == "seomonitor"),
    "For the %d keywords tracked daily in SEOmonitor all positions (VitrA and competitors) come from the 03.10.2026 mobile tracking data; for the other keywords they come from the median of three Google observations on the same day. The first three indicators and the first four sub-sections are calculated from group A, the AI Overview and question indicators from all three groups. Keywords with no Keyword Planner volume and generic keywords for which Google shows non-bathroom products were removed: on their own, \"kartuş\" and \"şamandıra\" return printer cartridges and fishing floats, \"banyo seti\" and \"banyo takımı\" textile sets, \"dolap kulpu\" furniture handles and \"çöp kovası\" general household bins. The bathroom-specific searches for these products (tap cartridge, WC float, bathroom cabinet handle, bathroom waste bin) remain in the keyword universe." % sum(1 for r in S.TUM if r.get("sira_kaynak") == "seomonitor"))])),
 kpi_kart(yzd(S.VITRA["hacim10"], 0), "VitrA gamındaki arama hacminin VitrA'nın ilk 10'da olduğu kelimelerden gelen payı · %d / %d kelimede ilk 10" % (S.VITRA["ilk10"], S.N), "Share of search volume in VitrA's range from keywords where VitrA is in the top 10 · top 10 in %d / %d keywords" % (S.VITRA["ilk10"], S.N), "hi"),
 kpi_kart(yzd(100 * S.D10["trendyol.com"] / S.N, 0), "Trendyol'un ilk 10'da olduğu kelime payı (VitrA gamı) · %d kelimede 1. sıra" % S.D1["trendyol.com"], "Share of keywords with Trendyol in the top 10 (VitrA range) · first place in %d keywords" % S.D1["trendyol.com"]),
 kpi_kart(yzd(100 * _P3 / _T3, 0), "Pazaryeri, yapı market ve fiyat karşılaştırma sitelerinin ilk 3 sıralardaki payı (VitrA gamı, %d yuvanın %s)" % (_T3, ek(_P3, "i")), "Share of top-3 slots held by marketplaces, DIY retailers and price comparison sites (VitrA range, %d of %d slots)" % (_P3, _T3)),
 kpi_kart("%d / %d" % (_AIG["A"]["vitra"], _AIG["A"]["icerik"]), "VitrA gamında VitrA'nın kaynak gösterildiği AI Overview · yakın kategoriler %d / %d, marka ve karşılaştırma %d / %d" % (_AIG["B"]["vitra"], _AIG["B"]["icerik"], _AIG["C"]["vitra"], _AIG["C"]["icerik"]), "AI Overviews citing VitrA in VitrA's range · adjacent categories %d / %d, brand and comparison %d / %d" % (_AIG["B"]["vitra"], _AIG["B"]["icerik"], _AIG["C"]["vitra"], _AIG["C"]["icerik"])),
 x("A · VitrA gamı: kategori bazında VitrA nerede?", "A · VitrA range: where is VitrA by category?"), _pop_kw(A, "A grubu: %d kelime" % S.N, "Group A: %d keywords" % S.N, False, "%d kelimeyi gör" % S.N, "See the %d keywords" % S.N),
 T_KAT,
 insight(("**VitrA kendi gamındaki aramaların hacim ağırlıklı %s ilk 10'da yer almaktadır**: %d kelimenin %s ilk 10'da, %s ilk 3'te ve %s 1. sıradadır. En güçlü olduğu kategoriler %s, en sınırlı kaldığı kategoriler %s. Search Console'un üç aylık ortalamasında da VitrA %d kelimede ilk 10'dadır.")
         % (yzd(S.VITRA["hacim10"], 0) + "'" + ek(round(S.VITRA["hacim10"]), "i").split("'")[1], S.N, ek(S.VITRA["ilk10"], "inde"), ek(S.VITRA["ilk3"], "inde"), ek(S.VITRA["bir"], "inde"),
            ", ".join("%s (%s)" % (t.lower() if t != "Banyo Mobilyaları" else "banyo mobilyası", yzd(v["hacim10"], 0)) for t, v in _iyi), ", ".join("%s (%s)" % (t.lower(), yzd(v["hacim10"], 0)) for t, v in _zay) + " olarak öne çıkmaktadır", S.VITRA["gsc10"]),
         ("**VitrA is in the top 10 for a volume-weighted %s of searches in its own range**: in the top 10 for %d of %d keywords, top 3 for %d and first for %d. Its strongest categories are %s, and the most limited are %s. By the three-month Search Console average, VitrA is also in the top 10 for %d keywords.")
         % (("%.0f" % S.VITRA["hacim10"]) + "%", S.VITRA["ilk10"], S.N, S.VITRA["ilk3"], S.VITRA["bir"], ", ".join("%s (%s)" % (TEMA_EN.get(t, t).lower(), ("%.0f" % v["hacim10"]) + "%") for t, v in _iyi),
            ", ".join("%s (%s)" % (TEMA_EN.get(t, t).lower(), ("%.0f" % v["hacim10"]) + "%") for t, v in _zay), S.VITRA["gsc10"]), "D19"),
 x("A · Kim sıralanıyor?", "A · Who ranks?"),
 T_DOM,
 insight(("**VitrA gamındaki aramalarda pazaryerleri ve perakendeciler belirleyicidir**: Trendyol %d kelimenin %s ilk 10'da ve %s 1. sıradadır; onu %s izlemektedir. İlk 3 sıradaki %d yuvanın %s pazaryeri, yapı market ve fiyat karşılaştırma sitelerindedir. İlk 10 sonucun %s kategori, %s pazaryeri arama ve liste sayfasıdır.")
         % (S.N, ek(S.D10["trendyol.com"], "inde"), ek(S.D1["trendyol.com"], "inde"), _izl("ve"), _T3, yzd(100 * _P3 / _T3, 0) + "'" + ek(round(100 * _P3 / _T3), "i").split("'")[1],
            yzd(S.TIP_PAY.get("kategori", 0), 0) + "'" + ek(round(S.TIP_PAY.get("kategori", 0)), "i").split("'")[1], yzd(S.TIP_PAY.get("pazaryeri arama/liste", 0), 0) + "'" + ek(round(S.TIP_PAY.get("pazaryeri arama/liste", 0)), "i").split("'")[1]),
         ("**Marketplaces and retailers are decisive in searches in VitrA's range**: Trendyol is in the top 10 for %d of %d keywords and first for %d; %s follow. %s of the %d top-3 slots are held by marketplaces, DIY retailers and price comparison sites. %s of top-10 results are category pages and %s marketplace search and listing pages.")
         % (S.D10["trendyol.com"], S.N, S.D1["trendyol.com"], _izl("and"), ("%.0f" % (100 * _P3 / _T3)) + "%", _T3,
            ("%.0f" % S.TIP_PAY.get("kategori", 0)) + "%", ("%.0f" % S.TIP_PAY.get("pazaryeri arama/liste", 0)) + "%"), "D19"),
 x("A · VitrA'nın ilk 20'de görünmediği kelimeler", "A · Keywords where VitrA is not in the top 20"),
 T_BOS,
 insight(("VitrA gamındaki %d kelimenin %s vitra.com.tr ilk 20'de görünmemektedir; bunların toplam aylık hacmi %s'dir. %s bu kelimelerin en büyükleridir. Bu kelimelerin %s Search Console ortalamasında VitrA ilk 10'dadır; bu kelimelerde görünürlük gün ve cihaza göre değişmektedir.")
         % (S.N, ek(len(BOS), "inde"), k(sum(r["hacim"] for r in BOS)), ", ".join('"%s" (%s)' % (r["kelime"], k(r["hacim"])) for r in BOS[:4]), ek(len(_BOS_GSC), "inde")),
         ("For %d of the %d keywords in VitrA's range, vitra.com.tr does not appear in the top 20; their total monthly volume is %s. The largest are %s. For %d of these keywords VitrA is in the top 10 by Search Console average; visibility in these keywords varies by day and device.")
         % (len(BOS), S.N, k(sum(r["hacim"] for r in BOS)).replace(",", "."), ", ".join('"%s" (%s)' % (r["kelime"], k(r["hacim"]).replace(",", ".")) for r in BOS[:4]), len(_BOS_GSC)), "D19"),
 x("B · Yakın kategori fırsatları: aramayı kim kazanıyor?", "B · Adjacent category opportunities: who wins the search?"),
 T_B,
 insight(("**VitrA'nın satmadığı ya da kısmen sattığı yakın kategorilerde aylık %s arama bulunmaktadır** (%d kelime); bu aramaların ilk 10 sonucunun %s pazaryeri, yapı market ve fiyat karşılaştırma sitelerindedir. vitra.com.tr bu kelimelerin %s ilk 20'de görünmektedir. %s talebin en büyük olduğu temalardır. Pazaryerinin baskın olduğu temalar kanal üzerinden, içerik payının yüksek olduğu temalar ise rehber içerikle girilebilecek alanlardır; tema bazında talep ve VitrA'ya uyum ayrıca değerlendirilmiştir (Bölüm [[b:yeni]]).")
         % (k(_Bh), len(B), yzd(_Bpz, 0) + "'" + ek(round(_Bpz), "i").split("'")[1], ek(_Bv, "inde"), ", ".join("%s (%s)" % (t.lower(), k(sum(r["hacim"] for r in L))) for t, L, *_ in BT[:4])),
         ("**There are %s monthly searches in adjacent categories that VitrA does not sell or sells only partly** (%d keywords); %s of the top-10 results for these searches are marketplaces, DIY retailers and price comparison sites. vitra.com.tr appears in the top 20 for %d of these keywords. The largest themes by demand are %s. Themes dominated by marketplaces can be entered through channels, while themes with a high content share are areas that can be entered with guide content; demand by theme and fit with VitrA are assessed in Section [[b:yeni]].")
         % (k(_Bh).replace(",", "."), len(B), ("%.0f" % _Bpz) + "%", _Bv, ", ".join("%s (%s)" % (TEMA_EN.get(t, t).lower(), k(sum(r["hacim"] for r in L)).replace(",", ".")) for t, L, *_ in BT[:4])), "D19"),
 x("C · Marka ve karşılaştırma aramaları", "C · Brand and comparison searches"),
 T_C,
 insight(("**VitrA adıyla yapılan %d aramanın %s vitra.com.tr 1. sıradadır**; kalan %d aramada 1. sıra %d farklı alan adına dağılmaktadır (en sık %s). **Rakip marka adıyla yapılan %d aramada vitra.com.tr %s**; rakip markanın kendi sitesi bu aramaların %s 1. sıradadır, diğerlerinde pazaryerleri öne çıkmaktadır. \"vitra mı eca mı\", \"en iyi klozet markası\" gibi %d karşılaştırma ve marka seçimi aramasında vitra.com.tr %d kelimede ilk 10'dadır; bu aramalarda ilk 10 sonucun %s rehber, forum, video ve sosyal içeriktir. Karşılaştırma sorularına markanın kendi sayfasında yanıt verilmesi, kullanıcının karar anında VitrA'nın kendi anlatımıyla karşılaşmasını destekleyebilir.")
         % (len(_CV), ek(_CVk, "inde"), len(_CV) - _CVk, len(_CVar), "%s, %d" % _CVar.most_common(1)[0] if _CVar else "-", len(_CR), ("%d kelimede ilk 10'dadır" % _CRv) if _CRv else "hiçbirinde ilk 10'da yer almamaktadır", ek(_CRk, "inde"), len(_CK), _CKv,
            yzd(100 * sum(_CKt[t] for t in ("blog/rehber", "forum/şikayet", "video", "sosyal/görsel")) / _CKtt, 0) + "'" + ek(round(100 * sum(_CKt[t] for t in ("blog/rehber", "forum/şikayet", "video", "sosyal/görsel")) / _CKtt), "i").split("'")[1]),
         ("**vitra.com.tr is first for %d of %d searches with the VitrA name**; in the remaining %d searches first place is spread across %d domains (most often %s). **In %d searches with a competitor brand name, vitra.com.tr %s**; the competitor's own site is first in %d of these searches, and marketplaces lead in the others. In %d comparison and brand choice searches such as \"vitra mı eca mı\" and \"en iyi klozet markası\", vitra.com.tr is in the top 10 for %d keywords; %s of the top-10 results in these searches are guide, forum, video and social content. Answering comparison questions on the brand's own pages can help users meet VitrA's own account at the moment of decision.")
         % (_CVk, len(_CV), len(_CV) - _CVk, len(_CVar), "%s, %d" % _CVar.most_common(1)[0] if _CVar else "-", len(_CR), ("is in the top 10 for %d keywords" % _CRv) if _CRv else "is not in the top 10 for any of them", _CRk, len(_CK), _CKv,
            ("%.0f" % (100 * sum(_CKt[t] for t in ("blog/rehber", "forum/şikayet", "video", "sosyal/görsel")) / _CKtt)) + "%"), "D19"),
 x("SERP özellikleri ve AI Overview", "SERP features and AI Overview"),
 T_OZ,
 insight(("AI Overview %d kelimenin %s çıkmıştır; A grubunda %d, B grubunda %d ve C grubunda %d kelimede görülmektedir. İçeriği alınabilen %d bloğun %s VitrA kaynak gösterilmektedir (VitrA gamında %d / %d, yakın kategorilerde %d / %d, marka ve karşılaştırma aramalarında %d / %d); %s en büyük örneklerdir. VitrA'nın kaynak gösterildiği kelimelerin %s VitrA organik olarak da 1. sıradadır. Bu gözlemde organik sonuç sayfasında Shopping bloğu yer almamış, ürün listeleri organik sonuç olarak pazaryeri ve karşılaştırma sayfalarında görünmüştür; Shopping sekmesindeki ilanlar ayrıca incelenmiştir (Bölüm [[b:fiyat]]).")
         % (S.NT, ek(len(S.AI_GORULEN), "inde"), _AIG["A"]["gorulen"], _AIG["B"]["gorulen"], _AIG["C"]["gorulen"], len(S.AI_ICERIK), ek(len(S.AI_VITRA), "inde"), _AIG["A"]["vitra"], _AIG["A"]["icerik"], _AIG["B"]["vitra"], _AIG["B"]["icerik"], _AIG["C"]["vitra"], _AIG["C"]["icerik"], ", ".join('"%s"' % r["kelime"] for r in _vs), ek(_AI1, "inde")),
         ("AI Overview appeared for %d of %d keywords: %d in group A, %d in group B and %d in group C. VitrA is cited in %d of the %d blocks whose content could be retrieved (%d / %d in VitrA's range, %d / %d in adjacent categories, %d / %d in brand and comparison searches); the largest examples are %s. VitrA also ranks first organically for %d of the keywords where it is cited. In this observation no Shopping block appeared on the organic results page, and product lists appeared as organic results on marketplace and comparison pages; listings on the Shopping tab are examined separately in Section [[b:fiyat]].")
         % (len(S.AI_GORULEN), S.NT, _AIG["A"]["gorulen"], _AIG["B"]["gorulen"], _AIG["C"]["gorulen"], len(S.AI_VITRA), len(S.AI_ICERIK), _AIG["A"]["vitra"], _AIG["A"]["icerik"], _AIG["B"]["vitra"], _AIG["B"]["icerik"], _AIG["C"]["vitra"], _AIG["C"]["icerik"], ", ".join('"%s"' % r["kelime"] for r in _vs), _AI1), "D19"),
 x("AI Overview'da en çok kaynak gösterilen alan adları", "Domains cited most in AI Overview"), RANK_AI,
 box("DİĞER SORULAR (PEOPLE ALSO ASK)", "PEOPLE ALSO ASK", "<p>%s</p>" % x("%d kelimede toplam %d benzersiz soru derlenmiştir; %s fiyat, %s \"nedir / nasıl\" niyeti taşımakta, %s VitrA'yı adıyla sormaktadır." % (S.PAA_KELIME, S.PAA_OZ["soru"], ek(S.PAA_OZ["fiyat"], "i"), ek(S.PAA_OZ["bilgi"], "i"), ek(S.PAA_OZ["vitra"], "i")), "%d unique questions were returned across %d keywords; %d carry price intent, %d \"what / how\" intent, and %d ask about VitrA by name." % (S.PAA_OZ["soru"], S.PAA_KELIME, S.PAA_OZ["fiyat"], S.PAA_OZ["bilgi"], S.PAA_OZ["vitra"]))),
 x("Kullanıcının Google'da sorduğu sorular", "Questions users ask on Google"),
 PAA_H,
 insight("Sorular işçilik dahil toplam maliyet (\"klozet iç takım değişimi ne kadar\", \"gömme rezervuar montaj ücreti ne kadar\"), ölçü ve uyumluluk (\"klozet kapakları her klozete uyar mı\", \"banyo dolabı kaç cm olur\"), montaj ve tamir (\"gömme rezervuar neden su doldurmaz\", \"şamandıra suyu neden kesmez\") ve marka güveni (\"VitrA ve Artema aynı marka mı\", \"en iyi klozet markası hangisidir\") olmak üzere dört ihtiyaç grubunda toplanmaktadır. Bu soruların cevaplarının kategori ve ürün sayfalarında kısa soru-cevap bloklarıyla verilmesi hem organik sıralamayı hem de AI Overview'da kaynak gösterilme olasılığını destekleyebilir.",
         "The questions fall into four need groups: total cost including labour (\"klozet iç takım değişimi ne kadar\" - cost of replacing a WC inner mechanism, \"gömme rezervuar montaj ücreti ne kadar\" - concealed cistern installation fee), size and compatibility (\"klozet kapakları her klozete uyar mı\" - do toilet seats fit every WC, \"banyo dolabı kaç cm olur\" - how wide is a bathroom cabinet), installation and repair (\"gömme rezervuar neden su doldurmaz\" - why the concealed cistern does not fill, \"şamandıra suyu neden kesmez\" - why the float valve does not stop the water) and brand trust (\"VitrA ve Artema aynı marka mı\" - are VitrA and Artema the same brand, \"en iyi klozet markası hangisidir\" - which is the best WC brand). Answering these questions with short Q&A blocks on category and product pages can support both organic rankings and the likelihood of being cited in AI Overview.", "D19"),
 kaynak("Google TR mobil sonuç sayfası · %d kelime (A %d · B %d · C %d) · ilk 20 organik sonuç · %s, üç gözlem · takipteki kelimelerde sıralar SEOmonitor 03.10.2026 · Search Console sc-domain:vitra.com.tr, 1 Tem - 30 Eyl 2026 · hacim Keyword Planner, Eyl 2025 - Ağu 2026" % (S.NT, len(S.GRUP["A"]), len(S.GRUP["B"]), len(S.GRUP["C"]), _tr(S.TARIH)),
        "Google TR mobile results page · %d keywords (A %d · B %d · C %d) · top 20 organic results · %s, three observations · positions for tracked keywords from SEOmonitor 03.10.2026 · Search Console sc-domain:vitra.com.tr, 1 Jul - 30 Sep 2026 · volume Keyword Planner, Sep 2025 - Aug 2026" % (S.NT, len(S.GRUP["A"]), len(S.GRUP["B"]), len(S.GRUP["C"]), _tr(S.TARIH)), "D19", "D42", "D12", "D2"),
) + "".join(_DIALAR)
