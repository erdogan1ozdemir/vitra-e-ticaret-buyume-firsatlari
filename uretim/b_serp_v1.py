# -*- coding: utf-8 -*-
"""Bolum: Google arama sonuclari (SERP) ve AI Overview."""
from ortak import *
import serp_ozet as S
_TS = S.TEMA_SAY
DOM = []
for a_, _ in S.D10.most_common(15):
    DOM.append((a_, S.D10[a_], S.D3[a_], f1(S.ort_sira(a_)), "%s / %s / %s / %s" % tuple(str(S.TEMA_D[a_].get(t_) or "-") for t_ in ("SSG", "BM", "Armatür-duş", "Bitişik"))))
T_DOM = tablo([th("Alan adı", "Domain", "Google TR mobil ilk 10 organik sonuçta görünen alan adı.", "Domain appearing in Google TR mobile top 10 organic results."),
               th("İlk 10 (kelime)", "Top 10 (keywords)", "%d kelimeden kaçında ilk 10'da." % S.N, "In how many of %d keywords it is in the top 10." % S.N, True),
               th("İlk 3 (kelime)", "Top 3 (keywords)", "Kaç kelimede ilk 3'te.", "In how many keywords it is in the top 3.", True),
               th("Ort. sıra", "Avg. position", "Görüldüğü kelimelerdeki en iyi sıranın ortalaması.", "Average of the best position in the keywords where it appears.", True),
               th("SSG / BM / Armatür / Bitişik", "SSG / BM / Taps / Adjacent", "Tema bazında ilk 10'da görüldüğü kelime sayısı (tema büyüklükleri %d / %d / %d / %d)." % (_TS["SSG"], _TS["BM"], _TS["Armatür-duş"], _TS["Bitişik"]), "Number of keywords in the top 10 by theme (theme sizes %d / %d / %d / %d)." % (_TS["SSG"], _TS["BM"], _TS["Armatür-duş"], _TS["Bitişik"]), True)],
              [[veri_m(a), cell(b), cell(c), n(d), n(e)] for a, b, c, d, e in DOM])
import json as _json, os as _os
_SK = S.SK   # hacmi olmayan kelimeler cikarilmis, hacim Keyword Planner
_GS = {k_: v_ for k_, v_ in _json.load(open(_os.path.join(veri.V, "ham/derin/serp/gsc_109.json"), encoding="utf-8")).items() if k_ not in S.CIKAN}
_GB = _json.load(open(_os.path.join(veri.V, "ham/derin/serp/gsc_bos_kontrol.json"), encoding="utf-8"))
_GG = _json.load(open(_os.path.join(veri.V, "ham/derin/serp/google_gizli_kontrol.json"), encoding="utf-8"))["sonuc"]
_AH = _json.load(open(_os.path.join(veri.V, "ham", "autocomplete_hacim.json"), encoding="utf-8"))["kelime"]
def _hac(r):
    return r.get("hacim")
_G10 = sum(1 for v_ in _GS.values() if v_ and v_["sira"] <= 10)
TEMA = [("SSG", "SSG", "SSG"), ("BM", "BM", "BM"), ("Armatür-duş", "Armatür ve duş", "Taps and showers"), ("Yıkanma", "Yıkanma", "Bathing areas"), ("Bitişik", "Bitişik ürünler", "Adjacent products"),
        ("Hizmet", "Hizmet ve ilham", "Services and inspiration"), ("Karo", "Karo", "Tiles"), ("Soru", "Soru ve karar", "Questions and decisions"), ("Marka", "Marka", "Brand")]
TEMA_AD = {a: (b, c) for a, b, c in TEMA}
def _ilk3(r):
    ds = []
    for t_ in sorted(r.get("top10") or [], key=lambda z: z["sira"]):
        if t_["alan"] not in ds: ds.append(t_["alan"])
    return " · ".join(ds[:3])
