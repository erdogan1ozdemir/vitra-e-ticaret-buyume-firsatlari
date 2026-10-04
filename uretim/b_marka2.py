# -*- coding: utf-8 -*-
"""Bolum 07 eki: marka adiyla ve marka + kategori ifadeleriyle yapilan aramalar (Google Ads Keyword Planner, Eyl 2022 - Agu 2026).
Veri: veri/islenmis/marka_kategori.json (marka_analiz.py). Yakin varyantlar tek sayilir; "<marka> seramik" sirket adi aramasi oldugu icin
kategori hesabina alinmaz. Rakipler VitrA listesinde hacmi olan kok ifadeler ve kelime evreninin ek bas kelimeleriyle olculmustur."""
import json, os, html as _h
from ortak import *
from rapor_parca1 import cizgi
from b_talep import sekmeler, AYA, YRENK, KAT_EN
import veri

O = json.load(open(os.path.join(veri.V, "islenmis", "marka_kategori.json"), encoding="utf-8"))
M, MK, K1, YAL, SV = O["marka"], O["marka_k1"], O["k1"], O["yalin"], O["servis"]
SV_T = {p: sum(v_[p] for v_ in SV.values()) for p in ("o2026", "o2025", "o2023")}
SVC = "Servis"   # ısı haritasının son sütunu: marka adıyla servis, yedek parça, bayi ve mağaza aramaları (marka + kategori toplamına dahil değildir)
K1_SIRA = sorted(K1, key=lambda k_: -K1[k_]["o2026"])
M_SIRA = sorted(M, key=lambda m_: -M[m_]["o2026"])
TOP26 = sum(M[m_]["o2026"] for m_ in M)
ESIK = 200   # değişim oranı yalnız taban dönemde aylık 200 ve üzeri aramada gösterilir

def _pay(m_, k1):
    t_ = sum(MK[a + "|" + k1]["o2026"] for a in M if a + "|" + k1 in MK)
    return 100 * MK[m_ + "|" + k1]["o2026"] / t_ if (m_ + "|" + k1) in MK and t_ else 0
def _yz(v): return yz(v) if v is not None else "-"
def _pe(v): return "-" if v is None else (("%+.1f" % v) if round(v, 1) else "0.0") + "%"
def _deg(t_, alan, taban):
    return t_[alan] if (t_.get(alan) is not None and t_[taban] >= ESIK) else None

# ---------------------------------------------------------------- 1 · yalin marka adi aramalari
URETICI = [("vitra", "VitrA"), ("vitra banyo", "VitrA"), ("vitra seramik", "VitrA"), ("artema", "Artema"), ("kale seramik", "Kale"), ("kalebodur", "Kale"), ("kale", "Kale"),
           ("creavit", "Creavit"), ("eca", "E.C.A."), ("geberit", "Geberit"), ("grohe", "Grohe"), ("hansgrohe", "Hansgrohe"), ("serel", "Serel"), ("duravit", "Duravit"),
           ("turkuaz seramik", "Turkuaz"), ("bocchi", "Bocchi"), ("isvea", "Isvea"), ("visam", "Visam"), ("newarc", "Newarc"), ("roca", "Roca"), ("ideal standard", "Ideal Standard"),
           ("orka banyo", "Orka"), ("idevit", "Idevit"), ("durul", "Durul"), ("yurtbay seramik", "Yurtbay"), ("ege seramik", "Ege Seramik"), ("çanakkale seramik", "Çanakkale Seramik"),
           ("kütahya seramik", "Kütahya Seramik"), ("ng kütahya seramik", "Kütahya Seramik"), ("seranit", "Seranit")]
PERAK = [("trendyol", "Trendyol"), ("hepsiburada", "Hepsiburada"), ("ikea", "IKEA"), ("koçtaş", "Koçtaş"), ("n11", "n11"), ("bauhaus", "Bauhaus"), ("vivense", "Vivense"),
         ("evidea", "Evidea"), ("tekzen", "Tekzen"), ("banyomarka", "Banyomarka")]
