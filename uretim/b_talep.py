# -*- coding: utf-8 -*-
"""Bolum: Kategori talebi ve donemsel degisim (Keyword Planner, 2.342 kelime)."""
from ortak import *
from rapor_parca1 import T, cizgi, barlar
import veri
K1 = A["k1"]; K2 = A["k2"]; TOP = A["toplam"]; AYK = A["aylik_k1"]
KAT_EN = {"Banyo Mobilyaları": "Bathroom Furniture", "Vitrifiyeler": "Sanitaryware", "Armatürler": "Taps and Mixers", "Yıkanma Alanları": "Bathing Areas",
          "Karo Seramik Ürünleri": "Ceramic Tiles", "Banyo Aksesuarları": "Bathroom Accessories", "Duşlar": "Showers", "Rezervuarlar": "Cisterns", "Toplam": "Total"}
K2_EN = {"Balkon, Teras & Bahçe Karo Seramikleri": "Balcony, Terrace & Garden Tiles", "Duşlar": "Showers", "Banyo Karo Seramikleri": "Bathroom Tiles", "Ankastre Duş Yönlendiriciler": "Concealed Shower Diverters",
         "Banyo Mobilyaları": "Bathroom Furniture", "Klozetler": "WCs", "Banyo Tezgahları": "Bathroom Countertops", "Duş Kanalları": "Shower Channels", "Duş Tekneleri": "Shower Trays",
         "Armatür Tamamlayıcı Ürünleri": "Tap Accessories", "Tuvalet Fırçaları": "Toilet Brushes", "Duvar Karoları": "Wall Tiles", "Lavabo Dolapları": "Washbasin Units", "Banyo Aksesuar Setleri": "Bathroom Accessory Sets",
         "Bideler": "Bidets", "Banyo Aynaları": "Bathroom Mirrors", "Banyo Aksesuarları": "Bathroom Accessories", "Banyo Set Modülleri": "Bathroom Set Modules", "Tuvalet Kağıtlıkları": "Toilet Roll Holders",
         "Banyo Mobilya Tamamlayıcıları": "Bathroom Furniture Add-ons", "Duş Başlıkları": "Shower Heads", "Duş Tamamlayıcı Ürünleri": "Shower Accessories", "Banyo Dolapları": "Bathroom Cabinets", "Duş Setleri": "Shower Sets",
         "Lavabolar": "Washbasins", "Klozet Kapakları": "Toilet Seats", "Gömme Rezervuarlar": "Concealed Cisterns", "Duşakabin": "Shower enclosure", "Küvetler": "Bathtubs", "Eviye Bataryaları": "Kitchen Taps",
         "Lavabo Bataryaları": "Basin Taps", "Banyo Bataryaları": "Bath Taps", "Ev İçi Zemin Karo Seramikleri": "Indoor Floor Tiles", "Porselen Karolar": "Porcelain Tiles", "Yer Karoları": "Floor Tiles",
         "Musluk ve Ara Musluklar": "Taps and Stop Valves", "Rezervuar Kumanda Panelleri": "Flush Plates", "Akıllı Klozet": "Smart WC", "Havluluklar": "Towel Rails", "Sabunluklar": "Soap Dispensers",
         "El Duşu Takımları": "Hand Shower Sets", "Bataryalı Duş Sistemleri": "Shower Systems with Mixer", "Duş Kolonları": "Shower Columns", "Pisuvarlar": "Urinals", "Eviyeler": "Kitchen Sinks",
         "Vitrifiye Tamamlayıcıları": "Sanitaryware Accessories", "Mutfak Karo Seramikleri": "Kitchen Tiles", "Havuz Karo Seramikleri": "Pool Tiles", "Ticari & Endüstriyel Alan Karo Seramikleri": "Commercial & Industrial Tiles",
         "Karo Seramik Ürünleri": "Ceramic Tiles", "Gömme Rezervuar Montaj Aksesuarları": "Concealed Cistern Fitting Accessories", "Gömme Rezervuar Setleri": "Concealed Cistern Sets", "Taşıyıcı Aparatlar": "Support Frames",
         "Vitrifiyeler": "Sanitaryware", "Duş Üniteleri": "Shower Units", "Yıkanma Alanları": "Bathing Areas", "Yıkanma Alanı Tamamlayıcı Ürünler": "Bathing Area Accessories", "Armatürler": "Taps and Mixers",
         "Bide Bataryaları": "Bidet Taps", "Banyo Askıları": "Bathroom Hooks", "Banyo Çöp Kovaları": "Bathroom Bins", "Diğer Banyo Aksesuarları": "Other Bathroom Accessories", "Diş Fırçalıkları": "Toothbrush Holders",
         "Masajlı Duş Sistemleri": "Massage Shower Systems", "Sürgülü El Duşu Takımları": "Sliding Hand Shower Sets"}