def _kw_tablo(lst):
    rows_ = []
    for r in sorted(lst, key=lambda z: -(_hac(z) or 0)):
        g = _GS.get(r["kelime"])
        rows_.append([kw(r["kelime"]), x(*TEMA_AD[r["tema"]]), cell(_hac(r)) if _hac(r) else n("-"), n(str(r["vitra_sira"]) if r.get("vitra_sira") else "-"),
                      n(("%.1f" % g["sira"]).replace(".", ",")) if g else n("-"), cell(g["tik"]) if g else n("-"), veri_m(_ilk3(r) or "-")])
    return tablo([th("Arama kelimesi", "Search keyword", "Arama kelimesi.", "Search keyword."), th("Tema", "Theme", "Kelime grubu.", "Keyword group."),
                  th("Aylık hacim", "Monthly volume", "Google Keyword Planner, Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Google Keyword Planner, average monthly search volume, September 2025 - August 2026.", True),
                  th("VitrA sırası (SERP)", "VitrA position (SERP)", "29.09.2026 Google TR mobil tek gözlemde vitra.com.tr'nin sırası; \"-\" ilk 20'de yok.", "Position of vitra.com.tr in the single Google TR mobile observation of 29.09.2026; \"-\" not in top 20.", True),
                  th("Search Console ort. sıra", "Search Console avg. position", "26.06 - 25.09.2026 ortalama sıra, tüm cihazlar; \"-\" gösterim yok.", "Average position 26.06 - 25.09.2026, all devices; \"-\" no impressions.", True),
                  th("Search Console click", "Search Console clicks", "Aynı dönemde bu kelimeden gelen click.", "Clicks from this keyword in the same period.", True),
                  th("İlk 3 alan adı", "Top 3 domains", "SERP gözleminde ilk üç organik sonucun alan adı.", "Domains of the first three organic results in the SERP observation.")], rows_, "uzun")
_POP109, _DIA109 = pop("%d kelime: hacim, VitrA sırası ve ilk 3 alan adı" % S.N, "%d keywords: volume, VitrA position and top 3 domains" % S.N, _kw_tablo(_SK), "%d kelimeyi gör" % S.N, "See the %d keywords" % S.N)
_DIALAR = [_DIA109]
VT = []
for kod, tr_, en_ in TEMA:
    lst = [r for r in _SK if r["tema"] == kod]
    b_, d_ = pop("%s: kelimeler ve metrikler" % tr_, "%s: keywords and metrics" % en_, _kw_tablo(lst), ikon=True)
    _DIALAR.append(d_)
    s3 = sum(1 for r in lst if r.get("vitra_sira") and r["vitra_sira"] <= 3); s10 = sum(1 for r in lst if r.get("vitra_sira") and r["vitra_sira"] <= 10)
    g10 = sum(1 for r in lst if _GS.get(r["kelime"]) and _GS[r["kelime"]]["sira"] <= 10); yok = sum(1 for r in lst if not r.get("vitra_sira"))
    VT.append([x(tr_, en_) + b_, cell(len(lst)), cell(s3), cell(s10), cell(g10), cell(yok)])
T_VT = tablo([th("Tema", "Theme", "Kelime grubu; ok simgesi temadaki kelimeleri ve metriklerini açar.", "Keyword group; the arrow opens the theme's keywords and metrics."), th("Kelime", "Keywords", "Temadaki kelime sayısı.", "Number of keywords in the theme.", True),
              th("VitrA ilk 3 (SERP)", "VitrA top 3 (SERP)", "29.09.2026 mobil gözlemde vitra.com.tr'nin ilk 3'te olduğu kelime sayısı.", "Keywords where vitra.com.tr is in the top 3 in the mobile observation of 29.09.2026.", True),
              th("VitrA ilk 10 (SERP)", "VitrA top 10 (SERP)", "Aynı gözlemde ilk 10'da olduğu kelime sayısı.", "Keywords in the top 10 in the same observation.", True),
              th("VitrA ilk 10 (Search Console)", "VitrA top 10 (Search Console)", "Search Console'da 26.06 - 25.09.2026 ortalama sırası 10 ve altında olan kelime sayısı; tüm cihazlar.", "Keywords with an average Search Console position of 10 or better, 26.06 - 25.09.2026; all devices.", True),
              th("SERP'te ilk 20'de yok", "Not in top 20 (SERP)", "Tek günlük gözlemde vitra.com.tr'nin ilk 20'de görünmediği kelime sayısı.", "Keywords where vitra.com.tr does not appear in the top 20 in the single-day observation.", True)], VT)