_BAS_Y = [th("Marka", "Brand", "Aranan marka.", "The brand searched."),
          th("Arama ifadesi", "Search phrase", "Google'a yazılan ifade; marka adı yalın ya da şirket adıyla (ör. kale seramik).", "The phrase typed into Google; the brand name alone or with the company name (e.g. kale seramik)."),
          th("2023 ort.", "2023 avg.", "2023 yılı aylık ortalama arama.", "Average monthly searches in 2023.", True),
          th("2024 ort.", "2024 avg.", "2024 yılı aylık ortalama arama.", "Average monthly searches in 2024.", True),
          th("2025 ort.", "2025 avg.", "2025 yılı aylık ortalama arama.", "Average monthly searches in 2025.", True),
          th("Oca-Ağu 2026 ort.", "Jan-Aug 2026 avg.", "Ocak - Ağustos 2026 aylık ortalama arama.", "Average monthly searches, January - August 2026.", True),
          th("2025 / 2024", "2025 / 2024", "2025 yıllık ortalamasının 2024 yıllık ortalamasına göre değişimi.", "Change of the 2025 annual average against the 2024 annual average.", True),
          th("YoY", "YoY", "Ocak - Ağustos 2026 ortalamasının 2025'in aynı aylarına göre değişimi.", "Change of the January - August 2026 average against the same months of 2025.", True),
          th("2023'ten bu yana", "Since 2023", "Ocak - Ağustos 2026 ortalamasının Ocak - Ağustos 2023 ortalamasına göre değişimi.", "Change of the January - August 2026 average against January - August 2023.", True)]
def _ysatir(L):
    out = []
    for ifade, ad in sorted([p_ for p_ in L if p_[0] in YAL], key=lambda p_: -YAL[p_[0]]["o2026"]):
        t_ = YAL[ifade]
        out.append([("<b>%s</b>" % x(ad, ad)) if ad == "VitrA" else x(ad, ad), kw(ifade), cellk(t_["y2023"]), cellk(t_["y2024"]), cellk(t_["y2025"]), cellk(t_["o2026"]),
                    n(_yz(t_["y2524"])), n(_yz(t_["yoy"])), n(_yz(t_["uc"]))])
    return out
T_YAL = sekmeler([("Üretici markalar", "Manufacturer brands", tablo(_BAS_Y, _ysatir(URETICI), "uzun xl")),
                  ("Perakendeci ve pazaryeri", "Retailers and marketplaces", tablo(_BAS_Y, _ysatir(PERAK), "xl"))])
_Y = lambda i_: YAL[i_]
_UR = sorted([(YAL[i_]["o2026"], i_) for i_, _ in URETICI if i_ in YAL and i_ != "kale"], reverse=True)
_VS = [i_ for _, i_ in _UR].index("vitra") + 1

