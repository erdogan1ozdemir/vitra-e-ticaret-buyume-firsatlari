# -*- coding: utf-8 -*-
"""VitrA e-ticaret buyume firsatlari · HTML rapor uretimi (TR + EN tek dosya)."""
import os, sys, base64, zipfile, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veri
from rapor_parca1 import VITRA, INBOUND, GLOSSARY
from rapor_css import CSS
from css_ek import CSS_EK
from rapor_js import JS, KAYNAKCA_CSS, TEMA, IKON
import t2_ortak, kaynakca, ceviri, dil
from t2_ortak import x, R
from ortak import logo_css, logo_alan_adlari, lg
import h3_not
import b_ozet, b_makro, b_talep, b_ssgbm, b_niyet, b_organik, b_marka, b_youtube, b_katalog, b_yeni, b_set, b_rakip, b_benchmark, b_model, b_adimlar, b_yontem, b_serp, b_kategori_trafik, b_pazaryeri, b_politika, b_sikayet, b_fiyat, b_derin, b_panel

AD = "VitrA_E-Ticaret_Buyume_Firsatlari"
XLS = os.path.join(veri.KOK, AD + ".xlsx")

# ---------------------------------------------------------------- bolumler
BOLUMLER = []
def bolum(bid, tr, en, govde):
    BOLUMLER.append((bid, tr))
    return '<section id="%s"><h2><span class="no">%02d</span>%s</h2>%s</section>' % (bid, len(BOLUMLER), x(tr, en), govde)

P = []
P.append(bolum("ozet", "Özet", "Summary", b_ozet.HTML))
P.append(bolum("makro", "Makro Ortam ve Ödeme Gücü", "Macro Environment and Purchasing Power", b_makro.HTML))
P.append(bolum("talep", "Kategori Talebi ve Dönemsel Değişim", "Category Demand and Period Change", b_talep.HTML))
P.append(bolum("ssgbm", "SSG ve BM: Derin Talep İncelemesi", "SSG and BM: In-Depth Demand Review", b_ssgbm.HTML))
P.append(bolum("ihtiyac", "İhtiyaç Dili: Kullanıcı Ne Arıyor?", "Need Language: What Is the User Searching For?", b_niyet.HTML))
P.append(bolum("organik", "Organik Kanal Performansı", "Organic Channel Performance", b_organik.HTML))
P.append(bolum("marka", "Marka Aramaları ve Autocomplete", "Brand Searches and Autocomplete", b_marka.HTML))
P.append(bolum("serp", "Google Arama Sonuçları ve AI Overview", "Google Search Results and AI Overview", b_serp.HTML))
P.append(bolum("youtube", "YouTube: Montaj, Tamir ve Karar Videoları", "YouTube: Installation, Repair and Decision Videos", b_youtube.HTML))
P.append(bolum("sikayet", "Şikayetvar: Satış Sonrası Deneyim", "Şikayetvar: After-Sales Experience", b_sikayet.HTML))
P.append(bolum("katalog", "Katalog ve Talep Eşleşmesi", "Catalogue and Demand Fit", b_katalog.HTML))
P.append(bolum("yeni", "Yeni Kategori ve Segment Fırsatları", "New Category and Segment Opportunities", b_yeni.HTML))
P.append(bolum("set", "Set, Komple Banyo ve Ürün + Hizmet", "Sets, Complete Bathrooms and Product + Service", b_set.HTML))
P.append(bolum("rakip", "Rakip Görünürlüğü ve Kanal Ölçeği", "Competitor Visibility and Channel Scale", b_rakip.HTML))
P.append(bolum("trafik", "Marka ve Uzman Sitelerde Kategori Trafiği", "Category Traffic on Brand and Specialist Sites", b_kategori_trafik.HTML))
P.append(bolum("pazaryeri", "Pazaryerleri: Kategori Yapısı ve Çok Satanlar", "Marketplaces: Category Structure and Best Sellers", b_pazaryeri.HTML))
P.append(bolum("derin", "Pazaryeri Alt Kategori Derinliği: Çok Satanlar ve Rakip Mağazalar", "Marketplace Sub-Category Depth: Best Sellers and Competitor Stores", b_derin.HTML))
P.append(bolum("panel", "VitrA Resmi Mağaza: Pazaryeri Panel Verisi", "VitrA Official Store: Marketplace Panel Data", b_panel.HTML))
P.append(bolum("fiyat", "Fiyat ve Satıcı Manzarası: Shopping, Trendyol, Hepsiburada", "Price and Seller Landscape: Shopping, Trendyol, Hepsiburada", b_fiyat.HTML))
P.append(bolum("politika", "Kanal Politikaları ve Keşif Kanalları", "Channel Policies and Discovery Channels", b_politika.HTML))
P.append(bolum("benchmark", "Benchmark: E-Ticaret Modelleri ve Dijital Deneyim", "Benchmark: E-Commerce Models and Digital Experience", b_benchmark.HTML))
P.append(bolum("model", "Kanal Rolleri ve Etkileşim Modeli", "Channel Roles and Engagement Model", b_model.HTML))
P.append(bolum("adimlar", "Sonraki Adımlar", "Next Steps", b_adimlar.HTML))
P.append(bolum("yontem", "Yöntem ve Kapsam", "Method and Scope", b_yontem.HTML))

