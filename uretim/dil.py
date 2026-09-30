# -*- coding: utf-8 -*-
"""Rapor uzerine dil katmani.

  1. Almanca ifadeleri hover sozluguyle isaretler (span.de).
  2. Turkce metin ve nitelikleri Ingilizce karsiliklariyla esler; calisma
     aninda dil degistiren bir katman gomer.

Kullanim:  DOC = dil.uygula(DOC)
"""
import re, json, html as _h
from bs4 import BeautifulSoup, NavigableString, Comment, Tag

import almanca
import ceviri

ATLA_ETIKET = {"script", "style"}
NITELIK = ("data-t", "data-term", "title", "aria-label", "alt")
SAYISAL = re.compile(r'^[\d\s.,%+\-–·/()|&;:x€$₺"\'’]*$')
# Almanca ifadenin tek basina hucreyi doldurdugu yerler
TAM_HUCRE = {"td", "th", "dt", "b", "span", "li", "figcaption"}


# --- sayi bicimi (TR -> EN) -------------------------------------------------
_YUZDE = re.compile(r'([+\-−])?%(\d[\d.,]*)')
_ONDALIK = re.compile(r'(?<=\d),(?=\d)')
_BINLIK = re.compile(r'(?<![\d,])\d{1,3}(?:\.\d{3})+(?![\d.])')


_SIRA = re.compile(r'^(\d{1,3})\.$')


def _ek(n):
    if 11 <= n % 100 <= 13:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def sayi_en(t):
    """%12,5 -> 12.5%  ·  12.100 -> 12,100  ·  1. -> 1st  ·  tarihler korunur."""
    m = _SIRA.match(t)
    if m:
        return m.group(1) + _ek(int(m.group(1)))
    t = _YUZDE.sub(lambda m: (m.group(1) or "") + m.group(2) + "%", t)
    t = _ONDALIK.sub(".", t)
    t = _BINLIK.sub(lambda m: m.group(0).replace(".", ","), t)
    return t


# ------------------------------------------------------------------ Almanca
_KELIME_SIRA = sorted(almanca.KELIME, key=len, reverse=True)
_TERIM_SIRA = sorted(almanca.TERIM, key=len, reverse=True)
_HIC = r'(?!x)x'
def _alt(l): return "|".join(re.escape(k) for k in l) if l else _HIC
KELIME_DESEN = re.compile(r'(?<![\w\-])(' + _alt(_KELIME_SIRA) + r')(?![\w\-])', re.I)
TERIM_DESEN = re.compile(r'(?<![\w\-])(' + _alt(_TERIM_SIRA) + r')(?![\w\-])')
# Tirnak icinde gecen arama kelimesi
TIRNAK_DESEN = re.compile(r'(["“”«»])(' + _alt(_KELIME_SIRA) + r')\1', re.I)

# Isaretlemenin yapilmadigi baglamlar: baslik, gezinme, bag metni, terim sozlugu
ISARET_DISI_ETIKET = {"title", "h1", "h2", "h3", "h4", "th", "a", "button", "option"}
ISARET_DISI_SINIF = {"sidenav", "tocsheet", "appbar", "eyebrow", "no", "sozluk", "v", "kn", "kb"}
# Veri baglami: tablo, grafik gosterge kutusu, kelime rozeti listesi
VERI_ETIKET = {"table", "figure"}
VERI_SINIF = {"kwlist", "legend"}
# Turkce govde metninde de gecen tek kelimelik kayitlar: yalnizca hucrenin
# tamamini dolduruyorsa isaretlenir ("Marka · klozet" isaretlenmez)
BELIRSIZ = {"klozet", "taharet", "bidet wc", "duş wc"}
# Ifadeden sonra gelebilecek Turkce baglaclar
DEVAM = ("ile ", "grubu", "grup", "ve ", "aramas", "kelimes", "yazim", "yazım")
# Ifadenin oncesinde / sonrasinda kabul edilen ayraclar
ON_AYRAC = '·,;/|([{"“”«»-–>'
SON_AYRAC = '·,;/|)]}"“”«»-–<'

_sayac = {}

# Ifadeden sonra gelebilecek baglaclar (dile gore)
DEVAM_TR = ("ile ", "grubu", "grup", "ve ", "aramas", "kelimes", "yazim", "yazım")
DEVAM_EN = ("group", "and ", "search", "spelling", "keyword")


