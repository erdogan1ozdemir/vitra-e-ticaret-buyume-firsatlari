# -*- coding: utf-8 -*-
"""VitrA e-ticaret buyume firsatlari · HTML rapor uretimi (TR + EN tek dosya)."""
import os, sys, base64, zipfile, json, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import veri
from rapor_parca1 import VITRA, INBOUND, GLOSSARY
from rapor_css import CSS
from css_ek import CSS_EK
from rapor_js import JS, KAYNAKCA_CSS, TEMA, IKON
import t2_ortak, kaynakca, ceviri, dil, ortak
from t2_ortak import x, R
from ortak import logo_css, logo_alan_adlari, lg
import h3_not
import b_seomonitor
import b_ozet, b_geo, b_makro, b_talep, b_ssgbm, b_niyet, b_organik, b_marka, b_youtube, b_katalog, b_yeni, b_set, b_rakip, b_benchmark, b_model, b_adimlar, b_yontem, b_serp, b_rakip_sw, b_kategori_trafik, b_pazaryeri, b_politika, b_sikayet, b_fiyat, b_derin, b_panel, b_yorum

AD = "VitrA_E-Ticaret_Buyume_Firsatlari"
XLS = os.path.join(veri.KOK, AD + ".xlsx")

# ---------------------------------------------------------------- bolumler
BOLUMLER = []
def bolum(bid, tr, en, govde):
    BOLUMLER.append((bid, tr))
    return '<section id="%s"><h2><span class="h2i"><span class="no">%02d</span>%s</span></h2>%s</section>' % (bid, len(BOLUMLER), x(tr, en), govde)

P = []
P.append(bolum("ozet", "Özet", "Summary", b_ozet.HTML))
P.append(bolum("makro", "Ekonomik Ortam: Harcama, Güven ve Konut Piyasası", "Economic Environment: Spending, Confidence and Housing Market", b_makro.HTML))
P.append(bolum("talep", "Kategori Talebi ve Dönemsel Değişim", "Category Demand and Period Change", b_talep.HTML))
P.append(bolum("ssgbm", "SSG ve BM: Derin Talep İncelemesi", "SSG and BM: In-Depth Demand Review", b_ssgbm.HTML))
P.append(bolum("ihtiyac", "İhtiyaç Dili: Kullanıcı Ne Arıyor?", "Need Language: What Is the User Searching For?", b_niyet.HTML))
P.append(bolum("organik", "GSC - Organik Kanal", "GSC - Organic Channel", b_organik.HTML))
import b_genai
P.append(bolum("yapayzeka", "Google Yapay Zeka Özellikleri ve Organik Tık", "Google AI Features and Organic Clicks", b_genai.HTML))
import b_ga4
P.append(bolum("ga4", "GA4 - Site ve E-Ticaret Performansı", "GA4 - Site and E-Commerce Performance", b_ga4.HTML))
P.append(bolum("marka", "Marka Aramaları ve Autocomplete", "Brand Searches and Autocomplete", b_marka.HTML))
P.append(bolum("serp", "Google Arama Sonuçları ve AI Overview", "Google Search Results and AI Overview", b_serp.HTML))
P.append(bolum("youtube", "YouTube: Montaj, Tamir ve Karar Videoları", "YouTube: Installation, Repair and Decision Videos", b_youtube.HTML))
P.append(bolum("sikayet", "Şikayetvar: Satış Sonrası Deneyim", "Şikayetvar: After-Sales Experience", b_sikayet.HTML + b_yorum.KOPRU_SIKAYET))
P.append(bolum("katalog", "Katalog ve Talep Eşleşmesi", "Catalogue and Demand Fit", b_katalog.HTML))
P.append(bolum("yeni", "Yeni Kategori ve Segment Fırsatları", "New Category and Segment Opportunities", b_yeni.HTML))
P.append(bolum("set", "Set, Komple Banyo ve Ürün + Hizmet", "Sets, Complete Bathrooms and Product + Service", b_set.HTML))
P.append(bolum("rakip", "Rakip Görünürlüğü ve Kanal Ölçeği", "Competitor Visibility and Channel Scale", b_rakip.HTML + b_seomonitor.HTML_SOC + b_rakip_sw.HTML))
P.append(bolum("trafik", "Marka ve Uzman Sitelerde Kategori Trafiği", "Category Traffic on Brand and Specialist Sites", b_kategori_trafik.HTML))
P.append(bolum("pazaryeri", "Pazaryerleri: Kategori Yapısı ve Çok Satanlar", "Marketplaces: Category Structure and Best Sellers", b_pazaryeri.HTML))
P.append(bolum("derin", "Pazaryeri Alt Kategori Derinliği: Çok Satanlar ve Rakip Mağazalar", "Marketplace Sub-Category Depth: Best Sellers and Competitor Stores", b_derin.HTML))
P.append(bolum("panel", "VitrA Resmi Mağaza: Pazaryeri Panel Verisi", "VitrA Official Store: Marketplace Panel Data", b_panel.HTML + b_yorum.KOPRU_PANEL))
P.append(bolum("yorum", "Pazaryeri Yorumları ve Soru-Cevap: Sentiment ve Pain Point Analizi", "Marketplace Reviews and Q&A: Sentiment and Pain Point Analysis", b_yorum.HTML))
P.append(bolum("fiyat", "Fiyat ve Satıcı Manzarası: Shopping, Trendyol, Hepsiburada", "Price and Seller Landscape: Shopping, Trendyol, Hepsiburada", b_fiyat.HTML))
P.append(bolum("politika", "Kanal Politikaları ve Keşif Kanalları", "Channel Policies and Discovery Channels", b_politika.HTML))
import b_yolculuk, b_seomonitor
P.append(bolum("yolculuk", "vitra.com.tr Satın Alma Yolculuğu: Site İçi Arama, Sepet ve Ödeme", "vitra.com.tr Purchase Journey: Site Search, Cart and Checkout", b_yolculuk.HTML))
P.append(bolum("benchmark", "Benchmark: E-Ticaret Modelleri ve Dijital Deneyim", "Benchmark: E-Commerce Models and Digital Experience", b_benchmark.HTML))
P.append(bolum("model", "Kanal Rolleri ve Etkileşim Modeli", "Channel Roles and Engagement Model", b_model.HTML))
P.append(bolum("geo", "AI Arama ve GEO Fırsatları", "AI Search and GEO Opportunities", b_geo.HTML))
P.append(bolum("adimlar", "Sonraki Adımlar İçin Öneriler", "Recommendations for Next Steps", b_adimlar.HTML))
P.append(bolum("ek", "Terim Sözlüğü, Kaynakça, Yöntem ve Kapsam", "Glossary, References, Method and Scope", "<!--EK-BAS-->" + "<h3>%s</h3>" % x("Yöntem ve Kapsam", "Method and Scope") + b_yontem.HTML))

