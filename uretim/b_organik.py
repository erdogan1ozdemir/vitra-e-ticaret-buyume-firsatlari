# -*- coding: utf-8 -*-
"""Bolum: Organik kanal performansi (Search Console, 2. çekim 04.10.2026).
Dönemler: toplamlar, cihaz, ülke ve blog listesi 1 Eki 2025 - 30 Eyl 2026 (12 ay); aylık seri Haz 2025 - Eyl 2026;
sayfa türü, kategori ve en çok tık alan sayfalar 1 Oca - 30 Eyl 2026 (Aralık 2025'te online.vitra.com.tr adresleri www.vitra.com.tr'ye taşındığı için)."""
from ortak import *
import json as _json, os as _os, html as _h
from rapor_parca1 import cizgi
from b_talep import kat, KAT_EN, sekmeler, AYA, YRENK
from grafik2 import halka as _halka, f_k as _fk, gruplu as _gr
import gsc12 as _G12
import rehber_grup as _RG
G2 = _json.load(open(_os.path.join(veri.V, "islenmis", "gsc2.json"), encoding="utf-8"))
AY = G2["ay"]; GT = G2["tur"]; GK = G2["kat"]; GA = G2["kat_alt"]; GTA = G2["tur_alt"]; GC = G2["cihaz"]; GU = G2["ulke"]
D12, D26 = _G12.D12, _G12.D26
def _pay_tr(v): return yzd(v)
def _pay_en(v): return ("%.1f" % v) + "%"
def _isr(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + "%" + ("%.1f" % abs(v)).replace(".", ",")
def _isr_en(v): return ("+" if round(v, 1) > 0 else ("-" if round(v, 1) < 0 else "")) + ("%.1f" % abs(v)) + "%"
def _ay(m): return AY.get(m)
x("Oca", "Jan"); x("Şub", "Feb"); x("Mar", "Mar"); x("Nis", "Apr"); x("May", "May"); x("Haz", "Jun"); x("Tem", "Jul"); x("Ağu", "Aug"); x("Eyl", "Sep"); x("Eki", "Oct"); x("Kas", "Nov"); x("Ara", "Dec")
AD = [a for a, _ in AYA]
def _yil(y, i): return [(_ay("%d-%02d" % (y, m)) or [None, None, None])[i] for m in range(1, 13)]
HE = ["06", "07", "08", "09"]
def _top(y, i, aylar=HE): return sum(AY["%d-%s" % (y, m)][i] for m in aylar)
c25, c26 = _top(2025, 0), _top(2026, 0); i25, i26 = _top(2025, 1), _top(2026, 1)
he_c = (c26 / c25 - 1) * 100; he_i = (i26 / i25 - 1) * 100
y12c, y12i = G2["y12"]["click"], G2["y12"]["gosterim"]
cih_t = sum(v[0] for v in GC.values()); cih_i = sum(v[1] for v in GC.values())
mob = 100 * GC["MOBILE"][0] / cih_t; mob_i = 100 * GC["MOBILE"][1] / cih_i
ctr_m = 100 * GC["MOBILE"][0] / GC["MOBILE"][1]; ctr_d = 100 * GC["DESKTOP"][0] / GC["DESKTOP"][1]

# ---------------------------------------------------------------- 1 · aylık seri 2025 ve 2026
# 2025 Ocak - Mayıs tık ve gösterimi marka ekibinin Search Console aylık dışa aktarımındandır (API 16 ay saklar); bu aylar için ortalama sıra yoktur.
from grafik2 import kombo2 as _kombo2, cift as _cift, f_k as _fk2, f_pay as _fpay
x("Click", "Clicks"); x("Gösterim", "Impressions"); x("Ort. sıra", "Avg. position")
def _sira_b(v): t = ("%.1f" % v); return x(t.replace(".", ","), t)
def _cizgi_yil(i, et_tr, et_en):
    return cizgi([("2025", YRENK["2025"], _yil(2025, i)), ("2026", YRENK["2026"], _yil(2026, i))], y_etiket=x(et_tr, et_en), aylar=AD, x_etiket=AD, kalin={1: 3.2})
def _cubuk_yil(i, ad_tr, ad_en, et_tr, et_en):
    return _kombo2(AD, [{"ad": "2025", "renk": YRENK["2025"], "deger": _yil(2025, i), "tip": "cubuk", "bicim": _fk2},
                        {"ad": "2026", "renk": YRENK["2026"], "deger": _yil(2026, i), "tip": "cubuk", "bicim": _fk2, "eksen_ad": x(ad_tr, ad_en)}], cap=x(et_tr, et_en))
_ET_C = ("Aylık organik tık · vitra.com.tr, 2025 ve 2026 üst üste", "Monthly organic clicks · vitra.com.tr, 2025 and 2026 overlaid")
_ET_G = ("Aylık gösterim · vitra.com.tr, 2025 ve 2026 üst üste", "Monthly impressions · vitra.com.tr, 2025 and 2026 overlaid")
_A26 = AD[:9]
_KG = _kombo2(AD, [{"ad": x("Gösterim 2025", "Impressions 2025"), "renk": "#B9C6C3", "deger": _yil(2025, 1), "tip": "cubuk", "eksen": "sol", "bicim": _fk2, "eksen_ad": x("Gösterim", "Impressions")},
                   {"ad": x("Gösterim 2026", "Impressions 2026"), "renk": "#F4B9A3", "deger": _yil(2026, 1), "tip": "cubuk", "eksen": "sol", "bicim": _fk2},
                   {"ad": x("Click 2025", "Clicks 2025"), "renk": YRENK["2025"], "deger": _yil(2025, 0), "tip": "cizgi", "eksen": "sag", "bicim": _fk2, "eksen_ad": x("Click", "Clicks")},
                   {"ad": x("Click 2026", "Clicks 2026"), "renk": YRENK["2026"], "deger": _yil(2026, 0), "tip": "cizgi", "eksen": "sag", "bicim": _fk2}],
              cap=x("Aylık gösterim (çubuk, sol eksen) ve organik tık (çizgi, sağ eksen) · 2025 ve 2026", "Monthly impressions (bars, left axis) and organic clicks (lines, right axis) · 2025 and 2026"))
_K26 = _kombo2(_A26, [{"ad": x("Gösterim", "Impressions"), "renk": "#B9C6C3", "deger": _yil(2026, 1)[:9], "tip": "cubuk", "eksen": "sol", "bicim": _fk2, "eksen_ad": x("Gösterim", "Impressions")},
                      {"ad": x("Click", "Clicks"), "renk": YRENK["2026"], "deger": _yil(2026, 0)[:9], "tip": "cizgi", "eksen": "sag", "bicim": _fk2, "eksen_ad": x("Click", "Clicks")},
                      {"ad": x("Ort. sıra", "Avg. position"), "renk": "#10332F", "deger": _yil(2026, 2)[:9], "tip": "kesik", "eksen": "sag2", "ters": True, "bicim": _sira_b, "eksen_ad": x("Sıra", "Position")}],
               cap=x("2026 · aylık gösterim (çubuk), organik tık (çizgi) ve ortalama Google sırası (kesikli çizgi, ters eksen: yukarısı daha iyi sıra)", "2026 · monthly impressions (bars), organic clicks (line) and average Google position (dashed line, reversed axis: higher is a better position)"))
G_AY = sekmeler([("Click", "Clicks", _cift(_cizgi_yil(0, *_ET_C), _cubuk_yil(0, "Click", "Clicks", *_ET_C))),
                 ("Gösterim", "Impressions", _cift(_cizgi_yil(1, *_ET_G), _cubuk_yil(1, "Gösterim", "Impressions", *_ET_G))),
                 ("Click ve gösterim", "Clicks and impressions", _KG),
                 ("2026: click, gösterim, sıra", "2026: clicks, impressions, position", _K26)], "gtabs")
# yatay ısı tabloları: aylar sütunda, yıllar satırda; hücre rengi satır içindeki görece büyüklüğü gösterir
def _kh(v):
    r = k(v) if v >= 1000 else bin(v); x(r, r.replace(",", "."))
    return '<span class="kh" data-v="%d">%s</span>' % (round(v), r)
def _isi_hucre(degerler, ters=False):
    vs = [v for v in degerler if v is not None]; lo, hi = (min(vs), max(vs)) if vs else (0, 1)
    out = []
    for v in degerler:
        if v is None: out.append(None); continue
        t = (v - lo) / (hi - lo) if hi > lo else 0.5
        if ters: t = 1 - t
        out.append(("var(--isi-a)", (t - 0.5) * 2 * 0.5) if t >= 0.5 else ("var(--isi-d)", (0.5 - t) * 2 * 0.5))
    return out
def _yatay(m_tr, m_en, ac_tr, ac_en, i, bicim, top_bicim, deg_tip, ters=False):
    v25 = [(_ay("2025-%02d" % m) or [None, None, None])[i] if i < 2 else None for m in range(1, 13)]
    v26 = [(_ay("2026-%02d" % m) or [None, None, None])[i] if i < 2 else None for m in range(1, 13)]
    if i == 2:   # CTR
        v25 = [100 * a[0] / a[1] if a else None for a in (_ay("2025-%02d" % m) for m in range(1, 13))]
        v26 = [100 * a[0] / a[1] if a else None for a in (_ay("2026-%02d" % m) for m in range(1, 13))]
    if i == 3:   # ortalama sıra
        v25 = [(_ay("2025-%02d" % m) or [None, None, None])[2] for m in range(1, 13)]
        v26 = [(_ay("2026-%02d" % m) or [None, None, None])[2] for m in range(1, 13)]
    def top(y):
        L = [_ay("%d-%02d" % (y, m)) for m in range(1, 10)]
        if i == 0: return sum(a[0] for a in L)
        if i == 1: return sum(a[1] for a in L)
        if i == 2: return 100 * sum(a[0] for a in L) / sum(a[1] for a in L)
        if all(a[2] for a in L): return sum(a[2] * a[1] for a in L) / sum(a[1] for a in L)
        return None
    bas = [th(m_tr, m_en, ac_tr, ac_en)] + [th(a_, b_, "%s %s" % (a_, "2025 ve 2026"), "%s %s" % (b_, "2025 and 2026"), True) for a_, b_ in AYA] + \
          [th("Oca-Eyl", "Jan-Sep", "Ocak - Eylül toplamı ya da ortalaması; iki yılın kıyaslanabildiği dönem.", "January - September total or average; the period comparable across the two years.", True)]
    rows = []
    for y, v, renk in ((2025, v25, YRENK["2025"]), (2026, v26, YRENK["2026"])):
        hs = _isi_hucre(v, ters)
        cells = ['<td class="yil"><i style="background:%s"></i>%d</td>' % (renk, y)]
        for val, h in zip(v, hs):
            cells.append('<td class="n">-</td>' if val is None else '<td class="n yh" style="--yr:%s;--a:%.2f">%s</td>' % (h[0], h[1], bicim(val)))
        tv = top(y); cells.append('<td class="n top">%s</td>' % (top_bicim(tv) if tv is not None else "-"))
        rows.append("<tr>%s</tr>" % "".join(cells))
    dc = ['<td>%s</td>' % x("Değişim", "Change")]
    for a, b in list(zip(v25, v26)) + [(top(2025), top(2026))]:
        if a is None or b is None: dc.append('<td class="n">-</td>'); continue
        if deg_tip == "oran": dc.append('<td class="n">%s</td>' % yz((b / a - 1) * 100))
        elif deg_tip == "puan":
            d = b - a; t_ = ("+" if d > 0 else "") + ("%.2f" % d).replace(".", ","); x(t_, t_.replace(",", "."))
            dc.append('<td class="n"><span class="%s">%s</span></td>' % ("up" if d > 0 else ("dn" if d < 0 else ""), t_))
        else:
            d = b - a; t_ = ("+" if d > 0 else "") + ("%.1f" % d).replace(".", ","); x(t_, t_.replace(",", "."))
            dc.append('<td class="n"><span class="%s">%s</span></td>' % ("up" if d < 0 else ("dn" if d > 0 else ""), t_))
    rows.append('<tr class="deg">%s</tr>' % "".join(dc))
    return '<div class="tw yatay xl"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % ("".join(bas), "".join(rows))
def _pct2(v): r = yzd(v, 2); return r
def _d(a, b): return n(yz((b / a - 1) * 100)) if a and b else n("-")
T_AY = (_yatay("Click", "Clicks", "Aylık organik tık; 2025 Ocak - Mayıs Search Console aylık dışa aktarımından, diğer aylar Search Console API'den. Değişim aynı ayın 2025'e göre yüzde değişimidir.", "Monthly organic clicks; January - May 2025 from the Search Console monthly export, other months from the Search Console API. Change is the percentage change against the same month of 2025.", 0, _kh, _kh, "oran")
        + _yatay("Gösterim", "Impressions", "Aylık gösterim; kaynak ve değişim tanımı Click tablosuyla aynıdır.", "Monthly impressions; source and change definition as in the Clicks table.", 1, _kh, _kh, "oran")
        + _yatay("CTR", "CTR", "Tık / gösterim; Değişim satırı 2026 ile 2025 arasındaki yüzde puan farkıdır (ör. +0,40 = 0,40 puan artış).", "Clicks / impressions; the Change row is the difference in percentage points between 2026 and 2025 (e.g. +0.40 = up 0.40 points).", 2, _pct2, _pct2, "puan")
        + _yatay("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası; 2025 Ocak - Mayıs için dışa aktarımda sıra bulunmamaktadır. Değişim sıra farkıdır, eksi değer daha iyi sıradır; renk düşük sırayı yeşil gösterir.", "Impression-weighted average Google position; the export has no position for January - May 2025. Change is the difference in position, a negative value is a better position; colour shows lower positions in green.", 3, lambda v: _sira_b(v), lambda v: _sira_b(v), "sira", ters=True))
_OE = lambda y, i_: sum(AY["%d-%02d" % (y, m)][i_] for m in range(1, 10))
oe_c = (_OE(2026, 0) / _OE(2025, 0) - 1) * 100; oe_i = (_OE(2026, 1) / _OE(2025, 1) - 1) * 100
_yy = {"%02d" % m: (AY["2026-%02d" % m][0] / AY["2025-%02d" % m][0] - 1) * 100 for m in range(1, 10)}
_yi = {"%02d" % m: (AY["2026-%02d" % m][1] / AY["2025-%02d" % m][1] - 1) * 100 for m in range(1, 10)}
_GS = G2["genai_site_pay"]
INS_AY = insight("Ocak - Eylül 2026'da organik tık 2025'in aynı aylarına göre %s, gösterim %s değişmiştir. Tık Şubat - Nisan'da artmış (Mart %s, Nisan %s), Mayıs'ta (%s) ve Ağustos - Eylül'de (%s, %s) gerilemiştir; Haziran'daki artış (%s) 2025 Haziran'ının yılın en düşük aylarından biri olmasıyla birliktedir. Gösterimdeki daralma Temmuz'dan itibaren derinleşmiş, Eylül'de %s'e ulaşmıştır. Kategori talebindeki gerileme (Bölüm [[b:talep]]) ve Google yapay zeka özelliklerinin site gösterimindeki payının Mayıs'ta %s iken Eylül'de %s'e çıkması (Bölüm [[b:yapayzeka]]) bu dönemle ilişkilendirilebilir."
                 % (yz(oe_c), yz(oe_i), yz(_yy["03"]), yz(_yy["04"]), yz(_yy["05"]), yz(_yy["08"]), yz(_yy["09"]), yz(_yy["06"]), yz(_yi["09"]), yzd(100 * _GS[0][2] / _GS[0][3]), yzd(100 * _GS[-1][2] / _GS[-1][3])),
                 "In January - September 2026, organic clicks changed %s and impressions %s against the same months of 2025. Clicks rose in February - April (March %s, April %s) and declined in May (%s) and August - September (%s, %s); the rise in June (%s) comes with June 2025 being one of the lowest months of the year. The contraction in impressions deepened from July and reached %s in September. The decline in category demand (Section [[b:talep]]) and the share of Google AI features in site impressions rising from %s in May to %s in September (Section [[b:yapayzeka]]) can be associated with this period."
                 % (yz(oe_c), yz(oe_i), yz(_yy["03"]), yz(_yy["04"]), yz(_yy["05"]), yz(_yy["08"]), yz(_yy["09"]), yz(_yy["06"]), yz(_yi["09"]), yzd(100 * _GS[0][2] / _GS[0][3]), yzd(100 * _GS[-1][2] / _GS[-1][3])), "D2", "D44")

# ---------------------------------------------------------------- 2 · sayfa türü (Oca - Eyl 2026), alt kırılım hover
tur_en = {"kategori": "Category pages", "urun": "Product pages", "eski-online": "Old online.vitra.com.tr addresses", "anasayfa": "Home page", "icerik": "Content and inspiration (blog)", "diger": "Other", "servis-bayi": "Service and dealer", "koleksiyon": "Collection pages", "kurumsal": "Corporate", "katalog": "Catalogue", "urun-teknik": "Product technical sheets"}
tur_tr = {"kategori": "Kategori sayfaları", "urun": "Ürün sayfaları", "eski-online": "Eski online.vitra.com.tr adresleri", "anasayfa": "Ana sayfa", "icerik": "İçerik ve ilham (blog)", "diger": "Diğer", "servis-bayi": "Servis ve bayi", "koleksiyon": "Koleksiyon sayfaları", "kurumsal": "Kurumsal", "katalog": "Katalog", "urun-teknik": "Ürün teknik föyleri"}
KAT_EN2 = dict(KAT_EN); KAT_EN2.update({"Karo Seramik": "Ceramic Tiles", "Koleksiyon sayfaları": "Collection pages", "Genel ürün listeleri ve kampanyalar": "General product lists and campaigns"})
K2_EN = {"Klozetler": "WCs", "Lavabolar": "Washbasins", "Klozet Kapakları": "WC seats", "Akıllı Klozet": "Smart WCs", "Pisuvarlar": "Urinals", "Bideler": "Bidets", "Tamamlayıcı": "Complementary products",
         "Ana kategori ve genel listeler": "Main category and general lists", "İç Takımlar": "Inner mechanisms", "Gömme Rezervuarlar": "Concealed cisterns", "Kumanda Panelleri": "Flush plates",
         "Banyo Dolapları": "Bathroom cabinets", "Lavabo Dolapları": "Washbasin cabinets", "Çamaşır Makinesi Dolapları": "Washing machine cabinets", "Banyo Aynaları": "Bathroom mirrors", "Tezgahlar": "Countertops",
         "Set Modülleri": "Set modules", "Eviye Bataryaları": "Kitchen mixers", "Eviyeler": "Kitchen sinks", "Banyo Bataryaları": "Bath mixers", "Lavabo Bataryaları": "Basin mixers", "Musluklar": "Taps",
         "Ankastre": "Concealed mixers", "Bide Bataryaları": "Bidet mixers", "Duş Setleri": "Shower sets", "Duş Başlıkları": "Shower heads", "Duş Sistemleri": "Shower systems", "El Duşları": "Hand showers",
         "Duş Kolonları": "Shower columns", "Duşakabin": "Shower enclosures", "Duş Tekneleri": "Shower trays", "Küvetler": "Bathtubs", "Duş Kanalları": "Shower channels", "Duş Üniteleri": "Shower units",
         "Tuvalet Kağıtlıkları": "Toilet roll holders", "Havluluklar": "Towel holders", "Tuvalet Fırçaları": "Toilet brushes", "Sabunluklar": "Soap dishes", "Çöp Kovaları": "Waste bins", "Tutunma Barları": "Grab bars",
         "Diğer": "Other", "Ürün sayfaları": "Product pages", "Diğer karo listeleri": "Other tile lists", "Banyo karoları": "Bathroom tiles", "Zemin karoları": "Floor tiles", "Mutfak karoları": "Kitchen tiles",
         "Dış mekan karoları": "Outdoor tiles", "Servisler ve satış noktaları listesi": "Services and sales points list", "Tek mağaza, bayi ve servis sayfaları": "Individual store, dealer and service pages", "Duvar karoları": "Wall tiles", "Dizin sayfası": "Index page"}
for a_, b_, c_ in _RG.GRUP: K2_EN[b_] = c_
for k_, v_ in KAT_EN2.items(): K2_EN.setdefault(k_, v_)
def _alt_ac(baslik_tr, baslik_en, L, toplam):
    """Alt kırılım balonu: ilk altı kalem ve tık payı."""
    tr_ = "; ".join("%s %s" % (a_ if a_.startswith("/") else a_, _pay_tr(100 * v_ / toplam)) for a_, v_ in L)
    en_ = "; ".join("%s %s" % (a_ if a_.startswith("/") else K2_EN.get(a_, a_), _pay_en(100 * v_ / toplam)) for a_, v_ in L)
    t_tr = "%s · alt kırılım, tık payı (%s): %s" % (baslik_tr, D26[0], tr_); t_en = "%s · breakdown, click share (%s): %s" % (baslik_en, D26[1], en_)
    x(t_tr, t_en); return t_tr
def _ac_span(et_tr, et_en, t_tr):
    return '<span class="ac" tabindex="0" data-t="%s">%s</span>' % (_h.escape(t_tr, quote=True), x(et_tr, et_en))
ttot = sum(v[0] for v in GT.values())
_GTs = sorted(GT.items(), key=lambda i: -i[1][0])
rows = []
for t, v in _GTs:
    ac_ = _alt_ac(tur_tr[t], tur_en[t], GTA.get(t, []), v[0]) if GTA.get(t) and t not in ("anasayfa",) else None
    rows.append([_ac_span(tur_tr[t], tur_en[t], ac_) if ac_ else x(tur_tr[t], tur_en[t]), cell(v[2]), cellk(v[0]), n(yzd(100 * v[0] / ttot)), cellk(v[1]), n(yzd(100 * v[0] / v[1]) if v[1] else "-")])
tbl = tablo([th("Sayfa türü", "Page type", "Adres yapısına göre sayfa sınıfı; /c- ve kategori dizinleri kategori, -p- ve -sku- kodlu adresler ürün sayfasıdır. Noktalı alt çizgili türün üzerine gelindiğinde alt kırılımı açılır.", "Page class by URL structure; /c- and category directories are category pages, addresses coded -p- and -sku- are product pages. Hovering over an underlined type opens its breakdown."),
             th("Sayfa", "Pages", "Dönemde en az bir gösterim almış tekil sayfa sayısı; sayfalama ve filtre parametreli adresler kendi temel adresiyle tek sayfa sayılmıştır.", "Number of unique pages with at least one impression in the period; paginated and filtered addresses are counted as one page with their base page.", True),
             th("Click", "Clicks", "%s toplam click." % D26[0], "Total clicks, %s." % D26[1], True),
             th("Pay", "Share", "Sayfa türünün toplam tık içindeki payı.", "Page type's share of total clicks.", True),
             th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
             th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows)
_HR = ["#10332F", "#2E7D32", "#E85F36", "#F5A623", "#7A8C89", "#C9D3D1"]
def _alt_liste(t, toplam):
    return [(x(a_, a_) if a_.startswith("/") else x(a_, K2_EN.get(a_, a_)), x(_pay_tr(100 * v_ / toplam), _pay_en(100 * v_ / toplam))) for a_, v_ in GTA.get(t, [])[:5]] if t != "anasayfa" else []
_diger = _GTs[5:]
HALKA_TUR = _halka([(x(tur_tr[t], tur_en[t]), v[0], _HR[i]) for i, (t, v) in enumerate(_GTs[:5])] + [(x("Diğer sayfa türleri", "Other page types"), sum(v[0] for _, v in _diger), _HR[5])],
                   x("Organik tıkların sayfa türlerine dağılımı · %s" % D26[0], "Organic clicks by page type · %s" % D26[1]),
                   merkez=(_fk(ttot), x("tık · sayfa düzeyi", "clicks · page level")), deger_bicim=_fk,
                   alt=[_alt_liste(t, v[0]) for t, v in _GTs[:5]] + [[(x(tur_tr[t], tur_en[t]), x(_pay_tr(100 * v[0] / sum(w[0] for _, w in _diger)), _pay_en(100 * v[0] / sum(w[0] for _, w in _diger)))) for t, v in _diger[:5]]])
INS_TUR = insight("%s döneminde organik tıkların %s'i kategori sayfalarına, %s'i ürün sayfalarına gelmektedir; kategori sayfası başına ortalama tık ürün sayfasının ~%sx'idir. Ürün sayfaları %s gösterimle %s CTR üretirken kategori sayfaları %s CTR ile çalışmaktadır: bu fark, kullanıcının jenerik aramada kategori sayfasına, model aramasında ürün sayfasına ulaştığına işaret etmektedir. İçerik ve ilham (blog) sayfaları tıkların %s'ini almaktadır."
                  % (_G12.D26U[0], yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), "%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2])), k(GT["urun"][1]),
                     yzd(100 * GT["urun"][0] / GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1]), yzd(100 * GT["icerik"][0] / ttot)),
                  "In %s, %s of organic clicks land on category pages and %s on product pages; the average click per category page is ~%sx that of a product page. Product pages, with %s impressions, produce %s CTR while category pages work at %s CTR: this gap indicates that users reach the category page in generic searches and the product page in model searches. Content and inspiration (blog) pages take %s of clicks."
                  % (_G12.D26U[1], yzd(100 * GT["kategori"][0] / ttot), yzd(100 * GT["urun"][0] / ttot), "%.0f" % ((GT["kategori"][0] / GT["kategori"][2]) / (GT["urun"][0] / GT["urun"][2])), k(GT["urun"][1]),
                     yzd(100 * GT["urun"][0] / GT["urun"][1]), yzd(100 * GT["kategori"][0] / GT["kategori"][1]), yzd(100 * GT["icerik"][0] / ttot)), "D2")

