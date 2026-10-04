# -*- coding: utf-8 -*-
"""Fiyat bolumu ek: Trendyol ve Hepsiburada cok satan listeleri, VitrA urunlerinde kanal fiyat farki (D26)."""
from ortak import *
import csv, json, os
D = os.path.join(veri.V, "ham", "derin", "pazaryeri_fiyat")
CS = json.load(open(os.path.join(D, "cok_satan_ozet.json"), encoding="utf-8"))
UF = list(csv.DictReader(open(os.path.join(D, "urun_fiyat.csv"), encoding="utf-8-sig")))
AN = json.load(open(os.path.join(D, "analiz.json"), encoding="utf-8"))["kanal_fiyat"]
KAT = [("klozet", "Klozet", "WC"), ("klozet_kapagi", "Klozet kapağı", "Toilet seat"), ("lavabo", "Lavabo", "Washbasin"), ("banyo_dolabi", "Banyo dolabı", "Bathroom cabinet"), ("camasir_makinesi_dolabi", "Çamaşır makinesi dolabı", "Washing machine cabinet"),
       ("dusakabin", "Duşakabin", "Shower enclosure"), ("banyo_bataryasi", "Banyo bataryası", "Bath tap"), ("lavabo_bataryasi", "Lavabo bataryası", "Basin tap"), ("dus_seti", "Duş seti", "Shower set"), ("taharet_musluk", "Taharet / ara musluk", "Bidet / stop valve"),
       ("rezervuar_ic_takim", "Rezervuar iç takımı", "Cistern inner mechanism"), ("gomme_rezervuar", "Gömme rezervuar", "Concealed cistern"), ("banyo_aynasi", "Banyo aynası", "Bathroom mirror"), ("banyo_aksesuar_seti", "Banyo aksesuar seti", "Bathroom accessory set")]
def K(kanal, k): 
    d = CS[kanal]
    for anahtar in (k, k.replace("_", "-"), k.replace("taharet_musluk", "taharet_musluğu")):
        if anahtar in d: return d[anahtar]
    return None
def cs_sat(k, tr, en):
    t, h = K("ty", k), K("hb", k)
    def payf(d): 
        if not d: return n("-")
        m = d["marka_ilk"][0]; return veri_m("%s %%%s" % (m[0].replace("Markasız (Genel Markalar)", "Markasız"), ("%.1f" % m[3]).replace(".", ",")))
    def tp(d): return n("%d / %d" % (d["satici_tipi"].get("3P", 0), d["n"])) if d else n("-")
    def vit(d): return n("%d · %%%s" % (d["vitra_urun"], ("%.1f" % d["vitra_degerlendirme_payi"]).replace(".", ","))) if d and d["vitra_urun"] else n("-")
    return [x(tr, en), cell(t["medyan_fiyat"]) if t else n("-"), cell(h["medyan_fiyat"]) if h else n("-"), tp(t), tp(h), payf(t), payf(h), vit(t), vit(h)]
