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
G_SERI = sekmeler([("Gösterim", "Impressions", _kombo2(ETK, [
                        {"ad": x("Site toplam gösterimi", "Total site impressions"), "renk": "#C9D3D1", "deger": [h[5] for h in HAFTA], "tip": "cubuk", "eksen": "sol", "bicim": _fk2, "eksen_ad": x("Site gösterimi", "Site impressions")},
                        {"ad": x("Yapay zeka gösterimi · site", "AI feature impressions · site"), "renk": "#E85F36", "deger": [h[4] for h in HAFTA], "tip": "cizgi", "eksen": "sag", "bicim": _fk2, "eksen_ad": x("Yapay zeka", "AI features")},
                        {"ad": x("Yapay zeka gösterimi · blog", "AI feature impressions · blog"), "renk": "#10332F", "deger": [h[1] for h in HAFTA], "tip": "kesik", "eksen": "sag", "bicim": _fk2}],
                        cap=x("Haftalık gösterim · site toplamı (çubuk, sol eksen) ve yapay zeka özelliklerindeki gösterim (çizgi, sağ eksen), hafta başlangıcı Pazartesi, %s - %s" % (_gun(D0), _gun(HAFTA[-1][0])),
                              "Weekly impressions · site total (bars, left axis) and impressions in AI features (lines, right axis), week starting Monday, %s - %s" % (_gun(D0, True), _gun(HAFTA[-1][0], True))))),
                   ("Pay", "Share", _kombo2(ETK, [
                        {"ad": x("Site gösterimindeki pay", "Share of site impressions"), "renk": "#E85F36", "deger": [round(100 * h[4] / h[5], 2) for h in HAFTA], "tip": "cizgi", "bicim": _pb, "eksen_ad": x("Pay (%)", "Share (%)")},
                        {"ad": x("Blog gösterimindeki pay", "Share of blog impressions"), "renk": "#10332F", "deger": [round(100 * h[1] / h[2], 2) for h in HAFTA], "tip": "kesik", "bicim": _pb}],
                        cap=x("Haftalık pay · yapay zeka özelliklerindeki gösterimin toplam gösterime oranı, site geneli ve blog", "Weekly share · AI feature impressions as a share of total impressions, site-wide and blog")))], "gtabs")
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
rows_ss = []
for p_, g, i_, c_, ps, t in G2["genai_site_sayfa"][:15]:
    rows_ss.append([u("https://www.vitra.com.tr" + (p_ if p_ != "/" else "/"), p_ if p_ != "/" else "/ (ana sayfa)"), x(_TTR[t], _TEN[t]), cellk(g), cellk(i_ or 0), n(yzd(100 * g / i_) if i_ else "-"), cellk(c_ or 0), n(yzd(100 * c_ / i_, 2) if i_ else "-"), n(_s(ps) if ps else "-")])
T_SS = tablo([th("Sayfa adresi", "Page address", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
              th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı.", "Page class by URL structure."),
              th("Yapay zeka gösterimi", "AI feature impressions", "18 May - 29 Eyl 2026 yapay zeka özelliklerinde gösterim.", "Impressions in AI features, 18 May - 29 Sep 2026.", True),
              th("Toplam gösterim", "Total impressions", "Aynı dönemde web aramasında toplam gösterim.", "Total web search impressions in the same period.", True),
              th("Yapay zeka payı", "AI share", "Yapay zeka gösterimi / toplam gösterim.", "AI feature impressions / total impressions.", True),
              th("Click", "Clicks", "Aynı dönemde organik click.", "Organic clicks in the same period.", True),
              th("CTR", "CTR", "Tık / toplam gösterim.", "Clicks / total impressions.", True),
              th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası.", "Impression-weighted average Google position.", True)], rows_ss, "dar")

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
                  th("Click değişimi", "Click change", "2026'nın 2025'e göre değişimi.", "Change of 2026 against 2025.", True),
                  th("Gösterim değişimi", "Impression change", "Aynı dönemde gösterimin değişimi.", "Change of impressions in the same period.", True),
                  th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True),
                  th("CTR", "CTR", "Tık / gösterim, 2025 → 2026.", "Clicks / impressions, 2025 → 2026.", True)], rows, "dar xl")