govde = "\n".join(P)
# --- son islemler: alt baslik aciklamasi, uzun tablo, logo
from ortak import hid as _hid
from t2_ortak import _kalin_cift
_IDLER = set()
def _h3_id(t):
    i = _hid(t); j = i; k_ = 2
    while j in _IDLER: j = "%s-%d" % (i, k_); k_ += 1
    _IDLER.add(j); return j
import serp_ozet as _SO
from ortak import kopru as _kopru
# alt basliktan ilgili veri seti alt sayfasina dugme (basligin aciklama notunun hemen altinda)
H3_ALT = {
 "A · Kim sıralanıyor?": ("Üç gruptaki %d kelimenin ilk 10 sonucu, AI Overview kaynakları ve \"Diğer sorular\" kutusu süzülebilir tablolar halinde ayrı sayfadadır." % _SO.NT,
                      "The top 10 results, AI Overview sources and \"People also ask\" box for the %d keywords in all three groups are in filterable tables on a separate page." % _SO.NT, "arama-sonuclari.html", "Arama Sonuçları sayfasını görüntüle", "View the Search Results page", ""),
 "Kullanıcının Google'da sorduğu sorular": ("%d sorunun tamamı, çıktığı kelimelerle birlikte:" % len(_SO.PAA_SORU), "All %d questions with the keywords where they appeared:" % len(_SO.PAA_SORU), "arama-sonuclari.html", "Soruları görüntüle", "View the questions", "#paa"),
 "Ana kategori düzeyinde değişim": ("Talep bölümlerindeki 2.299 kelimenin tamamı, kategori, niyet ve iki dönemin arama hacmiyle:", "All 2,299 keywords in the demand sections, with category, intent and search volume for both periods:", "kelime-evreni.html", "Kelime Evreni sayfasını görüntüle", "View the Keyword Universe page", ""),
 "Autocomplete önerilerinin tema oranı": ("Tüm otomatik tamamlama önerileri, kök ifade ve grupla:", "All autocomplete suggestions, with seed term and group:", "kelime-evreni.html", "Önerileri görüntüle", "View the suggestions", "#oneriler"),
 "Alt kesitler: vitra.com.tr, pazaryeri ve fiyat karşılaştırma siteleri": ("Taramadaki 11.982 ürün kartının tamamı (kanal, marka, satıcı, fiyat, puan):", "All 11,982 product cards from the scan (channel, brand, seller, price, rating):", "pazaryeri-taramasi.html", "Pazaryeri Taraması sayfasını görüntüle", "View the Marketplace Scan page", ""),
 "Genişletilmiş tarama: 68 arama, altı niyet grubu": ("68 aramanın tüm video sonuçları ve kanal özeti:", "All video results of the 68 searches and the channel summary:", "youtube-videolari.html", "YouTube Videoları sayfasını görüntüle", "View the YouTube Videos page", ""),
}
def _h3_not(m):
    t = m.group(1)
    ek_ = _kopru(*H3_ALT[t]) if t in H3_ALT else ""
    if t in h3_not.N:
        tr, en = h3_not.N[t]; return '<h3 id="%s">%s</h3><p class="h3n">%s</p>%s' % (_h3_id(t), t, x(*_kalin_cift(tr, en)), ek_)
    return '<h3 id="%s">%s</h3>%s' % (_h3_id(t), t, ek_)
_eksik_h3 = sorted({m for m in re.findall(r'(?<!</span>)<h3>([^<]+)</h3>', govde) if m not in h3_not.N and m != "Öne çıkan bulgular"})   # not eşleşmesinden önce bakılır (sonra tüm başlıklar id alır)
govde = re.sub(r'<h3>([^<]+)</h3>', _h3_not, govde)
_yok = [t for t in H3_ALT if 'id="%s"' % _hid(t) not in govde]
if _yok: raise SystemExit('alt sayfa dugmesi icin baslik bulunamadi: %s' % _yok)
# cok sutunlu tablolar: sutun sayisina gore asgari genislik, ilk (metin) sutununa asgari genislik
def _genislik(m):
    blok = m.group(0); nc = blok[:blok.find("</tr>")].count("<th")
    if nc < 6 or "genis" in m.group(1) or "urunt" in m.group(1) or "kompakt" in m.group(1): return blok
    return blok.replace('<div class="tw %s">' % m.group(1), '<div class="tw %s cok" style="--nc:%d">' % (m.group(1), nc), 1) if m.group(1) else blok.replace('<div class="tw">', '<div class="tw cok" style="--nc:%d">' % nc, 1)
govde = re.sub(r'<div class="tw ?([^"]*)">.*?</table></div>', _genislik, govde, flags=re.S)
# tablolarda VitrA satiri: ilk hucresi VitrA / vitra.com.tr olan satirlar hafif zeminle vurgulanir
_VR = re.compile(r'<tr><td>(?:<[^>]+>\s*)*(?:VitrA|vitra\.com\.tr)(?:\s*\([^)]*\))?\s*(?:<[^>]+>\s*)*</td>')
govde = _VR.sub(lambda m: m.group(0).replace("<tr><td>", '<tr class="vsat"><td>', 1), govde)
# ozetteki ok baglantilarinin hedefi var mi?
_hedef = set(re.findall(r'id="([^"]+)"', govde))
_kayip = sorted(set(re.findall(r'<a class="git" href="#([^"]+)"', govde)) - _hedef)
if _kayip: raise SystemExit("Ok bağlantısının hedefi bulunamadı: %s" % _kayip)
def _uzun(m):
    blok = m.group(0)
    if 'uzun' in m.group(1): return blok
    n_ = blok.count('<tr>') - 1
    return blok.replace('<div class="tw %s">' % m.group(1), '<div class="tw %s uzun">' % m.group(1), 1) if n_ > 9 else blok
govde = re.sub(r'<div class="tw ([^"]*)">.*?</table></div>', _uzun, govde, flags=re.S)
# ekran disindaki tablolar cizilmez (content-visibility); henuz cizilmemis tablonun yeri satir sayisindan tahmin edilir (--ih)
def _ih(m):
    acilis, stil, ic = m.group(1), m.group(2) or "", m.group(3)
    n_ = max(1, ic.count("<tr") - ic.count("<thead"))
    h_ = 46 + 37 * n_
    if " uzun" in acilis: h_ = min(h_, 560)
    stil = (stil[:-1] + ';--ih:%dpx"' % h_) if stil else ' style="--ih:%dpx"' % h_
    return acilis + stil + ">" + ic + "</div>"