K2_EN.update({'Akıllı Klozet Seti': 'Smart WC Sets', 'Akıllı Kumanda Panelleri': 'Smart Flush Plates', 'Ankastre Bataryalar': 'Concealed Mixers', 'Ankastre Lavabo Bataryaları': 'Concealed Basin Mixers', 'Ankastre Stop Valfler': 'Concealed Stop Valves', 'Asma Klozet Takımları': 'Wall-hung WC Sets', 'Asma Klozetler': 'Wall-hung WCs', 'Asma Klozetler için Gömme Rezervuarlar': 'Concealed Cisterns for Wall-hung WCs', 'Aynalı Banyo Dolabı': 'Mirror Cabinets', 'Banyo Batarya Çıkış Uçları': 'Bath Spouts', 'Banyo Dolabı Kulpları': 'Cabinet Handles', 'Banyo Dolap Ayakları': 'Cabinet Feet', 'Banyo Konsolları': 'Bathroom Consoles', 'Banyo Malzemelikleri': 'Bathroom Caddies', 'Banyo Rafları': 'Bathroom Shelves', 'Banyo Tutunma Barları': 'Grab Bars', 'Duvar Önü Rezervuarlar': 'Exposed Cisterns', 'Duvardan Banyo Bataryaları': 'Wall-mounted Bath Mixers', 'Duş Dirsekleri': 'Shower Elbows', 'Duş Teknesi Panelleri': 'Shower Tray Panels', 'Duş Teknesi ve Küvet Ayakları': 'Shower Tray and Bathtub Feet', 'Düz Aynalar': 'Flat Mirrors', 'Etajerli Lavabolar': 'Washbasins with Shelf', 'Hidromasajlı Bağımsız Küvetler': 'Freestanding Whirlpool Baths', 'Hidromasajlı Standart Küvetler': 'Standard Whirlpool Baths', 'Hidromasajsız Bağımsız Küvetler': 'Freestanding Baths', 'Küvet Bataryaları': 'Bath Mixers', 'Küvet Panelleri': 'Bath Panels', 'Lavabo Sifon ve Süzgeçleri': 'Basin Siphons and Wastes', 'Makyaj Aynaları ve Diğer Aksesuarlar': 'Make-up Mirrors and Other Accessories', 'Monoblok Lavabolar': 'Monoblock Washbasins', 'Pisuvar Ara Bölmeleri': 'Urinal Dividers', 'Pisuvar Yıkama Sistemleri': 'Urinal Flush Systems', 'Rezervuar ve Klozet İç Takımları': 'Cistern and WC Inner Mechanisms', 'Sifonlar': 'Siphons', 'Standart Lavabo ve Ayakları': 'Standard Washbasins and Pedestals', 'Standart ve Gömme Küvetler': 'Standard and Built-in Baths', 'Sıva Altı ve Diğer Tamamlayıcılar': 'Concealed Bodies and Other Accessories', 'Taharet El Duşları': 'Bidet Hand Sprays', 'Takım Klozetler': 'Close-coupled WCs', 'Tek Armatür Delikli Lavabo Bataryaları': 'Single-hole Basin Mixers', 'Temassız Lavabo Bataryaları': 'Touchless Basin Mixers', 'Termostatik Bataryalar': 'Thermostatic Mixers', 'Tezgahaltı Lavabolar': 'Under-counter Washbasins', 'Tezgahüstü Lavabolar': 'Countertop Washbasins', 'Tuvalet Taşları için Gömme Rezervuarlar': 'Concealed Cisterns for Squat Toilets', 'VitrA Kaydırmaz': 'VitrA Anti-slip', 'Yarım Tezgah Lavabolar': 'Semi-recessed Washbasins', 'Yerden Tek Klozetler': 'Floor-standing WCs', 'Çamaşır Makinesi Dolapları': 'Washing Machine Cabinets', 'Çanak Lavabo Bataryaları': 'Bowl Basin Mixers', 'Çanak Lavabolar': 'Bowl Washbasins', 'İki veya Üç Delikli Lavabo Bataryaları': 'Two or Three-hole Basin Mixers'})
def kat(k): return x(k, KAT_EN.get(k, k))
def kat2(k): return x(k, K2_EN.get(k, k))