def _span(gorunen, tr, en):
    _sayac[gorunen.lower()] = _sayac.get(gorunen.lower(), 0) + 1
    return ('<span class="de" data-de-tr="%s" data-de-en="%s" tabindex="0">%s</span>'
            % (_h.escape(tr, quote=True), _h.escape(en, quote=True), _h.escape(gorunen)))


def _sinirda(metin, bas, son, devam):
    """Ifade, dugum icinde kendi basina duran bir oge mi?"""
    onc = metin[:bas].rstrip()
    snr = metin[son:].lstrip()
    bas_ok = (not onc) or onc[-1] in ON_AYRAC
    son_ok = (not snr) or snr[0] in SON_AYRAC or snr[0].isdigit() or snr.startswith(devam)
    return bas_ok and son_ok


def _isaretsizde(metin, islev, desen):
    parca = re.split(r'(<span class="de".*?</span>)', metin)
    for i, p in enumerate(parca):
        if not p.startswith('<span class="de"'):
            parca[i] = desen.sub(islev, p)
    return "".join(parca)


def isaretle_metin(ham, baglam, dil="tr"):
    """Bir metni HTML'e cevirir ve icindeki Almanca ifadeleri span.de yapar."""
    g = _h.escape(ham, quote=False)
    if baglam is None:
        return g
    kaynak = g
    devam = DEVAM_EN if dil == "en" else DEVAM_TR

    def _tirnak(m):
        tr, en = almanca.KELIME[m.group(2).lower()]
        return m.group(1) + _span(m.group(2), tr, en) + m.group(1)

    def _terim(m):
        tr, en = almanca.TERIM[m.group(1)]
        return _span(m.group(1), tr, en)

    def _kelime(m):
        anahtar = m.group(1).lower()
        tam = m.group(0) == kaynak.strip()
        if anahtar in BELIRSIZ and not tam:
            return m.group(0)
        if not tam and not _sinirda(kaynak, m.start(1), m.end(1), devam):
            return m.group(0)
        tr, en = almanca.KELIME[anahtar]
        return _span(m.group(1), tr, en)

    # Arama kelimeleri yalnizca veri baglaminda isaretlenir.
    if baglam == "veri":
        g = TIRNAK_DESEN.sub(_tirnak, g)
        g = _isaretsizde(g, _kelime, KELIME_DESEN)
    # Sektor ve kategori terimleri her baglamda isaretlenir.
    g = _isaretsizde(g, _terim, TERIM_DESEN)
    return g


def _baglam(dugum):
    """('veri' | 'metin' | None) - None ise isaretleme yapilmaz."""
    for a in dugum.parents:
        if a.name in ("svg", "defs", "script", "style", "dl"):
            return None
        if a.name in ISARET_DISI_ETIKET:
            return None
        if a.name == "span" and a.get("class") and ({"de", "term"} & set(a.get("class"))):
            return None
        if set(a.get("class") or []) & ISARET_DISI_SINIF:
            return None
        if a.get("id") in ISARET_DISI_SINIF:
            return None
    for a in dugum.parents:
        if a.name in VERI_ETIKET or (set(a.get("class") or []) & VERI_SINIF):
            return "veri"
    return "metin"



# ------------------------------------------------------------------ terimler
# rapor.py doldurur: {tr_terim: (tr_tanim, en_terim, en_tanim)}
TERIMLER = {}
# Buyuk harfli kisaltmalar ve GSC metrik adlari yalnizca yazildigi bicimiyle eslenir
_TERIM_DUYARLI = {"Click", "Impression", "Position"}
_terim_gorulen = set()

def _terim_deseni(dil):
    ad = [(k if dil == "tr" else v[1]) for k, v in TERIMLER.items()]
    ad = sorted(set(ad), key=len, reverse=True)
    if not ad:
        return None
    return re.compile(r"(?<![\w-])(" + "|".join(re.escape(a) for a in ad) + r")(?=$|[^\w-]|['’]\w)", re.I)

def _terim_tanim(gorunen, dil):
    for k, (tr_t, en_ad, en_t) in TERIMLER.items():
        ad = k if dil == "tr" else en_ad
        if gorunen == ad or (ad not in _TERIM_DUYARLI and not ad.isupper() and gorunen.lower() == ad.lower()):
            return tr_t if dil == "tr" else en_t, ad
    return None, None