BOS = [("su arıtma cihazı", 73458), ("termosifon", 61500), ("banyo bataryası", 39267), ("taharet musluğu", 37417), ("tesisatçı", 36800), ("şofben", 36075), ("jakuzi", 28967), ("banyo paspası", 26717), ("dolap kulpu", 24242), ("mutfak tezgahı", 24242), ("lavabo bataryası", 23833), ("fayans fiyatları", 23425),
       ("banyo seti", 23017), ("çamaşır sepeti", 21308), ("evye", 18783), ("havlupan", 16642), ("derz dolgu", 14675), ("banyo rafı", 10708), ("gömme rezervuar iç takımı", 4650), ("granit evye", 4667), ("klozet kapağı menteşesi", 4483), ("geberit gömme rezervuar", 3933), ("creavit klozet", 3800), ("kanalsız klozet", 2025)]
def _gsira(kw_):
    l_ = _GG.get(kw_) or []
    return (l_.index("vitra.com.tr") + 1) if "vitra.com.tr" in l_ else None
brow = []
BOS = [(k_, (S.KP.get(k_) or {}).get("ort12") or h_) for k_, h_ in BOS]
for kw_, h_ in sorted(BOS, key=lambda i: -i[1]):
    gb = _GS.get(kw_) or {}; gs = _gsira(kw_); ilk5 = [("-" if d == "?" else d) for d in (_GG.get(kw_) or [])][:5]
    brow.append([kw(kw_), cell(h_), n(("%.1f" % gb["sira"]).replace(".", ",")) if gb.get("sira") else n("-"), cell(gb.get("tik") or 0), n(str(gs)) if gs else n("-"),
                 veri_m(" · ".join(ilk5)), n(x("İlk sayfada", "On page 1")) if gs else n(x("İlk sayfada yok", "Not on page 1"))])
BOS_VAR = [kw_ for kw_, _ in BOS if _gsira(kw_)]
T_BOS = tablo([th("Arama kelimesi", "Search keyword", "29.09.2026 mobil SERP gözleminde vitra.com.tr'nin ilk 20'de görünmediği kelime.", "Keyword where vitra.com.tr did not appear in the top 20 in the mobile SERP observation of 29.09.2026."),
               th("Aylık hacim", "Monthly volume", "Google Keyword Planner, Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Google Keyword Planner, average monthly search volume, September 2025 - August 2026.", True),
               th("Search Console ort. sıra", "Search Console avg. position", "vitra.com.tr'nin bu sorgudaki 26.06 - 25.09.2026 ortalama sırası (sorgu düzeyinde, tüm cihazlar); \"-\" sorgu raporda yok.", "vitra.com.tr average position for this query, 26.06 - 25.09.2026 (query level, all devices); \"-\" query not in the report.", True),
               th("Search Console click", "Search Console clicks", "Aynı dönemde bu kelimeden gelen click.", "Clicks from this keyword in the same period.", True),
               th("Google sırası (30.09)", "Google position (30.09)", "google.com.tr, oturumsuz arama, 30.09.2026; ilk sayfadaki organik sonuçlar arasında vitra.com.tr'nin sırası; \"-\" ilk sayfada yok.", "google.com.tr, signed-out search, 30.09.2026; position of vitra.com.tr among first-page organic results; \"-\" not on page 1.", True),
               th("İlk 5 sonuç (30.09)", "Top 5 results (30.09)", "Aynı Google kontrolünde ilk beş organik sonucun alan adı, sırasıyla; \"-\" alan adı okunamayan sonuç.", "Domains of the first five organic results in the same Google check, in order; \"-\" a result whose domain could not be read."),
               th("Durum", "Status", "VitrA'nın 30.09.2026 Google ilk sayfasındaki varlığı.", "VitrA's presence on the Google first page on 30.09.2026.")], brow, "uzun")