govde = "\n".join(P)
# --- son islemler: alt baslik aciklamasi, uzun tablo, logo
def _h3_not(m):
    t = m.group(1)
    if t in h3_not.N:
        tr, en = h3_not.N[t]; return '<h3>%s</h3><p class="h3n">%s</p>' % (t, x(tr, en))
    return m.group(0)
govde = re.sub(r'<h3>([^<]+)</h3>', _h3_not, govde)
_eksik_h3 = sorted({m for m in re.findall(r'(?<!</span>)<h3>([^<]+)</h3>', govde) if m not in h3_not.N and m != "Öne çıkan bulgular"})
def _uzun(m):
    blok = m.group(0)
    if 'uzun' in m.group(1): return blok
    n_ = blok.count('<tr>') - 1
    return blok.replace('<div class="tw %s">' % m.group(1), '<div class="tw %s uzun">' % m.group(1), 1) if n_ > 9 else blok
govde = re.sub(r'<div class="tw ([^"]*)">.*?</table></div>', _uzun, govde, flags=re.S)
_LOGO = sorted(logo_alan_adlari(), key=len, reverse=True)
_LG = re.compile(r'(<(?:td|span class="rl")>|<a class="(?:u|dis)"[^>]*>)((?:www\.)?(' + "|".join(re.escape(d) for d in _LOGO) + r'))(?=</)')
govde = _LG.sub(lambda m: m.group(1) + lg(m.group(3)) + m.group(2), govde)
_BNO = {b_: "%02d" % (i + 1) for i, (b_, _) in enumerate(BOLUMLER)}
def _btok(t):
    return re.sub(r"\[\[b:([a-z]+)\]\]", lambda m: _BNO.get(m.group(1), "??"), t)