def _kw_pop(filt, baslik_tr, baslik_en, ek_sutun=("Alt kategori", "Sub-category", "k2")):
    lst = sorted([r for r in veri.KELIME if filt(r)], key=lambda r: -(r["a26"] or 0))[:50]
    rows_ = []
    for r in lst:
        yoy_ = ((r["a26"] / r["a25"] - 1) * 100) if r.get("a25") else None
        ek = r.get(ek_sutun[2]) or "-"
        rows_.append([kw(r["kw"]), x(ek, K2_EN.get(ek, KAT_EN.get(ek, ek))) if ek != "-" else n("-"), cellk(r["a25"] or 0), cellk(r["a26"] or 0), n(yz(yoy_)) if yoy_ is not None else n("-")])
    t_ = tablo([th("Arama kelimesi", "Search keyword", "Kategorideki kelime; 2026 aylık ortalamaya göre ilk 50.", "Keyword in the category; top 50 by 2026 monthly average."),
                th(ek_sutun[0], ek_sutun[1], "Kelimenin bağlı olduğu grup.", "Group the keyword belongs to."),
                th("2025 aylık ort.", "2025 monthly avg.", "Ocak - Ağustos 2025 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2025.", True),
                th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2026.", True),
                th("YoY", "YoY", "2026 / 2025 aynı aylar yüzde değişimi.", "Percentage change, 2026 / 2025 same months.", True)], rows_, "uzun")
    return pop(baslik_tr, baslik_en, t_, ikon=True)
_TDIA = []
def katp(k_):
    b_, d_ = _kw_pop(lambda r: r["k1"] == k_, "%s: en yüksek hacimli 50 kelime" % k_, "%s: top 50 keywords by volume" % KAT_EN.get(k_, k_))
    _TDIA.append(d_); return kat(k_) + b_
toplam_yoy = (TOP["a26"] / TOP["a25"] - 1) * 100
sira = sorted(K1, key=lambda k: -K1[k]["a26"])
RENK = {"Banyo Mobilyaları": "#E85F36", "Vitrifiyeler": "#10332F", "Armatürler": "#2E7D32", "Yıkanma Alanları": "#F5A623", "Karo Seramik Ürünleri": "#7A8C89", "Banyo Aksesuarları": "#B96BC2", "Duşlar": "#4A90D9", "Rezervuarlar": "#8B5A2B"}
GRAFIK = cizgi([(kat("Toplam"), "#E85F36", AYK["Toplam"])] , y_etiket=x("Aylık arama hacmi · 2.342 kelime toplamı", "Monthly search volume · total of 2,342 keywords"), aylar=veri.AYLAR)
GRAFIK_K = cizgi([(kat(k), RENK[k], AYK[k]) for k in sira[:5]], y_etiket=x("Aylık arama hacmi · en büyük 5 kategori", "Monthly search volume · five largest categories"), aylar=veri.AYLAR)