_pzb = [S.tema_pz3(t_) for t_ in ("BM", "Armatür-duş", "Bitişik")]
_pzr = sorted(round(100 * a_ / b_) for a_, b_ in _pzb)
_PZB = ("%%%d" % _pzr[0]) if _pzr[0] == _pzr[-1] else ("%%%d-%d" % (_pzr[0], _pzr[-1]))
_AI1 = sum(1 for r_ in S.SK if r_["kelime"] in S.AI_VITRA and r_.get("vitra_sira") == 1)
def _iy(n_): return ek(n_, "i").split("'")[1]
_PZB_EK = _PZB + "'" + ek(_pzr[-1], "inde").split("'")[1]
_PZBE = ("%d%%" % _pzr[0]) if _pzr[0] == _pzr[-1] else ("%d-%d%%" % (_pzr[0], _pzr[-1]))
TEMA_KISA = {"SSG": ("SSG", "SSG"), "BM": ("BM", "BM"), "Armatür-duş": ("armatür", "taps"), "Yıkanma": ("yıkanma", "bathing"), "Bitişik": ("bitişik", "adjacent"), "Hizmet": ("hizmet", "services"), "Karo": ("karo", "tiles"), "Soru": ("soru", "questions"), "Marka": ("marka", "brand")}
def _oz(k_, tr_, en_, ek_tr=None, ek_en=None):
    n_, tm = S.ozellik(k_)
    yog = sorted(tm, key=lambda t_: (-tm[t_] / _TS[t_], -tm[t_]))[:3]
    yt = ek_tr or ", ".join("%s %d/%d" % (TEMA_KISA[t_][0], tm[t_], _TS[t_]) for t_ in yog)
    ye = ek_en or ", ".join("%s %d/%d" % (TEMA_KISA[t_][1], tm[t_], _TS[t_]) for t_ in yog)
    return (tr_, en_, "%d (%s)" % (n_, yzd(100 * n_ / S.N, 0)), "%d / %d / %d / %d" % tuple(tm.get(t_, 0) for t_ in ("SSG", "BM", "Armatür-duş", "Bitişik")), yt[:1].upper() + yt[1:], ye[:1].upper() + ye[1:])
OZ = [_oz("ai", "AI Overview", "AI Overview"), _oz("paa", "People Also Ask", "People Also Ask"), _oz("video", "Video / Shorts", "Video / Shorts"),
      _oz("yerel", "Yerel sonuçlar (Local pack)", "Local results (Local pack)"), _oz("ilan", "İlan ve hizmet platformları (Sahibinden, Armut)", "Listing and service platforms (Sahibinden, Armut)"),
      ("Shopping / ürün listeleme", "Shopping / product listings", "0", "0 / 0 / 0 / 0", "Organik sonuç sayfasında yer almadı", "Did not appear on the organic results page")]
T_OZ = tablo([th("SERP özelliği", "SERP feature", "Arama sonuç sayfasında organik sonuç dışındaki blok.", "Block on the results page other than organic results."),
              th("Kelime (pay)", "Keywords (share)", "%d kelimeden kaçında görüldüğü." % S.N, "In how many of %d keywords it appeared." % S.N, True),
              th("SSG / BM / Armatür / Bitişik", "SSG / BM / Taps / Adjacent", "Tema bazında görüldüğü kelime sayısı.", "Keywords by theme where it appeared.", True),
              th("En yoğun olduğu temalar", "Themes where most frequent", "En yüksek görülme oranı.", "Highest occurrence rate.")], [[x(a, b), n(c), n(d), x(e, f)] for a, b, c, d, e, f in OZ])