govde = _btok(govde)
t2_ortak.EK = {_btok(k_): _btok(v_) for k_, v_ in t2_ortak.EK.items()}
if "??" in govde: raise SystemExit("Bölüm atfı çözülemedi")
govde, sira = kaynakca.coz(govde)
P.append(bolum("kaynakca", "Kaynakça", "References", kaynakca.bolum_html(sira, x)))
GL_EN = {
 "CTR": "Click-through rate; the share of impressions that turn into clicks.", "Impression": "The number of times the site appeared in search results.",
 "Click": "A visit to the site from a search result.", "Position": "The site's average rank in search results.",
 "DR": "Domain Rating; Ahrefs' link strength score for a domain, on a 0-100 scale.", "Organik trafik": "Ahrefs' estimate of monthly free search visits from ranking keywords.",
 "Paid trafik": "Ahrefs' estimate of monthly visits from Google Ads.", "Long-tail": "Low-volume but clearly intended long search phrases.",
 "Autocomplete": "Completion phrases suggested while typing in the Google search box; derived from real user searches.", "Bundle": "A set of several products sold together at a single price.",
 "AOV": "Average Order Value; the average basket per order.", "Conversion rate": "The share of visits that turn into a purchase.",
 "Pureplayer": "A retailer without physical stores that sells online only.", "Marketplace": "A platform that hosts third-party sellers.",
 "Retargeting": "A reminder ad shown later to a user who visited the site.", "Kartlı Ödeme Endeksi": "An index the CBRT derives from bank and credit card spending; the real series is inflation-adjusted.",
 "Net yüzde": "A survey indicator obtained by subtracting the share of negative answers from the share of positive answers.",
 "SSG": "Sanitaryware; vitreous china products such as WCs, washbasins, bidets, urinals and cisterns.",
 "BM": "Bathroom furniture; basin units, tall cabinets, mirror cabinets, mirrors, countertops and complements.",
 "3P": "Third-party seller; a model where another seller's product is listed and sold on the brand site.",
 "GA4": "Google Analytics 4; the analytics tool measuring the site's visits, conversions and product performance.",
 "GSC": "Google Search Console; the tool reporting the search traffic Google sends to the site at impression, click and position level.",
 "SERP": "Search Engine Results Page; the results page Google returns for a search.",
 "KD": "Keyword Difficulty; Ahrefs' 0-100 score for how hard it is to rank in the top 10 for a keyword.",
 "TP": "Traffic Potential; the estimated monthly traffic the page ranking first receives from all its keywords (Ahrefs).",
 "PAA": "People Also Ask; the \"related questions\" box on the search results page.",
 "AI Overview": "The AI-generated summary Google shows above search results; it links to the sites it cites.",
 "YoY": "Year over year; a period's change against the same period of the previous year.",
 "TCMB": "Central Bank of the Republic of Türkiye (CBRT).",
 "EVDS": "CBRT Electronic Data Delivery System; the database publishing macro and financial series.",
 "BKM": "Interbank Card Center; the source of card payment statistics.",
 "CPC": "Cost per click; the average cost per click in Google Ads.",
 "Buybox": "The seller that wins the \"add to basket\" button among sellers offering the same product on a marketplace.",
 "PVC": "Polyvinyl chloride; a water-resistant plastic body material.",
 "MDF": "Medium-density fibreboard; a common body material in bathroom furniture.",
}
GL_TERM_EN = {"Organik trafik": "Organic traffic", "Paid trafik": "Paid traffic", "Kartlı Ödeme Endeksi": "Card Payment Index", "Net yüzde": "Net percentage", "SSG": "SSG", "BM": "BM", "3P": "3P", "TCMB": "CBRT", "EVDS": "EVDS"}
sozluk = '<dl class="gl">%s</dl>' % "".join('<dt>%s</dt><dd>%s</dd>' % (x(t, GL_TERM_EN.get(t, t)), x(GLOSSARY[t], GL_EN[t])) for t in GLOSSARY)
P.append(bolum("sozluk", "Terim Sözlüğü", "Glossary", sozluk))
govde = "\n".join(P[:-2]) if False else govde + "\n" + "\n".join(P[-2:])