# --- yil yil gorunum (Oca-Ara, 2023-2026) ---
import json as _json, os as _os
TY_ = _json.load(open(_os.path.join(veri.V, "islenmis", "talep_yillik.json"), encoding="utf-8"))
AYA = [("Oca", "Jan"), ("Şub", "Feb"), ("Mar", "Mar"), ("Nis", "Apr"), ("May", "May"), ("Haz", "Jun"), ("Tem", "Jul"), ("Ağu", "Aug"), ("Eyl", "Sep"), ("Eki", "Oct"), ("Kas", "Nov"), ("Ara", "Dec")]
for _a, _b in AYA: x(_a, _b)
for _y in ("2023", "2024", "2025", "2026"): x(_y, _y)
x("YoY değişim", "YoY change")
YRENK = {"2023": "#9AA8A5", "2024": "#F5A623", "2025": "#10332F", "2026": "#E85F36"}
def yil_grafik(kk, etiket_tr, etiket_en):
    d = TY_["kategori"][kk]
    return cizgi([(str(y), YRENK[str(y)], d[str(y)]) for y in TY_["yillar"]], y_etiket=x(etiket_tr, etiket_en),
                 aylar=[a for a, _ in AYA], x_etiket=[a for a, _ in AYA], kalin={3: 3.2})

# --- aylik seri Oca 2023 - Ağu 2026, yillara gore renkli, peak/base notlu ---
AY23 = ["%d-%02d" % (y_, m_) for y_ in TY_["yillar"] for m_ in range(1, 13)]
def _uzun(kk):
    d = TY_["kategori"][kk]; return [v for y_ in TY_["yillar"] for v in d[str(y_)]]
_son = max(i for i, v in enumerate(_uzun("Toplam")) if v is not None)
AY23 = AY23[:_son + 1]
x("peak", "peak"); x("base", "base")
def _kisa(v):
    r = k(v); x(r, r.replace(",", ".")); return r
_ys, _nt = [], []
for _j, _y in enumerate(TY_["yillar"]):
    _d = TY_["kategori"]["Toplam"][str(_y)]
    _s = [None] * len(AY23)
    for _m, _v in enumerate(_d):
        _i = _j * 12 + _m
        if _v is not None and _i < len(AY23): _s[_i] = _v
    _ys.append((str(_y), YRENK[str(_y)], _s))
    _ix = [i for i, v in enumerate(_s) if v is not None]
    _p = max(_ix, key=lambda i: _s[i]); _b = min(_ix, key=lambda i: _s[i])
    for _i2, _tur, _yer in ((_p, "peak", "ust"), (_b, "base", "alt")):
        _r = k(_s[_i2]); _nt.append((_j, _i2, x("%s %s" % (_r, _tur), "%s %s" % (_r.replace(",", "."), _tur)), _yer))
GRAFIK = cizgi(_ys, yukseklik=270, y_etiket=x("Aylık arama hacmi · 2.342 kelime toplamı · yıllara göre renkli (peak: yılın en yüksek ayı, base: en düşük ayı)", "Monthly search volume · total of 2,342 keywords · coloured by year (peak: highest month of the year, base: lowest month)"), aylar=AY23, notlar=_nt, bagla=True)
GRAFIK_K = cizgi([(kat(k_), RENK[k_], [None if v is None else v for v in _uzun(k_)][:len(AY23)]) for k_ in sira[:5]], y_etiket=x("Aylık arama hacmi · en büyük 5 kategori", "Monthly search volume · five largest categories"), aylar=AY23)
_AYF = [(b_ / a_ - 1) * 100 for a_, b_ in zip(TY_["kategori"]["Toplam"]["2025"][:8], TY_["kategori"]["Toplam"]["2026"][:8])]
_SEKME_NO = [0]
def sekmeler(parcalar, sinif=""):
    """parcalar: [(tr, en, html)] -> .tabs dugmeleri + paneller (ilk acik)."""
    _SEKME_NO[0] += 1; n_ = _SEKME_NO[0]
    b = "".join('<button type="button" role="tab" id="tt%d-%d" aria-controls="tp%d-%d" aria-selected="%s">%s</button>' % (n_, i_, n_, i_, "true" if i_ == 0 else "false", x(tr, en)) for i_, (tr, en, _) in enumerate(parcalar))
    p_ = "".join('<div role="tabpanel" id="tp%d-%d" aria-labelledby="tt%d-%d"%s>%s</div>' % (n_, i_, n_, i_, "" if i_ == 0 else " hidden", h) for i_, (_, _, h) in enumerate(parcalar))
    return '<div class="tabs %s" role="tablist">%s</div>%s' % (sinif, b, p_)
