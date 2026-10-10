# -*- coding: utf-8 -*-
"""Bölüm: Google yapay zeka özellikleri ve organik tık.
Veri: Search Console yapay zeka özellikleri raporu dışa aktarımı (18 May - 29 Eyl 2026, /ilham-veren-fikirler/ filtreli),
Search Console API (blog sayfaları ve sorguları, 1 Haz - 29 Eyl 2025 ve 2026), Ahrefs SERP özellikleri (blog kelimeleri, 01.10.2026 ve 15.09.2025)."""
from ortak import *
import json as _json, os as _os, datetime as _dt
from rapor_parca1 import cizgi
from b_talep import sekmeler
import gsc12 as _G12
G2 = _json.load(open(_os.path.join(veri.V, "islenmis", "gsc2.json"), encoding="utf-8"))
GG, BG, SG = G2["genai_gun"], G2["blog_gun"], G2["gun"]
def _isr(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + "%" + ("%.1f" % abs(v)).replace(".", ",")
def _isr_en(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + ("%.1f" % abs(v)) + "%"
def _pe(v): return ("%.1f" % v) + "%"
def _deg(a, b): return (b / a - 1) * 100 if a else None
def _s(v): return ("%.1f" % v).replace(".", ",")
GAYT = {"01": ("Oca", "Jan"), "02": ("Şub", "Feb"), "03": ("Mar", "Mar"), "04": ("Nis", "Apr"), "05": ("May", "May"), "06": ("Haz", "Jun"), "07": ("Tem", "Jul"), "08": ("Ağu", "Aug"), "09": ("Eyl", "Sep"), "10": ("Eki", "Oct"), "11": ("Kas", "Nov"), "12": ("Ara", "Dec")}
def _gun(d, en=False): return "%d %s" % (int(d[8:]), GAYT[d[5:7]][1 if en else 0])
D0, D1 = min(GG), max(GG)
GT_ = sum(GG.values()); BT_ = sum(BG[d][1] for d in GG if d in BG); ST_ = sum(SG[d][1] for d in GG if d in SG)

# ---------------------------------------------------------------- 1 · site geneli ve blog: haftalık seri ve aylık pay
from grafik2 import kombo2 as _kombo2, f_k as _fk2
GS_ = G2["genai_site_gun"]; GST = sum(GS_.values())
_bas = _dt.date.fromisoformat(D0); _son = _dt.date.fromisoformat(D1)
HAFTA = []
d = _bas
while d + _dt.timedelta(days=6) <= _son:
    gun = [(d + _dt.timedelta(days=i)).isoformat() for i in range(7)]
    HAFTA.append((gun[0], sum(GG.get(g, 0) for g in gun), sum(BG.get(g, [0, 0])[1] for g in gun), sum(BG.get(g, [0, 0])[0] for g in gun),
                  sum(GS_.get(g, 0) for g in gun), sum(SG.get(g, [0, 0])[1] for g in gun)))
    d += _dt.timedelta(days=7)
ETK = [_gun(h[0]) for h in HAFTA]
for h in HAFTA: x(_gun(h[0]), _gun(h[0], True))
def _pb(v): return x(("%" + ("%.1f" % v).replace(".", ",")), ("%.1f" % v) + "%")
def _pbs(v): return x(_isr(v), _isr_en(v))
def _ortu(top_i, ic_i, top_ad, ic_ad, cap_tr, cap_en):
    return _kombo2(ETK, [{"ad": x(*top_ad), "renk": "#C9D3D1", "deger": [h[top_i] for h in HAFTA], "tip": "cubuk", "bicim": _fk2, "eksen_ad": x("Gösterim", "Impressions")},
                         {"ad": x(*ic_ad), "renk": "#E85F36", "deger": [h[ic_i] for h in HAFTA], "tip": "cubuk", "ortu": True, "bicim": _fk2}],
                   cap=x(cap_tr, cap_en), ust_etiket=[_pb(100 * h[ic_i] / h[top_i]) for h in HAFTA],
                   ek_satir=[[(x("Yapay zeka payı", "AI share"), _pb(100 * h[ic_i] / h[top_i]))] for h in HAFTA])
G_SERI = sekmeler([("Site geneli", "Site-wide", _ortu(5, 4, ("Site toplam gösterimi", "Total site impressions"), ("Yapay zeka özelliklerinde gösterim", "Impressions in AI features"),
                        "Haftalık gösterim · site toplamı (gri çubuk) ve içinde yapay zeka özelliklerindeki gösterim (turuncu); çubuk üstündeki oran yapay zeka payıdır, hafta başlangıcı Pazartesi, %s - %s" % (_gun(D0), _gun(HAFTA[-1][0])),
                        "Weekly impressions · site total (grey bar) with impressions in AI features inside it (orange); the figure above the bar is the AI share, week starting Monday, %s - %s" % (_gun(D0, True), _gun(HAFTA[-1][0], True)))),
                   ("Blog", "Blog", _ortu(2, 1, ("Blog toplam gösterimi", "Total blog impressions"), ("Yapay zeka özelliklerinde gösterim · blog", "Impressions in AI features · blog"),
                        "Haftalık gösterim · blog sayfalarının toplamı (gri çubuk) ve içinde yapay zeka özelliklerindeki gösterim (turuncu); çubuk üstündeki oran blogdaki yapay zeka payıdır, /ilham-veren-fikirler/",
                        "Weekly impressions · total of blog pages (grey bar) with impressions in AI features inside it (orange); the figure above the bar is the AI share in the blog, /ilham-veren-fikirler/"))], "gtabs")
x("Mayıs (18-31)", "May (18-31)"); x("Eylül (1-29)", "September (1-29)")
_AYAD = {"05": ("Mayıs (18-31)", "May (18-31)"), "06": ("Haziran", "June"), "07": ("Temmuz", "July"), "08": ("Ağustos", "August"), "09": ("Eylül (1-29)", "September (1-29)")}
rows_ay = []
for (a, b, g, bi, si), (_, _, gs, ss, sc) in zip(G2["genai_pay"], G2["genai_site_pay"]):
    rows_ay.append([x(*_AYAD[a[5:7]]), cellk(gs), cellk(ss), n(yzd(100 * gs / ss)), cellk(g), cellk(bi), n(yzd(100 * g / bi)), n(yzd(100 * g / gs))])
rows_ay.append(["<b>%s</b>" % x("Toplam", "Total"), cellk(GST), cellk(ST_), n("<b>%s</b>" % yzd(100 * GST / ST_)), cellk(GT_), cellk(BT_), n("<b>%s</b>" % yzd(100 * GT_ / BT_)), n(yzd(100 * GT_ / GST))])
T_AY = tablo([th("Dönem", "Period", "Search Console yapay zeka özellikleri raporu 18 Mayıs 2026'da başlar; dışa aktarım 29 Eylül 2026'da biter.", "The Search Console AI features report starts on 18 May 2026; the export ends on 29 September 2026."),
              th("Yapay zeka gösterimi · site", "AI feature impressions · site", "Tüm vitra.com.tr sayfalarının Google yapay zeka özelliklerinde aldığı gösterim (Search Console, filtresiz dışa aktarım).", "Impressions all vitra.com.tr pages received in Google AI features (Search Console, unfiltered export).", True),
              th("Site toplam gösterimi", "Total site impressions", "Aynı günlerde sc-domain:vitra.com.tr web aramasındaki toplam gösterim.", "Total sc-domain:vitra.com.tr web search impressions on the same days.", True),
              th("Sitedeki pay", "Share in site", "Yapay zeka gösterimi / site toplam gösterimi.", "AI feature impressions / total site impressions.", True),
              th("Yapay zeka gösterimi · blog", "AI feature impressions · blog", "Blog sayfalarının (/ilham-veren-fikirler/) yapay zeka özelliklerinde aldığı gösterim (filtreli dışa aktarım).", "Impressions blog pages (/ilham-veren-fikirler/) received in AI features (filtered export).", True),
              th("Blog toplam gösterimi", "Total blog impressions", "Aynı günlerde blog sayfalarının web aramasındaki toplam gösterimi.", "Total web search impressions of blog pages on the same days.", True),
              th("Blogdaki pay", "Share in blog", "Blogun yapay zeka gösterimi / blog toplam gösterimi.", "The blog's AI feature impressions / total blog impressions.", True),
              th("Blogun payı", "Blog's share", "Blog sayfalarının site genelindeki yapay zeka gösterimi içindeki payı.", "The blog pages' share of site-wide AI feature impressions.", True)], rows_ay, "dar")
_pay_ay = [100 * g / bi for _, _, g, bi, _ in G2["genai_pay"]]
_spay = [100 * g / s_ for _, _, g, s_, _ in G2["genai_site_pay"]]
INS_AY = insight("18 Mayıs - 29 Eylül 2026'da vitra.com.tr sayfaları Google'ın yapay zeka özelliklerinde %s gösterim almıştır; bu, aynı günlerde sitenin toplam gösteriminin %s'idir. **Site genelindeki pay Mayıs'ın son iki haftasında %s iken Eylül'de %s'e yükselmiştir**: toplam gösterim daralırken yapay zeka özelliklerindeki gösterim artmaktadır. Blog sayfalarında pay %s ile %s arasında, sitenin üç katı düzeyinde seyretmektedir ve yapay zeka gösteriminin %s'i blogdandır. Gösterimlerin %s'i mobil cihazdandır."
                 % (k(GST), yzd(100 * GST / ST_), yzd(_spay[0]), yzd(_spay[-1]), yzd(min(_pay_ay)), yzd(max(_pay_ay)), yzd(100 * GT_ / GST), yzd(100 * G2["genai_site_cihaz"]["Mobile"] / sum(G2["genai_site_cihaz"].values()))),
                 "Between 18 May and 29 September 2026, vitra.com.tr pages received %s impressions in Google's AI features; this is %s of the site's total impressions on the same days. **The site-wide share rose from %s in the last two weeks of May to %s in September**: while total impressions contract, impressions in AI features grow. On blog pages the share moves between %s and %s, about three times the site level, and %s of AI feature impressions come from the blog. %s of these impressions are on mobile."
                 % (k(GST).replace(",", "."), _pe(100 * GST / ST_), _pe(_spay[0]), _pe(_spay[-1]), _pe(min(_pay_ay)), _pe(max(_pay_ay)), _pe(100 * GT_ / GST), _pe(100 * G2["genai_site_cihaz"]["Mobile"] / sum(G2["genai_site_cihaz"].values()))), "D44")

# ---------------------------------------------------------------- 1b · sayfa türüne göre ve site genelinde en çok gösterilen sayfalar
from b_organik import tur_tr as _TTR, tur_en as _TEN
GTUR = G2["genai_site_tur"]; _LT = G2["genai_site_liste_toplam"]
rows_t = []
for t, v in sorted(GTUR.items(), key=lambda i: -i[1][0]):
    if not v[0]: continue
    rows_t.append([x(_TTR[t], _TEN[t]), cellk(v[0]), n(yzd(100 * v[0] / _LT)), cell(v[3]), cellk(v[1]), n(yzd(100 * v[0] / v[1]) if v[1] else "-"), cellk(v[2]), n(yzd(100 * v[2] / v[1], 2) if v[1] else "-")])
T_TUR = tablo([th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı (Bölüm [[b:organik]] ile aynı sınıflama).", "Page class by URL structure (same classification as Section [[b:organik]])."),
               th("Yapay zeka gösterimi", "AI feature impressions", "Search Console dışa aktarımındaki ilk 1.000 sayfanın yapay zeka gösterimi; bir aramada birden fazla sayfa görünebildiği için toplamı site toplamından yüksektir.", "AI feature impressions of the top 1,000 pages in the Search Console export; as several pages can appear in one search, the total is higher than the site total.", True),
               th("Pay", "Share", "Sayfa türünün yapay zeka gösterimi içindeki payı.", "The page type's share of AI feature impressions.", True),
               th("Sayfa", "Pages", "İlk 1.000 sayfa listesinde yer alan sayfa sayısı.", "Number of pages in the top 1,000 list.", True),
               th("Toplam gösterim", "Total impressions", "18 May - 29 Eyl 2026 sayfa türünün web aramasındaki toplam gösterimi.", "Total web search impressions of the page type, 18 May - 29 Sep 2026.", True),
               th("Yapay zeka payı", "AI share", "Yapay zeka gösterimi / toplam gösterim.", "AI feature impressions / total impressions.", True),
               th("Click", "Clicks", "Aynı dönemde organik click.", "Organic clicks in the same period.", True),
               th("CTR", "CTR", "Tık / toplam gösterim.", "Clicks / total impressions.", True)], rows_t, "dar")
_kt, _ic, _ur = GTUR["kategori"], GTUR["icerik"], GTUR["urun"]
INS_TUR = insight("Yapay zeka özelliklerindeki gösterimin en büyük bölümü kategori sayfalarına (%s) ve blog yazılarına (%s) aittir. Ancak sayfa türünün kendi gösterimine oranla bakıldığında **yapay zeka özellikleri blogda gösterimin %s'ini, kategori sayfalarında %s'ini, ürün sayfalarında %s'ini** oluşturmaktadır: bilgi arayan sorularda yapay zeka özeti daha sık çıkmakta, ürün ve kategori aramalarında etkisi daha sınırlı kalmaktadır."
                  % (yzd(100 * _kt[0] / _LT), yzd(100 * _ic[0] / _LT), yzd(100 * _ic[0] / _ic[1]), yzd(100 * _kt[0] / _kt[1]), yzd(100 * _ur[0] / _ur[1])),
                  "The largest part of the impressions in AI features belongs to category pages (%s) and blog articles (%s). Relative to each page type's own impressions, however, **AI features make up %s of impressions on the blog, %s on category pages and %s on product pages**: AI summaries appear more often for information-seeking questions, while their effect on product and category searches stays more limited."
                  % (_pe(100 * _kt[0] / _LT), _pe(100 * _ic[0] / _LT), _pe(100 * _ic[0] / _ic[1]), _pe(100 * _kt[0] / _kt[1]), _pe(100 * _ur[0] / _ur[1])), "D44")

# ---------------------------------------------------------------- 2 · yapay zeka gösterim payına göre sayfa grupları
SAT = [dict(r, pay=100 * r["genai"] / r["gos_genai_donem"]) for r in G2["genai_sayfa_tablo"] if r["gos_genai_donem"] and r["c25"] >= 50 and r["i25"] and r["i26"]]
GRUPLAR = [(20, 101, "Yapay zeka payı %20 ve üzeri", "AI share 20% and above"), (10, 20, "Yapay zeka payı %10-20", "AI share 10-20%"), (0, 10, "Yapay zeka payı %10'un altında", "AI share below 10%")]
def _oz(L):
    c5 = sum(r["c25"] for r in L); c6 = sum(r["c26"] for r in L); i5 = sum(r["i25"] for r in L); i6 = sum(r["i26"] for r in L)
    p5 = sum(r["p25"] * r["i25"] for r in L) / i5; p6 = sum(r["p26"] * r["i26"] for r in L if r["p26"]) / i6
    return {"n": len(L), "c5": c5, "c6": c6, "i5": i5, "i6": i6, "p5": p5, "p6": p6, "dc": _deg(c5, c6), "di": _deg(i5, i6), "ctr5": 100 * c5 / i5, "ctr6": 100 * c6 / i6}
OZ = {}
for a, b, tr, en in GRUPLAR:
    L = [r for r in SAT if a <= r["pay"] < b]; OZ[tr] = (_oz(L), _oz([r for r in L if abs(r["p26"] - r["p25"]) <= 1]))
def _grup_tablo(i):
    rows = []
    for a, b, tr, en in GRUPLAR:
        o = OZ[tr][i]
        rows.append([x(tr, en), cell(o["n"]), cellk(o["c5"]), cellk(o["c6"]), n(yz(o["dc"])), n(yz(o["di"])), n("%s → %s" % (_s(o["p5"]), _s(o["p6"]))), n("%s → %s" % (yzd(o["ctr5"], 2), yzd(o["ctr6"], 2)))])
    return tablo([th("Sayfa grubu", "Page group", "Yazının 18 May - 29 Eyl 2026 yapay zeka özelliği gösteriminin aynı dönemdeki toplam gösterimine oranı; Haz-Eyl 2025'te en az 50 tık almış blog yazıları.", "The ratio of the article's AI feature impressions to its total impressions in 18 May - 29 Sep 2026; blog articles with at least 50 clicks in Jun-Sep 2025."),
                  th("Sayfa", "Pages", "Gruptaki yazı sayısı.", "Number of articles in the group.", True),
                  th("Click 2025", "Clicks 2025", "1 Haz - 29 Eyl 2025 organik click.", "Organic clicks, 1 Jun - 29 Sep 2025.", True),
                  th("Click 2026", "Clicks 2026", "1 Haz - 29 Eyl 2026 organik click.", "Organic clicks, 1 Jun - 29 Sep 2026.", True),
                  th("Click YoY", "Click YoY", "1 Haz - 29 Eyl 2026 click'inin 2025'in aynı günlerine göre değişimi (YoY).", "Change of 1 Jun - 29 Sep 2026 clicks against the same days of 2025 (YoY).", True),
                  th("Gösterim YoY", "Impressions YoY", "Aynı günlerde gösterimin 2025'e göre değişimi (YoY).", "Change of impressions against the same days of 2025 (YoY).", True),
                  th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True),
                  th("CTR", "CTR", "Tık / gösterim, 2025 → 2026.", "Clicks / impressions, 2025 → 2026.", True)], rows, "dar xl")
T_GRUP = sekmeler([("Tüm yazılar", "All articles", _grup_tablo(0)), ("Sıralaması korunan yazılar", "Articles whose ranking held", _grup_tablo(1))])
_y, _o, _a = OZ[GRUPLAR[0][2]], OZ[GRUPLAR[1][2]], OZ[GRUPLAR[2][2]]
INS_GRUP = insight("**Yapay zeka özelliklerinde gösterim payı yükseldikçe tık kaybı derinleşmektedir.** Gösteriminin %%20'si ve fazlası yapay zeka özelliklerinde gerçekleşen %d yazıda Haziran - Eylül tıkı 2025'e göre %s, payı %%10-20 olan %d yazıda %s, %%10'un altında kalan %d yazıda %s değişmiştir. Sıralaması korunan, yani 2025 ve 2026 ortalama Google sırası arasındaki fark en fazla 1 olan yazılarla sınırlandığında da tablo aynıdır: ilk grupta ortalama sıra %s → %s iken tık %s değişmiş, CTR %s'den %s'e inmiştir. Bu yazılarda sıralama korunurken kullanıcının sorusu arama sonucunda yanıtlanmakta ve tık sayfaya gelmemektedir."
                 % (_y[0]["n"], yz(_y[0]["dc"]), _o[0]["n"], yz(_o[0]["dc"]), _a[0]["n"], yz(_a[0]["dc"]), _s(_y[1]["p5"]), _s(_y[1]["p6"]), yz(_y[1]["dc"]), yzd(_y[1]["ctr5"], 2), yzd(_y[1]["ctr6"], 2)),
                 "**The higher the share of impressions in AI features, the deeper the click loss.** In the %d articles where 20%% or more of impressions take place in AI features, June - September clicks changed %s against 2025; in the %d articles with a 10-20%% share %s, and in the %d articles below 10%% %s. The picture is the same when limited to articles whose ranking held, i.e. whose average Google position differs by at most 1 between 2025 and 2026: in the first group the average position was %s → %s while clicks changed %s and CTR fell from %s to %s. In these articles the ranking is kept, but the user's question is answered on the results page and the click does not reach the page."
                 % (_y[0]["n"], yz(_y[0]["dc"]), _o[0]["n"], yz(_o[0]["dc"]), _a[0]["n"], yz(_a[0]["dc"]), _s(_y[1]["p5"]).replace(",", "."), _s(_y[1]["p6"]).replace(",", "."), yz(_y[1]["dc"]), yzd(_y[1]["ctr5"], 2), yzd(_y[1]["ctr6"], 2)), "D44", "D2")

# ---------------------------------------------------------------- 3 · yapay zeka gösterimi alan sayfalar: sayfa bazında click değişimi (grafik) ve site geneli süzgeçli tablo
_BT = G2["genai_sayfa_tablo"]; _BTD = {r["u"]: r for r in _BT}
_GP = sorted([r for r in _BT if r["c25"] + r["c26"] >= 20], key=lambda r: -r["genai"])
def _kisa_ad(p):
    t = p.rstrip("/").split("/")[-1]; return t if len(t) <= 34 else t[:32] + "…"
_GPE = [_kisa_ad(r["u"]) for r in _GP]
for e_ in _GPE: x(e_, e_)
def _yy(r): return _deg(r["c25"], r["c26"]) if r["c25"] else None
G_SAYFA = _kombo2(_GPE, [
    {"ad": x("Click 2025 (Haz-Eyl)", "Clicks 2025 (Jun-Sep)"), "renk": "#10332F", "deger": [r["c25"] for r in _GP], "tip": "cubuk", "bicim": _fk2, "eksen": "sol", "eksen_ad": x("Click", "Clicks")},
    {"ad": x("Click 2026 (Haz-Eyl)", "Clicks 2026 (Jun-Sep)"), "renk": "#E85F36", "deger": [r["c26"] for r in _GP], "tip": "cubuk", "bicim": _fk2, "eksen": "sol"},
    {"ad": x("Yapay zeka gösterimi", "AI feature impressions"), "renk": "#F5A623", "deger": [r["genai"] for r in _GP], "tip": "cizgi", "bicim": _fk2, "eksen": "sag", "eksen_ad": x("Gösterim", "Impressions")},
    {"ad": x("Toplam gösterim", "Total impressions"), "renk": "#7A8C89", "deger": [r["gos_genai_donem"] or None for r in _GP], "tip": "kesik", "bicim": _fk2, "eksen": "sag", "gizli": True}],
    cap=x("Yapay zeka gösterimi alan blog yazıları · Haziran - Eylül click'i 2025 ve 2026 (çubuk, sol eksen), yapay zeka gösterimi ve toplam gösterim 18 May - 29 Eyl 2026 (çizgi, sağ eksen); yazılar yapay zeka gösterimine göre sıralıdır, lejanttan seri açılıp kapatılabilir",
          "Blog articles with AI feature impressions · June - September clicks 2025 and 2026 (bars, left axis), AI feature impressions and total impressions 18 May - 29 Sep 2026 (lines, right axis); articles are sorted by AI impressions, series can be switched on and off in the legend"),
    dondur=True, yukseklik=380, genislik=max(880, 24 * len(_GP)), min_gen=max(880, 24 * len(_GP)),
    ek_satir=[[(x("Click YoY (Haz-Eyl)", "Click YoY (Jun-Sep)"), _pbs(_yy(r)) if _yy(r) is not None else "-"),
               (x("Yapay zeka payı", "AI share"), _pb(100 * r["genai"] / r["gos_genai_donem"]) if r["gos_genai_donem"] else "-"),
               (x("Ort. sıra 2025 → 2026", "Avg. position 2025 → 2026"), "%s → %s" % (_s(r["p25"]) if r["p25"] else "-", _s(r["p26"]) if r["p26"] else "-"))] for r in _GP])
for r in _GP:
    _a, _b = (_s(r["p25"]) if r["p25"] else "-"), (_s(r["p26"]) if r["p26"] else "-")
    x("%s → %s" % (_a, _b), "%s → %s" % (_a.replace(",", "."), _b.replace(",", ".")))
_dus = sum(1 for r in _GP if r["c26"] < r["c25"]); _art = len(_GP) - _dus
_U, _A = _GP[:40], _GP[40:]
def _top(L, a): return sum(r[a] for r in L)
_TUR_F = [("kategori", "Kategori", "Category"), ("icerik", "Blog", "Blog"), ("urun", "Ürün", "Product"), ("koleksiyon", "Koleksiyon", "Collection"), ("diger_grup", "Diğer", "Other")]
def _fgrup(t): return t if t in ("kategori", "icerik", "urun", "koleksiyon") else "diger_grup"
SATIR = {}
for p_, g, i_, c_, ps, t in G2["genai_site_sayfa"]:
    if g >= 100: SATIR[p_] = [p_, g, i_, c_, ps, t]
for r in _BT:   # filtreli blog dışa aktarımı daha kapsamlıdır: blog yazılarında oradaki değer kullanılır
    if r["genai"] >= 100: SATIR[r["u"]] = [r["u"], r["genai"], r["gos_genai_donem"], None, None, "icerik"]
_SGD = {p_: (c_, i_, ps) for p_, g, i_, c_, ps, t in G2["genai_site_sayfa"]}
_say = {}
gov = []
for p_, g, i_, c_, ps, t in sorted(SATIR.values(), key=lambda r: -r[1]):
    if c_ is None and p_ in _SGD: c_, _, ps = _SGD[p_]
    b_ = _BTD.get(p_) if t == "icerik" else None
    yy = _yy(b_) if b_ else None
    fg = _fgrup(t); _say[fg] = _say.get(fg, 0) + 1
    hucre = [u("https://www.vitra.com.tr" + (p_ if p_ != "/" else "/"), p_ if p_ != "/" else "/ (ana sayfa)"), x(_TTR[t], _TEN[t])]
    def _nh(v): return '<td class="n">%s</td>' % v
    gov.append('<tr data-f="%s"><td>%s</td><td>%s</td>%s%s%s%s%s%s%s</tr>' % (fg, hucre[0], hucre[1], _nh(cellk(g)[1:]), _nh(cellk(i_ or 0)[1:] if i_ else "-"), _nh(yzd(100 * g / i_) if i_ else "-"),
               _nh(cellk(c_)[1:] if c_ else "-"), _nh(yzd(100 * c_ / i_, 2) if (c_ and i_) else "-"), _nh(_s(ps) if ps else "-"), _nh(yz(yy) if yy is not None else "-")))
_BAS_S = [th("Sayfa adresi", "Page address", "Sayfa adresi; bağlantı web sitesindeki sayfayı açar.", "Page address; the link opens the page on the website."),
          th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı; tablonun üstündeki düğmelerle süzülebilir.", "Page class by URL structure; can be filtered with the buttons above the table."),
          th("Yapay zeka gösterimi", "AI feature impressions", "18 May - 29 Eyl 2026 yapay zeka özelliklerinde gösterim; 100 ve üzeri olan sayfalar.", "Impressions in AI features, 18 May - 29 Sep 2026; pages with 100 and above.", True),
          th("Toplam gösterim", "Total impressions", "Aynı dönemde web aramasında toplam gösterim.", "Total web search impressions in the same period.", True),
          th("Yapay zeka payı", "AI share", "Yapay zeka gösterimi / toplam gösterim.", "AI feature impressions / total impressions.", True),
          th("Click", "Clicks", "18 May - 29 Eyl 2026 organik click.", "Organic clicks, 18 May - 29 Sep 2026.", True),
          th("CTR", "CTR", "Tık / toplam gösterim.", "Clicks / total impressions.", True),
          th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası.", "Impression-weighted average Google position.", True),
          th("Click YoY (Haz-Eyl)", "Click YoY (Jun-Sep)", "1 Haz - 29 Eyl 2026 click'inin 2025'in aynı günlerine göre değişimi (YoY); adresi iki yılda aynı kalan blog yazıları için hesaplanabilmektedir, kategori ve ürün adresleri Aralık 2025'te değiştiği için boştur.",
             "Change of 1 Jun - 29 Sep 2026 clicks against the same days of 2025 (YoY); can be calculated for blog articles whose address stayed the same in both years, empty for category and product addresses as they changed in December 2025.", True)]
x("Tümü", "All")
_FILT = '<div class="tfilt" role="group" aria-label="%s"><button type="button" aria-pressed="true" data-f="">%s</button>%s</div>' % (
    x("Sayfa türü süzgeci", "Page type filter"), x("Tümü (%d)" % len(gov), "All (%d)" % len(gov)),
    "".join('<button type="button" aria-pressed="false" data-f="%s">%s</button>' % (a_, x("%s (%d)" % (b_, _say.get(a_, 0)), "%s (%d)" % (c_, _say.get(a_, 0)))) for a_, b_, c_ in _TUR_F if _say.get(a_)))
T_SAYFA = _FILT + '<div class="tw uzun"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join(_BAS_S), "".join(gov))
INS_SAYFA0 = insight("Yapay zeka gösterimi alan ve iki dönemde toplam en az 20 click alan %d blog yazısının %d'inde Haziran - Eylül click'i 2025'e göre düşmüş, %d'inde artmıştır. **Yapay zeka gösterimi en yüksek %d yazıda click toplamı %s → %s (%s) gerilerken**, yapay zeka gösterimi düşük kalan %d yazıda click %s → %s (%s) artmıştır; bu artış düşük bir tabandan gelmektedir."
                     % (len(_GP), _dus, _art, len(_U), bin(_top(_U, "c25")), bin(_top(_U, "c26")), yz(_deg(_top(_U, "c25"), _top(_U, "c26"))), len(_A), bin(_top(_A, "c25")), bin(_top(_A, "c26")), yz(_deg(_top(_A, "c25"), _top(_A, "c26")))),
                     "Of the %d blog articles with AI feature impressions and at least 20 clicks in the two periods combined, %d saw June - September clicks fall against 2025 and %d saw them rise. **In the %d articles with the most AI impressions, total clicks fell %s → %s (%s)**, while in the %d articles with low AI impressions clicks rose %s → %s (%s); this rise comes from a low base."
                     % (len(_GP), _dus, _art, len(_U), f"{_top(_U, 'c25'):,}", f"{_top(_U, 'c26'):,}", yz(_deg(_top(_U, "c25"), _top(_U, "c26"))), len(_A), f"{_top(_A, 'c25'):,}", f"{_top(_A, 'c26'):,}", yz(_deg(_top(_A, "c25"), _top(_A, "c26")))), "D44", "D2")

_ds = next(r for r in G2["genai_sayfa_tablo"] if r["u"].endswith("dusakabin-temizligi-nasil-yapilir"))
INS_SAYFA = insight("En çok yapay zeka gösterimi alan yazı \"duşakabin temizliği nasıl yapılır\" sayfasıdır: gösteriminin %s'i yapay zeka özelliklerindedir, ortalama sırası %s → %s ile neredeyse aynı kalırken Haziran - Eylül tıkı %s → %s (%s) gerilemiştir. Gömme rezervuar tamiri ve evye seçimi gibi yapay zeka payı düşük, ürün ve tamir ihtiyacına yakın yazılarda ise tık artmıştır."
                  % (yzd(100 * _ds["genai"] / _ds["gos_genai_donem"]), _s(_ds["p25"]), _s(_ds["p26"]), bin(_ds["c25"]), bin(_ds["c26"]), yz(_deg(_ds["c25"], _ds["c26"]))),
                  "The article with the most AI feature impressions is the \"duşakabin temizliği nasıl yapılır\" (how to clean a shower enclosure) page: %s of its impressions are in AI features, its average position stayed almost the same at %s → %s, while June - September clicks fell %s → %s (%s). In articles with a low AI share that are close to product and repair needs, such as concealed cistern repair and kitchen sink selection, clicks rose."
                  % (_pe(100 * _ds["genai"] / _ds["gos_genai_donem"]), _s(_ds["p25"]).replace(",", "."), _s(_ds["p26"]).replace(",", "."), f"{_ds['c25']:,}", f"{_ds['c26']:,}", yz(_deg(_ds["c25"], _ds["c26"]))), "D44")

# ---------------------------------------------------------------- 4 · sorgu düzeyi: AI Overview çıkan ve çıkmayan aramalar
AS = G2["aio_sorgu"]; AH = G2["aio_ahrefs"]
def _qoz(L):
    c5 = sum(r["c25"] for r in L); c6 = sum(r["c26"] for r in L); i5 = sum(r["i25"] for r in L); i6 = sum(r["i26"] for r in L)
    return {"n": len(L), "c5": c5, "c6": c6, "dc": _deg(c5, c6), "di": _deg(i5, i6), "p5": sum(r["p25"] * r["i25"] for r in L) / i5, "p6": sum(r["p26"] * r["i26"] for r in L) / i6, "ctr5": 100 * c5 / i5, "ctr6": 100 * c6 / i6}
QG = [("AI Overview çıkan aramalar", "Searches with an AI Overview", lambda r: r["aio"]), ("AI Overview çıkmayan aramalar", "Searches without an AI Overview", lambda r: not r["aio"])]
QS = [("Tümü", "All", lambda r: True), ("2025'te ilk 3'te olanlar", "In the top 3 in 2025", lambda r: r["p25"] <= 3), ("Sıralaması korunanlar (fark en fazla 1)", "Ranking held (difference at most 1)", lambda r: abs(r["p26"] - r["p25"]) <= 1)]
QO = {}
rows_q = []
for gtr, gen, gf in QG:
    for str_, sen, sf in QS:
        o = _qoz([r for r in AS if gf(r) and sf(r)]); QO[(gtr, str_)] = o
        rows_q.append([x("%s · %s" % (gtr, str_.lower() if str_ != "Tümü" else "tümü"), "%s · %s" % (gen, sen.lower() if sen != "All" else "all")), cell(o["n"]), cellk(o["c5"]), cellk(o["c6"]), n(yz(o["dc"])), n(yz(o["di"])),
                       n("%s → %s" % (_s(o["p5"]), _s(o["p6"]))), n("%s → %s" % (yzd(o["ctr5"], 2), yzd(o["ctr6"], 2)))])
T_SORGU = tablo([th("Arama grubu", "Search group", "Ahrefs'te blog sayfalarının sıralandığı ve hacmi %d ve üzeri olan %d kelimenin 1 Ekim 2026 Google sonucunda AI Overview çıkıp çıkmadığına göre ayrım; iki dönemde de Search Console'da gösterim alan aramalar." % (AH["min_hacim"], AH["kelime"]),
                     "Split by whether an AI Overview appeared on the 1 October 2026 Google results page for the %d keywords with volume of %d and above for which blog pages rank in Ahrefs; searches with Search Console impressions in both periods." % (AH["kelime"], AH["min_hacim"])),
                  th("Arama", "Searches", "Gruptaki arama sayısı.", "Number of searches in the group.", True),
                  th("Click 2025", "Clicks 2025", "1 Haz - 29 Eyl 2025 blog sayfalarına gelen click.", "Clicks to blog pages, 1 Jun - 29 Sep 2025.", True),
                  th("Click 2026", "Clicks 2026", "1 Haz - 29 Eyl 2026 blog sayfalarına gelen click.", "Clicks to blog pages, 1 Jun - 29 Sep 2026.", True),
                  th("Click YoY", "Click YoY", "1 Haz - 29 Eyl 2026 click'inin 2025'in aynı günlerine göre değişimi (YoY).", "Change of 1 Jun - 29 Sep 2026 clicks against the same days of 2025 (YoY).", True),
                  th("Gösterim YoY", "Impressions YoY", "Aynı günlerde gösterimin 2025'e göre değişimi (YoY).", "Change of impressions against the same days of 2025 (YoY).", True),
                  th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True),
                  th("CTR", "CTR", "Tık / gösterim, 2025 → 2026.", "Clicks / impressions, 2025 → 2026.", True)], rows_q, "dar")
