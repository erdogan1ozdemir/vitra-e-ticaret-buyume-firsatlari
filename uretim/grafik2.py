# -*- coding: utf-8 -*-
"""Ek grafik yardimcilari: kombo (cubuk + cizgi), sapmali cubuk, dumbbell, gruplu yatay cubuk,
%100 yigilmis cubuk ve tablo isi haritasi. Balonlar rapor_js 'genel' tipiyle basilir:
her hover bandi kendi basligini ve satirlarini tasir."""
import json, re, math
from t2_ortak import x, EK
_AY_TR = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara']; _AY_EN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

SOL_ET = 250


def _js(d):
    return json.dumps(d, ensure_ascii=False).replace("'", "&#39;")


def _fig(svg, noktalar, lej="", cap=""):
    return ('<figure class="fig" data-grafik=\'%s\'>%s%s<div class="tip" hidden></div>%s</figure>'
            % (_js({"tip": "genel", "noktalar": noktalar}), ('<figcaption class="figcap">%s</figcaption>' % cap) if cap else "", svg, lej))


def _lej(ogeler):
    """ogeler: [(ad, renk, 'kare'|'cizgi'|'nokta')]"""
    return '<div class="legend">' + "".join(
        '<span class="lg-s"><i class="%s" style="background:%s"></i>%s</span>' % (b, r, a) for a, r, b in ogeler) + '</div>'


def _svg(g, y):
    return '<svg class="chart" viewBox="0 0 %d %d" role="img" preserveAspectRatio="xMidYMid meet">' % (g, y)


def tr_sayi(v, ond=0):
    s = ("%." + str(ond) + "f") % v
    tam, _, kes = s.partition(".")
    tam = "{:,}".format(int(tam)).replace(",", ".") if tam.lstrip("-") else tam
    return tam + ("," + kes if kes else "")


def en_sayi(v, ond=0):
    return ("{:,.%df}" % ond).format(v)


_EN = {}


def f_adet(v):
    return x(tr_sayi(v), en_sayi(v))


def f_tl(v):
    return x(tr_sayi(v) + " TL", en_sayi(v) + " TL")


def f_pay(v, ond=1):
    return x("%" + tr_sayi(v, ond), en_sayi(v, ond) + "%")


def f_deg(v, ond=1):
    i = "+" if v > 0 else ("-" if v < 0 else "")
    return x(i + "%" + tr_sayi(abs(v), ond), i + en_sayi(abs(v), ond) + "%")


def f_ek(v):
    """Eksen etiketi: 10K, 2,5K, 1,5M (gereksiz ,0 yok)."""
    if not v:
        return "0"
    for b, e in ((1e6, "M"), (1e3, "K")):
        if abs(v) >= b:
            t = ("%.1f" % (v / b)).rstrip("0").rstrip(".")
            return x(t.replace(".", ",") + e, t + e)
    return f_adet(v)


def f_k(v):
    if abs(v) >= 1e6:
        t, e = tr_sayi(v / 1e6, 1) + "M", en_sayi(v / 1e6, 1) + "M"
    elif abs(v) >= 1e3:
        o = 1 if abs(v) < 1e5 else 0
        t, e = tr_sayi(v / 1e3, o) + "K", en_sayi(v / 1e3, o) + "K"
    else:
        t, e = tr_sayi(v), en_sayi(v)
    _EN[t] = e
    return x(t, e)


def f_kf(v):
    """Isaretli kisa fark: +26,5K / -1.200"""
    i = "+" if v > 0 else ("-" if v < 0 else "")
    k_ = f_k(abs(v))
    return x(i + k_, i + (_EN.get(k_) or k_))


def _adim(vmax, hedef=5):
    import math
    if vmax <= 0:
        return 1
    a = 10 ** int(math.floor(math.log10(vmax)))
    for c in (1, 2, 2.5, 5, 10):
        if vmax / (a * c) <= hedef:
            return a * c
    return a * 10