govde = re.sub(r'(<div class="tw(?: [^"]*)?")((?: style="[^"]*")?)>(.*?</table>)</div>', _ih, govde, flags=re.S)
_LOGO = sorted(logo_alan_adlari(), key=len, reverse=True)
_LG = re.compile(r'(<(?:td|span class="rl")>|<a class="(?:u|dis)"[^>]*>)((?:www\.)?(' + "|".join(re.escape(d) for d in _LOGO) + r'))(?=</)')
govde = _LG.sub(lambda m: m.group(1) + lg(m.group(3)) + m.group(2), govde)
_BNO = {b_: "%02d" % (i + 1) for i, (b_, _) in enumerate(BOLUMLER)}
def _btok(t):
    # Bölüm numarasından sonra gelen bulunma eki numaraya göre yeniden kurulur (20'de, 08'de, 06'da)
    t = re.sub(r"\[\[b:([a-z]+)\]\]'(?:da|de|ta|te)\b", lambda m: (_BNO.get(m.group(1), "??") + "'" + ortak.ek(int(_BNO[m.group(1)]), "de").split("'")[1]) if m.group(1) in _BNO else "??", t)
    return re.sub(r"\[\[b:([a-z]+)\]\]", lambda m: _BNO.get(m.group(1), "??"), t)
govde = _btok(govde)
t2_ortak.EK = {_btok(k_): _btok(v_) for k_, v_ in t2_ortak.EK.items()}
if "??" in govde: raise SystemExit("Bölüm atfı çözülemedi")
# Yontem tablosundaki "Kullanildigi bolum" hucreleri: kaynakca kodlarinin raporda atif aldigi bolum numaralari
_KB = {}
for _m in re.finditer(r'<section id="([^"]+)">(.*?)</section>', govde, re.S):
    if _m.group(1) == "ek": continue
    for _r in re.findall(r"\[\[ref:([^\]]+)\]\]", _m.group(2)):
        for _c in _r.split(","): _KB.setdefault(_c.strip(), set()).add(_BNO[_m.group(1)])
def _bk(t):
    return re.sub(r"\[\[bk:([^\]]+)\]\]", lambda m: ", ".join(sorted({n_ for c_ in m.group(1).split(",") for n_ in _KB.get(c_.strip(), ())})) or "-", t)
govde = _bk(govde); t2_ortak.EK = {_bk(k_): _bk(v_) for k_, v_ in t2_ortak.EK.items()}
# Tablo kaynak logoları: "Tabloyu kopyala" düğmesinin solunda kaynak logosu ve hover'da kaynak, kapsam, veri dönemi (tablo_kaynak.py)
import tablo_kaynak
govde, _TKR = tablo_kaynak.uygula(govde, t2_ortak.EK, x)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "tablo_kaynak_rapor.txt"), "w", encoding="utf-8").write("\n".join("%s | %s | %s | %s" % (a_, t_, b_, ", ".join(c_)) for a_, t_, b_, c_ in _TKR))
govde, sira = kaynakca.coz(govde)
_KAY = kaynakca.bolum_html(sira, x)
GL_EN = {
 "CTR": "Click-through rate; the share of impressions that turn into clicks.",
 "SSS": "Frequently asked questions; the Q&A pages in the support section.",
 "Search Console": "Google's measurement tool for site owners; shows the site's impressions, clicks and average position in Google search.",
 "Keyword Planner": "The Google Ads keyword tool; gives the average monthly search volume of keywords.",
 "SEOmonitor": "A measurement tool tracking the daily Google positions of the site and competitors, SERP features and estimated click share for selected keywords.",
 "Similarweb": "A market measurement tool estimating sites' total visits and traffic channels.",
 "Click payı": "The distribution of estimated organic clicks from tracked keywords across domains (share of clicks).",
 "Prompt": "A question or instruction given to an AI tool.",
 "AI Mode": "Google's conversational AI search mode.",
 "TÜİK": "Turkish Statistical Institute.",
 "KDV": "Value added tax (VAT).",
 "DR": "Domain Rating; Ahrefs' link strength score for a domain, on a 0-100 scale.", "Organik trafik": "Free visits from search engines; in the report given as Search Console clicks, an Ahrefs estimate or a Similarweb estimate depending on the source.",
 "Paid trafik": "Ahrefs' estimate of monthly visits from Google Ads.",
 "Autocomplete": "Completion phrases suggested while typing in the Google search box; derived from real user searches.",
 "Pure player": "A retailer without physical stores that sells online only.",
 "Retargeting": "A reminder ad shown later to a user who visited the site.", "Kartlı Ödeme Endeksi": "An index the CBRT derives from bank and credit card spending; the real series is inflation-adjusted.",
 "Net yüzde": "A survey indicator obtained by subtracting the share of negative answers from the share of positive answers.",
 "SSG": "Sanitaryware; vitreous china products such as WCs, washbasins, bidets and urinals; cisterns are also included in this group in the report.",
 "BM": "Bathroom furniture; basin units, tall cabinets, mirror cabinets, mirrors, countertops and complements.",
 "3P": "Third-party seller; a seller other than the brand itself that sells the product on a marketplace or the brand site.",
 "GA4": "Google Analytics 4; the analytics tool measuring the site's visits, conversions and product performance.",
 "SERP": "Search Engine Results Page; the results page Google returns for a search.",
 "KD": "Keyword Difficulty; Ahrefs' 0-100 score for how hard it is to rank in the top 10 for a keyword.",
 "TP": "Traffic Potential; the estimated monthly traffic the page ranking first receives from all its keywords (Ahrefs).",
 "PAA": "People Also Ask; the \"related questions\" box on the search results page.",
 "AI Overview": "The AI-generated summary Google shows above search results; it links to the sites it cites.",
 "YoY": "Year over year; a period's change against the same period of the previous year.",
 "TCMB": "Central Bank of the Republic of Türkiye.",
 "EVDS": "CBRT Electronic Data Delivery System; the database publishing macro and financial series.",
 "BKM": "Interbank Card Center; the source of card payment statistics.",
 "Buybox": "The seller that wins the \"add to basket\" button among sellers offering the same product on a marketplace.",
 "PVC": "Polyvinyl chloride; a water-resistant plastic body material.",
 "Lead": "A pre-purchase contact request; a measurable prospect event such as a form, call-back or appointment.",
 "SKU": "Stock keeping unit; the unique code of each product variant including colour and size.",
 "GEO": "Generative Engine Optimization; preparing content and brand information so that it is cited in AI answers.",
 "Entity": "The single record through which search engines and AI models recognise a brand or company; it holds information such as name, founding, website and related brands.",
 "Wikidata": "The openly editable structured knowledge base linked to Wikipedia; search engines and AI models also read brand information from it.",
 "llms.txt": "A text file placed at the site root that summarises the site's key pages for AI tools.",
 "Merchant Center": "The Google tool through which product information is submitted to be shown in Google Shopping and free product listings.",
 "Yerel paket": "The list of local businesses shown with a map on the results page (Local pack).",
 "Desi": "A volumetric weight unit used in shipping pricing in Turkey.",
 "Medyan": "The middle value of ordered values; less affected by extreme prices than the average.",
 "MDF": "Medium-density fibreboard; a common body material in bathroom furniture.",
}
GL_TERM_EN = {"SSS": "FAQ", "Click payı": "Click share", "TÜİK": "TurkStat", "KDV": "VAT", "Yerel paket": "Local pack", "Desi": "Desi (volumetric weight)", "Medyan": "Median", "Organik trafik": "Organic traffic", "Paid trafik": "Paid traffic", "Kartlı Ödeme Endeksi": "Card Payment Index", "Net yüzde": "Net percentage", "SSG": "SSG", "BM": "BM", "3P": "3P", "TCMB": "CBRT", "EVDS": "EVDS"}
_TRS = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
sozluk = '<dl class="gl sozluk">%s</dl>' % "".join('<dt>%s</dt><dd>%s</dd>' % (x(t, GL_TERM_EN.get(t, t)), x(GLOSSARY[t], GL_EN[t])) for t in sorted(GLOSSARY, key=lambda t_: t_.translate(_TRS).lower()))
# Ek bölümü: sırasıyla Terim Sözlüğü, Kaynakça, Yöntem ve Kapsam
govde = govde.replace("<!--EK-BAS-->", '<h3 id="sozluk">%s</h3><p class="h3n">%s</p>%s<h3 id="kaynakca">%s</h3>%s' % (
    x("Terim Sözlüğü", "Glossary"),
    x("Raporda geçen kısaltma ve terimlerin kısa tanımları; metinde noktalı alt çizgili terimlerin üzerine gelindiğinde aynı tanım açılır.",
      "Short definitions of the abbreviations and terms used in the report; hovering over a dotted-underlined term in the text opens the same definition."), sozluk,
    x("Kaynakça", "References"), _KAY), 1)