T_GRUP = sekmeler([("Tüm yazılar", "All articles", _grup_tablo(0)), ("Sırası ±1 içinde kalan yazılar", "Articles whose position stayed within ±1", _grup_tablo(1))])
_y, _o, _a = OZ[GRUPLAR[0][2]], OZ[GRUPLAR[1][2]], OZ[GRUPLAR[2][2]]
INS_GRUP = insight("**Yapay zeka özelliklerinde gösterim payı yükseldikçe tık kaybı derinleşmektedir.** Gösteriminin %%20'si ve fazlası yapay zeka özelliklerinde gerçekleşen %d yazıda Haziran - Eylül tıkı 2025'e göre %s, payı %%10-20 olan %d yazıda %s, %%10'un altında kalan %d yazıda %s değişmiştir. Sırası ±1 içinde kalan yazılarla sınırlandığında da tablo aynıdır: ilk grupta ortalama sıra %s → %s iken tık %s değişmiş, CTR %s'den %s'e inmiştir. Bu yazılarda sıralama korunurken kullanıcının sorusu arama sonucunda yanıtlanmakta ve tık sayfaya gelmemektedir."
                 % (_y[0]["n"], yz(_y[0]["dc"]), _o[0]["n"], yz(_o[0]["dc"]), _a[0]["n"], yz(_a[0]["dc"]), _s(_y[1]["p5"]), _s(_y[1]["p6"]), yz(_y[1]["dc"]), yzd(_y[1]["ctr5"], 2), yzd(_y[1]["ctr6"], 2)),
                 "**The higher the share of impressions in AI features, the deeper the click loss.** In the %d articles where 20%% or more of impressions take place in AI features, June - September clicks changed %s against 2025; in the %d articles with a 10-20%% share %s, and in the %d articles below 10%% %s. The picture is the same when limited to articles whose position stayed within ±1: in the first group the average position was %s → %s while clicks changed %s and CTR fell from %s to %s. In these articles the ranking is kept, but the user's question is answered on the results page and the click does not reach the page."
                 % (_y[0]["n"], yz(_y[0]["dc"]), _o[0]["n"], yz(_o[0]["dc"]), _a[0]["n"], yz(_a[0]["dc"]), _s(_y[1]["p5"]).replace(",", "."), _s(_y[1]["p6"]).replace(",", "."), yz(_y[1]["dc"]), yzd(_y[1]["ctr5"], 2), yzd(_y[1]["ctr6"], 2)), "D44", "D2")

# ---------------------------------------------------------------- 3 · sayfa listesi
rows_s = []
for r in sorted(G2["genai_sayfa_tablo"], key=lambda r: -r["genai"])[:15]:
    p = r["u"]; pay = 100 * r["genai"] / r["gos_genai_donem"] if r["gos_genai_donem"] else None
    rows_s.append([u("https://www.vitra.com.tr" + p + "/", p.replace("/ilham-veren-fikirler", "")), cellk(r["genai"]), n(yzd(pay) if pay else "-"), cellk(r["c25"]), cellk(r["c26"]), n(yz(_deg(r["c25"], r["c26"])) if r["c25"] else "-"),
                   n("%s → %s" % (_s(r["p25"]) if r["p25"] else "-", _s(r["p26"]) if r["p26"] else "-")), n("%s → %s" % (yzd(100 * r["c25"] / r["i25"], 2) if r["i25"] else "-", yzd(100 * r["c26"] / r["i26"], 2) if r["i26"] else "-"))])