# ---------------------------------------------------------------- 2 · marka x kategori isi haritasi
def _isi(metrik):
    bas = [th("Marka", "Brand", "Üretici marka; satırlar marka + kategori aramalarının toplam hacmine göre sıralanmıştır.", "Manufacturer brand; rows are ordered by the total volume of brand + category searches.")]
    ac = {"o2026": ("Ocak - Ağustos 2026 aylık ortalama marka + kategori araması (yakın yazım varyantları tek sayılmıştır).", "Average monthly brand + category searches, January - August 2026 (close spelling variants counted once)."),
          "yoy": ("Ocak - Ağustos 2026 ortalamasının 2025'in aynı aylarına göre değişimi; taban dönemde aylık 200'ün altında kalan hücrelerde gösterilmemiştir.", "Change of the January - August 2026 average against the same months of 2025; not shown where the base period is below 200 a month."),
          "uc": ("Ocak - Ağustos 2026 ortalamasının Ocak - Ağustos 2023 ortalamasına göre değişimi; taban dönemde aylık 200'ün altında kalan hücrelerde gösterilmemiştir.", "Change of the January - August 2026 average against January - August 2023; not shown where the base period is below 200 a month.")}[metrik]
    for k1 in K1_SIRA + ["Toplam"]:
        ad_tr, ad_en = (k1, KAT_EN.get(k1, k1)) if k1 != "Toplam" else ("Toplam", "Total")
        bas.append(th(ad_tr, ad_en, ("%s kategorisi · " % ad_tr if k1 != "Toplam" else "Tüm kategoriler · ") + ac[0], ("%s category · " % ad_en if k1 != "Toplam" else "All categories · ") + ac[1], True))
    bas.append(th("Servis, yedek parça, satış noktası", "Service, spare parts, sales points", "Marka adıyla yapılan servis, yedek parça, bayi, mağaza ve iletişim aramaları; marka + kategori toplamına dahil değildir. E.C.A. için alınmamıştır, çünkü bu aramalar kombi servisinden ayrıştırılamamaktadır. · " + ac[0],
                  "Service, spare parts, dealer, store and contact searches with the brand name; not included in the brand + category total. Not taken for E.C.A., as these searches cannot be separated from boiler service. · " + ac[1], True))
    mx = {k1: max([MK[m_ + "|" + k1]["o2026"] for m_ in M if m_ + "|" + k1 in MK] or [1]) for k1 in K1_SIRA}
    mx["Toplam"] = max(M[m_]["o2026"] for m_ in M); mx[SVC] = max([v_["o2026"] for v_ in SV.values()] or [1])
    govde = []
    for m_ in M_SIRA + ["Toplam"]:
        hucre = ['<td>%s</td>' % (("<b>%s</b>" % x(m_, m_)) if m_ in ("VitrA", "Toplam") else x(m_, m_)) if m_ != "Toplam" else '<td><b>%s</b></td>' % x("Toplam", "Total")]
        for k1 in K1_SIRA + ["Toplam", SVC]:
            if k1 == SVC: t_ = SV_T if m_ == "Toplam" else SV.get(m_)
            elif m_ == "Toplam": t_ = K1[k1] if k1 != "Toplam" else {"o2026": TOP26, "o2025": sum(M[a]["o2025"] for a in M), "o2023": sum(M[a]["o2023"] for a in M)}
            elif k1 == "Toplam": t_ = M[m_]
            else: t_ = MK.get(m_ + "|" + k1)
            if not t_ or not t_["o2026"]:
                hucre.append('<td class="n isi">-</td>'); continue
            yoy = (t_["o2026"] / t_["o2025"] - 1) * 100 if t_["o2025"] >= ESIK else None
            uc = (t_["o2026"] / t_["o2023"] - 1) * 100 if t_["o2023"] >= ESIK else None
            pay = None if k1 == SVC else (_pay(m_, k1) if (m_ not in ("Toplam",) and k1 != "Toplam") else (100 * t_["o2026"] / TOP26 if k1 == "Toplam" and m_ != "Toplam" else None))
            ad_k = {"Toplam": "tüm kategoriler", SVC: "servis, yedek parça ve satış noktası aramaları"}.get(k1, k1); ad_ke = {"Toplam": "all categories", SVC: "service, spare parts and sales point searches"}.get(k1, KAT_EN.get(k1, k1))
            mt = "Toplam" if m_ == "Toplam" else m_
            ac_tr = "%s · %s: aylık %s arama (Oca-Ağu 2026); YoY %s; 2023'ten bu yana %s%s" % (mt, ad_k, bin(t_["o2026"]), yzd(yoy).replace("%", "+%") if yoy and yoy > 0 else (yzd(yoy).replace("%-", "-%") if yoy is not None else "-"),
                     yzd(uc).replace("%", "+%") if uc and uc > 0 else (yzd(uc).replace("%-", "-%") if uc is not None else "-"), ("; kategori içindeki pay %s" % yzd(pay)) if pay is not None else "")
            ac_en = "%s · %s: %s searches a month (Jan-Aug 2026); YoY %s; since 2023 %s%s" % ("Total" if m_ == "Toplam" else m_, ad_ke, f"{round(t_['o2026']):,}", _pe(yoy), _pe(uc), ("; share within the category %s" % (("%.1f" % pay) + "%")) if pay is not None else "")
            x(ac_tr, ac_en)
            if metrik == "o2026":
                deger = k(t_["o2026"]) if t_["o2026"] >= 1000 else bin(t_["o2026"]); x(deger, deger.replace(",", "."))
                a_ = min(1.0, t_["o2026"] / mx[k1]); sinif = "isi-h"
            else:
                v_ = yoy if metrik == "yoy" else uc
                if v_ is None:
                    hucre.append('<td class="n isi" data-t="%s">-</td>' % _h.escape(ac_tr, quote=True)); continue
                deger = ("+" if round(v_, 1) > 0 else ("-" if round(v_, 1) < 0 else "")) + "%" + ("%.1f" % abs(v_)).replace(".", ","); x(deger, _pe(v_))
                a_ = min(1.0, abs(v_) / 40); sinif = "isi-a" if v_ > 0 else "isi-d"
            al_ = 0.08 + 0.62 * a_
            hucre.append('<td class="n isi %s%s" style="--a:%.2f" data-t="%s">%s</td>' % (sinif, " isi-k" if al_ >= 0.42 else "", al_, _h.escape(ac_tr, quote=True), deger))   # koyu hücrede yazı rengi tersine döner
        govde.append("<tr>%s</tr>" % "".join(hucre))
    return '<div class="tw isi-t uzun xl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join(bas), "".join(govde))