GRAFIK = sekmeler([("Aylık seri · Oca 2023 - Ağu 2026", "Monthly series · Jan 2023 - Aug 2026", GRAFIK),
                   ("Yıl yıl · 2023 - 2026", "Year on year · 2023 - 2026", yil_grafik("Toplam", "Aylık arama hacmi · 2.342 kelime toplamı, yıllar üst üste (2026: Oca - Ağu)", "Monthly search volume · total of 2,342 keywords, years overlaid (2026: Jan - Aug)"))], "gtabs")
_YK = sekmeler([(kk, KAT_EN.get(kk, kk), yil_grafik(kk, "Aylık arama hacmi · %s, yıllar üst üste" % kk, "Monthly search volume · %s, years overlaid" % KAT_EN.get(kk, kk))) for kk in sira], "gtabs ic")
GRAFIK_K = sekmeler([("Aylık seri · en büyük 5 kategori", "Monthly series · five largest categories", GRAFIK_K),
                     ("Yıl yıl · kategori seçimi", "Year on year · choose a category", _YK)], "gtabs")
BAR = barlar([(_q, K1[_q]["yoy"], "#2E7D32" if K1[_q]["yoy"] > 0 else "#D32F2F") for _q in sorted(K1, key=lambda q: -K1[q]["yoy"])])
for _kk in K1: kat(_kk)
tbl = tablo([th("Kategori", "Category", "VitrA kategori ağacındaki ana kategori; 2.342 kelime 8 ana kategoriye dağıtılmıştır. Ok simgesi kategorideki en yüksek hacimli 50 kelimeyi açar.", "Main category in the VitrA category tree; 2,342 keywords are distributed across 8 main categories. The arrow icon opens the 50 highest-volume keywords in the category."),
             th("Kelime", "Keywords", "Kategoriye atanan kelime sayısı.", "Number of keywords assigned to the category.", True),
             th("2025 aylık ort.", "2025 monthly avg.", "Ocak - Ağustos 2025 aylık ortalama arama hacmi (kategorideki kelimelerin toplamı, aya bölünmüş), Google Keyword Planner, Türkiye.", "Average monthly search volume for January - August 2025 (sum of the category's keywords, divided by months), Google Keyword Planner, Turkey.", True),
             th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi; aynı takvim aylarını kapsar.", "Average monthly search volume for January - August 2026; covers the same calendar months.", True),
             th("YoY", "YoY", "İki pencere arasındaki yüzde değişim; aynı takvim ayları karşılaştırılmıştır.", "Percentage change between the two windows; the same calendar months are compared.", True),
             th("Pay", "Share", "Kategorinin 2026 penceresindeki toplam hacim içindeki payı.", "The category's share of total volume in the 2026 window.", True)],
            [[katp(k), cell(K1[k]["n"]), cellk(K1[k]["a25"]), cellk(K1[k]["a26"]), n(yz(K1[k]["yoy"])), n(yzd(100 * K1[k]["a26"] / TOP["a26"]))] for k in sira] +
            [["<b>%s</b>" % kat("Toplam"), n("<b>%s</b>" % bin(TOP["n"])), cellk(TOP["a25"]), cellk(TOP["a26"]), n(yz(toplam_yoy)), n("%100")]])