if "<!--EK-BAS-->" in govde: raise SystemExit("Ek bölümü yer tutucusu bulunamadı")

CSS_SON = """
sup.ref{margin-left:.18em}
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
.fnote .fc{display:block;margin:0 0 4px}
.fnote h3,.kpi h3,.step h3,.box h3{display:block;background:none;padding:0;text-decoration:none}
.popb{font:inherit;font-size:12px;color:var(--coral-deep);background:var(--coral-tint);border:1px solid transparent;border-radius:14px;padding:2px 10px;cursor:pointer;margin-left:6px;white-space:nowrap}
.popb:hover,.popb:focus-visible{border-color:var(--coral-deep)}
.popb.ic{padding:0 6px;font-size:11px;line-height:1.5;margin-left:6px;vertical-align:1px}
dialog.popd{width:min(1100px,94vw);max-height:86vh;padding:0;border:1px solid var(--line);border-radius:12px;background:var(--card);color:var(--ink);box-shadow:0 20px 60px rgba(0,0,0,.25)}
dialog.popd::backdrop{background:rgba(16,51,47,.45)}
.pophd{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--card);z-index:3}
.popx{font:inherit;font-size:20px;line-height:1;background:none;border:0;color:var(--muted);cursor:pointer;padding:0 4px}
.popbd{padding:12px 16px 16px;overflow:auto;max-height:calc(86vh - 52px)}
.popbd .tw{max-height:calc(86vh - 170px);max-height:calc(86dvh - 170px)}
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
h2{position:relative;padding-bottom:0;border-bottom:1px solid var(--line);font-size:23.6px}
h2 .h2i{display:inline-block;padding-bottom:9px;margin-bottom:-1px;border-bottom:3px solid var(--coral-deep)}
@media(max-width:940px){h2{font-size:21.3px}}
@media(max-width:520px){h2{font-size:19.6px}}
h3{display:inline-block;padding:1px 0;text-decoration:underline var(--coral-tint);text-decoration-thickness:.58em;text-underline-offset:-.04em;text-decoration-skip-ink:none}   /* vurgu bandi her satirda yalniz metin kadar (sarilan basliklarda kutu genisligine yayilmaz) */
main h3{font-size:18.6px}
@media(max-width:940px){main h3{font-size:17.4px}}
main .fnote h3{font-size:15px}
/* madde imleri: Inbound turuncusu */
li::marker{color:#E85F36}
.two h3{display:inline-block}
.h3n{max-width:none}
/* vurgu */
b.mb{font-weight:650;color:var(--ink)}
.hl{color:var(--coral-deep);font-weight:650}
/* kelime hacim rozeti */
.kw .kv{display:inline-block;white-space:nowrap;font-style:normal;font-size:10.5px;margin-left:8px;padding:0 5px;border-radius:4px;background:var(--coral-tint);color:var(--coral-deep);font-weight:650;font-family:"Segoe UI",Arial,sans-serif}
/* tablo araclari */
.tbox{margin:0 0 14px}
.tbox .tw{margin:0}
.tbar{display:flex;justify-content:flex-end;align-items:center;gap:10px;margin:0 0 4px}
.tkay{display:inline-flex;align-items:center;gap:5px}
.tk{display:inline-flex;align-items:center;justify-content:center;cursor:help;border:1px solid var(--line);border-radius:6px;padding:3px;background:#fff}
.tk .lg{width:16px;height:16px;margin:0;vertical-align:0;border-radius:3px}
.lg-web{background-image:url("data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20viewBox%3D%220%200%2024%2024%22%20fill%3D%22none%22%20stroke%3D%22%2310332F%22%20stroke-width%3D%221.8%22%20stroke-linecap%3D%22round%22%3E%3Ccircle%20cx%3D%2212%22%20cy%3D%2212%22%20r%3D%229%22/%3E%3Cpath%20d%3D%22M3%2012h18M12%203c2.6%202.6%203.9%205.6%203.9%209s-1.3%206.4-3.9%209c-2.6-2.6-3.9-5.6-3.9-9S9.4%205.6%2012%203z%22/%3E%3C/svg%3E");background-color:#fff}
.tk:hover{border-color:var(--ink-2)}
.tk:focus-visible{outline:2px solid var(--coral);outline-offset:1px}
.figcap .fkay{float:right;margin:0 0 4px 12px}
.fkay.fk-satir{display:flex;justify-content:flex-end;margin:0 0 6px}
:root{--isi-h:#10332F;--isi-a:#2E7D32;--isi-d:#D32F2F;--isi-kt:#FFFFFF}
:root[data-theme="dark"]{--isi-h:#7FB3A8;--isi-a:#66BB6A;--isi-d:#EF5350;--isi-kt:#0B1513}
.isi-t td.isi-k{color:var(--isi-kt);font-weight:600}
.tw.tw.isi-t table{width:100%;min-width:100%}
.tw.tw.isi-t th{white-space:normal;vertical-align:bottom}
.tw.tw.isi-t th,.tw.tw.isi-t td{padding-left:8px;padding-right:8px;min-width:0}
.tw.tw.isi-t th:first-child,.tw.tw.isi-t td:first-child{min-width:96px}
.isi-t td.isi{white-space:nowrap;font-variant-numeric:tabular-nums}
.isi-t td.isi[data-t]{cursor:help}
.ac[data-t]{cursor:help;border-bottom:1px dotted currentColor}
.ac[data-t]:focus-visible{outline:2px solid var(--acc,#E85F36);outline-offset:2px}
.isi-t td.isi-h{background:color-mix(in srgb,var(--isi-h) calc(var(--a) * 100%),transparent)}
.isi-t td.isi-a{background:color-mix(in srgb,var(--isi-a) calc(var(--a) * 100%),transparent)}
.isi-t td.isi-d{background:color-mix(in srgb,var(--isi-d) calc(var(--a) * 100%),transparent)}
.tcopy{display:inline-flex;align-items:center;gap:5px;font:inherit;font-size:11px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:2px 8px;cursor:pointer;line-height:1.4}
.tcopy:hover,.tcopy:focus-visible{color:var(--ink);border-color:var(--ink-2)}
.tcopy.ok{color:var(--green);border-color:var(--green)}
.theat{display:inline-flex;align-items:center;gap:5px;font:inherit;font-size:11px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:2px 8px;cursor:pointer;line-height:1.4}
.theat:hover,.theat:focus-visible{color:var(--ink);border-color:var(--ink-2)}
.theat[aria-pressed="true"]{color:var(--ink);border-color:var(--ink-2);background:var(--coral-tint)}
/* isi haritasi: metrik renk aileleri (rapor genelinde ayni metrik ayni renk); acik ve koyu tema */
:root{--hm-click:#1F7A6B;--hm-imp:#6F63B0;--hm-ses:#3F7FB8;--hm-gelir:#C08A1E;--hm-satin:#E0663A;--hm-hacim:#2E8B9A;--hm-oran:#9A6B3F;--hm-sira:#5E7F7A;--hm-diger:#6E8784}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--hm-click:#5FC2B0;--hm-imp:#A89BEA;--hm-ses:#79B4E8;--hm-gelir:#E6B655;--hm-satin:#FF9A72;--hm-hacim:#6CC9D6;--hm-oran:#D4A578;--hm-sira:#9FC2BC;--hm-diger:#A9C0BC}}
:root[data-theme="dark"]{--hm-click:#5FC2B0;--hm-imp:#A89BEA;--hm-ses:#79B4E8;--hm-gelir:#E6B655;--hm-satin:#FF9A72;--hm-hacim:#6CC9D6;--hm-oran:#D4A578;--hm-sira:#9FC2BC;--hm-diger:#A9C0BC}
.tw.isi-js td.jh{background:color-mix(in srgb,var(--hc) calc(var(--ha) * 100%),transparent)}
.tw.isi-kapali td.yh,.tw.isi-kapali td.isi-h,.tw.isi-kapali td.isi-a,.tw.isi-kapali td.isi-d,.tw.isi-kapali td.hm{background:none!important}
.tw.isi-kapali td.isi-k{color:inherit;font-weight:inherit}
@media print{.theat{display:none}}
.tcolw{position:relative;display:inline-flex}
.tcol{display:inline-flex;align-items:center;gap:5px;font:inherit;font-size:11px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:2px 8px;cursor:pointer;line-height:1.4}
.tcol:hover,.tcol:focus-visible,.tcol[aria-expanded="true"]{color:var(--ink);border-color:var(--ink-2)}
.tcol.kisik::after{content:"";width:6px;height:6px;border-radius:50%;background:var(--coral-deep);margin-left:2px}
.tcol-p{position:absolute;right:0;top:calc(100% + 6px);z-index:40;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.18);padding:8px 10px;min-width:210px;max-width:min(320px,90vw);max-height:340px;overflow:auto;display:grid;gap:5px;font-size:12.5px}
.tcol-p[hidden]{display:none}
.tcol-p label{display:flex;gap:8px;align-items:center;cursor:pointer;line-height:1.3}
.tcol-p .tcol-all{justify-self:start;margin-top:4px;font:inherit;font-size:11.5px;color:var(--coral-deep);background:transparent;border:0;padding:2px 0;cursor:pointer}
.tfilt{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}
.tfilt button{font:inherit;font-size:12px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);padding:4px 12px;border-radius:999px;cursor:pointer}
.tfilt button[aria-pressed="true"]{background:var(--teal);color:#fff;border-color:var(--teal)}
.gcift{position:relative}
.gcift-b{display:inline-flex;border:1px solid var(--line);border-radius:999px;padding:2px;margin:0 0 8px;background:var(--card)}
.gcift-b button{font:inherit;font-size:11.5px;border:0;background:transparent;color:var(--muted);padding:3px 12px;border-radius:999px;cursor:pointer}
.gcift-b button[aria-pressed="true"]{background:var(--teal);color:#fff}
.gcift-p[hidden]{display:none}
.legend i.kesik{width:16px;height:0;border-top:2.5px dashed;background:transparent}
.fig .dl{display:none}
.fig.dl-acik .dl{display:inline}
.fig .dl-x{display:none!important}
.fig .dl,.fig .dlt{font-size:10px;font-weight:600;paint-order:stroke;stroke:var(--card);stroke-width:3px;stroke-linejoin:round;pointer-events:none}
.fig .dlb{fill:var(--ink-2)}
.fig text.dl.dlb{fill:var(--ink-2)}
.fig text.dl.dli{fill:#fff;stroke:none;font-size:9.5px}
button.dlb{float:right;display:inline-flex;align-items:center;gap:4px;margin:0 0 4px 8px;font:inherit;font-size:11px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:2px 8px;cursor:pointer;line-height:1.4}
button.dlb:hover,button.dlb:focus-visible{color:var(--ink);border-color:var(--ink-2)}
button.dlb[aria-pressed="true"]{color:var(--ink);border-color:var(--ink-2);background:var(--coral-tint)}
.dl-satir{display:flex;justify-content:flex-end;margin:0 0 4px}
.dl-satir button.dlb{float:none}
/* satın alma hunisi: adım kartları ve geçiş oranları (masaüstünde yatay, dar ekranda dikey) */
.hn{--hn-up:var(--green);--hn-dn:var(--red)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .hn{--hn-up:#7CC07F;--hn-dn:#F08A8A}}
:root[data-theme="dark"] .hn{--hn-up:#7CC07F;--hn-dn:#F08A8A}
.hn-g{display:grid;grid-template-columns:86px repeat(6,minmax(0,1fr) 48px) minmax(0,1fr);gap:12px 0;align-items:stretch;margin:6px 0 6px}
.hn-y{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:700;color:var(--ink);line-height:1.25}
.hn-y i{flex:0 0 auto;width:10px;height:10px;border-radius:3px;background:var(--teal)}
.hn-y.hn-y1 i{background:var(--coral-deep)}
.hn-k{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;gap:3px;border-radius:9px;padding:10px 6px;min-height:66px;
  background:var(--teal);color:#fff;font-variant-numeric:tabular-nums;cursor:help;outline-offset:2px}
.hn-k.hn-y1{background:var(--coral-deep)}
:root[data-theme="dark"] .hn-k.hn-y0,:root[data-theme="dark"] .hn-y.hn-y0 i{box-shadow:inset 0 0 0 1px rgba(255,255,255,.22)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .hn-k.hn-y0,:root:not([data-theme="light"]) .hn-y.hn-y0 i{box-shadow:inset 0 0 0 1px rgba(255,255,255,.22)}}
.hn-k .hn-a{font-size:11px;line-height:1.2;opacity:.92}
.hn-k b{font-size:15.5px;font-weight:700;letter-spacing:-.01em}
.hn-k small{font-size:9.5px;opacity:.72;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;line-height:1.25}
.hn-o{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;font-variant-numeric:tabular-nums;color:var(--ink);cursor:help;border-radius:6px;outline-offset:1px}
.hn-o b{font-size:12.5px;font-weight:700}
.hn-o i{font-style:normal;font-size:15px;line-height:1;color:var(--muted)}
.hn-o.up b{color:var(--hn-up)} .hn-o.dn b{color:var(--hn-dn)}
.hn-y0{grid-row:1}.hn-y1{grid-row:2}.hn-y{grid-column:1}
.hn-k.hn-a0{grid-column:2}.hn-k.hn-a1{grid-column:4}.hn-k.hn-a2{grid-column:6}.hn-k.hn-a3{grid-column:8}.hn-k.hn-a4{grid-column:10}.hn-k.hn-a5{grid-column:12}.hn-k.hn-a6{grid-column:14}.hn-o.hn-a1{grid-column:3}.hn-o.hn-a2{grid-column:5}.hn-o.hn-a3{grid-column:7}.hn-o.hn-a4{grid-column:9}.hn-o.hn-a5{grid-column:11}.hn-o.hn-a6{grid-column:13}
@media(max-width:1080px){
  .hn-g{grid-template-columns:1fr 1fr;gap:0 12px}
  .hn-y{grid-row:1;justify-content:center;margin-bottom:8px}.hn-y.hn-y0{grid-column:1}.hn-y.hn-y1{grid-column:2}
  .hn-k.hn-y0,.hn-o.hn-y0{grid-column:1}.hn-k.hn-y1,.hn-o.hn-y1{grid-column:2}
  .hn-k{min-height:0;padding:9px 8px}
  .hn-o{flex-direction:row;gap:6px;padding:5px 0}
  .hn-o i{transform:rotate(90deg)}
  .hn-k.hn-a0{grid-row:2}.hn-k.hn-a1{grid-row:4}.hn-k.hn-a2{grid-row:6}.hn-k.hn-a3{grid-row:8}.hn-k.hn-a4{grid-row:10}.hn-k.hn-a5{grid-row:12}.hn-k.hn-a6{grid-row:14}.hn-o.hn-a1{grid-row:3}.hn-o.hn-a2{grid-row:5}.hn-o.hn-a3{grid-row:7}.hn-o.hn-a4{grid-row:9}.hn-o.hn-a5{grid-row:11}.hn-o.hn-a6{grid-row:13}
}
.fig svg.chart.genis{max-width:none}
.fig:has(svg.chart.genis){overflow-x:auto}
.tw.tw.yatay table{width:100%;min-width:100%}
.tw.tw.yatay th,.tw.tw.yatay td{min-width:0;padding-left:7px;padding-right:7px;white-space:nowrap}
.tw.tw.yatay th:first-child,.tw.tw.yatay td:first-child{min-width:74px}
.yatay td.yh{background:color-mix(in srgb,var(--yr) calc(var(--a) * 100%),transparent);font-variant-numeric:tabular-nums}
.yatay td.yil{font-weight:700}
.yatay td.yil i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px;vertical-align:0}
.yatay tr.deg td{font-weight:600}
.yatay td.top{font-weight:700;border-left:1px solid var(--line)}
:root[data-theme="dark"] .legend i.kesik[style*="#10332F"]{border-top-color:#7FB3A8 !important}
:root[data-theme="dark"] .yatay td.yil i[style*="#10332F"]{background:#7FB3A8 !important}
:root[data-theme="dark"] svg.chart rect[fill="#B9C6C3"],:root[data-theme="dark"] svg.chart rect[fill="#C9D3D1"]{fill:#4B5E5A}
:root[data-theme="dark"] svg.chart rect[fill="#F4B9A3"]{fill:#9A5641}
:root[data-theme="dark"] .legend i[style*="#B9C6C3"],:root[data-theme="dark"] .legend i[style*="#C9D3D1"],:root[data-theme="dark"] #tt i[style*="#B9C6C3"],:root[data-theme="dark"] #tt i[style*="#C9D3D1"]{background:#4B5E5A !important}
:root[data-theme="dark"] .legend i[style*="#F4B9A3"],:root[data-theme="dark"] #tt i[style*="#F4B9A3"]{background:#9A5641 !important}
th.srt{cursor:pointer;user-select:none}
th.srt .q{position:relative;padding-right:12px;display:inline-block}
th.srt .q::after{content:"";position:absolute;right:0;top:50%;margin-top:-2px;width:0;height:0;border-left:4px solid transparent;border-right:4px solid transparent;border-top:5px solid rgba(255,255,255,.35)}
th.srt.sa .q::after{border-top:0;border-bottom:5px solid var(--coral)}
th.srt.sd .q::after{border-top:5px solid var(--coral)}
/* alt sayfa: yorum ve soru seti */
.altlink{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 10px;border-radius:6px;font-size:12px;font-weight:600;white-space:nowrap;
  border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);color:#fff;text-decoration:none}
.altlink:hover,.altlink:focus{background:rgba(255,255,255,.20);border-color:rgba(255,255,255,.5);color:#fff;text-decoration:none}
.altlink:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.altlink svg{width:14px;height:14px;flex:0 0 auto}
.altset{display:flex;gap:6px;flex-wrap:nowrap}
.altmenu{display:none;position:relative}
.altmenu__p{position:absolute;right:0;top:40px;z-index:60;min-width:230px;background:var(--card);border:1px solid var(--line);border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.18);padding:6px}
.altmenu__p[hidden]{display:none}
a.altm{display:flex;align-items:center;gap:9px;padding:9px 10px;border-radius:7px;color:var(--ink);font-size:13.5px;text-decoration:none}
a.altm:hover,a.altm:focus-visible{background:var(--neutral);text-decoration:none}
a.altm svg{width:16px;height:16px;flex:0 0 auto;color:var(--coral-deep)}
@media(max-width:1400px){.altset{display:none}.altmenu{display:block}}
@media(max-width:720px){.altmenu .altlink .lb{display:none}.altmenu .altlink{padding:0 8px}.altmenu__p{position:fixed;left:12px;right:12px;top:60px;min-width:0}}
a.popb.altb{text-decoration:none;display:inline-block;margin-left:0}
.fnote h4.kh4{margin:2px 0 8px;font-size:16px}
.kopru{margin:14px 0 4px;color:var(--ink-2);font-size:13.5px}
a.git{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;margin-left:7px;border-radius:50%;
  background:var(--coral-tint);color:var(--coral-deep);font-weight:700;font-size:12px;line-height:1;text-decoration:none;vertical-align:1px}
a.git:hover,a.git:focus-visible{background:var(--coral-deep);color:#fff;text-decoration:none}
a.git:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
/* soru tablolarinda metrikler ortali */
.tw.sorular td.n,.tw.sorular th.n,.tw.sorusut td:last-child,.tw.sorusut th:last-child{text-align:center;vertical-align:middle}
.tw.sorular td{vertical-align:middle}
/* grup etiketleri */
.etk{display:inline-block;padding:2px 9px;border-radius:11px;font-size:11.5px;font-weight:620;white-space:nowrap;line-height:1.5}
.e1{background:#DCEFEA;color:#10332F}.e2{background:#FFE3D8;color:#B6431F}.e3{background:#FCEBC7;color:#7A5000}.e4{background:#DCE8F7;color:#1F4E8C}
.e5{background:#ECE3F5;color:#5B3A87}.e6{background:#DFF0DD;color:#2E6B2E}.e7{background:#F8DDE6;color:#8C2950}.e8{background:#E8E6E1;color:#4A4A4A}
:root[data-theme="dark"] .e1{background:#1E3B36;color:#A9DCD1}:root[data-theme="dark"] .e2{background:#4A2A1F;color:#FFB99E}:root[data-theme="dark"] .e3{background:#45381C;color:#F5D08A}
:root[data-theme="dark"] .e4{background:#1F3048;color:#A9C6EE}:root[data-theme="dark"] .e5{background:#33284A;color:#CDB6EC}:root[data-theme="dark"] .e6{background:#21391F;color:#B2DCAA}
:root[data-theme="dark"] .e7{background:#47222F;color:#F2AFC5}:root[data-theme="dark"] .e8{background:#2E2D2A;color:#D3D0C9}
/* vurgu */
b.vk{font-weight:700;color:var(--ink)}
tr.vsat td{background:color-mix(in srgb,var(--coral-tint) 55%,transparent)}
tr.vsat td:first-child{font-weight:650}
/* ara tablo basliklari ve urun tablolari */
p.tbas{margin:30px 0 8px;font-size:14.5px}
.fnote p.fac{margin:0 0 8px;color:var(--muted);font-size:12.8px;line-height:1.5}
/* cok sutunlu tablolar: tablo kapsayiciyi doldurur, genislik icerikten gelir; kaydirma yalniz icerik sigmadiginda olusur */
.tw.cok table{min-width:100%}
.tw.cok td,.tw.cok th{min-width:84px}
.tw.cok td:first-child,.tw.cok th:first-child{min-width:120px}
.tw.cok td{vertical-align:middle}
.tw.kompakt th,.tw.kompakt td{min-width:0;padding-left:9px;padding-right:9px}
.tw.urunt table{min-width:100%}
.tw.urunt td:first-child,.tw.urunt th:first-child{min-width:220px;white-space:normal}
h3[id]{scroll-margin-top:calc(var(--apph, 64px) + 24px)}
.ekranlar{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:12px 0 14px}
.ekranlar figure{margin:0;position:relative;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px}
.ekranlar img{width:100%;height:auto;display:block;border-radius:6px;border:1px solid var(--line)}
.ekranlar figcaption{font-size:12.5px;line-height:1.45;color:var(--ink-2);margin-top:7px}
.ekranlar .eno{position:absolute;top:14px;left:14px;width:24px;height:24px;border-radius:50%;background:var(--coral-deep);color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center}
.ekranlar img{cursor:zoom-in}
.ekranlar figure.acik{grid-column:1/-1}
.ekranlar figure.acik img{cursor:zoom-out}
@media(max-width:720px){.ekranlar{grid-template-columns:1fr}}
.tw.genis table{min-width:1460px}
.tw.genis td:first-child{white-space:nowrap}
"""
# ---------------------------------------------------------------- icindekiler
KISA = {"ek": ("Sözlük, Kaynakça, Yöntem", "Glossary, References, Method"), "yapayzeka": ("Yapay Zeka Özellikleri ve Tık", "AI Features and Clicks"), "ga4": ("GA4 - Site ve E-Ticaret", "GA4 - Site and E-Commerce"), "yolculuk": ("Satın Alma Yolculuğu", "Purchase Journey"), "yorum": ("Yorumlar ve Soru-Cevap", "Reviews and Q&A"), "ihtiyac": ("İhtiyaç Dili", "Need Language"), "youtube": ("YouTube: Montaj ve Tamir", "YouTube: Installation and Repair"), "rakip": ("Rakip Görünürlüğü ve Ölçek", "Competitor Visibility and Scale"),
        "model": ("Kanal Rolleri ve Model", "Channel Roles and Model"), "panel": ("Resmi Mağaza Paneli", "Official Store Panel"), "makro": ("Ekonomik Ortam", "Economic Environment"), "talep": ("Kategori Talebi", "Category Demand"), "organik": ("GSC - Organik Kanal", "GSC - Organic Channel"),
        "marka": ("Marka Aramaları", "Brand Searches"), "ssgbm": ("SSG ve BM Derin Talep", "SSG and BM In Depth"), "katalog": ("Katalog ve Talep", "Catalogue and Demand"), "yeni": ("Yeni Kategori ve Segment", "New Categories and Segments"), "set": ("Set ve Ürün + Hizmet", "Sets and Product + Service"), "benchmark": ("Benchmark ve Dijital Deneyim", "Benchmark and Digital Experience"), "serp": ("Google SERP ve AI Overview", "Google SERP and AI Overview"), "trafik": ("Marka Sitelerinde Trafik", "Traffic on Brand Sites"), "pazaryeri": ("Pazaryeri ve Çok Satanlar", "Marketplaces and Best Sellers"), "politika": ("Kanal Politikaları", "Channel Policies"), "sikayet": ("Şikayetvar: Satış Sonrası", "Şikayetvar: After-Sales"), "fiyat": ("Fiyat ve Satıcı Manzarası", "Price and Seller Landscape"), "derin": ("Alt Kategori Derinliği", "Sub-Category Depth"), "geo": ("AI Arama ve GEO Fırsatları", "AI Search and GEO Opportunities")}