T_ISI = sekmeler([("Aylık arama · Oca-Ağu 2026", "Monthly searches · Jan-Aug 2026", _isi("o2026")),
                  ("YoY değişim", "YoY change", _isi("yoy")),
                  ("2023'ten bu yana", "Since 2023", _isi("uc"))])
x("tüm kategoriler", "all categories")

# ---------------------------------------------------------------- 3 · VitrA marka + kategori: yillar ve kategoriler
_BAS_V = [th("Ana kategori", "Main category", "VitrA kategori ağacındaki ana kategori; \"vitra\" ile başlayan aramalar kategori ifadesine göre eşlenmiştir.", "Main category of VitrA's category tree; searches starting with \"vitra\" are mapped by the category phrase."),
          th("2023 ort.", "2023 avg.", "2023 yılı aylık ortalama arama.", "Average monthly searches in 2023.", True),
          th("2024 ort.", "2024 avg.", "2024 yılı aylık ortalama arama.", "Average monthly searches in 2024.", True),
          th("2025 ort.", "2025 avg.", "2025 yılı aylık ortalama arama.", "Average monthly searches in 2025.", True),
          th("Oca-Ağu 2026 ort.", "Jan-Aug 2026 avg.", "Ocak - Ağustos 2026 aylık ortalama arama.", "Average monthly searches, January - August 2026.", True),
          th("2025 / 2024", "2025 / 2024", "2025 yıllık ortalamasının 2024'e göre değişimi.", "Change of the 2025 annual average against 2024.", True),
          th("YoY", "YoY", "Ocak - Ağustos 2026 ortalamasının 2025'in aynı aylarına göre değişimi.", "Change of the January - August 2026 average against the same months of 2025.", True),
          th("2023'ten bu yana", "Since 2023", "Ocak - Ağustos 2026 ortalamasının Ocak - Ağustos 2023 ortalamasına göre değişimi.", "Change of the January - August 2026 average against January - August 2023.", True)]
def _vsat(t_, ad):
    return [ad, cellk(t_["y2023"]), cellk(t_["y2024"]), cellk(t_["y2025"]), cellk(t_["o2026"]), n(_yz(t_["y2524"])), n(_yz(t_["yoy"])), n(_yz(t_["uc"]))]
_VK1 = sorted([k1 for k1 in K1 if "VitrA|" + k1 in MK], key=lambda k1: -MK["VitrA|" + k1]["o2026"])
T_VIT = tablo(_BAS_V, [_vsat(MK["VitrA|" + k1], x(k1, KAT_EN.get(k1, k1))) for k1 in _VK1] + [_vsat(M["VitrA"], "<b>%s</b>" % x("Toplam", "Total"))])
_AY = O["aylar"]
def _yil(seri, y_):
    return [seri[_AY.index("%d-%02d" % (y_, m_))] if "%d-%02d" % (y_, m_) in _AY else None for m_ in range(1, 13)]
G_VIT = cizgi([(str(y_), YRENK[str(y_)], _yil(M["VitrA"]["seri"], y_)) for y_ in (2023, 2024, 2025, 2026)],
              y_etiket=x("\"vitra\" + kategori aramaları · aylık toplam, yıllar üst üste (2026: Oca - Ağu)", "\"vitra\" + category searches · monthly total, years overlaid (2026: Jan - Aug)"),
              aylar=[a for a, _ in AYA], x_etiket=[a for a, _ in AYA], kalin={3: 3.2})
_RS = ["VitrA", "E.C.A.", "Artema", "Kale", "Creavit", "Geberit", "Serel", "Grohe"]
_RR = {"VitrA": "#10332F", "E.C.A.": "#E85F36", "Artema": "#F5A623", "Kale": "#7A8C89", "Creavit": "#2E7D32", "Geberit": "#4A90D9", "Serel": "#B96BC2", "Grohe": "#8B5A2B"}
_I23 = _AY.index("2023-01")
G_RAK = cizgi([(x(m_, m_), _RR[m_], M[m_]["seri"][_I23:]) for m_ in _RS], aylar=_AY[_I23:], gizli=(5, 6, 7), olcek=True,
              y_etiket=x("Marka + kategori aramaları · aylık toplam, Oca 2023 - Ağu 2026 · diğer markalar lejanttan açılabilir", "Brand + category searches · monthly total, Jan 2023 - Aug 2026 · other brands can be switched on in the legend"))
G_MARKA = sekmeler([("VitrA · yıllar üst üste", "VitrA · years overlaid", G_VIT), ("VitrA ve rakipler · aylık seri", "VitrA and competitors · monthly series", G_RAK)])

