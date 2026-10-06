# -*- coding: utf-8 -*-
"""Bölüm: GA4 - Site ve E-Ticaret Performansı (VitrA ekibinin GA4 dışa aktarımı, 05.10.2026; veri/islenmis/ga4.json, ga4_analiz.py)."""
from ortak import *
import json as _json, os as _os, re as _re
from rapor_parca1 import cizgi
from b_talep import sekmeler, AYA, YRENK
from grafik2 import kombo2 as _kombo2, f_k as _fk, gruplu as _gr, halka as _halka
from yatay import yatay as _yatay
import gsc12 as _G12
G = _json.load(open(_os.path.join(veri.V, "islenmis", "ga4.json"), encoding="utf-8"))
GN, KN = G["genel"], G["kanal"]
AD = [a for a, _ in AYA]
def _g(y, m, a): return (GN.get("%d-%02d" % (y, m)) or {}).get(a)
def _top(y, a, m2=9): return sum(_g(y, m, a) or 0 for m in range(1, m2 + 1))
def _deg(a, b): return (b / a - 1) * 100 if a else None
def tl(v):
    t = (k(v) if v >= 1000 else bin(v)) + " TL"; x(t, t.replace(",", ".")); return t
def _pe(v): return ("%.1f" % v) + "%"
def _isr(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + "%" + ("%.1f" % abs(v)).replace(".", ",")
def _isr_en(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + ("%.1f" % abs(v)) + "%"
r25, r26 = _top(2025, "gelir"), _top(2026, "gelir"); p25, p26 = _top(2025, "satin"), _top(2026, "satin"); o25, o26 = _top(2025, "oturum"), _top(2026, "oturum")
aov25, aov26 = r25 / p25, r26 / p26
D_GEN = ("Oca 2025 - Eyl 2026", "Jan 2025 - Sep 2026"); D_OE = ("Oca-Eyl 2025 ve 2026", "Jan-Sep 2025 and 2026")
D_12 = ("1 Eyl 2025 - 30 Eyl 2026", "1 Sep 2025 - 30 Sep 2026"); D_AR = ("1 May - 30 Eyl 2026", "1 May - 30 Sep 2026")

# ---------------------------------------------------------------- 1 · aylık genel görünüm
x("Gelir", "Revenue"); x("Satın alma", "Purchases"); x("Oturum", "Sessions")
def _tlk(v): t = k(v) + " TL" if v >= 1000 else bin(v) + " TL"; return x(t, t.replace(",", "."))
def _ad(v): t = bin(round(v)); return x(t, f"{round(v):,}")
def _yil(y, a): return [_g(y, m, a) for m in range(1, 13)]
G_GELIR = _kombo2(AD, [{"ad": x("Gelir 2025", "Revenue 2025"), "renk": "#10332F", "deger": _yil(2025, "gelir"), "tip": "cubuk", "bicim": _tlk, "eksen_ad": x("Gelir", "Revenue")},
                       {"ad": x("Gelir 2026", "Revenue 2026"), "renk": "#E85F36", "deger": _yil(2026, "gelir"), "tip": "cubuk", "bicim": _tlk},
                       {"ad": x("Satın alma 2025", "Purchases 2025"), "renk": "#5B7FA6", "deger": _yil(2025, "satin"), "tip": "cizgi", "eksen": "sag", "bicim": _ad, "eksen_ad": x("Satın alma", "Purchases")},
                       {"ad": x("Satın alma 2026", "Purchases 2026"), "renk": "#F5A623", "deger": _yil(2026, "satin"), "tip": "cizgi", "eksen": "sag", "bicim": _ad}],
                  cap=x("Aylık e-ticaret geliri (çubuk, sol eksen) ve satın alma sayısı (çizgi, sağ eksen) · 2025 ve 2026", "Monthly e-commerce revenue (bars, left axis) and number of purchases (lines, right axis) · 2025 and 2026"))
_AY21 = list(GN)
_ET21 = ["%s %s" % (AYA[int(m[5:]) - 1][0], m[2:4]) for m in _AY21]
for m, e in zip(_AY21, _ET21): x(e, "%s %s" % (AYA[int(m[5:]) - 1][1], m[2:4]))
G_SERI = _kombo2(_ET21, [{"ad": x("Gelir", "Revenue"), "renk": "#B9C6C3", "deger": [GN[m]["gelir"] for m in _AY21], "tip": "cubuk", "bicim": _tlk, "eksen_ad": x("Gelir", "Revenue")},
                         {"ad": x("Satın alma", "Purchases"), "renk": "#E85F36", "deger": [GN[m]["satin"] for m in _AY21], "tip": "cizgi", "eksen": "sag", "bicim": _ad, "eksen_ad": x("Satın alma", "Purchases")},
                         {"ad": x("Oturum", "Sessions"), "renk": "#10332F", "deger": [GN[m]["oturum"] for m in _AY21], "tip": "kesik", "eksen": "sag2", "bicim": _fk, "eksen_ad": x("Oturum", "Sessions")}],
                 cap=x("Oca 2025 - Eyl 2026 aylık seri · gelir (çubuk), satın alma (çizgi) ve oturum (kesikli çizgi); Aralık 2025'teki oturum artışı www.vitra.com.tr trafiğinin bu GA4 mülküne katılmasından kaynaklanır",
                       "Monthly series Jan 2025 - Sep 2026 · revenue (bars), purchases (line) and sessions (dashed line); the jump in sessions in December 2025 comes from www.vitra.com.tr traffic joining this GA4 property"))
G_AYLIK = sekmeler([("Gelir ve satın alma: 2025 ve 2026", "Revenue and purchases: 2025 and 2026", G_GELIR), ("Oca 2025 - Eyl 2026 seri", "Jan 2025 - Sep 2026 series", G_SERI)], "gtabs")
_YR = [("2025", YRENK["2025"]), ("2026", YRENK["2026"])]
def _aov(y): return [(_g(y, m, "gelir") / _g(y, m, "satin")) if _g(y, m, "satin") else None for m in range(1, 13)]
T_AYLIK = (_yatay("Gelir (TL)", "Revenue (TL)", "Aylık e-ticaret geliri (Total revenue, TL). Değişim aynı ayın 2025'e göre yüzde değişimidir.", "Monthly e-commerce revenue (Total revenue, TL). Change is the percentage change against the same month of 2025.",
                  [("2025", YRENK["2025"], _yil(2025, "gelir"), r25), ("2026", YRENK["2026"], _yil(2026, "gelir"), r26)], _tlk)
           + _yatay("Satın alma", "Purchases", "Aylık e-ticaret satın alma sayısı (Ecommerce purchases).", "Monthly number of e-commerce purchases (Ecommerce purchases).",
                    [("2025", YRENK["2025"], _yil(2025, "satin"), p25), ("2026", YRENK["2026"], _yil(2026, "satin"), p26)], _ad)
           + _yatay("Ort. sipariş tutarı", "Avg. order value", "Gelir / satın alma (TL); Oca-Eyl sütunu dönem toplamlarından hesaplanmıştır.", "Revenue / purchases (TL); the Jan-Sep column is calculated from the period totals.",
                    [("2025", YRENK["2025"], _aov(2025), aov25), ("2026", YRENK["2026"], _aov(2026), aov26)], _tlk)
           + _yatay("Oturum", "Sessions", "Aylık oturum. Aralık 2025'te www.vitra.com.tr trafiği bu GA4 mülküne katıldığı için Aralık öncesi ve sonrası doğrudan kıyaslanmaz.", "Monthly sessions. As www.vitra.com.tr traffic joined this GA4 property in December 2025, before and after December are not directly comparable.",
                    [("2025", YRENK["2025"], _yil(2025, "oturum"), o25), ("2026", YRENK["2026"], _yil(2026, "oturum"), o26)], lambda v: _fk(v)))
_cr25 = 100 * p25 / o25; _cr26 = 100 * p26 / o26
INS_AYLIK = insight("Ocak - Eylül 2026'da e-ticaret geliri 2025'in aynı aylarına göre %s artarak %s'ye, satın alma sayısı %s artarak %s'e ulaşmıştır; ortalama sipariş tutarı %s'den %s'ye yükselmiştir. Gelir artışı Haziran - Eylül'de yoğunlaşmaktadır. Oturum sayısı Aralık 2025'ten itibaren yaklaşık dört katına çıkmıştır: bu, www.vitra.com.tr trafiğinin aynı GA4 mülküne katılmasının sonucudur; bu nedenle oturum başına dönüşüm oranı (2025'te %s, 2026'da %s) iki dönem arasında kıyaslanmamalıdır."
                    % (yz(_deg(r25, r26)), tl(r26), yz(_deg(p25, p26)), bin(p26), tl(aov25), tl(aov26), yzd(_cr25, 2), yzd(_cr26, 2)),
                    "In January - September 2026, e-commerce revenue rose %s against the same months of 2025 to %s and the number of purchases rose %s to %s; the average order value increased from %s to %s. The revenue growth is concentrated in June - September. Sessions roughly quadrupled from December 2025: this is the result of www.vitra.com.tr traffic joining the same GA4 property, so the conversion rate per session (%s in 2025, %s in 2026) should not be compared between the two periods."
                    % (yz(_deg(r25, r26)), tl(r26), yz(_deg(p25, p26)), f"{int(p26):,}", tl(aov25), tl(aov26), yzd(_cr25, 2), yzd(_cr26, 2)), "D45")

# ---------------------------------------------------------------- 2 · kanal performansı
KEN = {"Organic Search": "Organic Search", "Paid Search": "Paid Search", "Direct": "Direct", "Paid Social": "Paid Social", "Unassigned": "Unassigned", "Cross-network": "Cross-network",
       "Organic Social": "Organic Social", "AI Assistant": "AI Assistant", "Referral": "Referral", "Organic Shopping": "Organic Shopping", "Mobile Push Notifications": "Mobile Push Notifications",
       "Email": "Email", "Display": "Display", "SMS": "SMS", "Paid Other": "Paid Other", "Organic Video": "Organic Video", "Paid Video": "Paid Video"}
for k_ in KN: x(k_, k_)
def _kt(k_, y, a): return sum((KN[k_].get("%d-%02d" % (y, m)) or {}).get(a) or 0 for m in range(1, 10))
KS = sorted(KN, key=lambda k_: -_kt(k_, 2026, "gelir"))
KS = [k_ for k_ in KS if _kt(k_, 2026, "oturum") + _kt(k_, 2025, "oturum") >= 1000]
_tg26 = sum(_kt(k_, 2026, "gelir") for k_ in KN); _tg25 = sum(_kt(k_, 2025, "gelir") for k_ in KN)
rows_k = []
for k_ in KS:
    s5, s6, a5, a6, g5, g6 = _kt(k_, 2025, "oturum"), _kt(k_, 2026, "oturum"), _kt(k_, 2025, "satin"), _kt(k_, 2026, "satin"), _kt(k_, 2025, "gelir"), _kt(k_, 2026, "gelir")
    rows_k.append([x(k_, k_), cellk(s5), cellk(s6), cell(a5), cell(a6), n(tl(g5) if g5 else "-"), n(tl(g6) if g6 else "-"), n(yz(_deg(g5, g6)) if g5 >= 50000 else "-"), n(yzd(100 * g6 / _tg26)), n(yzd(100 * a6 / s6, 2) if s6 else "-")])
T_KANAL = tablo([th("Kanal", "Channel", "GA4 varsayılan kanal grubu (Session default channel group).", "GA4 session default channel group."),
                 th("Oturum 2025", "Sessions 2025", "Oca-Eyl 2025 oturum.", "Sessions, Jan-Sep 2025.", True), th("Oturum 2026", "Sessions 2026", "Oca-Eyl 2026 oturum; Aralık 2025'ten itibaren www.vitra.com.tr trafiği dahildir.", "Sessions, Jan-Sep 2026; www.vitra.com.tr traffic included from December 2025.", True),
                 th("Satın alma 2025", "Purchases 2025", "Oca-Eyl 2025 e-ticaret satın alma.", "E-commerce purchases, Jan-Sep 2025.", True), th("Satın alma 2026", "Purchases 2026", "Oca-Eyl 2026 e-ticaret satın alma.", "E-commerce purchases, Jan-Sep 2026.", True),
                 th("Gelir 2025", "Revenue 2025", "Oca-Eyl 2025 gelir (TL).", "Revenue, Jan-Sep 2025 (TL).", True), th("Gelir 2026", "Revenue 2026", "Oca-Eyl 2026 gelir (TL).", "Revenue, Jan-Sep 2026 (TL).", True),
                 th("Gelir YoY", "Revenue YoY", "Oca-Eyl 2026 gelirinin 2025'in aynı aylarına göre değişimi; 2025 geliri 50K TL'nin altındaki kanallarda gösterilmemiştir.", "Change of Jan-Sep 2026 revenue against the same months of 2025; not shown for channels with 2025 revenue below 50K TL.", True),
                 th("Gelir payı 2026", "Revenue share 2026", "Kanalın Oca-Eyl 2026 toplam gelirindeki payı.", "The channel's share of total Jan-Sep 2026 revenue.", True),
                 th("Dönüşüm oranı 2026", "Conversion rate 2026", "Satın alma / oturum, Oca-Eyl 2026.", "Purchases / sessions, Jan-Sep 2026.", True)], rows_k, "dar")
_KG = [k_ for k_ in KS if _kt(k_, 2026, "gelir") >= 200000 or _kt(k_, 2025, "gelir") >= 200000]
G_KANAL = _gr([(x(k_, k_), [_kt(k_, 2025, "gelir"), _kt(k_, 2026, "gelir")]) for k_ in _KG],
              [(x("Gelir Oca-Eyl 2025", "Revenue Jan-Sep 2025"), "#9AA8A5"), (x("Gelir Oca-Eyl 2026", "Revenue Jan-Sep 2026"), "#10332F")],
              x("Kanal bazında e-ticaret geliri · Oca-Eyl 2025 ve 2026 (TL)", "E-commerce revenue by channel · Jan-Sep 2025 and 2026 (TL)"), bicim=_tlk)
_KC = ["Organic Search", "Paid Search", "Direct", "Paid Social", "AI Assistant"]
_RKC = ["#10332F", "#E85F36", "#7A8C89", "#F5A623", "#5B7FA6"]
G_KAY = cizgi([(x(k_, k_), r_, [(KN[k_].get(m) or {}).get("gelir") or 0 for m in _AY21]) for k_, r_ in zip(_KC, _RKC)],
              y_etiket=x("Aylık gelir · kanal bazında, Oca 2025 - Eyl 2026 (TL; lejanttan kanal açılıp kapatılabilir)", "Monthly revenue · by channel, Jan 2025 - Sep 2026 (TL; channels can be switched on and off in the legend)"),
              aylar=_ET21, x_etiket=_ET21, olcek=True)
_o = lambda k_, y, a: _kt(k_, y, a)
_os_, _ai = "Organic Search", "AI Assistant"
INS_KANAL = insight("Ocak - Eylül 2026'da gelirin %s'i organik aramadan gelmektedir (2025'te %s); organik aramanın geliri %s → %s (%s), satın alması %s → %s olmuştur. Bu artışın bir bölümü, Aralık 2025'te www.vitra.com.tr'ye gelen organik trafiğin mağazayla aynı sitede buluşmasıyla ilişkilendirilebilir. Paid Search geliri %s, Direct %s artmıştır; 2026'da Meta reklamları Paid Social kanalında %s gelir getirmiştir (2025'te aynı reklamlar Organic Social altında izlenmektedir). **Yapay zeka asistanlarından gelen trafik (AI Assistant) 2026'da %s oturum, %s satın alma ve %s gelir üretmiştir**; dönüşüm oranı (%s) organik aramanın (%s) üzerindedir (Bölüm [[b:geo]])."
                    % (yzd(100 * _o(_os_, 2026, "gelir") / _tg26), yzd(100 * _o(_os_, 2025, "gelir") / _tg25), tl(_o(_os_, 2025, "gelir")), tl(_o(_os_, 2026, "gelir")), yz(_deg(_o(_os_, 2025, "gelir"), _o(_os_, 2026, "gelir"))),
                       bin(_o(_os_, 2025, "satin")), bin(_o(_os_, 2026, "satin")), yz(_deg(_o("Paid Search", 2025, "gelir"), _o("Paid Search", 2026, "gelir"))), yz(_deg(_o("Direct", 2025, "gelir"), _o("Direct", 2026, "gelir"))),
                       tl(_o("Paid Social", 2026, "gelir")), bin(_o(_ai, 2026, "oturum")), bin(_o(_ai, 2026, "satin")), tl(_o(_ai, 2026, "gelir")), yzd(100 * _o(_ai, 2026, "satin") / _o(_ai, 2026, "oturum"), 2), yzd(100 * _o(_os_, 2026, "satin") / _o(_os_, 2026, "oturum"), 2)),
                    "In January - September 2026, %s of revenue comes from organic search (%s in 2025); organic search revenue went %s → %s (%s) and purchases %s → %s. Part of this growth can be associated with the organic traffic to www.vitra.com.tr meeting the shop on the same site from December 2025. Paid Search revenue rose %s and Direct %s; in 2026 Meta ads brought %s of revenue in the Paid Social channel (in 2025 the same ads were tracked under Organic Social). **Traffic from AI assistants (AI Assistant) produced %s sessions, %s purchases and %s of revenue in 2026**; its conversion rate (%s) is above organic search (%s) (Section [[b:geo]])."
                    % (yzd(100 * _o(_os_, 2026, "gelir") / _tg26), yzd(100 * _o(_os_, 2025, "gelir") / _tg25), tl(_o(_os_, 2025, "gelir")), tl(_o(_os_, 2026, "gelir")), yz(_deg(_o(_os_, 2025, "gelir"), _o(_os_, 2026, "gelir"))),
                       f"{int(_o(_os_, 2025, 'satin')):,}", f"{int(_o(_os_, 2026, 'satin')):,}", yz(_deg(_o("Paid Search", 2025, "gelir"), _o("Paid Search", 2026, "gelir"))), yz(_deg(_o("Direct", 2025, "gelir"), _o("Direct", 2026, "gelir"))),
                       tl(_o("Paid Social", 2026, "gelir")), f"{int(_o(_ai, 2026, 'oturum')):,}", f"{int(_o(_ai, 2026, 'satin')):,}", tl(_o(_ai, 2026, "gelir")), yzd(100 * _o(_ai, 2026, "satin") / _o(_ai, 2026, "oturum"), 2), yzd(100 * _o(_os_, 2026, "satin") / _o(_os_, 2026, "oturum"), 2)), "D45")
_KY = [r for r in G["kaynak_2026"] if r["oturum"]][:15]
for r in _KY: x(r["sm"], r["sm"])
T_KAYNAK = tablo([th("Kaynak / ortam", "Source / medium", "GA4 oturum kaynağı ve ortamı (Session source / medium).", "GA4 session source and medium."),
                  th("Oturum", "Sessions", "1 Oca - 5 Eki 2026 oturum.", "Sessions, 1 Jan - 5 Oct 2026.", True), th("Satın alma", "Purchases", "Aynı dönemde e-ticaret satın alma.", "E-commerce purchases in the same period.", True),
                  th("Gelir", "Revenue", "Aynı dönemde gelir (TL).", "Revenue in the same period (TL).", True), th("Dönüşüm oranı", "Conversion rate", "Satın alma / oturum.", "Purchases / sessions.", True),
                  th("Etkileşim oranı", "Engagement rate", "Etkileşimli oturumların oranı (Engagement rate).", "Share of engaged sessions (Engagement rate).", True)],
                 [[x(r["sm"], r["sm"]), cellk(r["oturum"]), cell(r["satin"] or 0), n(tl(r["gelir"]) if r["gelir"] else "-"), n(yzd(100 * (r["satin"] or 0) / r["oturum"], 2)), n(yzd(100 * (r["etkilesim"] or 0)))] for r in _KY], "dar")

# ---------------------------------------------------------------- 2b · giriş sayfası (landing page)
LT = G["lp_tur"]; LS = G["lp_oturum_top"]
LAD = {"odeme": ("Sepet, giriş ve ödeme adımları", "Cart, sign-in and checkout steps"), "anasayfa": ("Ana sayfa", "Home page"), "urun": ("Ürün sayfaları", "Product pages"),
       "kategori": ("Kategori sayfaları", "Category pages"), "koleksiyon": ("Koleksiyon, seri ve kampanya sayfaları", "Collection, series and campaign pages"),
       "arama": ("Site içi arama sonuçları", "Site search results"), "destek": ("Servis, destek ve satış noktaları", "Service, support and sales points"),
       "kurumsal": ("Kurumsal, proje ve katalog", "Corporate, projects and catalogues"), "blog": ("Blog (İlham Veren Fikirler)", "Blog (İlham Veren Fikirler)"), "diger": ("Diğer ve (not set)", "Other and (not set)")}
def _lt(t, y, i): return (LT.get(t, {}).get(str(y)) or [0, 0, 0, 0])[i]
_lg25 = sum(_lt(t, 2025, 1) for t in LT); _lg26 = sum(_lt(t, 2026, 1) for t in LT)
_LSIRA = sorted(LT, key=lambda t: (t == "diger", -_lt(t, 2026, 1)))
rows_lp = []
for t in _LSIRA:
    g5, g6, o6 = _lt(t, 2025, 1), _lt(t, 2026, 1), _lt(t, 2026, 0)
    rows_lp.append([x(*LAD[t]), n(yzd(100 * o6 / LS["2026"])), n(tl(g5) if g5 >= 1000 else "-"), n(tl(g6) if g6 >= 1000 else "-"), n(yz(_deg(g5, g6)) if g5 >= 50000 else "-"),
                    n(yzd(100 * g6 / _lg26)), n(yzd(100 * _lt(t, 2026, 3) / o6) if o6 else "-")])
T_LP = tablo([th("Giriş sayfası türü", "Landing page type", "Oturumun başladığı sayfanın türü; eski mağaza (/tr/...) ve yeni site adresleri aynı türlere eşlenmiştir.", "Type of the page where the session started; old shop (/tr/...) and new site addresses are mapped to the same types."),
              th("Oturum payı 2026", "Share of sessions 2026", "Türün Oca-Eyl 2026 landing page raporundaki oturumlar içindeki payı.", "The type's share of sessions in the landing page report, Jan-Sep 2026.", True),
              th("Gelir 2025", "Revenue 2025", "Bu türdeki sayfalarla başlayan oturumların Oca-Eyl 2025 geliri (TL).", "Jan-Sep 2025 revenue of sessions starting on pages of this type (TL).", True),
              th("Gelir 2026", "Revenue 2026", "Bu türdeki sayfalarla başlayan oturumların Oca-Eyl 2026 geliri (TL).", "Jan-Sep 2026 revenue of sessions starting on pages of this type (TL).", True),
              th("Gelir YoY", "Revenue YoY", "Oca-Eyl 2026 gelirinin 2025'in aynı aylarına göre değişimi; 2025 geliri 50K TL'nin altındaki türlerde gösterilmemiştir.", "Change of Jan-Sep 2026 revenue against the same months of 2025; not shown for types with 2025 revenue below 50K TL.", True),
              th("Gelir payı 2026", "Revenue share 2026", "Türün Oca-Eyl 2026 toplam gelirindeki payı.", "The type's share of total Jan-Sep 2026 revenue.", True),
              th("Etkileşim oranı 2026", "Engagement rate 2026", "Etkileşimli oturumların oranı (Engagement rate), Oca-Eyl 2026.", "Share of engaged sessions (Engagement rate), Jan-Sep 2026.", True)], rows_lp, "dar")
LO = G["lp_odeme_ay"]; _LOA = [m for m in _AY21 if m in LO]
G_LP = _kombo2([_ET21[_AY21.index(m)] for m in _LOA],
               [{"ad": x("Toplam gelir", "Total revenue"), "renk": "#C9D3D1", "deger": [LO[m][1] for m in _LOA], "tip": "cubuk", "bicim": _tlk, "eksen_ad": x("Gelir", "Revenue")},
                {"ad": x("Sepet, giriş ve ödeme adımlarında başlayan oturumların geliri", "Revenue of sessions starting at cart, sign-in and checkout steps"), "renk": "#E85F36", "deger": [LO[m][0] for m in _LOA], "tip": "cubuk", "ortu": True, "bicim": _tlk}],
               cap=x("Aylık gelir (gri çubuk) ve içinde sepet, giriş ve ödeme sayfalarında başlayan oturumların geliri (turuncu); çubuk üstündeki oran bu oturumların gelir payıdır · Oca 2025 - Eyl 2026",
                     "Monthly revenue (grey bar) with the revenue of sessions starting on cart, sign-in and checkout pages inside it (orange); the figure above the bar is these sessions' share of revenue · Jan 2025 - Sep 2026"),
               ust_etiket=[x(yzd(100 * LO[m][0] / LO[m][1]), _pe(100 * LO[m][0] / LO[m][1])) for m in _LOA])
LP26 = G["lp_2026"]
def _lprow(r):
    p_, t, o, g, ke, eo = r
    return [u("https://www.vitra.com.tr" + p_, p_) if p_ != "(not set)" else x("(not set)", "(not set)"), x(*LAD[t]), n(tl(g) if g >= 1000 else "-"), n(yzd(100 * g / _lg26, 2)), n(yzd(100 * o / LS["2026"], 2)), n(yzd(100 * eo / o) if o else "-")]
_LPH = [th("Giriş sayfası", "Landing page", "Oturumun başladığı sayfa; bağlantı canlı sayfaya gider.", "The page where the session started; the link opens the live page."),
        th("Tür", "Type", "Giriş sayfası türü.", "Landing page type."),
        th("Gelir", "Revenue", "Bu sayfayla başlayan oturumların Oca-Eyl 2026 geliri (TL).", "Jan-Sep 2026 revenue of sessions starting on this page (TL).", True),
        th("Gelir payı", "Revenue share", "Oca-Eyl 2026 toplam gelirindeki pay.", "Share of total Jan-Sep 2026 revenue.", True),
        th("Oturum payı", "Share of sessions", "Oca-Eyl 2026 landing page raporundaki oturumlar içindeki pay.", "Share of sessions in the landing page report, Jan-Sep 2026.", True),
        th("Etkileşim oranı", "Engagement rate", "Etkileşimli oturumların oranı (Engagement rate).", "Share of engaged sessions (Engagement rate).", True)]
_LPG = [r for r in LP26 if r[1] != "odeme"][:15]
_LPO = sorted([r for r in LP26 if r[1] != "odeme" and r[0] != "(not set)"], key=lambda r: -r[2])[:15]
T_LPS = sekmeler([("Gelire göre ilk 15", "Top 15 by revenue", tablo(_LPH, [_lprow(r) for r in _LPG], "dar xl")),
                  ("Oturuma göre ilk 15", "Top 15 by sessions", tablo(_LPH, [_lprow(r) for r in _LPO], "dar xl"))], "ttabs")
_qf = next(r for r in LP26 if r[0] == "/v/vitra-quantumflush-i")
_bl6 = _lt("blog", 2026, 1)
INS_LP = insight("Ocak - Eylül 2026 gelirinin %s'i sepet, giriş ve ödeme sayfalarında başlayan oturumlarda görünmektedir (2025'in aynı aylarında %s); bu sayfalar oturumların yalnız %s'ini oluşturmaktadır. **Kullanıcı ödeme adımında siteye yeni bir oturumla girmiş sayılmakta ve satın almayı başlatan giriş sayfası bu oturumda görünmemektedir**; örüntü ödeme sırasında banka doğrulaması gibi site dışı bir adımdan dönüşle ya da oturum zaman aşımıyla ilişkilendirilebilir. Kalan gelirde ana sayfa (%s), ürün sayfaları (%s) ve kategori sayfaları (%s) öne çıkmaktadır. QuantumFlush tanıtım sayfası 2026'da giriş sayfası oturumlarının %s'ini almış, gelirin %s'ini getirmiştir; blog yazılarıyla başlayan oturumların geliri %s'dir. Ödeme adımında oturumun neden yenilendiğinin incelenmesi, giriş sayfası ve kanal bazında gelirin eksiksiz okunmasını sağlayabilir."
                 % (yzd(100 * _lt("odeme", 2026, 1) / _lg26), yzd(100 * _lt("odeme", 2025, 1) / _lg25), yzd(100 * _lt("odeme", 2026, 0) / LS["2026"]), yzd(100 * _lt("anasayfa", 2026, 1) / _lg26), yzd(100 * _lt("urun", 2026, 1) / _lg26), yzd(100 * _lt("kategori", 2026, 1) / _lg26),
                    yzd(100 * _qf[2] / LS["2026"]), yzd(100 * _qf[3] / _lg26), tl(_bl6)),
                 "%s of January - September 2026 revenue appears in sessions starting on cart, sign-in and checkout pages (%s in the same months of 2025); these pages account for only %s of sessions. **The user is counted as entering the site with a new session at the payment step, and the landing page that started the purchase does not appear in that session**; the pattern can be associated with returning from an off-site step such as bank verification during payment, or with a session timeout. In the remaining revenue, the home page (%s), product pages (%s) and category pages (%s) stand out. The QuantumFlush promotion page took %s of landing page sessions in 2026 and brought %s of revenue; sessions starting on blog articles produced %s of revenue. Reviewing why the session restarts at the payment step can make it possible to read revenue by landing page and channel in full."
                 % (yzd(100 * _lt("odeme", 2026, 1) / _lg26), yzd(100 * _lt("odeme", 2025, 1) / _lg25), yzd(100 * _lt("odeme", 2026, 0) / LS["2026"]), yzd(100 * _lt("anasayfa", 2026, 1) / _lg26), yzd(100 * _lt("urun", 2026, 1) / _lg26), yzd(100 * _lt("kategori", 2026, 1) / _lg26),
                    yzd(100 * _qf[2] / LS["2026"]), yzd(100 * _qf[3] / _lg26), tl(_bl6)), "D45")

# ---------------------------------------------------------------- 3 · site içi arama
from site_arama_deg import DEGK as _DEGK, DEG as _DEG
SINIF = [("parca", "Yedek parça ve tamamlayıcı", "Spare parts and complementary", r"stop val|süzge|suzge|sifon|ara musluk|conta|kartuş|kartus|iç takım|ic takim|şamandıra|samandira|menteşe|mentese|flatör|flator|yedek|vida|gider|spiral|hortum|valf|musluk başlığı|perlatör|perlator|bağlantı|dirsek|dirseği"),
         ("hizmet", "Hizmet, destek ve katalog", "Service, support and catalogue", r"(?<!gizli )\bmontaj\b|servis|garanti|iade|kargo|katalog|fiyat listesi|keşif|kesif|banyo asistan|randevu|mağaza|magaza|bayi|tasarla"),
         ("seri", "Seri, koleksiyon ve ürün kodu", "Series, collection and product code", r"^(?:vitra )?(origin|sento|metropole|integra|s20|s50|s60|r11|kitkat|zentrum|terrazzo|traverten|liquid|plural|istanbul|memoria|equal|nest|frame|retromix|cementera|marmori|naturalux|root|shift|matrix|v-care|aquacare|idealine|suit|mia|minimax|solid|joy|flow|marmostone|cardostone|urbancrete|resincrete|novatone|novapetra|nova|cementside|glora|miniworx|loop|outline|water jewels|options|valarte|valerte|uniq|step|arkitekta|d-light|ecora|serenada|form|tre|pure|base|t4|t6|focus|x-line|q-line|eternity|geo|prime|eco flow|ultra|retro|wood|bliss|cement|nuo|core|marin|set ?\d|limestone|hilton|dynamica|aquaheat|aqua|archiplan|arkitekt|beton-x|neo|quantum|marmo|ardea|kids|metropol|primr)\b|^[a-z]?\d{3,}(?![x*]\d)|^\d+[a-wyz]\d+|^[a-z]\d{2}\b|^\d{3}-\d"),
         ("olcu", "Ölçü, renk ve özellik", "Size, colour and feature", r"\d+\s?[x*]\s?\d+|\d+\s?cm|siyah|beyaz|altın|altin|bakır|bakir|\bmat\b|\bmatt\b|krom|gold|antrasit|\bgri\b|yeşil|kırmızı|mavi|krem|bej|pembe|lacivert|vizon|engelli|özel ihtiyaç|çocuk|cocuk|akıllı|akilli|temassız|temassiz|kanalsız|kanalsiz|mermer|marble|ahşap"),
         ("urun", "Ürün tipi", "Product type", r"lavabo|klozet|batarya|ayna|küvet|kuvet|eviye|evye|duş|dus|havlu|sabunluk|pisuvar|pisuar|kapak|dolap|rezervuar|karo|seramik|fayans|banyo|tezgah|kağıtlık|kagitlik|fırça|firca|askı|aski|çöp|cop|bide|panel|tekne|kanal|başlık|baslik|etajer|tuvalet|wc|hela|sıva altı|ankastre|aksesuar|raf|mutfak|musluk|taharet|kumanda|dispanser|süpürgelik|mozaik|çamaşır|basamak|armatür|çıkış ucu|çikiş ucu|bordür|kulp|sabun|kağıt|dekor|çanak|gömme rez|malzemelik")]
for a_, b_, c_, _ in SINIF: x(b_, c_)
x("Diğer", "Other")
def sinif(q):
    for a_, b_, c_, rx in SINIF:
        if _re.search(rx, q): return a_
    return "diger"
SAD = {a_: (b_, c_) for a_, b_, c_, _ in SINIF}; SAD["diger"] = ("Diğer", "Other")
AR = G["arama"]; ART = sum(r[1] for r in AR); ARO = sum(v["oturum"] for v in G["arama_donem"].values())   # iki dönemin tekil oturum toplamı
_sc = {}
for r in AR: s_ = sinif(r[0]); _sc[s_] = _sc.get(s_, 0) + r[1]
_DEGL = {a_.lower(): b_ for a_, b_ in _DEGK.items()}
rows_a = []
for q, c, s in AR[:30]:
    d_ = _DEGL.get(q)
    rows_a.append([kw(q), cell(c), cell(s), x(*SAD[sinif(q)]), x(*_DEG[d_]) if d_ else "-"])
T_ARAMA = tablo([th("Arama terimi", "Search term", "vitra.com.tr arama kutusuna yazılan terim (view_search_results olayı); küçük harfe çevrilip boşluklar tekilleştirilmiştir.", "The term typed into the vitra.com.tr search box (view_search_results event); lower-cased with spaces normalised."),
                 th("Arama", "Searches", "1 May - 30 Eyl 2026 view_search_results olay sayısı; 1 May - 31 Tem ve 1 Ağu - 30 Eyl 2026 dışa aktarımlarının toplamıdır.", "Number of view_search_results events, 1 May - 30 Sep 2026; the sum of the 1 May - 31 Jul and 1 Aug - 30 Sep 2026 exports.", True),
                 th("Oturum", "Sessions", "Terimin arandığı oturum sayısı, 1 May - 30 Eyl 2026.", "Number of sessions in which the term was searched, 1 May - 30 Sep 2026.", True),
                 th("Tür", "Type", "Terimin türü: ürün tipi, seri ve koleksiyon adı, yedek parça ve tamamlayıcı, ölçü ve özellik, hizmet ve destek.", "Type of the term: product type, series and collection name, spare parts and complementary, size and feature, service and support."),
                 th("Arama testi (04.10.2026)", "Search test (04.10.2026)", "Terim Bölüm [[b:yolculuk]]'daki site içi arama testinde denendiyse sonucu.", "The result if the term was tried in the site search test in Section [[b:yolculuk]].")], rows_a, "dar")
rows_s = [[x(*SAD[a_]), n(yzd(100 * _sc.get(a_, 0) / ART))] for a_ in ["urun", "seri", "parca", "olcu", "hizmet", "diger"]]
T_SINIF = tablo([th("Terim türü", "Term type", "Arama terimlerinin kural tabanlı sınıflaması.", "Rule-based classification of search terms."),
                 th("Arama payı", "Share of searches", "Türün toplam arama içindeki payı (1 May - 30 Eyl 2026, %s terim)." % bin(len(AR)), "The type's share of all searches (1 May - 30 Sep 2026, %s terms)." % f"{len(AR):,}", True)], rows_s, "dar")
def _sp(a_): return 100 * _sc.get(a_, 0) / ART
INS_ARAMA = insight("1 Mayıs - 30 Eylül 2026'da vitra.com.tr'de %s oturumda %s arama yapılmış ve %s farklı terim aranmıştır. Aramaların %s'i seri, koleksiyon adı ya da ürün kodu (Origin, Terrazzo, Sento, Minimax, Integra), %s'i ürün tipi (ayna, lavabo, batarya, kumanda paneli), %s'i ölçü, renk ya da özellik (60x120, engelli), %s'i yedek parça ve tamamlayıcı ürün (stop valf, sifon, süzgeç, ara musluk) içermektedir; montaj, servis ve katalog aramaları %s'te kalmaktadır. **Her beş aramadan ikisi belirli bir seri, koleksiyon ya da ürün koduna yöneliktir**; bu aramaların doğru ürün listesine ulaşması dönüşüm açısından önem taşımaktadır. En çok aranan terimlerden \"lavabo\", \"batarya\" ve \"integra\" site içi arama testinde sonuç sayfasında boş ya da ilgisiz sonuç vermiştir (Bölüm [[b:yolculuk]]); \"kartuş\", \"conta\" ve \"yedek parça\" aramalarında ilgili ürün bulunamamıştır."
                    % (k(ARO), k(ART), bin(len(AR)), yzd(_sp("seri")), yzd(_sp("urun")), yzd(_sp("olcu")), yzd(_sp("parca")), yzd(_sp("hizmet"))),
                    "In 1 May - 30 September 2026, %s searches were made on vitra.com.tr in %s sessions across %s distinct terms. %s of searches contain a series, collection name or product code (Origin, Terrazzo, Sento, Minimax, Integra), %s a product type (mirror, washbasin, tap, flush plate), %s a size, colour or feature (60x120, accessible) and %s a spare part or complementary product (stop valve, siphon, drain, angle valve); installation, service and catalogue searches stay at %s. **Two in five searches target a specific series, collection or product code**; these searches reaching the right product list matters for conversion. Among the most searched terms, \"lavabo\", \"batarya\" and \"integra\" returned an empty or off-target results page in the site search test (Section [[b:yolculuk]]); no relevant product was found for \"kartuş\", \"conta\" and \"yedek parça\"."
                    % (k(ART), k(ARO), bin(len(AR)), yzd(_sp("seri")), yzd(_sp("urun")), yzd(_sp("olcu")), yzd(_sp("parca")), yzd(_sp("hizmet"))), "D45")

# ---------------------------------------------------------------- 4 · ödeme ve teslimat adımı
OD, KG = G["odeme"], G["teslimat"]
odt, kgt = sum(v for _, v in OD), sum(v for _, v in KG)
x("(not set)", "(not set)")
OD_EN = {"Kredi Kartı / Banka Kartı": "Credit / debit card", "İyzico İle Öde": "Pay with iyzico", "EFT / Havale": "Bank transfer", "Kargo ile Teslimat": "Delivery by cargo"}
T_ODEME = ('<div class="two"><div>%s</div><div>%s</div></div>' % (
    tablo([th("Ödeme türü", "Payment type", "add_payment_info olayının payment_type parametresi.", "The payment_type parameter of the add_payment_info event."), th("Olay sayısı", "Event count", "%s olay sayısı." % D_12[0], "Event count, %s." % D_12[1], True), th("Pay", "Share", "Toplam içindeki pay.", "Share of the total.", True)],
          [[x(a_, OD_EN.get(a_, a_)), cell(v), n(yzd(100 * v / odt))] for a_, v in OD], "dar"),
    tablo([th("Teslimat türü", "Shipping tier", "add_shipping_info olayının shipping_tier parametresi.", "The shipping_tier parameter of the add_shipping_info event."), th("Olay sayısı", "Event count", "%s olay sayısı." % D_12[0], "Event count, %s." % D_12[1], True), th("Pay", "Share", "Toplam içindeki pay.", "Share of the total.", True)],
          [[x(a_, OD_EN.get(a_, a_)), cell(v), n(yzd(100 * v / kgt))] for a_, v in KG], "dar")))
_ns_o = next((v for a_, v in OD if a_ == "(not set)"), 0); _ns_k = next((v for a_, v in KG if a_ == "(not set)"), 0)
_kk = next((v for a_, v in OD if a_.startswith("Kredi")), 0)
INS_ODEME = insight("1 Eylül 2025 - 30 Eylül 2026'da ödeme adımına %s, teslimat adımına %s kez ulaşılmıştır. Ödeme türü belirtilen olayların %s'inde kredi ya da banka kartı seçilmiştir; EFT / havale ve iyzico birlikte %s'te kalmaktadır. **Ödeme olaylarının %s'inde ve teslimat olaylarının %s'inde tür bilgisi boştur (not set)**; teslimat türü ayrıca iki farklı adla (\"Kargo ile Teslimat\" ve \"standard-net\") kaydedilmektedir. Bu parametrelerin tutarlı gönderilmesi, ödeme ve teslimat tercihinin dönüşüme etkisinin ölçülmesini sağlayabilir."
                    % (bin(odt), bin(kgt), yzd(100 * _kk / (odt - _ns_o)), yzd(100 * (odt - _ns_o - _kk) / (odt - _ns_o)), yzd(100 * _ns_o / odt), yzd(100 * _ns_k / kgt)),
                    "In 1 September 2025 - 30 September 2026, the payment step was reached %s times and the shipping step %s times. In the events with a payment type, credit or debit card was chosen in %s; bank transfer and iyzico together stay at %s. **The type is empty (not set) in %s of payment events and %s of shipping events**; the shipping tier is also recorded under two different names (\"Kargo ile Teslimat\" and \"standard-net\"). Sending these parameters consistently can make it possible to measure the effect of payment and shipping choices on conversion."
                    % (f"{int(odt):,}", f"{int(kgt):,}", _pe(100 * _kk / (odt - _ns_o)), _pe(100 * (odt - _ns_o - _kk) / (odt - _ns_o)), _pe(100 * _ns_o / odt), _pe(100 * _ns_k / kgt)), "D45")

# ---------------------------------------------------------------- 5 · satın alma dışı talep olayları
OL = G["olay"]
_OLAY_EN = {"servisler_ve_satis_noktalari": "servisler_ve_satis_noktalari (services and sales points button)"}
_aylar_ol = sorted({m for d in OL.values() for m in d})
_AO = ["%s %s" % (AYA[int(m[5:]) - 1][0], m[:4]) for m in _aylar_ol]
_AOE = ["%s %s" % (AYA[int(m[5:]) - 1][1], m[:4]) for m in _aylar_ol]
T_OLAY = tablo([th("Olay", "Event", "GA4 olay adı; servisler ve satış noktaları düğmesine tıklamayı ölçer.", "GA4 event name; measures clicks on the services and sales points button.")] + [th(e, _AOE[i], "%s tıklama sayısı." % e, "Click count, %s." % _AOE[i], True) for i, e in enumerate(_AO)] + [th("Toplam", "Total", "Dönem toplamı.", "Period total.", True)],
               [[x(k_, _OLAY_EN.get(k_, k_))] + [cell(d.get(m, [0])[0] or 0) if m in d else n("-") for m in _aylar_ol] + [cell(sum(v[0] for v in d.values()))] for k_, d in OL.items()], "dar kompakt")
_ol_top = sum(v[0] for d in OL.values() for v in d.values())
INS_OLAY = insight("GA4'te satın alma dışındaki talep olaylarından yalnız servisler ve satış noktaları düğmesine tıklama izlenmektedir (1 Eyl 2025 - 30 Eyl 2026'da %s tıklama); Ocak - Nisan 2026 için veri bulunmamaktadır. **Banyo Asistanı'nın açılış, adım ve form gönderimi, WhatsApp ve telefon tıklaması GA4'te ayrı olay olarak görünmemektedir**; bu nedenle ürün + hizmet akışının kaç talep ürettiği ve bu taleplerin satışa dönüşümü ölçülememektedir (Bölüm [[b:set]], [[b:adimlar]])."
                   % bin(_ol_top),
                   "Among non-purchase request events, only clicks on the services and sales points button are tracked in GA4 (%s clicks in 1 Sep 2025 - 30 Sep 2026); no data is available for January - April 2026. **The Bathroom Assistant's opening, steps and form submission, WhatsApp and phone clicks do not appear as separate events in GA4**; therefore how many requests the product + service flow generates and how these requests convert to sales cannot be measured (Sections [[b:set]], [[b:adimlar]])."
                   % f"{int(_ol_top):,}", "D45")

# ---------------------------------------------------------------- 6 · blog ve koleksiyon sayfaları
BL, KL = G["blog"], G["koleksiyon"]
bv = sum(r[1] for r in BL); bu_ = sum(r[2] for r in BL); bk = sum(r[3] or 0 for r in BL)
rows_b = []
for p, v, us, ke in sorted(BL, key=lambda r: -r[1])[:15]:
    pp = p.split("?")[0].rstrip("/"); gc = _G12.sayfa(pp)[0]
    rows_b.append([u("https://www.vitra.com.tr" + pp + "/", pp.replace("/ilham-veren-fikirler", "") or "/ilham-veren-fikirler/"), cellk(v), cellk(gc) if gc else n("-"), n(("%.1f" % (v / gc)).replace(".", ",")) if gc else n("-")])
x("/ilham-veren-fikirler/", "/ilham-veren-fikirler/")
T_BLOG = tablo([th("Yazı", "Article", "Blog yazısının adresi (/ilham-veren-fikirler/ sonrası); bağlantı canlı sayfaya gider.", "The blog article's address (after /ilham-veren-fikirler/); the link opens the live page."),
                th("Görüntüleme", "Views", "%s sayfa görüntüleme (GA4)." % D_12[0], "Page views, %s (GA4)." % D_12[1], True),
                th("Organik click", "Organic clicks", "Search Console, %s organik click." % _G12.D12[0], "Search Console organic clicks, %s." % _G12.D12[1], True),
                th("Görüntüleme / click", "Views / click", "GA4 görüntülemesinin Search Console organik click'ine oranı; dönemler bir ay farklıdır, yön gösterir.", "GA4 views as a ratio of Search Console organic clicks; periods differ by one month, indicative.", True)], rows_b, "dar")
_OLU = {"/koleksiyonlar/"}   # 05.10.2026 kontrolünde 404 dönen eski adresler bağlantısız kalır
def _kol(p):
    p = p.split("?")[0]
    if p in _OLU: return x(p, p)
    return u("https://www.vitra.com.tr" + (p[3:] if p.startswith("/tr/") else p), p)   # eski /tr/ adresi yeni adrese yönlenir; bağlantı yeni adrese verilir
rows_kl = [[_kol(p), cellk(v)] for p, v, us, ke in sorted(KL, key=lambda r: -r[1])[:8]]
T_KOL = tablo([th("Koleksiyon ve katalog sayfası", "Collection and catalogue page", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
               th("Görüntüleme", "Views", "%s sayfa görüntüleme." % D_12[0], "Page views, %s." % D_12[1], True)], rows_kl, "dar")
INS_BLOG = insight("Blog yazıları (/ilham-veren-fikirler/) %s döneminde %s görüntüleme almıştır; en çok görüntülenen sayfalar blog ana sayfası ve montaj rehberi hub'ıdır. GA4 sayfa raporu blog yazısının satışa katkısını göstermemektedir: blogla başlayan oturumların Ocak - Eylül 2026 geliri %s'dir ve blog okuyan oturumların sonrasında ürün görüntüleme, sepete ekleme ve satın almaya geçişi ayrı bir oturum segmentiyle ölçülebilir. Koleksiyon listesi sayfası (/v-/koleksiyonlar) tek başına %s görüntüleme almıştır."
                   % (D_12[0], k(bv), tl(_bl6), k(KL[0][1])),
                   "Blog articles (/ilham-veren-fikirler/) received %s views in %s; the most viewed pages are the blog home page and the installation guide hub. The GA4 page report does not show a blog article's contribution to sales: sessions starting on the blog produced %s of revenue in January - September 2026, and how sessions that read the blog go on to view products, add to cart and purchase can be measured with a separate session segment. The collection list page (/v-/koleksiyonlar) alone received %s views."
                   % (k(bv).replace(",", "."), D_12[1], tl(_bl6), k(KL[0][1]).replace(",", ".")), "D45", "D2")

# ---------------------------------------------------------------- 7 · promosyon ve kupon
PR = [r for r in G["promosyon"] if r["gor"]]
prt = sum(r["gor"] for r in PR); prk = sum(r["tik"] for r in PR)
rows_p = []
for r in sorted([r for r in PR if r["ad"] != "(not set)"], key=lambda r: -r["gor"])[:15]:
    rows_p.append([x(r["ad"], r["ad"]), cellk(r["gor"]), cellk(r["tik"]), n(yzd(100 * r["tik"] / r["gor"], 1) if r["gor"] else "-")])
T_PROMO = tablo([th("Promosyon adı", "Promotion name", "GA4 item promotion name (promosyon alanının sitedeki metni); kendi yazımıyla verilmiştir.", "GA4 item promotion name (the promotion slot's text on the site); given in its own wording."),
                 th("Görüntülenme", "Views", "%s promosyonda görüntülenen ürün (Items viewed in promotion)." % D_12[0], "Items viewed in promotion, %s." % D_12[1], True),
                 th("Tıklama", "Clicks", "Promosyonda tıklanan ürün (Items clicked in promotion).", "Items clicked in promotion.", True),
                 th("Tıklama oranı", "Click-through rate", "Tıklama / görüntülenme.", "Clicks / views.", True)], rows_p, "dar")
_ku = next((r for r in G["promosyon"] if r.get("kupon") and r["kupon"] not in ("(not set)",) and r["satin"]), None)
_ns = next((r for r in G["promosyon"] if r["ad"] == "(not set)" and r["kupon"] == "(not set)"), {"satin": 0, "gelir": 0})
_ctr = sorted([r for r in PR if r["ad"] != "(not set)" and r["gor"] >= 10000], key=lambda r: -r["tik"] / r["gor"])[:3]
def _pad(r): return _re.sub(r"^(Slider|Anasayfa) - ", "", r["ad"]).rstrip(".")
_CTR_TR = ", ".join("\"%s\" (%s)" % (_pad(r), yzd(100 * r["tik"] / r["gor"])) for r in _ctr)
_CTR_EN = ", ".join("\"%s\" (%s)" % (_pad(r), _pe(100 * r["tik"] / r["gor"])) for r in _ctr)
INS_PROMO = insight("Sitedeki promosyon alanları %s döneminde %s ürün görüntülenmesi ve %s tıklama almıştır; 10 bin ve üzeri görüntülenme alan promosyonlarda en yüksek tıklama oranı %s ile gerçekleşmiştir. **Promosyon adı taşıyan alanların hiçbirine sepete ekleme ya da satın alma atanmamaktadır**: satın alınan ürünlerin tamamı promosyon adı boş (not set) görünmektedir; kupon kodu yalnız %s'de kayıtlıdır (%s ürün, %s). Promosyon tıklamasının satın almaya taşınması, kampanyaların gelire etkisinin ölçülmesini sağlayabilir."
                    % (D_12[0], k(prt), k(prk), _CTR_TR, _ku["kupon"] if _ku else "-", bin(_ku["satin"]) if _ku else "-", tl(_ku["gelir"]) if _ku else "-"),
                    "The promotion slots on the site received %s item views and %s clicks in %s; among promotions with 10 thousand views or more, the highest click-through rates are %s. **No add-to-cart or purchase is attributed to any slot with a promotion name**: all purchased items appear with an empty (not set) promotion name; a coupon code is recorded only for %s (%s items, %s). Carrying the promotion click through to the purchase can make it possible to measure campaigns' effect on revenue."
                    % (k(prt).replace(",", "."), k(prk).replace(",", "."), D_12[1], _CTR_EN, _ku["kupon"] if _ku else "-", f"{int(_ku['satin']):,}" if _ku else "-", tl(_ku["gelir"]) if _ku else "-"), "D45")

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
%s
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
%s
""" % (
 x("Google Analytics 4 (GA4) verisi, vitra.com.tr'nin oturum, satın alma ve gelir performansını kanal, site içi arama, ödeme adımı, içerik ve promosyon kırılımında göstermektedir. Veri VitrA ekibinin GA4 dışa aktarımından alınmıştır (05.10.2026); tabloların dönemleri başlık ve sütun açıklamalarında verilmiştir. Aralık 2025'te www.vitra.com.tr trafiği aynı GA4 mülküne katıldığı için oturum ve oturum başına dönüşüm oranı Aralık öncesi ve sonrası arasında kıyaslanmaz; satın alma ve gelir iki dönemde de kıyaslanabilir.",
   "Google Analytics 4 (GA4) data shows vitra.com.tr's sessions, purchases and revenue by channel, site search, payment step, content and promotion. The data comes from the VitrA team's GA4 export (05.10.2026); each table's period is given in its heading and column descriptions. As www.vitra.com.tr traffic joined the same GA4 property in December 2025, sessions and the conversion rate per session are not compared before and after December; purchases and revenue are comparable in both periods."),
 kpi_kart(tl(r26), "E-ticaret geliri · Oca-Eyl 2026; Oca-Eyl 2025'e göre %s" % _isr(_deg(r25, r26)), "E-commerce revenue · Jan-Sep 2026; %s against Jan-Sep 2025" % _isr_en(_deg(r25, r26))),
 kpi_kart(bin(p26), "E-ticaret satın alma · Oca-Eyl 2026; Oca-Eyl 2025'e göre %s" % _isr(_deg(p25, p26)), "E-commerce purchases · Jan-Sep 2026; %s against Jan-Sep 2025" % _isr_en(_deg(p25, p26))),
 kpi_kart(tl(aov26), "Ortalama sipariş tutarı · Oca-Eyl 2026; 2025'te %s" % tl(aov25), "Average order value · Jan-Sep 2026; %s in 2025" % tl(aov25)),
 kpi_kart(yzd(100 * _o(_os_, 2026, "gelir") / _tg26), "Organik aramanın gelir payı · Oca-Eyl 2026; 2025'te %s" % yzd(100 * _o(_os_, 2025, "gelir") / _tg25), "Organic search share of revenue · Jan-Sep 2026; %s in 2025" % _pe(100 * _o(_os_, 2025, "gelir") / _tg25)),
 x("Aylık genel görünüm: gelir, satın alma ve oturum", "Monthly overview: revenue, purchases and sessions"), G_AYLIK, T_AYLIK, INS_AYLIK,
 x("Kanal performansı: oturum, satın alma ve gelir", "Channel performance: sessions, purchases and revenue"), G_KANAL, T_KANAL, G_KAY, INS_KANAL, T_KAYNAK,
 x("Giriş sayfası (landing page) türüne göre gelir", "Revenue by landing page type"), T_LP, G_LP, T_LPS, INS_LP,
 x("Site içi arama terimleri", "Site search terms"), T_ARAMA, T_SINIF, INS_ARAMA,
 x("Ödeme ve teslimat adımı", "Payment and shipping step"), T_ODEME, INS_ODEME,
 x("Satın alma dışı talep olayları", "Non-purchase request events"), T_OLAY, INS_OLAY,
 x("Blog ve koleksiyon sayfaları: görüntüleme", "Blog and collection pages: views"), T_BLOG, T_KOL, INS_BLOG,
 x("Promosyon ve kupon", "Promotions and coupons"), T_PROMO, INS_PROMO,
 kaynak("Google Analytics 4, VitrA ekibi dışa aktarımı (05.10.2026): genel bakış Oca 2025 - Eyl 2026, kanal ve kaynak / ortam 2025 ve 1 Oca - 5 Eki 2026; site içi arama 1 May - 30 Eyl 2026, ödeme, teslimat, olay, sayfa ve promosyon 1 Eyl 2025 - 30 Eyl 2026 · Google Search Console, 1 Eki 2025 - 30 Eyl 2026",
        "Google Analytics 4, VitrA team export (05.10.2026): overview Jan 2025 - Sep 2026, channel and source / medium 2025 and 1 Jan - 5 Oct 2026, site search 1 May - 30 Sep 2026; payment, shipping, events, pages and promotions 1 Sep 2025 - 30 Sep 2026 · Google Search Console, 1 Oct 2025 - 30 Sep 2026", "D45", "D2"),
)