CSS_SON = """
.lg{display:inline-block;width:16px;height:16px;vertical-align:-3px;margin-right:6px;border-radius:3px;background-size:cover;background-position:center;background-color:#fff;flex:0 0 auto}
.rank li .rl .lg{margin-right:7px}
.h3n{margin:-6px 0 12px;color:var(--ink-2);font-size:13px;line-height:1.55;max-width:78ch}
.insight ul.ins-li{margin:8px 0 0;padding-left:18px}
.insight ul.ins-li li{margin:0 0 5px}
.insight .ins-ref{display:inline-block}
.note ul.nl{margin:0;padding-left:18px}
.note ul.nl li{margin:0 0 6px;color:var(--ink)}
.note ul.nl li:last-child{margin-bottom:0}
.tw.uzun{max-height:min(60vh, 560px);overflow:auto}
.two{grid-template-columns:minmax(0,1fr) minmax(0,1fr)}
.two > div{min-width:0}
@media(max-width:1180px){.two{grid-template-columns:minmax(0,1fr)}}
.tw.uzun thead th{position:sticky;top:0;z-index:2}

/* grafik sekmeleri ve lejant ac/kapa */
.tabs.gtabs{margin:4px 0 8px}
.tabs.gtabs.ic{margin:0 0 6px}
.tabs.gtabs.ic button{font-size:11.5px;padding:4px 10px}
.legend .lg-t{cursor:pointer;user-select:none;border-radius:4px;padding:1px 4px}
.legend .lg-t:hover{color:var(--ink)}
.legend .lg-t:focus-visible{outline:2px solid var(--coral);outline-offset:1px}
.legend .lg-t.off{opacity:.38;text-decoration:line-through}

/* duzen: icindekiler sola bitisik, icerik alani genis */
.appbar .in{max-width:none;padding:12px max(24px,3vw) 12px 16px}
.wrap{max-width:none;margin:0;padding:0 max(24px,3vw) 0 14px;gap:30px}
main{max-width:1280px}
@media(max-width:940px){.wrap{padding:0 16px}.appbar .in{padding:10px 16px}}
/* basliklar */
h2{position:relative;padding-bottom:9px;border-bottom:1px solid var(--line)}
h2::after{content:"";position:absolute;left:0;bottom:-1px;width:72px;height:3px;border-radius:2px;background:linear-gradient(90deg,var(--coral) 0%,var(--coral-deep) 100%)}
h3{display:inline-block;padding:1px 10px 1px 0;border-radius:2px;background:linear-gradient(to top,var(--coral-tint) 0 34%,transparent 34%)}
.two h3{display:inline-block}
.h3n{max-width:none}
/* vurgu */
b.mk{font-weight:650;color:var(--ink)}
.hl{color:var(--coral-deep);font-weight:650}
/* kelime hacim rozeti */
.kwlist .kw .kv{font-style:normal;font-size:10.5px;margin-left:7px;padding:0 5px;border-radius:4px;background:var(--coral-tint);color:var(--coral-deep);font-weight:650;font-family:"Segoe UI",Arial,sans-serif}
/* tablo araclari */
.tbox{margin:0 0 14px}
.tbox .tw{margin:0}
.tbar{display:flex;justify-content:flex-end;margin:0 0 4px}
.tcopy{display:inline-flex;align-items:center;gap:5px;font:inherit;font-size:11px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:2px 8px;cursor:pointer;line-height:1.4}
.tcopy:hover,.tcopy:focus-visible{color:var(--ink);border-color:var(--ink-2)}
.tcopy.ok{color:var(--green);border-color:var(--green)}
th.srt{cursor:pointer;user-select:none}
th.srt .q::after{content:"";display:inline-block;width:0;height:0;margin-left:5px;vertical-align:middle;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(255,255,255,.35)}
th.srt.sa .q::after{border-top:0;border-bottom:5px solid var(--coral)}
th.srt.sd .q::after{border-top:5px solid var(--coral)}
"""
# ---------------------------------------------------------------- icindekiler
KISA = {"ihtiyac": ("İhtiyaç Dili", "Need Language"), "youtube": ("YouTube: Montaj ve Tamir", "YouTube: Installation and Repair"), "rakip": ("Rakip Görünürlüğü ve Ölçek", "Competitor Visibility and Scale"),
        "model": ("Kanal Rolleri ve Model", "Channel Roles and Model"), "panel": ("Resmi Mağaza Paneli", "Official Store Panel"), "makro": ("Makro Ortam", "Macro Environment"), "talep": ("Kategori Talebi", "Category Demand"), "organik": ("Organik Kanal", "Organic Channel"),
        "marka": ("Marka Aramaları", "Brand Searches"), "ssgbm": ("SSG ve BM Derin Talep", "SSG and BM In Depth"), "katalog": ("Katalog ve Talep", "Catalogue and Demand"), "yeni": ("Yeni Kategori ve Segment", "New Categories and Segments"), "set": ("Set ve Ürün + Hizmet", "Sets and Product + Service"), "benchmark": ("Benchmark ve Dijital Deneyim", "Benchmark and Digital Experience"), "serp": ("Google SERP ve AI Overview", "Google SERP and AI Overview"), "trafik": ("Marka Sitelerinde Trafik", "Traffic on Brand Sites"), "pazaryeri": ("Pazaryeri ve Çok Satanlar", "Marketplaces and Best Sellers"), "politika": ("Kanal Politikaları", "Channel Policies"), "sikayet": ("Şikayetvar: Satış Sonrası", "Şikayetvar: After-Sales"), "fiyat": ("Fiyat ve Satıcı Manzarası", "Price and Seller Landscape"), "derin": ("Alt Kategori Derinliği", "Sub-Category Depth")}
