# -*- coding: utf-8 -*-
"""Bolum: Marka ve uzman sitelerde kategori trafigi (Ahrefs)."""
from ortak import *
import json, os
D = os.path.join(veri.V, "ham", "derin", "ahrefs_markalar")
KPV = json.load(open(os.path.join(veri.V, "ham", "kp_ahrefs_degis.json"), encoding="utf-8"))["kelimeler"]   # Google Keyword Planner hacimleri
TEM = [("Klozet (asma, takım, set)", "WCs (wall-hung, close-coupled, sets)", 35054, "creavit.com.tr", 8537), ("Lavabo", "Washbasin", 20946, "creavit.com.tr", 4966), ("Batarya ve armatür", "Taps and fittings", 20329, "banyomarka.com", 10059),
       ("Duş seti, başlık, kolon", "Shower sets, heads, columns", 14634, "creavit.com.tr", 3484), ("Banyo dolabı / mobilya", "Bathroom cabinet / furniture", 12503, "balneom.com", 8812), ("Duşakabin", "Shower enclosure", 12007, "yapimanya.com", 597),
       ("Gömme rezervuar, kumanda paneli", "Concealed cisterns, flush plates", 9988, "banyomarka.com", 3012), ("Lavabo dolabı", "Washbasin unit", 8640, "creavit.com.tr", 4001), ("Banyo aksesuarı", "Bathroom accessories", 4538, "creavit.com.tr", 1001),
       ("Çamaşır makinesi dolabı", "Washing machine cabinet", 3487, "creavit.com.tr", 1499), ("Karo, seramik, fayans", "Tiles", 28950, "kale.com.tr", 59089), ("Klozet kapağı", "Toilet seat", 1647, "creavit.com.tr", 3199),
       ("Çanak lavabo", "Bowl washbasins", 2247, "creavit.com.tr", 3781), ("Taharet musluğu, el duşu", "Bidet valves, hand sprays", 469, "yapimanya.com", 850), ("Engelli ürünleri", "Accessible products", 261, "creavit.com.tr", 512),
       ("Yapı kimyasalı", "Building chemicals", 0, "kalekim.com", 20829), ("Parke, PVC, tavan kaplama", "Parquet, PVC, ceiling cladding", 0, "yerevdekor.com", 16908), ("Mutfak tezgahı", "Kitchen countertops", 0, "kale.com.tr", 9120),
       ("Mutfak evyesi (VitrA rehber yazısı)", "Kitchen sinks (VitrA guide article)", 2888, "banyomarka.com", 529), ("Çocuk klozet ve takımları", "Children's WCs and sets", 0, "banyomarka.com", 396)]
def durum(v, r):
    if not v: return '<span class="badge b-yok">%s</span>' % x("Trafik alan VitrA sayfası yok", "No VitrA page with traffic")
    return '<span class="badge %s">%s</span>' % (("b-var", x("VitrA önde", "VitrA ahead")) if v >= r else ("b-kis", x("Rakip önde", "Competitor ahead")))
T_TEM = tablo([th("Tema", "Theme", "Top pages sayfalarının URL ve en iyi kelimesine göre eşlendiği kategori teması.", "Category theme to which top pages were mapped by URL and top keyword."),
               th("vitra.com.tr", "vitra.com.tr", "Temaya eşlenen VitrA sayfalarının Ahrefs tahmini aylık organik trafiği.", "Ahrefs estimated monthly organic traffic of VitrA pages mapped to the theme.", True),
               th("En yüksek marka / uzman site rakibi", "Top brand / specialist competitor", "Temada en yüksek trafiği alan marka ya da uzman site; pazaryerleri ve yapı marketler karşılaştırmaya dahil değildir.", "Brand or specialist site with the highest traffic in the theme; marketplaces and DIY retailers are not included."),
               th("Rakip trafiği", "Competitor traffic", "Rakibin tema trafiği.", "Competitor's theme traffic.", True),
               th("Durum", "Status", "VitrA ile en yüksek marka / uzman site rakibinin karşılaştırması.", "Comparison of VitrA with the top brand / specialist competitor.")],
              [[x(a, b), cell(c) if c else n("-"), u("https://www." + d, d), cell(e), durum(c, e)] for a, b, c, d, e in sorted(TEM, key=lambda t_: -max(t_[2], t_[4]))], "uzun")