KUMELER = [("DURUM", "STATUS", ["ozet", "makro"]), ("TALEP", "DEMAND", ["talep", "ssgbm", "ihtiyac", "organik", "yapayzeka", "ga4", "marka", "serp", "youtube", "sikayet"]), ("FIRSAT", "OPPORTUNITY", ["katalog", "yeni", "set"]), ("REKABET VE MODEL", "COMPETITION AND MODEL", ["rakip", "trafik", "pazaryeri", "derin", "panel", "yorum", "fiyat", "politika", "yolculuk", "benchmark", "model"]),
           ("PLAN", "PLAN", ["geo", "adimlar"]), ("EK", "APPENDIX", ["ek"])]
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
    return ('<a class="dl %s" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,%s" download="%s" title="Veri dosyasını indir · %d sekme · %s KB">%s<span class="lb">%s</span> </a>'
            % (sinif, b64, os.path.basename(XLS), sekme, kb, IKON, x("Veri dosyası", "Data file")))

# ---------------------------------------------------------------- alt sayfa baglantisi (ust bar, dil dugmesinin solu)
from alt_veri import SETLER as _SETLER
def _altlink(f, tr, en, ikon, sinif="altlink"):
    return ('<a class="%s" href="%s" target="_blank" rel="noopener" title="%s">'
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>'
            '<span class="lb">%s</span></a>') % (sinif, f, x("%s sayfasını yeni sekmede aç" % tr, "Open the %s page in a new tab" % en), ikon, x(tr, en))