_qa, _qy = QO[("AI Overview çıkan aramalar", "Tümü")], QO[("AI Overview çıkmayan aramalar", "Tümü")]
_qa3, _qy3 = QO[("AI Overview çıkan aramalar", "2025'te ilk 3'te olanlar")], QO[("AI Overview çıkmayan aramalar", "2025'te ilk 3'te olanlar")]
_qas, _qys = QO[("AI Overview çıkan aramalar", "Sıralaması korunanlar (fark en fazla 1)")], QO[("AI Overview çıkmayan aramalar", "Sıralaması korunanlar (fark en fazla 1)")]
INS_SORGU = insight("Ahrefs'te blog sayfalarının sıralandığı %d kelimenin %d'sinde 1 Ekim 2026 itibarıyla AI Overview çıkmaktadır; Eylül 2025 gözleminde bu kelimelerin hiçbirinde AI Overview görünmemekteydi. Search Console'da iki dönemde de gösterim alan %d AI Overview'lı aramada Haziran - Eylül tıkı %s değişirken AI Overview çıkmayan %d aramada değişim %s'de kalmıştır; AI Overview'lı aramalarda gösterim %s artmasına karşın CTR %s'den %s'e inmiştir. Kaybın bir bölümü sıra kaybıyla birliktedir: 2025'te ilk 3'te olan AI Overview'lı aramalarda ortalama sıra %s → %s gerilemiştir; \"duşakabin temizliği\" gibi yüksek hacimli baş aramalarda sıra 1'den 3-4 bandına inerken yazıların sayfa düzeyindeki ortalama sırası uzun kuyruk aramalarla korunmaktadır. Sıralaması korunan (2025 ile 2026 arasında sıra farkı en fazla 1) aramalarda iki grubun click değişimi birbirine yakındır (%s ve %s); sorgu düzeyindeki bu örneklem küçük olduğu için sayfa düzeyindeki bulgu daha güçlü bir göstergedir."
                    % (AH["kelime"], AH["aio"], _qa["n"], yz(_qa["dc"]), _qy["n"], yz(_qy["dc"]), yzd(_qa["di"]), yzd(_qa["ctr5"], 2), yzd(_qa["ctr6"], 2), _s(_qa3["p5"]), _s(_qa3["p6"]), yz(_qas["dc"]), yz(_qys["dc"])),
                    "As of 1 October 2026, an AI Overview appears for %d of the %d keywords for which blog pages rank in Ahrefs; in the September 2025 observation none of these keywords showed an AI Overview. For the %d searches with an AI Overview that had Search Console impressions in both periods, June - September clicks changed %s, while for the %d searches without an AI Overview the change stayed at %s; in searches with an AI Overview impressions rose %s but CTR fell from %s to %s. Part of the loss comes with a loss of position: for searches with an AI Overview that were in the top 3 in 2025, the average position fell %s → %s; in high-volume head searches such as \"duşakabin temizliği\" the position moved from 1 to the 3-4 band, while the articles' page-level average position is held by long-tail searches. For searches whose ranking held (a position difference of at most 1 between 2025 and 2026), the click change of the two groups is close (%s and %s); as this query-level sample is small, the page-level finding is the stronger indicator."
                    % (AH["aio"], AH["kelime"], _qa["n"], yz(_qa["dc"]), _qy["n"], yz(_qy["dc"]), _pe(_qa["di"]), yzd(_qa["ctr5"], 2), yzd(_qa["ctr6"], 2), _s(_qa3["p5"]).replace(",", "."), _s(_qa3["p6"]).replace(",", "."), yz(_qas["dc"]), yz(_qys["dc"])), "D44")