# ---------------------------------------------------------------- kombo
def kombo(etiketler, cubuk, cizgi, cap="", genislik=880, yukseklik=270):
    """etiketler: [str] (x ile kayitli); cubuk / cizgi: (ad, renk, [deger], bicim_fn). Cubuk sol, cizgi sag eksende."""
    sol, sag, ust, alt = 58, 66, 24, 34
    iw = genislik - sol - sag; ih = yukseklik - ust - alt
    n_ = len(etiketler); bw = iw / n_
    ca, cr, cv, cf = cubuk; la, lr, lv, lf = cizgi
    am = _adim(max(cv) * 1.1); cmax = am * math.ceil(max(cv) * 1.1 / am)
    bm = _adim(max(lv) * 1.1); lmax = bm * math.ceil(max(lv) * 1.1 / bm)
    def Y1(v): return ust + ih - ih * v / cmax
    def Y2(v): return ust + ih - ih * v / lmax
    p = [_svg(genislik, yukseklik)]
    g = 0
    while g <= cmax + 1e-9:
        p.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (sol, Y1(g), genislik - sag, Y1(g)))
        p.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 8, Y1(g) + 4, f_ek(g)))
        g += am
    g = 0
    while g <= lmax + 1e-9:
        p.append('<text class="ax" x="%d" y="%.1f" text-anchor="start" fill="%s">%s</text>' % (genislik - sag + 8, Y2(g) + 4, lr, f_ek(g)))
        g += bm
    pts = []
    for i, (et, v1, v2) in enumerate(zip(etiketler, cv, lv)):
        cx = sol + bw * i + bw / 2; w = bw * 0.52
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"/>' % (cx - w / 2, Y1(v1), w, ust + ih - Y1(v1), cr))
        p.append('<text class="bv" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (cx, Y1(v1) - 6, cf(v1)))
        p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (cx, yukseklik - 12, et))
        pts.append((cx, Y2(v2)))
    p.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linejoin="round"/>' % (" ".join(("M" if i == 0 else "L") + "%.1f %.1f" % q for i, q in enumerate(pts)), lr))
    for (cx, cy), v2 in zip(pts, lv):
        p.append('<circle cx="%.1f" cy="%.1f" r="3.6" fill="%s"/>' % (cx, cy, lr))
        p.append('<text class="anl" x="%.1f" y="%.1f" text-anchor="middle" fill="%s">%s</text>' % (cx, cy - 9, lr, lf(v2)))
    nok = []
    for i, (et, v1, v2) in enumerate(zip(etiketler, cv, lv)):
        p.append('<rect class="hz" data-i="%d" x="%.1f" y="%d" width="%.1f" height="%d"/>' % (i, sol + bw * i, ust, bw, ih))
        nok.append({"b": et, "s": [{"a": ca, "r": cr, "v": cf(v1)}, {"a": la, "r": lr, "v": lf(v2)}]})
    p.append("</svg>")
    return _fig("".join(p), nok, _lej([(ca, cr, "kare"), (la, lr, "cizgi")]), cap)


# ---------------------------------------------------------------- sapmali cubuk
def sapma(satirlar, olcu, cap="", genislik=880, bicim=f_deg, pozitif="#2E7D32", negatif="#D32F2F", ek=None):
    """satirlar: [(etiket, deger)] ; sifir ekseni ortada. ek: [(ad, [deger_str])] balona eklenecek satirlar."""
    bh, ara = 22, 8; sol = SOL_ET; sag = 20
    n_ = len(satirlar); yukseklik = n_ * (bh + ara) + 30
    iw = genislik - sol - sag
    vmax = max(abs(v) for _, v in satirlar) or 1
    vmax *= 1.18
    x0 = sol + iw / 2
    def W(v): return iw / 2 * abs(v) / vmax
    p = [_svg(genislik, yukseklik)]
    p.append('<line class="grid" x1="%.1f" y1="4" x2="%.1f" y2="%d"/>' % (x0, x0, yukseklik - 20))
    nok = []
    for i, (et, v) in enumerate(satirlar):
        y = 6 + i * (bh + ara); w = W(v); renk = pozitif if v >= 0 else negatif
        rx = x0 if v >= 0 else x0 - w
        p.append('<text class="bl" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 12, y + bh * 0.7, et))
        p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" rx="3" fill="%s"/>' % (rx, y, max(w, 1.5), bh, renk))
        tx = x0 + w + 6 if v >= 0 else x0 - w - 6
        p.append('<text class="bv" x="%.1f" y="%.1f" text-anchor="%s">%s</text>' % (tx, y + bh * 0.7, "start" if v >= 0 else "end", bicim(v)))
        p.append('<rect class="hz" data-i="%d" x="%d" y="%.1f" width="%d" height="%d"/>' % (i, 0, y - ara / 2, genislik, bh + ara))
        s = [{"a": olcu, "r": renk, "v": bicim(v)}]
        for ad, degs in (ek or []):
            s.append({"a": ad, "r": "", "v": degs[i]})
        nok.append({"b": et, "s": s})
    p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">0</text>' % (x0, yukseklik - 6))
    p.append("</svg>")
    return _fig("".join(p), nok, "", cap)


# ---------------------------------------------------------------- dumbbell
def dumbbell(satirlar, a, b, cap="", genislik=880, bicim=f_k, ek=None):
    """satirlar: [(etiket, deger_a, deger_b)] ; a/b: (ad, renk). ek: [(ad, [deger_str])]"""
    bh, ara = 22, 8; sol = SOL_ET; sag = 70
    n_ = len(satirlar); ust = 6; yukseklik = n_ * (bh + ara) + ust + 26
    iw = genislik - sol - sag
    vm = max(max(v1, v2) for _, v1, v2 in satirlar)
    ad_ = _adim(vm * 1.12); vmax = ad_ * math.ceil(vm * 1.12 / ad_)
    def X(v): return sol + iw * v / vmax
    p = [_svg(genislik, yukseklik)]
    g = 0
    while g <= vmax + 1e-9:
        p.append('<line class="grid" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (X(g), ust, X(g), yukseklik - 22))
        p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(g), yukseklik - 8, f_ek(g)))
        g += ad_
    nok = []
    for i, (et, v1, v2) in enumerate(satirlar):
        cy = ust + i * (bh + ara) + bh / 2
        renk = b[1]
        p.append('<text class="bl" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 12, cy + 4, et))
        p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" stroke-opacity=".45"/>' % (X(v1), cy, X(v2), cy, "#2E7D32" if v2 >= v1 else "#D32F2F"))
        p.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (X(v1), cy, a[1]))
        p.append('<circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>' % (X(v2), cy, b[1]))
        p.append('<text class="bv" x="%.1f" y="%.1f">%s</text>' % (X(max(v1, v2)) + 10, cy + 4, bicim(v2)))
        p.append('<rect class="hz" data-i="%d" x="0" y="%.1f" width="%d" height="%d"/>' % (i, cy - (bh + ara) / 2, genislik, bh + ara))
        s = [{"a": a[0], "r": a[1], "v": bicim(v1)}, {"a": b[0], "r": b[1], "v": bicim(v2)}]
        for ad, degs in (ek or []):
            s.append({"a": ad, "r": "", "v": degs[i]})
        nok.append({"b": et, "s": s})
    p.append("</svg>")
    return _fig("".join(p), nok, _lej([(a[0], a[1], "nokta"), (b[0], b[1], "nokta")]), cap)


