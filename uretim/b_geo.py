# -*- coding: utf-8 -*-
"""Bolum: AI aramada gorunurluk (GEO) - AI Overview odakli icerik plani, entity tutarliligi, site disi sinyaller, AI alisveris."""
from ortak import *
from rapor_parca1 import T
from grafik2 import gruplu
import csv as _csv, os as _os, json as _json

_D = _os.path.join(veri.V, "ham", "geo")
IL = [(s_, int(c), int(i), float(p_)) for s_, c, i, p_ in _csv.reader(open(_os.path.join(_D, "gsc_ilham.tsv"), encoding="utf-8"), delimiter="\t")]
SO = [(q, int(c), int(i), float(p_)) for q, c, i, p_ in _csv.reader(open(_os.path.join(_D, "gsc_soru.tsv"), encoding="utf-8"), delimiter="\t")]
SOD = {q: (c, i, p_) for q, c, i, p_ in SO}
_SK = {r["kelime"]: r for r in _json.load(open(_os.path.join(veri.V, "ham/derin/serp/kelime_sonuc.json"), encoding="utf-8"))}
ILHAM = "https://www.vitra.com.tr/ilham-veren-fikirler/"

# ---------------------------------------------------------------- rehber icerik gruplari
GRUP = [("tamir", "Tamir, temizlik ve bakım", "Repair, cleaning and maintenance"), ("montaj", "Montaj ve kurulum", "Installation and fitting"),
        ("secim", "Seçim, ölçü ve \"nedir\" rehberleri", "Selection, size and \"what is\" guides"), ("plan", "Planlama ve tadilat", "Planning and renovation"),
        ("dekor", "Dekorasyon, trend ve karo modelleri", "Decoration, trends and tile designs"), ("surd", "Sürdürülebilirlik ve kurumsal", "Sustainability and corporate")]
GAD = {a: (b, c) for a, b, c in GRUP}
def grup(s_):
    if any(k_ in s_ for k_ in ("surdurul", "yesil-", "dongusel", "geri-donus", "cevre", "dunya-", "kuresel", "inovasyon-gunu", "temas-yoluyla", "herkes-icin")): return "surd"
    if any(k_ in s_ for k_ in ("temizl", "tamir", "hijyen")): return "tamir"
    if any(k_ in s_ for k_ in ("montaj", "takilir", "dosenir")): return "montaj"
    if any(k_ in s_ for k_ in ("tadilat", "yenile", "planlama", "mimari", "engelli")): return "plan"
    if any(k_ in s_ for k_ in ("secim", "secil", "secerken", "nedir", "nelerdir", "olculeri", "kullanisli", "saglikli", "quantumflush", "satin-alma", "kuvet-mi")): return "secim"
    return "dekor"
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
            x("Rehber içerik gruplarının sayfa sayısı ve organik tık payı · /ilham-veren-fikirler/, 1 Eki 2025 - 25 Eyl 2026", "Share of pages and organic clicks by guide content group · /ilham-veren-fikirler/, 1 Oct 2025 - 25 Sep 2026"))
T_GR = tablo([th("İçerik grubu", "Content group", "Sayfa adresindeki konuya göre yapılan gruplama.", "Grouping by the topic in the page address."),
              th("Sayfa", "Pages", "Dönemde en az 5 tık alan sayfa sayısı.", "Number of pages with at least 5 clicks in the period.", True),
              th("Tık", "Clicks", "1 Eki 2025 - 25 Eyl 2026 organik tık.", "Organic clicks, 1 Oct 2025 - 25 Sep 2026.", True),
              th("Tık payı", "Click share", "Rehber içeriklerin toplam tıkı içindeki pay.", "Share of the total clicks of guide content.", True),
              th("Gösterim", "Impressions", "Aynı dönemde gösterim.", "Impressions in the same period.", True),
              th("CTR", "CTR", "Tık / gösterim.", "Clicks / impressions.", True),
              th("En çok tık alan sayfa", "Page with most clicks", "Grubun en çok tık alan sayfası; bağlantı canlı sayfayı açar.", "The group's page with the most clicks; the link opens the live page.")],
             [[x(b, c), cell(GS[a][0]), cellk(GS[a][1]), n(yzd(100 * GS[a][1] / TOP_T)), cellk(GS[a][2]), n(yzd(100 * GS[a][1] / GS[a][2])), u(ILHAM + GS[a][3][0] + ("" if GS[a][3][0].endswith("rehberi") else "/"), _baslik(GS[a][3][0])) + " (%s)" % bin(GS[a][3][1])] for a, b, c in GRUP])

