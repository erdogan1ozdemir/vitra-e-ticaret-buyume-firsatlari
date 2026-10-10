# -*- coding: utf-8 -*-
"""Bolum: AI aramada gorunurluk (GEO) - AI Overview odakli icerik plani, entity tutarliligi, site disi sinyaller, AI alisveris."""
from ortak import *
from rapor_parca1 import T
from grafik2 import gruplu
import serp_ozet as _SO
import b_seomonitor as _BS
import csv as _csv, os as _os, json as _json
_DE = _json.load(open(_os.path.join(veri.V, "ham", "geo", "destek_envanter.json"), encoding="utf-8"))
_DS = _DE["sayfalar"]; _DSN = len(_DS); _DSQ = sum(p_["soru"] for p_ in _DS); _DSB = [p_ for p_ in _DS if p_["bozuk_title"]]
_DSE = sum(_DE["eski_domain_gosterim"].values())

_D = _os.path.join(veri.V, "ham", "geo")
_IL0 = [(s_, int(c), int(i), float(p_)) for s_, c, i, p_ in _csv.reader(open(_os.path.join(_D, "gsc_ilham.tsv"), encoding="utf-8"), delimiter="\t")]
_ILB = {}
for s_, c, i, p_ in _IL0:   # ayni yazinin eski adresi (-old) tek sayfa sayilir
    k_ = s_[:-4] if s_.endswith("-old") else s_
    a_ = _ILB.setdefault(k_, [0, 0, 0.0]); a_[2] = (a_[2] * a_[1] + p_ * i) / (a_[1] + i) if (a_[1] + i) else p_; a_[0] += c; a_[1] += i
IL = [(k_, v_[0], v_[1], v_[2]) for k_, v_ in _ILB.items()]
SO = [(q, int(c), int(i), float(p_)) for q, c, i, p_ in _csv.reader(open(_os.path.join(_D, "gsc_soru.tsv"), encoding="utf-8"), delimiter="\t")]
SOD = {q: (c, i, p_) for q, c, i, p_ in SO}
_SK = {r["kelime"]: r for r in _json.load(open(_os.path.join(veri.V, "ham/derin/serp/kelime_sonuc.json"), encoding="utf-8"))}   # ilk gozlem (genisletilmis sette olmayan soru ornekleri icin)
_SK.update({r["kelime"]: r for r in _SO.TUM})   # genisletilmis gozlem
_TRH = ".".join(reversed(_SO.TARIH.split("-")))
ILHAM = "https://www.vitra.com.tr/ilham-veren-fikirler/"

# ---------------------------------------------------------------- rehber icerik gruplari
from rehber_grup import GRUP, GAD, grup
GS = {g: [0, 0, 0, None] for g, _, _ in GRUP}   # sayfa, tik, gosterim, en iyi sayfa
for s_, c, i, p_ in IL:
    g = GS[grup(s_)]; g[0] += 1; g[1] += c; g[2] += i
    if g[3] is None or c > g[3][1]: g[3] = (s_, c)
TOP_T = sum(g[1] for g in GS.values()); TOP_N = sum(g[0] for g in GS.values())
PRAT = ("tamir", "montaj")
prat_t = 100 * sum(GS[g][1] for g in PRAT) / TOP_T; prat_n = 100 * sum(GS[g][0] for g in PRAT) / TOP_N
TAMIR_N = sum(1 for s_, *_ in IL if "tamir" in s_)
def _baslik(s_):
    t = s_.split("/")[-1].replace("-", " ")
    return t[:1].upper() + t[1:]
x("Sayfa sayısı payı", "Share of pages"); x("Tık payı", "Click share")
GR = gruplu([(x(b, c), [100 * GS[a][0] / TOP_N, 100 * GS[a][1] / TOP_T]) for a, b, c in GRUP],
            [(x("Sayfa sayısı payı", "Share of pages"), "#9AA8A5"), (x("Tık payı", "Click share"), "#10332F")],
            x("Rehber içerik gruplarının sayfa sayısı ve organik tık payı · /ilham-veren-fikirler/, 1 Eki 2025 - 30 Eyl 2026", "Share of pages and organic clicks by guide content group · /ilham-veren-fikirler/, 1 Oct 2025 - 30 Sep 2026"))