def terim_isaretle(g, dil, bolum, kimlik=None):
    """Bolum icinde ilk gecen sozluk terimini span.term yapar; mevcut span'lar atlanir."""
    desen = _terim_deseni(dil)
    if desen is None:
        return g
    parca = re.split(r"(<span[^>]*>.*?</span>)", g)
    for i, p in enumerate(parca):
        if p.startswith("<span"):
            continue
        def _y(m):
            tanim, ad = _terim_tanim(m.group(1), dil)
            if tanim is None:
                return m.group(0)
            if ad in _TERIM_DUYARLI or ad.isupper():
                if m.group(1) != ad:
                    return m.group(0)
            kisaltma = ad.isupper() or ad in _TERIM_DUYARLI or ad == "AI Overview"
            anahtar = (bolum, dil, ad, kimlik if kisaltma else None)
            if anahtar in _terim_gorulen:
                return m.group(0)
            _terim_gorulen.add(anahtar)
            return ('<span class="term" data-term="%s" tabindex="0">%s</span>'
                    % (_h.escape(tanim, quote=True), m.group(1)))
        parca[i] = desen.sub(_y, p)
    return "".join(parca)

# ------------------------------------------------------------------ ceviri
def _cevrilir(t):
    return bool(t.strip()) and not SAYISAL.match(t.strip())



def _duz_html(t):
    return " ".join(_h.unescape(t).split())

_BLOK_ETIKET = ["p", "li", "td", "dd", "h4", "div", "span"]

def _blok_sar(corba):
    """Satir ici etiket (<b>, <span class="up">, <a>) iceren ve ceviri sozlugunde
    butun olarak kayitli olan bloklari tek span.t icinde tasir; boylece parcalar
    konumsal olarak degil, blok olarak cevrilir."""
    n = 0
    for el in list(corba.find_all(_BLOK_ETIKET)):
        if el.find_parent("span", class_="t") or el.name == "span" and "t" in (el.get("class") or []):
            continue
        if not any(isinstance(c, Tag) for c in el.children):
            continue
        if el.find(["table", "div", "ul", "ol", "p", "figure", "svg", "h3", "h4", "li"]):
            continue
        inner = "".join(str(c) for c in el.children)
        k = _duz_html(inner)
        if "<" not in k or k not in ceviri.EN:
            continue
        en = ceviri.EN[k]
        ilk = el.find(string=True)
        baglam = _baglam(ilk) if ilk is not None else None
        tr_html, en_html = inner, en
        if baglam == "metin" and TERIMLER:
            sec = el.find_parent("section"); bolum = sec.get("id") if sec is not None else ""
            if bolum and not any(set(a.get("class") or []) & {"src", "lede"} for a in el.parents):
                tr_html = terim_isaretle(tr_html, "tr", bolum, id(el))
                en_html = terim_isaretle(en_html, "en", bolum, id(el))
        el.clear()
        el.append(BeautifulSoup('<span class="t" data-en="%s">%s</span>' % (_h.escape(en_html, quote=True), tr_html), "html.parser"))
        n += 1
    return n

def _topla(corba):
    """Cevrilecek benzersiz metin ve nitelik degerlerini toplar."""
    metin, nitelik, sayisal = set(), set(), set()
    for dugum in corba.find_all(string=True):
        if isinstance(dugum, Comment):
            continue
        ust = dugum.parent
        if ust is None or ust.name in ATLA_ETIKET:
            continue
        if dugum.find_parent("span", class_="t") is not None:
            continue
        if any(a.name == "span" and a.get("class") and "de" in (a.get("class") or [])
               for a in dugum.parents):
            continue            # Almanca ifade oldugu gibi kalir
        t = str(dugum).strip()
        if _cevrilir(t):
            metin.add(t)
        elif t:
            sayisal.add(t)
    for etiket in corba.find_all(True):
        if etiket.find_parent("span", class_="t") is not None:
            continue
        for ad in NITELIK:
            d = etiket.get(ad)
            if d and _cevrilir(d):
                nitelik.add(d.strip())
    return metin, nitelik, sayisal


def _grafik_etiketleri(corba):
    """figure[data-grafik] icindeki seri ve donem adlari."""
    et = set()
    for f in corba.find_all(attrs={"data-grafik": True}):
        try:
            g = json.loads(f["data-grafik"])
        except Exception:
            continue
        for s in g.get("seriler", []):
            if s.get("ad"):
                et.add(s["ad"])
        if g.get("birim"):
            et.add(g["birim"])
        if g.get("olcu"):
            et.add(g["olcu"])
        for a in g.get("aylar", []):
            if a and not a[:1].isdigit():
                et.add(a)
    return et


def sozluk(corba):
    metin, nitelik, _s = _topla(corba)
    return metin | nitelik | _grafik_etiketleri(corba)