# ---------------------------------------------------------------- 4 · VitrA ile birlikte aranan ifadeler: ihtiyac sinifi
NV = O["vitra_niyet"]; _NT = sum(v_["o2026"] for v_ in NV.values())
N_EN = {"Jenerik ürün": "Generic product", "Fiyat": "Price", "Tamir ve bakım": "Repair and maintenance", "Tasarım ve fikir": "Design and ideas", "Ölçü ve teknik": "Dimensions and technical",
        "Montaj": "Installation", "Seçim ve karşılaştırma": "Choice and comparison", "Taksit ve ödeme": "Instalments and payment", "Yer ve kanal": "Place and channel"}
def _oran(a, b): return (a / b - 1) * 100 if b >= ESIK else None
_ORN = {}
for r_ in O["vitra_kw"]:
    _ORN.setdefault(r_["niyet"], [])
    if len(_ORN[r_["niyet"]]) < 4: _ORN[r_["niyet"]].append(r_["kw"])
T_NIY = tablo([th("İhtiyaç sınıfı", "Need class", "\"vitra\" ile yapılan aramanın taşıdığı ihtiyaç; kelime evreniyle aynı ifade kurallarıyla sınıflandırılmıştır.", "The need carried by the \"vitra\" search; classified with the same phrase rules as the keyword universe."),
               th("Aylık arama", "Monthly searches", "Ocak - Ağustos 2026 aylık ortalama.", "Average monthly searches, January - August 2026.", True),
               th("Pay", "Share", "\"vitra\" + kategori aramaları içindeki pay.", "Share of \"vitra\" + category searches.", True),
               th("YoY", "YoY", "Ocak - Ağustos 2026 / 2025.", "January - August 2026 / 2025.", True),
               th("2023'ten bu yana", "Since 2023", "Ocak - Ağustos 2026 / 2023.", "January - August 2026 / 2023.", True),
               th("Örnek aramalar", "Example searches", "Sınıfta en çok aranan ifadeler.", "The most searched phrases in the class.")],
              [[x(nm, N_EN.get(nm, nm)), cellk(v_["o2026"]), n(yzd(100 * v_["o2026"] / _NT)), n(_yz(_oran(v_["o2026"], v_["o2025"]))), n(_yz(_oran(v_["o2026"], v_["o2023"]))),
                '<div class="kwlist">%s</div>' % "".join('<span class="kw">%s</span>' % veri_m(q) for q in _ORN.get(nm, []))]
               for nm, v_ in sorted(NV.items(), key=lambda i_: -i_[1]["o2026"])])
_TOPV = tablo([th("Arama ifadesi", "Search phrase", "Google'a yazılan ifade.", "The phrase typed into Google."),
               th("Ana kategori", "Main category", "Kategori ağacındaki karşılığı.", "Its place in the category tree."),
               th("İhtiyaç sınıfı", "Need class", "İfadenin taşıdığı ihtiyaç.", "The need the phrase carries."),
               th("Oca-Ağu 2026 ort.", "Jan-Aug 2026 avg.", "Ocak - Ağustos 2026 aylık ortalama arama.", "Average monthly searches, January - August 2026.", True),
               th("YoY", "YoY", "Ocak - Ağustos 2026 / 2025.", "January - August 2026 / 2025.", True),
               th("2023'ten bu yana", "Since 2023", "Ocak - Ağustos 2026 / 2023.", "January - August 2026 / 2023.", True)],
              [[kw(r_["kw"]), x(r_["k1"], KAT_EN.get(r_["k1"], r_["k1"])), x(r_["niyet"], N_EN.get(r_["niyet"], r_["niyet"])), cellk(r_["o2026"]), n(_yz(_oran(r_["o2026"], r_["o2025"]))), n(_yz(_oran(r_["o2026"], r_["o2023"])))]
               for r_ in O["vitra_kw"][:60]], "uzun")
_POPV, _DIAV = pop("\"vitra\" ile en çok yapılan 60 arama", "The 60 most frequent searches with \"vitra\"", _TOPV, "60 aramayı gör", "See the 60 searches")