KUMELER = [("DURUM", "STATUS", ["ozet", "makro"]), ("TALEP", "DEMAND", ["talep", "ssgbm", "ihtiyac", "organik", "marka", "serp", "youtube", "sikayet"]), ("FIRSAT", "OPPORTUNITY", ["katalog", "yeni", "set"]), ("REKABET VE MODEL", "COMPETITION AND MODEL", ["rakip", "trafik", "pazaryeri", "derin", "panel", "fiyat", "politika", "benchmark", "model"]),
           ("PLAN", "PLAN", ["adimlar"]), ("EK", "APPENDIX", ["yontem", "kaynakca", "sozluk"])]
_bas = dict(BOLUMLER); _sira = {b: i + 1 for i, (b, _) in enumerate(BOLUMLER)}
_kumede = [b for _, _, ids in KUMELER for b in ids]
if _kumede != [b for b, _ in BOLUMLER]:
    raise SystemExit("Küme sırası belge sırasıyla uyuşmuyor: %s" % [b for b, _ in BOLUMLER if b not in _kumede])
def _toc():
    out = []
    for tr, en, ids in KUMELER:
        out.append('<p class="grp">%s</p><ul class="tocg">' % x(tr, en))
        for b in ids:
            kisa = x(*KISA[b]) if b in KISA else _bas[b]
            out.append('<li><a href="#%s" title="%s"><span class="no">%02d</span><span class="tx">%s</span></a></li>' % (b, _bas[b], _sira[b], kisa))
        out.append('</ul>')
    return "".join(out)
toc = _toc()
target_css = "".join(
    (':root:not(.js) body:has(#%s:target) .sidenav a[href="#%s"]{background:var(--coral-tint);color:var(--ink);font-weight:640}'
     ':root:not(.js) body:has(#%s:target) .sidenav a[href="#%s"] .no{background:var(--teal);color:#fff}') % (b, b, b, b) for b, _ in BOLUMLER)

# ---------------------------------------------------------------- excel dugmesi
def dl_buton(sinif=""):
    if not os.path.exists(XLS): return ""
    b64 = base64.b64encode(open(XLS, "rb").read()).decode(); kb = round(os.path.getsize(XLS) / 1024)
    with zipfile.ZipFile(XLS) as z: sekme = sum(1 for nm in z.namelist() if nm.startswith("xl/worksheets/sheet"))
    x("Veri dosyasını indir · %d sekme · %s KB" % (sekme, kb), "Download the data file · %d sheets · %s KB" % (sekme, kb))
    x("· Excel, %s KB" % kb, "· Excel, %s KB" % kb)
    return ('<a class="dl %s" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,%s" download="%s" title="Veri dosyasını indir · %d sekme · %s KB">%s<span class="t">%s</span> <span class="dl-alt">&middot; Excel, %s KB</span></a>'
            % (sinif, b64, os.path.basename(XLS), sekme, kb, IKON, x("Veri dosyası", "Data file"), kb))

