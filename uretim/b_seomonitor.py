# -*- coding: utf-8 -*-
"""SEOmonitor (vitra.com.tr, kampanya 324384) · takip edilen kelimelerde AI Overview durumu (GEO bolumu) ve Google click payi (rakip bolumu)."""
from ortak import *
import json as _j, os as _o, collections as _c
_K = _j.load(open(_o.path.join(veri.V, "ham", "seomonitor", "kelimeler_2026-10-03.json"), encoding="utf-8"))
_SOC = _j.load(open(_o.path.join(veri.V, "ham", "seomonitor", "share_of_clicks.json"), encoding="utf-8"))
_FOLD = {582638: "Vitrifiyeler", 582499: "Banyo Mobilyaları", 582219: "Armatürler", 582535: "Duşlar", 582658: "Yıkanma Alanları", 582605: "Rezervuarlar", 582488: "Banyo Aksesuarları", 582594: "Karo Seramik Ürünleri"}
_ALT = {582638: (582639, 582645), 582499: (582500, 582506), 582219: (582299, 582335), 582535: (582585, 582593), 582658: (582659, 582666), 582605: (582606, 582609), 582488: (582489, 582498), 582594: (582595, 582604)}
_EK = {654343: 582219, 582299: 582219}
_EN = {"Vitrifiyeler": "Sanitaryware", "Banyo Mobilyaları": "Bathroom Furniture", "Armatürler": "Taps and Mixers", "Duşlar": "Showers", "Yıkanma Alanları": "Bathing Areas",
       "Rezervuarlar": "Cisterns", "Banyo Aksesuarları": "Bathroom Accessories", "Karo Seramik Ürünleri": "Ceramic Tiles", "Tümü": "All", "Marka": "Brand"}
def _kat(k):
    for g in (k.get("groups") or "").split(","):
        if not g: continue
        g = int(g)
        if g in _EK: return _FOLD[_EK[g]]
        for f, (a, b) in _ALT.items():
            if a <= g <= b: return _FOLD[f]
    return None
_M = [k for k in _K if not k.get("main_keyword_id")]
def _aio(k): return any(f["feature"] == "AIO" for f in (k.get("serp_data") or {}).get("mobile") or []) or _vk(k)
def _vk(k): return (((k.get("ai_overview") or {}).get("mobile") or {}).get("rank") or 100) < 100
AIO = _c.OrderedDict()
for k in _M:
    c = _kat(k)
    if not c: continue
    t = AIO.setdefault(c, {"n": 0, "aio": 0, "vitra": 0, "hacim": 0, "aio_h": 0, "vit_h": 0})
    v = k["search_data"]["search_volume"] or 0
    t["n"] += 1; t["hacim"] += v
    if _aio(k): t["aio"] += 1; t["aio_h"] += v
    if _vk(k): t["vitra"] += 1; t["vit_h"] += v
AIO = _c.OrderedDict(sorted(AIO.items(), key=lambda i: -i[1]["aio"]))
TOP = {k_: sum(t[k_] for t in AIO.values()) for k_ in ("n", "aio", "vitra", "hacim", "aio_h", "vit_h")}
def _p(a, b): return 100 * a / b if b else 0
T_AIO = tablo([th("Kategori", "Category", "SEOmonitor'de VitrA kategori ağacına göre gruplanmış ana kategori.", "Main category in SEOmonitor, grouped by VitrA's category tree."),
               th("Takip edilen kelime", "Tracked keywords", "Kategoride SEOmonitor'de takip edilen ana kelime sayısı (yakın varyantlar hariç).", "Main keywords tracked in SEOmonitor in the category (close variants excluded).", True),
               th("AI Overview çıkan", "With AI Overview", "Mobil sonuçta AI Overview çıkan kelime sayısı, 03.10.2026.", "Keywords with an AI Overview in mobile results, 03.10.2026.", True),
               th("AI Overview payı", "AI Overview share", "AI Overview çıkan kelimelerin kategorideki payı.", "Share of keywords with an AI Overview in the category.", True),
               th("VitrA kaynak", "VitrA cited", "AI Overview'da vitra.com.tr'nin kaynak gösterildiği kelime sayısı.", "Keywords where vitra.com.tr is cited in the AI Overview.", True),
               th("AI Overview içinde VitrA payı", "VitrA share within AI Overviews", "AI Overview çıkan kelimelerden VitrA'nın kaynak gösterildiklerinin payı.", "Share of keywords with an AI Overview where VitrA is cited.", True),
               th("Hacim ağırlıklı VitrA payı", "Volume-weighted VitrA share", "AI Overview çıkan kelimelerin aylık arama hacmi içinde VitrA'nın kaynak gösterildiği kelimelerin payı.", "Share of the monthly search volume of AI Overview keywords coming from keywords where VitrA is cited.", True)],
              [[x(c, _EN[c]), cell(t["n"]), cell(t["aio"]), n(yzd(_p(t["aio"], t["n"]), 0)), cell(t["vitra"]), n(yzd(_p(t["vitra"], t["aio"]), 0)), n(yzd(_p(t["vit_h"], t["aio_h"]), 0))] for c, t in AIO.items()]
              + [["<b>%s</b>" % x("Toplam", "Total"), cell(TOP["n"]), cell(TOP["aio"]), n(yzd(_p(TOP["aio"], TOP["n"]), 0)), cell(TOP["vitra"]), n(yzd(_p(TOP["vitra"], TOP["aio"]), 0)), n(yzd(_p(TOP["vit_h"], TOP["aio_h"]), 0))]])
