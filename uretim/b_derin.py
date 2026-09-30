# -*- coding: utf-8 -*-
"""Bolum: Pazaryeri alt kategori derinligi - cok satanlar, hedef disi kesitler, rakip magazalar (D29)."""
from ortak import *
import json, os
from urllib.parse import quote as _q
D = os.path.join(veri.V, "ham", "derin", "pazaryeri_derin")
def L(f): return [json.loads(l) for l in open(os.path.join(D, f), encoding="utf-8")]
TY = L("ty_kategori.jsonl"); HB = L("hb_kategori.jsonl"); AK = L("akakce_kategori.jsonl"); CI = L("cimri_kategori.jsonl"); RK = L("rakip_magaza_kategori.jsonl")
AD = {"klozet": ("Klozet", "WC"), "asma-klozet": ("Asma klozet", "Wall-hung WC"), "klozet-takimi": ("Klozet takımı", "Close-coupled WC"), "akilli-klozet": ("Akıllı klozet", "Smart WC"), "klozet-kapagi": ("Klozet kapağı", "Toilet seat"),
      "lavabo": ("Lavabo", "Washbasin"), "tezgah-ustu-lavabo": ("Tezgah üstü lavabo", "Countertop basin"), "tezgah-alti-lavabo": ("Tezgah altı lavabo", "Undercounter basin"), "lavabo-dolabi": ("Lavabo dolabı", "Washbasin unit"), "banyo-dolabi": ("Banyo dolabı", "Bathroom cabinet"),
      "boy-dolabi": ("Boy dolabı", "Tall cabinet"), "aynali-dolap": ("Aynalı dolap", "Mirror cabinet"), "gomme-rezervuar": ("Gömme rezervuar", "Concealed cistern"), "rezervuar-ic-takimi": ("Rezervuar iç takımı", "Cistern inner mechanism"), "lavabo-bataryasi": ("Lavabo bataryası", "Basin tap"),
      "banyo-bataryasi": ("Banyo bataryası", "Bath tap"), "ankastre-batarya": ("Ankastre batarya", "Concealed tap"), "dus-seti": ("Duş seti", "Shower set"), "dus-basligi": ("Duş başlığı", "Shower head"), "dusakabin": ("Duşakabin", "Shower enclosure"), "dus-teknesi": ("Duş teknesi", "Shower tray"),
      "kuvet": ("Küvet", "Bathtub"), "pisuvar": ("Pisuvar", "Urinal"), "bide": ("Bide", "Bidet"), "camasir-makinesi-dolabi": ("Çamaşır makinesi dolabı", "Washing machine cabinet"), "banyo-aynasi": ("Banyo aynası", "Bathroom mirror"), "ledli-ayna": ("Ledli ayna", "LED mirror"),
      "boy-aynasi": ("Boy aynası", "Full-length mirror"), "havlupan": ("Havlupan", "Towel radiator"), "banyo-aksesuar-seti": ("Banyo aksesuar seti", "Bathroom accessory set"), "banyo-rafi": ("Banyo rafı", "Bathroom shelf"), "taharet-musluk": ("Taharet musluğu", "Bidet valve"),
      "ara-musluk": ("Ara musluk", "Stop valve"), "sifon-gider": ("Sifon ve gider", "Trap and drain"), "evye": ("Evye", "Sinks"), "mutfak-bataryasi": ("Mutfak bataryası", "Kitchen tap"), "su-aritma": ("Su arıtma cihazı", "Water purifier"), "sofben": ("Şofben", "Water heater"),
      "termosifon": ("Termosifon", "Storage water heater"), "banyo-paspasi": ("Banyo paspası", "Bath mat"), "tutunma-bari": ("Tutunma barı", "Grab bar")}