import collections as _col
_T3, _P3 = S.ILK3["yuva"], S.ILK3["pz"]
_AIC = S.AI_ALAN
AI = sorted(_AIC.items(), key=lambda t_: (-t_[1], t_[0]))[:12]   # esit sayida olanlar alfabetik
RANK_AI = rank_list([(veri_m(a), b) for a, b in AI], max(b_ for _, b_ in AI), you=lambda e: "vitra" in e, fmt=lambda v: bin(v))
PAA = [("Fiyat", "Price", ["Klozet yaptırmak kaç TL?", "Klozet iç takım değişimi ne kadar?", "Banyo dolabı fiyatları ne kadar?", "Bir banyo tadilatı ne kadara mal olur?", "Arıtma taktırmak kaç TL?"]),
       ("Ölçü ve seçim", "Size and selection", ["Klozet kapakları standart mı?", "Banyo dolabı yüksekliği kaç santim olmalı?", "Kanallı klozet mi iyi kanalsız mı?", "Gömme rezervuar mantıklı mı?", "MDF banyo dolabı suya dayanıklı mı?"]),
       ("Montaj ve tamir", "Installation and repair", ["Klozet montajı kaç TL?", "Klozet değişimini kim yapar?", "Klozet suyu neden durmuyor?", "Taharet musluğu değişimi kaç TL?", "Banyo fayansları kırılmadan nasıl yenilenir?"]),
       ("VitrA ve marka", "VitrA and brand", ["VitrA iyi marka mı?", "VitrA ve Artema aynı marka mı?", "VitrA gömme rezervuar neden su doldurmuyor?", "Bataryada E.C.A. mı Artema mı?", "Artema hangi ülkenin markası?"])]