T_GR = tablo([th("İçerik grubu", "Content group", "Sayfa adresindeki konuya göre yapılan gruplama.", "Grouping by the topic in the page address."),
              th("Sayfa", "Pages", "Dönemde en az 5 tık alan sayfa sayısı.", "Number of pages with at least 5 clicks in the period.", True),
              th("Click", "Clicks", "1 Eki 2025 - 30 Eyl 2026 organik click.", "Organic clicks, 1 Oct 2025 - 30 Sep 2026.", True),
              th("Click payı", "Click share", "Rehber içeriklerin toplam click'i içindeki pay.", "Share of the total clicks of guide content.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("En çok click alan sayfa", "Page with most clicks", "Grubun en çok click alan sayfası; bağlantı web sitesindeki sayfayı açar.", "The group's page with the most clicks; the link opens the page on the website.")],
             [[x(b, c), cell(GS[a][0]), cellk(GS[a][1]), n(yzd(100 * GS[a][1] / TOP_T)), cellk(GS[a][2]), n(yzd(100 * GS[a][1] / GS[a][2])), u(ILHAM + GS[a][3][0] + ("" if GS[a][3][0].endswith("rehberi") else "/"), _baslik(GS[a][3][0])) + " (%s)" % bin(GS[a][3][1])] for a, b, c in GRUP])

# ---------------------------------------------------------------- soru sorgulari
so_i = sum(i for _, _, i, _ in SO); so_c = sum(c for _, c, _, _ in SO)
so_p = sum(p_ * i for _, _, i, p_ in SO) / so_i
T_SO = tablo([th("Sorgu", "Query", "Search Console'da vitra.com.tr'nin gösterim aldığı soru biçimli sorgu; \"nasıl\" ve \"su kaçır\" içeren sorgulardan gösterime göre seçilmiştir.", "Question-type query for which vitra.com.tr received impressions; selected by impressions from queries containing \"nasıl\" (how) and \"su kaçır\" (leaking)."),
              th("Gösterim", "Impressions", "1 Eki 2025 - 30 Eyl 2026 gösterim.", "Impressions, 1 Oct 2025 - 30 Sep 2026.", True),
              th("Click", "Clicks", "Aynı dönemde click.", "Clicks in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("Ort. sıra", "Avg. position", "Gösterim ağırlıklı ortalama sıra, tüm cihazlar.", "Impression-weighted average position, all devices.", True)],
             [[kw(q), cellk(i), cell(c), n(yzd(100 * c / i, 2)), n(("%.1f" % p_).replace(".", ","))] for q, c, i, p_ in sorted(SO, key=lambda r: -r[2])], "uzun")
KAPAK = ["klozet kapağı nasıl takılır", "amortisörlü klozet kapağı nasıl takılır", "üstten vidalı klozet kapağı nasıl takılır", "eski tip klozet kapağı nasıl takılır", "yavaş kapanan klozet kapağı nasıl takılır", "klozet kapağı nasıl değiştirilir"]
kap_i = sum(SOD[q][1] for q in KAPAK); kap_c = sum(SOD[q][0] for q in KAPAK)

# ---------------------------------------------------------------- AI Overview odakli icerik plani
def _aio(k_):
    r = _SK.get(k_) or {}; a = r.get("ai") or {}
    d = []
    for z in a.get("ref_alanlar") or []:
        if z not in d: d.append(z)
    return d
def _ref(k_, n_=4):
    d = _aio(k_)
    return ", ".join(veri_m(z) for z in d[:n_])
def soru(*qs):
    return '<div class="kwlist">%s</div>' % "".join('<span class="kw">%s</span>' % veri_m(q) for q in qs)
OC = {"Öncelik 1": "b-o1", "Öncelik 2": "b-o2", "Öncelik 3": "b-o3"}; OE = {"Öncelik 1": "Priority 1", "Öncelik 2": "Priority 2", "Öncelik 3": "Priority 3"}
def ob(o): return '<span class="badge %s">%s</span>' % (OC[o], x(o, OE[o]))
gk = SOD["gömme klozet su kaçırıyorsa çok basit tamiri"]; gt = next(r for r in IL if r[0] == "gomme-rezervuar-tamiri")
dt = next(r for r in IL if r[0] == "dusakabin-temizligi-nasil-yapilir"); bn = next(r for r in IL if r[0] == "bide-nedir")
PLAN = [
 ("Öncelik 1", ("Gömme rezervuar ve iç takım arızaları: su kaçırma, su doldurmama, iç takım, şamandıra ve kumanda paneli değişimi", "Concealed cistern and inner mechanism faults: leaking, not filling, replacing the inner mechanism, float valve and flush plate"),
  ("Destek sayfası; model ve rezervuar tipine göre alt başlıklar", "Support page; sub-headings by model and cistern type"),
  soru("Gömme rezervuar neden su doldurmaz?", "Klozet iç takım değişimi ne kadar?", "basmalı rezervuar iç takımı nasıl takılır"),
  ("\"gömme klozet su kaçırıyorsa çok basit tamiri\" %s gösterim, CTR %s; sitedeki tek tamir yazısı %s tık, %s gösterim; \"gömme rezervuar iç takımı\" AI Overview'unda kaynaklar %s, VitrA yok" % (k(gk[1]), yzd(100 * gk[0] / gk[1]), bin(gt[1]), k(gt[2]), _ref("gömme rezervuar iç takımı")),
   "\"gömme klozet su kaçırıyorsa çok basit tamiri\" %s impressions, CTR %s; the site's only repair article %s clicks, %s impressions; in the \"gömme rezervuar iç takımı\" AI Overview the sources are %s, not VitrA" % (k(gk[1]).replace(",", "."), ("%.1f" % (100 * gk[0] / gk[1])) + "%", f"{gt[1]:,}", k(gt[2]).replace(",", "."), _ref("gömme rezervuar iç takımı"))), ("D33", "D19")),
 ("Öncelik 1", ("Klozet kapağı montajı ve uyumluluk: kapak tipine göre montaj, hangi kapak hangi klozete uyar", "WC seat fitting and compatibility: fitting by seat type, which seat fits which WC"),
  ("Destek sayfası; ürün sayfalarında klozet koduna göre uyumlu kapak tablosu", "Support page; a compatible-seat table by WC code on product pages"),
  soru("Klozet kapakları her klozete uyar mı?", "amortisörlü klozet kapağı nasıl takılır", "eski tip klozet kapağı nasıl takılır"),
  ("Kapak montajı soran 6 sorgu toplam %s gösterim, %s tık (CTR %s); ortalama sıra 4,8-5,9" % (k(kap_i), bin(kap_c), yzd(100 * kap_c / kap_i, 2)),
   "6 queries about seat fitting total %s impressions and %s clicks (CTR %s); average position 4.8-5.9" % (k(kap_i).replace(",", "."), f"{kap_c:,}", ("%.2f" % (100 * kap_c / kap_i)) + "%")), ("D33",)),
 ("Öncelik 1", ("Batarya bakımı ve parça değişimi: conta, kartuş, kireç, damlatma ve montaj", "Tap maintenance and part replacement: seals, cartridges, limescale, dripping and fitting"),
  ("Destek sayfası; armatür ürün sayfalarından bağlantı", "Support page; linked from tap product pages"),
  soru("banyo batarya contası nasıl değiştirilir", "tezgah üstü musluk nasıl takılır", "lavabo bataryası nasıl takılır"),
  ("Conta değişimi %s, tezgah üstü musluk montajı %s gösterim; YouTube'da batarya ve kartuş konuları 7,0M izlenme ve VitrA kanal videosu yok" % (k(SOD["banyo batarya contası nasıl değiştirilir"][1]), k(SOD["tezgah üstü musluk nasıl takılır"][1])),
   "Seal replacement %s, countertop tap fitting %s impressions; on YouTube tap and cartridge topics have 7.0M views and no VitrA channel video" % (k(SOD["banyo batarya contası nasıl değiştirilir"][1]).replace(",", "."), k(SOD["tezgah üstü musluk nasıl takılır"][1]).replace(",", "."))), ("D33", "D20")),
 ("Öncelik 1", ("Ölçü ve yerleşim: klozet, lavabo, banyo dolabı ve duşakabin ölçüleri, montaj yükseklikleri", "Sizes and layout: WC, washbasin, bathroom cabinet and shower enclosure sizes, fitting heights"),
  ("Rehber yazı; kategori sayfalarında kısa soru-cevap", "Guide article; short Q&A on category pages"),
  soru("Klozet ölçüleri standart mıdır?", "Banyo dolabı yüksekliği kaç santim olmalı?", "60 cm banyo dolabı ölçüleri nelerdir?"),
  ("\"klozet ölçüleri\" AI Overview'unda VitrA kaynak gösterilmektedir; \"80 cm banyo dolabı\" AI Overview'unda kaynaklar %s, VitrA yok" % _ref("80 cm banyo dolabı"),
   "VitrA is cited in the \"klozet ölçüleri\" AI Overview; in the \"80 cm banyo dolabı\" AI Overview the sources are %s, not VitrA" % _ref("80 cm banyo dolabı")), ("D19",)),
 ("Öncelik 1", ("Seçim karşılaştırmaları: gömme mi dış rezervuar mı, kanallı mı kanalsız mı, suya dayanıklı dolap malzemesi", "Selection comparisons: concealed or exposed cistern, rim or rimless, water-resistant cabinet materials"),
  ("Rehber yazı; karşılaştırma tablosuyla", "Guide article with a comparison table"),
  soru("Gömme rezervuar iyi mi?", "Kanalsız klozet kullanışlı mı?", "MDF banyo dolabı suya dayanıklı mı?"),
  ("\"80 cm banyo dolabı\" AI Overview'unda kaynaklar %s, VitrA yok; \"suya dayanıklı banyo dolabı\" AI Overview'unda VitrA kaynak gösterilmektedir" % _ref("80 cm banyo dolabı"),
   "In the \"80 cm banyo dolabı\" AI Overview the sources are %s, not VitrA; VitrA is cited in the \"suya dayanıklı banyo dolabı\" AI Overview" % _ref("80 cm banyo dolabı")), ("D19",)),
 ("Öncelik 1", ("Marka soruları: VitrA ve Artema ilişkisi, menşei, kalite ve garanti", "Brand questions: the VitrA-Artema relationship, origin, quality and warranty"),
  ("Kurumsal soru-cevap sayfası; Wikidata ve Wikipedia güncellemeleriyle birlikte", "Corporate Q&A page, together with Wikidata and Wikipedia updates"),
  soru("VitrA ve Artema aynı marka mı?", "Artema hangi ülkenin markası?", "VitrA iyi marka mı?"),
  ("Bu sorular PAA kutusunda çıkmaktadır; Artema'nın Wikidata ve Wikipedia kaydı bulunmamaktadır", "These questions appear in the PAA box; Artema has no Wikidata or Wikipedia record"), ("D19", "D34")),
 ("Öncelik 1", ("Yedek parça, garanti ve servis: parça bulma, garanti süresi, servis ücreti ve başvuru adımları", "Spare parts, warranty and service: finding parts, warranty period, service fee and application steps"),
  ("Destek sayfası; ürün sayfalarından ve yedek parça kategorisinden bağlantı", "Support page; linked from product pages and the spare-parts category"),
  soru("vitra servis", "vitra yedek parça", "Klozet şamandıra bozuk olursa ne olur?"),
  ("Şikayetvar'da servis ve garanti teması %54,7, yedek parça teması %17,8 (Nis - Eyl 2026); ürün sayfalarında garanti süresi bulunmamaktadır", "On Şikayetvar the service and warranty theme is 54.7% and the spare-part theme 17.8% (Apr - Sep 2026); product pages show no warranty period"), ("D24", "D13")),
 ("Öncelik 2", ("Montaj ücreti ve işçilik: ürün bazında montaj kapsamı ve fiyatı", "Installation fee and labour: installation scope and price by product"),
  ("Montaj hizmeti sayfasında soru-cevap bölümü", "A Q&A section on the installation service page"),
  soru("Gömme rezervuar montaj ücreti ne kadar?", "komple banyo yenileme fiyatları ne kadar?", "Bir banyo tadilatı ne kadara mal olur?"),
  ("\"klozet montaj ücreti\" AI Overview'unda kaynaklar %s; VitrA'da 11 fiyatlı montaj kalemi bulunmaktadır" % _ref("klozet montaj ücreti"),
   "In the \"klozet montaj ücreti\" AI Overview the sources are %s; VitrA has 11 priced installation items" % _ref("klozet montaj ücreti")), ("D19", "D13")),
 ("Öncelik 2", ("Temizlik ve bakım: duşakabin, klozet ve batarya temizliği, kireç", "Cleaning and care: shower enclosure, WC and tap cleaning, limescale"),
  ("Mevcut yazıların soru-cevap bölümüyle güncellenmesi; ürün sayfalarına bakım bağlantısı", "Updating the existing articles with a Q&A section; care links on product pages"),
  soru("duşakabin kireci nasıl temizlenir", "Tepe duş başlığı kireci nasıl temizlenir?", "duşakabin camı nasıl temizlenir"),
  ("Duşakabin temizliği yazısı %s tık ile ikinci en çok tık alan rehber içeriktir; \"duşakabin kireci nasıl temizlenir\" %s gösterim, sıra %s" % (bin(dt[1]), k(SOD["duşakabin kireci nasıl temizlenir"][1]), ("%.1f" % SOD["duşakabin kireci nasıl temizlenir"][2]).replace(".", ",")),
   "The shower enclosure cleaning article is the second most-clicked guide with %s clicks; \"duşakabin kireci nasıl temizlenir\" %s impressions, position %s" % (f"{dt[1]:,}", k(SOD["duşakabin kireci nasıl temizlenir"][1]).replace(",", "."), "%.1f" % SOD["duşakabin kireci nasıl temizlenir"][2])), ("D33",)),
 ("Öncelik 2", ("Erişilebilir ve çocuk banyosu: engelli klozeti ölçüleri, tutunma barları, çocuk klozeti", "Accessible and children's bathrooms: accessible WC dimensions, grab bars, children's WCs"),
  ("Rehber yazı; erişilebilir banyo kategori sayfasıyla birlikte", "Guide article together with an accessible bathroom category page"),
  soru("Engelli tuvaleti nasıl olmalı?", "Engelli tutunma barının yerden yüksekliği ne kadar olmalıdır?", "2026 engelli wc yönetmeliği nedir?"),
  ("\"engelli klozet\" aramasında VitrA 9. sıradadır; Google'ın soru kutusunda engelli tuvaleti ölçüsü ve yönetmeliği sorulmaktadır", "VitrA ranks 9th for \"engelli klozet\"; Google's question box asks about accessible toilet dimensions and regulations"), ("D19",)),
 ("Öncelik 2", ("Alt kategori açılımı: sayfası olmayan ya da farklı adla duran kesitler", "Sub-category expansion: segments with no page or a different name"),
  ("Kategori sayfası ve kısa soru-cevap", "Category page with a short Q&A"),
  soru("sıva üstü banyo bataryası", "fotoselli batarya", "jakuzi", "ayaklı lavabo"),
  ("Pazaryerlerinde ayrı kategori olarak aranan bu kesitlerin vitra.com.tr'de karşılık gelen sayfası bulunmamakta ya da farklı adla durmaktadır", "These segments, searched as separate categories on marketplaces, have no matching page on vitra.com.tr or sit under a different name"), ("D29", "D30")),
 ("Öncelik 3", ("Ürün tanımları ve bitişik ürünler: \"nedir\" yazılarının güncellenmesi, havlupan ve ısıtmalı kapak rehberleri", "Product definitions and adjacent products: updating \"what is\" articles, towel radiator and heated seat guides"),
  ("Mevcut yazıların güncellenmesi; yeni rehber yazı", "Updating existing articles; new guide articles"),
  soru("Pisuvar nedir?", "Şamandıra suyu neden kesmez?", "Elektrikli havlupan banyoyu ısıtır mı?"),
  ("Bide nedir yazısı %s tık; \"pisuvar\" AI Overview'unda VitrA kaynak gösterilmektedir; \"şamandıra\" ve \"elektrikli havlupan\" AI Overview'larında VitrA yok" % bin(bn[1]),
   "The \"what is a bidet\" article %s clicks; VitrA is cited in the \"pisuvar\" AI Overview; not in the \"şamandıra\" and \"elektrikli havlupan\" AI Overviews" % f"{bn[1]:,}"), ("D33", "D19")),
]

# ---------------------------------------------------------------- entity
ENT = [
 (u("https://www.wikidata.org/wiki/Q7937213", "Wikidata · Q7937213"),
  ("Wikipedia maddelerine bağlı ana kayıt; resmi web sitesi alanında vitra.com.tr yerine ilgisiz bir alan adı kayıtlı; kuruluş yılı 1942; Instagram, YouTube, LinkedIn ve Facebook alanları boş; X hesabı iki yazımla", "The main record linked to the Wikipedia articles; the official website field holds an unrelated domain instead of vitra.com.tr; founding year 1942; Instagram, YouTube, LinkedIn and Facebook fields empty; the X account in two spellings"),
  ("Resmi web sitesinin vitra.com.tr olarak düzeltilmesi; sosyal hesap alanlarının eklenmesi; ürün grubu, üst kuruluş ve Artema ilişkisinin kaynakla girilmesi", "Correcting the official website to vitra.com.tr; adding the social account fields; entering the product group, parent organisation and Artema relationship with sources")),
 (u("https://www.wikidata.org/wiki/Q127325081", "Wikidata · Q127325081"),
  ("Aynı şirket için ikinci kayıt; web sitesi vitra.com.tr; Wikipedia bağlantısı yok", "A second record for the same company; website vitra.com.tr; no Wikipedia link"),
  ("İki kaydın tek kayıtta birleştirilmesi", "Merging the two records into one")),
 (u("https://tr.wikipedia.org/wiki/VitrA", "Wikipedia TR · VitrA"),
  ("Kısa madde (2.031 bayt); son düzenleme 17.12.2025; ürün grupları, Artema ve güncel üretim bilgisi yer almıyor", "A short article (2,031 bytes); last edited 17.12.2025; product groups, Artema and current production information are missing"),
  ("Bağımsız yayınlara dayanan genişletme: ürün grupları, üretim, Artema ilişkisi, tasarım ödülleri", "An expansion based on independent publications: product groups, production, the Artema relationship, design awards")),
 (u("https://en.wikipedia.org/wiki/VitrA_(sanitaryware)", "Wikipedia EN · VitrA (sanitaryware)"),
  ("6.619 bayt; son düzenleme 31.08.2026", "6,619 bytes; last edited 31.08.2026"),
  ("Ürün gamı ve Artema bilgisinin güncel tutulması", "Keeping the product range and Artema information current")),
 (x("Artema", "Artema"),
  ("Wikidata ve Wikipedia'da kayıt bulunmuyor; \"Artema hangi ülkenin markası?\" ve \"VitrA ve Artema aynı marka mı?\" soruları PAA kutusunda çıkıyor", "No Wikidata or Wikipedia record; the questions \"which country is Artema from?\" and \"are VitrA and Artema the same brand?\" appear in the PAA box"),
  ("Wikidata kaydının açılması (üst kuruluş, web sitesi, ürün grubu); VitrA maddesinde Artema bölümü; sitede marka ilişkisini anlatan sayfa", "Opening a Wikidata record (parent organisation, website, product group); an Artema section in the VitrA article; a page on the site explaining the brand relationship")),
 (u("https://www.vitra.com.tr/llms.txt", "vitra.com.tr · llms.txt"),
  ("Kurumsal metin \"1958 yılında kurulan VitrA\" ifadesini kullanıyor; Wikipedia ve Wikidata 1942'yi gösteriyor", "The corporate text says \"VitrA, founded in 1958\"; Wikipedia and Wikidata show 1942"),
  ("Kuruluş tarihi için tek anlatının belirlenmesi ve tüm kayıtlarda aynı biçimde yer alması", "Settling a single founding narrative and using it consistently across all records")),
]

# ---------------------------------------------------------------- AI Overview kaynak siteleri (site disi)
YAYIN = sorted(((d_, _SO.AI_ALAN[d_]) for d_ in ("banyome.com", "instagram.com", "wikipedia.org", "yapilir.com", "youtube.com", "banyomega.com", "eksisozluk.com")), key=lambda t_: -t_[1])

_POPSO, _DIASO = pop("Soru sorguları: gösterim, tık ve sıra", "Question queries: impressions, clicks and position", T_SO, "21 sorguyu gör", "See the 21 queries")
# ---------------------------------------------------------------- yapay zeka yanitlarinda VitrA (ChatGPT, Gemini, AI Overview)
AIG = _json.load(open(_os.path.join(_D, "ai_gorunurluk.json"), encoding="utf-8"))
_PRV = [("chatgpt", "ChatGPT"), ("gemini", "Gemini"), ("google_ai_overview", "Google AI Overview")]
_RK = [("kale.com.tr", "Kale"), ("creavit.com.tr", "Creavit"), ("geberit.com.tr", "Geberit"), ("trendyol.com", "Trendyol"), ("hepsiburada.com", "Hepsiburada"), ("koctas.com.tr", "Koçtaş")]
def _po(a_, b_): return 100 * a_ / b_ if b_ else 0
AIV = {p_: _po(AIG["saglayici"][p_]["vitra"], AIG["saglayici"][p_]["markasiz_n"]) for p_, _ in _PRV}
T_AIG = tablo([th("Platform", "Platform", "Yanıtın alındığı yapay zeka platformu.", "The AI platform the answer was taken from."),
               th("Yanıt", "Answers", "4 Eyl - 3 Eki 2026 arasında marka adı geçmeyen 111 soruya alınan yanıt sayısı.", "Answers received to the 111 questions without a brand name, 4 Sep - 3 Oct 2026.", True),
               th("VitrA", "VitrA", "VitrA'nın adıyla geçtiği yanıtların payı.", "Share of answers that name VitrA.", True)]
              + [th(ad_, ad_, "%s adının geçtiği yanıtların payı (aynı yanıtlar)." % ad_, "Share of answers that name %s (same answers)." % ad_, True) for _, ad_ in _RK],
              [[x(a_, a_), cell(AIG["saglayici"][p_]["markasiz_n"]), n("<b>%s</b>" % yzd(AIV[p_]))] + [n(yzd(_po(AIG["saglayici"][p_]["rakip"][d_], AIG["saglayici"][p_]["markasiz_n"]))) for d_, _ in _RK] for p_, a_ in _PRV])
_KYN = AIG["kaynak"]
T_AIK = tablo([th("Alan adı", "Domain", "Yanıtta kaynak olarak bağlantı verilen alan adı; bağlantı siteyi açar.", "Domain linked as a source in the answer; the link opens the site."),
               th("Yanıt", "Answers", "Alan adının en az bir kez kaynak gösterildiği yanıt sayısı, markasız sorular, üç platform toplamı.", "Answers citing the domain at least once, questions without a brand name, all three platforms.", True),
               th("AI Overview", "AI Overview", "Google AI Overview yanıtlarında kaynak gösterildiği yanıt sayısı.", "Google AI Overview answers citing the domain.", True),
               th("ChatGPT", "ChatGPT", "ChatGPT yanıtlarında kaynak gösterildiği yanıt sayısı.", "ChatGPT answers citing the domain.", True),
               th("Gemini", "Gemini", "Gemini yanıtlarında kaynak gösterildiği yanıt sayısı.", "Gemini answers citing the domain.", True),
               th("Satın alma soruları", "Purchase questions", "\"Nereden alınır\", teslimat, iade ve montaj dahil satış gibi 14 markasız satın alma sorusunda (28.09 - 01.10.2026) kaynak gösterildiği yanıt sayısı.", "Answers citing the domain for 14 purchase questions without a brand name such as where to buy, delivery, returns and sales with installation (28.09 - 01.10.2026).", True)],
              [[u("https://" + r_[0], r_[0]), cell(r_[1]), cell(r_[2]), cell(r_[3]), cell(r_[4]), cell(r_[5])] for r_ in _KYN])
_PZ4 = sum(r_[1] for r_ in _KYN if r_[0] in ("trendyol.com", "koctas.com.tr", "hepsiburada.com", "akakce.com"))
_KD = {r_[0]: r_ for r_ in _KYN}
_KS = [dict(zip(AIG["klasor_sutun"], r_)) for r_ in AIG["klasor_soru"]]
def _oy(a_, b_): return "%d / %d" % (a_, b_)
def _kac(a_, b_): return "tamamında" if a_ == b_ else ek(a_, "inde")
T_AIS = tablo([th("Soru metni", "Question", "Yapay zeka platformlarına sorulan soru; kullanıcının yazdığı biçimde korunmuştur.", "The question asked to the AI platforms, kept as the user would type it."),
               th("Grup", "Group", "Satın alma ve teslimat soruları ile montaj soruları.", "Purchase and delivery questions and installation questions."),
               th("Markalı", "Branded", "Soruda VitrA adı geçiyor mu?", "Does the question name VitrA?"),
               th("VitrA adı geçen", "VitrA named", "VitrA'nın adıyla geçtiği yanıt / toplam yanıt (ChatGPT, Gemini ve AI Overview birlikte).", "Answers naming VitrA / total answers (ChatGPT, Gemini and AI Overview together).", True),
               th("vitra.com.tr kaynak", "vitra.com.tr cited", "vitra.com.tr'nin kaynak gösterildiği yanıt / toplam yanıt.", "Answers citing vitra.com.tr / total answers.", True),
               th("Pazaryeri kaynak", "Marketplace cited", "Trendyol, Hepsiburada, Koçtaş, n11, Amazon, Bauhaus, Akakçe veya Cimri'nin kaynak gösterildiği yanıt / toplam yanıt.", "Answers citing Trendyol, Hepsiburada, Koçtaş, n11, Amazon, Bauhaus, Akakçe or Cimri / total answers.", True)],
              [[kw(r_["soru"]), etk("Satın alma ve satış sonrası", "Purchase and after-sales", "ais-e") if r_["klasor"] == "e-ticaret" else etk("Montaj", "Installation", "ais-m"), x("Evet", "Yes") if r_["markali"] else x("Hayır", "No"),
                n(_oy(r_["vitra_adi"], r_["yanit"])), n(_oy(r_["vitra_kaynak"], r_["yanit"])), n(_oy(r_["pazaryeri_kaynak"], r_["yanit"]))]
               for r_ in sorted(_KS, key=lambda r_: (r_["klasor"] != "e-ticaret", r_["markali"], r_["vitra_adi"] / r_["yanit"]))], "uzun")
_Q = {r_["soru"]: r_ for r_ in _KS}
_q1 = _Q["vitra klozet trendyol mu hepsiburada mı daha uygun"]; _q2 = _Q["klozet nereden alınır en uygun fiyata"]
_q3 = _Q["banyo ürünlerinde iade ve değişim nasıl yapılır online alışverişte"]; _q4 = _Q["online alınan klozet nasıl teslim edilir kargo hasarı olur mu"]
_q5 = _Q["klozet montajı dahil satış yapan siteler"]; _q6 = _Q["banyo dolabı montajı"]
_DY = AIG["duygu"]

_soN = len(SO)
_SOR_SA = sum(1 for r_ in _KS if r_["klasor"] == "e-ticaret"); _SOR_MO = len(_KS) - _SOR_SA
T_VK = tablo([th("Veri seti", "Data set", "Bölümde kullanılan dört ölçüm; alt başlıklar bu sırayla ilerler.", "The four measurements used in the section; the sub-sections follow this order."),
              th("Örneklem", "Sample", "Ölçülen soru, kelime ya da sayfa seti.", "The set of questions, keywords or pages measured."),
              th("Ne ölçer?", "What does it measure?", "Veri setinin VitrA için gösterdiği şey.", "What the data set shows for VitrA."),
              th("Dönem", "Period", "Verinin alındığı tarih ya da dönem.", "The date or period of the data."),
              th("Ana sonuç", "Main result", "Setin VitrA için temel değeri.", "The set's headline value for VitrA.")],
             [[x("Yapay zeka yanıt takibi (ChatGPT, Gemini, Google AI Overview)", "AI answer tracking (ChatGPT, Gemini, Google AI Overview)"),
               x("%d soru (prompt): %d'i marka adı içermez, %d'ü VitrA adıyla sorulur; 11 konu klasörü" % (AIG["soru"], AIG["markasiz_soru"], AIG["markali_soru"]), "%d questions (prompts): %d without a brand name, %d naming VitrA; 11 topic folders" % (AIG["soru"], AIG["markasiz_soru"], AIG["markali_soru"])),
               x("Yanıtta hangi markaların adının geçtiği ve hangi sitelerin kaynak gösterildiği", "Which brands are named in the answer and which sites are cited"),
               x("4 Eyl - 3 Eki 2026, düzenli aralıklarla tekrarlı ölçüm", "4 Sep - 3 Oct 2026, repeated at regular intervals"),
               x("Markasız sorularda VitrA yanıtların %s (ChatGPT) ile %s (Gemini) arasında adıyla geçmektedir" % (yzd(AIV["chatgpt"]), yzd(AIV["gemini"])), "In questions without a brand name VitrA is named in %s (ChatGPT) to %s (Gemini) of answers" % (("%.1f" % AIV["chatgpt"]) + "%", ("%.1f" % AIV["gemini"]) + "%"))],
              [x("SEOmonitor takibi", "SEOmonitor tracking"),
               x("vitra.com.tr kampanyasında günlük takip edilen %s ana kelime, 8 kategori" % bin(_BS.TOP["n"]), "%s main keywords tracked daily in the vitra.com.tr campaign, 8 categories" % f"{_BS.TOP['n']:,}"),
               x("Google mobil sonucunda AI Overview çıkıp çıkmadığı ve vitra.com.tr'nin kaynak gösterilip gösterilmediği", "Whether an AI Overview appears in Google mobile results and whether vitra.com.tr is cited"),
               x("03.10.2026", "03.10.2026"),
               x("%s kelimede AI Overview çıkmakta, VitrA bunların %s kaynak gösterilmektedir" % (bin(_BS.TOP["aio"]), yzd(100 * _BS.TOP["vitra"] / _BS.TOP["aio"], 0) + "'" + ek(round(100 * _BS.TOP["vitra"] / _BS.TOP["aio"]), "inde").split("'")[1]), "An AI Overview appears for %s keywords and VitrA is cited in %s of them" % (f"{_BS.TOP['aio']:,}", ("%.0f" % (100 * _BS.TOP["vitra"] / _BS.TOP["aio"])) + "%"))],
              [x("Rapor hedef kelimeleri (Bölüm [[b:serp]])", "Report target keywords (Section [[b:serp]])"),
               x("Bu rapor için seçilen %d kelime: VitrA gamı %d, yakın kategoriler %d, marka ve karşılaştırma %d" % (_SO.NT, len(_SO.GRUP["A"]), len(_SO.GRUP["B"]), len(_SO.GRUP["C"])), "%d keywords selected for this report: VitrA range %d, adjacent categories %d, brand and comparison %d" % (_SO.NT, len(_SO.GRUP["A"]), len(_SO.GRUP["B"]), len(_SO.GRUP["C"]))),
               x("Google mobil sonucunda AI Overview çıkıp çıkmadığı ve kaynak gösterilen siteler", "Whether an AI Overview appears in Google mobile results and which sites are cited"),
               x("%s, aynı gün üç gözlem" % _TRH, "%s, three observations on the same day" % _TRH),
               x("VitrA gamında içeriği alınan %d AI Overview'un %s VitrA kaynak gösterilmektedir" % (_SO.ai_grup("A")["icerik"], ek(_SO.ai_grup("A")["vitra"], "inde")), "VitrA is cited in %d of the %d AI Overviews retrieved in the VitrA range" % (_SO.ai_grup("A")["vitra"], _SO.ai_grup("A")["icerik"]))],
              [x("Search Console (vitra.com.tr)", "Search Console (vitra.com.tr)"),
               x("Rehber sayfaları (/ilham-veren-fikirler/, en az 5 tık alan %d sayfa) ve \"nasıl\", \"su kaçır\" içeren %d soru biçimli arama" % (TOP_N, _soN), "Guide pages (/ilham-veren-fikirler/, %d pages with at least 5 clicks) and %d question-style searches containing \"nasıl\" (how) or \"su kaçır\" (leaking)" % (TOP_N, _soN)),
               x("Sitenin bu sayfalarda ve sorularda aldığı gösterim, tık ve ortalama sıra", "The impressions, clicks and average position the site gets on these pages and questions"),
               x("1 Eki 2025 - 30 Eyl 2026", "1 Oct 2025 - 30 Sep 2026"),
               x("Soru biçimli aramalarda ortalama sıra %s, CTR %s" % (("%.1f" % so_p).replace(".", ","), yzd(100 * so_c / so_i, 2)), "Average position %s and CTR %s on question-style searches" % ("%.1f" % so_p, ("%.2f" % (100 * so_c / so_i)) + "%"))]])
# rapor hedef kelimeleri: grup bazında AI Overview
import collections as _col
def sayi_ayni(t): x(t, t); return t   # alan adı listesi iki dilde aynıdır
def _hk_alan(L):
    c_ = _col.Counter(d_ for r_ in L if r_.get("ai") for d_ in set(r_["ai"].get("ref_alanlar") or []))
    return c_.most_common(4)
T_HK = tablo([th("Grup", "Group", "Bölüm [[b:serp]] kelime grubu.", "Keyword group of Section [[b:serp]]."),
              th("Kelime", "Keywords", "Gruptaki kelime sayısı.", "Number of keywords in the group.", True),
              th("AI Overview çıkan", "With AI Overview", "Google mobil sonucunda AI Overview görülen kelime sayısı.", "Keywords with an AI Overview in Google mobile results.", True),
              th("İçeriği alınan", "Content retrieved", "AI Overview metni ve kaynakları alınabilen kelime sayısı.", "Keywords whose AI Overview text and sources could be retrieved.", True),
              th("VitrA kaynak", "VitrA cited", "vitra.com.tr'nin kaynak gösterildiği AI Overview / içeriği alınan AI Overview.", "AI Overviews citing vitra.com.tr / AI Overviews retrieved.", True),
              th("En çok kaynak gösterilen alan adları", "Most cited domains", "Gruptaki AI Overview'larda en çok kaynak gösterilen dört alan adı ve kaç AI Overview'da geçtiği.", "The four domains cited most in the group's AI Overviews and in how many AI Overviews they appear.")],
             [[x(*_SO.GRUP_AD[g_]), cell(len(_SO.GRUP[g_])), cell(_SO.ai_grup(g_)["gorulen"]), cell(_SO.ai_grup(g_)["icerik"]), n("%d / %d" % (_SO.ai_grup(g_)["vitra"], _SO.ai_grup(g_)["icerik"])),
               sayi_ayni(", ".join("%s (%d)" % (veri_m(d_), c_) for d_, c_ in _hk_alan(_SO.GRUP[g_])))] for g_ in "ABC"]
             + [["<b>%s</b>" % x("Toplam", "Total"), cell(_SO.NT), cell(len(_SO.AI_GORULEN)), cell(len(_SO.AI_ICERIK)), n("%d / %d" % (len(_SO.AI_VITRA), len(_SO.AI_ICERIK))),
                 sayi_ayni(", ".join("%s (%d)" % (veri_m(d_), c_) for d_, c_ in _hk_alan(_SO.TUM)))]])

_AIVX = [r_["kelime"] for r_ in sorted([r_ for r_ in _SO.TUM if r_["kelime"] in _SO.AI_VITRA], key=lambda r_: -r_["hacim"])[:3]]
def firsat(no, h_tr, h_en, maddeler):
    return ('<article class="fnote"><span class="fc">%s</span><h3>%s</h3><ul>%s</ul></article>'
            % (x("Fırsat %02d" % no, "Opportunity %02d" % no), x(h_tr, h_en), "".join("<li>%s</li>" % x(a, b) for a, b in maddeler)))
FIRSAT = '<div class="fnotes">%s</div>' % "".join([
 firsat(1, "Sorun çözen destek içeriği", "Problem-solving support content",
        [("Rehber sayfalarında tıkların %s'i montaj, tamir ve temizlik yazılarından gelmektedir; bu yazılar sayfaların yalnız %s'idir" % (yzd(prat_t), yzd(prat_n)), "%s of guide page clicks come from installation, repair and cleaning articles, which are only %s of pages" % (("%.1f" % prat_t) + "%", ("%.1f" % prat_n) + "%")),
         ("Destek bölümünde garanti, montaj hizmeti, ürün grupları, sipariş ve teslimat konularında %d SSS sayfası ve yaklaşık %d soru bulunmaktadır; ancak %d sayfada sayfa başlığı \"Accelerator Title\" olarak kalmış ve soru-cevap işaretlemesi yer almamaktadır, lavabo, banyo mobilyası, yıkanma alanları ve aksesuar için ikişer ayrı SSS sayfası bulunmaktadır" % (_DSN, round(_DSQ, -1), len(_DSB)),
          "The support section has %d FAQ pages with about %d questions on warranty, installation service, product groups, ordering and delivery; however %d pages still carry the page title \"Accelerator Title\" and have no question-and-answer markup, and washbasins, bathroom furniture, bathing areas and accessories each have two separate FAQ pages" % (_DSN, round(_DSQ, -1), len(_DSB))),
         ("Site haritasında destek bölümünden yalnızca %d adres yer almakta, eski online.vitra.com.tr SSS adresleri ise Search Console'da yılda %s gösterim almaya devam etmektedir; arıza konusunda öne çıkan tek içerik gömme rezervuar tamiri yazısıdır" % (_DE["sitemap_destek_adres"], k(_DSE)),
          "Only %d support addresses are in the sitemap, while the old online.vitra.com.tr FAQ addresses still receive %s impressions a year in Search Console; the only prominent troubleshooting content is the concealed cistern repair article" % (_DE["sitemap_destek_adres"], k(_DSE).replace(",", "."))),
         ("Arıza, parça uyumu ve bakım sorularını cevaplayan destek sayfaları hem AI yanıtlarında kaynak olma hem de satış sonrası başvuruyu siteye taşıma fırsatı sunmaktadır", "Support pages answering troubleshooting, part compatibility and care questions offer the opportunity both to be a source in AI answers and to bring after-sales enquiries to the site")]),
 firsat(2, "Karar ve ölçü sorularında kaynak olmak", "Becoming the source on decision and size questions",
        [("VitrA %d AI Overview'un %s kaynak gösterilmektedir (%s)" % (len(_SO.AI_ICERIK), ek(len(_SO.AI_VITRA), "inde"), ", ".join(_AIVX)), "VitrA is cited in %d of %d AI Overviews (%s)" % (len(_SO.AI_VITRA), len(_SO.AI_ICERIK), ", ".join(_AIVX))),
         ("\"80 cm banyo dolabı\" sorusunda kaynaklar %s, \"klozet montaj ücreti\" sorusunda %s; bu sorularda VitrA kaynak gösterilmemektedir" % (_ref("80 cm banyo dolabı", 3), _ref("klozet montaj ücreti", 3)), "For \"80 cm banyo dolabı\" the sources are %s and for \"klozet montaj ücreti\" %s; VitrA is not cited in these questions" % (_ref("80 cm banyo dolabı", 3), _ref("klozet montaj ücreti", 3))),
         ("Ölçü, seçim ve karşılaştırma odaklı rehber içerik ile kategori sayfalarındaki kısa soru-cevaplar bu sorularda görünürlüğü artırabilir", "Guide content focused on sizes, selection and comparison, together with short Q&A on category pages, can raise visibility on these questions")]),
 firsat(3, "Soru sorgularında ilk sayfadan tıka", "From the first page to the click on question queries",
        [("vitra.com.tr soru biçimli sorgularda ortalama %s. sıradadır, CTR %s'tir" % (("%.1f" % so_p).replace(".", ","), yzd(100 * so_c / so_i, 2)), "vitra.com.tr ranks %s on average on question queries with a CTR of %s" % ("%.1f" % so_p, ("%.2f" % (100 * so_c / so_i)) + "%")),
         ("Klozet kapağı montajını soran sorgular %s gösterim almaktadır; düşük CTR, cevabın sonuç sayfasında verilmesiyle ilişkilendirilebilir" % k(kap_i), "Queries about fitting a WC seat receive %s impressions; the low CTR can be linked to the answer being given on the results page" % k(kap_i).replace(",", ".")),
         ("Bu sorgularda AI Overview'da kaynak gösterilen sayfa olmak, tık kadar önemli bir görünürlük biçimidir", "Being the page cited in AI Overview is a form of visibility as important as the click on these queries")]),
 firsat(4, "Marka ve entity tutarlılığı", "Brand and entity consistency",
        [("Wikidata'da VitrA için iki ayrı kayıt bulunmaktadır; ana kayıtta resmi web sitesi alanı vitra.com.tr'yi göstermemektedir", "Wikidata holds two separate VitrA records; the official website field of the main record does not show vitra.com.tr"),
         ("Türkçe Wikipedia maddesi kısadır; Artema'nın Wikidata ve Wikipedia kaydı bulunmamaktadır, \"VitrA ve Artema aynı marka mı?\" sorusu sonuç sayfasında çıkmaktadır", "The Turkish Wikipedia article is short; Artema has no Wikidata or Wikipedia record, and the question \"are VitrA and Artema the same brand?\" appears on the results page"),
         ("Marka kayıtlarının tutarlı hale gelmesi, AI yanıtlarında VitrA ve Artema'nın doğru tanımlanmasını destekleyebilir", "Consistent brand records can support VitrA and Artema being identified correctly in AI answers")]),
 firsat(5, "Site dışı sinyaller", "Off-site signals",
        [("Şikayetvar'da VitrA puanı 100 üzerinden 18'dir (son 1 yıl çözüm oranı); marka güvenilirliği sorularında bu platformlar kaynak gösterilebilmektedir", "On Şikayetvar the VitrA score is 18 out of 100 (the last-year resolution rate); these platforms can be cited on brand reliability questions"),
         ("En çok izlenen 14 YouTube tamir ve kurulum konusunda VitrA kanal videosu bulunmamaktadır; AI Overview kaynakları arasında markadan bağımsız rehber ve topluluk siteleri yer almaktadır", "There is no VitrA channel video in the 14 most-watched YouTube repair and installation topics; AI Overview sources include brand-independent guide and community sites"),
         ("Şikayet yanıtları, tamir videoları ve rehber sitelerinde uzman içerik, markanın site dışında anılmasını güçlendirebilir", "Complaint replies, repair videos and expert content on guide sites can strengthen off-site mentions of the brand")]),
 firsat(6, "AI ile alışveriş", "Shopping with AI",
        [("\"vitra klozet trendyol mu hepsiburada mı daha uygun\" sorusunda yapay zeka yanıtlarının %d'%s VitrA geçmekte, vitra.com.tr %s kaynak gösterilmektedir; iade ve teslimat sorularında VitrA %d yanıtın yalnız %s anılmaktadır" % (_q1["yanit"], "inin tamamında" if _q1["vitra_adi"] == _q1["yanit"] else "", ek(_q1["vitra_kaynak"], "inde"), _q3["yanit"] + _q4["yanit"], ek(_q3["vitra_adi"] + _q4["vitra_adi"], "inde")),
          "For \"vitra klozet trendyol mu hepsiburada mı daha uygun\" VitrA is named in all %d AI answers while vitra.com.tr is cited in %d; in return and delivery questions VitrA is named in only %d of %d answers" % (_q1["yanit"], _q1["vitra_kaynak"], _q3["vitra_adi"] + _q4["vitra_adi"], _q3["yanit"] + _q4["yanit"])),
         ("Google Shopping'de VitrA sitesi listelemelerin %0,7'sini almakta, 27 kategori kelimesinin 15'inde görünmemektedir", "On Google Shopping the VitrA site takes 0.7% of listings and does not appear in 15 of 27 category keywords"),
         ("Google AI Mode ve ChatGPT alışveriş yanıtları ürün akışlarından ve ürün sayfası verisinden yararlanmaktadır", "Google AI Mode and ChatGPT shopping answers draw on product feeds and product page data"),
         ("Ürün akışının kapsamı, ürün bilgisinin zenginliği ve llms.txt'nin destek ve rehber içeriğiyle genişletilmesi bu yanıtlarda yer almayı destekleyebilir", "The coverage of the product feed, richer product information and an llms.txt expanded with support and guide content can support appearing in these answers")]),
])

# her başlıktaki örneklem sayısı başlık metniyle aynı olmalıdır (h3_not.py anahtarları bu metinlerle eşlenir)
assert (AIG["markasiz_soru"], len(_KS), _BS.TOP["n"], _SO.NT, _soN) == (111, 29, 2140, 322, 21), "GEO başlık örneklemleri değişti"
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
<h3>%s</h3>
%s
<h3>%s</h3>
<div class="kpis">%s%s</div>
<p class="popl">%s</p>
%s
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Google AI Overview, Gemini ve ChatGPT gibi yapay zeka yanıtları kullanıcının sorusunu birden fazla kaynaktan derlenen tek bir cevapla karşılamaktadır; bu cevaplarda kaynak gösterilmek, soruyu doğrudan cevaplayan sayfaya, markanın tutarlı tanımlanmasına ve markadan site dışında söz edilmesine bağlıdır. VitrA'nın bu yanıtlardaki yeri 125 soruluk yapay zeka yanıt takibi (4 Eyl - 3 Eki 2026), SEOmonitor'de takip edilen 2.140 kelime (03.10.2026), bu rapor için seçilen 322 hedef kelime (" + _TRH + ") ve vitra.com.tr'nin Search Console verisi (1 Eki 2025 - 30 Eyl 2026) ile ölçülmüştür.",
   "AI answers such as Google AI Overview, Gemini and ChatGPT meet the user's question with a single answer compiled from several sources; being cited in these answers depends on a page that answers the question directly, consistent identification of the brand and mentions of the brand off the site. VitrA's place in these answers was measured with 125-question AI answer tracking (4 Sep - 3 Oct 2026), the 2,140 keywords tracked in SEOmonitor (03.10.2026), the 322 target keywords selected for this report (" + _TRH + ") and vitra.com.tr's Search Console data (1 Oct 2025 - 30 Sep 2026)."),
 kpi_kart("%s-%s" % (yzd(AIV["chatgpt"], 0), ("%.0f" % AIV["gemini"])), "Yapay zeka yanıt takibi · 111 markasız soruda VitrA'nın adıyla geçtiği yanıt payı, ChatGPT ile Gemini arası · 4 Eyl - 3 Eki 2026", "AI answer tracking · share of answers naming VitrA in 111 questions without a brand name, ChatGPT to Gemini · 4 Sep - 3 Oct 2026", "hi"),
 kpi_kart(yzd(100 * _BS.TOP["vitra"] / _BS.TOP["aio"], 0), "SEOmonitor takibi · 2.140 kelimeden AI Overview çıkan %s kelimede VitrA'nın kaynak gösterildiği pay · 03.10.2026" % bin(_BS.TOP["aio"]),
          "SEOmonitor tracking · share of the %s keywords with an AI Overview (out of 2,140) where VitrA is cited · 03.10.2026" % f"{_BS.TOP['aio']:,}"),
 kpi_kart("%d / %d" % (_SO.ai_grup("A")["vitra"], _SO.ai_grup("A")["icerik"]), "Rapor hedef kelimeleri · VitrA gamındaki %d kelimede içeriği alınan AI Overview'larda VitrA'nın kaynak gösterildiği sayı · %s" % (len(_SO.GRUP["A"]), _TRH), "Report target keywords · AI Overviews citing VitrA among those retrieved for the %d keywords in the VitrA range · %s" % (len(_SO.GRUP["A"]), _TRH)),
 kpi_kart("%d / %d" % (len(_DSB), _DSN), "vitra.com.tr destek bölümündeki %d SSS sayfasından sayfa başlığı şablon metinde kalmış ve soru-cevap işaretlemesi olmayan sayfa · ayrıca 4 ürün grubunda çift SSS sayfası, 04.10.2026" % _DSN, "Of the %d FAQ pages in vitra.com.tr's support section, pages whose title is still template text and that have no Q&A markup · plus duplicate FAQ pages for 4 product groups, 04.10.2026" % _DSN),
 x("Ölçüm setleri: dört veri seti ve örneklemleri", "Measurement sets: four data sets and their samples"),
 T_VK + insight("Oranlar ölçülen örnekleme göre değişmektedir. Yapay zeka yanıt takibindeki sorular doğal dilde yazılmış uzun sorulardır ve VitrA'nın yanıtta adıyla geçip geçmediğini ölçmektedir; SEOmonitor takibi ve rapor hedef kelimeleri ise Google'a yazılan kısa aramalardır ve vitra.com.tr'nin AI Overview'da kaynak gösterilip gösterilmediğini ölçmektedir. Rapor hedef kelimelerinde VitrA gamındaki oran (%s) SEOmonitor takibindeki orana (%s) yakındır; VitrA'nın satmadığı yakın kategorilerde ise vitra.com.tr kaynak gösterilmemektedir (%d / %d). Aynı kelimede AI Overview'un çıkıp çıkmadığı gün ve ölçüm aracına göre de değişebilmektedir." % (yzd(100 * _SO.ai_grup("A")["vitra"] / _SO.ai_grup("A")["icerik"], 0), yzd(100 * _BS.TOP["vitra"] / _BS.TOP["aio"], 0), _SO.ai_grup("B")["vitra"], _SO.ai_grup("B")["icerik"]),
         "Rates vary with the sample measured. The questions in AI answer tracking are long natural-language questions and measure whether VitrA is named in the answer; SEOmonitor tracking and the report target keywords are short searches typed into Google and measure whether vitra.com.tr is cited in the AI Overview. In the report target keywords the rate in the VitrA range (%s) is close to the rate in SEOmonitor tracking (%s); in adjacent categories VitrA does not sell, vitra.com.tr is not cited (%d / %d). Whether an AI Overview appears for the same keyword can also vary by day and measurement tool." % (("%.0f" % (100 * _SO.ai_grup("A")["vitra"] / _SO.ai_grup("A")["icerik"])) + "%", ("%.0f" % (100 * _BS.TOP["vitra"] / _BS.TOP["aio"])) + "%", _SO.ai_grup("B")["vitra"], _SO.ai_grup("B")["icerik"]), "D39", "D42", "D19") + kopru("Takip edilen %d promptun tamamı, platform bazında oranları ve en son yanıt metinleri ayrı sayfadadır." % AIG["soru"], "All %d tracked prompts, their rates by platform and the latest answer texts are on a separate page." % AIG["soru"], "geo-promptlari.html", "GEO Promptları sayfasını görüntüle", "View the GEO Prompts page"),
 x("Yapay zeka yanıt takibi · 111 markasız soruda markaların anılma payı", "AI answer tracking · how often brands are named in 111 questions without a brand name"),
 T_AIG + kopru("Soru bazında oranlar ve yanıt metinleri:", "Rates by question and answer texts:", "geo-promptlari.html", "GEO Promptları", "GEO Prompts", "#promptlar"),
 insight(("**Marka adı geçmeyen %d soruda VitrA, yapay zeka yanıtlarında en sık adı geçen üretici markadır**: ChatGPT yanıtlarının %s, Gemini'nin %s ve Google AI Overview'un %s VitrA'yı adıyla anmaktadır. Kale ve Creavit üç platformda da bu oranın altındadır; AI Overview'da ise Trendyol, Hepsiburada ve Koçtaş gibi satış kanalları yanıtların %%28-32 bandında yer almaktadır. VitrA'nın geçtiği ve tonu belirlenebilen yanıtların %s olumsuz tonludur.")
         % (AIG["markasiz_soru"], yzd(AIV["chatgpt"]) + "'inde", yzd(AIV["gemini"]) + "'ünde", yzd(AIV["google_ai_overview"]) + "'unda", yzd_ek(100 * _DY["olumsuz"] / (_DY["olumlu"] + _DY["olumsuz"] + _DY["notr"]), 1, "i")),
         ("**In %d questions without a brand name, VitrA is the manufacturer brand named most often in AI answers**: %s of ChatGPT answers, %s of Gemini answers and %s of Google AI Overview answers name VitrA. Kale and Creavit stay below this rate on all three platforms; in AI Overview, sales channels such as Trendyol, Hepsiburada and Koçtaş appear in 28-32%% of answers. %s of the answers naming VitrA with an identifiable tone are negative.")
         % (AIG["markasiz_soru"], ("%.1f" % AIV["chatgpt"]) + "%", ("%.1f" % AIV["gemini"]) + "%", ("%.1f" % AIV["google_ai_overview"]) + "%", ("%.1f" % (100 * _DY["olumsuz"] / (_DY["olumlu"] + _DY["olumsuz"] + _DY["notr"]))) + "%"), "D39"),
 x("Yapay zeka yanıt takibi · 111 markasız soruda kaynak gösterilen alan adları", "AI answer tracking · domains cited in 111 questions without a brand name"),
 T_AIK,
 insight(("**vitra.com.tr, yapay zeka yanıtlarında en çok kaynak gösterilen alan adıdır** (%s yanıt); ancak Trendyol, Koçtaş, Hepsiburada ve Akakçe birlikte %s yanıtta kaynaktır. **Satın alma sorularında sıralama değişmektedir**: Koçtaş (%d), Trendyol (%d) ve Bauhaus (%d) vitra.com.tr'nin (%d) önündedir. Rehber siteleri (banyome.com, yapilir.com) ve YouTube da montaj ve seçim sorularında sık kaynak gösterilmektedir.")
         % (bin(_KD["vitra.com.tr"][1]), bin(_PZ4), _KD["koctas.com.tr"][5], _KD["trendyol.com"][5], _KD["bauhaus.com.tr"][5], _KD["vitra.com.tr"][5]),
         ("**vitra.com.tr is the domain cited most in AI answers** (%s answers); however Trendyol, Koçtaş, Hepsiburada and Akakçe together are cited in %s answers. **The order changes for purchase questions**: Koçtaş (%d), Trendyol (%d) and Bauhaus (%d) are ahead of vitra.com.tr (%d). Guide sites (banyome.com, yapilir.com) and YouTube are also frequently cited for installation and selection questions.")
         % (f"{_KD['vitra.com.tr'][1]:,}", f"{_PZ4:,}", _KD["koctas.com.tr"][5], _KD["trendyol.com"][5], _KD["bauhaus.com.tr"][5], _KD["vitra.com.tr"][5]), "D39"),
 x("Yapay zeka yanıt takibi · 29 satın alma ve montaj sorusunda VitrA ve vitra.com.tr", "AI answer tracking · VitrA and vitra.com.tr in 29 purchase and installation questions"),
 T_AIS + kopru("Bu soruların ChatGPT, Gemini ve AI Overview'daki en son yanıtları:", "The latest ChatGPT, Gemini and AI Overview answers to these questions:", "geo-promptlari.html", "Yanıt metinlerini görüntüle", "View the answer texts", "#yanitlar"),
 insight(("**Satın almaya yakın sorularda VitrA adı geçse de yanıt kullanıcıyı pazaryerine yönlendirmektedir**: \"vitra klozet trendyol mu hepsiburada mı daha uygun\" sorusunda VitrA %d yanıtın %s geçmekte, vitra.com.tr yalnızca %s kaynak gösterilmektedir; \"klozet nereden alınır en uygun fiyata\" sorusunda pazaryeri kaynakları %d yanıtın %s yer almaktadır. **Teslimat ve iade sorularında VitrA neredeyse hiç anılmamaktadır** (iade ve değişim %d yanıtın %s, kargo ve teslimat %d yanıtın %s). Montaj dahil satış sorusunda ise vitra.com.tr %d yanıtın %s kaynaktır; \"banyo dolabı montajı\" sorusunda vitra.com.tr hiç kaynak gösterilmemektedir. **Teslimat, kargo hasarı, iade, kurulum ve banyo dolabı montajı koşullarının vitra.com.tr'de soru-cevap biçiminde yer alması**, bu yanıtlarda kaynak gösterilme potansiyeli taşımaktadır.")
         % (_q1["yanit"], _kac(_q1["vitra_adi"], _q1["yanit"]), ek(_q1["vitra_kaynak"], "inde"),
            _q2["yanit"], ek(_q2["pazaryeri_kaynak"], "inde"), _q3["yanit"], ek(_q3["vitra_adi"], "inde"), _q4["yanit"], ek(_q4["vitra_adi"], "inde"), _q5["yanit"], ek(_q5["vitra_kaynak"], "inde")),
         ("**In questions close to purchase, VitrA is named but the answer points the user to marketplaces**: for \"vitra klozet trendyol mu hepsiburada mı daha uygun\" VitrA is named in %s answers while vitra.com.tr is cited in only %d; for \"klozet nereden alınır en uygun fiyata\" marketplace sources appear in %d of %d answers. **VitrA is barely named in delivery and return questions** (returns and exchanges %d of %d answers, shipping and delivery %d of %d). For the question on sales including installation, vitra.com.tr is cited in %d of %d answers; for \"banyo dolabı montajı\" vitra.com.tr is never cited. **Presenting delivery, shipping damage, returns, installation and cabinet fitting terms on vitra.com.tr in a question-and-answer format** has the potential to be cited in these answers.")
         % (("all %d" % _q1["yanit"]) if _q1["vitra_adi"] == _q1["yanit"] else ("%d of %d" % (_q1["vitra_adi"], _q1["yanit"])), _q1["vitra_kaynak"], _q2["pazaryeri_kaynak"], _q2["yanit"], _q3["vitra_adi"], _q3["yanit"], _q4["vitra_adi"], _q4["yanit"], _q5["vitra_kaynak"], _q5["yanit"]), "D39"),
 x("SEOmonitor takibi · 2.140 kelimede AI Overview ve VitrA", "SEOmonitor tracking · AI Overview and VitrA in 2,140 keywords"),
 _BS.T_AIO + _BS.INS_AIO,
 x("Rapor hedef kelimeleri · 322 kelimede AI Overview ve kaynak siteler", "Report target keywords · AI Overview and cited sites in 322 keywords"),
 T_HK + insight("%d rapor hedef kelimesinin %d'%s AI Overview çıkmıştır. VitrA gamında içeriği alınan %d AI Overview'un %s vitra.com.tr kaynak gösterilmektedir; marka ve karşılaştırma aramalarında oran %d / %d, VitrA'nın satmadığı yakın kategorilerde %d / %d'dir. Üç grupta en sık kaynak gösterilen alan adları %s olarak görülmektedir; satın almaya yakın kısa aramalarda pazaryerleri ve rehber siteleri kaynak olarak öne çıkmaktadır." % (_SO.NT, len(_SO.AI_GORULEN), ek(len(_SO.AI_GORULEN), "inde").split("'")[1], _SO.ai_grup("A")["icerik"], ek(_SO.ai_grup("A")["vitra"], "inde"), _SO.ai_grup("C")["vitra"], _SO.ai_grup("C")["icerik"], _SO.ai_grup("B")["vitra"], _SO.ai_grup("B")["icerik"], ", ".join(veri_m(d_) for d_, _ in _hk_alan(_SO.TUM))),
         "AI Overviews appeared for %d of the %d report target keywords. vitra.com.tr is cited in %d of the %d AI Overviews retrieved in the VitrA range; in brand and comparison searches the rate is %d / %d and in adjacent categories VitrA does not sell %d / %d. The domains cited most across the three groups are %s; in short searches close to purchase, marketplaces and guide sites stand out as sources." % (len(_SO.AI_GORULEN), _SO.NT, _SO.ai_grup("A")["vitra"], _SO.ai_grup("A")["icerik"], _SO.ai_grup("C")["vitra"], _SO.ai_grup("C")["icerik"], _SO.ai_grup("B")["vitra"], _SO.ai_grup("B")["icerik"], ", ".join(veri_m(d_) for d_, _ in _hk_alan(_SO.TUM))), "D19"),
 x("Sitenin hazırlığı · Search Console'da rehber sayfaları ve 21 soru sorgusu", "Site readiness · guide pages and 21 question queries in Search Console"),
 kpi_kart(yzd(prat_t), "Rehber içerik tıklarının montaj, tamir ve temizlik yazılarından gelen payı · sayfaların %s'i, 1 Eki 2025 - 30 Eyl 2026" % yzd(prat_n), "Share of guide content clicks from installation, repair and cleaning articles · %s of pages, 1 Oct 2025 - 30 Sep 2026" % (("%.1f" % prat_n) + "%"), "hi"),
 kpi_kart(yzd(100 * so_c / so_i, 2), "Soru sorgularında CTR · ortalama sıra %s, 1 Eki 2025 - 30 Eyl 2026" % ("%.1f" % so_p).replace(".", ","), "CTR on question queries · average position %s, 1 Oct 2025 - 30 Sep 2026" % ("%.1f" % so_p), "dn"),
 _POPSO,
 GR,
 insight("vitra.com.tr'nin rehber sayfaları dönemde %s organik tık almıştır. Montaj, tamir ve temizlik yazıları sayfaların %s'ini oluşturup tıkların %s'ini almakta, dekorasyon, trend ve sürdürülebilirlik yazıları ise sayfaların %s'ini oluşturup tıkların %s'ini almaktadır; tamir konusunda tek yazı bulunmaktadır. Soru biçimli sorgularda site ilk sayfadadır ancak CTR %s'te kalmaktadır: cevabın sonuç sayfasında verildiği bu sorgularda AI Overview'da kaynak gösterilmek görünürlüğün ana biçimi haline gelmektedir." % (
         k(TOP_T), yzd(prat_n), yzd(prat_t), yzd(100 * (GS["dekor"][0] + GS["surd"][0]) / TOP_N), yzd(100 * (GS["dekor"][1] + GS["surd"][1]) / TOP_T), yzd(100 * so_c / so_i, 2)),
         "vitra.com.tr guide pages received %s organic clicks in the period. Installation, repair and cleaning articles make up %s of pages and take %s of clicks, while decoration, trend and sustainability articles make up %s of pages and take %s of clicks; there is a single repair article. On question queries the site is on the first page but CTR stays at %s: for these queries, answered on the results page itself, being cited in AI Overview becomes the main form of visibility." % (
         k(TOP_T).replace(",", "."), ("%.1f" % prat_n) + "%", ("%.1f" % prat_t) + "%", ("%.1f" % (100 * (GS["dekor"][0] + GS["surd"][0]) / TOP_N)) + "%", ("%.1f" % (100 * (GS["dekor"][1] + GS["surd"][1]) / TOP_T)) + "%", ("%.2f" % (100 * so_c / so_i)) + "%"), "D33", "D19"),

 x("Fırsat alanları", "Opportunity areas"),
 FIRSAT,
 insight("Fırsatların ortak noktası, kullanıcının bir sorunu çözmek ya da karar vermek için sorduğu sorulardır. Talep, satış sonrası şikayetler ve arama sonuçları aynı konularda (tamir, montaj, uyumluluk, ölçü) yoğunlaşmaktadır; bu konularda VitrA'nın üretici bilgisiyle kaynak olması, hem AI yanıtlarındaki görünürlüğü hem de satış sonrası deneyimi destekleyebilir.",
         "What the opportunities share is the questions users ask to solve a problem or make a decision. Demand, after-sales complaints and search results concentrate on the same topics (repair, installation, compatibility, size); VitrA being the source on these topics with manufacturer knowledge can support both visibility in AI answers and the after-sales experience.", "D24", "D19"),
 kaynak("Google Search Console · /ilham-veren-fikirler/ sayfaları ve soru sorguları, 1 Eki 2025 - 30 Eyl 2026 · Google arama sonuçları ve AI Overview, %d kelime, %s · Yapay zeka yanıt takibi, 125 soru, ChatGPT, Gemini ve Google AI Overview, 4 Eyl - 3 Eki 2026 · Wikidata ve Wikipedia, 02.10.2026 · vitra.com.tr llms.txt ve site haritaları, 02.10.2026 · Şikayetvar, YouTube ve Google Shopping verileri ilgili bölümlerdeki kaynaklardandır" % (_SO.NT, _TRH),
        "Google Search Console · /ilham-veren-fikirler/ pages and question queries, 1 Oct 2025 - 30 Sep 2026 · Google search results and AI Overview, %d keywords, %s · AI answer tracking, 125 questions, ChatGPT, Gemini and Google AI Overview, 4 Sep - 3 Oct 2026 · Wikidata and Wikipedia, 02.10.2026 · vitra.com.tr llms.txt and sitemaps, 02.10.2026 · Şikayetvar, YouTube and Google Shopping data come from the sources of the related sections" % (_SO.NT, _TRH), "D33", "D19", "D39", "D34", "D35", "D24", "D20", "D25"),
) + _DIASO