def sayilar(corba):
    """Cevrilmeyen sayisal dugumlerin Ingilizce bicimi (yalnizca degisenler)."""
    _m, _n, sayisal = _topla(corba)
    return {t: sayi_en(t) for t in sayisal if sayi_en(t) != t}


# ------------------------------------------------------------------ katman
DIL_BUTON = (
 '<button class="dilbtn" type="button" id="dil" aria-label="Rapor dilini değiştir" '
 'title="Switch to English" data-tr="Switch to English" data-en="Switch to Turkish">'
 '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
 '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18"/>'
 '</svg><span class="dilbtn__t">EN</span></button>'
)

RUNTIME = r"""
/* --- Rapor dili (TR / EN) ------------------------------------------------- */
(function(){
  var veri = window.__DIL__; if(!veri) return;
  var btn = document.getElementById('dil'); if(!btn) return;
  var kok = document.documentElement;
  var NITELIK = ['data-t','data-term','title','aria-label','alt'];
  var kabuklar = [], nitelikler = [], grafikler = [], svgMetin = [];

  /* Govde metni: her span.t iki dilin isaretlenmis halini tasir */
  [].forEach.call(document.querySelectorAll('span.t'), function(e){
    kabuklar.push([e, e.innerHTML, e.getAttribute('data-en')]);
  });

  [].forEach.call(document.querySelectorAll('*'), function(e){
    NITELIK.forEach(function(a){
      var v = e.getAttribute(a);
      if(v && veri.m[v.trim()] !== undefined) nitelikler.push([e, a, v, veri.m[v.trim()]]);
    });
    if(e.hasAttribute('data-grafik')) grafikler.push([e, e.getAttribute('data-grafik')]);
  });

  /* SVG icindeki eksen ve gosterge etiketleri span alamaz; dogrudan cevrilir */
  [].forEach.call(document.querySelectorAll('svg text, svg tspan'), function(e){
    if(e.children.length) return;
    var t = e.textContent.trim();
    if(t && veri.m[t] !== undefined && veri.m[t] !== t){
      svgMetin.push([e, e.textContent, e.textContent.replace(t, veri.m[t])]);
    }
  });

  grafikler.forEach(function(g){
    var o; try{ o = JSON.parse(g[1]); }catch(err){ return; }
    (o.seriler||[]).forEach(function(s){ if(veri.m[s.ad] !== undefined) s.ad = veri.m[s.ad]; });
    (o.satirlar||[]).forEach(function(s){ if(veri.m[s.ad] !== undefined) s.ad = veri.m[s.ad]; });
    if(o.birim && veri.m[o.birim] !== undefined) o.birim = veri.m[o.birim];
    if(o.olcu && veri.m[o.olcu] !== undefined) o.olcu = veri.m[o.olcu];
    if(o.aylar) o.aylar = o.aylar.map(function(a){ return veri.m[a] !== undefined ? veri.m[a] : a; });
    g.push(JSON.stringify(o));
  });

  var aktif = 'tr';
  function uygula(dil){
    var en = (dil === 'en');
    kabuklar.forEach(function(x){ x[0].innerHTML = en ? x[2] : x[1]; });
    nitelikler.forEach(function(x){ x[0].setAttribute(x[1], en ? x[3] : x[2]); });
    svgMetin.forEach(function(x){ x[0].textContent = en ? x[2] : x[1]; });
    grafikler.forEach(function(x){ if(x[2]) x[0].setAttribute('data-grafik', en ? x[2] : x[1]); });
    kok.setAttribute('lang', en ? 'en' : 'tr');
    kok.setAttribute('data-dil', dil);
    document.title = en ? veri.baslik_en : veri.baslik_tr;
    btn.querySelector('.dilbtn__t').textContent = en ? 'TR' : 'EN';
    btn.title = btn.getAttribute(en ? 'data-en' : 'data-tr');
    btn.setAttribute('aria-label', btn.title);
    aktif = dil;
    document.dispatchEvent(new CustomEvent('dilchange'));
  }

  var kayit = null;
  try{ kayit = localStorage.getItem('vitra-dil'); }catch(e){}
  uygula(kayit || 'tr');
  btn.addEventListener('click', function(){
    var y = (aktif === 'en') ? 'tr' : 'en';
    uygula(y);
    try{ localStorage.setItem('vitra-dil', y); }catch(e){}
  });
})();
"""


def _svg_icinde(dugum):
    return any(a.name in ("svg", "defs") for a in dugum.parents)