from grafik2 import sapma as _sp, f_kf, f_k as _fk, _EN as _GEN
def _ek(t): return _GEN.get(t, t)
_TF = sorted([t_ for t_ in TEM], key=lambda t_: -((t_[2] or 0) - t_[4]))
GFARK = _sp([(x(a, b), (c or 0) - e) for a, b, c, d, e in _TF], x("VitrA - rakip trafik farkı", "VitrA - competitor traffic gap"),
            x("Tema bazında VitrA ile en yüksek marka / uzman site rakibi arasındaki tahmini aylık organik trafik farkı · Ahrefs", "Estimated monthly organic traffic gap between VitrA and the top brand / specialist competitor by theme · Ahrefs"),
            bicim=f_kf, ek=[(x("vitra.com.tr", "vitra.com.tr"), [_fk(c or 0) for a, b, c, d, e in _TF]), (x("Rakip", "Competitor"), [x(d + " · " + _fk(e), d + " · " + _ek(_fk(e))) for a, b, c, d, e in _TF])])
BK = [("banyo dolabı", 60000, 24000, "5"), ("duşakabin", 59000, 5600, "4"), ("duş başlığı", 43000, 2000, "2"), ("klozet", 39000, 31000, "1"), ("taharet musluğu", 32000, 2200, "-"), ("lavabo", 28000, 18000, "1"),
      ("çamaşır makinesi dolabı", 27000, 4100, "3"), ("klozet kapağı", 27000, 11000, "6"), ("banyo bataryası", 24000, 8000, "3*"), ("banyo modelleri", 24000, 7700, "5"), ("dolap kulpu", 22000, 19000, "-"),
      ("duş seti", 17000, 18000, "5"), ("gömme rezervuar", 15000, 3300, "2"), ("klozet takımı", 10000, 9800, "3"), ("musluk başlığı", 11000, 6200, "-"), ("banyo aynası", 7500, 5600, "6")]
import serp_ozet as _SO
_SMR = {k_["keyword"]: ((k_.get("ranking_data") or {}).get("mobile") or {}).get("rank") for k_ in json.load(open(os.path.join(veri.V, "ham", "seomonitor", "kelimeler_2026-10-03.json"), encoding="utf-8"))}
_SOV = {r["kelime"]: r.get("vitra_sira") for r in _SO.TUM}
def _vs(k_):
    r_ = _SMR.get(k_) if k_ in _SMR else _SOV.get(k_); return str(r_) if r_ and r_ <= 20 else "-"
BK = [(a, KPV[a]["ort12"], c, _vs(a)) for a, b, c, d in BK]   # hacim: Keyword Planner Eyl 2025 - Agu 2026 ortalamasi; VitrA sirasi SEOmonitor 03.10.2026 (takip disinda 04.10.2026 Google gozlemi)
_BKD = {a: (b, d) for a, b, c, d in BK}
T_BK = tablo([th("Baş kelime", "Head keyword", "Kategori baş kelimesi.", "Category head keyword."),
              th("Aylık hacim", "Monthly volume", "Google Keyword Planner, Türkiye, Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Google Keyword Planner, Turkey, average monthly search volume September 2025 - August 2026.", True),
              th("Trafik potansiyeli", "Traffic potential", "Bu kelimede 1. sıradaki sayfanın tüm kelimelerinden aldığı tahmini aylık trafik (Ahrefs TP).", "Estimated monthly traffic the page ranking first receives from all its keywords (Ahrefs TP).", True),
              th("VitrA sırası", "VitrA position", "vitra.com.tr'nin Google TR mobil sırası: SEOmonitor günlük takibi (03.10.2026), takip dışı kelimelerde 04.10.2026 Google gözlemi; \"-\" ilk 20'de yok.", "vitra.com.tr's Google TR mobile position: SEOmonitor daily tracking (03.10.2026), Google observation of 04.10.2026 for untracked keywords; \"-\" not in the top 20.", True)],
             [[veri_m(a), cell(b), cell(c), n(d)] for a, b, c, d in sorted(BK, key=lambda t_: -t_[1])], "uzun")