# ---------------------------------------------------------------- metin
_V = M["VitrA"]; _A = M["Artema"]
_ARM = sorted([(_pay(m_, "Armatürler"), m_) for m_ in M if m_ + "|Armatürler" in MK], reverse=True)
_K1V = {k1: _pay("VitrA", k1) for k1 in K1}
_LID = {k1: max(((_pay(m_, k1), m_) for m_ in M if m_ + "|" + k1 in MK)) for k1 in K1}
_BUY = sorted([(M[m_]["uc"], m_) for m_ in M if M[m_]["o2023"] >= 5000 and m_ != "VitrA"], reverse=True)
_GER = sorted([(M[m_]["uc"], m_) for m_ in M if M[m_]["o2023"] >= 5000 and m_ != "VitrA"])
assert _ARM[0][1] == "E.C.A." and _LID["Banyo Mobilyaları"][1] == "VitrA" and _VS == 1, "marka metni veriyle uyuşmuyor"
KPI = (kpi_kart(k(_V["o2026"]), "\"vitra\" + kategori aramaları · aylık ortalama, Oca-Ağu 2026; 2023'ten bu yana %s" % yzd(_V["uc"]).replace("%", "+%"), "\"vitra\" + category searches · monthly average, Jan-Aug 2026; %s since 2023" % _pe(_V["uc"]), "hi")
       + kpi_kart(yzd(100 * _V["o2026"] / TOP26), "VitrA'nın %d üretici marka içindeki marka + kategori arama payı · VitrA ve Artema birlikte %s" % (len(M), yzd(100 * (_V["o2026"] + _A["o2026"]) / TOP26)),
                  "VitrA's share of brand + category searches among %d manufacturer brands · VitrA and Artema together %s" % (len(M), ("%.1f" % (100 * (_V["o2026"] + _A["o2026"]) / TOP26)) + "%"))
       + kpi_kart(yzd(_K1V["Armatürler"]), "VitrA'nın armatür marka aramalarındaki payı · E.C.A. %s, Artema %s" % (yzd(_ARM[0][0]), yzd(_pay("Artema", "Armatürler"))), "VitrA's share of tap brand searches · E.C.A. %s, Artema %s" % (("%.1f" % _ARM[0][0]) + "%", ("%.1f" % _pay("Artema", "Armatürler")) + "%"), "dn")
       + kpi_kart(k(YAL["vitra"]["o2026"]), "\"vitra\" yalın marka araması · aylık ortalama, Oca-Ağu 2026; 2023'ten bu yana %s" % yzd(YAL["vitra"]["uc"]).replace("%", "+%"), "\"vitra\" brand-name search · monthly average, Jan-Aug 2026; %s since 2023" % _pe(YAL["vitra"]["uc"])))

def _p(v): return yzd(v)
INS_YAL = insight(("Marka dışı anlamları da bulunan \"kale\" dışarıda tutulduğunda **VitrA, adıyla en çok aranan üretici markadır** (aylık %s); bu arama 2023'ten bu yana %s düzeyinde yatay seyretmektedir. Rakipler arasında Creavit (%s), Geberit (%s) ve Isvea (düşük tabandan %s) adıyla yapılan aramalarını büyütmüştür. Perakende tarafında Trendyol (%s) ve Hepsiburada (%s) 2023'e göre gerilerken IKEA (%s), Koçtaş (%s) ve Bauhaus (%s) büyümektedir. \"kale\" kelimesi marka dışı anlamlar da taşıdığından hacmi Kale markası için üst sınır olarak okunmalıdır; marka için \"kale seramik\" ve \"kalebodur\" satırları daha doğru bir göstergedir.")
                  % (k(YAL["vitra"]["o2026"]), yz(YAL["vitra"]["uc"]), yz(YAL["creavit"]["uc"]), yz(YAL["geberit"]["uc"]), yz(YAL["isvea"]["uc"]), yz(YAL["trendyol"]["uc"]), yz(YAL["hepsiburada"]["uc"]), yz(YAL["ikea"]["uc"]), yz(YAL["koçtaş"]["uc"]), yz(YAL["bauhaus"]["uc"])),
                  ("Leaving out \"kale\", which also has non-brand meanings, **VitrA is the manufacturer brand searched most by name** (%s a month); this search has been flat since 2023 at %s. Among competitors, Creavit (%s), Geberit (%s) and Isvea (%s from a low base) have grown their brand-name searches. On the retail side Trendyol (%s) and Hepsiburada (%s) are below 2023 while IKEA (%s), Koçtaş (%s) and Bauhaus (%s) are growing. As \"kale\" also carries non-brand meanings, its volume should be read as an upper bound for the Kale brand; \"kale seramik\" and \"kalebodur\" are better indicators for the brand.")
                  % (k(YAL["vitra"]["o2026"]), yz(YAL["vitra"]["uc"]), yz(YAL["creavit"]["uc"]), yz(YAL["geberit"]["uc"]), yz(YAL["isvea"]["uc"]), yz(YAL["trendyol"]["uc"]), yz(YAL["hepsiburada"]["uc"]), yz(YAL["ikea"]["uc"]), yz(YAL["koçtaş"]["uc"]), yz(YAL["bauhaus"]["uc"])), "D43")