# ---------------------------------------------------------------- gruplu yatay cubuk
def gruplu(satirlar, seriler, cap="", genislik=880, bicim=f_pay, vurgu=None, sol=None):
    """satirlar: [(etiket, [deger...])] ; seriler: [(ad, renk)] ; vurgu: etiket -> kalin."""
    k_ = len(seriler); bh = 11 if k_ > 1 else 18; ic = 2; ara = 10
    grp = k_ * bh + (k_ - 1) * ic
    sol = sol or (SOL_ET if genislik > 600 else 170); sag = 66; ust = 4
    n_ = len(satirlar); yukseklik = n_ * (grp + ara) + ust + 4
    iw = genislik - sol - sag
    vmax = max(v for _, vs in satirlar for v in vs) or 1
    p = [_svg(genislik, yukseklik)]
    nok = []
    for i, (et, vs) in enumerate(satirlar):
        y0 = ust + i * (grp + ara)
        kal = ' style="font-weight:700"' if vurgu and et in vurgu else ""
        p.append('<text class="bl" x="%d" y="%.1f" text-anchor="end"%s>%s</text>' % (sol - 12, y0 + grp / 2 + 4, kal, et))
        for j, v in enumerate(vs):
            y = y0 + j * (bh + ic); w = iw * v / vmax
            p.append('<rect x="%d" y="%.1f" width="%.1f" height="%d" rx="2" fill="%s"/>' % (sol, y, max(w, 1.5), bh, seriler[j][1]))
            p.append('<text class="bv" x="%.1f" y="%.1f" style="font-size:%spx">%s</text>' % (sol + w + 6, y + bh - 1.5, 10.5 if k_ > 1 else 11.5, bicim(v)))
        p.append('<rect class="hz" data-i="%d" x="0" y="%.1f" width="%d" height="%d"/>' % (i, y0 - ara / 2, genislik, grp + ara))
        nok.append({"b": et, "s": [{"a": s[0], "r": s[1], "v": bicim(v)} for s, v in zip(seriler, vs)]})
    p.append("</svg>")
    return _fig("".join(p), nok, _lej([(a, r, "kare") for a, r in seriler]) if k_ > 1 else "", cap)


# ---------------------------------------------------------------- %100 yigilmis
def _acik(renk):
    """Dolgu rengi acik mi (koyu yazi gerekir mi)?"""
    try:
        r_, g_, b_ = (int(renk[i:i + 2], 16) for i in (1, 3, 5))
        return (0.299 * r_ + 0.587 * g_ + 0.114 * b_) > 150
    except Exception:
        return False