# ---------------------------------------------------------------- hero
HERO = """<div class="hero dark"><div class="ring"></div>
  <p class="eyebrow">%s</p>
  <h1>%s</h1>
  <p class="sub">%s</p>
  <div class="chips"><span class="chip f">%s</span><span class="chip">%s</span><span class="chip">%s</span><span class="chip">%s</span><span class="chip">%s</span></div>
</div>""" % (x("VitrA TÜRKİYE · E-TİCARET BÜYÜME FIRSATLARI", "VitrA TURKEY · E-COMMERCE GROWTH OPPORTUNITIES"),
             x("E-Ticaret Büyüme Fırsatları: Talep, Kullanıcı Davranışı ve Kanal Modeli", "E-Commerce Growth Opportunities: Demand, User Behaviour and Channel Model"),
             x("Pazar talebi, SSG ve BM derin incelemesi, katalog boşlukları, yeni kategori ve segmentler, set ve ürün + hizmet modelleri, benchmark ve makro ortam verileriyle vitra.com.tr, Trendyol ve Hepsiburada için büyüme fırsatları. Pazaryeri ve GA4 verisiyle genişletilecektir.",
               "Growth opportunities for vitra.com.tr, Trendyol and Hepsiburada built on market demand, an in-depth SSG and BM review, catalogue gaps, new categories and segments, set and product + service models, benchmarks and macro data. To be extended with marketplace and GA4 data."),
             x("Sürüm 6 · %s" % "30.09.2026", "Version 6 · %s" % "30.09.2026"), x("Talep: Eyl 2022 - Ağu 2026", "Demand: Sep 2022 - Aug 2026"), x("Search Console: Haz 2025 - Eyl 2026", "Search Console: Jun 2025 - Sep 2026"),
             x("53 bin kelime · 58 tema", "53K keywords · 58 themes"), x("Türkiye", "Turkey"))

DOC = """<!doctype html>
<html lang="tr" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VitrA Türkiye | E-Ticaret Büyüme Fırsatları</title>
<style>%s
%s</style></head>
<body>
<header class="appbar"><div class="in">
  <div class="brandbit"><span class="lbl">%s</span>
    <span class="logo-card"><img src="%s" alt="VitrA"></span></div>
  <div class="brandbit" style="gap:12px">%s%s<span class="lbl">%s</span>
    <span class="ib"><img src="%s" alt="Inbound"></span></div>
</div></header>
<div class="wrap">
<nav class="sidenav" aria-label="%s"><div class="tocbox">%s</div></nav>
<main>
%s
%s
<footer>%s<br>%s</footer>
</main></div>
<button class="tocfab" id="tocfab" type="button" aria-expanded="false" aria-controls="tocsheet" aria-label="%s">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h10"/></svg></button>
<div class="tocsheet" id="tocsheet" role="dialog" aria-modal="true" aria-label="%s">
  <div class="tocsheet__in"><div class="tocsheet__tut"></div>%s</div>
</div>
<script>%s</script>
</body></html>""" % (CSS + CSS_EK + KAYNAKCA_CSS + CSS_SON + logo_css(), target_css, x("Marka", "Brand"), VITRA, TEMA, dl_buton(), x("Hazırlayan", "Prepared by"), INBOUND, x("İçindekiler", "Contents"), toc, HERO, govde,
                     dl_buton("dl-foot"), x("Hacimler Google Keyword Planner &middot; sayfa ve sorgu verisi Google Search Console &middot; rakip ölçümü Ahrefs &middot; makro seriler TCMB EVDS &middot; autocomplete ve YouTube Google",
                                            "Volumes Google Keyword Planner &middot; page and query data Google Search Console &middot; competitor measurement Ahrefs &middot; macro series CBRT EVDS &middot; autocomplete and YouTube Google"),
                     x("İçindekiler menüsünü aç", "Open the contents menu"), x("İçindekiler", "Contents"), toc, JS)
x("VitrA Türkiye | E-Ticaret Büyüme Fırsatları", "VitrA Turkey | E-Commerce Growth Opportunities"); x("html", "html")
x("Açık ve koyu tema arasında geçiş yap", "Switch between light and dark theme"); x("Tema değiştir", "Switch theme"); x("Erişim", "Accessed")
ceviri.EN.update(t2_ortak.EK)
if t2_ortak._CAKISMA: print("uyarı · farklı çeviri:", t2_ortak._CAKISMA)
dil.TERIMLER = {t: (GLOSSARY[t], GL_TERM_EN.get(t, t), GL_EN[t]) for t in GLOSSARY}
DOC, _n, _de = dil.uygula(DOC, "VitrA Turkey | E-Commerce Growth Opportunities")
yol = os.path.join(veri.KOK, AD + ".html")
open(yol, "w", encoding="utf-8").write(DOC)
if _eksik_h3: print("uyarı · açıklaması olmayan alt başlık:", _eksik_h3)
print("kaydedildi:", yol, len(DOC), "karakter,", len(BOLUMLER), "bölüm,", _n, "ifade çevrildi")