_GUC = [k1 for k1 in ("Vitrifiyeler", "Rezervuarlar", "Banyo Mobilyaları", "Karo Seramik Ürünleri")]
INS_ISI = insight(("**Marka + kategori aramalarının %s'i VitrA'ya aittir** (Artema ile birlikte %s). VitrA; vitrifiye (%s), rezervuar (%s), banyo mobilyası (%s) ve karoda (%s) en çok aranan markadır. **Armatürde ise E.C.A. (%s) ve Artema (%s) öndedir, VitrA %s'te kalmaktadır**; duşta Artema, E.C.A. ve VitrA birbirine yakındır. Banyo mobilyasında Orka (%s), yıkanma alanlarında Durul (%s) VitrA'nın en yakın rakibidir. 2023'ten bu yana büyük rakipler içinde en çok büyüyen %s (%s), en çok gerileyen %s (%s) olmuştur.")
                  % (_p(100 * _V["o2026"] / TOP26), _p(100 * (_V["o2026"] + _A["o2026"]) / TOP26), _p(_K1V["Vitrifiyeler"]), _p(_K1V["Rezervuarlar"]), _p(_K1V["Banyo Mobilyaları"]), _p(_K1V["Karo Seramik Ürünleri"]),
                     _p(_ARM[0][0]), _p(_pay("Artema", "Armatürler")), _p(_K1V["Armatürler"]), _p(_pay("Orka", "Banyo Mobilyaları")), _p(_pay("Durul", "Yıkanma Alanları")), _BUY[0][1], yz(_BUY[0][0]), _GER[0][1], yz(_GER[0][0])),
                  ("**VitrA accounts for %s of brand + category searches** (%s together with Artema). VitrA is the most searched brand in sanitaryware (%s), cisterns (%s), bathroom furniture (%s) and tiles (%s). **In taps and mixers, however, E.C.A. (%s) and Artema (%s) lead while VitrA stays at %s**; in showers Artema, E.C.A. and VitrA are close. Orka (%s) in bathroom furniture and Durul (%s) in bathing areas are VitrA's closest competitors. Since 2023, the fastest-growing large competitor has been %s (%s) and the one with the steepest decline %s (%s).")
                  % (_p(100 * _V["o2026"] / TOP26), _p(100 * (_V["o2026"] + _A["o2026"]) / TOP26), _p(_K1V["Vitrifiyeler"]), _p(_K1V["Rezervuarlar"]), _p(_K1V["Banyo Mobilyaları"]), _p(_K1V["Karo Seramik Ürünleri"]),
                     _p(_ARM[0][0]), _p(_pay("Artema", "Armatürler")), _p(_K1V["Armatürler"]), _p(_pay("Orka", "Banyo Mobilyaları")), _p(_pay("Durul", "Yıkanma Alanları")), _BUY[0][1], yz(_BUY[0][0]), _GER[0][1], yz(_GER[0][0])), "D43")
_VA = MK["VitrA|Armatürler"]; _VR = MK["VitrA|Rezervuarlar"]; _VV = MK["VitrA|Vitrifiyeler"]; _VB = MK["VitrA|Banyo Mobilyaları"]; _VY = MK["VitrA|Yıkanma Alanları"]
INS_VIT = insight(("**\"vitra\" + kategori aramaları 2023'ten bu yana %s artmış, son yılda yatay seyretmiştir (%s)**; aynı dönemde kategori adıyla yapılan genel aramalar %s daralmıştır (Bölüm [[b:talep]]). Artış armatür (%s), rezervuar (%s) ve vitrifiyede (%s) toplanmaktadır; banyo mobilyası (%s) ve yıkanma alanlarında (%s) marka aramaları gerilemiştir. Marka talebinin kategori talebine göre daha dayanıklı olması, mevcut ürün sahibinin ve markayı bilen kullanıcının aramaya devam ettiğine işaret etmektedir.")
                  % (yz(_V["uc"]), yz(_V["yoy"]), yz(A["toplam"]["a26"] / A["toplam"]["a25"] * 100 - 100), yz(_VA["uc"]), yz(_VR["uc"]), yz(_VV["uc"]), yz(_VB["uc"]), yz(_VY["uc"])),
                  ("**\"vitra\" + category searches have risen %s since 2023 and were flat over the last year (%s)**; in the same period generic searches with the category name contracted %s (Section [[b:talep]]). The rise is concentrated in taps (%s), cisterns (%s) and sanitaryware (%s); brand searches declined in bathroom furniture (%s) and bathing areas (%s). Brand demand being more resilient than category demand indicates that existing product owners and users who know the brand keep searching.")
                  % (yz(_V["uc"]), yz(_V["yoy"]), yz(A["toplam"]["a26"] / A["toplam"]["a25"] * 100 - 100), yz(_VA["uc"]), yz(_VR["uc"]), yz(_VV["uc"]), yz(_VB["uc"]), yz(_VY["uc"])), "D43", "D1")