def _sar(corba):
    """Cevrilebilir her metin dugumunu iki dilin isaretlenmis halini tasiyan
    span.t icine alir. SVG icindekiler sarilmaz (span gecersiz olur)."""
    sarilan = eksik = 0
    hatalar = []
    for dugum in list(corba.find_all(string=True)):
        if isinstance(dugum, Comment) or dugum.parent is None:
            continue
        if dugum.parent.name in ATLA_ETIKET:
            continue
        if dugum.find_parent("span", class_="t") is not None:
            continue
        ham = str(dugum)
        duz = ham.strip()
        if not duz:
            continue
        baglam = None if _svg_icinde(dugum) else _baglam(dugum)

        if _cevrilir(duz):
            if duz not in ceviri.EN:
                hatalar.append(duz)
                continue
            hedef = ceviri.EN[duz]
        else:
            hedef = sayi_en(duz)

        tr_html = isaretle_metin(duz, baglam, "tr")
        en_html = isaretle_metin(hedef, baglam, "en")
        if baglam == "metin" and TERIMLER:
            sec = dugum.find_parent("section")
            bolum = sec.get("id") if sec is not None else ""
            if bolum and not any(set(a.get("class") or []) & {"src", "lede"} for a in dugum.parents):
                tr_html = terim_isaretle(tr_html, "tr", bolum, id(dugum))
                en_html = terim_isaretle(en_html, "en", bolum, id(dugum))
        if tr_html == _h.escape(duz, quote=False) and en_html == _h.escape(hedef, quote=False) \
           and duz == hedef:
            continue                      # ceviri de isaret de yok
        if _svg_icinde(dugum):
            continue                      # SVG metinleri harita yontemiyle cevrilir

        on = ham[:len(ham) - len(ham.lstrip())]
        arka = ham[len(ham.rstrip()):]
        kabuk = ('%s<span class="t" data-en="%s">%s</span>%s'
                 % (on, _h.escape(en_html, quote=True), tr_html, arka))
        dugum.replace_with(BeautifulSoup(kabuk, "html.parser"))
        sarilan += 1
    return sarilan, hatalar


def uygula(doc, baslik_en):
    corba = BeautifulSoup(doc, "html.parser")
    _blok = _blok_sar(corba)

    # 1) Ceviri sozlugu isaretlemeden ONCE dogrulanir
    gerekli = sozluk(corba)
    eksik = sorted(t for t in gerekli if t not in ceviri.EN)
    if eksik:
        import os
        _y = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eksik_ceviri.txt")
        open(_y, "w", encoding="utf-8").write("\n".join(eksik))
        raise SystemExit("Cevirisi olmayan %d ifade · liste: %s" % (len(eksik), _y))

    # 2) Harita yalnizca span alamayan yerler icin: nitelikler, SVG metinleri,
    #    grafik etiketleri. Govde metni span.t icinde tasindigi icin haritaya
    #    girmez; boylece dosya gereksiz buyumez.
    _m, nitelik, _s = _topla(corba)
    svg_metin = set()
    for d in corba.find_all(string=True):
        if isinstance(d, Comment) or d.parent is None:
            continue
        if not _svg_icinde(d):
            continue
        t = str(d).strip()
        if t:
            svg_metin.add(t)
    sayi_haritasi = sayilar(corba)
    harita = {}
    for t in nitelik | _grafik_etiketleri(corba) | svg_metin:
        if t in ceviri.EN:
            harita[t] = ceviri.EN[t]
        elif t in sayi_haritasi:
            harita[t] = sayi_haritasi[t]

    # 3) Govde metni: her dugum iki dilin isaretlenmis halini tasir
    sarilan, hatalar = _sar(corba)
    if hatalar:
        raise SystemExit("Sarmalama sirasinda cevirisi bulunamayan %d ifade:\n  - %s"
                         % (len(hatalar), "\n  - ".join(hatalar[:40])))

    baslik_tr = corba.title.string if corba.title else ""
    yuk = json.dumps({"m": harita, "baslik_tr": baslik_tr, "baslik_en": baslik_en},
                     ensure_ascii=False)

    # dil dugmesini tema dugmesinin soluna yerlestir
    tema = corba.find("button", id="tema")
    if tema is None:
        raise SystemExit("Tema dugmesi bulunamadi; dil dugmesi yerlestirilemedi.")
    tema.insert_before(BeautifulSoup(DIL_BUTON, "html.parser"))

    cikti = str(corba)
    cikti = cikti.replace(
        "</body>",
        "<script>window.__DIL__=%s;</script>\n<script>%s</script>\n</body>" % (yuk, RUNTIME))
    return cikti, sarilan + _blok, dict(_sayac)