# ---------------------------------------------------------------- soru sorgulari
so_i = sum(i for _, _, i, _ in SO); so_c = sum(c for _, c, _, _ in SO)
so_p = sum(p_ * i for _, _, i, p_ in SO) / so_i
T_SO = tablo([th("Sorgu", "Query", "Search Console'da vitra.com.tr'nin gösterim aldığı soru biçimli sorgu; \"nasıl\" ve \"su kaçır\" içeren sorgulardan gösterime göre seçilmiştir.", "Question-type query for which vitra.com.tr received impressions; selected by impressions from queries containing \"nasıl\" (how) and \"su kaçır\" (leaking)."),
              th("Gösterim", "Impressions", "1 Eki 2025 - 25 Eyl 2026 gösterim.", "Impressions, 1 Oct 2025 - 25 Sep 2026.", True),
              th("Tık", "Clicks", "Aynı dönemde tık.", "Clicks in the same period.", True),
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
  soru("VitrA gömme rezervuar neden su doldurmuyor?", "Klozet iç takım değişimi ne kadar?", "basmalı rezervuar iç takımı nasıl takılır"),
  ("\"gömme klozet su kaçırıyorsa çok basit tamiri\" %s gösterim, CTR %s; sitedeki tek tamir yazısı %s tık, %s gösterim; \"gömme rezervuar iç takımı\" AI Overview'unda kaynaklar %s, VitrA yok" % (k(gk[1]), yzd(100 * gk[0] / gk[1]), bin(gt[1]), k(gt[2]), _ref("gömme rezervuar iç takımı")),
   "\"gömme klozet su kaçırıyorsa çok basit tamiri\" %s impressions, CTR %s; the site's only repair article %s clicks, %s impressions; in the \"gömme rezervuar iç takımı\" AI Overview the sources are %s, not VitrA" % (k(gk[1]).replace(",", "."), ("%.1f" % (100 * gk[0] / gk[1])) + "%", f"{gt[1]:,}", k(gt[2]).replace(",", "."), _ref("gömme rezervuar iç takımı"))), ("D33", "D19")),
 ("Öncelik 1", ("Klozet kapağı montajı ve uyumluluk: kapak tipine göre montaj, hangi kapak hangi klozete uyar", "WC seat fitting and compatibility: fitting by seat type, which seat fits which WC"),
  ("Destek sayfası; ürün sayfalarında klozet koduna göre uyumlu kapak tablosu", "Support page; a compatible-seat table by WC code on product pages"),
  soru("Klozet kapakları standart mı?", "amortisörlü klozet kapağı nasıl takılır", "eski tip klozet kapağı nasıl takılır"),
  ("Kapak montajı soran 6 sorgu toplam %s gösterim, %s tık (CTR %s); ortalama sıra 4,8-5,9" % (k(kap_i), bin(kap_c), yzd(100 * kap_c / kap_i, 2)),
   "6 queries about seat fitting total %s impressions and %s clicks (CTR %s); average position 4.8-5.9" % (k(kap_i).replace(",", "."), f"{kap_c:,}", ("%.2f" % (100 * kap_c / kap_i)) + "%")), ("D33",)),
 ("Öncelik 1", ("Batarya bakımı ve parça değişimi: conta, kartuş, kireç, damlatma ve montaj", "Tap maintenance and part replacement: seals, cartridges, limescale, dripping and fitting"),
  ("Destek sayfası; armatür ürün sayfalarından bağlantı", "Support page; linked from tap product pages"),
  soru("banyo batarya contası nasıl değiştirilir", "tezgah üstü musluk nasıl takılır", "lavabo bataryası nasıl takılır"),
  ("Conta değişimi %s, tezgah üstü musluk montajı %s gösterim; YouTube'da batarya ve kartuş konuları 7,0M izlenme ve VitrA kanal videosu yok" % (k(SOD["banyo batarya contası nasıl değiştirilir"][1]), k(SOD["tezgah üstü musluk nasıl takılır"][1])),
   "Seal replacement %s, countertop tap fitting %s impressions; on YouTube tap and cartridge topics have 7.0M views and no VitrA channel video" % (k(SOD["banyo batarya contası nasıl değiştirilir"][1]).replace(",", "."), k(SOD["tezgah üstü musluk nasıl takılır"][1]).replace(",", "."))), ("D33", "D20")),
 ("Öncelik 1", ("Ölçü ve yerleşim: klozet, lavabo, banyo dolabı ve duşakabin ölçüleri, montaj yükseklikleri", "Sizes and layout: WC, washbasin, bathroom cabinet and shower enclosure sizes, fitting heights"),
  ("Rehber yazı; kategori sayfalarında kısa soru-cevap", "Guide article; short Q&A on category pages"),
  soru("Klozet duvardan kaç cm uzakta olmalı?", "Banyo dolabı yüksekliği kaç santim olmalı?", "80'lik banyo dolabının ölçüleri nedir?"),
  ("\"klozet ölçüleri\" AI Overview'unda VitrA kaynak gösterilmektedir; \"80 cm banyo dolabı\" AI Overview'unda kaynaklar %s, VitrA yok" % _ref("80 cm banyo dolabı"),
   "VitrA is cited in the \"klozet ölçüleri\" AI Overview; in the \"80 cm banyo dolabı\" AI Overview the sources are %s, not VitrA" % _ref("80 cm banyo dolabı")), ("D19",)),
 ("Öncelik 1", ("Seçim karşılaştırmaları: gömme mi dış rezervuar mı, kanallı mı kanalsız mı, suya dayanıklı dolap malzemesi", "Selection comparisons: concealed or exposed cistern, rim or rimless, water-resistant cabinet materials"),
  ("Rehber yazı; karşılaştırma tablosuyla", "Guide article with a comparison table"),
  soru("Gömme rezervuar mantıklı mı?", "Kanallı klozet mi iyi kanalsız mı?", "MDF banyo dolabı suya dayanıklı mı?"),
  ("\"gömme rezervuar mı dış rezervuar mı\" AI Overview'unda kaynaklar %s; VitrA bu sorguda 14. sırada. \"suya dayanıklı banyo dolabı\" AI Overview'unda kaynaklar Trendyol ve Instagram" % _ref("gömme rezervuar mı dış rezervuar mı"),
   "In the \"gömme rezervuar mı dış rezervuar mı\" AI Overview the sources are %s; VitrA ranks 14th for this query. In the \"suya dayanıklı banyo dolabı\" AI Overview the sources are Trendyol and Instagram" % _ref("gömme rezervuar mı dış rezervuar mı")), ("D19",)),
 ("Öncelik 1", ("Marka soruları: VitrA ve Artema ilişkisi, menşei, kalite ve garanti", "Brand questions: the VitrA-Artema relationship, origin, quality and warranty"),
  ("Kurumsal soru-cevap sayfası; Wikidata ve Wikipedia güncellemeleriyle birlikte", "Corporate Q&A page, together with Wikidata and Wikipedia updates"),
  soru("VitrA ve Artema aynı marka mı?", "Artema hangi ülkenin markası?", "VitrA iyi marka mı?"),
  ("Bu sorular PAA kutusunda çıkmaktadır; Artema'nın Wikidata ve Wikipedia kaydı bulunmamaktadır", "These questions appear in the PAA box; Artema has no Wikidata or Wikipedia record"), ("D19", "D34")),
 ("Öncelik 1", ("Yedek parça, garanti ve servis: parça bulma, garanti süresi, servis ücreti ve başvuru adımları", "Spare parts, warranty and service: finding parts, warranty period, service fee and application steps"),
  ("Destek sayfası; ürün sayfalarından ve yedek parça kategorisinden bağlantı", "Support page; linked from product pages and the spare-parts category"),
  soru("vitra servis", "vitra yedek parça", "Klozet değişimini kim yapar?"),
  ("Şikayetvar'da servis ve garanti teması %54,7, yedek parça teması %17,8 (Nis - Eyl 2026); ürün sayfalarında garanti süresi bulunmamaktadır", "On Şikayetvar the service and warranty theme is 54.7% and the spare-part theme 17.8% (Apr - Sep 2026); product pages show no warranty period"), ("D24", "D13")),
 ("Öncelik 2", ("Montaj ücreti ve işçilik: ürün bazında montaj kapsamı ve fiyatı", "Installation fee and labour: installation scope and price by product"),
  ("Montaj hizmeti sayfasında soru-cevap bölümü", "A Q&A section on the installation service page"),
  soru("Klozet montajı kaç TL?", "Klozet yaptırmak kaç TL?", "Bir banyo tadilatı ne kadara mal olur?"),
  ("\"klozet montaj ücreti\" AI Overview'unda kaynaklar %s; VitrA'da 11 fiyatlı montaj kalemi bulunmaktadır" % _ref("klozet montaj ücreti"),
   "In the \"klozet montaj ücreti\" AI Overview the sources are %s; VitrA has 11 priced installation items" % _ref("klozet montaj ücreti")), ("D19", "D13")),
 ("Öncelik 2", ("Temizlik ve bakım: duşakabin, klozet ve batarya temizliği, kireç", "Cleaning and care: shower enclosure, WC and tap cleaning, limescale"),
  ("Mevcut yazıların soru-cevap bölümüyle güncellenmesi; ürün sayfalarına bakım bağlantısı", "Updating the existing articles with a Q&A section; care links on product pages"),
  soru("duşakabin kireci nasıl temizlenir", "Klozet nasıl temizlenir?", "duşakabin camı nasıl temizlenir"),
  ("Duşakabin temizliği yazısı %s tık ile ikinci en çok tık alan rehber içeriktir; \"duşakabin kireci nasıl temizlenir\" %s gösterim, sıra %s" % (bin(dt[1]), k(SOD["duşakabin kireci nasıl temizlenir"][1]), ("%.1f" % SOD["duşakabin kireci nasıl temizlenir"][2]).replace(".", ",")),
   "The shower enclosure cleaning article is the second most-clicked guide with %s clicks; \"duşakabin kireci nasıl temizlenir\" %s impressions, position %s" % (f"{dt[1]:,}", k(SOD["duşakabin kireci nasıl temizlenir"][1]).replace(",", "."), "%.1f" % SOD["duşakabin kireci nasıl temizlenir"][2])), ("D33",)),
 ("Öncelik 2", ("Erişilebilir ve çocuk banyosu: engelli klozeti ölçüleri, tutunma barları, çocuk klozeti", "Accessible and children's bathrooms: accessible WC dimensions, grab bars, children's WCs"),
  ("Rehber yazı; erişilebilir banyo kategori sayfasıyla birlikte", "Guide article together with an accessible bathroom category page"),
  soru("Engelli klozetinin farkı nedir?", "Engelli tuvaletinin ölçüleri nelerdir?", "Klozet adaptörü ne işe yarar?"),
  ("\"engelli klozet\" AI Overview'unda kaynaklar %s; VitrA yok" % _ref("engelli klozet", 5), "In the \"engelli klozet\" AI Overview the sources are %s; not VitrA" % _ref("engelli klozet", 5)), ("D19",)),
 ("Öncelik 2", ("Alt kategori açılımı: sayfası olmayan ya da farklı adla duran kesitler", "Sub-category expansion: segments with no page or a different name"),
  ("Kategori sayfası ve kısa soru-cevap", "Category page with a short Q&A"),
  soru("sıva üstü banyo bataryası", "fotoselli batarya", "jakuzi", "ayaklı lavabo"),
  ("Pazaryerlerinde ayrı kategori olarak aranan bu kesitlerin vitra.com.tr'de karşılık gelen sayfası bulunmamakta ya da farklı adla durmaktadır", "These segments, searched as separate categories on marketplaces, have no matching page on vitra.com.tr or sit under a different name"), ("D29", "D30")),
 ("Öncelik 3", ("Ürün tanımları ve bitişik ürünler: \"nedir\" yazılarının güncellenmesi, havlupan ve ısıtmalı kapak rehberleri", "Product definitions and adjacent products: updating \"what is\" articles, towel radiator and heated seat guides"),
  ("Mevcut yazıların güncellenmesi; yeni rehber yazı", "Updating existing articles; new guide articles"),
  soru("Pisuvar nedir?", "Şamandıra nedir ne işe yarar?", "Elektrikli havlupan banyoyu ısıtır mı?"),
  ("Bide nedir yazısı %s tık; \"pisuvar\" AI Overview'unda VitrA kaynak gösterilmektedir; \"şamandıra\" ve \"elektrikli havlupan\" AI Overview'larında VitrA yok" % bin(bn[1]),
   "The \"what is a bidet\" article %s clicks; VitrA is cited in the \"pisuvar\" AI Overview; not in the \"şamandıra\" and \"elektrikli havlupan\" AI Overviews" % f"{bn[1]:,}"), ("D33", "D19")),
]
T_PLAN = tablo([th("Öncelik", "Priority", "Talep, mevcut görünürlük ve satış sonrası etkisi birlikte değerlendirilerek verilen sıra.", "Order given by assessing demand, current visibility and after-sales impact together."),
                th("Konu kümesi", "Topic cluster", "Aynı ihtiyacı karşılayan soru grubu.", "A group of questions serving the same need."),
                th("Sayfa tipi", "Page type", "Konunun karşılanacağı sayfa: destek sayfası, rehber yazı ya da kategori sayfasında soru-cevap.", "The page that answers the topic: support page, guide article or Q&A on a category page."),
                th("Kullanıcı soruları", "User questions", "PAA kutusu, Search Console ve Autocomplete'ten örnek sorular; kullanıcının yazdığı biçimde.", "Example questions from the PAA box, Search Console and Autocomplete, as typed by users."),
                th("Dayanak", "Basis", "Konuyu öne çıkaran bulgu.", "The finding that puts the topic forward.")],
               [[ob(o), "<b>%s</b>" % x(*a), x(*t), sq, x(*d) + R(*kd)] for o, a, t, sq, d, kd in PLAN], "uzun")

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
T_ENT = tablo([th("Kayıt", "Record", "Markanın yapay zeka modelleri ve arama motorlarınca okunan kaydı; bağlantı kaydı açar.", "The brand record read by AI models and search engines; the link opens the record."),
               th("Mevcut durum (02.10.2026)", "Current state (02.10.2026)", "Kaydın 2 Ekim 2026 tarihli durumu.", "The state of the record on 2 October 2026."),
               th("Önerilen güncelleme", "Suggested update", "Kaydı vitra.com.tr ve kurumsal bilgiyle tutarlı hale getirecek düzenleme.", "The edit that would make the record consistent with vitra.com.tr and corporate information.")],
              [[a, x(*b), x(*c)] for a, b, c in ENT])