PAA_H = '<div class="fnotes">%s</div>' % "".join('<article class="fnote"><span class="fc">%s</span><ul>%s</ul></article>' % (x(a, b), "".join("<li>%s</li>" % veri_m(q) for q in qs)) for a, b, qs in PAA)
HTML = """
<p class="lede">%s</p>
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
<div class="split"><div>%s</div>%s</div>
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Google Türkiye mobil arama sonuçlarının ilk 20 organik sonucu ve SERP özellikleri %d kelime için incelenmiştir. Kelimeler sabit bir hacim sıralamasıyla değil, VitrA'nın kategori ağacını ve fırsat alanlarını temsil edecek biçimde dokuz temadan seçilmiştir: SSG, banyo mobilyası, armatür ve duş, yıkanma alanları, bitişik ürünler, hizmet ve ilham, karo, soru ve marka. Her temada ana kelime, fiyat ifadeli biçimi ve önemli alt tipler alınmış; Google Keyword Planner'da arama hacmi olmayan kelimeler analizden çıkarılmıştır. Sonuçlar 29 Eylül 2026 tarihli tek gözlemdir." % S.N,
   "The top 20 organic results and SERP features of Google Turkey mobile results were examined for %d keywords. The keywords were not taken from a fixed volume ranking but chosen from nine themes to represent VitrA's category tree and opportunity areas: SSG, bathroom furniture, taps and showers, bathing areas, adjacent products, services and inspiration, tiles, questions and brand. In each theme the head term, its price variant and important sub-types were taken; keywords with no search volume in Google Keyword Planner were removed from the analysis. The results are a single observation dated 29 September 2026." % S.N),
 kpi_kart(yzd(100 * S.D10["trendyol.com"] / S.N, 0), "Trendyol'un ilk 10'da olduğu kelime payı · %d kelimede 1. sıra" % S.D1["trendyol.com"], "Share of keywords with Trendyol in the top 10 · first place in %d keywords" % S.D1["trendyol.com"], "hi"),
 kpi_kart(yzd(100 * _P3 / _T3, 0), "Pazaryeri, yapı market ve fiyat karşılaştırma sitelerinin ilk 3 sıralardaki payı (%d yuvanın %s)" % (_T3, ek(_P3, "i")), "Share of top-3 slots held by marketplaces, DIY retailers and price comparison sites (%d of %d slots)" % (_P3, _T3)),
 kpi_kart("%d / %d" % (_G10, S.N), "Search Console'da VitrA'nın ortalama ilk 10'da olduğu kelime (26.06 - 25.09.2026); tek günlük mobil SERP gözleminde %d, %s 1. sıra" % (S.VITRA["ilk10"], ek(S.VITRA["bir"], "inde")), "Keywords where VitrA's average Search Console position is in the top 10 (26.06 - 25.09.2026); %d in the single-day mobile SERP observation, first in %d" % (S.VITRA["ilk10"], S.VITRA["bir"]), "up"),
 kpi_kart("%d / %d" % (len(S.AI_VITRA), len(S.AI_ICERIK)), "VitrA'nın referans verildiği AI Overview (içeriği alınan %d blok)" % len(S.AI_ICERIK), "AI Overviews citing VitrA (of %d blocks with content)" % len(S.AI_ICERIK)),
 x("Kim sıralanıyor?", "Who ranks?"), _POP109,
 T_DOM,
 insight(("Arama sonuçlarında pazaryerleri ve perakendeciler belirleyicidir: Trendyol %d kelimenin %s ilk 10'da ve %s 1. sıradadır; Koçtaş (%d), Hepsiburada (%d), vitra.com.tr (%d) ve Akakçe (%d) onu izlemektedir. Banyo mobilyası, armatür ve bitişik ürün kelimelerinin %s en az bir pazaryeri veya perakendeci ilk 3'tedir. İlk 10 sonucun %s kategori, %s pazaryeri arama ve liste sayfasıdır; ürün sayfalarının payı %%3'ün altındadır. Hizmet ve soru kelimelerinde ise tablo değişmekte; Armut, Pinterest, YouTube ve rehber içerikleri öne çıkmaktadır.")
         % (S.N, ek(S.D10["trendyol.com"], "inde"), ek(S.D1["trendyol.com"], "inde"), S.D10["koctas.com.tr"], S.D10["hepsiburada.com"], S.D10["vitra.com.tr"], S.D10["akakce.com"], _PZB_EK, yzd(S.TIP_PAY["kategori"], 0) + "'" + _iy(round(S.TIP_PAY["kategori"])), yzd(S.TIP_PAY["pazaryeri arama/liste"], 0) + "'" + _iy(round(S.TIP_PAY["pazaryeri arama/liste"]))),
         ("Marketplaces and retailers are decisive in search results: Trendyol is in the top 10 for %d of %d keywords and first for %d; Koçtaş (%d), Hepsiburada (%d), vitra.com.tr (%d) and Akakçe (%d) follow. In %s of bathroom furniture, tap and adjacent product keywords at least one marketplace or retailer is in the top 3. %s of top-10 results are category pages and %s marketplace search and listing pages; product pages are under 3%%. For service and question keywords the picture changes, with Armut, Pinterest, YouTube and guide content coming to the fore.")
         % (S.D10["trendyol.com"], S.N, S.D1["trendyol.com"], S.D10["koctas.com.tr"], S.D10["hepsiburada.com"], S.D10["vitra.com.tr"], S.D10["akakce.com"], _PZBE, ("%.0f" % S.TIP_PAY["kategori"]) + "%", ("%.0f" % S.TIP_PAY["pazaryeri arama/liste"]) + "%"), "D19"),
 x("VitrA nerede?", "Where is VitrA?"),
 T_VT,
 insight("VitrA SSG'de güçlüdür: 16 kelimenin 12'sinde ilk 3'te; klozet, asma klozet, akıllı klozet, lavabo ve bidede, BM'de ise lavabo dolabında 1. sıradadır. Tek günlük mobil gözlem armatürde 13 kelimenin 8'inde VitrA'yı ilk 20 dışında göstermektedir; ancak Search Console ve 30.09.2026 Google kontrolü banyo ve lavabo bataryasında vitra.com.tr'nin 3. sırada olduğunu göstermektedir (Search Console ortalama sırası %s, 26 Haziran - 25 Eylül 2026 döneminde %s tık). Search Console ortalama sırasına göre VitrA %d kelimenin %s ilk 10'dadır. Tek günlük gözlemde belirgin boşluk bitişik ürünlerde (24 kelimenin tek günlük gözlemde 3'ünde, Search Console ortalamasında 7'sinde ilk 10) ve taharet musluğu, robot duş seti, sifon gibi tamamlayıcı armatürlerde kalmaktadır. artema.com.tr ilk 10'da yalnızca %d kelimede görünmektedir." % (("%.1f" % _GS["banyo bataryası"]["sira"]).replace(".", ","), bin(_GS["banyo bataryası"]["tik"]), S.N, ek(_G10, "inde"), S.VITRA["artema10"]),
         "VitrA is strong in SSG: in the top 3 for 12 of 16 keywords and first for WC, wall-hung WC, smart WC, washbasin and bidet, and in BM for basin unit. The single-day mobile observation shows VitrA outside the top 20 for 8 of 13 tap keywords; however Search Console and the Google check of 30.09.2026 show vitra.com.tr in 3rd place for bath and basin taps (Search Console average position %s, %s clicks in 26 June - 25 September 2026). By Search Console average position, VitrA is in the top 10 for %d of %d keywords. In the single-day observation the clear gap remains in adjacent products (top 10 for 3 of 24 keywords in the single-day observation and 7 by Search Console average) and in complementary taps such as bidet valves, rain shower sets and siphons. artema.com.tr appears in the top 10 for only %d keywords." % ("%.1f" % _GS["banyo bataryası"]["sira"], "{:,}".format(_GS["banyo bataryası"]["tik"]), _G10, S.N, S.VITRA["artema10"]), "D19", "D2"),
 x("Tek günlük gözlemde VitrA'nın ilk 20'de görünmediği kelimeler: SERP, Search Console ve Google kontrolü", "Keywords where VitrA did not appear in the top 20 in the single-day observation: SERP, Search Console and Google check"),
 T_BOS,
 insight("Tek günlük mobil gözlemde VitrA'nın ilk 20'de görünmediği %d kelimenin %s 30.09.2026 Google kontrolünde vitra.com.tr ilk sayfadadır: banyo ve lavabo bataryasında 3., kanalsız klozette 4., evye ve jakuzide 6. sırada. Kalan kelimelerin çoğu VitrA'nın ürün ailesi dışındaki bitişik ürünlerdir (su arıtma, termosifon, şofben, paspas, çamaşır sepeti, derz dolgu); bu kelimelerde Trendyol, Koçtaş ve Hepsiburada ilk sıraları paylaşmaktadır. VitrA'nın ürünü olup ilk sayfada yer almadığı kelimeler havlupan, taharet musluğu, banyo rafı, gömme rezervuar iç takımı, klozet kapağı menteşesi ve dolap kulpudur; bu kelimelerde Search Console ortalama sırası yaklaşık 10 ile 20 arasındadır (dolap kulpunda sorgu raporda yer almamaktadır)." % (len(BOS), ek(len(BOS_VAR), "inde")),
         "For %d of the %d keywords where the single-day mobile observation showed VitrA outside the top 20, vitra.com.tr is on the first page in the Google check of 30.09.2026: 3rd for bath and basin taps, 4th for rimless WCs and 6th for sinks and whirlpools. Most of the remaining keywords are adjacent products outside VitrA's range (water purifiers, storage water heaters, instantaneous water heaters, mats, laundry baskets, grout), where Trendyol, Koçtaş and Hepsiburada share the top positions. The keywords where VitrA has products but is not on the first page are towel radiators, bidet valves, bathroom shelves, concealed cistern inner mechanisms, toilet seat hinges and cabinet handles; their average Search Console position ranges from about 10 to 20 (the cabinet handle query does not appear in the report)." % (len(BOS_VAR), len(BOS)), "D19", "D2"),
 x("SERP özellikleri ve AI Overview", "SERP features and AI Overview"),
 T_OZ,
 insight(("AI Overview %d kelimede çıkmıştır ve en yoğun olduğu yer soru kelimeleridir (%s %s). VitrA %d AI Overview'da kaynak gösterilmektedir: %s. Bu kelimelerin %s VitrA organik olarak da 1. sıradadır. Bitişik ürünlerde (elektrikli havlupan, derz dolgu, ısıtmalı klozet kapağı, şamandıra) AI Overview çıkmakta, VitrA kaynak gösterilmemektedir. Bu gözlemde organik sonuç sayfasında Shopping bloğu yer almamış, ürün listeleri organik sonuç olarak pazaryeri ve karşılaştırma sayfalarında görünmüştür; Shopping sekmesindeki ilanlar Bölüm [[b:fiyat]]'da ayrıca incelenmiştir.")
         % (len(S.AI_GORULEN), ek(_TS["Soru"], "in"), ek(S.ozellik("ai")[1].get("Soru", 0), "i"), len(S.AI_VITRA), ", ".join('"%s"' % k_ for k_ in S.AI_VITRA), ek(_AI1, "inde")),
         ("AI Overview appeared for %d keywords and is most frequent for question keywords (%d of %d). VitrA is cited in %d AI Overviews: %s. VitrA also ranks first organically for %d of these keywords. For adjacent products (electric towel radiator, grout, heated toilet seat, float valve) AI Overview appears without citing VitrA. In this observation no Shopping block appeared on the organic results page, and product lists appeared as organic results on marketplace and comparison pages; listings on the Shopping tab are examined separately in Section [[b:fiyat]].")
         % (len(S.AI_GORULEN), S.ozellik("ai")[1].get("Soru", 0), _TS["Soru"], len(S.AI_VITRA), ", ".join('"%s"' % k_ for k_ in S.AI_VITRA), _AI1), "D19"),
 x("AI Overview'da en çok kaynak gösterilen alan adları", "Domains cited most in AI Overview"), RANK_AI,
 box("PEOPLE ALSO ASK", "PEOPLE ALSO ASK", "<p>%s</p>" % x("%d kelimede toplam %d benzersiz soru derlenmiştir; %s fiyat, %s \"nedir / nasıl\" niyeti taşımakta, %s VitrA'yı adıyla sormaktadır." % (S.PAA_KELIME, S.PAA_OZ["soru"], ek(S.PAA_OZ["fiyat"], "i"), ek(S.PAA_OZ["bilgi"], "i"), ek(S.PAA_OZ["vitra"], "i")), "%d unique questions were returned across %d keywords; %d carry price intent, %d \"what / how\" intent, and %d ask about VitrA by name." % (S.PAA_OZ["soru"], S.PAA_KELIME, S.PAA_OZ["fiyat"], S.PAA_OZ["bilgi"], S.PAA_OZ["vitra"]))),
 x("Kullanıcının Google'da sorduğu sorular", "Questions users ask on Google"),
 PAA_H,
 insight("Sorular dört ihtiyaç grubunda toplanmaktadır: işçilik dahil toplam maliyet (\"klozet yaptırmak kaç TL\", \"iç takım değişimi ne kadar\"), ölçü ve uyumluluk (\"klozet kapakları standart mı\", \"banyo dolabı yüksekliği\"), montaj ve tamir (\"klozet değişimini kim yapar\", \"klozet suyu neden durmuyor\") ve marka güveni (\"VitrA iyi marka mı\", \"VitrA ve Artema aynı marka mı\"). Bu soruların cevaplarının kategori ve ürün sayfalarında kısa soru-cevap bloklarıyla verilmesi hem organik sıralamayı hem de AI Overview'da kaynak gösterilme olasılığını destekleyebilir.",
         "The questions fall into four need groups: total cost including labour (\"klozet yaptırmak kaç TL\" - how much to have a WC fitted, \"iç takım değişimi ne kadar\" - cost of replacing an inner mechanism), size and compatibility (\"klozet kapakları standart mı\" - are toilet seats standard, \"banyo dolabı yüksekliği\" - bathroom cabinet height), installation and repair (\"klozet değişimini kim yapar\" - who replaces a WC, \"klozet suyu neden durmuyor\" - why the WC keeps running) and brand trust (\"VitrA iyi marka mı\" - is VitrA a good brand, \"VitrA ve Artema aynı marka mı\" - are VitrA and Artema the same brand). Answering these questions with short Q&A blocks on category and product pages can support both organic rankings and the likelihood of being cited in AI Overview.", "D19"),
 kaynak("Google TR mobil sonuç sayfası · %d kelime · ilk 20 organik sonuç · 29.09.2026 · Search Console sc-domain:vitra.com.tr, 26.06 - 25.09.2026 · google.com.tr oturumsuz kontrol, 24 kelime, 30.09.2026 · hacim Keyword Planner", "Google TR mobile results page · %d keywords · top 20 organic results · 29.09.2026 · Search Console sc-domain:vitra.com.tr, 26.06 - 25.09.2026 · google.com.tr signed-out check, 24 keywords, 30.09.2026 · volume Keyword Planner" % S.N, "D19", "D12", "D2"),
) + "".join(_DIALAR)