UYUM = {"ara-musluk": "Yakın", "taharet-musluk": "Yakın", "sifon-gider": "Yakın", "mutfak-bataryasi": "Yakın", "camasir-makinesi-dolabi": "Yakın", "banyo-aynasi": "Yakın", "ledli-ayna": "Yakın", "havlupan": "Yakın", "banyo-aksesuar-seti": "Yakın", "tutunma-bari": "Yakın",
        "banyo-rafi": "Orta", "boy-aynasi": "Orta", "evye": "Orta", "su-aritma": "Uzak", "sofben": "Uzak", "termosifon": "Uzak", "banyo-paspasi": "Uzak"}
UYUM_EN = {"Yakın": "Close", "Orta": "Medium", "Uzak": "Distant"}
def ilk(lst, std):
    for r in lst:
        if r.get("std") == std: return r
    return None
def med(r): return cell(round(r["fiyat"]["med"])) if r and r.get("fiyat") and r["fiyat"].get("med") else n("-")
def vit(r):
    if not r: return n("-")
    a = r.get("vitra_adet", 0)
    if not a: return n("0")
    s = r.get("vitra_siralar") or []; yp = r.get("vitra_yorum_payi")
    return n("%d · %s · %s" % (a, ("%d." % min(s)) if s else "-", yzd(yp) if yp is not None else "-"))
HEDEF = [s for s in AD if any(r.get("std") == s and r.get("kapsam") == "hedef" for r in TY + HB)]
HDIS = [s for s in AD if s in UYUM]
rows = []
for s in HEDEF:
    t, h, a, c = ilk(TY, s), ilk(HB, s), ilk(AK, s), ilk(CI, s)
    isaret = "*" if any(r and r.get("saflik") is not None and r["saflik"] < 70 for r in (t, h)) else ""
    rows.append([x(AD[s][0] + isaret, AD[s][1] + isaret), med(t), med(h), med(a), med(c), vit(t), vit(h), n(yzd(h["platform_pay"])) if h and h.get("platform_pay") is not None else n("-")])
T1 = tablo([th("Hedef kategori", "Target category", "VitrA ürün gamındaki kategori; * çok satan listesine aksesuar karıştığı için fiyat bandının temsil gücü sınırlı.", "Category in VitrA's range; * accessories mixed into the best-seller list, so the price band is less representative."),
            th("Trendyol medyan", "Trendyol median", "Çok satan sıralamasında ilk 72 ürünün medyan fiyatı (TL), 30.09.2026.", "Median price (TL) of the first 72 products in best-seller order, 30.09.2026.", True),
            th("Hepsiburada medyan", "Hepsiburada median", "Çok satan ilk 72 ürünün medyan fiyatı (TL).", "Median price (TL) of the first 72 best sellers.", True),
            th("Akakçe medyan", "Akakçe median", "Popülerlik sırasında ilk 2 sayfanın en düşük fiyat medyanı (TL).", "Median of the lowest prices on the first 2 pages in popularity order (TL).", True),
            th("Cimri medyan", "Cimri median", "Popülerlik sırasında okunan ürünlerin en düşük fiyat medyanı (TL).", "Median of the lowest prices of the products read in popularity order (TL).", True),
            th("VitrA · Trendyol", "VitrA · Trendyol", "İlk 72 üründe VitrA ve Artema ürün sayısı · en iyi sıra · yorum payı.", "VitrA and Artema products in the first 72 · best rank · review share."),
            th("VitrA · Hepsiburada", "VitrA · Hepsiburada", "Aynı ölçü, Hepsiburada.", "Same measure, Hepsiburada."),
            th("HB platform satış payı", "HB platform sales share", "İlk 72 üründe Hepsiburada'nın kendi sattığı ürün payı.", "Share of the first 72 products sold by Hepsiburada itself.", True)], rows, "uzun")
rows2 = []
for s in HDIS:
    t, h = ilk(TY, s), ilk(HB, s)
    m1 = (t or {}).get("marka_adet_top5") or []
    rows2.append([x(AD[s][0], AD[s][1]), cell(t["toplam"]) if t and t.get("toplam") else n("-"), med(t), cell(t["toplam_yorum"]) if t else n("-"), cell(t["marka_sayisi"]) if t else n("-"), n(yzd(t["markasiz_pay"])) if t and t.get("markasiz_pay") is not None else n("-"),
                  veri_m("%s (%d)" % (m1[0]["ad"], m1[0]["adet"])) if m1 else n("-"), med(h), cell(h["toplam_yorum"]) if h else n("-"), vit(h), x(UYUM[s], UYUM_EN[UYUM[s]])])
