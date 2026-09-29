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
    return '<div class="metric"><div class="mk">%s</div><div class="mv">%s</div><div class="md">%s</div></div>' % (x(mk_tr, mk_en), sayi(mv), x(md_tr, md_en))
def note(nt_tr, nt_en, govde_html, sinif=""):
    return '<div class="note %s"><div class="nt">%s</div>%s</div>' % (sinif, x(nt_tr, nt_en), govde_html)
def box(bt_tr, bt_en, govde_html):
    return '<div class="box"><div class="bt">%s</div>%s</div>' % (x(bt_tr, bt_en), govde_html)
def fnote(no, h_tr, h_en, maddeler):
    """maddeler: [(tr, en)]"""
    return ('<article class="fnote"><span class="fc">%s</span><h3>%s</h3><ul>%s</ul></article>'
            % (x("Bulgu %02d" % no, "Finding %02d" % no), x(h_tr, h_en), "".join("<li>%s</li>" % x(a, b) for a, b in maddeler)))
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
    return '<ul class="marks">%s</ul>' % "".join('<li><span class="mk %s">%s</span>%s</li>' % (s, "✓" if s == "up" else "▲", x(a, b)) for s, a, b in maddeler)
def u(url, metin=None):
    m = metin or url.replace("https://www.", "").replace("https://", "")
    from t2_ortak import EK as _EK
    if m not in _EK: x(m, m)   # baglanti metni (alan adi, sayfa yolu, video basligi) veridir; iki dilde aynidir
    return '<a class="dis" href="%s" target="_blank" rel="noopener">%s</a>' % (url, m)
def kw(s):
    x(s, s)   # arama kelimesi veridir; cevrilmez
    return '<span class="kw">%s</span>' % s
def veri_m(s):
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
    return '<ul class="nl">%s</ul>' % "".join('<li><b>%s</b> %s</li>' % (x(kt, ke), x(t, e)) for kt, ke, t, e in maddeler)
def _J(*p): return _j.load(open(_o.path.join(veri.V, *p), encoding="utf-8"))
SB = _J("islenmis", "ssg_bm.json"); YK = _J("islenmis", "yeni_kategori.json"); KT = _J("islenmis", "katalog.json"); TY = _J("islenmis", "trendyol_ozet.json")["sorgular"]
HZ = _J("ham", "hizmet", "vitra_hizmetler.json")
def f1(v):
    return ("%.1f" % v).replace(".", ",")