_NJ = NV.get("Jenerik ürün", {"o2026": 0}); _NTB = NV["Tamir ve bakım"]; _NTF = NV["Tasarım ve fikir"]; _NF = NV["Fiyat"]
INS_NIY = insight(("\"vitra\" ile yapılan aramaların %s'i yalnızca ürün adıyla yapılmaktadır (\"vitra klozet\", \"vitra gömme rezervuar\"). İhtiyacı belirgin aramalarda **tamir ve bakım ifadeleri** (iç takım, klozet kapağı menteşesi) 2023'ten bu yana %s, **tasarım ve model aramaları** %s artmış, fiyat aramaları ise %s değişmiştir. Bu tablo, Google önerilerinde ve Şikayetvar'da görülen yedek parça ilgisiyle (Bölüm [[b:sikayet]]) tutarlıdır: markayı arayan kullanıcının önemli bir kısmı mevcut ürünün parçası için aramaktadır.")
                  % (yzd(100 * _NJ["o2026"] / _NT), yz(_oran(_NTB["o2026"], _NTB["o2023"])), yz(_oran(_NTF["o2026"], _NTF["o2023"])), yz(_oran(_NF["o2026"], _NF["o2023"]))),
                  ("%s of searches with \"vitra\" use only the product name (\"vitra klozet\", \"vitra gömme rezervuar\"). Among searches with a clear need, **repair and maintenance phrases** (inner mechanism, WC seat hinge) have grown %s since 2023 and **design and model searches** %s, while price searches changed %s. This is consistent with the spare-part interest seen in Google suggestions and on Şikayetvar (Section [[b:sikayet]]): a significant part of the users searching for the brand are looking for a part of a product they already own.")
                  % (yzd(100 * _NJ["o2026"] / _NT), yz(_oran(_NTB["o2026"], _NTB["o2023"])), yz(_oran(_NTF["o2026"], _NTF["o2023"])), yz(_oran(_NF["o2026"], _NF["o2023"]))), "D43")

BLOK = """
<div class="kpis">%s</div>
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
<p class="popl">%s</p>
%s
%s
""" % (KPI,
       x("Marka adıyla yapılan aramalar: üreticiler ve perakendeciler", "Searches by brand name: manufacturers and retailers"), T_YAL, INS_YAL,
       x("Marka + kategori aramaları: markaların kategori bazında aranma hacmi", "Brand + category searches: search volume of brands by category"), T_ISI, INS_ISI,
       x("\"vitra\" + kategori aramaları: yıllar ve kategoriler", "\"vitra\" + category searches: years and categories"), G_MARKA, T_VIT, INS_VIT,
       x("\"vitra\" ile birlikte aranan ifadeler: ihtiyaç sınıfları", "Phrases searched with \"vitra\": need classes"), _POPV, T_NIY, INS_NIY)
BLOK += kaynak("Google Ads Keyword Planner · marka adı ve marka + kategori aramaları · %d üretici marka ve 10 perakendeci · \"vitra\" için %s ifade, rakipler için %d kategori ifadesi · Türkiye, Türkçe · aylık hacim Eyl 2022 - Ağu 2026 · 04.10.2026" % (len(M), bin(O["kok_sayisi"]["vitra"]), O["kok_sayisi"]["rakip_kok"]),
                "Google Ads Keyword Planner · brand-name and brand + category searches · %d manufacturer brands and 10 retailers · %s phrases for \"vitra\", %d category phrases for competitors · Turkey, Turkish · monthly volume Sep 2022 - Aug 2026 · 04.10.2026" % (len(M), f"{O['kok_sayisi']['vitra']:,}", O["kok_sayisi"]["rakip_kok"]), "D43")
DIALOG = _DIAV