# ---------------------------------------------------------------- 3 · kategori kırılımı (Oca - Eyl 2026)
EK_GRUP = ("Koleksiyon sayfaları", "Genel ürün listeleri ve kampanyalar")
K8 = sorted([k_ for k_ in GK if k_ not in EK_GRUP], key=lambda k_: -GK[k_][0])
k8tot = sum(GK[k_][0] for k_ in K8); ktot = sum(v[0] for v in GK.values())
_TK = {"Karo Seramik": "Karo Seramik Ürünleri"}
def _tp(k1): return 100 * A["k1"][_TK.get(k1, k1)]["a26"] / A["toplam"]["a26"]
rows2 = []
for k1 in K8 + list(EK_GRUP):
    v = GK[k1]; ac_ = _alt_ac(k1, KAT_EN2.get(k1, k1), GA.get(k1, []), v[0])
    rows2.append([_ac_span(k1, KAT_EN2.get(k1, k1), ac_), cell(v[2]), cellk(v[0]), n(yzd(100 * v[0] / k8tot)) if k1 in K8 else n("-"), n(yzd(_tp(k1))) if k1 in K8 else n("-"), cellk(v[1]), n(yzd(100 * v[0] / v[1]))])
tbl2 = tablo([th("Kategori", "Category", "Kategori, ürün, koleksiyon ve teknik föy sayfalarının adres yapısından türetilen ana kategori; son iki satır kategoriye eşlenmeyen koleksiyon sayfaları ile genel ürün listeleri ve kampanya sayfalarıdır. Kategori adının üzerine gelindiğinde alt kırılım açılır.", "Main category derived from the URL structure of category, product, collection and technical sheet pages; the last two rows are collection pages and general product list and campaign pages not mapped to a category. Hovering over a category name opens its breakdown."),
              th("Sayfa", "Pages", "Kategoriye eşlenen tekil sayfa sayısı; sayfalama ve filtre parametreli adresler tek sayılmıştır.", "Number of unique pages mapped to the category; paginated and filtered addresses are counted once.", True),
              th("Click", "Clicks", "%s toplam click." % D26[0], "Total clicks, %s." % D26[1], True),
              th("Click payı", "Click share", "Sekiz ana kategorinin toplam click'i içindeki pay; talep payıyla aynı tabandadır, ek satırlar için yoktur.", "Share of the total clicks of the eight main categories; on the same base as demand share, not applicable to the additional rows.", True),
              th("Talep payı", "Demand share", "Kategorinin Oca-Ağu 2026 arama talebindeki payı (Bölüm [[b:talep]], 2.299 kelime); ek satırlar için yoktur.", "The category's share of Jan-Aug 2026 search demand (Section [[b:talep]], 2,299 keywords); not applicable to the additional rows.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)], rows2, "dar")
GPAY = _gr([(x(k1, KAT_EN2.get(k1, k1)), [_tp(k1), 100 * GK[k1][0] / k8tot]) for k1 in sorted(K8, key=lambda k_: -_tp(k_))],
           [(x("Arama talebi payı · Oca-Ağu 2026", "Search demand share · Jan-Aug 2026"), "#9AA8A5"), (x("Organik tık payı · %s" % D26[0], "Organic click share · %s" % D26[1]), "#10332F")],
           x("Kategori bazında arama talebi payı ve vitra.com.tr organik tık payı (8 ana kategori)", "Search demand share and vitra.com.tr organic click share by category (8 main categories)"))
_RK = ["#10332F", "#7A8C89", "#2E7D32", "#E85F36", "#F5A623", "#5B7FA6", "#B5838D", "#9C6644", "#C9D3D1", "#6D597A"]
_AY26 = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl"]
GRAFIK = cizgi([(x(k1, KAT_EN2.get(k1, k1)), _RK[i], G2["kat_ay"][k1]) for i, k1 in enumerate(K8 + list(EK_GRUP))],
               y_etiket=x("Aylık organik tık · kategori bazında, Oca - Eyl 2026 (lejanttan kategori açılıp kapatılabilir)", "Monthly organic clicks · by category, Jan - Sep 2026 (categories can be switched on and off in the legend)"),
               aylar=_AY26, x_etiket=_AY26, gizli=tuple(range(5, len(K8) + 2)), olcek=True)
_ACIK = sorted([(100 * GK[k1][0] / k8tot - _tp(k1), k1) for k1 in K8])
if {_ACIK[0][1], _ACIK[1][1]} != {"Banyo Mobilyaları", "Yıkanma Alanları"}: raise SystemExit("organik: en geniş talep-tık açığı değişti: %s" % _ACIK[:3])
_bm_sira = [k1 for k1, _ in sorted(A["k1"].items(), key=lambda i: -i[1]["a26"])].index("Banyo Mobilyaları") + 1
_SIRA_TR = {1: "en", 2: "ikinci", 3: "üçüncü", 4: "dördüncü"}; _SIRA_EN = {1: "largest", 2: "second-largest", 3: "third-largest", 4: "fourth-largest"}
_kl = dict(GA["Vitrifiyeler"])
INS_KAT = insight("Sekiz ana kategoriye gelen tıkların %s'i Vitrifiyeler (Klozetler %s, Lavabolar %s) ve %s'i Karo Seramik sayfalarındadır. Arama talebinde %s büyük kategori olan Banyo Mobilyaları (talep payı %s) organik tıkta %s pay almaktadır; Yıkanma Alanları da talep payı %s iken tık payında %s'de kalmaktadır. Talebin büyüklüğü ile sitenin bu talepten aldığı pay arasındaki en geniş açık bu iki kategoridedir. Kategoriye eşlenmeyen koleksiyon sayfaları %s tık almaktadır."
                  % (yzd(100 * GK["Vitrifiyeler"][0] / k8tot), yzd(100 * _kl["Klozetler"] / k8tot), yzd(100 * _kl["Lavabolar"] / k8tot), yzd(100 * GK["Karo Seramik"][0] / k8tot), _SIRA_TR[_bm_sira],
                     yzd(_tp("Banyo Mobilyaları")), yzd(100 * GK["Banyo Mobilyaları"][0] / k8tot), yzd(_tp("Yıkanma Alanları")), yzd(100 * GK["Yıkanma Alanları"][0] / k8tot), k(GK["Koleksiyon sayfaları"][0])),
                  "%s of the clicks landing on the eight main categories are on Sanitaryware (WCs %s, Washbasins %s) and %s on Ceramic Tiles pages. Bathroom Furniture, the %s category in search demand (demand share %s), takes %s of organic clicks; Bathing Areas also stays at %s of clicks against a demand share of %s. The widest gaps between the size of demand and the share the site captures are in these two categories. Collection pages not mapped to a category receive %s clicks."
                  % (yzd(100 * GK["Vitrifiyeler"][0] / k8tot), yzd(100 * _kl["Klozetler"] / k8tot), yzd(100 * _kl["Lavabolar"] / k8tot), yzd(100 * GK["Karo Seramik"][0] / k8tot), _SIRA_EN[_bm_sira],
                     yzd(_tp("Banyo Mobilyaları")), yzd(100 * GK["Banyo Mobilyaları"][0] / k8tot), yzd(_tp("Yıkanma Alanları")), yzd(100 * GK["Yıkanma Alanları"][0] / k8tot), k(GK["Koleksiyon sayfaları"][0])), "D2", "D1")

# ---------------------------------------------------------------- 4 · en çok tık alan sayfalar (Oca - Eyl 2026)
x("/ (ana sayfa)", "/ (home page)")
TS = G2["top_sayfa"][:15]
rows3 = []
for uu, c, i, p in TS:
    p_ = _G12.yol(uu)
    rows3.append([u("https://www.vitra.com.tr" + (p_ if p_ != "/" else "/"), p_ if p_ != "/" else "/ (ana sayfa)"), cellk(c), cellk(i), n(yzd(100 * c / i)), n(("%.1f" % p).replace(".", ","))])
tbl3 = tablo([th("Sayfa adresi", "Page address", "Sayfa adresi; bağlantı canlı sayfaya gider.", "Page address; the link opens the live page."),
              th("Click", "Clicks", "%s organik click." % D26[0], "Organic clicks, %s." % D26[1], True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası.", "Impression-weighted average Google position.", True)], rows3, "dar")

# ---------------------------------------------------------------- 5 · blog (İlham Veren Fikirler)
BA = G2["blog_ay"]; SAS = G2["site_ay_sayfa"]
def _bl(y, i): return [(BA.get("%d-%02d" % (y, m)) or [None, None])[i] for m in range(1, 13)]
def _blog_cubuk(i, ad_tr, ad_en, et_tr, et_en):
    return _kombo2(AD, [{"ad": "2025", "renk": YRENK["2025"], "deger": _bl(2025, i), "tip": "cubuk", "bicim": _fk2},
                        {"ad": "2026", "renk": YRENK["2026"], "deger": _bl(2026, i), "tip": "cubuk", "bicim": _fk2, "eksen_ad": x(ad_tr, ad_en)}], cap=x(et_tr, et_en))
_EBC = ("Blog sayfalarının aylık organik tıkı · /ilham-veren-fikirler/, tüm alt alan adları, 2025 ve 2026 üst üste", "Monthly organic clicks of blog pages · /ilham-veren-fikirler/, all subdomains, 2025 and 2026 overlaid")
_EBG = ("Blog sayfalarının aylık gösterimi · /ilham-veren-fikirler/, 2025 ve 2026 üst üste", "Monthly impressions of blog pages · /ilham-veren-fikirler/, 2025 and 2026 overlaid")
G_BLOG = sekmeler([("Click", "Clicks", _cift(cizgi([("2025", YRENK["2025"], _bl(2025, 0)), ("2026", YRENK["2026"], _bl(2026, 0))], y_etiket=x(*_EBC), aylar=AD, x_etiket=AD, kalin={1: 3.2}),
                                          _blog_cubuk(0, "Click", "Clicks", *_EBC))),
                   ("Gösterim", "Impressions", _cift(cizgi([("2025", YRENK["2025"], _bl(2025, 1)), ("2026", YRENK["2026"], _bl(2026, 1))], y_etiket=x(*_EBG), aylar=AD, x_etiket=AD, kalin={1: 3.2}),
                                          _blog_cubuk(1, "Gösterim", "Impressions", *_EBG)))], "gtabs")
b12c = sum(BA[m][0] for m in _G12.Y12); b12i = sum(BA[m][1] for m in _G12.Y12); s12 = sum(SAS[m] for m in _G12.Y12)
bc25, bc26 = sum(BA["2025-" + m][0] for m in HE), sum(BA["2026-" + m][0] for m in HE); bi25, bi26 = sum(BA["2025-" + m][1] for m in HE), sum(BA["2026-" + m][1] for m in HE)
B26, B25 = G2["blog_hazeyl"]["2026"], G2["blog_hazeyl"]["2025"]
def _tekil(p): return p[:-4] if p.endswith("-old") else p
BL = {}
for p, c, i, ps in G2["blog_12ay"]:
    q = _tekil(p); a = BL.setdefault(q, [0, 0, 0.0]); a[0] += c; a[1] += i; a[2] += (ps or 0) * i
def _he(p, d):
    c_ = 0
    for k_ in (p, p + "-old"):
        if k_ in d: c_ += d[k_][0]
    return c_
_BG = {}
for p, (c, i, ps) in BL.items():
    s_ = p.rstrip("/").split("/")[-1]
    if s_ == "ilham-veren-fikirler": continue
    g = _BG.setdefault(_RG.grup(s_), [0, 0, 0, 0, 0]); g[0] += 1 if c >= 5 else 0; g[1] += c; g[2] += i; g[3] += _he(p, B25); g[4] += _he(p, B26)
_bgt = sum(g[1] for g in _BG.values())
rows_bg = [[x(b_, c_), cell(_BG[a_][0]), cellk(_BG[a_][1]), n(yzd(100 * _BG[a_][1] / _bgt)), cellk(_BG[a_][2]), n(yzd(100 * _BG[a_][1] / _BG[a_][2], 2)), _d(_BG[a_][3], _BG[a_][4])] for a_, b_, c_ in _RG.GRUP if a_ in _BG]
T_BG = tablo([th("Konu grubu", "Topic group", "Blog yazılarının adresteki konuya göre gruplanması (Bölüm [[b:geo]] ile aynı gruplar).", "Grouping of blog articles by the topic in the address (same groups as Section [[b:geo]])."),
              th("Sayfa", "Pages", "12 ayda en az 5 tık alan yazı sayısı.", "Number of articles with at least 5 clicks in 12 months.", True),
              th("Click", "Clicks", "%s organik click." % D12[0], "Organic clicks, %s." % D12[1], True),
              th("Pay", "Share", "Blog tıkları içindeki pay.", "Share of blog clicks.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Click değişimi Haz-Eyl", "Click change Jun-Sep", "1 Haz - 29 Eyl 2026 tıkının 2025'in aynı günlerine göre değişimi.", "Change of clicks in 1 Jun - 29 Sep 2026 against the same days of 2025.", True)], rows_bg, "dar")
rows_bp = []
for p, (c, i, ps) in sorted(BL.items(), key=lambda r: -r[1][0])[:15]:
    rows_bp.append([u("https://www.vitra.com.tr" + p + "/", p.replace("/ilham-veren-fikirler", "") or "/ilham-veren-fikirler/"), cellk(c), cellk(i), n(yzd(100 * c / i, 2)), n(("%.1f" % (ps / i)).replace(".", ",")), _d(_he(p, B25), _he(p, B26))])
x("/ilham-veren-fikirler/", "/ilham-veren-fikirler/")
T_BP = tablo([th("Yazı", "Article", "Blog yazısının adresi (/ilham-veren-fikirler/ sonrası); bağlantı canlı sayfaya gider.", "The blog article's address (after /ilham-veren-fikirler/); the link opens the live page."),
              th("Click", "Clicks", "%s organik click; yazının eski (-old) adresi dahil." % D12[0], "Organic clicks, %s; including the article's old (-old) address." % D12[1], True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Ort. sıra", "Avg. position", "Gösterimle ağırlıklı ortalama Google sırası.", "Impression-weighted average Google position.", True),
              th("Click değişimi Haz-Eyl", "Click change Jun-Sep", "1 Haz - 29 Eyl 2026 tıkının 2025'in aynı günlerine göre değişimi.", "Change of clicks in 1 Jun - 29 Sep 2026 against the same days of 2025.", True)], rows_bp, "dar")
INS_BLOG = insight("Blog (/ilham-veren-fikirler/) sayfaları %s döneminde %s organik tık ve %s gösterim almıştır; bu, sitenin sayfa düzeyindeki tıklarının %s'idir. Haziran - Eylül'de blog tıkları 2025'e göre %s değişirken gösterimler %s değişmiştir: sayfalar aramalarda daha çok görünmekte, ancak daha az tıklanmaktadır. Tıkın en çok gerilediği yazılar, Google'ın yapay zeka özelliklerinde en çok gösterilen yazılardır (Bölüm [[b:yapayzeka]])."
                   % (_G12.D12U[0], k(b12c), k(b12i), yzd(100 * b12c / s12), yz((bc26 / bc25 - 1) * 100), yz((bi26 / bi25 - 1) * 100)),
                   "Blog (/ilham-veren-fikirler/) pages received %s organic clicks and %s impressions in %s; this is %s of the site's page-level clicks. In June - September, blog clicks changed %s against 2025 while impressions changed %s: the pages appear more in searches but are clicked less. The articles with the steepest decline in clicks are those shown most in Google's AI features (Section [[b:yapayzeka]])."
                   % (k(b12c), k(b12i), _G12.D12U[1], yzd(100 * b12c / s12), yz((bc26 / bc25 - 1) * 100), yz((bi26 / bi25 - 1) * 100)), "D2")

# ---------------------------------------------------------------- 6 · cihaz ve ülke (12 ay)
T_CU = tablo([th("Kırılım", "Breakdown", "Search Console cihaz ve ülke boyutu.", "Search Console device and country dimension."),
              th("Click", "Clicks", "%s toplam." % D12[0], "Total, %s." % D12[1], True),
              th("Pay", "Share", "Toplam tık içindeki pay.", "Share of total clicks.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True)],
             [[x("Mobil", "Mobile"), cellk(GC["MOBILE"][0]), n(yzd(mob)), n(yzd(ctr_m))],
              [x("Masaüstü", "Desktop"), cellk(GC["DESKTOP"][0]), n(yzd(100 * GC["DESKTOP"][0] / cih_t)), n(yzd(ctr_d))],
              [x("Tablet", "Tablet"), cellk(GC["TABLET"][0]), n(yzd(100 * GC["TABLET"][0] / cih_t)), n(yzd(100 * GC["TABLET"][0] / GC["TABLET"][1]))],
              [x("Türkiye", "Turkey"), cellk(GU[0][1]), n(yzd(GU[0][2])), n("-")], [x("Almanya", "Germany"), cellk(GU[1][1]), n(yzd(GU[1][2])), n("-")], [x("Kıbrıs", "Cyprus"), cellk(GU[2][1]), n(yzd(GU[2][2])), n("-")]], "dar")
INS_SON = insight("Oca - Eyl 2026'da en çok tık alan sayfa ana sayfadır (%s); ilk 15 sayfanın %d'i kategori sayfasıdır. Cihaz kırılımında mobil, gösterimlerin %s'ini almasına karşın tıkların %s'ini üretmektedir; CTR masaüstünde %s, mobilde %s seviyesindedir (%s)."
                  % (bin(TS[0][1]), sum(1 for uu, *_ in TS if "/c-" in uu), yzd(mob_i), yzd(mob), yzd(ctr_d), yzd(ctr_m), D12[0]),
                  "In Jan - Sep 2026 the page with the most clicks is the home page (%s); %d of the top 15 pages are category pages. By device, mobile takes %s of impressions but produces %s of clicks; CTR is %s on desktop and %s on mobile (%s)."
                  % (f"{TS[0][1]:,}", sum(1 for uu, *_ in TS if "/c-" in uu), yzd(mob_i), yzd(mob), yzd(ctr_d), yzd(ctr_m), D12[1]), "D2")

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
<h3>%s</h3>
%s
%s
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Search Console verisi, vitra.com.tr'nin Google'dan aldığı trafiğin aylık seyrini, hangi sayfa türlerine ve kategorilere geldiğini göstermektedir. Veri alan adı düzeyindeki mülkten (sc-domain:vitra.com.tr) alınmıştır; tüm alt alan adları tek toplam olarak kapsanmaktadır. Toplamlar, blog, cihaz ve ülke kırılımı 1 Ekim 2025 - 30 Eylül 2026 (12 ay) dönemine aittir. Aralık 2025'te online.vitra.com.tr adresleri www.vitra.com.tr'ye taşındığı için sayfa türü, kategori ve en çok tık alan sayfalar 1 Ocak - 30 Eylül 2026 verisiyle verilmiştir.",
   "Search Console data shows the monthly trend of the traffic vitra.com.tr receives from Google and which page types and categories it lands on. Data comes from the domain-level property (sc-domain:vitra.com.tr); all subdomains are covered as a single total. Totals, blog, device and country breakdowns cover 1 October 2025 - 30 September 2026 (12 months). As online.vitra.com.tr addresses moved to www.vitra.com.tr in December 2025, page types, categories and the pages with most clicks are given with 1 January - 30 September 2026 data."),
 kpi_kart(k(y12c), "Organik tık · %s (12 ay); gösterim %s" % (D12[0], k(y12i)), "Organic clicks · %s (12 months); impressions %s" % (D12[1], k(y12i).replace(",", "."))),
 kpi_kart(yzd(100 * y12c / y12i), "Ortalama CTR · %s" % D12[0], "Average CTR · %s" % D12[1]),
 kpi_kart(yz(oe_c), "Organik tık değişimi · Oca-Eyl 2026 / Oca-Eyl 2025; gösterim %s" % _isr(oe_i), "Organic click change · Jan-Sep 2026 / Jan-Sep 2025; impressions %s" % _isr_en(oe_i), "dn" if oe_c < 0 else ""),
 kpi_kart(yzd(mob), "Mobil tık payı · %s; gösterim payı %s" % (D12[0], yzd(mob_i)), "Mobile click share · %s; impression share %s" % (D12[1], _pay_en(mob_i))),
 x("Aylık organik performans: 2025 ve 2026", "Monthly organic performance: 2025 and 2026"), G_AY, T_AY, INS_AY,
 x("Trafik hangi sayfa türlerine geliyor? · Oca-Eyl 2026", "Which page types does the traffic land on? · Jan-Sep 2026"), HALKA_TUR + tbl, INS_TUR,
 x("Kategori bazında organik trafik · Oca-Eyl 2026", "Organic traffic by category · Jan-Sep 2026"), tbl2, GPAY, GRAFIK, INS_KAT,
 x("En çok tık alan sayfalar · Oca-Eyl 2026", "Pages with most clicks · Jan-Sep 2026"), tbl3,
 x("Blog (İlham Veren Fikirler): aylık tık, konu grupları ve yazılar", "Blog (İlham Veren Fikirler): monthly clicks, topic groups and articles"), G_BLOG, T_BG, T_BP, INS_BLOG,
 x("Cihaz ve ülke · 12 ay", "Device and country · 12 months"), T_CU, INS_SON,
 kaynak("Google Search Console · sc-domain:vitra.com.tr · toplamlar, blog, cihaz ve ülke %s; sayfa türü, kategori ve sayfalar %s; aylık seri Haz 2025 - Eyl 2026 · aylık sayfa, gün×cihaz ve ülke boyutları · %s" % (D12[0], D26[0], veri.TARIH),
        "Google Search Console · sc-domain:vitra.com.tr · totals, blog, device and country %s; page types, categories and pages %s; monthly series Jun 2025 - Sep 2026 · monthly page, day×device and country dimensions · %s" % (D12[1], D26[1], veri.TARIH), "D2"),
)
