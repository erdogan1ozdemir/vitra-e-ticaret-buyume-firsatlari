# -*- coding: utf-8 -*-
"""Bicimlendirme yardimcilari (TR bicimi; dil katmani EN'e cevirir)."""
import json, os, veri
from t2_ortak import x, R, th, tablo, n, insight, p, h3, li, kaynak, olcek, sayi
A = json.load(open(os.path.join(veri.V, "islenmis", "analiz.json"), encoding="utf-8"))
AY_TR = {"01":"Oca","02":"Şub","03":"Mar","04":"Nis","05":"May","06":"Haz","07":"Tem","08":"Ağu","09":"Eyl","10":"Eki","11":"Kas","12":"Ara"}
AY_EN = {"01":"Jan","02":"Feb","03":"Mar","04":"Apr","05":"May","06":"Jun","07":"Jul","08":"Aug","09":"Sep","10":"Oct","11":"Nov","12":"Dec"}
def ay_et(m):
    y, a = m.split("-"); return x("%s %s" % (AY_TR[a], y), "%s %s" % (AY_EN[a], y))
def ay_kisa(m):
    y, a = m.split("-"); return x("%s'%s" % (AY_TR[a], y[2:]), "%s'%s" % (AY_EN[a], y[2:]))
def bin(v):
    """12345 -> 12.345"""
    return f"{int(round(v)):,}".replace(",", ".")
def k(v):
    """Kisa bicim: 12.3K / 1.2M"""
    v = float(v)
    if abs(v) >= 1e6: return ("%.1fM" % (v/1e6)).replace(".", ",")
    if abs(v) >= 1e3: return ("%.1fK" % (v/1e3)).replace(".", ",") if v < 1e5 else "%dK" % round(v/1e3)
    return bin(v)
def yz(v, isaret=True, ond=1):
    """+%12,5 biciminde yuzde; renk sinifi ile"""
    if v is None: return "-"
    s = ("%+." + str(ond) + "f") % v if isaret else ("%." + str(ond) + "f") % v
    s = s.replace(".", ",")
    if isaret: s = s[0] + "%" + s[1:]
    else: s = "%" + s
    cls = "up" if v > 0 else ("dn" if v < 0 else "")
    return '<span class="%s">%s</span>' % (cls, s) if cls else s
def yzd(v, ond=1):
    """duz yuzde metni: %12,5"""
    return ("%" + ("%." + str(ond) + "f") % v).replace(".", ",")
def cell(v): return n(bin(v))
def kpi_kart(v, k_tr, k_en, cls="", tag_tr=None, tag_en=None):
    t = ('<div class="tag">%s</div>' % x(tag_tr, tag_en)) if tag_tr else ""
    return '<div class="kpi"><div class="v %s">%s</div><div class="k">%s</div>%s</div>' % (cls, sayi(v), x(k_tr, k_en), t)
def metric(mk_tr, mk_en, mv, md_tr, md_en):
    return '<div class="metric"><div class="mv">%s</div><div class="mk">%s</div><div class="md">%s</div></div>' % (sayi(mv), x(mk_tr, mk_en), x(md_tr, md_en))
def note(nt_tr, nt_en, govde_html, sinif=""):
    return '<div class="note %s"><div class="nt">%s</div>%s</div>' % (sinif, x(nt_tr, nt_en), govde_html)
def box(bt_tr, bt_en, govde_html):
    return '<div class="box"><div class="bt">%s</div>%s</div>' % (x(bt_tr, bt_en), govde_html)
def _kc(a, b):
    from t2_ortak import _kalin_cift
    return _kalin_cift(a, b)
def fnote(no, h_tr, h_en, maddeler):
    """maddeler: [(tr, en)]"""
    return ('<article class="fnote"><span class="fc">%s</span><h3>%s</h3><ul>%s</ul></article>'
            % (x("Bulgu %02d" % no, "Finding %02d" % no), x(h_tr, h_en), "".join("<li>%s</li>" % x(*_kc(a, b)) for a, b in maddeler)))
def rank_list(satirlar, azami, you=None, fmt=bin):
    """satirlar: [(etiket_html, deger)]"""
    out = ['<ol class="rank">']
    for i, (et, v) in enumerate(satirlar, 1):
        out.append('<li%s><span class="rn">%d</span><span class="rl">%s</span>%s<span class="rv">%s</span></li>'
                   % (' class="you"' if you and you(et) else "", i, et, olcek(v, azami), fmt(v)))
    out.append('</ol>'); return "".join(out)