def k2rows(liste):
    out = []
    for key, a26, yoy in liste:
        k1, k2 = key.split("|"); v = K2[key]
        b_, d_ = _kw_pop(lambda r, k1=k1, k2=k2: r["k1"] == k1 and r["k2"] == k2, "%s: en yüksek hacimli kelimeler" % k2, "%s: top keywords by volume" % K2_EN.get(k2, k2), ("Alt-alt kategori", "Sub-sub-category", "k3"))
        _TDIA.append(d_)
        out.append([kat(k1), kat2(k2) + b_, cell(v["n"]), cellk(v["a25"]), cellk(a26), n(yz(yoy))])
    return out
bas2 = [th("Ana kategori", "Main category", "Alt kategorinin bağlı olduğu ana kategori.", "Main category the sub-category belongs to."),
        th("Alt kategori", "Sub-category", "VitrA kategori ağacındaki alt kategori.", "Sub-category in the VitrA category tree."),
        th("Kelime", "Keywords", "Alt kategoriye atanan kelime sayısı.", "Number of keywords assigned to the sub-category.", True),
        th("2025 aylık ort.", "2025 monthly avg.", "Ocak - Ağustos 2025 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2025.", True),
        th("2026 aylık ort.", "2026 monthly avg.", "Ocak - Ağustos 2026 aylık ortalama arama hacmi.", "Average monthly search volume, January - August 2026.", True),
        th("YoY", "YoY", "İki pencere arasındaki yüzde değişim. Tabloya aylık 3.000 ve üzeri hacimli alt kategoriler alınmıştır.", "Percentage change between the two windows. Sub-categories with monthly volume of 3,000 and above are listed.", True)]
from grafik2 import sapma as _sapma, f_k as _fk
_YD = sorted(A["k2_yukselen"] + A["k2_dusen"], key=lambda r: -r[2])
SAPMA = _sapma([(kat2(r[0].split("|")[1]), r[2]) for r in _YD], x("YoY değişim", "YoY change"),
               x("Alt kategori talebinde YoY değişim · Oca-Ağu 2026 / Oca-Ağu 2025, aylık 3.000 ve üzeri hacimli alt kategoriler", "YoY change in sub-category demand · Jan-Aug 2026 / Jan-Aug 2025, sub-categories with monthly volume of 3,000 and above"),
               ek=[(x("2026 aylık ort.", "2026 monthly avg."), [_fk(r[1]) for r in _YD])])