T_SAYFA = tablo([th("Yazı", "Article", "Blog yazısının adresi (/ilham-veren-fikirler/ sonrası); bağlantı canlı sayfaya gider.", "The blog article's address (after /ilham-veren-fikirler/); the link opens the live page."),
                 th("Yapay zeka gösterimi", "AI feature impressions", "18 May - 29 Eyl 2026 yapay zeka özelliklerinde gösterim.", "Impressions in AI features, 18 May - 29 Sep 2026.", True),
                 th("Yapay zeka payı", "AI share", "Yapay zeka gösteriminin yazının aynı dönemdeki toplam gösterimine oranı.", "AI feature impressions as a share of the article's total impressions in the same period.", True),
                 th("Click 2025", "Clicks 2025", "1 Haz - 29 Eyl 2025 organik click.", "Organic clicks, 1 Jun - 29 Sep 2025.", True),
                 th("Click 2026", "Clicks 2026", "1 Haz - 29 Eyl 2026 organik click.", "Organic clicks, 1 Jun - 29 Sep 2026.", True),
                 th("Değişim", "Change", "2026 tıkının 2025'e göre değişimi.", "Change of 2026 clicks against 2025.", True),
                 th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True),
                 th("CTR", "CTR", "Tık / gösterim, 2025 → 2026.", "Clicks / impressions, 2025 → 2026.", True)], rows_s, "dar")
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
QS = [("Tümü", "All", lambda r: True), ("2025'te ilk 3'te olanlar", "In the top 3 in 2025", lambda r: r["p25"] <= 3), ("Sırası ±1 içinde kalanlar", "Position stayed within ±1", lambda r: abs(r["p26"] - r["p25"]) <= 1)]
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
                  th("Click değişimi", "Click change", "2026'nın 2025'e göre değişimi.", "Change of 2026 against 2025.", True),
                  th("Gösterim değişimi", "Impression change", "Aynı dönemde gösterimin değişimi.", "Change of impressions in the same period.", True),
                  th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası, 2025 → 2026.", "Impression-weighted average Google position, 2025 → 2026.", True),
                  th("CTR", "CTR", "Tık / gösterim, 2025 → 2026.", "Clicks / impressions, 2025 → 2026.", True)], rows_q, "dar")
_qa, _qy = QO[("AI Overview çıkan aramalar", "Tümü")], QO[("AI Overview çıkmayan aramalar", "Tümü")]
_qa3, _qy3 = QO[("AI Overview çıkan aramalar", "2025'te ilk 3'te olanlar")], QO[("AI Overview çıkmayan aramalar", "2025'te ilk 3'te olanlar")]
_qas, _qys = QO[("AI Overview çıkan aramalar", "Sırası ±1 içinde kalanlar")], QO[("AI Overview çıkmayan aramalar", "Sırası ±1 içinde kalanlar")]
INS_SORGU = insight("Ahrefs'te blog sayfalarının sıralandığı %d kelimenin %d'sinde 1 Ekim 2026 itibarıyla AI Overview çıkmaktadır; Eylül 2025 gözleminde bu kelimelerin hiçbirinde AI Overview görünmemekteydi. Search Console'da iki dönemde de gösterim alan %d AI Overview'lı aramada Haziran - Eylül tıkı %s değişirken AI Overview çıkmayan %d aramada değişim %s'de kalmıştır; AI Overview'lı aramalarda gösterim %s artmasına karşın CTR %s'den %s'e inmiştir. Kaybın bir bölümü sıra kaybıyla birliktedir: 2025'te ilk 3'te olan AI Overview'lı aramalarda ortalama sıra %s → %s gerilemiştir; \"duşakabin temizliği\" gibi yüksek hacimli baş aramalarda sıra 1'den 3-4 bandına inerken yazıların sayfa düzeyindeki ortalama sırası uzun kuyruk aramalarla korunmaktadır. Sırası ±1 içinde kalan aramalarda iki grubun tık değişimi birbirine yakındır (%s ve %s); sorgu düzeyindeki bu örneklem küçük olduğu için sayfa düzeyindeki bulgu daha güçlü bir göstergedir."
                    % (AH["kelime"], AH["aio"], _qa["n"], yz(_qa["dc"]), _qy["n"], yz(_qy["dc"]), yzd(_qa["di"]), yzd(_qa["ctr5"], 2), yzd(_qa["ctr6"], 2), _s(_qa3["p5"]), _s(_qa3["p6"]), yz(_qas["dc"]), yz(_qys["dc"])),
                    "As of 1 October 2026, an AI Overview appears for %d of the %d keywords for which blog pages rank in Ahrefs; in the September 2025 observation none of these keywords showed an AI Overview. For the %d searches with an AI Overview that had Search Console impressions in both periods, June - September clicks changed %s, while for the %d searches without an AI Overview the change stayed at %s; in searches with an AI Overview impressions rose %s but CTR fell from %s to %s. Part of the loss comes with a loss of position: for searches with an AI Overview that were in the top 3 in 2025, the average position fell %s → %s; in high-volume head searches such as \"duşakabin temizliği\" the position moved from 1 to the 3-4 band, while the articles' page-level average position is held by long-tail searches. For searches whose position stayed within ±1, the click change of the two groups is close (%s and %s); as this query-level sample is small, the page-level finding is the stronger indicator."
                    % (AH["aio"], AH["kelime"], _qa["n"], yz(_qa["dc"]), _qy["n"], yz(_qy["dc"]), _pe(_qa["di"]), yzd(_qa["ctr5"], 2), yzd(_qa["ctr6"], 2), _s(_qa3["p5"]).replace(",", "."), _s(_qa3["p6"]).replace(",", "."), yz(_qas["dc"]), yz(_qys["dc"])), "D44")