T2 = tablo([th("Hedef dışı kategori", "Non-target category", "VitrA gamında bulunmayan ya da sınırlı bulunan bitişik kategori.", "Adjacent category absent or limited in VitrA's range."),
            th("TY ürün", "TY products", "Trendyol kategori toplam ürün sayısı.", "Total products in the Trendyol category.", True),
            th("TY medyan", "TY median", "Çok satan ilk 72 ürünün medyan fiyatı (TL).", "Median price (TL) of the first 72 best sellers.", True),
            th("TY yorum", "TY reviews", "İlk 72 ürünün toplam değerlendirme sayısı; hacmin göstergesi.", "Total reviews of the first 72 products; an indicator of volume.", True),
            th("Marka sayısı", "Brands", "İlk 72 üründeki farklı marka sayısı.", "Number of distinct brands in the first 72 products.", True),
            th("Markasız pay", "Unbranded share", "Marka adı olmayan (genel) ürünlerin payı.", "Share of unbranded (generic) products.", True),
            th("İlk marka (ürün)", "Top brand (products)", "Trendyol ilk 72'de en çok ürünü olan marka.", "Brand with the most products in the Trendyol first 72."),
            th("HB medyan", "HB median", "Hepsiburada çok satan ilk 72 medyan fiyatı (TL).", "Hepsiburada median price (TL) of the first 72 best sellers.", True),
            th("HB yorum", "HB reviews", "Hepsiburada ilk 72 toplam değerlendirme.", "Total reviews of the Hepsiburada first 72.", True),
            th("VitrA · HB", "VitrA · HB", "Hepsiburada ilk 72'de VitrA ve Artema: adet · en iyi sıra · yorum payı.", "VitrA and Artema in the Hepsiburada first 72: count · best rank · review share."),
            th("VitrA'ya uyum", "Fit with VitrA", "Ürün ailesi, üretim ve marka konumu açısından yakınlık: Yakın / Orta / Uzak (değerlendirme).", "Proximity in product family, manufacturing and brand position: Close / Medium / Far (assessment).")], rows2, "uzun")
SEC = ["klozet", "asma-klozet", "klozet-kapagi", "lavabo", "banyo-dolabi", "gomme-rezervuar", "rezervuar-ic-takimi", "lavabo-bataryasi", "banyo-bataryasi", "dusakabin", "camasir-makinesi-dolabi", "banyo-aynasi", "havlupan", "banyo-rafi", "mutfak-bataryasi"]
_UR = L("urunler.jsonl")
_URL = {(u_["kanal"], u_["kategori"], u_["sira"]): u_["url"] for u_ in _UR if u_.get("url")}
_AD = {(u_["kanal"], u_["ad"]): u_["url"] for u_ in _UR if u_.get("url")}
rows3 = []
for s in SEC:
    for kanal, lst in (("Trendyol", TY), ("Hepsiburada", HB)):
        r = ilk(lst, s)
        if not r or not r.get("en_cok_yorum10"): continue
        e = r["en_cok_yorum10"][0]
        _ara = _URL.get((kanal.lower(), r.get("kategori"), e[0])) or _URL.get((kanal.lower(), s, e[0])) or _AD.get((kanal.lower(), str(e[2]))) or \
               (("https://www.trendyol.com/sr?q=" if kanal == "Trendyol" else "https://www.hepsiburada.com/ara?q=") + _q("%s %s" % (e[1], str(e[2])[:60])))
        rows3.append([x(AD[s][0], AD[s][1]), veri_m(kanal), u(_ara, str(e[2])[:48]), u(_ara, str(e[1])[:22]), cell(round(e[3])) if e[3] else n("-"), cell(e[4]), n(("%.1f" % e[5]).replace(".", ",")) if e[5] else n("-")])