kloz = K2["Vitrifiyeler|Klozetler"]; bm = K1["Banyo Mobilyaları"]; ld = K2["Banyo Mobilyaları|Lavabo Dolapları"]; bk = K2["Karo Seramik Ürünleri|Banyo Karo Seramikleri"]
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<div class="two">
<div><h3>%s</h3>%s</div>
<div><h3>%s</h3>%s</div>
</div>
%s
%s
""" % (
 x("Talep tabanı, VitrA kategori ağacına eşlenmiş 2.342 tekil arama kelimesidir; Keyword Planner'ın aynı aylık hacmi verdiği yakın yazım varyantları (ör. \"banyo dolabı\", \"banyo dolap\", \"banyo dolapları\") tek kelime olarak sayılmıştır. Hacimler Google Keyword Planner'dan Ocak 2023 - Ağustos 2026 dönemi için aylık olarak alınmıştır; yıllık karşılaştırma aynı takvim aylarını kapsayan Ocak - Ağustos pencereleri üzerinden yapılmaktadır.",
   "The demand base is 2,342 unique search keywords mapped to the VitrA category tree; close spelling variants to which Keyword Planner assigns the same monthly volume (e.g. \"banyo dolabı\", \"banyo dolap\", \"banyo dolapları\") are counted as one keyword. Volumes were taken monthly from Google Keyword Planner for January 2023 - August 2026; the year-on-year comparison uses January - August windows covering the same calendar months."),
 kpi_kart(k(TOP["a26"]), "Aylık ortalama arama · 2026 (Oca-Ağu), 2.342 kelime", "Average monthly searches · 2026 (Jan-Aug), 2,342 keywords"),
 kpi_kart(yz(toplam_yoy), "Toplam talep değişimi · 2026 / 2025, aynı aylar", "Total demand change · 2026 / 2025, same months", "dn"),
 kpi_kart(yz(A["k2_yukselen"][0][2]), "%s · en hızlı büyüyen alt kategori" % A["k2_yukselen"][0][0].split("|")[1], "%s · fastest-growing sub-category" % K2_EN.get(A["k2_yukselen"][0][0].split("|")[1], A["k2_yukselen"][0][0].split("|")[1]), "up"),
 kpi_kart(yz(bm["yoy"]), "Banyo Mobilyaları · ikinci büyük kategoride daralma", "Bathroom Furniture · contraction in the second-largest category", "dn"),
 GRAFIK,
 insight("2.342 kelimenin toplam talebi 2026'nın ilk sekiz ayında bir önceki yılın aynı dönemine göre %s daralmıştır. Daralma yılın ilk iki ayında yoğunlaşmaktadır (Ocak %s, Şubat %s); Mart - Temmuz arasında aylık fark %s ile %s arasında dalgalanmakta, Ağustos'ta %s seviyesine inmektedir. Daralmanın kategori genelinde bir performans kaybından çok makro ortamla (Bölüm [[b:makro]]) uyumlu bir talep ertelemesi olduğu değerlendirilebilir." % (yz(toplam_yoy), yz(_AYF[0]), yz(_AYF[1]), yz(min(_AYF[2:7])), yz(max(_AYF[2:7])), yz(_AYF[7])),
         "Total demand for the 2,342 keywords contracted %s in the first eight months of 2026 compared with the same period a year earlier. The contraction is concentrated in the first two months (January %s, February %s); between March and July the monthly gap fluctuates between %s and %s, and in August it falls to %s. The contraction can be read as a demand deferral consistent with the macro environment (Section [[b:makro]]) rather than a category-wide loss of performance." % (yz(toplam_yoy), yz(_AYF[0]), yz(_AYF[1]), yz(min(_AYF[2:7])), yz(max(_AYF[2:7])), yz(_AYF[7])), "D1", "D11"),
 x("Ana kategori düzeyinde değişim", "Change at main category level"),
 tbl, BAR,
 x("Kategorilerin aylık seyri", "Monthly course of the categories"),
 GRAFIK_K,
 insight("Ana kategorilerde yalnızca Karo Seramik (%s) hafif artış göstermekte, Rezervuarlar (%s) yatay seyretmektedir; Vitrifiyeler (%s) daralırken en belirgin daralma Duşlar (%s), Banyo Mobilyaları (%s) ve Banyo Aksesuarlarındadır (%s). Vitrifiyeler içinde Klozetler alt kategorisi %s ile kategori ortalamasından daha az daralmıştır: klozetin, yenileme ertelense bile arıza ve değişim ihtiyacıyla talebi süren bir ürün grubu olduğu değerlendirilebilir. Banyo mobilyası ise ertelenebilir, tasarım odaklı ve yüksek sepetli bir karar olduğundan daralmanın merkezinde yer almaktadır." % (yz(K1["Karo Seramik Ürünleri"]["yoy"]), yz(K1["Rezervuarlar"]["yoy"]), yz(K1["Vitrifiyeler"]["yoy"]), yz(K1["Duşlar"]["yoy"]), yz(bm["yoy"]), yz(K1["Banyo Aksesuarları"]["yoy"]), yz(kloz["yoy"])),
         "Among the main categories only Ceramic Tiles (%s) shows a slight increase and Cisterns (%s) are flat; Sanitaryware (%s) contracts, and the sharpest contraction is in Showers (%s), Bathroom Furniture (%s) and Bathroom Accessories (%s). Within Sanitaryware the WCs sub-category contracted less than the category average at %s: the WC can be seen as a product group whose demand continues through breakdown and replacement needs even when renovation is postponed. Bathroom furniture, a deferrable, design-led and high-basket decision, sits at the centre of the contraction." % (yz(K1["Karo Seramik Ürünleri"]["yoy"]), yz(K1["Rezervuarlar"]["yoy"]), yz(K1["Vitrifiyeler"]["yoy"]), yz(K1["Duşlar"]["yoy"]), yz(bm["yoy"]), yz(K1["Banyo Aksesuarları"]["yoy"]), yz(kloz["yoy"])), "D1"),
 x("Büyüyen alt kategoriler", "Growing sub-categories"), tablo(bas2, k2rows(A["k2_yukselen"]), "dar"),
 x("Daralan alt kategoriler", "Contracting sub-categories"), tablo(bas2, k2rows(A["k2_dusen"]), "dar"),
 SAPMA + insight("Büyüyen alt kategoriler üç örüntü taşımaktadır: (1) dış mekan ve banyo karosu gibi tadilatın görünür yüzeyleri (Balkon, Teras & Bahçe Karo Seramikleri %s, Banyo Karo Seramikleri %s), (2) kategori adıyla yapılan genel aramalar (Duşlar %s, Banyo Mobilyaları %s), (3) tezgah ve duş kanalı gibi tamamlayıcı ürünler. Daralan tarafta ise Lavabo Dolapları (%s), Banyo Aynaları (%s) ve Banyo Aksesuar Setleri (%s) gibi \"mobilya ve estetik\" ürünler yer almaktadır. E-ticaret kanalı için bu ayrım, kampanya ve set kurgusunun hangi kategoride talebi yakalayabileceğine işaret etmektedir: karo ve tamamlayıcı ürün tarafında mevcut talebin karşılanması, mobilya tarafında ise talebin kampanya ve içerikle desteklenmesi değerlendirilebilir." % (yz(K2["Karo Seramik Ürünleri|Balkon, Teras & Bahçe Karo Seramikleri"]["yoy"]), yz(bk["yoy"]), yz(K2["Duşlar|Duşlar"]["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Mobilyaları"]["yoy"]), yz(ld["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Aynaları"]["yoy"]), yz(K2["Banyo Aksesuarları|Banyo Aksesuar Setleri"]["yoy"])),
         "The growing sub-categories carry three patterns: (1) the visible surfaces of a refit such as outdoor and bathroom tiles (Balcony, Terrace & Garden Tiles %s, Bathroom Tiles %s), (2) general searches made with the category name (Showers %s, Bathroom Furniture %s), (3) complementary products such as countertops and shower channels. On the contracting side sit \"furniture and aesthetics\" products such as Washbasin Units (%s), Bathroom Mirrors (%s) and Bathroom Accessory Sets (%s). For the e-commerce channel this distinction indicates where campaign and set design can capture demand: on the tile and complementary product side existing demand can be served, while on the furniture side demand can be supported through campaigns and content." % (yz(K2["Karo Seramik Ürünleri|Balkon, Teras & Bahçe Karo Seramikleri"]["yoy"]), yz(bk["yoy"]), yz(K2["Duşlar|Duşlar"]["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Mobilyaları"]["yoy"]), yz(ld["yoy"]), yz(K2["Banyo Mobilyaları|Banyo Aynaları"]["yoy"]), yz(K2["Banyo Aksesuarları|Banyo Aksesuar Setleri"]["yoy"])), "D1"),
 kaynak("Google Ads Keyword Planner · Türkiye, Türkçe · 2.342 kelime · aylık hacim Oca 2023 - Ağu 2026 · kategori eşlemesi Inbound kelime araştırması (2025)",
        "Google Ads Keyword Planner · Turkey, Turkish · 2,342 keywords · monthly volume Jan 2023 - Aug 2026 · category mapping from Inbound keyword research (2025)", "D1", "D11"),
) + "".join(_TDIA)