ALTLINK = ('<div class="altset">%s</div><div class="altmenu"><button class="altlink" type="button" id="altmenu-b" aria-expanded="false" aria-controls="altmenu-p" title="%s">'
           '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/><path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/></svg>'
           '<span class="lb">%s</span></button><div class="altmenu__p" id="altmenu-p" hidden>%s</div></div>') % (
    "".join(_altlink(*s_) for s_ in _SETLER), x("Veri setlerini göster", "Show the data sets"), x("Veri setleri", "Data sets"),
    "".join(_altlink(*s_, sinif="altm") for s_ in _SETLER))

# ---------------------------------------------------------------- hero
HERO = """<div class="hero dark"><div class="ring"></div>
  <p class="eyebrow">%s</p>
  <h1>%s</h1>
</div>""" % (x("VitrA TÜRKİYE · E-TİCARET BÜYÜME FIRSATLARI", "VitrA TURKEY · E-COMMERCE GROWTH OPPORTUNITIES"),
             x("E-Ticaret Büyüme Fırsatları: Talep, Kullanıcı Davranışı ve Kanal Modeli", "E-Commerce Growth Opportunities: Demand, User Behaviour and Channel Model"))

DOC = """<!doctype html>
<html lang="tr" data-theme="light"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VitrA Türkiye | E-Ticaret Büyüme Fırsatları</title>
<style>%s
%s</style></head>
<body>
<header class="appbar"><div class="in">
  <div class="brandbit">
    <span class="logo-card"><img src="%s" alt="VitrA"></span></div>
  <div class="brandbit" style="gap:12px">%s%s%s
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
</body></html>""" % (CSS + CSS_EK + KAYNAKCA_CSS + CSS_SON + logo_css(), target_css, VITRA, ALTLINK, TEMA, dl_buton(), INBOUND, x("İçindekiler", "Contents"), toc, HERO, govde,
                     dl_buton("dl-foot"), x("Hacimler Google Keyword Planner &middot; sayfa ve sorgu verisi Google Search Console &middot; rakip ölçümü Ahrefs &middot; makro seriler TCMB EVDS &middot; autocomplete ve YouTube Google",
                                            "Volumes Google Keyword Planner &middot; page and query data Google Search Console &middot; competitor measurement Ahrefs &middot; macro series CBRT EVDS &middot; autocomplete and YouTube Google"),
                     x("İçindekiler menüsünü aç", "Open the contents menu"), x("İçindekiler", "Contents"), toc, JS)