# ---------------------------------------------------------------- AI Overview kaynak siteleri (site disi)
YAYIN = [("banyome.com", 5), ("instagram.com", 5), ("wikipedia.org", 4), ("yapilir.com", 4), ("youtube.com", 3), ("banyomega.com", 3), ("eksisozluk.com", 2)]
RK = [(veri_m(a), b) for a, b in YAYIN]
RANK_Y = '<p class="figcap">%s</p>' % x("AI Overview'da kaynak gösterilen rehber ve topluluk siteleri · kaç blokta geçtiği (24 blok, 29.09.2026)", "Guide and community sites cited in AI Overview · number of blocks (24 blocks, 29.09.2026)") + rank_list(RK, 5, fmt=lambda v: bin(v))

HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
<div class="split"><div>%s</div>%s</div>
<h3>%s</h3>
%s
%s
""" % (
 x("Google AI Overview, Gemini ve ChatGPT gibi yapay zeka yanıtları kullanıcının sorusunu birden fazla kaynaktan derlenen tek bir cevapla karşılamaktadır. Bu cevaplarda kaynak gösterilmek üç unsura bağlıdır: soruyu doğrudan cevaplayan sayfa, markanın ansiklopedik kayıtlarda tutarlı tanımlanması ve markadan site dışında söz edilmesi. Değerlendirme vitra.com.tr rehber içeriklerinin Search Console performansına (1 Eki 2025 - 25 Eyl 2026), 29.09.2026 AI Overview gözlemine ve 02.10.2026 tarihli Wikidata ve Wikipedia kayıtlarına dayanmaktadır.",
   "AI answers such as Google AI Overview, Gemini and ChatGPT meet the user's question with a single answer compiled from several sources. Being cited in these answers depends on three elements: a page that answers the question directly, consistent identification of the brand in encyclopaedic records, and mentions of the brand off the site. The assessment is based on the Search Console performance of vitra.com.tr guide content (1 Oct 2025 - 25 Sep 2026), the AI Overview observation of 29.09.2026 and the Wikidata and Wikipedia records of 02.10.2026."),
 kpi_kart(yzd(prat_t), "Rehber içerik tıklarının montaj, tamir ve temizlik yazılarından gelen payı · sayfaların %s'i, 1 Eki 2025 - 25 Eyl 2026" % yzd(prat_n), "Share of guide content clicks from installation, repair and cleaning articles · %s of pages, 1 Oct 2025 - 25 Sep 2026" % (("%.1f" % prat_n) + "%"), "hi"),
 kpi_kart(yzd(100 * so_c / so_i, 2), "Soru sorgularında CTR · %d sorgu, %s gösterim, ortalama sıra %s" % (len(SO), k(so_i), ("%.1f" % so_p).replace(".", ",")), "CTR on question queries · %d queries, %s impressions, average position %s" % (len(SO), k(so_i).replace(",", "."), "%.1f" % so_p), "dn"),
 kpi_kart("5", "Destek bölümündeki sayfa sayısı (SSS, ödeme, teslimat, işlem, değişim-iade); montaj, arıza, uyumluluk ve garanti sayfası yok", "Pages in the support section (FAQ, payment, delivery, process, exchange-return); no installation, troubleshooting, compatibility or warranty page"),
 kpi_kart("2", "Wikidata'da VitrA için ayrı kayıt; ana kayıtta resmi web sitesi alanı vitra.com.tr'yi göstermiyor", "Separate VitrA records on Wikidata; in the main record the official website field does not show vitra.com.tr", "dn"),
 x("Rehber içerik: hangi konular trafik alıyor?", "Guide content: which topics bring traffic?"),
 GR, T_GR,
 insight("vitra.com.tr'nin /ilham-veren-fikirler/ altındaki %d rehber sayfası dönemde %s organik tık almıştır. Montaj, tamir ve temizlik yazıları sayfaların %s'ini oluşturup tıkların %s'ini almaktadır; tamir konusunda tek yazı (gömme rezervuar tamiri) %s tık ile üçüncü sıradadır. Dekorasyon, trend ve sürdürülebilirlik yazıları sayfaların %s'ini, tıkların %s'ini oluşturmaktadır. Kullanıcının sorunu çözmeye yönelik içerikleri daha çok tıkladığı ve bu alanın sitede en az işlenen başlık olduğu görülmektedir." % (
         TOP_N, k(TOP_T), yzd(prat_n), yzd(prat_t), bin(gt[1]), yzd(100 * (GS["dekor"][0] + GS["surd"][0]) / TOP_N), yzd(100 * (GS["dekor"][1] + GS["surd"][1]) / TOP_T)),
         "The %d guide pages under /ilham-veren-fikirler/ on vitra.com.tr received %s organic clicks in the period. Installation, repair and cleaning articles make up %s of pages and take %s of clicks; the only repair article (concealed cistern repair) ranks third with %s clicks. Decoration, trend and sustainability articles make up %s of pages and %s of clicks. Users click more on content that solves a problem, and this is the least developed topic on the site." % (
         TOP_N, k(TOP_T).replace(",", "."), ("%.1f" % prat_n) + "%", ("%.1f" % prat_t) + "%", f"{gt[1]:,}", ("%.1f" % (100 * (GS["dekor"][0] + GS["surd"][0]) / TOP_N)) + "%", ("%.1f" % (100 * (GS["dekor"][1] + GS["surd"][1]) / TOP_T)) + "%"), "D33"),
 x("Soru sorgularında sıra ve tık", "Position and clicks on question queries"),
 T_SO,
 insight("vitra.com.tr soru biçimli sorgularda ilk sayfada yer almaktadır: tablodaki %d sorgunun gösterim ağırlıklı ortalama sırası %s'dir. Buna karşın CTR %s seviyesinde kalmaktadır; klozet kapağı montajını soran 6 sorgu %s gösterime karşılık %s tık almıştır. Bu sorgularda cevabın sonuç sayfasında (AI Overview, PAA, video) verilmesi tık oranının düşük kalmasıyla ilişkilendirilebilir; kaynak gösterilen sayfa olmak bu sorgularda tık kadar önemli bir görünürlük biçimidir. Kapak tipine göre ayrışan sorgular (amortisörlü, üstten vidalı, eski tip, yavaş kapanan) her tip için ayrı cevap beklendiğini göstermektedir." % (
         len(SO), ("%.1f" % so_p).replace(".", ","), yzd(100 * so_c / so_i, 2), k(kap_i), bin(kap_c)),
         "vitra.com.tr appears on the first page for question-type queries: the impression-weighted average position of the %d queries in the table is %s. Yet CTR stays at %s; the 6 queries about fitting a WC seat received %s clicks against %s impressions. The low CTR can be associated with the answer being given on the results page itself (AI Overview, PAA, video); being the cited page is a form of visibility as important as the click for these queries. Queries that split by seat type (soft-close, top-fixing, old type) show that a separate answer is expected for each type." % (
         len(SO), "%.1f" % so_p, ("%.2f" % (100 * so_c / so_i)) + "%", f"{kap_c:,}", k(kap_i).replace(",", ".")), "D33"),
 x("AI Overview odaklı içerik planı: destek sayfaları ve rehber içerik", "AI Overview-focused content plan: support pages and guide content"),
 T_PLAN,
 marks([("up", "Sayfanın ilk paragrafında soruya 40-60 kelimelik doğrudan cevap, ardından numaralı adımlar", "A direct 40-60 word answer to the question in the page's first paragraph, followed by numbered steps"),
        ("up", "Model ve parça tipine göre ayrışan cevaplar ayrı başlıklarda: kapak tipi, rezervuar tipi, batarya tipi", "Answers that differ by model and part type under separate headings: seat type, cistern type, tap type"),
        ("up", "Ölçü, uyumluluk ve parça bilgisi görsel içinde değil, sayfada metin ve tablo olarak", "Size, compatibility and part information as text and tables on the page, not inside images"),
        ("up", "İlgili ürün, yedek parça, montaj hizmeti ve servis sayfalarına bağlantı; aynı konuda video varsa sayfaya gömülü", "Links to the related product, spare part, installation service and service pages; the video on the same topic embedded on the page"),
        ("up", "Güncelleme tarihi ve içeriği hazırlayan uzman bilgisi; yüksek trafikli mevcut yazıların (evye, duşakabin temizliği, gömme rezervuar tamiri) soru-cevap bölümüyle güncellenmesi", "An update date and information on the expert who prepared the content; updating the high-traffic existing articles (sinks, shower enclosure cleaning, concealed cistern repair) with a Q&A section")]),
 insight("Planın odağı, kullanıcının bir sorunu çözmek ya da karar vermek için sorduğu sorulardır: tamir, montaj, uyumluluk, ölçü ve karşılaştırma. Bu soruların bir bölümünde VitrA bugün AI Overview'da kaynak gösterilmektedir (klozet ölçüleri, en iyi klozet markası, pisuvar); iç takım, montaj ücreti, engelli klozeti ve seçim karşılaştırmalarında kaynaklar pazaryerleri, rakip markalar ve rehber sitelerdir. Destek sayfaları aynı zamanda Şikayetvar'da yoğunlaşan yedek parça, montaj ve garanti konularına satış sonrası bir başvuru noktası sağlayabilir.",
         "The plan focuses on the questions users ask to solve a problem or make a decision: repair, installation, compatibility, size and comparison. In some of these, VitrA is already cited in AI Overview today (WC dimensions, best WC brand, urinal); for inner mechanisms, installation fees, accessible WCs and selection comparisons the sources are marketplaces, competitor brands and guide sites. Support pages can also provide an after-sales reference point for the spare-part, installation and warranty topics concentrated on Şikayetvar.", "D19", "D24"),
 x("Marka ve entity tutarlılığı: Wikidata ve Wikipedia", "Brand and entity consistency: Wikidata and Wikipedia"),
 T_ENT,
 note("NOT", "NOTE", "<p>%s</p>" % x("Wikipedia'da marka adına yapılacak düzenlemeler, platformun çıkar çatışması kuralları gereği bağımsız yayınlara dayandırılmalı ve maddenin tartışma sayfası üzerinden önerilmelidir. Wikidata düzeltmeleri kaynak gösterilerek doğrudan yapılabilir.",
                                         "Edits on behalf of the brand on Wikipedia should, under the platform's conflict-of-interest rules, be based on independent publications and proposed via the article's talk page. Wikidata corrections can be made directly with sources.")),
 x("Site dışı sinyaller: Şikayetvar, YouTube ve rehber siteleri", "Off-site signals: Şikayetvar, YouTube and guide sites"),
 marks([("at", "Şikayetvar: VitrA puanı 18, son 1 yıl çözüm oranı %18; marka güvenilirliği sorularında yapay zeka yanıtları şikayet ve forum platformlarını kaynak gösterebilmektedir. Yedek parça, montaj ve garanti şikayetlerine standart yanıt ve ilgili destek sayfasına bağlantı verilmesi, çözülen kayıtların kapatılması değerlendirilebilir",
         "Şikayetvar: VitrA score 18, last-year resolution rate 18%; for brand reliability questions AI answers may cite complaint and forum platforms. A standard reply with a link to the related support page for spare-part, installation and warranty complaints, and closing resolved records, can be considered"),
        ("at", "YouTube: en çok izlenen 14 tamir ve kurulum konusunun hiçbirinde VitrA kanal videosu yok; \"gömme rezervuar iç takımı\" ve \"gömme rezervuar mı dış rezervuar mı\" AI Overview'larında YouTube kaynak gösterilmektedir. Destek sayfalarıyla aynı başlıklarda video serisi ve videoların ilgili sayfaya gömülmesi değerlendirilebilir",
         "YouTube: none of the 14 most-watched repair and installation topics has a VitrA channel video; YouTube is cited in the \"gömme rezervuar iç takımı\" and \"gömme rezervuar mı dış rezervuar mı\" AI Overviews. A video series under the same headings as the support pages, with the videos embedded on the related pages, can be considered"),
        ("up", "Rehber ve topluluk siteleri: AI Overview'da kaynak gösterilen içeriklerin bir bölümü markadan bağımsız rehber ve topluluk sitelerindedir. Bu sitelerde ölçü, seçim ve bakım konularında uzman içerik ve konuk yazı ile VitrA'nın kaynak olarak anılması değerlendirilebilir",
         "Guide and community sites: part of the content cited in AI Overview sits on guide and community sites independent of brands. Expert content and guest posts on size, selection and care topics on these sites, with VitrA cited as a source, can be considered")]),
 RANK_Y,
 x("AI ile alışveriş: ürün verisi ve llms.txt", "Shopping with AI: product data and llms.txt"),
 marks([("at", "Google Shopping'de VitrA sitesi listelemelerin %0,7'sini almakta ve 27 kategori kelimesinin 15'inde görünmemektedir. Google AI Mode ve ChatGPT alışveriş yanıtları ürün akışlarından ve ürün sayfası verisinden yararlanmaktadır; Merchant Center akışının tüm kategorileri kapsaması ve ölçü, renk, model kodu, uyumlu kapak ve iç takım, garanti süresi ve montaj hizmeti bilgisini taşıması değerlendirilebilir",
         "On Google Shopping the VitrA site takes 0.7% of listings and does not appear in 15 of 27 category keywords. Google AI Mode and ChatGPT shopping answers draw on product feeds and product page data; a Merchant Center feed covering all categories and carrying size, colour, model code, compatible seat and inner mechanism, warranty period and installation service information can be considered"),
        ("at", "Kategori sayfalarındaki kartların %71,1'i stoklu süzgeci dışındadır; stok ve fiyat bilgisinin ürün sayfası ile ürün akışında tutarlı olması, AI alışveriş yanıtlarında stokta olmayan ürünün önerilmesini sınırlayabilir",
         "71.1% of the cards on category pages fall outside the in-stock filter; consistent stock and price information on the product page and in the product feed can limit out-of-stock products being suggested in AI shopping answers"),
        ("up", "llms.txt yayında ve 83 bağlantı içermektedir; bunların 3'ü rehber içeriğe, 1'i destek sayfasına gitmektedir. Destek, montaj, yedek parça, garanti ve Artema bölümleriyle genişletilebilir. Sayfaların yapay zeka araçları için sade metin sürümleri gibi altyapı gerektiren düzenlemeler e-ticaret altyapısıyla birlikte ilerleyen dönemde değerlendirilebilir",
         "llms.txt is live and contains 83 links, 3 of which go to guide content and 1 to a support page. It can be expanded with support, installation, spare-part, warranty and Artema sections. Changes that need platform work, such as plain-text versions of pages for AI tools, can be assessed later together with the e-commerce platform"),
        ("at", "Rehber içerik site haritasında (sitemap-ilham.xml) 103 kaydın 2'si doldurulmamış şablon adresidir ve 1 adres iki kez yer almaktadır",
         "In the guide content sitemap (sitemap-ilham.xml), 2 of 103 entries are unfilled template addresses and 1 address appears twice")]),
 kaynak("Google Search Console · /ilham-veren-fikirler/ sayfaları ve soru sorguları, 1 Eki 2025 - 25 Eyl 2026 · Google arama sonuçları ve AI Overview, 109 kelime, 29.09.2026 · Wikidata ve Wikipedia, 02.10.2026 · vitra.com.tr llms.txt ve site haritaları, 02.10.2026 · Şikayetvar, YouTube ve Google Shopping verileri ilgili bölümlerdeki kaynaklardandır",
        "Google Search Console · /ilham-veren-fikirler/ pages and question queries, 1 Oct 2025 - 25 Sep 2026 · Google search results and AI Overview, 109 keywords, 29.09.2026 · Wikidata and Wikipedia, 02.10.2026 · vitra.com.tr llms.txt and sitemaps, 02.10.2026 · Şikayetvar, YouTube and Google Shopping data come from the sources of the related sections", "D33", "D19", "D34", "D35", "D24", "D20", "D25"),
)