REH = [("Mutfak lavabosu tıkanıklığı, lavabo kokusu", "Kitchen sink blockage, basin odour", "Creavit", 1862, ("Yok", "Not available"), 0),
       ("Banyo asma tavan seçimi", "Bathroom suspended ceiling choice", "Creavit", 640, ("Yok", "Not available"), 0),
       ("Fayans metrekare ve derz hesabı", "Tile square-metre and grout calculation", "Kalekim", 3991, ("Karo nasıl döşenir rehberi", "How to lay tiles guide"), 24),
       ("Hilton lavabo nedir", "What is a Hilton basin", "Kale", 780, ("Rehber yok; kategori sayfası 1.878", "No guide; category page 1,878"), 0),
       ("Lavabo ölçüleri ve yüksekliği", "Washbasin dimensions and height", "Kale", 480, ("Lavabo seçim rehberi", "Washbasin selection guide"), 117),
       ("Klozet temizliği", "WC cleaning", "Banyomega, Kale", 571, ("Yok", "Not available"), 0),
       ("Asma klozet ve rezervuar su kaçırma", "Wall-hung WC and cistern leaks", "Banyomarka, Banyomega", 545, ("Gömme rezervuar tamiri rehberi", "Concealed cistern repair guide"), 834),
       ("Duş süzgeci mi duş kanalı mı", "Shower drain or shower channel", "Creavit", 326, ("Rehber yok; kategori sayfası 2.246", "No guide; category page 2,246"), 0),
       ("Klozet kapağı montajı", "Toilet seat installation", "Kale, Creavit", 776, ("Klozet kapağı montaj rehberi", "Toilet seat installation guide"), 1265)]
T_REH = tablo([th("Rehber konusu", "Guide topic", "Rakiplerin rehber sayfalarından organik trafik aldığı konu.", "Topic from which competitors' guide pages receive organic traffic."),
               th("Rakip", "Competitor", "Konuda trafik alan rakip siteler.", "Competitor sites receiving traffic on the topic."),
               th("Rakip trafiği", "Competitor traffic", "Rakip rehber sayfalarının toplam Ahrefs tahmini aylık organik trafiği.", "Total Ahrefs estimated monthly organic traffic of the competitor guide pages.", True),
               th("VitrA sayfası", "VitrA page", "vitra.com.tr /ilham-veren-fikirler içindeki karşılık.", "Counterpart in vitra.com.tr /ilham-veren-fikirler."),
               th("VitrA trafiği", "VitrA traffic", "VitrA rehber sayfasının Ahrefs tahmini aylık organik trafiği.", "Ahrefs estimated monthly organic traffic of the VitrA guide page.", True)],
              [[x(a, b), veri_m(c), cell(d), x(*e), cell(f) if f else n("-")] for a, b, c, d, e, f in REH])
MK = [("vitra", "VitrA"), ("artema", "Artema"), ("kale", "Kale *"), ("kale banyo", "Kale banyo"), ("eca", "E.C.A. **"), ("bien", "Bien"), ("bocchi", "Bocchi"), ("creavit", "Creavit"),
      ("grohe", "Grohe"), ("geberit", "Geberit"), ("hansgrohe", "Hansgrohe"), ("turkuaz seramik", "Turkuaz Seramik"), ("duravit", "Duravit"), ("visam", "Visam"), ("serel", "Serel"),
      ("banyomarka", "Banyomarka"), ("ikea banyo", "IKEA banyo"), ("banyomega", "Banyomega"), ("banyoline", "Banyoline"), ("bauhaus banyo", "Bauhaus banyo")]
SEOM = {"kale", "creavit", "banyomarka", "ikea banyo", "bauhaus banyo", "banyomega", "banyoline"}   # SEOmonitor kampanyasinda dogrudan rakip olarak tanimli
def chg(v):
    s_ = [v["seri"][a] or 0 for a in sorted(v["seri"])]
    return (sum(s_[12:24]) / sum(s_[:12]) - 1) * 100 if len(s_) >= 24 and sum(s_[:12]) else None
def _mad(a, b):
    return x(b + (" · SEOmonitor rakibi" if a in SEOM else ""), b + (" · SEOmonitor competitor" if a in SEOM else ""))