def yigin(satirlar, seriler, cap="", genislik=880, bicim=f_pay, sol=150, mutlak=False, bh=30, ara=12, esik=None):
    """satirlar: [(etiket, [pay...])] toplam ~100 ; seriler: [(ad, renk)]. mutlak: olcek en buyuk satir toplamina gore."""
    sag = 50 if mutlak else 14; ust = 4
    n_ = len(satirlar); yukseklik = n_ * (bh + ara) + ust
    iw = genislik - sol - sag
    gmax = max(sum(vs) for _, vs in satirlar) or 1
    p = [_svg(genislik, yukseklik)]
    nok = []
    for i, (et, vs) in enumerate(satirlar):
        y = ust + i * (bh + ara); top = (gmax if mutlak else sum(vs)) or 1; xx = sol
        p.append('<text class="bl" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 12, y + bh * 0.64, et))
        for j, v in enumerate(vs):
            w = iw * v / top
            p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%d" fill="%s" stroke="var(--card)" stroke-width="1"/>' % (xx, y, w, bh, seriler[j][1]))
            goster = (w > 34) if esik is None else (v >= esik and w >= 18)
            if goster and not mutlak:
                yazi = ("#10332F" if _acik(seriler[j][1]) else "#FFFFFF") if esik is not None else ("#FFFFFF" if j >= len(vs) // 2 else "#10332F")
                p.append('<text x="%.1f" y="%.1f" text-anchor="middle" style="font-size:%spx;font-weight:650" fill="%s">%s</text>' % (xx + w / 2, y + bh * 0.64, 11 if w >= 34 else 9.5, yazi, bicim(v, 0)))
            xx += w
        if mutlak:
            p.append('<text class="bv" x="%.1f" y="%.1f">%s</text>' % (xx + 6, y + bh * 0.72, bicim(sum(vs))))
        p.append('<rect class="hz" data-i="%d" x="0" y="%.1f" width="%d" height="%d"/>' % (i, y - ara / 2, genislik, bh + ara))
        nok.append({"b": et, "s": [{"a": s[0], "r": s[1], "v": bicim(v)} for s, v in zip(seriler, vs)]})
    p.append("</svg>")
    return _fig("".join(p), nok, _lej([(a, r, "kare") for a, r in seriler]), cap)


# ---------------------------------------------------------------- isi haritasi
_TD = re.compile(r'<td class="n">(.*?)</td>', re.S)
_ETK = re.compile(r"<[^>]+>")


def _deger(h):
    t = _ETK.sub("", h).strip()
    mp = re.search(r"\(\s*[+-]?%(\d[\d.]*(?:,\d+)?)", t)
    if mp:
        return float(mp.group(1).replace(".", "").replace(",", "."))
    m = re.search(r"-?%?\s?(\d[\d.]*(?:,\d+)?)", t)
    if not m or t in ("-", ""):
        return None
    try:
        return float(m.group(1).replace(".", "").replace(",", "."))
    except ValueError:
        return None


def isi(tablo_html, sutunlar=None, renk="var(--coral)", tavan=62, satir_bazli=False):
    """Tablodaki sayisal hucreleri degerine gore tonlar. sutunlar: 0 tabanli td indeksleri (None = tum sayisal)."""
    bas, govde_son = tablo_html.split("<tbody>", 1)
    govde, son = govde_son.split("</tbody>", 1)
    satirlar = re.findall(r"<tr>(.*?)</tr>", govde, re.S)
    hucreler = [re.findall(r"<td(?: class=\"n\")?>.*?</td>", s, re.S) for s in satirlar]
    def uygun(j, h): return (sutunlar is None or j in sutunlar) and h.startswith('<td class="n">')
    tum = [_deger(h) for hs in hucreler for j, h in enumerate(hs) if uygun(j, h)]
    tum = [v for v in tum if v is not None]
    gmax = max(tum) if tum else 1
    yeni = []
    for hs in hucreler:
        smax = max([v for v in (_deger(h) for j, h in enumerate(hs) if uygun(j, h)) if v is not None] or [1]) if satir_bazli else gmax
        out = []
        for j, h in enumerate(hs):
            v = _deger(h) if uygun(j, h) else None
            if v is not None and smax:
                a = round(tavan * v / smax)
                if a >= 4:
                    h = h.replace('<td class="n">', '<td class="n hm" style="background:color-mix(in srgb,%s %d%%,transparent)">' % (renk, a), 1)
            out.append(h)
        yeni.append("<tr>%s</tr>" % "".join(out))
    return bas + "<tbody>" + "".join(yeni) + "</tbody>" + son


# ---------------------------------------------------------------- sacilim
def sacilim(noktalar, x_ad, y_ad, renkler, cap="", genislik=880, yukseklik=380, xbicim=f_k, ybicim=f_k, ek=None):
    """noktalar: [(etiket, xv, yv, grup)] ; logaritmik iki eksen ; renkler: [(grup, ad, renk)]."""
    sol, sag, ust, alt = 62, 24, 16, 40
    iw = genislik - sol - sag; ih = yukseklik - ust - alt
    xs = [p_[1] for p_ in noktalar]; ys = [p_[2] for p_ in noktalar]
    lx0, lx1 = math.floor(math.log10(min(xs))), math.ceil(math.log10(max(xs)))
    ly0, ly1 = math.floor(math.log10(min(ys))), math.ceil(math.log10(max(ys)))
    def X(v): return sol + iw * (math.log10(v) - lx0) / (lx1 - lx0)
    def Y(v): return ust + ih - ih * (math.log10(v) - ly0) / (ly1 - ly0)
    rk = {g: r for g, _, r in renkler}
    p = [_svg(genislik, yukseklik)]
    for e in range(lx0, lx1 + 1):
        for m in ((1, 2, 5) if e < lx1 else (1,)):
            v = m * 10 ** e
            p.append('<line class="grid" x1="%.1f" y1="%d" x2="%.1f" y2="%d"/>' % (X(v), ust, X(v), ust + ih))
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (X(v), ust + ih + 16, f_ek(v)))
    for e in range(ly0, ly1 + 1):
        for m in ((1, 2, 5) if e < ly1 else (1,)):
            v = m * 10 ** e
            p.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (sol, Y(v), genislik - sag, Y(v)))
            p.append('<text class="ax" x="%d" y="%.1f" text-anchor="end">%s</text>' % (sol - 8, Y(v) + 4, f_ek(v)))
    p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (sol + iw / 2, yukseklik - 4, x_ad))
    p.append('<text class="ax" x="14" y="%.1f" text-anchor="middle" transform="rotate(-90 14 %.1f)">%s</text>' % (ust + ih / 2, ust + ih / 2, y_ad))
    nok = []; kutular = []
    def cakisir(b):
        return any(not (b[2] < k[0] or b[0] > k[2] or b[3] < k[1] or b[1] > k[3]) for k in kutular)
    for i, (et, xv, yv, g) in enumerate(noktalar):
        cx, cy = X(xv), Y(yv); w_ = 6.2 * len(et)
        p.append('<circle cx="%.1f" cy="%.1f" r="5.5" fill="%s" fill-opacity=".85"/>' % (cx, cy, rk[g]))
        adaylar = [(cx + 8, cy + 4, "start"), (cx - 8, cy + 4, "end"), (cx, cy - 10, "middle"), (cx, cy + 17, "middle")]
        if cx > sol + iw * 0.8: adaylar = [adaylar[1], adaylar[0]] + adaylar[2:]
        sec = adaylar[0]
        for tx, ty, an in adaylar:
            x0_ = tx if an == "start" else (tx - w_ if an == "end" else tx - w_ / 2)
            b_ = (x0_, ty - 10, x0_ + w_, ty + 2)
            if not cakisir(b_) and x0_ >= sol and x0_ + w_ <= genislik:
                sec = (tx, ty, an); break
        tx, ty, an = sec; x0_ = tx if an == "start" else (tx - w_ if an == "end" else tx - w_ / 2)
        kutular.append((x0_, ty - 10, x0_ + w_, ty + 2)); kutular.append((cx - 6, cy - 6, cx + 6, cy + 6))
        p.append('<text class="anl" x="%.1f" y="%.1f" text-anchor="%s" fill="var(--ink)" style="font-weight:500">%s</text>' % (tx, ty, an, et))
        p.append('<rect class="hz" data-i="%d" x="%.1f" y="%.1f" width="16" height="16" rx="8"/>' % (i, cx - 8, cy - 8))
        s = [{"a": x_ad, "r": rk[g], "v": xbicim(xv)}, {"a": y_ad, "r": "", "v": ybicim(yv)}]
        for ad, degs in (ek or []):
            s.append({"a": ad, "r": "", "v": degs[i]})
        nok.append({"b": et, "s": s})
    p.append("</svg>")
    return _fig("".join(p), nok, _lej([(a, r, "nokta") for _, a, r in renkler]), cap)


