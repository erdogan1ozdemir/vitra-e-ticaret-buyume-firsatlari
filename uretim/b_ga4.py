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
def _p1k(v): return ("%.2f" % v).replace(".", ",")
def _isr(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + "%" + ("%.1f" % abs(v)).replace(".", ",")
def _isr_en(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + ("%.1f" % abs(v)) + "%"
r25, r26 = _top(2025, "gelir"), _top(2026, "gelir"); p25, p26 = _top(2025, "satin"), _top(2026, "satin"); o25, o26 = _top(2025, "oturum"), _top(2026, "oturum")
aov25, aov26 = r25 / p25, r26 / p26
D_GEN = ("Oca 2025 - Eyl 2026", "Jan 2025 - Sep 2026"); D_OE = ("Oca-Eyl 2025 ve 2026", "Jan-Sep 2025 and 2026")
D_12 = ("1 Eki 2025 - 30 Eyl 2026", "1 Oct 2025 - 30 Sep 2026"); D_AR = ("1 May - 30 Eyl 2026", "1 May - 30 Sep 2026")

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
LAD = {"siparis": ("Sipariş onay sayfası", "Order confirmation page"), "odeme": ("Sepet, giriş ve ödeme adımları", "Cart, sign-in and checkout steps"), "anasayfa": ("Ana sayfa", "Home page"), "urun": ("Ürün sayfaları", "Product pages"),
       "kategori": ("Kategori sayfaları", "Category pages"), "koleksiyon": ("Koleksiyon, seri ve kampanya sayfaları", "Collection, series and campaign pages"),
       "arama": ("Site içi arama sonuçları", "Site search results"), "destek": ("Servis, destek ve satış noktaları", "Service, support and sales points"),
       "kurumsal": ("Kurumsal, proje ve katalog", "Corporate, projects and catalogues"), "blog": ("Blog (İlham Veren Fikirler)", "Blog (İlham Veren Fikirler)"), "diger": ("Diğer ve (not set)", "Other and (not set)")}
def _lt(t, y, i): return (LT.get(t, {}).get(str(y)) or [0, 0, 0, 0])[i]
_lg25 = sum(_lt(t, 2025, 1) for t in LT); _lg26 = sum(_lt(t, 2026, 1) for t in LT)
_LSIRA = sorted(LT, key=lambda t: (t == "diger", -_lt(t, 2026, 1)))
rows_lp = []
for t in _LSIRA:
    g5, g6, o6 = _lt(t, 2025, 1), _lt(t, 2026, 1), _lt(t, 2026, 0)
    rows_lp.append([x(*LAD[t]), n(yzd(100 * o6 / LS["2026"], 2 if 100 * o6 / LS["2026"] < 0.1 else 1)), n(tl(g5) if g5 >= 1000 else "-"), n(tl(g6) if g6 >= 1000 else "-"), n(yz(_deg(g5, g6)) if g5 >= 50000 else "-"),
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
                {"ad": x("Sipariş onay sayfasında başlayan oturumların geliri", "Revenue of sessions starting on the order confirmation page"), "renk": "#E85F36", "deger": [LO[m][2] for m in _LOA], "tip": "cubuk", "ortu": True, "bicim": _tlk}],
               cap=x("Aylık gelir (gri çubuk) ve içinde doğrudan sipariş onay sayfasında başlayan oturumların geliri (turuncu); çubuk üstündeki oran bu oturumların gelir payıdır · Oca 2025 - Eyl 2026",
                     "Monthly revenue (grey bar) with the revenue of sessions starting directly on the order confirmation page inside it (orange); the figure above the bar is these sessions' share of revenue · Jan 2025 - Sep 2026"),
               ust_etiket=[x(yzd(100 * LO[m][2] / LO[m][1]), _pe(100 * LO[m][2] / LO[m][1])) for m in _LOA])
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
_LPG = [r for r in LP26 if r[1] not in ("odeme", "siparis")][:15]
_LPO = sorted([r for r in LP26 if r[1] not in ("odeme", "siparis") and r[0] != "(not set)"], key=lambda r: -r[2])[:15]
T_LPS = sekmeler([("Gelire göre ilk 15", "Top 15 by revenue", tablo(_LPH, [_lprow(r) for r in _LPG], "dar xl")),
                  ("Oturuma göre ilk 15", "Top 15 by sessions", tablo(_LPH, [_lprow(r) for r in _LPO], "dar xl"))], "ttabs")
# sepet ve giriş sayfasında yeniden başlayan oturumlarda önceki sayfa (session_start olayının sayfa yönlendireni, Oca - Eyl 2026)
OY = G["oturum_yenilenme"]; _oyi, _oyd = OY["site_ici"], OY["dis"]; _oyt = sum(_oyi.values()) + sum(_oyd.values())
OYAD = [("urun", "Ürün sayfası", "Product page"), ("cart", "Sepet (aynı sayfa yeniden)", "Cart (same page again)"), ("kategori", "Kategori sayfası", "Category page"), ("anasayfa", "Ana sayfa", "Home page"),
        ("hesap", "Hesabım", "My account"), ("login", "Giriş", "Sign-in"), ("arama", "Site içi arama", "Site search"), ("checkout", "Ödeme adımı", "Checkout step"), ("diger", "Diğer site sayfaları", "Other site pages")]
OYDAD = [("(boş)", "Yönlendiren yok", "No referrer"), ("Google", "Google", "Google"), ("diğer dış site", "Diğer dış siteler", "Other external sites")]
rows_oy = [[x("vitra.com.tr · " + b_, "vitra.com.tr · " + c_), cell(_oyi.get(a_, 0)), n(yzd(100 * _oyi.get(a_, 0) / _oyt))] for a_, b_, c_ in OYAD] + \
          [[x("Dış kaynak · " + b_, "External · " + c_), cell(_oyd.get(a_, 0)), n(yzd(100 * _oyd.get(a_, 0) / _oyt))] for a_, b_, c_ in OYDAD]
T_OY = tablo([th("Önceki sayfa", "Previous page", "Sepet, giriş ve hesap sayfasında yeni oturum başladığında (session_start) sayfa yönlendireni (Page referrer); vitra.com.tr satırları oturumun site içinde gezinirken yenilendiğini gösterir.", "The page referrer when a new session starts (session_start) on the cart, sign-in and account pages; vitra.com.tr rows show the session restarting while browsing within the site."),
              th("Yeni oturum", "New sessions", "session_start olay sayısı, 1 Oca - 30 Eyl 2026 (aylık dışa aktarımların toplamı).", "session_start event count, 1 Jan - 30 Sep 2026 (sum of monthly exports).", True),
              th("Pay", "Share", "Toplam içindeki pay.", "Share of the total.", True)], rows_oy, "dar")
# sipariş onay sayfasında yeni oturumun önceki sayfası (Tablo C) ve satın almanın kaynak / ortamı (Tablo D) · 1 Eki 2025 - 30 Eyl 2026
_SR = {}
for _v in G["siparis_ref"].values():
    for _k, _c in _v.items(): _SR[_k] = _SR.get(_k, 0) + _c
_srt = sum(_SR.values()); _sri = sum(v for k, v in _SR.items() if k.startswith("iyzico"))
SRAD = [("iyzico_api", "iyzico · api.iyzipay.com (ödeme sonucu dönüşü)", "iyzico · api.iyzipay.com (payment result return)"),
        ("iyzico_cpp", "iyzico · cpp.iyzipay.com (ödeme formu)", "iyzico · cpp.iyzipay.com (payment form)"),
        ("iyzico_ode", "iyzico · ode.iyzico.com", "iyzico · ode.iyzico.com"),
        ("iyzico_3ds", "iyzico · 3D Secure doğrulama dönüşü", "iyzico · 3D Secure verification return"),
        ("siparis", "vitra.com.tr · aynı sipariş onay sayfası (yeniden yükleme)", "vitra.com.tr · same order confirmation page (reload)"),
        ("giris", "vitra.com.tr · ödeme adımında üye girişi", "vitra.com.tr · sign-in during checkout"),
        ("odeme", "vitra.com.tr · ödeme yöntemi sayfası", "vitra.com.tr · payment method page"),
        ("bos", "Yönlendiren yok", "No referrer")]
assert set(_SR) <= {a_ for a_, _, _ in SRAD}, ("sipariş onay yönlendiren türü tanımsız", set(_SR))
T_SR = tablo([th("Sipariş onayında önceki sayfa", "Previous page on order confirmation", "Sipariş onay sayfasında yeni oturum başladığında (session_start) sayfa yönlendireni (Page referrer); iyzico satırları kullanıcının ödeme sayfasından siteye dönüşüdür.", "The page referrer when a new session starts (session_start) on the order confirmation page; the iyzico rows are the user's return to the site from the payment page."),
              th("Yeni oturum payı", "Share of new sessions", "%s · %s session_start olayı içindeki pay (aylık keşif dışa aktarımları; örneklenen aylarda GA4'ün ölçeklediği değerler, paylar etkilenmez)." % (D_12[0], bin(_srt)), "%s · share of %s session_start events (monthly exploration exports; in sampled months the values are scaled by GA4, shares are not affected)." % (D_12[1], bin(_srt)), True)],
             [[x(b_, c_), n(yzd(100 * _SR.get(a_, 0) / _srt))] for a_, b_, c_ in SRAD if _SR.get(a_)], "dar")
SK = G["siparis_kaynak"]; SKN = G["siparis_kaynak_n"]
_skt = {g: sum(v.values()) for g, v in SK.items()}; _skT = sum(_skt.values())
def _skp(g, k): return 100 * SK[g].get(k, 0) / _skt[g]
def _skh(k): return 100 * (SK["yeniden"].get(k, 0) + SK["ayni"].get(k, 0)) / _skT
_KN = {}
for _c, _d in G["kanal"].items():
    for _m, _v in _d.items():
        if "2025-10" <= _m <= "2026-09": _KN[_c] = _KN.get(_c, 0) + (_v.get("gelir") or 0)
_knt = sum(_KN.values())
_KNG = {"direct": 100 * _KN.get("Direct", 0) / _knt, "organik": 100 * _KN.get("Organic Search", 0) / _knt, "ucretli": 100 * _KN.get("Paid Search", 0) / _knt}
_KNG["diger"] = 100 - sum(_KNG.values())
SKAD = [("direct", "(direct) / (none)", "(direct) / (none)"), ("organik", "Organik arama", "Organic search"), ("ucretli", "Ücretli arama", "Paid search"), ("diger", "Diğer (sosyal, yönlendiren, e-posta, not set)", "Other (social, referral, email, not set)")]
rows_sk = [[x(b_, c_), n(yzd(_skp("yeniden", a_))), n(yzd(_skp("ayni", a_))), n(yzd(_skh(a_))), n(yzd(_KNG[a_]))] for a_, b_, c_ in SKAD]
rows_sk.append([x("Sipariş sayısı", "Number of orders"), cell(SKN["yeniden"]), cell(SKN["ayni"]), cell(SKN["yeniden"] + SKN["ayni"]), n("-")])
rows_sk.append([x("Satın alma gelirindeki pay", "Share of purchase revenue"), n(yzd(100 * _skt["yeniden"] / _skT)), n(yzd(100 * _skt["ayni"] / _skT)), n(yzd(100.0)), n("-")])
T_SK = tablo([th("Kaynak grubu", "Source group", "Satın alma gelirinin kaynak grubu; organik ve ücretli arama Google, Bing ve Yandex'i kapsar.", "Source group of purchase revenue; organic and paid search cover Google, Bing and Yandex."),
              th("Oturumu sipariş onay sayfasında yeniden başlayan siparişler", "Orders whose session restarted on the order confirmation page", "Sipariş onay sayfasında session_start olayı görülen siparişler; satın alma olayının kaynak / ortamı (Source / medium, GA4 atama modeli) içindeki gelir payı, %s." % D_12[0], "Orders with a session_start event on the order confirmation page; revenue share within the purchase event's source / medium (Source / medium, GA4 attribution model), %s." % D_12[1], True),
              th("Oturumu yenilenmeyen siparişler", "Orders whose session did not restart", "Sipariş onay sayfasında yeni oturum başlamayan siparişler; aynı kırılım.", "Orders with no new session on the order confirmation page; same breakdown.", True),
              th("Tüm siparişler", "All orders", "İki grubun toplamı; satın alma olayının kaynak / ortamı içindeki gelir payı.", "Both groups together; revenue share within the purchase event's source / medium.", True),
              th("Oturum kanalı tablosu", "Session channel table", "Aynı dönemde oturum kanal grubuna (Session default channel group) göre gelir payı: Direct, Organic Search, Paid Search ve diğer kanallar.", "Revenue share by session channel group (Session default channel group) in the same period: Direct, Organic Search, Paid Search and other channels.", True)], rows_sk, "dar")
_sy = 100 * _skt["yeniden"] / _skT
INS_SO = insight("%s döneminde sipariş onay sayfasında başlayan yeni oturumların %s'inde önceki sayfa iyzico'nun ödeme sayfalarıdır (api.iyzipay.com %s): kullanıcı ödeme ve 3D Secure adımından siteye döndüğünde oturum yeniden başlamaktadır. iyzico alan adları istenmeyen yönlendirmeler (unwanted referrals) listesinde olduğundan bu oturumlar iyzico'ya yönlendiren olarak yazılmamakta, ancak oturum yine de yenilenmektedir; bu durum sepete geçişte görülen çerez yenilenmesiyle aynı yöndedir. Oturumu bu şekilde yeniden başlayan %s sipariş satın alma gelirinin %s'ini taşımaktadır. Satın alma olayının kaynak / ortam kırılımında bu siparişlerin gelirinin %s'i (direct) olarak görünürken, oturumu yenilenmeyen siparişlerde direct payı %s, organik ve ücretli arama toplamı %s'dir. Tüm siparişlerde direct payı %s'e çıkmakta, aynı dönemde oturum kanalı tablosunda Direct'in gelir payı %s'de kalmaktadır. **Kanal kırılımı oturum düzeyinde korunurken, satın almanın kaynağa atanmasında siparişlerin yaklaşık yarısı kaynağını kaybetmektedir**; atama modeline dayanan raporlarda ve bu dönüşümü kullanan reklam hesaplarında organik ve ücretli aramanın katkısı olduğundan düşük görünebilir. iyzico dönüşünde GA4 çerezlerinin ve oturum kimliğinin korunup korunmadığının geliştirme ekibiyle kontrol edilmesi önerilir."
                 % (D_12[0], yzd(100 * _sri / _srt), yzd(100 * _SR.get("iyzico_api", 0) / _srt), bin(SKN["yeniden"]), yzd(_sy), yzd(_skp("yeniden", "direct")), yzd(_skp("ayni", "direct")), yzd(_skp("ayni", "organik") + _skp("ayni", "ucretli")), yzd(_skh("direct")), yzd(_KNG["direct"])),
                 "In %s, the previous page in %s of new sessions starting on the order confirmation page is one of iyzico's payment pages (api.iyzipay.com %s): the session restarts when the user returns to the site from the payment and 3D Secure step. As the iyzico domains are on the unwanted referrals list, these sessions are not recorded with iyzico as the referrer, yet the session still restarts; this points the same way as the cookie renewal seen when moving to the cart. The %s orders whose session restarts this way carry %s of purchase revenue. In the purchase event's source / medium breakdown, %s of these orders' revenue appears as (direct), while for orders whose session did not restart the direct share is %s and organic and paid search together account for %s. Across all orders the direct share rises to %s, whereas in the session channel table for the same period Direct's share of revenue stays at %s. **While the channel split is preserved at session level, about half of the orders lose their source when the purchase is attributed**; in reports based on the attribution model, and in ad accounts using this conversion, the contribution of organic and paid search can appear lower than it is. Checking with the development team whether the GA4 cookies and the session ID are kept on the return from iyzico is recommended."
                 % (D_12[1], yzd(100 * _sri / _srt), yzd(100 * _SR.get("iyzico_api", 0) / _srt), bin(SKN["yeniden"]), yzd(_sy), yzd(_skp("yeniden", "direct")), yzd(_skp("ayni", "direct")), yzd(_skp("ayni", "organik") + _skp("ayni", "ucretli")), yzd(_skh("direct")), yzd(_KNG["direct"])), "D45")
_qf = next(r for r in LP26 if r[0] == "/v/vitra-quantumflush-i")
_bl6 = _lt("blog", 2026, 1)
_sp26, _sp25 = 100 * _lt("siparis", 2026, 1) / _lg26, 100 * _lt("siparis", 2025, 1) / _lg25
_sn26, _sn25 = G["lp_siparis_no"]["2026"], G["lp_siparis_no"]["2025"]
_oyic = 100 * sum(_oyi.values()) / _oyt; _oyur = 100 * _oyi.get("urun", 0) / _oyt
_KY = G["odeme_giris_kaynak"]; _kyg = 100 * (_KY.get("google / organic", 0) + _KY.get("google / cpc", 0)) / sum(_KY.values())
INS_LP = insight("Ocak - Eylül 2026 gelirinin %s'i doğrudan sipariş onay sayfasında başlayan oturumlarda görünmektedir (2025'in aynı aylarında %s); giriş sayfası sipariş onay olan %s farklı sipariş, aynı dönemdeki %s satın almanın %s'ine karşılık gelmektedir. **Satın alma tamamlandığında kullanıcı siteye yeni bir oturumla girmiş sayılmakta ve satın almayı başlatan giriş sayfası bu oturumda görünmemektedir**; sepet, giriş ve ödeme sayfalarında başlayan oturumlar da gelirin %s'ini taşımaktadır. Sepet, giriş ve hesap sayfalarında yeniden başlayan oturumların %s'inde önceki sayfa vitra.com.tr'nin kendi sayfasıdır (%s'inde ürün sayfası): oturum dış bir siteden dönüşte değil, site içinde gezinirken yenilenmektedir. Bu oturumların gelirinin %s'i Google organik ve ücretli aramaya atandığı için oturum düzeyindeki kanal kırılımı büyük ölçüde korunmakta, kaybolan bilgi giriş sayfası ve içeriğin katkısı olmaktadır. Kalan gelirde ana sayfa (%s), ürün sayfaları (%s) ve kategori sayfaları (%s) öne çıkmaktadır; QuantumFlush tanıtım sayfası giriş sayfası oturumlarının %s'ini almış, gelirin %s'ini getirmiştir. 06.10.2026'daki tarayıcı kontrolünde ürün sayfasından sepete geçerken GA4 oturum çerezindeki oturum kimliğinin değiştiği görülmüştür: **oturum sepet sayfasında yeniden başlatılmaktadır**; aynı kontrolde kullanıcı çerezi (_ga) de değişmekte, bu nedenle yeni ve geri dönen kullanıcı ile ilk kez satın alan kırılımı güvenilir biçimde okunamamaktadır. Sepet ve ödeme sayfalarındaki GA4 etiket ve çerez ayarlarının diğer sayfalarla aynı hale getirilmesi, giriş sayfası ve içerik bazında gelirin eksiksiz okunmasını sağlayabilir."
                 % (yzd(_sp26), yzd(_sp25), bin(_sn26), bin(p26), yzd(100 * _sn26 / p26), yzd(100 * _lt("odeme", 2026, 1) / _lg26), yzd(_oyic), yzd(_oyur), yzd(_kyg),
                    yzd(100 * _lt("anasayfa", 2026, 1) / _lg26), yzd(100 * _lt("urun", 2026, 1) / _lg26), yzd(100 * _lt("kategori", 2026, 1) / _lg26), yzd(100 * _qf[2] / LS["2026"]), yzd(100 * _qf[3] / _lg26)),
                 "%s of January - September 2026 revenue appears in sessions starting directly on the order confirmation page (%s in the same months of 2025); the %s distinct orders whose landing page is the order confirmation correspond to %s of the %s purchases in the same period. **When the purchase is completed, the user is counted as entering the site with a new session, and the landing page that started the purchase does not appear in that session**; sessions starting on cart, sign-in and checkout pages also carry %s of revenue. In %s of the sessions restarting on the cart, sign-in and account pages the previous page is a vitra.com.tr page (a product page in %s): the session restarts while browsing within the site, not on return from an external site. As %s of these sessions' revenue is attributed to Google organic and paid search, the session-level channel split is largely preserved; what is lost is the contribution of the landing page and the content. In the remaining revenue, the home page (%s), product pages (%s) and category pages (%s) stand out; the QuantumFlush promotion page took %s of landing page sessions and brought %s of revenue. In a browser check on 06.10.2026, the session ID in the GA4 session cookie changed when moving from a product page to the cart: **the session is restarted on the cart page**; in the same check the user cookie (_ga) also changes, so the new vs returning user and first-time purchaser splits cannot be read reliably. Aligning the GA4 tag and cookie settings on the cart and checkout pages with the other pages can make it possible to read revenue by landing page and content in full."
                 % (yzd(_sp26), yzd(_sp25), bin(_sn26), yzd(100 * _sn26 / p26), bin(p26), yzd(100 * _lt("odeme", 2026, 1) / _lg26), yzd(_oyic), yzd(_oyur), yzd(_kyg),
                    yzd(100 * _lt("anasayfa", 2026, 1) / _lg26), yzd(100 * _lt("urun", 2026, 1) / _lg26), yzd(100 * _lt("kategori", 2026, 1) / _lg26), yzd(100 * _qf[2] / LS["2026"]), yzd(100 * _qf[3] / _lg26)), "D45")

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
INS_ODEME = insight("1 Ekim 2025 - 30 Eylül 2026'da ödeme adımına %s, teslimat adımına %s kez ulaşılmıştır. Ödeme türü belirtilen olayların %s'inde kredi ya da banka kartı seçilmiştir; EFT / havale ve iyzico birlikte %s'te kalmaktadır. **Ödeme olaylarının %s'inde ve teslimat olaylarının %s'inde tür bilgisi boştur (not set)**; teslimat türü ayrıca iki farklı adla (\"Kargo ile Teslimat\" ve \"standard-net\") kaydedilmektedir. Bu parametrelerin tutarlı gönderilmesi, ödeme ve teslimat tercihinin dönüşüme etkisinin ölçülmesini sağlayabilir."
                    % (bin(odt), bin(kgt), yzd(100 * _kk / (odt - _ns_o)), yzd(100 * (odt - _ns_o - _kk) / (odt - _ns_o)), yzd(100 * _ns_o / odt), yzd(100 * _ns_k / kgt)),
                    "In 1 October 2025 - 30 September 2026, the payment step was reached %s times and the shipping step %s times. In the events with a payment type, credit or debit card was chosen in %s; bank transfer and iyzico together stay at %s. **The type is empty (not set) in %s of payment events and %s of shipping events**; the shipping tier is also recorded under two different names (\"Kargo ile Teslimat\" and \"standard-net\"). Sending these parameters consistently can make it possible to measure the effect of payment and shipping choices on conversion."
                    % (f"{int(odt):,}", f"{int(kgt):,}", _pe(100 * _kk / (odt - _ns_o)), _pe(100 * (odt - _ns_o - _kk) / (odt - _ns_o)), _pe(100 * _ns_o / odt), _pe(100 * _ns_k / kgt)), "D45")

# ---------------------------------------------------------------- 5 · satın alma dışı talep olayları
OL = {k_: {m: v for m, v in d.items() if "2025-10" <= m <= "2026-09"} for k_, d in G["olay"].items()}   # son 12 ay: 1 Eki 2025 - 30 Eyl 2026
_OLAY_EN = {"servisler_ve_satis_noktalari": "servisler_ve_satis_noktalari (services and sales points button)"}
_aylar_ol = sorted({m for d in OL.values() for m in d})
_AO = ["%s %s" % (AYA[int(m[5:]) - 1][0], m[:4]) for m in _aylar_ol]
_AOE = ["%s %s" % (AYA[int(m[5:]) - 1][1], m[:4]) for m in _aylar_ol]
T_OLAY = tablo([th("Olay", "Event", "GA4 olay adı; servisler ve satış noktaları düğmesine tıklamayı ölçer.", "GA4 event name; measures clicks on the services and sales points button.")] + [th(e, _AOE[i], "%s tıklama sayısı." % e, "Click count, %s." % _AOE[i], True) for i, e in enumerate(_AO)] + [th("Toplam", "Total", "Dönem toplamı.", "Period total.", True)],
               [[x(k_, _OLAY_EN.get(k_, k_))] + [cell(d.get(m, [0])[0] or 0) if m in d else n("-") for m in _aylar_ol] + [cell(sum(v[0] for v in d.values()))] for k_, d in OL.items()], "dar kompakt")
_ol_top = sum(v[0] for d in OL.values() for v in d.values())
INS_OLAY = insight("GA4'te satın alma dışındaki talep olaylarından yalnız servisler ve satış noktaları düğmesine tıklama izlenmektedir (1 Eki 2025 - 30 Eyl 2026'da %s tıklama); Ocak - Nisan 2026 için veri bulunmamaktadır. **Banyo Asistanı'nın açılış, adım ve form gönderimi, WhatsApp ve telefon tıklaması GA4'te ayrı olay olarak görünmemektedir**; bu nedenle ürün + hizmet akışının kaç talep ürettiği ve bu taleplerin satışa dönüşümü ölçülememektedir (Bölüm [[b:set]], [[b:adimlar]])."
                   % bin(_ol_top),
                   "Among non-purchase request events, only clicks on the services and sales points button are tracked in GA4 (%s clicks in 1 Oct 2025 - 30 Sep 2026); no data is available for January - April 2026. **The Bathroom Assistant's opening, steps and form submission, WhatsApp and phone clicks do not appear as separate events in GA4**; therefore how many requests the product + service flow generates and how these requests convert to sales cannot be measured (Sections [[b:set]], [[b:adimlar]])."
                   % f"{int(_ol_top):,}", "D45")

# ---------------------------------------------------------------- 6 · blog ve koleksiyon sayfaları
BL, KL = G["blog"], G["koleksiyon"]
# Search Console blog click'i, GA4'teki www ölçüm dönemiyle aynı pencere (1 Ara 2025 - 30 Eyl 2026)
_SA = _json.load(open(_os.path.join(veri.V, "ham", "gsc2", "sayfa_aylik.json"), encoding="utf-8"))
_GSC_ARA = {}
for _m, _rows in _SA.items():
    if "2025-12" <= _m <= "2026-09":
        for _r in _rows:
            _k = _G12.yol(_r["keys"][0]); _GSC_ARA[_k] = _GSC_ARA.get(_k, 0) + _r["clicks"]
BO = G["blog_olay"]   # blog sayfalarında olay sayıları (keşif, 1 Eyl 2025 - 30 Eyl 2026)
bv = sum(r[1] for r in BL); bu_ = sum(r[2] for r in BL); bk = sum(r[3] or 0 for r in BL)
rows_b = []
for p, v, us, ke in sorted(BL, key=lambda r: -r[1])[:15]:
    pp = p.split("?")[0].rstrip("/"); gc = _GSC_ARA.get(pp.lower(), 0)
    rows_b.append([u("https://www.vitra.com.tr" + pp + "/", pp.replace("/ilham-veren-fikirler", "") or "/ilham-veren-fikirler/"), cellk(v), cellk(gc) if gc else n("-"), n(("%.1f" % (v / gc)).replace(".", ",")) if gc else n("-")])
x("/ilham-veren-fikirler/", "/ilham-veren-fikirler/")
T_BLOG = tablo([th("Yazı", "Article", "Blog yazısının adresi (/ilham-veren-fikirler/ sonrası); bağlantı canlı sayfaya gider.", "The blog article's address (after /ilham-veren-fikirler/); the link opens the live page."),
                th("Görüntüleme", "Views", "GA4 sayfa görüntüleme; www.vitra.com.tr sayfaları bu mülkte Aralık 2025'ten itibaren ölçüldüğü için değer 1 Ara 2025 - 30 Eyl 2026 dönemini kapsar.", "GA4 page views; as www.vitra.com.tr pages are measured in this property from December 2025, the value covers 1 Dec 2025 - 30 Sep 2026.", True),
                th("Organik click", "Organic clicks", "Search Console organik click, 1 Ara 2025 - 30 Eyl 2026 (GA4 görüntülemesiyle aynı dönem).", "Search Console organic clicks, 1 Dec 2025 - 30 Sep 2026 (same period as the GA4 views).", True),
                th("Görüntüleme / click", "Views / click", "GA4 görüntülemesinin Search Console organik click'ine oranı, 1 Ara 2025 - 30 Eyl 2026.", "GA4 views as a ratio of Search Console organic clicks; periods differ by one month, indicative.", True)], rows_b, "dar")
_OLU = {"/koleksiyonlar/"}   # 05.10.2026 kontrolünde 404 dönen eski adresler bağlantısız kalır
def _kol(p):
    p = p.split("?")[0]
    if p in _OLU: return x(p, p)
    return u("https://www.vitra.com.tr" + (p[3:] if p.startswith("/tr/") else p), p)   # eski /tr/ adresi yeni adrese yönlenir; bağlantı yeni adrese verilir
rows_kl = [[_kol(p), cellk(v)] for p, v, us, ke in sorted(KL, key=lambda r: -r[1])[:8]]
T_KOL = tablo([th("Koleksiyon ve katalog sayfası", "Collection and catalogue page", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
               th("Görüntüleme", "Views", "GA4 sayfa görüntüleme; www.vitra.com.tr sayfaları Aralık 2025'ten itibaren ölçüldüğü için 1 Ara 2025 - 30 Eyl 2026.", "GA4 page views; as www.vitra.com.tr pages are measured from December 2025, 1 Dec 2025 - 30 Sep 2026.", True)], rows_kl, "dar")
# ---------------------------------------------------------------- 11 · içerikten ürüne: blog oturumları
IU = G["icerik_urun"]
def _iu(seg, e): return sum(d[seg].get(e, 0) for d in IU.values())
IUAD = [("page_view", "Sayfa görüntüleme", "Page view"), ("view_item", "Ürün görüntüleme", "Product view"), ("add_to_cart", "Sepete ekleme", "Add to cart"), ("begin_checkout", "Ödemeye başlama", "Begin checkout"), ("purchase", "Satın alma", "Purchase")]
def _bin1k(seg, e): return 1000 * _iu(seg, e) / _iu(seg, "page_view")
rows_iu = [[x("%s (%s)" % (b_, a_), "%s (%s)" % (c_, a_)), cellk(_iu("blog", a_)), cellk(_iu("diger", a_)), n(yzd(100 * _iu("blog", a_) / (_iu("blog", a_) + _iu("diger", a_)))),
            n(x(_p1k(_bin1k("blog", a_)), "%.2f" % _bin1k("blog", a_)) if a_ != "page_view" else "-"), n(x(_p1k(_bin1k("diger", a_)), "%.2f" % _bin1k("diger", a_)) if a_ != "page_view" else "-")] for a_, b_, c_ in IUAD]
BKN = G["blog_kanal"]; _bkt = sum(BKN.values()); _BKS = list(BKN)[:8]
T_BKAN = tablo([th("Kanal", "Channel", "Blog sayfası görüntülenen oturumların varsayılan kanal grubu (Session default channel group).", "Default channel group of sessions with a blog page view."),
                th("Oturum payı", "Share of sessions", "Kanalın blog sayfası görüntülenen oturumlar içindeki payı, 1 Ara 2025 - 30 Eyl 2026 (blog sayfaları bu mülkte Aralık 2025'ten itibaren ölçülür).", "The channel's share of sessions with a blog page view, 1 Dec 2025 - 30 Sep 2026 (blog pages are measured in this property from December 2025).", True)],
               [[x(k_, k_), n(yzd(100 * BKN[k_] / _bkt))] for k_ in _BKS] + [[x("Diğer", "Other"), n(yzd(100 * sum(v for k_, v in BKN.items() if k_ not in _BKS) / _bkt))]], "dar")
_bgi = G["blog_giris"]; _bgp = 100 * _bgi.get("blog", 0) / sum(_bgi.values())
T_IU = tablo([th("Olay", "Event", "GA4 olayı.", "GA4 event."),
              th("Blog görüntülenen oturumlar", "Sessions with a blog view", "Oturumda /ilham-veren-fikirler sayfası görüntülenen oturum segmentinde olay sayısı, Oca-Eyl 2026 (aylık dışa aktarımların toplamı).", "Event count in the segment of sessions with a /ilham-veren-fikirler page view, Jan-Sep 2026 (sum of monthly exports).", True),
              th("Diğer oturumlar", "Other sessions", "Blog sayfası görüntülenmeyen oturumlarda olay sayısı, Oca-Eyl 2026.", "Event count in sessions without a blog page view, Jan-Sep 2026.", True),
              th("Blog oturumlarının payı", "Blog sessions' share", "Olayın blog görüntülenen oturumlardaki payı.", "The event's share in sessions with a blog view.", True),
              th("1.000 sayfa görüntülemede · blog", "Per 1,000 page views · blog", "Olay sayısı / sayfa görüntüleme × 1.000, blog görüntülenen oturumlar.", "Event count / page views × 1,000, sessions with a blog view.", True),
              th("1.000 sayfa görüntülemede · diğer", "Per 1,000 page views · other", "Olay sayısı / sayfa görüntüleme × 1.000, diğer oturumlar.", "Event count / page views × 1,000, other sessions.", True)], rows_iu, "dar")

# blog görüntülenen oturumlarda oturum, satın alma ve gelir (Ara 2025 - Eyl 2026; blog sayfaları bu mülkte Aralık 2025'ten itibaren)
IG = G["icerik_gelir"]; _IGA = [m for m in IG if "2025-12" <= m <= "2026-09"]
_ig = {sg: {k_: sum(IG[m][sg][k_] for m in _IGA) for k_ in ("oturum", "gelir", "satin")} for sg in ("blog", "diger")}
_igg = _ig["blog"]["gelir"] + _ig["diger"]["gelir"]
def _cr(sg): return 100 * _ig[sg]["satin"] / _ig[sg]["oturum"]
def _tlo(sg): v = _ig[sg]["gelir"] / _ig[sg]["oturum"]; return x(("%.2f" % v).replace(".", ",") + " TL", "%.2f TL" % v)
T_BGEL = tablo([th("Oturum grubu", "Session group", "Blog yazısı (/ilham-veren-fikirler) görüntülenen ve görüntülenmeyen oturum segmentleri.", "Session segments with and without a blog article (/ilham-veren-fikirler) view."),
                th("Oturum", "Sessions", "1 Ara 2025 - 30 Eyl 2026 oturum (aylık dışa aktarımların toplamı).", "Sessions, 1 Dec 2025 - 30 Sep 2026 (sum of monthly exports).", True),
                th("Satın alma", "Purchases", "Aynı oturumda gerçekleşen e-ticaret satın alma.", "E-commerce purchases in the same session.", True),
                th("Gelir", "Revenue", "Aynı oturumda gerçekleşen gelir (TL).", "Revenue in the same session (TL).", True),
                th("Gelir payı", "Revenue share", "Grubun toplam gelir içindeki payı.", "The group's share of total revenue.", True),
                th("Satın alma oranı", "Purchase rate", "Satın alma / oturum.", "Purchases / sessions.", True),
                th("Oturum başına gelir", "Revenue per session", "Gelir / oturum (TL).", "Revenue / sessions (TL).", True)],
               [[x(a_, b_), cellk(_ig[sg]["oturum"]), cell(_ig[sg]["satin"]), n(tl(_ig[sg]["gelir"])), n(yzd(100 * _ig[sg]["gelir"] / _igg)), n(yzd(_cr(sg), 3)), n(_tlo(sg))]
                for sg, a_, b_ in (("blog", "Blog yazısı görüntülenen oturumlar", "Sessions with a blog article view"), ("diger", "Diğer oturumlar", "Other sessions"))], "dar")
INS_BLOG = insight("Blog yazıları (/ilham-veren-fikirler/) 1 Ara 2025 - 30 Eyl 2026'da %s görüntüleme almıştır (www.vitra.com.tr sayfaları bu GA4 mülkünde Aralık 2025'ten itibaren ölçülmektedir); en çok görüntülenen sayfalar blog ana sayfası ve montaj rehberi hub'ıdır. **Blog yazısı görüntülenen %s oturumda %s satın alma ve %s gelir gerçekleşmiştir** (gelirin %s'i); bu oturumların satın alma oranı %s ile diğer oturumların (%s) üzerindedir. Sepet sayfasında oturum yenilendiği için blogdan sonra yeni bir oturumda tamamlanan satın almalar bu sayılara girmemektedir; değerler alt sınır olarak okunmalıdır. Blog sayfalarındaki ürün listeleri %s kez görüntülenmiş (view_item_list), bu listelerden ürüne %s tıklama (select_item) ve doğrudan %s sepete ekleme (add_to_cart) gerçekleşmiştir. Blog sayfası görüntülenen oturumların %s'i organik aramadan, %s'i ücretli aramadan gelmekte, %s'i doğrudan bir blog sayfasında başlamaktadır. Koleksiyon listesi sayfası (/v-/koleksiyonlar) tek başına %s görüntüleme almıştır."
                   % (k(bv), k(_ig["blog"]["oturum"]), bin(_ig["blog"]["satin"]), tl(_ig["blog"]["gelir"]), yzd(100 * _ig["blog"]["gelir"] / _igg), yzd(_cr("blog"), 3), yzd(_cr("diger"), 3),
                      k(BO["view_item_list"]), bin(BO["select_item"]), bin(BO["add_to_cart"]), yzd(100 * BKN.get("Organic Search", 0) / _bkt), yzd(100 * BKN.get("Paid Search", 0) / _bkt), yzd(_bgp), k(KL[0][1])),
                   "Blog articles (/ilham-veren-fikirler/) received %s views in 1 Dec 2025 - 30 Sep 2026 (www.vitra.com.tr pages are measured in this GA4 property from December 2025); the most viewed pages are the blog home page and the installation guide hub. **The %s sessions with a blog article view had %s purchases and %s of revenue** (%s of revenue); their purchase rate of %s is above other sessions (%s). As the session is renewed on the cart page, purchases completed in a new session after the blog are not included in these figures; the values should be read as a lower bound. Product lists on blog pages were viewed %s times (view_item_list), with %s clicks from these lists to products (select_item) and %s direct add-to-carts (add_to_cart). Of sessions with a blog page view, %s come from organic search and %s from paid search, and %s start directly on a blog page. The collection list page (/v-/koleksiyonlar) alone received %s views."
                   % (k(bv), k(_ig["blog"]["oturum"]), bin(_ig["blog"]["satin"]), tl(_ig["blog"]["gelir"]), yzd(100 * _ig["blog"]["gelir"] / _igg), yzd(_cr("blog"), 3), yzd(_cr("diger"), 3),
                      k(BO["view_item_list"]), bin(BO["select_item"]), bin(BO["add_to_cart"]), yzd(100 * BKN.get("Organic Search", 0) / _bkt), yzd(100 * BKN.get("Paid Search", 0) / _bkt), yzd(_bgp), k(KL[0][1])), "D45", "D2")

# ---------------------------------------------------------------- 7 · promosyon ve kupon (görüntülenme ve tıklama: son 12 ay aylık dışa aktarım; satın alma ataması ve kupon: önceki dışa aktarım)
PR = [{"ad": r[0], "gor": r[1], "tik": r[2]} for r in G["promosyon_12ay"] if r[1]]
prt = sum(r["gor"] for r in PR); prk = sum(r["tik"] for r in PR)
_prns = next((r["gor"] for r in PR if r["ad"] == "(not set)"), 0)
rows_p = []
for r in sorted([r for r in PR if r["ad"] != "(not set)"], key=lambda r: -r["gor"])[:15]:
    rows_p.append([x(r["ad"], r["ad"]), cellk(r["gor"]), cellk(r["tik"]), n(yzd(100 * r["tik"] / r["gor"], 1) if r["gor"] else "-")])
T_PROMO = tablo([th("Promosyon adı", "Promotion name", "GA4 item promotion name (promosyon alanının sitedeki metni); kendi yazımıyla verilmiştir.", "GA4 item promotion name (the promotion slot's text on the site); given in its own wording."),
                 th("Görüntülenme", "Views", "%s promosyonda görüntülenen ürün (Items viewed in promotion); aylık dışa aktarımların toplamı." % D_12[0], "Items viewed in promotion, %s; sum of monthly exports." % D_12[1], True),
                 th("Tıklama", "Clicks", "Promosyonda tıklanan ürün (Items clicked in promotion).", "Items clicked in promotion.", True),
                 th("Tıklama oranı", "Click-through rate", "Tıklama / görüntülenme.", "Clicks / views.", True)], rows_p, "dar")
_ku = next((r for r in G["promosyon"] if r.get("kupon") and r["kupon"] not in ("(not set)",) and r["satin"]), None)
_ctr = sorted([r for r in PR if r["ad"] != "(not set)" and r["gor"] >= 10000], key=lambda r: -r["tik"] / r["gor"])[:3]
def _pad(r): return _re.sub(r"^(Slider|Anasayfa) - ", "", r["ad"]).rstrip(".")
_CTR_TR = ", ".join("\"%s\" (%s)" % (_pad(r), yzd(100 * r["tik"] / r["gor"])) for r in _ctr)
_CTR_EN = ", ".join("\"%s\" (%s)" % (_pad(r), _pe(100 * r["tik"] / r["gor"])) for r in _ctr)
INS_PROMO = insight("Sitedeki promosyon alanları 1 Ekim 2025 - 30 Eylül 2026'da %s ürün görüntülenmesi ve %s tıklama almıştır; 10 bin ve üzeri görüntülenme alan promosyonlarda en yüksek tıklama oranı %s ile gerçekleşmiştir. Görüntülenmelerin %s'i promosyon adı boş (not set) alanlardadır. **Promosyon adı taşıyan alanların hiçbirine sepete ekleme ya da satın alma atanmamaktadır**: satın alma kırılımını içeren dışa aktarımda (1 Eyl 2025 - 30 Eyl 2026) satın alınan ürünlerin tamamı promosyon adı boş görünmekte, kupon kodu yalnız %s'de kayıtlıdır (%s ürün, %s). Promosyon tıklamasının satın almaya taşınması, kampanyaların gelire etkisinin ölçülmesini sağlayabilir."
                    % (k(prt), k(prk), _CTR_TR, yzd(100 * _prns / prt), _ku["kupon"] if _ku else "-", bin(_ku["satin"]) if _ku else "-", tl(_ku["gelir"]) if _ku else "-"),
                    "The promotion slots on the site received %s item views and %s clicks in 1 October 2025 - 30 September 2026; among promotions with 10 thousand views or more, the highest click-through rates are %s. %s of views are in slots with an empty (not set) promotion name. **No add-to-cart or purchase is attributed to any slot with a promotion name**: in the export with the purchase breakdown (1 Sep 2025 - 30 Sep 2026) all purchased items appear with an empty promotion name, and a coupon code is recorded only for %s (%s items, %s). Carrying the promotion click through to the purchase can make it possible to measure campaigns' effect on revenue."
                    % (k(prt), k(prk), _CTR_EN, yzd(100 * _prns / prt), _ku["kupon"] if _ku else "-", bin(_ku["satin"]) if _ku else "-", tl(_ku["gelir"]) if _ku else "-"), "D45")

# ---------------------------------------------------------------- 8 · satın alma hunisi
HU = G["huni"]
def _hu(y, m2=9): return [sum((HU.get("%d-%02d" % (y, m)) or [0] * 7)[i] for m in range(1, m2 + 1)) for i in range(7)]
_h25, _h26, _h26a = _hu(2025), _hu(2026), _hu(2026, 8)
def _gc(t, i): return 100 * t[i] / t[i - 1] if t[i - 1] else None
HAD = [("view_item_list", "Ürün listesi görüntüleme", "Product list view"), ("view_item", "Ürün görüntüleme", "Product view"), ("add_to_cart", "Sepete ekleme", "Add to cart"),
       ("begin_checkout", "Ödemeye başlama", "Begin checkout"), ("add_shipping_info", "Teslimat bilgisi", "Shipping info"), ("add_payment_info", "Ödeme bilgisi", "Payment info"), ("purchase", "Satın alma", "Purchase")]
rows_h = [[x("%s (%s)" % (b_, a_), "%s (%s)" % (c_, a_)), cellk(_h25[i]), cellk(_h26[i]), n(yzd(_gc(_h25, i)) if i else "-"), n(yzd(_gc(_h26, i)) if i else "-")] for i, (a_, b_, c_) in enumerate(HAD)]
T_HUNI = tablo([th("Huni adımı", "Funnel step", "GA4 e-ticaret olayı; adımlar ürün listesinden satın almaya sıralıdır.", "GA4 e-commerce event; steps are ordered from product list to purchase."),
                th("Oca-Eyl 2025", "Jan-Sep 2025", "Aylık olay sayısının (Event count) Ocak - Eylül 2025 toplamı.", "January - September 2025 total of the monthly event count.", True),
                th("Oca-Eyl 2026", "Jan-Sep 2026", "Aylık olay sayısının (Event count) Ocak - Eylül 2026 toplamı; Eylül 2026'da sepete ekleme olayında hatalı tetiklenme bulunmaktadır.", "January - September 2026 total of the monthly event count; the add-to-cart event fired erroneously in September 2026.", True),
                th("Geçiş 2025", "Step rate 2025", "Olay sayısının bir önceki adıma oranı, Oca-Eyl 2025.", "The step value as a share of the previous step, Jan-Sep 2025.", True),
                th("Geçiş 2026", "Step rate 2026", "Olay sayısının bir önceki adıma oranı, Oca-Eyl 2026.", "The step value as a share of the previous step, Jan-Sep 2026.", True)], rows_h, "dar")
# huni görseli: adım kartları ve aralarında geçiş oranı (masaüstünde yatay, dar ekranda dikey); 2026 oranı 2025'e göre renklenir
import html as _hh
def _hn():
    p_ = ['<div class="hn-g">']
    for y_, (yl_tr, yl_en) in enumerate((("Oca-Eyl 2025", "Jan-Sep 2025"), ("Oca-Eyl 2026", "Jan-Sep 2026"))):
        p_.append('<div class="hn-y hn-y%d"><i></i>%s</div>' % (y_, x(yl_tr, yl_en)))
    for i, (a_, b_, c_) in enumerate(HAD):
        x(a_, a_)
        for _pc in a_.replace("_", "_\n").split("\n"): x(_pc, _pc)   # <wbr> olay adini metin parcalarina boler; parcalar iki dilde aynidir
        for y_, (yil, t_) in enumerate(((2025, _h25), (2026, _h26))):
            if i:
                o_, o25 = _gc(t_, i), _gc(_h25, i)
                yon = "" if y_ == 0 else (" up" if o_ > o25 + 0.05 else (" dn" if o_ < o25 - 0.05 else ""))
                not_tr = "%s adımından %s adımına geçiş, Oca-Eyl %d%s." % (HAD[i - 1][1], HAD[i][1].lower(), yil, "" if y_ == 0 else "; 2025'te %s" % yzd(o25))
                not_en = "Step rate from %s to %s, Jan-Sep %d%s." % (HAD[i - 1][2].lower(), HAD[i][2].lower(), yil, "" if y_ == 0 else "; %s in 2025" % yzd(o25))
                x(not_tr, not_en)
                p_.append('<div class="hn-o hn-a%d hn-y%d%s" tabindex="0" data-t="%s"><b>%s</b><i aria-hidden="true">→</i></div>' % (i, y_, yon, _hh.escape(not_tr, quote=True), yzd(o_)))
            not_tr = "GA4 olay sayısı (Event count), 1 Oca - 30 Eyl %d%s." % (yil, "; Eylül 2026'da bu olayda hatalı tetiklenme bulunmaktadır" if (yil == 2026 and a_ == "add_to_cart") else "")
            not_en = "GA4 event count, 1 Jan - 30 Sep %d%s." % (yil, "; the event fired erroneously in September 2026" if (yil == 2026 and a_ == "add_to_cart") else "")
            x(not_tr, not_en)
            p_.append('<div class="hn-k hn-a%d hn-y%d" tabindex="0" data-t="%s"><span class="hn-a">%s</span><b>%s</b><small>%s</small></div>'
                      % (i, y_, _hh.escape(not_tr, quote=True), x(b_, {"Satın alma": "Purchases"}.get(b_, c_)), bin(t_[i]), a_.replace("_", "_<wbr>")))
    p_.append("</div>")
    cap = x("Satın alma hunisi · GA4 olay sayısı, Oca - Eyl 2025 (koyu) ve 2026 (turuncu); oklardaki oran bir önceki adıma geçiştir, 2026 oranı 2025'ten yüksekse yeşil, düşükse kırmızıdır",
            "Purchase funnel · GA4 event count, Jan - Sep 2025 (dark) and 2026 (orange); the rate on each arrow is the step rate from the previous step, the 2026 rate is green when higher than 2025 and red when lower")
    return '<figure class="fig hn"><figcaption class="figcap">%s</figcaption>%s</figure>' % (cap, "".join(p_))
V_HUNI = _hn()
INS_HUNI = insight("Ocak - Eylül 2026'da sepete eklemeden ödemeye başlamaya geçiş oranı %s'e inmiştir (2025'in aynı aylarında %s); Sepete ekleme olayının hatalı tetiklendiği Eylül 2026 hariç tutulduğunda da oran %s'dir. Ödemeye başlayanların teslimat bilgisine ilerleme oranı ise %s'den %s'e, ödeme bilgisinden satın almaya geçiş %s'ten %s'e yükselmiştir. **Kayıp ödeme adımında değil, sepet ile ödemeye başlama arasında yoğunlaşmaktadır**; bu, sepet sonrasındaki giriş ve üyelik ekranlarıyla (Bölüm [[b:yolculuk]]) ilişkilendirilebilir."
                   % (yzd(_gc(_h26, 3)), yzd(_gc(_h25, 3)), yzd(_gc(_h26a, 3)), yzd(_gc(_h25, 4)), yzd(_gc(_h26, 4)), yzd(_gc(_h25, 6)), yzd(_gc(_h26, 6))),
                   "In January - September 2026, the rate from add to cart to begin checkout fell to %s (%s in the same months of 2025); it is %s when September 2026, when the add-to-cart event fired erroneously, is excluded. The rate from begin checkout to shipping info rose from %s to %s, and from payment info to purchase from %s to %s. **The loss is concentrated between the cart and beginning checkout, not in the payment step**; this can be associated with the sign-in and account screens after the cart (Section [[b:yolculuk]])."
                   % (yzd(_gc(_h26, 3)), yzd(_gc(_h25, 3)), yzd(_gc(_h26a, 3)), yzd(_gc(_h25, 4)), yzd(_gc(_h26, 4)), yzd(_gc(_h25, 6)), yzd(_gc(_h26, 6))), "D45")

# ---------------------------------------------------------------- 9 · yeni ve geri dönen kullanıcılar, tekrar alım
YD, AL = G["yeni_donen"], G["alici"]
def _yd(y, tur, a): return sum((YD.get("%d-%02d" % (y, m)) or {}).get(tur, {}).get(a) or 0 for m in range(1, 10))
def _ydp(y, tur, a):
    t = sum(_yd(y, k_, a) for k_ in ("new", "returning", "(not set)")); return 100 * _yd(y, tur, a) / t if t else None
def _al(y, a): return sum((AL.get("%d-%02d" % (y, m)) or {}).get(a) or 0 for m in range(1, 10))
def _tekrar(y): return 100 * (1 - _al(y, "ilk") / _al(y, "toplam"))
rows_yd = [[x(e, e_en)] + [n(yzd(_ydp(y, "returning", a))) for a in ("oturum", "islem", "gelir")] + [n(yzd(_ydp(y, "(not set)", "islem"))), n(yzd(_tekrar(y)))] for e, e_en, y in (("Oca-Eyl 2025", "Jan-Sep 2025", 2025), ("Oca-Eyl 2026", "Jan-Sep 2026", 2026))]
T_YD = tablo([th("Dönem", "Period", "Ocak - Eylül toplamı.", "January - September total."),
              th("Geri dönen · oturum payı", "Returning · share of sessions", "Geri dönen kullanıcı (returning) oturumlarının tüm oturumlar içindeki payı.", "Returning users' sessions as a share of all sessions.", True),
              th("Geri dönen · işlem payı", "Returning · share of transactions", "Geri dönen kullanıcıların işlem (transaction) payı.", "Returning users' share of transactions.", True),
              th("Geri dönen · gelir payı", "Returning · share of revenue", "Geri dönen kullanıcıların gelir payı.", "Returning users' share of revenue.", True),
              th("(not set) · işlem payı", "(not set) · share of transactions", "Yeni ya da geri dönen olarak sınıflanamayan işlemlerin payı; 2025'te yüksek olduğu için yıllar arası kıyas yön gösterir.", "Share of transactions not classified as new or returning; as it is high in 2025, the comparison between years is indicative.", True),
              th("Tekrar alan alıcı payı", "Repeat purchaser share", "Alıcılar içinde ilk kez satın almayanların payı (1 - First time purchasers / Total purchasers).", "Share of purchasers who are not first-time purchasers (1 - First time purchasers / Total purchasers).", True)], rows_yd, "dar")
INS_YD = insight("Ocak - Eylül 2026'da gelirin %s'i geri dönen kullanıcılardan gelmektedir (2025'in aynı aylarında %s); alıcıların %s'i daha önce de satın almış kullanıcılardır (2025'te %s). Geri dönen kullanıcı oturumlarının payının %s'den %s'e çıkmasında Aralık 2025'te www.vitra.com.tr ziyaretçilerinin aynı GA4 mülküne katılmasının da etkisi bulunmaktadır. **Tekrar alan alıcı payının iki katına çıkması**, ilk alımdan sonra sitenin yeniden tercih edildiğini göstermektedir; bu alıcılar yedek parça, aksesuar ve montaj gibi tamamlayıcı ürünlerin hedef kitlesidir (Bölüm [[b:set]])."
                 % (yzd(_ydp(2026, "returning", "gelir")), yzd(_ydp(2025, "returning", "gelir")), yzd(_tekrar(2026)), yzd(_tekrar(2025)), yzd(_ydp(2025, "returning", "oturum")), yzd(_ydp(2026, "returning", "oturum"))),
                 "In January - September 2026, %s of revenue comes from returning users (%s in the same months of 2025); %s of purchasers had purchased before (%s in 2025). The rise in returning users' share of sessions from %s to %s is also affected by www.vitra.com.tr visitors joining the same GA4 property in December 2025. **The repeat purchaser share doubling** shows the site being chosen again after the first purchase; these purchasers are the target audience for complementary products such as spare parts, accessories and installation (Section [[b:set]])."
                 % (yzd(_ydp(2026, "returning", "gelir")), yzd(_ydp(2025, "returning", "gelir")), yzd(_tekrar(2026)), yzd(_tekrar(2025)), yzd(_ydp(2025, "returning", "oturum")), yzd(_ydp(2026, "returning", "oturum"))), "D45")

# ---------------------------------------------------------------- 10 · ürün ve kategori performansı (item)
UK, UM, U26 = G["urun_kat"], G["urun_marka"], G["urun_2026"]
_uk26 = UK["2026"]; _ukt = [sum(v[i] for v in _uk26.values()) for i in range(4)]
UKAD = {"Banyo Mobilyaları": "Bathroom Furniture", "Klozetler ve Rezervuarlar": "WCs and cisterns", "Bataryalar ve Musluklar": "Taps and valves", "Banyo Aksesuarları": "Bathroom Accessories",
        "Yıkanma Alanları": "Bathing Areas", "Lavabolar": "Washbasins", "Vitrifiyeler": "Sanitaryware", "Montaj Hizmeti": "Installation service", "Armatürler": "Taps and Mixers", "Duş Sistemleri": "Shower systems"}   # rapordaki mevcut karşılıklarla aynı
for a_, b_ in UKAD.items(): x(a_, b_)
x("Diğer", "Other")
_ukana = [k_ for k_ in sorted(_uk26, key=lambda k_: -_uk26[k_][3]) if k_ in UKAD]
_ukdig = [sum(v[i] for k_, v in _uk26.items() if k_ not in UKAD) for i in range(4)]
def _sep(v): return n(yzd(100 * v[4] / v[5])) if len(v) > 5 and v[5] else n("-")
rows_uk = [[x(k_, UKAD[k_]), cellk(_uk26[k_][0]), _sep(_uk26[k_]), cell(_uk26[k_][2]), n(x(_p1k(1000 * _uk26[k_][2] / _uk26[k_][0]), "%.2f" % (1000 * _uk26[k_][2] / _uk26[k_][0]))), n(yzd(100 * _uk26[k_][3] / _ukt[3]))] for k_ in _ukana] + \
          [[x("Diğer", "Other"), cellk(_ukdig[0]), n("-"), cell(_ukdig[2]), n("-"), n(yzd(100 * _ukdig[3] / _ukt[3]))]]
T_UK = tablo([th("Ana kategori", "Main category", "GA4 ürün kategorisi (2026 ağacında ikinci seviye).", "GA4 item category (second level in the 2026 tree)."),
              th("Görüntülenen ürün", "Items viewed", "Items viewed, Oca-Eyl 2026.", "Items viewed, Jan-Sep 2026.", True),
              th("Sepete ekleme oranı", "Add-to-cart rate", "Sepete eklenen ürün / görüntülenen ürün, Oca-Ağu 2026; sepete eklenen adette hatalı değer taşıyan beş ürün kodu (7910B476-0090, 121-003-909, ETIC_MTJ(KUCUK), ETIC_MTJ(BUYUK), ETIC_MTJ(ARMATUR)) ve hatalı tetiklenmenin görüldüğü Eylül 2026 hesaba katılmamıştır.", "Items added to cart / items viewed, Jan-Aug 2026; five item IDs with invalid added-to-cart quantities (7910B476-0090, 121-003-909, ETIC_MTJ(KUCUK), ETIC_MTJ(BUYUK), ETIC_MTJ(ARMATUR)) and September 2026, when the event fired erroneously, are excluded.", True),
              th("Satın alınan ürün", "Items purchased", "Items purchased (adet), Oca-Eyl 2026.", "Items purchased (units), Jan-Sep 2026.", True),
              th("1.000 görüntülemede satın alma", "Purchases per 1,000 views", "Satın alınan ürün / görüntülenen ürün × 1.000.", "Items purchased / items viewed × 1,000.", True),
              th("Ürün geliri payı", "Share of item revenue", "Kategorinin Oca-Eyl 2026 ürün geliri (item revenue) içindeki payı; ürün geliri genel bakıştaki gelirden farklı hesaplandığı için pay olarak verilmiştir.", "The category's share of Jan-Sep 2026 item revenue; given as a share because item revenue is calculated differently from the overview revenue.", True)], rows_uk, "dar")
_UH = [th("Ürün", "Product", "GA4 ürün adı (Item name) ve ürün kodu.", "GA4 item name and item ID."), th("Kategori", "Category", "Ana kategori.", "Main category."), th("Marka", "Brand", "Item brand.", "Item brand."),
       th("Görüntülenen", "Viewed", "Items viewed, Oca-Eyl 2026.", "Items viewed, Jan-Sep 2026.", True), th("Satın alınan", "Purchased", "Items purchased, Oca-Eyl 2026.", "Items purchased, Jan-Sep 2026.", True),
       th("1.000 görüntülemede satın alma", "Purchases per 1,000 views", "Satın alınan / görüntülenen × 1.000.", "Purchased / viewed × 1,000.", True), th("Ürün geliri payı", "Share of item revenue", "Oca-Eyl 2026 ürün geliri içindeki pay.", "Share of Jan-Sep 2026 item revenue.", True)]
def _urow(r):
    k_, ad, kat, mr, v, pu, rv = r
    x(mr or "-", mr or "-")
    return [x("%s · %s" % (ad, k_), "%s · %s" % (ad, k_)), x(kat, UKAD.get(kat, kat)) if kat in UKAD else x(kat or "-", kat or "-"), x(mr or "-", mr or "-"), cellk(v), cell(pu),
            n(x(_p1k(1000 * pu / v), "%.2f" % (1000 * pu / v)) if v else "-"), n(yzd(100 * rv / _ukt[3], 2))]
_U_SAT = sorted([r for r in U26 if r[2] != "Montaj Hizmeti"], key=lambda r: -r[5])[:15]
_U_DUS = sorted([r for r in U26 if r[2] != "Montaj Hizmeti" and r[4] >= 8000], key=lambda r: r[5] / r[4])[:15]
_U_MTJ = sorted([r for r in U26 if r[2] == "Montaj Hizmeti"], key=lambda r: -r[5])[:10]
T_UURN = sekmeler([("En çok satın alınan 15 ürün", "Top 15 items purchased", tablo(_UH, [_urow(r) for r in _U_SAT], "dar xl")),
                   ("Çok görüntülenip az satın alınan ürünler", "Most viewed, least purchased items", tablo(_UH, [_urow(r) for r in _U_DUS], "dar xl")),
                   ("Montaj hizmeti kalemleri", "Installation service items", tablo(_UH, [_urow(r) for r in _U_MTJ], "dar xl"))], "ttabs")
_mt25, _mt26 = UK["2025"].get("Montaj Hizmeti", [0, 0, 0, 0]), _uk26.get("Montaj Hizmeti", [0, 0, 0, 0])
def _mpay(y): d = UM[y]; return 100 * d.get("Artema", 0) / sum(d.values())
def _kr(k_): return 1000 * _uk26[k_][2] / _uk26[k_][0]
INS_UK = insight("Ocak - Eylül 2026'da 1.000 ürün görüntülemesine düşen satın alma banyo aksesuarlarında %s ile en yüksektir; banyo mobilyasında %s, duş sistemlerinde %s, lavabolarda %s seviyesindedir. Adet olarak en çok satın alınan ürünler filtreli ara musluk, klozet kapakları, ankastre stop valf ve aksesuarlar gibi tamamlayıcı ürünlerdir; çok görüntülenen duş başlığı, duş kolonu, lavabo dolabı ve asma klozet modellerinde satın alma sınırlı kalmaktadır. **Montaj hizmeti kalemi %s adet satın alınmıştır (2025'in aynı aylarında %s)**; bu, aynı dönemdeki %s siparişe oranla her üç siparişe yaklaşık bir montaj kalemi düştüğünü göstermektedir. Artema'nın ürün geliri içindeki payı %s'dir (2025'te %s)."
                 % (_p1k(_kr("Banyo Aksesuarları")), _p1k(_kr("Banyo Mobilyaları")), _p1k(_kr("Duş Sistemleri")), _p1k(_kr("Lavabolar")), bin(_mt26[2]), bin(_mt25[2]), bin(p26), yzd(_mpay("2026")), yzd(_mpay("2025"))),
                 "In January - September 2026, purchases per 1,000 item views are highest in bathroom accessories at %s; they are %s in bathroom furniture, %s in shower systems and %s in washbasins. By units, the most purchased items are complementary products such as the filtered angle valve, toilet seats, concealed stop valve and accessories; purchases stay limited for widely viewed shower head, shower column, basin cabinet and wall-hung WC models. **%s installation service items were purchased (%s in the same months of 2025)**; against the %s orders in the same period, this means roughly one installation item for every three orders. Artema's share of item revenue is %s (%s in 2025)."
                 % ("%.2f" % _kr("Banyo Aksesuarları"), "%.2f" % _kr("Banyo Mobilyaları"), "%.2f" % _kr("Duş Sistemleri"), "%.2f" % _kr("Lavabolar"), bin(_mt26[2]), bin(_mt25[2]), bin(p26), yzd(_mpay("2026")), yzd(_mpay("2025"))), "D45")

def _blok(h3_tr, h3_en, *parcalar):
    return "<h3>%s</h3>\n%s" % (x(h3_tr, h3_en), "\n".join(parcalar))
HTML = "\n".join([
 '<p class="lede">%s</p>' % x("Google Analytics 4 (GA4) verisi, vitra.com.tr'nin oturum, satın alma ve gelir performansını kanal, site içi arama, ödeme adımı, içerik ve promosyon kırılımında göstermektedir. Veri VitrA ekibinin GA4 dışa aktarımından alınmıştır (05.10.2026); tabloların dönemleri başlık ve sütun açıklamalarında verilmiştir. Aralık 2025'te www.vitra.com.tr trafiği aynı GA4 mülküne katıldığı için oturum ve oturum başına dönüşüm oranı Aralık öncesi ve sonrası arasında kıyaslanmaz; satın alma ve gelir iki dönemde de kıyaslanabilir.", "Google Analytics 4 (GA4) data shows vitra.com.tr's sessions, purchases and revenue by channel, site search, payment step, content and promotion. The data comes from the VitrA team's GA4 export (05.10.2026); each table's period is given in its heading and column descriptions. As www.vitra.com.tr traffic joined the same GA4 property in December 2025, sessions and the conversion rate per session are not compared before and after December; purchases and revenue are comparable in both periods."),
 '<div class="kpis">%s%s%s%s</div>' % (kpi_kart(tl(r26), "E-ticaret geliri · Oca-Eyl 2026; Oca-Eyl 2025'e göre %s" % _isr(_deg(r25, r26)), "E-commerce revenue · Jan-Sep 2026; %s against Jan-Sep 2025" % _isr_en(_deg(r25, r26))), kpi_kart(bin(p26), "E-ticaret satın alma · Oca-Eyl 2026; Oca-Eyl 2025'e göre %s" % _isr(_deg(p25, p26)), "E-commerce purchases · Jan-Sep 2026; %s against Jan-Sep 2025" % _isr_en(_deg(p25, p26))), kpi_kart(tl(aov26), "Ortalama sipariş tutarı · Oca-Eyl 2026; 2025'te %s" % tl(aov25), "Average order value · Jan-Sep 2026; %s in 2025" % tl(aov25)), kpi_kart(yzd(100 * _o(_os_, 2026, "gelir") / _tg26), "Organik aramanın gelir payı · Oca-Eyl 2026; 2025'te %s" % yzd(100 * _o(_os_, 2025, "gelir") / _tg25), "Organic search share of revenue · Jan-Sep 2026; %s in 2025" % _pe(100 * _o(_os_, 2025, "gelir") / _tg25))),
 _blok("Aylık genel görünüm: gelir, satın alma ve oturum", "Monthly overview: revenue, purchases and sessions", G_AYLIK, T_AYLIK, INS_AYLIK),
 _blok("Satın alma hunisi: ürün listesinden satın almaya", "Purchase funnel: from product list to purchase", V_HUNI, T_HUNI, INS_HUNI),
 _blok("Kanal performansı: oturum, satın alma ve gelir", "Channel performance: sessions, purchases and revenue", G_KANAL, T_KANAL, G_KAY, INS_KANAL, T_KAYNAK),
 _blok("Giriş sayfası (landing page) türüne göre gelir", "Revenue by landing page type", T_LP, G_LP, T_OY, T_LPS, INS_LP, T_SR, T_SK, INS_SO),
 _blok("Ürün ve kategori performansı", "Item and category performance", T_UK, T_UURN, INS_UK),
 _blok("Site içi arama terimleri", "Site search terms", T_ARAMA, T_SINIF, INS_ARAMA),
 _blok("Ödeme ve teslimat adımı", "Payment and shipping step", T_ODEME, INS_ODEME),
 _blok("Satın alma dışı talep olayları", "Non-purchase request events", T_OLAY, INS_OLAY),
 _blok("Blog ve koleksiyon sayfaları: görüntüleme ve ürüne geçiş", "Blog and collection pages: views and move to products", T_BLOG, T_BGEL, T_IU, T_BKAN, T_KOL, INS_BLOG),
 _blok("Promosyon ve kupon", "Promotions and coupons", T_PROMO, INS_PROMO),
 kaynak("Google Analytics 4, VitrA ekibi dışa aktarımı (05.10.2026): genel bakış Oca 2025 - Eyl 2026, kanal ve kaynak / ortam 2025 ve 1 Oca - 5 Eki 2026; site içi arama 1 May - 30 Eyl 2026, sepet ve giriş sayfası oturumları Oca - Eyl 2026, ödeme, teslimat, servis düğmesi ve promosyon 1 Eki 2025 - 30 Eyl 2026, blog ve koleksiyon sayfaları 1 Ara 2025 - 30 Eyl 2026, huni ve ürün Oca 2025 - Eyl 2026 · Google Search Console, 1 Eki 2025 - 30 Eyl 2026",
        "Google Analytics 4, VitrA team export (05.10.2026): overview Jan 2025 - Sep 2026, channel and source / medium 2025 and 1 Jan - 5 Oct 2026, site search 1 May - 30 Sep 2026, cart and sign-in page sessions Jan - Sep 2026; payment, shipping, service button and promotions 1 Oct 2025 - 30 Sep 2026, blog and collection pages 1 Dec 2025 - 30 Sep 2026, funnel and items Jan 2025 - Sep 2026 · Google Search Console, 1 Oct 2025 - 30 Sep 2026", "D45", "D2"),
])