T_CS2 = tablo([th("Kategori", "Category", "Pazaryerinde \"çok satan\" sıralamasının ilk 36 ürünü; 29.09.2026.", "First 36 products of the marketplace \"best seller\" ranking; 29.09.2026."),
               th("Trendyol medyan (TL)", "Trendyol median (TL)", "Trendyol ilk 36 ürünün medyan fiyatı.", "Median price of the first 36 Trendyol products.", True),
               th("Hepsiburada medyan (TL)", "Hepsiburada median (TL)", "Hepsiburada ilk 36 ürünün medyan fiyatı; dört kategoride arama sonucu kullanıldığı için aksesuar ağırlıklıdır.", "Median price of the first 36 Hepsiburada products; search results were used in four categories, so accessory-heavy.", True),
               th("Trendyol üçüncü taraf / 36", "Trendyol third-party / 36", "Trendyol'da üçüncü taraf satıcı listelemesi sayısı.", "Number of third-party seller listings on Trendyol.", True),
               th("Hepsiburada üçüncü taraf / 36", "Hepsiburada third-party / 36", "Hepsiburada'da üçüncü taraf satıcı listelemesi; kalan marka mağazası ve Hepsiburada'nın kendi satışıdır.", "Third-party seller listings on Hepsiburada; the rest are brand stores and Hepsiburada's own sales.", True),
               th("Trendyol en yüksek değerlendirme payı", "Trendyol top review share", "Trendyol ilk 36'da değerlendirme sayısı payı en yüksek marka.", "Brand with the highest review count share in the Trendyol top 36."),
               th("Hepsiburada en yüksek değerlendirme payı", "Hepsiburada top review share", "Hepsiburada ilk 36'da değerlendirme payı en yüksek marka.", "Brand with the highest review share in the Hepsiburada top 36."),
               th("VitrA + Artema TY", "VitrA + Artema TY", "İlk 36'daki VitrA ve Artema ürün sayısı ve değerlendirme payı; \"-\" yer almıyor.", "Number of VitrA and Artema products in the top 36 and review share; \"-\" not present.", True),
               th("VitrA + Artema HB", "VitrA + Artema HB", "Aynı ölçü, Hepsiburada.", "Same measure, Hepsiburada.", True)],
              [cs_sat(k, a, b) for k, a, b in KAT], "uzun")
GRUP_EN = {"Asma klozet": "Wall-hung WC", "Lavabo": "Washbasin", "Banyo mobilyası (lavabo dolabı)": "Bathroom furniture (basin unit)", "Banyo mobilyası (boy dolabı)": "Bathroom furniture (tall cabinet)", "Armatür (lavabo bataryası)": "Tap (basin)", "Armatür (banyo bataryası)": "Tap (bath)",
           "Armatür (termostatik batarya)": "Tap (thermostatic)", "Armatür (ara musluk)": "Tap (stop valve)", "Armatür (çamaşır musluğu)": "Tap (washing machine valve)", "Duş seti": "Shower set", "Gömme rezervuar seti": "Concealed cistern set", "Klozet kapağı": "Toilet seat", "İç takım": "Inner mechanism", "Klozet (takım)": "WC (close-coupled)"}
KANAL_EN = {"vitra.com.tr": "vitra.com.tr", "tek kanal": "single channel", "Koçtaş": "Koçtaş"}
def kanal_x(s):
    if s in KANAL_EN: return x(s, KANAL_EN[s])
    return veri_m(s)
def f(v): return cell(round(float(v))) if v not in ("", None) else n("-")
def sat(v, s): return n("%s (%s)" % (bin(round(float(v))), s)) if v not in ("", None) else n("-")
rows = []
for r in UF:
    rows.append([u(r["vitra_url"], r["urun"]) if r.get("vitra_url") else veri_m(r["urun"]), veri_m(r["kod"]), x(r["grup"], GRUP_EN.get(r["grup"], r["grup"])), f(r["vitra_com_tr"]), f(r["ty_vitra_magazasi"]), sat(r["ty_en_dusuk_3p"], r["ty_satici_adi"]) if r["ty_en_dusuk_3p"] else n("-"),
                 sat(r["hb_buybox"], r["hb_satici"]) if r["hb_buybox"] else n("-"), f(r["koctas"]), kanal_x(r["en_ucuz_kanal"]), n(("%%%s" % r["fark_yuzde"].replace(".", ",")) if r["fark_yuzde"] not in ("", "0.0") else ("-" if r["en_ucuz_kanal"] == "tek kanal" else "%0")), x("stokta", "in stock") if r["vitra_stok"] == "stokta" else x("stokta yok", "out of stock")])