_sir = sorted([(c, _p(t["vitra"], t["aio"])) for c, t in AIO.items() if t["aio"] >= 20], key=lambda i: -i[1])
INS_AIO = insight(("**SEOmonitor'de takip edilen %s kelimenin %s mobilde AI Overview çıkmaktadır ve VitrA bu kelimelerin %s kaynak gösterilmektedir**. AI Overview en sık armatür ve vitrifiye kelimelerinde çıkmaktadır. VitrA'nın AI Overview içindeki payı %s; en sınırlı kaldığı kategoriler %s. Bu kategorilerde soruya doğrudan yanıt veren kategori ve rehber içeriği, kaynak gösterilme payını artırabilir.")
                  % (bin(TOP["n"]), ek(TOP["aio"], "inde"), yzd(_p(TOP["vitra"], TOP["aio"]), 0) + "'" + ek(round(_p(TOP["vitra"], TOP["aio"])), "inde").split("'")[1],
                     ", ".join("%s %s" % (c.lower(), yzd(v, 0)) for c, v in _sir[:2]) + " ile en yüksek", ", ".join("%s (%s)" % (c.lower(), yzd(v, 0)) for c, v in _sir[-2:])),
                  ("**%s of the %s keywords tracked in SEOmonitor show an AI Overview on mobile, and VitrA is cited in %s of them**. AI Overviews appear most often on tap and sanitaryware keywords. VitrA's share within AI Overviews is highest in %s; the most limited categories are %s. In these categories, category and guide content that answers the question directly can increase the citation share.")
                  % (f"{TOP['aio']:,}", f"{TOP['n']:,}", ("%.0f" % _p(TOP["vitra"], TOP["aio"])) + "%", ", ".join("%s %s" % (_EN[c].lower(), ("%.0f" % v) + "%") for c, v in _sir[:2]),
                     ", ".join("%s (%s)" % (_EN[c].lower(), ("%.0f" % v) + "%") for c, v in _sir[-2:])), "D42")
# ---------------------------------------------------------------- Google click payi (share of clicks), mobil, son 15 gun ortalamasi
def _ort(gunler):
    t = _c.defaultdict(list)
    for g in gunler:
        for d in g["domains"]:
            if d["domain"] not in ("sum_top_10", "others"): t[d["domain"]].append(d["share_of_clicks"])
    n_ = len(gunler)
    return {k_: 100 * sum(v_) / n_ for k_, v_ in t.items()}
SOC = {ad: _ort(g) for ad, g in _SOC["grup"].items()}
SOC0 = _ort(_SOC["tum_onceki"])
_KISA = {"trendyol.com": "Trendyol", "koctas.com.tr": "Koçtaş", "hepsiburada.com": "Hepsiburada", "kale.com.tr": "Kale", "shop.creavit.com.tr": "Creavit", "akakce.com": "Akakçe", "tr.pinterest.com": "Pinterest",
         "sahibinden.com": "Sahibinden", "banyomarka.com": "Banyomarka", "ikea.com.tr": "IKEA", "bauhaus.com.tr": "Bauhaus", "dusakabincim.com": "Duşakabincim", "egeseramikshop.com": "Ege Seramik"}
def _ilk(d, n_=3):
    L = sorted([(k_, v_) for k_, v_ in d.items() if k_ != "vitra.com.tr"], key=lambda i: -i[1])[:n_]
    return ", ".join("%s %s" % (k_, yzd(v_, 1)) for k_, v_ in L), ", ".join("%s %s" % (k_, ("%.1f" % v_) + "%") for k_, v_ in L)
_SIRA = ["Tümü", "Vitrifiyeler", "Banyo Mobilyaları", "Armatürler", "Duşlar", "Yıkanma Alanları", "Rezervuarlar", "Banyo Aksesuarları", "Karo Seramik Ürünleri", "Marka"]
def _vs(d): return d.get("vitra.com.tr", 0)
def _sira(d):
    L = sorted(d.items(), key=lambda i: -i[1]); return next((i + 1 for i, (k_, _) in enumerate(L) if k_ == "vitra.com.tr"), None)