def step(no, h_tr, h_en, p_tr, p_en):
    return '<div class="step"><span class="sn">%d</span><h4>%s</h4><p>%s</p></div>' % (no, x(h_tr, h_en), x(p_tr, p_en))
def marks(maddeler):
    """[(isaret 'up'|'at', tr, en)]"""
    return '<ul class="marks">%s</ul>' % "".join('<li><span class="mk %s">%s</span><span class="mt">%s</span></li>' % (s, "✓" if s == "up" else "▲", x(*_kc(a, b))) for s, a, b in maddeler)
def u(url, metin=None):
    m = metin or url.replace("https://www.", "").replace("https://", "")
    from tr_ek import marka as _mk, marka_tek as _mt; m = _mt(_mk(m))
    from t2_ortak import EK as _EK
    if m not in _EK: x(m, m)   # baglanti metni (alan adi, sayfa yolu, video basligi) veridir; iki dilde aynidir
    return '<a class="dis" href="%s" target="_blank" rel="noopener">%s</a>' % (url, m)
def kw(s):
    x(s, s)   # arama kelimesi veridir; cevrilmez
    return '<span class="kw">%s</span>' % s
_AH = None
def _hacim(s):
    global _AH
    if _AH is None:
        try: _AH = _j.load(open(_o.path.join(veri.V, "ham", "autocomplete_hacim.json"), encoding="utf-8"))["kelime"]
        except Exception: _AH = {}
    v = _AH.get(s) or _AH.get(s.lower())
    return v.get("ort2026") if v else None
def cellk(v):
    """Hacim hucresi: ekranda yuvarlanmis (21,6K), kopyalama ve Excel'de tam sayi (data-v)."""
    v = round(v or 0)
    if v < 1000: return cell(v)
    r = k(v); x(r, r.replace(",", "."))
    return n('<span class="kh" data-v="%d">%s</span>' % (v, r))
def kwv(s):
    """Arama kelimesi + 2026 aylik ortalama hacim rozeti (Oca-Agu 2026, Google Ads)."""
    x(s, s); h = _hacim(s)
    if h is None: return '<span class="kw">%s</span>' % s
    r = k(round(h)) if h >= 1000 else bin(round(h)); x(r, r.replace(".", "").replace(",", "."))
    return '<span class="kw">%s<i class="kv">%s</i></span>' % (s, r)
def veri_m(s):
    from tr_ek import marka as _mk, marka_tek as _mt; s = _mt(_mk(s))
    x(s, s); return s
import json as _j, os as _o
import base64 as _b64
_LOGO_DIR = _o.path.join(veri.V, "ham", "logo")
def logo_css():
    """Her alan adi icin bir kez tanimlanan arka plan resmi (data URI)."""
    from PIL import Image
    import io
    out = []
    for f in sorted(_o.listdir(_LOGO_DIR)):
        if not f.endswith(".png"): continue
        d = f[:-4]
        try:
            im = Image.open(_o.path.join(_LOGO_DIR, f)).convert("RGBA")
            if max(im.size) > 32: im = im.resize((32, 32), Image.LANCZOS)
            buf = io.BytesIO(); im.save(buf, "PNG", optimize=True); b = buf.getvalue()
        except Exception:
            b = open(_o.path.join(_LOGO_DIR, f), "rb").read()
        out.append('.lg-%s{background-image:url(data:image/png;base64,%s)}' % (d.replace(".", "_"), _b64.b64encode(b).decode()))
    return "\n".join(out)
def logo_alan_adlari():
    return [f[:-4] for f in _o.listdir(_LOGO_DIR) if f.endswith(".png")]
def lg(domain):
    return '<i class="lg lg-%s" aria-hidden="true"></i>' % domain.replace("www.", "").replace(".", "_")
def ul_b(maddeler):
    """[(kalin_tr, kalin_en, tr, en)] -> madde listesi; kalin bolum basta."""
    return '<ul class="nl">%s</ul>' % "".join('<li><b>%s</b> <span class="mt">%s</span></li>' % (x(kt, ke), x(*_kc(t, e))) for kt, ke, t, e in maddeler)
def _J(*p): return _j.load(open(_o.path.join(veri.V, *p), encoding="utf-8"))
SB = _J("islenmis", "ssg_bm.json"); YK = _J("islenmis", "yeni_kategori.json"); KT = _J("islenmis", "katalog.json"); TY = _J("islenmis", "trendyol_ozet.json")["sorgular"]
HZ = _J("ham", "hizmet", "vitra_hizmetler.json")
def f1(v):
    return ("%.1f" % v).replace(".", ",")

