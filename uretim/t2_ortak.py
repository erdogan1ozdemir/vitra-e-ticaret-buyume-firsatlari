# -*- coding: utf-8 -*-
"""Ikinci tur icerigi icin ortak yardimcilar.

x(tr, en)  metin parcasini dondurur ve Ingilizce karsiligini EK sozlugune yazar.
R(*kod)    kaynak atfi yer tutucusu; rapor3 numaralandirip Kaynakca'ya baglar.
"""
import html as _h
import re as _re

_SAYISAL = _re.compile(r'^[\d\s.,%+\-–·/()|&;:x€$₺"\'’]*$')
_YUZDE = _re.compile(r'([+\-−])?%(\d[\d.,]*)')
_ONDALIK = _re.compile(r'(?<=\d),(?=\d)')
_BINLIK = _re.compile(r'(?<![\d,])\d{1,3}(?:\.\d{3})+(?![\d.])')


def _sayi_en(t):
    t = _YUZDE.sub(lambda m: (m.group(1) or "") + m.group(2) + "%", t)
    t = _ONDALIK.sub(".", t)
    return _BINLIK.sub(lambda m: m.group(0).replace(".", ","), t)


def sayi(v):
    """Harf iceren sayisal ifadeyi (EUR, K, Mn) Ingilizce bicimiyle kaydeder."""
    d = _duz(v)
    if d and not _SAYISAL.match(d):
        EK.setdefault(d, _sayi_en(d.replace("Mn", "M").replace("Mrd.", "bn")))
    return v

EK = {}
_CAKISMA = []


def _duz(t):
    return " ".join(_h.unescape(t).split())


_ETIKET = _re.compile(r"<[^>]+>")


def _kaydet(k, v):
    if k in EK and EK[k] != v:
        _CAKISMA.append((k, EK[k], v))
    EK[k] = v


def x(tr, en):
    k, v = _duz(tr), _sayi_en(_duz(en))
    _kaydet(k, v)
    # Satir ici etiket (<b>, <span class="up">) iceren metinlerde tarayici metni
    # parcalara boler; parcalar konumsal olarak eslenir ve ayrica kaydedilir.
    if "<" in k:
        pk, pv = _ETIKET.split(k), _ETIKET.split(v)
        if len(pk) == len(pv):
            for a, b in zip(pk, pv):
                a, b = a.strip(), b.strip()
                if a and not _SAYISAL.match(a):
                    _kaydet(a, b)
        else:
            _CAKISMA.append((k[:60], "parça sayısı", "%d/%d" % (len(pk), len(pv))))
    return tr


def R(*kodlar):
    return "[[ref:%s]]" % ",".join(kodlar)


def kaynak(tr, en, *kodlar):
    return '<p class="src">%s%s</p>' % (x("Kaynak: " + tr, "Source: " + en), R(*kodlar) if kodlar else "")


def th(tr, en, ac_tr, ac_en, sayi=False):
    x(ac_tr, ac_en)
    return '<th%s data-t="%s" tabindex="0"><span class="q">%s</span></th>' % (
        ' class="n"' if sayi else "", _h.escape(ac_tr, quote=True), x(tr, en))


def tablo(basliklar, satirlar, sinif=""):
    bas = "".join(basliklar)
    govde = "".join("<tr>%s</tr>" % "".join(
        ('<td class="n">%s</td>' % h[1:]) if isinstance(h, str) and h.startswith("\x01") else "<td>%s</td>" % h
        for h in s) for s in satirlar)
    return '<div class="tw%s"><table><thead><tr>%s</tr></thead><tbody>%s</tbody></table></div>' % (
        (" " + sinif) if sinif else "", bas, govde)


def n(v):
    """Sayisal hucre isareti."""
    return "\x01" + sayi(v)


def insight(tr, en, *kodlar):
    return '<div class="insight"><p>%s%s</p></div>' % (x(tr, en), R(*kodlar) if kodlar else "")


def p(tr, en, *kodlar, sinif=None):
    return '<p%s>%s%s</p>' % ((' class="%s"' % sinif) if sinif else "", x(tr, en), R(*kodlar) if kodlar else "")


def h3(tr, en):
    return "<h3>%s</h3>" % x(tr, en)


def li(tr, en, *kodlar):
    return "<li>%s%s</li>" % (x(tr, en), R(*kodlar) if kodlar else "")


def kpi(v, tr, en, *kodlar):
    return '<div class="kpi"><div class="v">%s</div><div class="k">%s%s</div></div>' % (
        sayi(v), x(tr, en), R(*kodlar) if kodlar else "")


def olcek(deger, azami, renk="var(--teal)"):
    return ("<span class='olcek'><span class='bar-mini' style='width:%.1f%%;background:%s'></span></span>"
            % (max(3.0, 100.0 * deger / azami), renk))


VAR = '<span class="badge b-var">Var</span>'
YOK = '<span class="badge b-yok">Yok</span>'