rows_ornek = []
for r in sorted([r for r in AS if r["aio"]], key=lambda r: -r["c25"])[:12]:
    rows_ornek.append([kw(r["q"]), cellk(r["vol"]), cellk(r["c25"]), cellk(r["c26"]), n(yz(_deg(r["c25"], r["c26"]))), n("%s → %s" % (_s(r["p25"]), _s(r["p26"])))])
T_ORNEK = tablo([th("Arama ifadesi", "Search phrase", "AI Overview çıkan ve Haziran - Eylül 2025'te blog sayfalarına en çok tık getiren aramalar.", "Searches with an AI Overview that brought the most clicks to blog pages in June - September 2025."),
                 th("Hacim", "Volume", "Ahrefs aylık arama hacmi, Türkiye.", "Ahrefs monthly search volume, Turkey.", True),
                 th("Click 2025", "Clicks 2025", "1 Haz - 29 Eyl 2025.", "1 Jun - 29 Sep 2025.", True), th("Click 2026", "Clicks 2026", "1 Haz - 29 Eyl 2026.", "1 Jun - 29 Sep 2026.", True),
                 th("Click YoY", "Click YoY", "1 Haz - 29 Eyl 2026 click'inin 2025'in aynı günlerine göre değişimi (YoY).", "Change of 1 Jun - 29 Sep 2026 clicks against the same days of 2025 (YoY).", True),
                 th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True)], rows_ornek, "dar")