T_KF = tablo([th("Ürün", "Product", "vitra.com.tr ürün sayfası; bağlantı canlı sayfaya gider.", "vitra.com.tr product page; the link opens the live page."), th("Kod", "Code", "Ürün kodu (SKU); eşleşme başlıkta kod geçen listelemelerle yapılmıştır.", "Product code (SKU); matching was done with listings carrying the code in the title."),
              th("Grup", "Group", "Ürün grubu.", "Product group."), th("vitra.com.tr", "vitra.com.tr", "Ürün sayfasındaki liste fiyatı (TL); sepette %10-15 ek indirim etiketi ayrıca vardır.", "List price on the product page (TL); an additional 10-15% basket discount label exists separately.", True),
              th("Trendyol VitrA mağazası", "Trendyol VitrA store", "Trendyol'daki VitrA mağazasının liste fiyatı; \"-\" listelenmemiş.", "List price of the VitrA store on Trendyol; \"-\" not listed.", True),
              th("Trendyol en düşük 3P (satıcı)", "Trendyol lowest 3P (seller)", "Trendyol'da üçüncü taraf satıcıların en düşük fiyatı ve satıcı adı.", "Lowest third-party seller price on Trendyol and the seller name.", True),
              th("Hepsiburada buybox (satıcı)", "Hepsiburada buybox (seller)", "Hepsiburada'da \"sepete ekle\" düğmesini kazanan satıcının fiyatı.", "Price of the seller winning the \"add to basket\" button on Hepsiburada.", True),
              th("Koçtaş", "Koçtaş", "Koçtaş'taki fiyat; 16 eşleşmenin tamamı üçüncü taraf satıcı listelemesidir.", "Price at Koçtaş; all 16 matches are third-party seller listings.", True),
              th("En ucuz kanal", "Cheapest channel", "Liste fiyatı en düşük kanal.", "Channel with the lowest list price."), th("Fark", "Gap", "vitra.com.tr liste fiyatından en ucuz kanala düşüş oranı; pozitif değer, kanalın vitra.com.tr'den daha ucuz olduğunu gösterir.", "Reduction from the vitra.com.tr list price to the cheapest channel.", True),
              th("vitra.com.tr stok", "vitra.com.tr stock", "Gözlem anında ürün sayfasındaki stok durumu.", "Stock status on the product page at the time of observation.")], rows, "uzun")
import statistics as _st
_UC = [r for r in UF if r["en_ucuz_kanal"] not in ("vitra.com.tr", "tek kanal")]
_FM = _st.median(float(r["fark_yuzde"]) for r in _UC)
_SY = sum(1 for r in UF if r["vitra_stok"] == "stokta yok")
KPI_KF = '<div class="kpis">%s%s%s</div>' % (
    kpi_kart("%d / %d" % (len(_UC), len(UF)), "En ucuz fiyatın vitra.com.tr dışındaki bir kanalda bulunduğu ürün · 29.09.2026", "Products whose cheapest price is in a channel other than vitra.com.tr · 29.09.2026", "hi"),
    kpi_kart(yzd(_FM), "Bu ürünlerde vitra.com.tr liste fiyatı ile en ucuz kanal arasındaki fark medyanı", "Median gap between the vitra.com.tr list price and the cheapest channel for these products", "dn"),
    kpi_kart("%d / %d" % (_SY, len(UF)), "Gözlem anında vitra.com.tr ürün sayfasında stokta olmayan ürün", "Products out of stock on the vitra.com.tr product page at the time of observation", "dn"))
GF = [("Armatür", "Taps", 8, "%29,8"), ("Klozet kapağı", "Toilet seat", 3, "%27,2"), ("İç takım", "Inner mechanism", 1, "%24,7"), ("Duş seti", "Shower set", 1, "%18,9"), ("Gömme rezervuar seti", "Concealed cistern set", 3, "%18,5"), ("Lavabo", "Washbasin", 2, "%3,6"), ("Asma klozet", "Wall-hung WC", 4, "%0"), ("Banyo mobilyası", "Bathroom furniture", 4, "%0")]
T_GF = tablo([th("Ürün grubu", "Product group", "Birden fazla kanalda fiyatı bulunan ürünlerin grubu.", "Group of products priced in more than one channel."), th("Ürün sayısı", "Products", "Karşılaştırılan ürün sayısı.", "Number of products compared.", True),
              th("Fark medyanı", "Median gap", "vitra.com.tr liste fiyatına göre en ucuz kanalın altında kalma oranının medyanı.", "Median of the reduction of the cheapest channel below the vitra.com.tr list price.", True)],
             [[x(a, b), cell(c), n(d)] for a, b, c, d in GF], "dar")