# ---------------------------------------------------------------- halka (pay dagilimi)
def halka(dilimler, cap="", merkez=None, genislik=880, bicim=None, deger_bicim=None, r_dis=96, r_ic=58, alt=None):
    """dilimler: [(etiket, deger, renk)] ; paylar toplamdan hesaplanir. Solda halka, sagda etiket + pay + deger listesi.
    merkez: (ust_yazi, alt_yazi) halkanin ortasina; bicim: pay bicimi (varsayilan f_pay, 1 ondalik).
    alt: her dilim icin [(ad, deger_metni)] alt kirilim; balonda pay ve degerin altinda listelenir."""
    bicim = bicim or (lambda v: f_pay(v, 1))
    top = float(sum(v for _, v, _ in dilimler)) or 1.0
    n_ = len(dilimler); satir_h = 26
    yukseklik = max(2 * r_dis + 24, n_ * satir_h + 20)
    cx, cy = r_dis + 14, yukseklik / 2
    p = [_svg(genislik, yukseklik)]
    nok = []; a0 = -math.pi / 2
    def _nokta(r, a): return cx + r * math.cos(a), cy + r * math.sin(a)
    def _yay(a1, a2):
        if a2 - a1 >= 2 * math.pi - 1e-6: a2 = a1 + 2 * math.pi - 1e-4
        b = 1 if (a2 - a1) > math.pi else 0
        x1, y1 = _nokta(r_dis, a1); x2, y2 = _nokta(r_dis, a2); x3, y3 = _nokta(r_ic, a2); x4, y4 = _nokta(r_ic, a1)
        return "M%.2f %.2f A%d %d 0 %d 1 %.2f %.2f L%.2f %.2f A%d %d 0 %d 0 %.2f %.2f Z" % (x1, y1, r_dis, r_dis, b, x2, y2, x3, y3, r_ic, r_ic, b, x4, y4)
    yollar, bantlar, yay_bant = [], [], []
    lx = cx + r_dis + 46; y0 = cy - n_ * satir_h / 2 + satir_h / 2
    for i, (et, v, renk) in enumerate(dilimler):
        pay = 100.0 * v / top; a1 = a0 + 2 * math.pi * v / top
        d_ = _yay(a0, a1)
        yollar.append('<path d="%s" fill="%s" stroke="var(--card)" stroke-width="1.5"/>' % (d_, renk))
        yay_bant.append('<path class="hz" data-i="%d" d="%s"/>' % (i, d_))
        y = y0 + i * satir_h
        p.append('<rect x="%.1f" y="%.1f" width="12" height="12" rx="2" fill="%s"/>' % (lx, y - 9, renk))
        p.append('<text class="bl" x="%.1f" y="%.1f">%s</text>' % (lx + 20, y + 1.5, et))
        p.append('<text class="bv" x="%.1f" y="%.1f" text-anchor="end" style="font-weight:700">%s</text>' % (genislik - 120, y + 1.5, bicim(pay)))
        if deger_bicim:
            p.append('<text class="bl" x="%.1f" y="%.1f" text-anchor="end">%s</text>' % (genislik - 8, y + 1.5, deger_bicim(v)))
        bantlar.append('<rect class="hz" data-i="%d" x="%.1f" y="%.1f" width="%.1f" height="%d"/>' % (i, lx - 6, y - satir_h / 2 - 1, genislik - lx, satir_h))
        s_ = [{"a": x("Pay", "Share"), "r": renk, "v": bicim(pay)}]
        if deger_bicim: s_.append({"a": x("Değer", "Value"), "r": "", "v": deger_bicim(v)})
        for a_, v_ in ((alt or [None] * n_)[i] or []): s_.append({"a": a_, "r": "", "v": v_})
        nok.append({"b": et, "s": s_})
        a0 = a1
    p[1:1] = yollar
    if merkez:
        p.append('<text x="%.1f" y="%.1f" text-anchor="middle" style="font-size:20px;font-weight:700;fill:var(--ink);pointer-events:none">%s</text>' % (cx, cy + 2, merkez[0]))
        if len(merkez) > 1 and merkez[1]:
            p.append('<text class="bl" x="%.1f" y="%.1f" text-anchor="middle" style="font-size:11px;pointer-events:none">%s</text>' % (cx, cy + 19, merkez[1]))
    p += bantlar + yay_bant   # once lejant satirlari (dikdortgen), sonra halka dilimleri
    p.append("</svg>")
    return _fig("".join(p), nok, "", cap)