T_MK = tablo([th("Marka araması", "Brand search", "Aranan marka ifadesi; \"SEOmonitor rakibi\" etiketi kampanyada doğrudan rakip olarak tanımlı siteleri gösterir. Perakendecilerde banyo ile birlikte yapılan aramalar alınmıştır.", "Brand phrase searched; the \"SEOmonitor competitor\" label marks sites defined as direct competitors in the campaign. For retailers, searches combined with bathroom were used."),
              th("Aylık hacim", "Monthly volume", "Google Keyword Planner, Türkiye, Eylül 2025 - Ağustos 2026 aylık ortalama arama hacmi.", "Google Keyword Planner, Turkey, average monthly search volume September 2025 - August 2026.", True),
              th("Son 12 ay / önceki 12 ay", "Last 12 months / previous 12", "Eylül 2025 - Ağustos 2026 ile Eylül 2024 - Ağustos 2025 aylık arama toplamlarının değişimi (Google Keyword Planner).", "Change between the monthly search totals of Sep 2025 - Aug 2026 and Sep 2024 - Aug 2025 (Google Keyword Planner).", True)],
             [[_mad(a, b), cell(KPV[a]["ort12"] or 0), n(yz(chg(KPV[a])))] for a, b in sorted(MK, key=lambda t_: -(KPV.get(t_[0], {}).get("ort12") or 0)) if a in KPV])
