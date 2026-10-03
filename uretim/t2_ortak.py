# -*- coding: utf-8 -*-
"""Ikinci tur icerigi icin ortak yardimcilar.

x(tr, en)  metin parcasini dondurur ve Ingilizce karsiligini EK sozlugune yazar.
R(*kod)    kaynak atfi yer tutucusu; rapor3 numaralandirip Kaynakca'ya baglar.
"""
import html as _h
import re as _re

_SAYISAL = _re.compile(r'^[\d\s.,%+\-–·/()|&;:x€$₺"\'’]*$')
_YUZDE = _re.compile(r'([+\-−])?%(\d+(?:[.,]\d+)*)')
_ONDALIK = _re.compile(r'(?<=\d),(?=\d)')
_BINLIK = _re.compile(r'(?<![\d,])\d{1,3}(?:\.\d{3})+(?![\d.])')


_FIIL_EKSI = _re.compile(r"\b(contracted|fell|declined|dropped|decreased|shrank|down|lost|a contraction of|a decline of|a drop of)( (?:<[^>]+>)*)[-−](?=\d)")
_FIIL_ARTI = _re.compile(r"\b(grew|rose|increased|climbed|gained|up|only|growth of|an increase of|a rise of)( (?:<[^>]+>)*)\+(?=\d)")
def _sayi_en(t):
    t = _YUZDE.sub(lambda m: (m.group(1) or "") + m.group(2) + "%", t)
    t = _FIIL_EKSI.sub(r"\1\2", t); t = _FIIL_ARTI.sub(r"\1\2", t)
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


from tr_ek import duzelt as _tr_ek, marka as _marka, marka_tek as _mtek
def x(tr, en):
    tr = _tr_ek(_mtek(_marka(tr))); en = _mtek(_marka(en))
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


_SAYI_TOK = _re.compile(r'(?<![\w>#"=/-])([+\-−]?(?:%\d+(?:[.,]\d+)*|\d+(?:[.,]\d+)*(?:\s?(?:K|M|x|TL|USD|bn|kat|\+))?%?|\d+(?:[.,]\d+)*-\d+(?:[.,]\d+)*(?:\s?(?:K|M|x|TL))?%?))(?![\w<%-])')
_TARIH = _re.compile(r'^\d{1,2}\.\d{1,2}\.\d{4}$|^(?:19|20)\d{2}$|^\d{1,2}$')

_MARKA = _re.compile(r"(?<![\w>])(VitrA|Artema|Trendyol|Hepsiburada|Koçtaş|Creavit|Kalekim|Kale|Turkuaz|Turavit|Geberit|Grohe|Hansgrohe|Duravit|Bauhaus|IKEA|Banyomarka|Banyoline|Banyomega|Akakçe|Cimri|Serel|Visam|NKP|Durul|KUSTAR|Amazon TR|Amazon|n11|YouTube|Şikayetvar|Google Shopping|Google|Tekzen|Evidea|Roca|Kohler|Eca|E\.C\.A\.|Tekzen|Vivense|Şok|Aras Kargo|Ceva)(?![\w])")
_UST_TR = _re.compile(r"\b(en (?:yüksek|düşük|çok|az|büyük|küçük|geniş|dar|dirençli|sınırlı|hızlı|yavaş|ucuz|pahalı|derin|güçlü|yoğun|kalabalık|belirgin) [\wçğıöşüÇĞİÖŞÜ'’-]+)")
_UST_EN = _re.compile(r"\b((?:the )?(?:highest|lowest|largest|smallest|biggest|most|least|widest|narrowest|fastest|slowest|cheapest|strongest|weakest|deepest|densest|busiest|clearest) [\w'’-]+)")
_TIRNAK = _re.compile(r'("[^"]*"|“[^”]*”)')
def _disinda(p_, rx, fn):
    """Tirnak icindeki arama ifadelerine dokunmadan yalnizca tirnak disindaki metinde degistirir."""
    return "".join(q if (q.startswith('"') or q.startswith("“")) else rx.sub(fn, q) for q in _TIRNAK.split(p_))
def _vurgu(t, en=False):
    """Etiket disindaki marka adlari <b class=mk>, ustunluk ifadeleri <span class=hl>."""
    parca = _ETIKET.split(t); etk = _ETIKET.findall(t); out = []
    ust = _UST_EN if en else _UST_TR
    for i, p_ in enumerate(parca):
        p_ = _disinda(p_, _MARKA, lambda m: '<b class="mb">%s</b>' % m.group(1))
        p_ = _disinda(p_, ust, lambda m: '<span class="hl">%s</span>' % m.group(1))
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
        out.append(_disinda(p_, _SAYI_TOK, _b))
        if i < len(etk): out.append(etk[i])
    return "".join(out)

_BOLD = _re.compile(r"<b(?: [^>]*)?>(.*?)</b>")
def _sira_ayni(a, b):
    """Kalin parcalar iki dilde ayni sirada mi? Sayilar TR->EN bicimine cevrilerek karsilastirilir."""
    pa = [_sayi_en(_re.sub(r"<[^>]+>", "", t)).strip() for t in _BOLD.findall(a)]
    pb = [_re.sub(r"<[^>]+>", "", t).strip() for t in _BOLD.findall(b)]
    if len(pa) != len(pb): return False
    for u, v in zip(pa, pb):
        nu, nv = _re.sub(r"[^\d]", "", u), _re.sub(r"[^\d]", "", v)
        if (nu or nv) and nu != nv: return False
    return True
_YILDIZ = _re.compile(r"\*\*(.+?)\*\*")
def _yildiz(t):
    """**ifade** isaretini okumayi kolaylastiran vurguya cevirir."""
    return _YILDIZ.sub(r'<b class="vk">\1</b>', t)
def _kalin_cift(tr, en):
    tr, en = _yildiz(tr), _yildiz(en)
    a, b = _kalin(_vurgu(tr)), _kalin(_vurgu(en, True))
    if a.count("<b") != b.count("<b") or a.count("<span") != b.count("<span") or not _sira_ayni(a, b):
        a, b = _kalin(tr), _kalin(en)
    return (a, b) if a.count("<b") == b.count("<b") and _sira_ayni(a, b) else (tr, en)

_CUMLE = _re.compile(r'(?<=[.!?])\s+(?=[A-ZÇĞİÖŞÜ"“(\d])')

_KISALTMA = _re.compile(r'(?:\b(?:[A-ZÇĞİÖŞÜ]\.){2,}|\b(?:vb|vs|ör|bkz|No|St|Dr)\.)$')
def _cumleler(t):
    out = []
    for c in _CUMLE.split(t):
        if not c.strip(): continue
        if out and _KISALTMA.search(out[-1].rstrip()): out[-1] = out[-1] + " " + c
        else: out.append(c)
    return out

def insight(tr, en, *kodlar):
    ref = R(*kodlar) if kodlar else ""
    ct, ce = _cumleler(tr), _cumleler(en)
    if len(ct) >= 3 and len(ct) == len(ce):
        bas = x(*_kalin_cift(ct[0], ce[0]))
        _ms = list(zip(ct[1:], ce[1:]))
        maddeler = "".join("<li>%s%s</li>" % (x(*_kalin_cift(a, b)), ref if i_ == len(_ms) - 1 else "") for i_, (a, b) in enumerate(_ms))
        return '<div class="insight"><p>%s</p><ul class="ins-li">%s</ul></div>' % (bas, maddeler)
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