x("VitrA Türkiye | E-Ticaret Büyüme Fırsatları", "VitrA Turkey | E-Commerce Growth Opportunities"); x("html", "html")
x("Açık ve koyu tema arasında geçiş yap", "Switch between light and dark theme"); x("Tema değiştir", "Switch theme"); x("Erişim", "Accessed")
ceviri.EN.update(t2_ortak.EK)
if t2_ortak._CAKISMA: print("uyarı · farklı çeviri:", t2_ortak._CAKISMA)
dil.TERIMLER = {t: (GLOSSARY[t], GL_TERM_EN.get(t, t), GL_EN[t]) for t in GLOSSARY}
# metrik adları rapor genelinde İngilizce (session, impression, click, revenue ...): Türkçe metin ve çeviri sözlüğü aynı dönüşümden geçer
import metrik_ad
DOC = metrik_ad.html_donustur(DOC)
_en2, _mc = metrik_ad.sozluk_donustur(ceviri.EN); ceviri.EN.clear(); ceviri.EN.update({k: metrik_ad.para_en(v) for k, v in _en2.items()})
_bs2, _ = metrik_ad.sozluk_donustur(t2_ortak.BOSLUK); t2_ortak.BOSLUK.clear(); t2_ortak.BOSLUK.update(_bs2)
dil.TERIMLER = {metrik_ad.donustur(t): (metrik_ad.donustur(v[0]), v[1], v[2]) for t, v in dil.TERIMLER.items()}
if _mc: print("uyarı · metrik adı dönüşümünde farklı çeviri:", len(_mc), _mc[:5])
DOC, _n, _de = dil.uygula(DOC, "VitrA Turkey | E-Commerce Growth Opportunities")
yol = os.path.join(veri.KOK, AD + ".html")
DOC, _ekd = ortak.yuzde_ek_duzelt(DOC)   # %X,Y'ek: ek, okunan son sayiya gore
if ortak.KARO_EKSIK:   # her karo açıklama balonu taşımalıdır (karo_aciklama.py)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "karo_eksik.txt"), "w", encoding="utf-8").write("\n".join(sorted(set(ortak.KARO_EKSIK))))
    raise SystemExit("açıklaması olmayan karo: %d (uretim/karo_eksik.txt)" % len(set(ortak.KARO_EKSIK)))
DOC = DOC.replace("\u2013", "-")   # urun adlarindaki en dash
print("yüzde eki düzeltmesi:", _ekd)
open(yol, "w", encoding="utf-8").write(DOC)
if _eksik_h3: print("uyarı · açıklaması olmayan alt başlık:", _eksik_h3)
print("kaydedildi:", yol, len(DOC), "karakter,", len(BOLUMLER), "bölüm,", _n, "ifade çevrildi")

# ---------------------------------------------------------------- alt sayfalar: genis veri setleri
import alt_veri
alt_veri.main(ceviri.EN)