_V = KPV["vitra"]; _MT = KPV["mutfak tezgahı"]["ort12"] if "mutfak tezgahı" in KPV else None
def _yuz(a): return yz(chg(KPV[a]))
HTML = """
<p class="lede">%s</p>
<div class="kpis">%s%s%s%s</div>
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div>%s</div></div>
%s
""" % (
 x("Marka ve uzman e-ticaret sitelerinin (Kale, Creavit, E.C.A., Geberit, Duravit, Banyomarka, Banyoline, Yapımanya, Yerevdekor, Balneom, Kalekim, seramik markaları ve diğerleri) en yüksek trafikli sayfaları Ahrefs ile çekilmiş, kategori temalarına eşlenmiş ve vitra.com.tr ile karşılaştırılmıştır. Değerler Ahrefs tahmini aylık organik trafiktir; listelenen sayfalar site toplamının çoğunlukla %66-93'ünü kapsamaktadır (Turkuaz'da %45).",
   "The highest-traffic pages of brand and specialist e-commerce sites (Kale, Creavit, E.C.A., Geberit, Duravit, Banyomarka, Banyoline, Yapımanya, Yerevdekor, Balneom, Kalekim, tile brands and others) were pulled with Ahrefs, mapped to category themes and compared with vitra.com.tr. Values are Ahrefs estimated monthly organic traffic; the listed pages mostly cover 66-93% of each site's total (45% for Turkuaz)."),
 kpi_kart(k(330499), "vitra.com.tr tahmini aylık organik trafik · marka siteleri arasında en yüksek", "vitra.com.tr estimated monthly organic traffic · highest among brand sites", "up"),
 kpi_kart("4x", "Klozet temasında VitrA'nın organik trafiği en yakın rakibin (Creavit) yaklaşık 4 katı", "VitrA's organic traffic in the WC theme is about 4 times that of the nearest competitor (Creavit)", "up"),
 kpi_kart("2x", "Karo temasında Kale'nin organik trafiği VitrA'nın yaklaşık 2 katı", "In the tile theme Kale's organic traffic is about 2 times VitrA's", "dn"),
 kpi_kart("%8,0", "Banyomarka'nın en yüksek trafikli 90 sayfasında VitrA ve Artema ürün sayfalarının payı (2,5K / 32,0K)", "Share of VitrA and Artema product pages in Banyomarka's 90 highest-traffic pages (2.5K / 32.0K)", "hi"),
 x("Tema bazında VitrA ve en yüksek rakip", "VitrA and top competitor by theme"),
 GFARK + T_TEM,
 insight("VitrA sıhhi tesisat ve armatürün ana temalarında, yani klozet (35.054, Creavit 8.537), lavabo (20.946), batarya (20.329, Banyomarka 10.059), duş seti (14.634) ve duşakabinde (12.007) marka siteleri arasında belirgin farkla öndedir. Rakibin önde olduğu temalar iki gruptadır. İlk grupta VitrA'nın sayfası bulunmakla birlikte karo (Kale 59.089 / VitrA 28.950), klozet kapağı ve çanak lavabo (Creavit), taharet musluğu (Yapımanya) ve engelli ürünlerinde (Creavit) rakip daha fazla trafik almaktadır. İkinci grupta VitrA'nın sayfası hiç bulunmamaktadır: yapı kimyasalı (Kalekim 20.829), parke ve tavan kaplama (Yerevdekor 16.908), mutfak tezgahı (Kale 9.120; \"mutfak tezgahı\" baş kelimesi aylık 24.242 arama), çocuk klozet; bu temada VitrA'nın sınırlı ürünü bulunmakla birlikte trafik alan bir sayfası yoktur. Evyede VitrA'nın kategori sayfası trafik almamakta, \"En kullanışlı evye hangisi\" rehberi ise aylık yaklaşık 2.900 tahmini trafik almaktadır (Banyomarka 529). Banyomarka'nın en yüksek trafikli 90 sayfasının trafiğinin %8,0'i VitrA ve Artema ürün sayfalarından, Banyoline'ın 29 sayfasınınkinin %1,7'si VitrA ve Artema kategori ve marka sayfalarından gelmektedir.",
         "VitrA leads the brand sites by a clear margin in the main plumbing and tap themes: WCs (35,054, Creavit 8,537), washbasins (20,946), taps (20,329, Banyomarka 10,059), shower sets (14,634) and shower enclosures (12,007). Themes where a competitor leads fall into two groups. In the first, VitrA has a page but the competitor receives more traffic: tiles (Kale 59,089 / VitrA 28,950), toilet seats and bowl washbasins (Creavit), bidet valves (Yapımanya), accessible products (Creavit). In the second, VitrA has no page at all: building chemicals (Kalekim 20,829), parquet and ceiling cladding (Yerevdekor 16,908), kitchen countertops (Kale 9,120; the head keyword \"mutfak tezgahı\" has 24,242 monthly searches), children's WCs; in this theme VitrA has a limited range but no page receiving traffic. In sinks VitrA's category page receives no traffic, while the guide \"En kullanışlı evye hangisi\" (which sink is most practical) receives about 2,900 estimated monthly visits (Banyomarka 529). 8.0% of the traffic of Banyomarka's 90 highest-traffic pages comes from VitrA and Artema product pages, and 1.7% of that of Banyoline's 29 pages from VitrA and Artema category and brand pages.", "D18"),
 x("Kategori baş kelimeleri: hacim, potansiyel ve VitrA sırası", "Category head keywords: volume, potential and VitrA position"),
 T_BK,
 insight(("VitrA'nın ilk 3 dışında kaldığı yüksek hacimli baş kelimeler %s; %s aramalarında ise VitrA ilk 20'de değildir. Banyo dolabı, duşakabin, banyo bataryası ve gömme rezervuar gibi büyük kelimelerde VitrA ilk 3'tedir." % (
             " ve ".join("%s (aylık %s, %s. sıra)" % (a, bin(b), d) for a, b, c, d in sorted(BK, key=lambda t_: -t_[1]) if d != "-" and int(d) > 3), ", ".join(a for a, b, c, d in sorted(BK, key=lambda t_: -t_[1]) if d == "-")))
         + " Ahrefs'in Türkiye'de incelenen 69 baş kelimenin 65'inde KD değerini 0-2 göstermesi ve DR 1-16 aralığındaki sitelerin ilk 10'da yer alması, sıralamanın alan adı gücünden çok sayfa kurgusuyla belirlendiğine işaret etmektedir.",
         ("High-volume head keywords where VitrA is outside the top 3 are %s; in %s VitrA is not in the top 20. In large keywords such as bathroom cabinet, shower enclosure, bath taps and concealed cistern VitrA is in the top 3." % (
             " and ".join("%s (%s a month, position %s)" % (a, f"{b:,}", d) for a, b, c, d in sorted(BK, key=lambda t_: -t_[1]) if d != "-" and int(d) > 3), ", ".join(a for a, b, c, d in sorted(BK, key=lambda t_: -t_[1]) if d == "-")))
         + " Ahrefs shows KD 0-2 for 65 of the 69 head keywords reviewed in Turkey and sites with DR 1-16 rank in the top 10, which indicates that rankings are determined more by page setup than by domain strength.", "D18", "D42", "D19"),
 x("Rehber içerik: rakiplerin trafik aldığı konular", "Guide content: topics bringing competitors traffic"),
 T_REH,
 insight("VitrA'nın " + u("https://www.vitra.com.tr/ilham-veren-fikirler", "/ilham-veren-fikirler") + " bölümü 14.613 aylık trafikle rakip rehberlerin (Creavit 5.783, Kale 4.711) üzerindedir ve klozet kapağı montajında rakipleri geçmektedir. Buna karşın bakım ve arıza giderme (tıkanıklık, koku, temizlik) ile uygulama hesapları (derz) konularında rakipler trafik almakta, VitrA'nın karşılığı bulunmamaktadır; su kaçırmada VitrA'nın gömme rezervuar tamiri rehberi rakibin üzerindedir, fayans hesabında karşılığı sınırlıdır. Bu konuların yedek parça ve bakım ürünlerine yönlendiren giriş sayfaları olarak değerlendirilmesi fayda sağlayabilir.",
         "VitrA's " + u("https://www.vitra.com.tr/ilham-veren-fikirler", "/ilham-veren-fikirler") + " section, at 14,613 monthly visits, is ahead of competitor guides (Creavit 5,783, Kale 4,711) and outperforms competitors on toilet seat installation. Competitors, however, receive traffic on maintenance and troubleshooting (blockage, odour, cleaning) and application calculations (grout), where VitrA has no counterpart; on leaks VitrA's concealed cistern repair guide is ahead of the competitor, and on tile calculations its counterpart is limited. These topics could serve as entry pages that direct users to spare-part and maintenance products.", "D18"),
 x("Marka arama talebi", "Brand search demand"), T_MK,
 note("OKUMA", "READING", ul_b([("\"vitra\" aylık %s arama:" % bin(_V["ort12"]), "\"vitra\" %s monthly searches:" % f"{_V['ort12']:,}", "Karışık anlamlı \"kale\" ve \"eca\" dışında banyo markası aramaları arasında en yüksek hacimdir; son 12 ayda önceki 12 aya göre %s değişmiştir." % _yuz("vitra"), "excluding the ambiguous \"kale\" and \"eca\", the highest volume among bathroom brand searches; it changed %s in the last 12 months versus the previous 12." % _yuz("vitra")),
                                 ("* \"kale\" hacmi karışık:", "* \"kale\" volume is mixed:", "karo, yapı kimyasalı ve Kale Grubu'nun diğer işleri de dahildir; banyo karşılaştırması için \"kale banyo\" satırı daha yakındır.", "it includes tiles, building chemicals and other Kale Group businesses; the \"kale banyo\" row is closer for a bathroom comparison."),
                                 ("** \"eca\" hacmi karışık:", "** \"eca\" volume is mixed:", "önemli bölümü kombi ve klima aramalarından gelmektedir.", "a large part comes from boiler and air-conditioning searches."),
                                 ("Artan markalar:", "Growing brands:", "Creavit (%s), Turkuaz Seramik (%s), Bocchi (%s), Geberit (%s) ve Visam (%s) aramaları son 12 ayda belirgin biçimde artmıştır; Hansgrohe (%s) hafif gerilemiştir." % tuple(_yuz(k_) for k_ in ("creavit", "turkuaz seramik", "bocchi", "geberit", "visam", "hansgrohe")),
                                  "searches for Creavit (%s), Turkuaz Seramik (%s), Bocchi (%s), Geberit (%s) and Visam (%s) grew markedly in the last 12 months; Hansgrohe (%s) declined slightly." % tuple(_yuz(k_) for k_ in ("creavit", "turkuaz seramik", "bocchi", "geberit", "visam", "hansgrohe"))),
                                 ("Perakendeciler:", "Retailers:", "SEOmonitor'de doğrudan rakip olarak tanımlı Banyomarka (%s) marka aramalarını büyütürken Banyoline (%s) ve \"ikea banyo\" (%s) gerilemektedir." % (_yuz("banyomarka"), _yuz("banyoline"), _yuz("ikea banyo")),
                                  "Banyomarka (%s), defined as a direct competitor in SEOmonitor, is growing its brand searches while Banyoline (%s) and \"ikea banyo\" (%s) are declining." % (_yuz("banyomarka"), _yuz("banyoline"), _yuz("ikea banyo")))])),
 kaynak("Ahrefs Site Explorer top pages (TR, 28.09.2026; trafik tahmini) · arama hacimleri Google Keyword Planner (TR, Eyl 2024 - Ağu 2026) · SEOmonitor rakip listesi · Google TR mobil sonuç sayfası (29.09.2026)", "Ahrefs Site Explorer top pages (TR, 28.09.2026; traffic estimates) · search volumes Google Keyword Planner (TR, Sep 2024 - Aug 2026) · SEOmonitor competitor list · Google TR mobile results page (29.09.2026)", "D18", "D19"),
)