def _koyu(renk):
    try:
        r, g, b = int(renk[1:3], 16), int(renk[3:5], 16), int(renk[5:7], 16)
        return 0.299 * r + 0.587 * g + 0.114 * b < 150
    except Exception:
        return False


# ---------------------------------------------------------------- kombo2: gruplu cubuk + cizgi + kesikli cizgi, uc eksen
def kombo2(etiketler, seriler, cap="", genislik=880, yukseklik=300, etiket_goster=False, ust_etiket=None, dondur=False, ek_satir=None, min_gen=None):
    """etiketler: [str] (x ile kayitli). seriler: [dict(ad, renk, deger=[v|None], tip='cubuk'|'cizgi'|'kesik', eksen='sol'|'sag'|'sag2',
    bicim=fn, ters=False, eksen_ad=str)]. Ayni eksendeki cubuklar yan yana gruplanir; None degerler bosluk birakir.
    ters=True eksende kucuk deger ustte cizilir (ortalama sira icin). ortu=True olan cubuk bir onceki cubugun uzerine, ayni yerde ve tabandan cizilir
    (toplamin icindeki pay). ust_etiket: her x icin cubuk grubunun ustune her zaman yazilan metin. dondur: x etiketleri egik yazilir (cok sayida x).
    ek_satir: her x icin balona eklenecek [(ad, metin)]. min_gen: genis grafiklerde asgari piksel genisligi (kendi icinde kaydirilir).
    Tum degerler 'dl' sinifli gizli etiket olarak cizilir; grafik ustundeki Degerler dugmesi bunlari acar."""
    eksenler = []
    for s_ in seriler:
        if s_.get("eksen", "sol") not in eksenler: eksenler.append(s_.get("eksen", "sol"))
    sol, ust, alt = (62 + (70 if dondur else 0)), 30 + (14 if ust_etiket else 0), (96 if dondur else 34)
    sag = 20 + (52 if "sag" in eksenler else 0) + (52 if "sag2" in eksenler else 0)
    iw = genislik - sol - sag; ih = yukseklik - ust - alt
    n_ = len(etiketler); bw = iw / n_
    olc = {}
    for e in eksenler:
        vs = [v for s_ in seriler if s_.get("eksen", "sol") == e for v in s_["deger"] if v is not None]
        ters = any(s_.get("ters") for s_ in seriler if s_.get("eksen", "sol") == e)
        if ters:
            lo, hi = min(vs), max(vs); pad = max(0.5, (hi - lo) * 0.25); lo = max(0, math.floor((lo - pad) * 2) / 2); hi = math.ceil((hi + pad) * 2) / 2
            olc[e] = (lo, hi, True)
        else:
            a_ = _adim(max(vs) * 1.08); olc[e] = (0, a_ * math.ceil(max(vs) * 1.08 / a_), False)
    def Y(e, v):
        lo, hi, t = olc[e]
        f = (v - lo) / (hi - lo) if hi > lo else 0
        return ust + ih * f if t else ust + ih - ih * f
    p = [_svg(genislik, yukseklik)]; dlp = []   # deger etiketleri en sonda cizilir: cubuk ve cizgilerin ustunde kalir
    # eksenler
    ex = {"sol": sol - 8, "sag": genislik - sag + 8, "sag2": genislik - sag + 60}
    for e in eksenler:
        lo, hi, t = olc[e]; renk = next(s_["renk"] for s_ in seriler if s_.get("eksen", "sol") == e)
        adim = _adim(hi - lo) if not t else max(0.5, _adim(hi - lo))
        g = lo
        while g <= hi + 1e-9:
            if e == "sol": p.append('<line class="grid" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>' % (sol, Y(e, g), genislik - sag, Y(e, g)))
            et = (("%.1f" % g).rstrip("0").rstrip(".").replace(".", ",") if t else f_ek(g))
            if t: et = x(et, et.replace(",", "."))
            p.append('<text class="ax" x="%d" y="%.1f" text-anchor="%s"%s>%s</text>' % (ex[e], Y(e, g) + 4, "end" if e == "sol" else "start", "" if e == "sol" else ' fill="%s"' % renk, et))
            g += adim
        ad_ = next((s_.get("eksen_ad") for s_ in seriler if s_.get("eksen", "sol") == e and s_.get("eksen_ad")), None)
        if ad_:   # eksen başlığı: sol eksende sola, en dıştaki sağ eksende sağa yaslı (uzun başlıklar kırpılmaz)
            if e == "sol": ax_, an_ = 4, "start"
            elif e == "sag2" or "sag2" not in eksenler: ax_, an_ = genislik - 4, "end"
            else: ax_, an_ = ex[e], "start"
            p.append('<text class="ax" x="%d" y="%d" text-anchor="%s" style="font-weight:600"%s>%s</text>' % (ax_, ust - 12, an_, "" if e == "sol" else ' fill="%s"' % renk, ad_))
    cubuklar = [s_ for s_ in seriler if s_.get("tip", "cizgi") == "cubuk"]
    grup = [s_ for s_ in cubuklar if not s_.get("ortu")]
    nb = len(grup); gw = bw * (0.72 if nb > 1 else 0.52); w1 = gw / max(1, nb)
    for i, et in enumerate(etiketler):
        cx = sol + bw * i + bw / 2; ust_y = None; j = -1
        # ortu cubugu (toplamin icindeki pay): etiketinin kapladigi yerin ustu hesaplanir; taban cubugun etiketi bunun ustunden baslar
        ov_y = None
        for s_ in cubuklar:
            if not s_.get("ortu") or s_["deger"][i] is None or not s_.get("dl", True): continue
            yv = Y(s_.get("eksen", "sol"), s_["deger"][i]); hv = ust + ih - yv; uz = 5.8 * len(s_["bicim"](s_["deger"][i])) + 4
            yo = (yv - 4) if (w1 < 36 and hv >= max(34, uz)) or (uz <= w1 + 2 and hv >= 16) else (yv - 18)
            ov_y = yo if ov_y is None else min(ov_y, yo)
        for s_ in cubuklar:
            v = s_["deger"][i]
            if not s_.get("ortu"): j += 1
            if v is None: continue
            e = s_.get("eksen", "sol"); x0 = cx - gw / 2 + max(0, j) * w1
            k_ = seriler.index(s_)
            p.append('<rect class="sr" data-k="%d" x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2.5" fill="%s"/>' % (k_, x0 + 1, Y(e, v), max(1, w1 - 2), max(0, ust + ih - Y(e, v)), s_["renk"]))
            if not s_.get("ortu"): ust_y = Y(e, v) if ust_y is None else min(ust_y, Y(e, v))
            if s_.get("dl", True):   # cubuk degeri cubugun icinde, tabana yakin (cizgi etiketleriyle cakismaz); koyu cubukta beyaz yazi
                ek = " dlo" if s_.get("ortu") else ""
                taban = ust + ih if (s_.get("ortu") or ov_y is None) else min(ust + ih, ov_y + 5)   # ustune ortu binen cubukta etiket ortu etiketinin ustunden baslar
                hv = taban - Y(e, v); uz = 5.8 * len(s_["bicim"](v)) + 4
                koyu = _koyu(s_["renk"]) and (s_.get("ortu") or ov_y is None)
                if w1 < 36 and hv >= max(34, uz):   # dar cubuk: deger cubugun icinde dikey yazilir
                    xx = x0 + w1 / 2 + 3.5; yb = taban - 5
                    dlp.append('<text class="dl %s%s" data-k="%d" x="%.1f" y="%.1f" transform="rotate(-90 %.1f %.1f)" text-anchor="start">%s</text>' % ("dli" if koyu else "dlb", ek, k_, xx, yb, xx, yb, s_["bicim"](v)))
                elif uz <= w1 + 2 and hv >= 16:   # yazi cubuga sigiyor: cubugun icinde, tabana yakin
                    dlp.append('<text class="dl %s%s" data-k="%d" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % ("dli" if koyu else "dlb", ek, k_, x0 + w1 / 2, taban - 6, s_["bicim"](v)))
                elif w1 < 36 and not s_.get("ortu"):   # dar cubukta sigmiyor: cubugun ustunde dikey, kendi sutununda kalir
                    xx = x0 + w1 / 2 + 3.5; yb = Y(e, v) - 4
                    dlp.append('<text class="dl dlb dlu%s" data-k="%d" x="%.1f" y="%.1f" transform="rotate(-90 %.1f %.1f)" text-anchor="start">%s</text>' % (ek, k_, xx, yb, xx, yb, s_["bicim"](v)))
                else:   # sigmiyor: cubugun ustunde, koyu yazi
                    dlp.append('<text class="dl dlb dlu%s" data-k="%d" x="%.1f" y="%.1f" text-anchor="middle">%s</text>' % (ek, k_, x0 + w1 / 2, Y(e, v) - 4, s_["bicim"](v)))
            if etiket_goster: p.append('<text class="bv" x="%.1f" y="%.1f" text-anchor="middle" style="font-size:10px">%s</text>' % (x0 + w1 / 2, Y(e, v) - 4, s_["bicim"](v)))
        if ust_etiket and ust_etiket[i] and ust_y is not None:
            p.append('<text class="bv" x="%.1f" y="%.1f" text-anchor="middle" style="font-size:10.5px;font-weight:700">%s</text>' % (cx, ust_y - 6, ust_etiket[i]))
        if dondur:
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="end" transform="rotate(-55 %.1f %d)" style="font-size:9.5px">%s</text>' % (cx + 3, ust + ih + 12, cx + 3, ust + ih + 12, et))
        elif " " in et and 6.0 * len(et) > bw - 4:   # sigmayan "Oca 25" tipi etiket iki satira bolunur (ay / yil); parcalar ceviri kaydina eklenir
            a_, _, b_ = et.partition(" "); en_ = EK.get(" ".join(et.split()), "")
            if " " in en_: EK.setdefault(a_, en_.partition(" ")[0]); EK.setdefault(b_, en_.partition(" ")[2])
            elif a_ in _AY_TR: EK.setdefault(a_, _AY_EN[_AY_TR.index(a_)])
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle"><tspan>%s</tspan><tspan x="%.1f" dy="12">%s</tspan></text>' % (cx, yukseklik - 19, a_, cx, b_))
        else:
            p.append('<text class="ax" x="%.1f" y="%d" text-anchor="middle">%s</text>' % (cx, yukseklik - 12, et))
    for s_ in seriler:
        if s_.get("tip", "cizgi") == "cubuk": continue
        e = s_.get("eksen", "sol"); seg = []; yol_ = []
        for i, v in enumerate(s_["deger"]):
            if v is None:
                if seg: yol_.append(seg); seg = []
                continue
            seg.append((sol + bw * i + bw / 2, Y(e, v)))
        if seg: yol_.append(seg)
        das = ' stroke-dasharray="6 4"' if s_.get("tip") == "kesik" else ""
        k_ = seriler.index(s_)
        for sg in yol_:
            p.append('<path class="sr" data-k="%d" d="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-linejoin="round"%s/>' % (k_, " ".join(("M" if k == 0 else "L") + "%.1f %.1f" % q for k, q in enumerate(sg)), s_["renk"], das))
            for q in sg: p.append('<circle class="sr" data-k="%d" cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (k_, q[0], q[1], s_["renk"]))
        if s_.get("dl", True):
            alt_ = s_.get("tip") == "kesik"
            for i, v in enumerate(s_["deger"]):
                if v is None: continue
                dlp.append('<text class="dl dll" data-k="%d"%s x="%.1f" y="%.1f" text-anchor="middle" fill="%s">%s</text>' % (k_, ' data-alt="1"' if alt_ else "", sol + bw * i + bw / 2, Y(e, v) + (15 if alt_ else -8), s_["renk"], s_["bicim"](v)))
    p += dlp
    nok = []
    for i, et in enumerate(etiketler):
        p.append('<rect class="hz" data-i="%d" x="%.1f" y="%d" width="%.1f" height="%d"/>' % (i, sol + bw * i, ust, bw, ih))
        nok.append({"b": et, "s": [{"a": s_["ad"], "r": s_["renk"], "v": s_["bicim"](s_["deger"][i]) if s_["deger"][i] is not None else "-"} for s_ in seriler]
                    + [{"a": a_, "r": "", "v": v_} for a_, v_ in ((ek_satir or [None] * n_)[i] or [])]})
    p.append("</svg>")
    gz = [k_ for k_, s_ in enumerate(seriler) if s_.get("gizli")]
    lej = '<div class="legend">' + "".join(
        ('<span class="lg-t lg-s%s" data-k="%d" role="button" tabindex="0" aria-pressed="%s"><i class="%s" style="%s"></i>%s</span>' % (
            " off" if k_ in gz else "", k_, "false" if k_ in gz else "true", "kesik" if s_.get("tip") == "kesik" else ("kare" if s_.get("tip") == "cubuk" else "cizgi"),
            ("border-top-color:%s" % s_["renk"]) if s_.get("tip") == "kesik" else ("background:%s" % s_["renk"]), s_["ad"])) for k_, s_ in enumerate(seriler)) + '</div>'
    svg_ = "".join(p)
    if min_gen: svg_ = svg_.replace('<svg class="chart"', '<svg class="chart genis" style="min-width:%dpx"' % min_gen, 1)
    if gz:   # baslangicta kapali seriler
        for k_ in gz: svg_ = svg_.replace('data-k="%d"' % k_, 'data-k="%d" style="display:none"' % k_)
    fig = _fig(svg_, nok, lej, cap)
    if gz: fig = fig.replace('"tip": "genel"', '"tip": "genel", "gizli": %s' % json.dumps(gz), 1)
    return fig


def cift(cizgi_html, cubuk_html):
    """Ayni veri icin cizgi ve cubuk gorunumu; dugmeyle gecis (rapor_js .gcift)."""
    return ('<div class="gcift"><div class="gcift-b" role="group" aria-label="%s"><button type="button" aria-pressed="true" data-g="0">%s</button><button type="button" aria-pressed="false" data-g="1">%s</button></div>'
            '<div class="gcift-p" data-g="0">%s</div><div class="gcift-p" data-g="1" hidden>%s</div></div>') % (x("Grafik türü", "Chart type"), x("Çizgi", "Line"), x("Çubuk", "Bar"), cizgi_html, cubuk_html)