# ---------------------------------------------------------------- acilir pencere (kelime listeleri vb.)
_POP_NO = [0]
x("×", "×"); x("↗", "↗")
def pop(baslik_tr, baslik_en, icerik, etiket_tr=None, etiket_en=None, ikon=False):
    """Dugme + <dialog>. etiket verilirse metinli dugme, ikon=True ise yalniz ok simgeli kucuk dugme."""
    _POP_NO[0] += 1; pid = "pop%d" % _POP_NO[0]
    if ikon:
        dug = '<button type="button" class="popb ic" data-pop="%s" aria-label="%s" title="%s">↗</button>' % (pid, x(baslik_tr, baslik_en), baslik_tr)
    else:
        dug = '<button type="button" class="popb" data-pop="%s">%s <span aria-hidden="true">↗</span></button>' % (pid, x(etiket_tr, etiket_en))
    dia = ('<dialog class="popd" id="%s"><div class="pophd"><b>%s</b><button type="button" class="popx" aria-label="%s">×</button></div>'
           '<div class="popbd">%s</div></dialog>') % (pid, x(baslik_tr, baslik_en), x("Kapat", "Close"), icerik)
    return dug, dia

# ---------------------------------------------------------------- ozetten ilgili alt basliga ok baglantisi
_HTR = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosucgiosu")
def hid(baslik):
    """Alt baslik (h3) metninden kimlik: 'h-' + sade harfler."""
    import re as _r
    return "h-" + _r.sub(r"[^a-z0-9]+", "-", baslik.translate(_HTR).lower()).strip("-")[:70]
x("İlgili bölüme git", "Go to the related section"); x("→", "→")
def git(hedef):
    """hedef: '#bolum' (bolum kimligi) ya da alt baslik metni."""
    i = hedef[1:] if hedef.startswith("#") else hid(hedef)
    return '<a class="git" href="#%s" aria-label="İlgili bölüme git" title="İlgili bölüme git">→</a>' % i

# ---------------------------------------------------------------- grup etiketi (tablolarda renkli kume rozeti)
_ETK = {}
def etk(tr, en, anahtar=None):
    """Grup / kume degerini renkli rozetle yazar; ayni deger rapor boyunca ayni rengi alir (8 renk dongusu)."""
    k_ = anahtar or tr
    if k_ not in _ETK: _ETK[k_] = len(_ETK) % 8 + 1
    return '<span class="etk e%d">%s</span>' % (_ETK[k_], x(tr, en))


_SON = {1: ("i", 0), 2: ("i", 1), 3: ("ü", 0), 4: ("ö", 0), 5: ("e", 0), 6: ("ı", 1), 7: ("i", 1), 8: ("i", 0), 9: ("u", 0)}
_ONL = {1: ("o", 0), 2: ("i", 1), 3: ("u", 0), 4: ("ı", 0), 5: ("i", 1), 6: ("ı", 0), 7: ("i", 0), 8: ("e", 0), 9: ("a", 0)}
_SERT = {1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0, 9: 0}


def ek(n, tip):
    """Sayiya Turkce ek: tip 'i' (iyelik: 84'u, 6'si), 'in' (6'nin, 14'un), 'de' (19'unda degil -> 19'da), 'e' (3'e, 6'ya)."""
    n = int(n); s = str(n)
    if n % 1000 == 0 and n: unl, sesli, sert = "i", 0, 0
    elif n % 100 == 0 and n: unl, sesli, sert = "ü", 0, 0
    elif n % 10 == 0 and n: unl, sesli = _ONL[(n // 10) % 10]; sert = (n // 10) % 10 in (4, 6, 7)
    else: unl, sesli = _SON.get(n % 10, ("ı", 1)); sert = _SERT.get(n % 10, 0)
    h4 = {"e": "i", "i": "i", "a": "ı", "ı": "ı", "o": "u", "u": "u", "ö": "ü", "ü": "ü"}[unl]
    h2 = "e" if unl in "eiöü" else "a"
    if tip == "i": return s + "'" + ("s" if sesli else "") + h4
    if tip == "inde": return s + "'" + ("s" if sesli else "") + h4 + "nd" + ("e" if h4 in "iü" else "a")
    if tip == "in": return s + "'" + ("n" if sesli else "") + h4 + "n"
    if tip == "de": return s + "'" + ("t" if sert else "d") + h2
    if tip == "e": return s + "'" + ("y" if sesli else "") + h2
    raise ValueError(tip)