ONERI = marks([
 ("up", "Yapay zeka payı yüksek \"nedir\" ve \"nasıl temizlenir\" yazılarında amaç tıktan çok yapay zeka yanıtında kaynak gösterilmek olarak tanımlanabilir; kısa ve doğrudan yanıt, adım listesi ve ürün adıyla anılan VitrA çözümleri bu yanıtlarda alıntılanma olasılığını artırabilir (Bölüm [[b:geo]])",
  "For \"what is\" and \"how to clean\" articles with a high AI share, the goal can be defined as being cited in the AI answer rather than the click; a short direct answer, step lists and VitrA solutions named with the product name can increase the likelihood of being quoted in these answers (Section [[b:geo]])"),
 ("up", "Tamir, yedek parça ve ürün seçimi gibi kullanıcıyı ürüne ve servise yönlendiren yazılarda tık korunmaktadır; bu yazılara ürün, yedek parça ve servis bağlantıları eklenmesi trafiği satışa ve servise taşıyabilir",
  "Clicks hold up in articles that lead the user to a product or service, such as repair, spare parts and product selection; adding product, spare part and service links to these articles can carry the traffic to sales and service"),
 ("at", "Blog performansı yalnız tıkla değerlendirildiğinde yapay zeka özelliklerinde kazanılan görünürlük görünmez kalmaktadır; Search Console yapay zeka gösterimi ve tık birlikte izlenebilir",
  "When blog performance is judged by clicks alone, the visibility gained in AI features remains invisible; Search Console AI feature impressions and clicks can be monitored together"),
])