EK = """
<h3>%s</h3>
%s
%s
<h3>%s</h3>
%s
%s
<div class="two"><div><h3>%s</h3>%s</div><div>%s</div></div>
%s
""" % (
 x("Trendyol ve Hepsiburada çok satan listeleri: 14 kategori", "Trendyol and Hepsiburada best-seller lists: 14 categories"),
 T_CS2,
 insight("Seramik sağlık gereçlerinde (klozet, klozet kapağı, lavabo, iç takım) Trendyol çok satanlarının %78 - %89'u üçüncü taraf satıcılardadır; banyo mobilyası, çamaşır makinesi dolabı ve duşakabinde ise marka mağazaları öndedir (Durul duşakabinde Trendyol 18/36, Hepsiburada 27/36 ürün; lavaboda Turkuaz %59 - %65 değerlendirme payı). VitrA ve Artema Trendyol'da 6 kategoride 23, Hepsiburada'da 8 kategoride 44 listelemeyle görünmekte; görünürlük iç takım, conta ve klozet kapağında yoğunlaşmaktadır (Hepsiburada iç takımında değerlendirme payı %36,5, gömme rezervuar aramasında %44,2). Bu listelemelerin yalnızca 5'i (TY) ve 2'si (HB) VitrA mağazasındandır. Lavabo, banyo dolabı, duşakabin ve duş seti listelerinde VitrA ürünü ilk 36'da yer almamaktadır.",
         "In sanitaryware (WC, toilet seat, washbasin, inner mechanism) 78% - 89% of Trendyol best sellers are with third-party sellers; in bathroom furniture, washing machine cabinets and shower enclosures brand stores lead (Durul 18/36 on Trendyol and 27/36 on Hepsiburada in shower enclosures; Turkuaz 59% - 65% review share in washbasins). VitrA and Artema appear with 23 listings in 6 categories on Trendyol and 44 in 8 categories on Hepsiburada; visibility concentrates in inner mechanisms, seals and toilet seats (36.5% review share in Hepsiburada inner mechanisms, 44.2% in the concealed cistern search). Only 5 (TY) and 2 (HB) of these listings are from the VitrA store. No VitrA product is in the top 36 of the washbasin, bathroom cabinet, shower enclosure and shower set lists.", "D26"),
 x("VitrA ürünlerinde kanal fiyat farkı: 29 ürün", "Channel price gap for VitrA products: 29 products"), KPI_KF + T_KF,
 insight("29 üründen 26'sında vitra.com.tr dışında en az bir kanalda fiyat bulunmuş, bunların 19'unda en ucuz kanal vitra.com.tr dışındadır (Hepsiburada buybox 11, Trendyol 3P 7, Koçtaş 1); 7 üründe vitra.com.tr en ucuzdur. Bu 19 üründe fark medyanı %24,7'dir (çeyrekler %15,7 - %32,4; en yüksek Artema Flow Round banyo bataryası %41,1). Asma klozet ve banyo mobilyasında fark medyanı %0'dır; fark armatür (%29,8), klozet kapağı (%27,2), iç takım ve gömme rezervuar setinde toplanmaktadır. Trendyol'da VitrA mağazası ile 3P satıcının birlikte bulunduğu 6 ürünün 6'sında 3P daha düşüktür (medyan %11,8). Sepet indirimleri hesaba alındığında (vitra.com.tr %10-15, Trendyol VitrA mağazası %20-23) fark medyanı %15,4'e inmektedir. Koçtaş'ta 16 eşleşmenin tamamı üçüncü taraf satıcı listelemesidir ve medyanda vitra.com.tr'den %3,6 daha yüksektir. Gözlem anında 29 ürünün 15'i vitra.com.tr'de \"stokta yok\" görünmekte, fiyat gösterilmeye devam etmektedir.",
         "For 26 of 29 products a price was found in at least one channel other than vitra.com.tr, and for 19 of them the cheapest channel is outside vitra.com.tr (Hepsiburada buybox 11, Trendyol 3P 7, Koçtaş 1); vitra.com.tr is cheapest for 7 products. The median gap for these 19 products is 24.7% (quartiles 15.7% - 32.4%; highest Artema Flow Round bath tap 41.1%). The median gap is 0% in wall-hung WCs and bathroom furniture; the gap concentrates in taps (29.8%), toilet seats (27.2%), inner mechanisms and concealed cistern sets. On Trendyol, in all 6 products where the VitrA store and a 3P seller coexist, the 3P seller is lower (median 11.8%). Taking basket discounts into account (vitra.com.tr 10-15%, Trendyol VitrA store 20-23%) the median gap falls to 15.4%. At Koçtaş all 16 matches are third-party listings and the median is 3.6% above vitra.com.tr. At the time of observation 15 of 29 products showed \"out of stock\" on vitra.com.tr while the price remained displayed.", "D26"),
 x("Ürün grubuna göre fark medyanı", "Median gap by product group"), T_GF,
 marks([("at", "Hepsiburada'da aynı ürün için birden fazla katalog kaydı bulunmakta (A41994 için 4 kayıt ve 7 satıcı); bazı kayıtlarda fiyat vitra.com.tr liste fiyatının 2,5x'ine çıkmaktadır (Sento asma klozet 36.764 TL, liste 14.767 TL)", "On Hepsiburada the same product has several catalogue records (4 records and 7 sellers for A41994); in some records the price rises to 2.5 times the vitra.com.tr list price (Sento wall-hung WC 36,764 TL, list 14,767 TL)"),
        ("at", "Büyük satıcılar (Evdema) liste fiyatına yakın (%1,5); diğer 3P satıcılar ve Hepsiburada'nın kendi satışı armatür, gömme rezervuar ve klozet kapağında liste fiyatının %14 - %41 altında", "Large sellers (Evdema) stay close to the list price (1.5%); other 3P sellers and Hepsiburada's own sales are 14% - 41% below the list price in taps, concealed cisterns and toilet seats"),
        ("at", "Hepsiburada çok satan 2. ve 3. sayfalarında (216 ürün) klozette VitrA 16 ürün (11 klozet ve takım, 5 parça), lavaboda 2, banyo bataryasında Artema 9 ürün; Artema ürünlerinin tamamı üçüncü taraf satıcıda", "On Hepsiburada best-seller pages 2 and 3 (216 products) VitrA has 16 products in WCs (11 WCs and sets, 5 parts), 2 in washbasins, and Artema 9 in bath taps; all Artema products are with third-party sellers"),
        ("up", "Ürün sayfasında \"Ücretsiz Montaj\" etiketi 29 ürünün 1'inde (Sento lavabo dolabı); Koçtaş'ta 6 ürün sayfasında \"Montaj Satın Al\" seçeneği bulunmaktadır", "The \"Free Installation\" label appears on 1 of 29 product pages (Sento basin unit); Koçtaş offers \"Buy Installation\" on 6 product pages")]),
 kaynak("Trendyol çok satan listeleri (14 kategori × 36 ürün) ve VitrA ürün eşleşmeleri · Hepsiburada ilk sayfa (14 × 36) · Koçtaş ve vitra.com.tr ürün sayfaları · 29.09.2026 · liste fiyatı esas", "Trendyol best-seller lists (14 categories × 36 products) and VitrA product matches · Hepsiburada first page (14 × 36) · Koçtaş and vitra.com.tr product pages · 29.09.2026 · list price basis", "D26"),
)