rows_ornek = []
for r in sorted([r for r in AS if r["aio"]], key=lambda r: -r["c25"])[:12]:
    rows_ornek.append([kw(r["q"]), cellk(r["vol"]), cellk(r["c25"]), cellk(r["c26"]), n(yz(_deg(r["c25"], r["c26"]))), n("%s → %s" % (_s(r["p25"]), _s(r["p26"])))])
T_ORNEK = tablo([th("Arama ifadesi", "Search phrase", "AI Overview çıkan ve Haziran - Eylül 2025'te blog sayfalarına en çok tık getiren aramalar.", "Searches with an AI Overview that brought the most clicks to blog pages in June - September 2025."),
                 th("Hacim", "Volume", "Ahrefs aylık arama hacmi, Türkiye.", "Ahrefs monthly search volume, Turkey.", True),
                 th("Click 2025", "Clicks 2025", "1 Haz - 29 Eyl 2025.", "1 Jun - 29 Sep 2025.", True), th("Click 2026", "Clicks 2026", "1 Haz - 29 Eyl 2026.", "1 Jun - 29 Sep 2026.", True),
                 th("Değişim", "Change", "2026 tıkının 2025'e göre değişimi.", "Change of 2026 clicks against 2025.", True),
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
 x("Yapay zeka özelliklerinde en çok gösterilen sayfalar · site geneli", "Pages shown most in AI features · site-wide"), T_SS,
 x("Yapay zeka gösterim payına göre blog yazılarında tık değişimi", "Click change in blog articles by AI impression share"), T_GRUP, INS_GRUP,
 x("Yapay zeka özelliklerinde en çok gösterilen blog yazıları", "Blog articles shown most in AI features"), T_SAYFA, INS_SAYFA,
 x("AI Overview çıkan ve çıkmayan blog aramalarında tık ve sıra", "Clicks and position in blog searches with and without an AI Overview"), T_SORGU, T_ORNEK, INS_SORGU,
 x("Olası adımlar", "Possible steps"), ONERI,
 kaynak("Google Search Console · yapay zeka özellikleri raporu, site geneli ve /ilham-veren-fikirler/ sayfaları, 18 May - 29 Eyl 2026 · sc-domain:vitra.com.tr sayfa toplamları 18 May - 29 Eyl 2026, blog sayfaları ve sorguları 1 Haz - 29 Eyl 2025 ve 2026 · Ahrefs Site Explorer, /ilham-veren-fikirler/ kelimeleri ve SERP özellikleri, 01.10.2026 ve 15.09.2025",
        "Google Search Console · AI features report, site-wide and /ilham-veren-fikirler/ pages, 18 May - 29 Sep 2026 · sc-domain:vitra.com.tr page totals 18 May - 29 Sep 2026, blog pages and queries 1 Jun - 29 Sep 2025 and 2026 · Ahrefs Site Explorer, /ilham-veren-fikirler/ keywords and SERP features, 01.10.2026 and 15.09.2025", "D44", "D2"),
)