T3 = tablo([th("Kategori", "Category", "Kategori.", "Category."), th("Kanal", "Channel", "Pazaryeri.", "Marketplace."), th("En çok değerlendirilen ürün", "Most-reviewed product", "Çok satan ilk 72 ürün içinde değerlendirme sayısı en yüksek ürün.", "Product with the most reviews among the first 72 best sellers."),
            th("Marka", "Brand", "Ürünün markası; bağlantı ürün sayfasını yeni sekmede açar.", "Brand of the product; the link opens the product page in a new tab."), th("Fiyat (TL)", "Price (TL)", "Liste fiyatı, 30.09.2026.", "List price, 30.09.2026.", True), th("Değerlendirme sayısı", "Reviews", "Değerlendirme sayısı.", "Number of reviews.", True), th("Puan", "Rating", "Ortalama puan (5 üzerinden).", "Average rating (out of 5).", True)], rows3, "uzun")
MAG = ["Koçtaş", "Bauhaus", "Banyomarka", "Banyomega", "Banyoline", "Creavit (e-mağaza)"]
def rk(m, s):
    for r in RK:
        if r.get("magaza") == m and (r.get("std") or r.get("kategori")) == s: return r
    return None
def rkc(r):
    if not r: return n("-")
    m = r.get("fiyat", {}).get("med"); a = r.get("vitra_adet", 0); nn = r.get("n") or 0
    return n("%s · %d/%d" % (bin(round(m)) if m else "-", a, nn))