HTML = """
<p class="lede">%s</p>
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
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
""" % (
 x("Google, arama sonucunda kullanıcının sorusunu yapay zeka özetiyle (AI Overview) ve benzeri yapay zeka özellikleriyle yanıtlamaktadır. Search Console bu özelliklerde sitenin aldığı gösterimi 18 Mayıs 2026'dan itibaren ayrı raporlamaktadır. vitra.com.tr'nin bu rapordaki gösterimi (18 Mayıs - 29 Eylül 2026) önce site geneli ve sayfa türü bazında verilmiş; ardından adresi iki yılda da aynı kalan blog sayfalarında (/ilham-veren-fikirler/) tık ve sıra 2025'in aynı aylarıyla ve Ahrefs'te AI Overview çıkan aramalarla karşılaştırılmıştır.",
   "Google answers the user's question on the results page with an AI summary (AI Overview) and similar AI features. Search Console reports the impressions a site receives in these features separately from 18 May 2026. vitra.com.tr's impressions in this report (18 May - 29 September 2026) are first given site-wide and by page type; then, on blog pages (/ilham-veren-fikirler/) whose addresses stayed the same in both years, clicks and position are compared with the same months of 2025 and with searches showing an AI Overview in Ahrefs."),
 kpi_kart(k(GST), "Yapay zeka özelliklerinde gösterim · site geneli, 18 May - 29 Eyl 2026; blog %s" % yzd(100 * GT_ / GST), "Impressions in AI features · site-wide, 18 May - 29 Sep 2026; blog %s" % _pe(100 * GT_ / GST)),
 kpi_kart(yzd(_spay[-1]), "Site gösterimindeki pay · Eylül 2026 (1-29); Mayıs'ın son iki haftasında %s" % yzd(_spay[0]), "Share of site impressions · September 2026 (1-29); %s in the last two weeks of May" % _pe(_spay[0]), "dn"),
 kpi_kart(yz(_y[0]["dc"]), "Yapay zeka payı %%20 ve üzeri %d blog yazısında tık değişimi · Haz-Eyl 2026 / 2025; ortalama sıra %s → %s" % (_y[0]["n"], _s(_y[0]["p5"]), _s(_y[0]["p6"])), "Click change in %d blog articles with an AI share of 20%% and above · Jun-Sep 2026 / 2025; average position %s → %s" % (_y[0]["n"], _s(_y[0]["p5"]).replace(",", "."), _s(_y[0]["p6"]).replace(",", ".")), "dn"),
 kpi_kart(yz(_qa["dc"]), "AI Overview çıkan %d blog aramasında tık değişimi · Haz-Eyl 2026 / 2025; AI Overview çıkmayanlarda %s" % (_qa["n"], _isr(_qy["dc"])), "Click change in %d blog searches with an AI Overview · Jun-Sep 2026 / 2025; %s for searches without one" % (_qa["n"], _isr_en(_qy["dc"])), "dn"),
 x("Yapay zeka özelliklerinde gösterim: site geneli ve blog", "Impressions in AI features: site-wide and blog"), G_SERI, T_AY, INS_AY,
 x("Sayfa türüne göre yapay zeka gösterimi", "AI feature impressions by page type"), T_TUR, INS_TUR,
 x("Yapay zeka özelliklerinde gösterim alan sayfalar ve click değişimi", "Pages with AI feature impressions and click change"), G_SAYFA, INS_SAYFA0, T_SAYFA, INS_SAYFA,
 x("Yapay zeka gösterim payına göre blog yazılarında click değişimi", "Click change in blog articles by AI impression share"), T_GRUP, INS_GRUP,
 x("AI Overview çıkan ve çıkmayan blog aramalarında click ve sıra", "Clicks and position in blog searches with and without an AI Overview"), T_SORGU, T_ORNEK, INS_SORGU,
 x("Olası adımlar", "Possible steps"), ONERI,
 kaynak("Google Search Console · yapay zeka özellikleri raporu, site geneli ve /ilham-veren-fikirler/ sayfaları, 18 May - 29 Eyl 2026 · sc-domain:vitra.com.tr sayfa toplamları 18 May - 29 Eyl 2026, blog sayfaları ve sorguları 1 Haz - 29 Eyl 2025 ve 2026 · Ahrefs Site Explorer, /ilham-veren-fikirler/ kelimeleri ve SERP özellikleri, 01.10.2026 ve 15.09.2025",
        "Google Search Console · AI features report, site-wide and /ilham-veren-fikirler/ pages, 18 May - 29 Sep 2026 · sc-domain:vitra.com.tr page totals 18 May - 29 Sep 2026, blog pages and queries 1 Jun - 29 Sep 2025 and 2026 · Ahrefs Site Explorer, /ilham-veren-fikirler/ keywords and SERP features, 01.10.2026 and 15.09.2025", "D44", "D2"),
)