T_SOC = tablo([th("Kategori", "Category", "SEOmonitor'de takip edilen kelime grubu; Marka, VitrA ve Artema adıyla yapılan aramalardır.", "Keyword group tracked in SEOmonitor; Brand covers searches with the VitrA and Artema names."),
               th("vitra.com.tr click payı", "vitra.com.tr click share", "Gruptaki kelimelerden gelen tahmini organik click'lerin vitra.com.tr'ye düşen payı; mobil, 19 Eyl - 3 Eki 2026 günlük ortalaması.", "Share of estimated organic clicks from the group's keywords going to vitra.com.tr; mobile, daily average 19 Sep - 3 Oct 2026.", True),
               th("VitrA'nın sırası", "VitrA's rank", "vitra.com.tr'nin click payına göre alan adları arasındaki sırası.", "vitra.com.tr's rank among domains by click share.", True),
               th("En yüksek payı alan üç rakip", "Top three competitors by share", "vitra.com.tr dışında en yüksek click payını alan üç alan adı ve payları.", "The three domains other than vitra.com.tr with the highest click share, with their shares.")],
              [[x(g, _EN.get(g, g)), n(yzd(_vs(SOC[g]), 1)), cell(_sira(SOC[g])), x(*_ilk(SOC[g]))] for g in _SIRA if g in SOC])
_v0 = SOC0.get("vitra.com.tr", 0) + SOC0.get("online.vitra.com.tr", 0)
_KZ = sorted([(g, _vs(SOC[g])) for g in _SIRA[1:-1] if g in SOC], key=lambda i: -i[1])
INS_SOC = insight(("**vitra.com.tr, takip edilen tüm kelimelerde mobil click'lerin %s almaktadır ve Trendyol'dan (%s) sonra ikinci sıradadır**; Koçtaş %s, Hepsiburada %s ile izlemektedir. Geçen yılın aynı döneminde vitra.com.tr ve online.vitra.com.tr birlikte %s almaktaydı; alan adı birleşmesinden sonra pay yükselmiştir. Kategorilerde VitrA'nın payı %s en yüksek, %s en düşüktür; karoda Kale ve Koçtaş, aksesuar ve armatürde Trendyol öndedir.")
                  % (yzd(_vs(SOC["Tümü"]), 1) + "'" + ek(round(_vs(SOC["Tümü"])), "i").split("'")[1], yzd(SOC["Tümü"].get("trendyol.com", 0), 1), yzd(SOC["Tümü"].get("koctas.com.tr", 0), 1), yzd(SOC["Tümü"].get("hepsiburada.com", 0), 1),
                     yzd(_v0, 1) + "'" + ek(round(_v0), "i").split("'")[1], " ve ".join("%s (%s)" % (g.lower(), yzd(v, 1)) for g, v in _KZ[:2]) + " kategorilerinde", " ve ".join("%s (%s)" % (g.lower(), yzd(v, 1)) for g, v in _KZ[-2:])),
                  ("**vitra.com.tr takes %s of mobile clicks across all tracked keywords and ranks second after Trendyol (%s)**; Koçtaş follows with %s and Hepsiburada with %s. In the same period last year vitra.com.tr and online.vitra.com.tr together took %s; the share has risen after the domain merger. By category VitrA's share is highest in %s and lowest in %s; Kale and Koçtaş lead in tiles, and Trendyol in accessories and taps.")
                  % (("%.1f" % _vs(SOC["Tümü"])) + "%", ("%.1f" % SOC["Tümü"].get("trendyol.com", 0)) + "%", ("%.1f" % SOC["Tümü"].get("koctas.com.tr", 0)) + "%", ("%.1f" % SOC["Tümü"].get("hepsiburada.com", 0)) + "%",
                     ("%.1f" % _v0) + "%", " and ".join("%s (%s)" % (_EN[g].lower(), ("%.1f" % v) + "%") for g, v in _KZ[:2]), " and ".join("%s (%s)" % (_EN[g].lower(), ("%.1f" % v) + "%") for g, v in _KZ[-2:])), "D42")
HTML_SOC = '<h3>%s</h3>%s%s%s' % (x("Google'da click payı: vitra.com.tr ve rakipler", "Click share on Google: vitra.com.tr and competitors"), T_SOC, INS_SOC,
                                  kaynak("SEOmonitor · vitra.com.tr kampanyası, takip edilen %s kelime · mobil tahmini click payı, 19 Eyl - 3 Eki 2026 günlük ortalama; geçen yıl 19 Eyl - 3 Eki 2025" % bin(TOP["n"]),
                                         "SEOmonitor · vitra.com.tr campaign, %s tracked keywords · mobile estimated click share, daily average 19 Sep - 3 Oct 2026; last year 19 Sep - 3 Oct 2025" % f"{TOP['n']:,}", "D42"))