rows4 = [[x(AD[s][0], AD[s][1])] + [rkc(rk(m, s)) for m in MAG] for s in HEDEF if any(rk(m, s) for m in MAG)]
T4 = tablo([th("Hedef kategori", "Target category", "Kategori.", "Category.")] + [th(m, m, "Mağazanın kategori sayfasında okunan ürünlerin medyan fiyatı (TL) · VitrA ve Artema ürün sayısı / okunan ürün. Koçtaş çok satan sıralı, diğerleri varsayılan sıralama ilk sayfa; Creavit tek marka.", "Median price (TL) of the products read on the store's category page · VitrA and Artema products / products read. Koçtaş in best-seller order, others default order first page; Creavit single brand.", True) for m in MAG], rows4, "uzun")
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
<h3>%s</h3>
%s
%s
%s
%s
""" % (
 x("Trendyol (42 kategori), Hepsiburada (40), Akakçe (42 sayfa ve 8 VitrA marka sayfası) ve Cimri'de (30) çok satan ya da popülerlik sıralamasının ilk iki sayfası ile Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline ve Creavit e-mağazasının kategori sayfaları okunmuştur; toplam 9.000'den fazla pazaryeri ve 2.500'den fazla mağaza ürün satırı. Kategoriler VitrA'nın hedef gamı (SSG, rezervuar, mobilya, armatür, yıkanma) ve hedef dışı bitişik kesitler olarak ayrılmıştır. Değerlendirme sayısı satış hacminin yaklaşık göstergesidir; fiyatlar 30.09.2026 tarihli liste fiyatlarıdır. Kale fiyat göstermediği, IKEA TR ürün listesi vermediği için kapsam dışıdır.",
   "The first two pages of best-seller or popularity order on Trendyol (42 categories), Hepsiburada (40), Akakçe (42 pages and 8 VitrA brand pages) and Cimri (30) were read together with the category pages of Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline and the Creavit e-store; more than 9,000 marketplace and 2,500 store product rows in total. Categories are split into VitrA's target range (sanitaryware, cisterns, furniture, taps, bathing) and non-target adjacent segments. Review count is an approximate indicator of sales volume; prices are list prices of 30.09.2026. Kale shows no prices and IKEA TR gives no product list, so both are out of scope."),
 kpi_kart("0 / 7", "Duşakabinde VitrA ürünü bulunan kanal · küvette 0 / 5; Trendyol duşakabin yorumlarının %90,9'u Durul", "Channels with a VitrA product in shower enclosures · bathtubs 0 / 5; 90.9% of Trendyol shower enclosure reviews belong to Durul", "dn"),
 kpi_kart("%39,7", "Hepsiburada gömme rezervuar çok satanlarında VitrA yorum payı · ankastre bataryada Artema %70,9", "VitrA review share in Hepsiburada concealed cistern best sellers · Artema 70.9% in concealed taps", "up"),
 kpi_kart("%0,4", "Trendyol lavabo çok satanlarında VitrA yorum payı (1 ürün, 40. sıra) · Turkuaz %62,8", "VitrA review share in Trendyol washbasin best sellers (1 product, rank 40) · Turkuaz 62.8%", "dn"),
 kpi_kart(k(202768), "Trendyol banyo rafı ilk 72 ürünün toplam değerlendirmesi · medyan 248 TL; boy aynası 132K, paspas 70K", "Total reviews of the first 72 Trendyol bathroom shelf products · median 248 TL; full-length mirror 132K, mat 70K", "hi"),
 x("Hedef kategoriler: fiyat bandı ve VitrA'nın yeri", "Target categories: price band and VitrA's place"), T1,
 insight("Klozet ailesi, rezervuar ve pisuvar VitrA'nın pazaryerinde görünür olduğu kesitlerdir: Hepsiburada'da klozet listesinin 72 ürününün 17'si, iç takımın 20'si, gömme rezervuarın 18'i VitrA veya Artema'dır ve gömme rezervuarda yorum payı %39,7'ye ulaşmaktadır. Lavaboda tablo tersine dönmektedir: Trendyol'da 72 üründe 1 VitrA ürünü (40. sıra, yorum payı %0,4), Hepsiburada'da 1 ürün (61. sıra); Turkuaz iki kanalda da yorumların yaklaşık %62'sini almaktadır. Dolap ailesinde Trendyol banyo dolabı listesinde tek VitrA ürünü (68. sıra), Hepsiburada boy dolabında hiç ürün yoktur; lavabo dolabı ve aynalı dolapta 3'er ürünle yorum payı %24 civarındadır. Duşakabin ve küvette hiçbir kanalda VitrA ürünü bulunmamaktadır. Hepsiburada'nın kendi satışı lavaboda %59,7, klozette %45,8 iken duşakabin, küvet ve dolaplarda %0'dır.",
         "The WC family, cisterns and urinals are the segments where VitrA is visible on marketplaces: on Hepsiburada 17 of the 72 WC products, 20 of the inner-mechanism products and 18 of the concealed cistern products are VitrA or Artema, and the review share in concealed cisterns reaches 39.7%. In washbasins the picture reverses: 1 VitrA product among 72 on Trendyol (rank 40, review share 0.4%) and 1 on Hepsiburada (rank 61); Turkuaz takes about 62% of reviews on both. In the cabinet family the Trendyol bathroom cabinet list has a single VitrA product (rank 68) and Hepsiburada tall cabinets none; basin units and mirror cabinets have 3 products each with about 24% review share. No VitrA product exists in shower enclosures or bathtubs on any channel. Hepsiburada's own sales are 59.7% in washbasins and 45.8% in WCs but 0% in shower enclosures, bathtubs and cabinets.", "D29"),
 x("Hedef dışı kesitler: hacim, marka yoğunluğu ve VitrA'ya uyum", "Non-target segments: volume, brand density and fit with VitrA"), T2,
 insight("Yorum hacmi en yüksek hedef dışı kesitler Trendyol'da banyo rafı (202.768), boy aynası (132.368), banyo paspası (70.023), banyo aksesuar seti (69.138) ve mutfak bataryasıdır (53.076); bu kesitlerin medyan fiyatı 180 - 1.650 TL bandındadır, yani düşük fiyat ve yüksek adet. Aynalar, raflar ve aksesuar setlerinde markasız pay %0 - %4 ancak 22 - 46 farklı marka listelenmektedir; taharet musluğu, şofben, tutunma barı, sifon, mutfak bataryası ve ara muslukta markasız pay %12,5 - %19,4'tür. VitrA'nın mevcut ailesine yakın kesitler ara musluk ve mutfak bataryası (Hepsiburada'da Artema 72 ürünün 14'ü ve 13'ü ile ilk sırada), taharet musluğu, çamaşır makinesi dolabı (Trendyol 1.688 ürün, medyan 3.281 TL), banyo aynası, ledli ayna, havlupan ve aksesuar setidir. Şofben, termosifon, su arıtma ve paspas ürün ailesinin dışındadır; termosifonda Baymak ve Demirdöküm ağırlıklıdır.",
         "The non-target segments with the highest review volume on Trendyol are bathroom shelves (202,768), full-length mirrors (132,368), bath mats (70,023), accessory sets (69,138) and kitchen taps (53,076); their median price sits in the 180 - 1,650 TL band, meaning low price and high volume. In mirrors, shelves and accessory sets the unbranded share is 0% - 4% but 22 - 46 brands are listed; in bidet valves, water heaters, grab bars, traps, kitchen taps and stop valves the unbranded share is 12.5% - 19.4%. Segments close to VitrA's current family are stop valves and kitchen taps (on Hepsiburada Artema leads with 14 and 13 of 72 products), bidet valves, washing machine cabinets (Trendyol 1,688 products, median 3,281 TL), bathroom and LED mirrors, towel radiators and accessory sets. Water heaters, storage heaters, purifiers and mats are outside the product family; Baymak and Demirdöküm dominate storage heaters.", "D29"),
 x("En çok değerlendirilen ürünler", "Most-reviewed products"), T3,
 insight("En çok değerlendirilen ürünler kategoriye göre iki uçta toplanmaktadır: klozet, lavabo ve batarya listelerinde orta fiyatlı yerel markalar ve marka mağazaları (Turkuaz, Kale, Creavit, Durul, KUSTAR, VİOSA), hedef dışı kesitlerde ise düşük fiyatlı ve yüksek adetli ürünler (Trendyol banyo rafında 21.076 değerlendirmeli 233 TL'lik yapışkanlı raf). Akakçe ve Cimri'de satıcı sayısı medyanı lavabo bataryasında 26, banyo bataryasında 26,5 iken klozette 3, lavaboda 4, banyo dolabında 3'tür; fiyat rekabeti armatür ve klozet kapağında yoğun, seramik ve mobilyada seyrektir.",
         "The most-reviewed products cluster at two ends: mid-priced local brands and brand stores in WC, washbasin and tap lists (Turkuaz, Kale, Creavit, Durul, KUSTAR, VİOSA), and low-priced high-volume products in non-target segments (a 233 TL adhesive shelf with 21,076 reviews in Trendyol bathroom shelves). On Akakçe and Cimri the median seller count is 26 in basin taps and 26.5 in bath taps but 3 in WCs, 4 in washbasins and 3 in bathroom cabinets; price competition is intense in taps and toilet seats and sparse in ceramics and furniture.", "D29"),
 x("Rakip perakendeci ve marka mağazaları", "Competitor retailers and brand stores"), T4,
 insight("Koçtaş'ta çok satan ilk 48 ürünün tamamı Koçtaş satışlıdır; klozette Creavit 19, Kale 7, VitrA 4 ürünle yer almakta, yorum hacmi Kale ve Norm'da toplanmaktadır. VitrA'nın Koçtaş'ta öne çıktığı kesitler gömme rezervuar (17 ürün), iç takım (7 ürün) ve klozet kapağıdır (7 ürün); VitrA ve Artema fiyatı kategori medyanının klozette 1,66, lavaboda 1,99 katıdır. Bauhaus'ta klozet takımında ilk 24 ürünün 8'i VitrA, banyo dolabında VitrA Ora 25.990 TL ile medyanın 3,3 katında listelenmekte, duşakabin ve küvet listeleri Er-Duş markasındadır. Banyomarka VitrA ağırlıklı bir mağazadır: lavabo dolabı (32/32), boy dolabı (31), aynalı dolap (31) ve tezgah üstü lavabo (19) listeleri VitrA ile dolmaktadır; akıllı klozette Geberit, bataryada Grohe öndedir. Banyomega'da VitrA klozet kapağı (11) ve gömme rezervuarda (6) görünmekte, lavabo ve batarya kesitlerinde Duravit, Grohe ve Fontana öndedir. Banyoline'da VitrA klozet (16/24) ve asma klozet (18/24) listelerini doldururken lavaboda Turkuaz (24/24), dolapta Orka ve Denko yer almaktadır. Creavit e-mağazası tüm ürünleri liste fiyatının %35 - %50 altında indirimli göstermektedir.",
         "At Koçtaş all of the first 48 best sellers are sold by Koçtaş; in WCs Creavit has 19, Kale 7 and VitrA 4 products, with review volume concentrated in Kale and Norm. VitrA stands out at Koçtaş in concealed cisterns (17 products), inner mechanisms (7) and toilet seats (7); VitrA and Artema prices are 1.66 times the category median in WCs and 1.99 in washbasins. At Bauhaus 8 of the first 24 close-coupled WCs are VitrA, the VitrA Ora bathroom cabinet is listed at 25,990 TL, 3.3 times the median, and the shower enclosure and bathtub lists are Er-Duş. Banyomarka is a VitrA-heavy store: basin unit (32/32), tall cabinet (31), mirror cabinet (31) and countertop basin (19) lists are filled with VitrA; Geberit leads in smart WCs and Grohe in taps. At Banyomega VitrA appears in toilet seats (11) and concealed cisterns (6) while Duravit, Grohe and Fontana lead in washbasins and taps. At Banyoline VitrA fills the WC (16/24) and wall-hung WC (18/24) lists while Turkuaz fills washbasins (24/24) and Orka and Denko the cabinets. The Creavit e-store shows all products discounted 35% - 50% below list price.", "D29"),
 note("KISIT", "LIMITATION", ul_b([("Karışık listeler:", "Mixed lists:", "Trendyol ve Hepsiburada çok satan listelerinde klozet takımı ve dolap aramalarına paspas ve düzenleyici gibi yan ürünler karışmaktadır; bu kesitler * ile işaretlidir ve VitrA varlığı değerlendirilmemiştir.", "side products such as mats and organisers mix into WC set and cabinet searches on Trendyol and Hepsiburada; these segments are marked * and VitrA presence was not assessed."),
                                   ("Sıralama:", "Ordering:", "Koçtaş dışındaki mağazalarda çok satan sıralaması bulunmadığından varsayılan sıralamanın ilk sayfası okunmuştur; satış hacmini yansıtmayabilir. Hepsiburada kategori toplamı 10.000 ile sınırlı gösterilmektedir.", "stores other than Koçtaş have no best-seller order, so the first page of the default order was read; it may not reflect sales volume. Hepsiburada caps the category total at 10,000."),
                                   ("Doğrulanmayan:", "Unverified:", "Koçtaş ve Bauhaus'ta öne çıkan Norm, Housera, Roomart, Fly ve Penta markalarının mağaza özel markası olup olmadığı doğrulanamamıştır; Koçtaş'ta sifon ve mutfak bataryası okunmamıştır.", "whether Norm, Housera, Roomart, Fly and Penta at Koçtaş and Bauhaus are store private labels could not be verified; traps and kitchen taps were not read at Koçtaş.")])),
 kaynak("Trendyol, Hepsiburada, Akakçe ve Cimri kategori listeleri (ilk 2 sayfa) · Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline ve Creavit e-mağaza kategori sayfaları · Chrome · 30.09.2026", "Trendyol, Hepsiburada, Akakçe and Cimri category lists (first 2 pages) · Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline and Creavit e-store category pages · Chrome · 30.09.2026", "D29"),
)

from b_derin2 import EK as _EK
HTML = HTML + _EK
