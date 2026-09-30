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
                    if _MARKA.fullmatch(a) or _MARKA.fullmatch(b):
                        EK.setdefault(a, a); continue   # marka adi her iki dilde aynidir
                    EK.setdefault(a, b)   # parca kaydi yalnizca yedektir; butun blok dil katmaninda tek parca cevrilir
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


_SAYI_TOK = _re.compile(r'(?<![\w>#"=/-])([+\-−]?(?:%\d[\d.,]*|\d[\d.,]*(?:\s?(?:K|M|x|TL|USD|bn|kat|\+))?%?|\d[\d.,]*-\d[\d.,]*(?:\s?(?:K|M|x|TL))?%?))(?![\w<%-])')
_TARIH = _re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}$|^(?:19|20)\d{2}$|^\d{1,2}$')

_MARKA = _re.compile(r"(?<![\w>])(VitrA|Artema|Trendyol|Hepsiburada|Koçtaş|Creavit|Kalekim|Kale|Turkuaz|Turavit|Geberit|Grohe|Hansgrohe|Duravit|Bauhaus|IKEA|Banyomarka|Banyoline|Banyomega|Akakçe|Cimri|Serel|Visam|NKP|Durul|KUSTAR|Amazon TR|Amazon|n11|YouTube|Şikayetvar|Google Shopping|Google|Tekzen|Evidea|Roca|Kohler|Eca|E\.C\.A\.|Tekzen|Vivense|Şok|Aras Kargo|Ceva)(?![\w])")
_UST_TR = _re.compile(r"\b(en (?:yüksek|düşük|çok|az|büyük|küçük|geniş|dar|dirençli|sınırlı|hızlı|yavaş|ucuz|pahalı|derin|güçlü|yoğun|kalabalık|belirgin) [\wçğıöşüÇĞİÖŞÜ'’-]+)")
_UST_EN = _re.compile(r"\b((?:the )?(?:highest|lowest|largest|smallest|biggest|most|least|widest|narrowest|fastest|slowest|cheapest|strongest|weakest|deepest|densest|busiest|clearest) [\w'’-]+)")
def _vurgu(t, en=False):
    """Etiket disindaki marka adlari <b class=mk>, ustunluk ifadeleri <span class=hl>."""
    parca = _ETIKET.split(t); etk = _ETIKET.findall(t); out = []
    ust = _UST_EN if en else _UST_TR
    for i, p_ in enumerate(parca):
        p_ = _MARKA.sub(lambda m: '<b class="mk">%s</b>' % m.group(1), p_)
        p_ = ust.sub(lambda m: '<span class="hl">%s</span>' % m.group(1), p_)
        out.append(p_)
        if i < len(etk): out.append(etk[i])
    return "".join(out)

def _kalin(t):
    """Etiket disindaki sayisal ifadeleri <b> icine alir; yil, tarih ve tek-iki haneli sayilar haric."""
    parca = _ETIKET.split(t); etk = _ETIKET.findall(t)
    def _b(m):
        s = m.group(1)
        if _TARIH.match(s) or s.strip() in ("-", "+"): return s
        return "<b>%s</b>" % s
    out = []
    for i, p_ in enumerate(parca):
        out.append(_SAYI_TOK.sub(_b, p_))
        if i < len(etk): out.append(etk[i])
    return "".join(out)

def _kalin_cift(tr, en):
    a, b = _kalin(_vurgu(tr)), _kalin(_vurgu(en, True))
    if a.count("<b") != b.count("<b") or a.count("<span") != b.count("<span"):
        a, b = _kalin(tr), _kalin(en)
    return (a, b) if a.count("<b") == b.count("<b") else (tr, en)

_CUMLE = _re.compile(r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ"“(\d])')

def _cumleler(t):
    return [c for c in _CUMLE.split(t) if c.strip()]

def insight(tr, en, *kodlar):
    ref = R(*kodlar) if kodlar else ""
    ct, ce = _cumleler(tr), _cumleler(en)
    if len(ct) >= 3 and len(ct) == len(ce):
        bas = x(*_kalin_cift(ct[0], ce[0]))
        maddeler = "".join("<li>%s</li>" % x(*_kalin_cift(a, b)) for a, b in zip(ct[1:], ce[1:]))
        return '<div class="insight"><p>%s</p><ul class="ins-li">%s</ul><span class="ins-ref">%s</span></div>' % (bas, maddeler, ref)
    return '<div class="insight"><p>%s%s</p></div>' % (x(*_kalin_cift(tr, en)), ref)


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
