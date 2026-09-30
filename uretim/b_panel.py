# -*- coding: utf-8 -*-
"""Bolum: VitrA resmi magaza performansi - Trendyol satici paneli ve Hepsiburada panel verisi (D31).
Ciro tutari verilmez; adet, pay, oran ve ortalama fiyat kullanilir."""
from ortak import *
from grafik2 import kombo, yigin, f_adet, f_tl, f_pay
import json, os
P = json.load(open(os.path.join(veri.V, "islenmis", "panel.json"), encoding="utf-8"))
PU = json.load(open(os.path.join(veri.V, "islenmis", "panel_url.json"), encoding="utf-8"))["url"]
import re as _re
from urllib.parse import quote as _q
_KOD = _re.compile(r"\b(A4\d{4,6}|\d{3}B\d{4}|\d{4}[BL]\d{3}-\d{4}|\d{2,3}-\d{3}[R-]?\d{3}|\d{5}V?|\d{3}-\d{4}(?:-\d{2})?|\d{11})\b")
def plink(kod, ad):
    """Urun adi -> Trendyol urun sayfasi; bulunamazsa model koduyla arama."""
    ad = ad or kod; m = _KOD.search(ad); k2 = m.group(1) if m else kod
    if len(ad) >= 90: ad = ad[:ad.rstrip().rfind(" ")].rstrip(" -,") + "…"   # raporda kesilmis adlar kelime sinirinda kisaltilir
    url = PU.get(kod) or PU.get(k2) or ("https://www.trendyol.com/sr?q=" + _q(k2))
    return u(url, ad)
CQ = {c["q"]: c for c in P["ceyrek"]}
def qad(q): return x(q[:4] + " " + q[4:], q[:4] + " " + q[4:])
def ondalik(v, o=1): return ("%." + str(o) + "f") % v
def f1(v): return ondalik(v).replace(".", ",")
def pz(v): return n(yzd(v)) if v is not None else n("-")
KAT_EN = {"Banyo Dolabı Seti": "Bathroom cabinet set", "Lavabo Bataryası": "Basin tap", "Duş Sistemi": "Shower system", "Klozet": "WC", "Eviye Bataryası": "Kitchen tap", "Ara Musluk": "Stop valve",
          "Klozet Kapağı": "Toilet seat", "Banyo Bataryası": "Bath tap", "Lavabo": "Washbasin", "Banyo Askısı": "Towel rail and hook", "Tuvalet Kağıtlığı": "Toilet roll holder", "Banyo Tesisatı": "Bathroom plumbing",
          "Rezervuar": "Cistern", "Tuvalet Fırçası": "Toilet brush", "Banyo Düzenleyici": "Bathroom organiser", "Çöp Kovası": "Bin", "Musluk Başlığı": "Tap head", "Çamaşır Makinesi Dolabı": "Washing machine cabinet",
          "Sabunluk": "Soap dish", "Banyo Aynası": "Bathroom mirror", "Diş Fırçalık": "Toothbrush holder", "Tutunma Barı": "Grab bar", "Ayna Etajeri": "Mirror shelf", "Duşakabin": "Shower enclosure",
          "Banyo Aksesuarları": "Bathroom Accessories", "Banyo Mobilyası": "Bathroom furniture", "Bataryalar & Musluklar": "Taps & valves", "Eviye": "Sink"}
def kat(k_): return x(k_, KAT_EN.get(k_, k_))
c4, c3 = CQ["2025Q4"], CQ["2026Q3"]
# --- tablo 1: ceyrek
T1 = tablo([th("Çeyrek", "Quarter", "Trendyol satış raporu çeyrekleri; 2026 Q3 29.09.2026'ya kadardır.", "Trendyol sales report quarters; 2026 Q3 runs to 29.09.2026."),
            th("Net satış adedi", "Net units sold", "Brüt satış adedinden iptal ve iade düşülmüş adet.", "Gross units minus cancellations and returns.", True),
            th("Satılan model", "Models sold", "Çeyrekte en az bir satış alan model kodu sayısı.", "Number of model codes with at least one sale in the quarter.", True),
            th("Artema adet payı", "Artema unit share", "Net adedin Artema markalı ürünlerden gelen payı.", "Share of net units from Artema-branded products.", True),
            th("Ort. net fiyat (TL)", "Avg. net price (TL)", "Net ciro / net satış adedi; satış karışımının fiyat düzeyini gösterir.", "Net revenue / net units; shows the price level of the sales mix.", True),
            th("İndirim / brüt ciro", "Discount / gross revenue", "Kampanya, kupon ve indirimlerin brüt ciroya oranı.", "Campaigns, coupons and discounts as a share of gross revenue.", True),
            th("İptal", "Cancellation", "İptal adedi / brüt satış adedi.", "Cancelled units / gross units.", True),
            th("İade", "Returns", "İade adedi / brüt satış adedi.", "Returned units / gross units.", True),
            th("Komisyon / net ciro", "Commission / net revenue", "Trendyol komisyonunun net ciroya oranı.", "Trendyol commission as a share of net revenue.", True)],
           [[qad(c["q"]), cell(c["net"]), cell(c["model"]), pz(c["artema_pay"]), cell(c["ort_fiyat"]), pz(c["indirim"]), pz(c["iptal"]), pz(c["iade"]), pz(c["komisyon"])] for c in P["ceyrek"]])
# --- tablo 2: kategori
rows2 = []
for r in P["kategori"][:20]:
    deg = (r["q3"] / r["q4"] - 1) * 100 if r["q4"] else None
    rows2.append([kat(r["kategori"]), cell(r["net"]), pz(r["adet_pay"]), pz(r["ciro_pay"]), cell(r["ort_fiyat"]), pz(r["iade"]),
                  n(f1(r["puan"])) if r["puan"] else n("-"), pz(r["dusuk"]), (n(yz(deg, ond=0).replace("%", "%") + " (%s → %s)" % (bin(r["q4"]), bin(r["q3"]))) if deg is not None and abs(deg) >= 1000 else (n(yz(deg, ond=0)) if deg is not None else n("-")))])
T2 = tablo([th("Kategori", "Category", "Trendyol satış raporundaki ürün kategorisi; 12 ayda en az 25 net satış alan kategoriler, ciro payına göre sıralı.", "Product category in the Trendyol sales report; categories with at least 25 net units in 12 months, ordered by revenue share."),
            th("Net adet (12 ay)", "Net units (12 months)", "2025 Q4 - 2026 Q3 net satış adedi.", "Net units, 2025 Q4 - 2026 Q3.", True),
            th("Adet payı", "Unit share", "Kategorinin toplam net adet içindeki payı.", "The category's share of total net units.", True),
            th("Ciro payı", "Revenue share", "Kategorinin toplam net ciro içindeki payı.", "The category's share of total net revenue.", True),
            th("Ort. net fiyat (TL)", "Avg. net price (TL)", "Net ciro / net adet.", "Net revenue / net units.", True),
            th("İade", "Returns", "İade adedi / brüt satış adedi.", "Returned units / gross units.", True),
            th("Ürün puanı", "Product rating", "Ürün değerlendirmelerinin ortalaması (5 üzerinden), 02.10.2025 - 28.09.2026; 5'ten az değerlendirmede \"-\".", "Average product rating (out of 5), 02.10.2025 - 28.09.2026; \"-\" below 5 reviews.", True),
            th("Düşük puan payı", "Low-rating share", "1 ve 2 puanlı değerlendirmelerin payı.", "Share of 1 and 2-star reviews.", True),
            th("Adet değişimi", "Unit change", "2026 Q3 net adedinin 2025 Q4'e göre değişimi; %1.000 üzerindeki değişimlerde çeyreklik adet parantez içinde verilmiştir.", "Change in 2026 Q3 net units against 2025 Q4; for changes above 1,000% the quarterly units are given in brackets.", True)], rows2, "uzun")
# --- tablo 3: urun
def stok(v): return n(x("Yok", "Not available")) if v == 0 else (n(x("Var", "Available")) if v else n("-"))
def urun_rows(lst):
    return [[plink(r["kod"], r["ad"]), kat(r["kat"]) if r["kat"] else n("-"), veri_m(r["marka"] or "-"), cell(r["net"]), pz(r["adet_pay"]), pz(r["ciro_pay"]), cell(r["ort_fiyat"]), pz(r["iade"]), stok(r["stok"])] for r in lst]
UB = [th("Ürün", "Product", "Trendyol'daki ürün adı; bağlantı ürün sayfasını açar (resmi mağazada listelenmeyenlerde ürünün genel sayfası, bulunamayanlarda model koduyla arama). Ad alanı boş satırlarda favori-görüntüleme raporundaki ad kullanılmıştır.", "Product name on Trendyol; the link opens the product page (the general product page where the official store has no listing, a model-code search where none was found). For rows with an empty name the name in the favourite-view report is used."),
      th("Kategori", "Category", "Satış raporundaki kategori (Trendyol sınıflandırması; ör. çamaşır musluğu \"Musluk Başlığı\" altında yer almaktadır).", "Category in the sales report (Trendyol classification; e.g. washing machine taps sit under \"Tap head\")."), th("Marka", "Brand", "Satış raporundaki marka (Trendyol sınıflandırması).", "Brand in the sales report (Trendyol classification)."),
      th("Net adet", "Net units", "2025 Q4 - 2026 Q3 net satış adedi.", "Net units, 2025 Q4 - 2026 Q3.", True), th("Adet payı", "Unit share", "Mağaza net adedi içindeki pay.", "Share of the store's net units.", True),
      th("Ciro payı", "Revenue share", "Mağaza net cirosu içindeki pay.", "Share of the store's net revenue.", True), th("Ort. net fiyat (TL)", "Avg. net price (TL)", "Net ciro / net adet.", "Net revenue / net units.", True),
      th("İade", "Returns", "İade adedi / brüt satış adedi.", "Returned units / gross units.", True), th("Güncel stok", "Current stock", "30.09.2026 itibarıyla stok: Var / Yok.", "Stock as of 30.09.2026: Available / Not available.", True)]
T3 = tablo(UB, urun_rows(P["urun_adet"]), "uzun")
T3b = tablo(UB, urun_rows(P["urun_ciro"]), "uzun")
FB = tablo([th("Fiyat bandı (TL)", "Price band (TL)", "Ürünün 12 aylık ortalama net satış fiyatı.", "The product's 12-month average net selling price."),
            th("Ürün sayısı", "Products", "Banttaki satılan ürün sayısı.", "Number of products sold in the band.", True),
            th("Adet payı", "Unit share", "Net adet içindeki pay.", "Share of net units.", True), th("Ciro payı", "Revenue share", "Net ciro içindeki pay.", "Share of net revenue.", True)],
           [[veri_m(b["band"]), cell(b["urun"]), pz(b["adet_pay"]), pz(b["ciro_pay"])] for b in P["fiyat_bandi"]], "dar")
# --- tablo 4: donusum
D = P["donusum"]
T4 = tablo([th("Kategori", "Category", "Favori-görüntüleme raporundaki kategori, Ocak - Eylül 2026.", "Category in the favourite-view report, January - September 2026."),
            th("Görüntülenme payı", "Share of views", "Mağaza ürün sayfası görüntülenmesi içindeki pay (satıcı görüntülenmesi).", "Share of store product page views (seller views).", True),
            th("Sepete ekleme", "Add to basket", "Sepete ekleme / görüntülenme.", "Add-to-basket / views.", True),
            th("Satışa dönüş", "Conversion", "Brüt satış adedi / görüntülenme.", "Gross units / views.", True),
            th("Aktif favori", "Active favourites", "Ürünleri favorisinde tutan kullanıcı sayısı toplamı.", "Total users keeping the products in favourites.", True)],
           [[kat(r["kategori"]), pz(r["gor_pay"]), n(yzd(r["sepet"], 2)), n(yzd(r["cr"], 2)), cell(r["fav"])] for r in D["kat"]], "uzun")
T4b = tablo([th("Ürün", "Product", "Görüntülenmesi yüksek, Ocak - Eylül 2026'da en fazla 2 satış alan ürünler.", "Products with high views and at most 2 sales in January - September 2026."),
             th("Kategori", "Category", "Ürün kategorisi.", "Product category."), th("Görüntülenme", "Views", "Satıcı ürün sayfası görüntülenmesi.", "Seller product page views.", True),
             th("Sepete ekleme", "Add to basket", "Sepete ekleme sayısı.", "Add-to-basket count.", True), th("Satış", "Sales", "Brüt satış adedi.", "Gross units sold.", True)],
            [[plink(r["ad"], r["ad"]), kat(r["kat"]), cell(r["gor"]), cell(r["sepet"]), cell(r["sat"])] for r in D["bakan_cok"]])
# --- tablo 5: profil
PR = P["profil"]
T5 = tablo([th("Gösterge", "Indicator", "Trendyol sipariş dağılım raporu, sipariş bazında pay.", "Trendyol order distribution report, share by order.")] +
           [th(c["q"][:4] + " " + c["q"][4:], c["q"][:4] + " " + c["q"][4:], "Çeyrek.", "Quarter.", True) for c in PR],
           [[x("Yeni müşteri siparişi", "Orders from new customers")] + [pz(c["yeni"]) for c in PR],
            [x("Trendyol Plus üyesi siparişi", "Orders from Trendyol Plus members")] + [pz(c["plus"]) for c in PR],
            [x("Tek ürünlü sipariş", "Single-item orders")] + [pz(c["tek"]) for c in PR],
            [x("5.000 TL ve üzeri sipariş", "Orders of 5,000 TL and above")] + [pz(c["ust5"]) for c in PR],
            [x("Kadın müşteri siparişi", "Orders from female customers")] + [pz(c["kadin"]) for c in PR]], "dar")
# --- tablo 6: enleri
EN = P["enleri"]; EO = P["enleri_ozet"]
SIRA_E = ["Klozet", "Klozet Kapağı", "Rezervuar", "Lavabo", "Banyo Mobilyası", "Bataryalar & Musluklar", "Duş Sistemi", "Eviye", "Banyo Aksesuarları"]
ENd = {e["kategori"]: e for e in EN}
def vv(a, b): return n("%d / %d" % (a, b))
T6 = tablo([th("Kategori", "Category", "Trendyol'un Enleri raporundaki kategori, Eylül 2026, ilk 50 ürün.", "Category in the Trendyol Top Lists report, September 2026, top 50 products."),
            th("Çok satanlar: resmi mağaza / VitrA markalı", "Best sellers: official store / VitrA-branded", "İlk 50 içinde VitrA resmi mağazasının satırı / VitrA veya Artema markalı tüm satırlar (üçüncü taraf dahil).", "Rows of the VitrA official store / all VitrA or Artema-branded rows (third parties included) in the top 50.", True),
            th("Ciro listesi: resmi / VitrA", "Revenue list: official / VitrA", "En çok ciro getirenler listesinde aynı ölçü.", "Same measure in the top-revenue list.", True),
            th("Favori listesi: VitrA", "Favourites list: VitrA", "En çok favorilenen 50 ürün içinde VitrA veya Artema markalı satır.", "VitrA or Artema-branded rows among the 50 most-favourited products.", True),
            th("Görüntülenme payı (VitrA)", "Share of views (VitrA)", "En çok görüntülenen 50 ürünün toplam görüntülenmesi içinde VitrA ve Artema satırlarının payı.", "Share of VitrA and Artema rows in the total views of the 50 most-viewed products.", True),
            th("Çok satan medyan fiyat (TL)", "Best-seller median price (TL)", "İlk 50 çok satan ürünün ortalama satış fiyatı medyanı.", "Median average selling price of the top 50 best sellers.", True),
            th("VitrA medyan fiyat (TL)", "VitrA median price (TL)", "Tüm listelerdeki VitrA ve Artema satırlarının medyanı; satır sayısı az olan kategorilerde tek bir ürünü yansıtabilir.", "Median of VitrA and Artema rows across all lists; in categories with few rows it may reflect a single product.", True),
            th("Çok satanlarda lider marka", "Leading brand in best sellers", "İlk 50 çok satanda en çok satırı olan marka ve satır sayısı.", "Brand with the most rows in the top 50 best sellers and its row count.")],
           [[kat(k_), vv(ENd[k_]["sat_siz"], ENd[k_]["sat_vit"]), vv(ENd[k_]["ciro_siz"], ENd[k_]["ciro_vit"]), cell(ENd[k_]["fav_vit"]),
             pz(ENd[k_]["gor_pay"]) if ENd[k_]["gor_pay"] is not None else n("-"), cell(ENd[k_]["sat_med"]), cell(ENd[k_]["vit_med"]) if ENd[k_]["vit_med"] else n("-"),
             veri_m("%s · %d" % (ENd[k_]["lider"], ENd[k_]["lider_n"]))] for k_ in SIRA_E])
# --- tablo 7-8: yorum ve soru temalari
TM_EN = {"Kalite ve malzeme": "Quality and material", "Görünüm ve tasarım": "Look and design", "Hediye ve paketleme jesti": "Gift and packaging gesture", "Kargo ve teslimat": "Shipping and delivery",
         "Ambalaj": "Packaging", "Eksik parça ve aksesuar": "Missing parts and accessories", "Ölçü ve uyum": "Size and fit", "Kırık ve hasar": "Broken and damaged", "Montaj": "Installation",
         "İade ve değişim": "Returns and exchange", "Su kaçağı ve işlev": "Leaks and function"}
T7 = tablo([th("Yorum teması", "Review theme", "Yorum metnindeki anahtar kelimelerle sınıflandırılmıştır; bir yorum birden fazla temaya girebilir.", "Classified by keywords in the review text; a review can fall into more than one theme."),
            th("Yorumlu değerlendirme", "Reviews", "Temaya giren yorumlu değerlendirme sayısı (toplam %d)." % P["deger"]["yorumlu"], "Number of reviews with text in the theme (total %d)." % P["deger"]["yorumlu"], True),
            th("Ortalama puan", "Average rating", "Temaya giren değerlendirmelerin ortalama puanı.", "Average rating of reviews in the theme.", True),
            th("Düşük puan (1-2)", "Low rating (1-2)", "Temadaki 1 ve 2 puanlı değerlendirme sayısı.", "Number of 1 and 2-star reviews in the theme.", True)],
           [[x(t["tema"], TM_EN[t["tema"]]), cell(t["n"]), n(f1(t["ort"])), cell(t["dusuk"])] for t in sorted(P["tema"], key=lambda t: -t["n"])], "dar")
SQ_EN = {"Uyumluluk (klozet, lavabo, valf kodu)": "Compatibility (WC, basin, valve code)", "Stok, renk ve varyant": "Stock, colour and variant", "Ölçü ve boyut": "Size and dimensions", "Yedek parça": "Spare parts",
         "Kargo ve teslim süresi": "Shipping and delivery time", "Montaj": "Installation", "Kutu içeriği (kapak, rezervuar, hortum dahil mi)": "Box contents (seat, cistern, hose included?)",
         "Eksik, hasarlı, arızalı ürün": "Missing, damaged, faulty product", "Orijinallik ve marka": "Authenticity and brand"}
SC_EN = {"Danışma Hattı / yetkili servise yönlendirme": "Referral to the Helpline / authorised service", "\"İlgili ekibe ilettik, tekrar sorun\"": "\"Forwarded to the team, please ask again\"",
         "\"Ürün kodunu paylaşırsanız\"": "\"If you share the product code\"", "Farklı marka uyumluluğu paylaşılamıyor": "Compatibility with other brands cannot be shared",
         "Trendyol kuralı: parça ve bağlantı gönderilemiyor": "Trendyol rule: parts and links cannot be sent"}
T8 = tablo([th("Soru teması", "Question theme", "Eylül 2026'da ürün sayfalarında sorulan %d sorunun sınıflandırması; bir soru birden fazla temaya girebilir." % P["soru"]["n"], "Classification of the %d questions asked on product pages in September 2026; a question can fall into more than one theme." % P["soru"]["n"]),
            th("Soru", "Questions", "Temaya giren soru sayısı.", "Number of questions in the theme.", True)],
           [[x(t["tema"], SQ_EN[t["tema"]]), cell(t["n"])] for t in sorted(P["soru"]["tema"], key=lambda t: -t["n"])], "dar")
T8b = tablo([th("Yanıt kalıbı", "Answer pattern", "Onaylanan yanıtlarda tekrar eden kalıp.", "Recurring pattern in approved answers."), th("Yanıt", "Answers", "Kalıbı içeren yanıt sayısı.", "Number of answers containing the pattern.", True)],
            [[x(c["kalip"], SC_EN[c["kalip"]]), cell(c["n"])] for c in sorted(P["soru"]["cevap"], key=lambda c: -c["n"])], "dar")
# --- degerler
NE = P["neden"]; iade_top = NE["Kusurlu Ürün Gönderildi"] + NE["Yanlış Ürün Gönderildi"] + NE["Vazgeçtim"] + NE["Diğer"] + NE["Bedeni/Ebatı Küçük Geldi"] + NE["Bedeni/Ebatı Büyük Geldi"]
olcu = (NE["Bedeni/Ebatı Küçük Geldi"] + NE["Bedeni/Ebatı Büyük Geldi"]) / iade_top * 100; kusur = NE["Kusurlu Ürün Gönderildi"] / iade_top * 100
ipt_top = NE["Müşterinin İptal Ettiği"] + NE["Trendyol'un İptal Ettiği"] + NE["Benim İptal Ettiğim"]
OP = P["operasyon"]; HB = P["hb"]; DG = P["deger"]; SV = P["satici"]; ST = P["stok"]; PA = P["pareto"]; MG = P["magaza"]
ucuz = HB["iptal_neden"].get("Müşteri daha ucuza buldu", 0) / HB["iptal_top"] * 100
kat_d = {r["kategori"]: r for r in P["kategori"]}

x("%s kat" % f1(c3["net"] / c4["net"]), "%sx" % ondalik(c3["net"] / c4["net"]))
from grafik2 import gruplu as _gr
_KG = sorted([r for r in P["kategori"] if r.get("ciro_pay") is not None], key=lambda r: -r["ciro_pay"])[:12]
GKAT = _gr([(x(r["kategori"], KAT_EN.get(r["kategori"], r["kategori"])), [r["adet_pay"], r["ciro_pay"]]) for r in _KG],
           [(x("Net adet payı", "Net unit share"), "#9AA8A5"), (x("Net ciro payı", "Net revenue share"), "#10332F")],
           x("Ciro payına göre ilk 12 kategoride net adet ve net ciro payı · 2025 Q4 - 2026 Q3, Trendyol resmi mağaza", "Net unit and net revenue share in the top 12 categories by revenue share · 2025 Q4 - 2026 Q3, Trendyol official store"))
GK1 = kombo([qad(c["q"]) for c in P["ceyrek"]],
             (x("Net satış adedi", "Net units sold"), "#10332F", [c["net"] for c in P["ceyrek"]], f_adet),
             (x("Ortalama net satış fiyatı", "Average net selling price"), "#E85F36", [round(c["ort_fiyat"]) for c in P["ceyrek"]], f_tl),
             x("Çeyreklik net satış adedi (sol eksen) ve ortalama net satış fiyatı (sağ eksen) · Trendyol resmi mağaza", "Quarterly net units (left axis) and average net selling price (right axis) · Trendyol official store"))
_FBR = ["#F3E6DC", "#F7C8B3", "#FF9E7D", "#FF7B52", "#C9573A", "#4E6E68", "#10332F"]
GFB = yigin([(x("Adet payı", "Unit share"), [b["adet_pay"] for b in P["fiyat_bandi"]]), (x("Ciro payı", "Revenue share"), [b["ciro_pay"] for b in P["fiyat_bandi"]])],
            [(x(b["band"] + " TL", b["band"].replace(".", ",") + " TL"), r) for b, r in zip(P["fiyat_bandi"], _FBR)],
            x("Fiyat bandına göre net adet ve net ciro dağılımı (%100) · 12 aylık ortalama net satış fiyatı", "Distribution of net units and net revenue by price band (100%) · 12-month average net selling price"), genislik=460, sol=92)
EK = """
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
<div class="two"><div>%s</div><div>%s</div></div>
%s
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
<h3>%s</h3>
<div class="two"><div>%s</div><div>%s%s</div></div>
%s
<h3>%s</h3>
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("VitrA'nın Trendyol resmi mağazasına ait satıcı paneli raporları (2025 Q4 - 2026 Q3 satış ve sipariş dağılımı, 2025 ve 2026 ürün görüntülenme, 12 aylık ürün ve satıcı değerlendirmeleri, Eylül 2026 ürün soruları, Eylül 2026 \"Trendyol'un Enleri\" kategori listeleri) ile Hepsiburada panel raporları (hak ediş, görüntülenme, iptal, değerlendirme) incelenmiştir. Ciro tutarları verilmemiş; adet, pay, oran ve ortalama fiyat kullanılmıştır.",
   "The seller panel reports of VitrA's official Trendyol store (2025 Q4 - 2026 Q3 sales and order distribution, 2025 and 2026 product views, 12 months of product and seller reviews, September 2026 product questions, September 2026 \"Trendyol Top Lists\" category lists) and Hepsiburada panel reports (settlement, views, cancellations, reviews) were examined. Revenue amounts are not shown; units, shares, rates and average prices are used."),
 kpi_kart("%sx" % f1(c3["net"] / c4["net"]), "2026 Q3 net satış adedi 2025 Q4'ün %sx'i (%s → %s)" % (f1(c3["net"] / c4["net"]), bin(c4["net"]), bin(c3["net"])), "2026 Q3 net units are %sx 2025 Q4 (%s → %s)" % (ondalik(c3["net"] / c4["net"]), f"{c4['net']:,}", f"{c3['net']:,}"), "up"),
 kpi_kart(yz((c3["ort_fiyat"] / c4["ort_fiyat"] - 1) * 100, ond=0), "Ortalama net satış fiyatı · %s TL → %s TL; karışım düşük fiyatlı tamamlayıcıya kaydı" % (bin(c4["ort_fiyat"]), bin(c3["ort_fiyat"])), "Average net selling price · %s TL → %s TL; the mix shifted to low-priced complements" % (f"{round(c4['ort_fiyat']):,}", f"{round(c3['ort_fiyat']):,}"), "dn"),
 kpi_kart("%d / 9" % sum(1 for e in EN if e["sat_siz"] == 0 and e["ciro_siz"] == 0), "Eylül 2026 kategori listelerinde resmi mağazanın hiç yer almadığı kategori (aksesuar, mobilya, batarya, duş, evye)", "Categories where the official store is absent from the September 2026 lists (accessories, furniture, taps, shower, sink)", "dn"),
 kpi_kart(f1(DG["ort"]), "Ortalama ürün puanı (%s değerlendirme) · banyo dolabı seti %s, klozet %s" % (bin(DG["n"]), f1(kat_d["Banyo Dolabı Seti"]["puan"]), f1(kat_d["Klozet"]["puan"])), "Average product rating (%s reviews) · bathroom cabinet set %s, WC %s" % (f"{DG['n']:,}", ondalik(kat_d["Banyo Dolabı Seti"]["puan"]), ondalik(kat_d["Klozet"]["puan"])), "hi"),
 x("Çeyreklik satış, fiyat ve karışım", "Quarterly sales, price and mix"), GK1 + T1,
 insight("Net satış adedi 2025 Q4'te %s iken 2026 Q3'te %s'e çıkmıştır; aynı dönemde ortalama net satış fiyatı %s TL'den %s TL'ye inmiştir. Artış, düşük fiyatlı tamamlayıcı ürünlerden gelmektedir: Artema A45200 filtreli ara musluk tek başına 12 aylık net adedin %s'ini oluşturmakta, Artema'nın adet payı 2026 Q2'de %s'e ulaşmıştır. İndirimin brüt ciroya oranı %s'ten %s'e yükselmiş, 2026 Q3'te satılan ürünlerde ortalama satış fiyatı güncel liste fiyatının medyan %s altında gerçekleşmiştir. İade oranı ise %s'ten %s'e gerilemiştir; operasyon raporunda kusurlu, yanlış ve eksik ürün kaynaklı iade oranı 2025'te %s, 2026'da %s'dir." % (
         bin(c4["net"]), bin(c3["net"]), bin(c4["ort_fiyat"]), bin(c3["ort_fiyat"]), yzd(P["urun_adet"][0]["adet_pay"]), yzd(CQ["2026Q2"]["artema_pay"]), yzd(c4["indirim"]), yzd(c3["indirim"]), yzd(abs(P["liste_fark"]["medyan"])), yzd(c4["iade"]), yzd(c3["iade"]), yzd(OP["2025"]["Kusurlu & Yanlış & Eksik İade Oranı"]), yzd(OP["2026"]["Kusurlu & Yanlış & Eksik İade Oranı"])),
         "Net units rose from %s in 2025 Q4 to %s in 2026 Q3; over the same period the average net selling price fell from %s TL to %s TL. The growth comes from low-priced complementary products: the Artema A45200 filtered stop valve alone makes up %s of 12-month net units, and Artema's unit share reached %s in 2026 Q2. Discounts as a share of gross revenue rose from %s to %s, and in 2026 Q3 the average selling price of the products sold was a median %s below the current list price. The return rate fell from %s to %s; in the operations report the return rate caused by defective, wrong and missing products is %s in 2025 and %s in 2026." % (
         f"{c4['net']:,}", f"{c3['net']:,}", f"{round(c4['ort_fiyat']):,}", f"{round(c3['ort_fiyat']):,}", ondalik(P["urun_adet"][0]["adet_pay"]) + "%", ondalik(CQ["2026Q2"]["artema_pay"]) + "%", ondalik(c4["indirim"]) + "%", ondalik(c3["indirim"]) + "%", ondalik(abs(P["liste_fark"]["medyan"])) + "%", ondalik(c4["iade"]) + "%", ondalik(c3["iade"]) + "%", ondalik(OP["2025"]["Kusurlu & Yanlış & Eksik İade Oranı"]) + "%", ondalik(OP["2026"]["Kusurlu & Yanlış & Eksik İade Oranı"]) + "%"), "D31"),
 x("Kategori bazında adet, ciro payı ve memnuniyet", "Units, revenue share and satisfaction by category"), GKAT + T2,
 insight("Ciro, adedin toplandığı aksesuar ve ara muslukta değil, batarya, mobilya ve seramikte oluşmaktadır: banyo dolabı seti adedin %s'i ile cironun %s'ini, lavabo bataryası %s ile %s'ini, klozet %s ile %s'ini üretmektedir. Adette ilk sıradaki ara musluk (%s) cironun %s'inde kalmaktadır. Memnuniyet de aynı ayrımı göstermektedir: banyo dolabı setinde ortalama puan %s ve düşük puan payı %s, klozette %s ve %s; aksesuar ve bataryada puan çoğunlukla 4,5 ve üzerindedir. Ciroda ilk sıradaki lavabo bataryasında adet 2025 Q4'e göre %s gerilemiştir." % (
         yzd(kat_d["Banyo Dolabı Seti"]["adet_pay"]), yzd(kat_d["Banyo Dolabı Seti"]["ciro_pay"]), yzd(kat_d["Lavabo Bataryası"]["adet_pay"]), yzd(kat_d["Lavabo Bataryası"]["ciro_pay"]), yzd(kat_d["Klozet"]["adet_pay"]), yzd(kat_d["Klozet"]["ciro_pay"]), yzd(kat_d["Ara Musluk"]["adet_pay"]), yzd(kat_d["Ara Musluk"]["ciro_pay"]),
         f1(kat_d["Banyo Dolabı Seti"]["puan"]), yzd(kat_d["Banyo Dolabı Seti"]["dusuk"]), f1(kat_d["Klozet"]["puan"]), yzd(kat_d["Klozet"]["dusuk"]), "%%%d" % round(abs((kat_d["Lavabo Bataryası"]["q3"] / kat_d["Lavabo Bataryası"]["q4"] - 1) * 100))),
         "Revenue is generated not in accessories and stop valves, where units concentrate, but in taps, furniture and ceramics: bathroom cabinet sets produce %s of revenue with %s of units, basin taps %s with %s, WCs %s with %s. The stop valve, first by units (%s), stays at %s of revenue. Satisfaction shows the same split: the average rating is %s with a %s low-rating share in bathroom cabinet sets and %s and %s in WCs; accessories and taps mostly rate 4.5 and above. In basin taps, first in revenue, units fell %s against 2025 Q4." % (
         ondalik(kat_d["Banyo Dolabı Seti"]["ciro_pay"]) + "%", ondalik(kat_d["Banyo Dolabı Seti"]["adet_pay"]) + "%", ondalik(kat_d["Lavabo Bataryası"]["ciro_pay"]) + "%", ondalik(kat_d["Lavabo Bataryası"]["adet_pay"]) + "%", ondalik(kat_d["Klozet"]["ciro_pay"]) + "%", ondalik(kat_d["Klozet"]["adet_pay"]) + "%", ondalik(kat_d["Ara Musluk"]["adet_pay"]) + "%", ondalik(kat_d["Ara Musluk"]["ciro_pay"]) + "%",
         ondalik(kat_d["Banyo Dolabı Seti"]["puan"]), ondalik(kat_d["Banyo Dolabı Seti"]["dusuk"]) + "%", ondalik(kat_d["Klozet"]["puan"]), ondalik(kat_d["Klozet"]["dusuk"]) + "%", "%d%%" % round(abs((kat_d["Lavabo Bataryası"]["q3"] / kat_d["Lavabo Bataryası"]["q4"] - 1) * 100))), "D31"),
 x("Çok satan ürünler: adet ve ciro katkısı", "Best-selling products: unit and revenue contribution"), T3,
 '<p><b>%s</b></p>' % x("Ciroya en çok katkı veren 15 ürün", "The 15 products contributing most to revenue") + T3b, '<p><b>%s</b></p>' % x("Fiyat bandına göre adet ve ciro payı", "Unit and revenue share by price band") + GFB + FB,
 marks([("at", "Adedin %%50'si %d üründen, %%80'i %d üründen gelmektedir; cironun %%50'si %d, %%80'i %d üründedir (satılan %d model kodu)" % (PA["adet50"], PA["adet80"], PA["ciro50"], PA["ciro80"], PA["urun"]),
         "%d products make up 50%% of units and %d make up 80%%; 50%% of revenue comes from %d and 80%% from %d products (%d model codes sold)" % (PA["adet50"], PA["adet80"], PA["ciro50"], PA["ciro80"], PA["urun"])),
        ("at", "2026 Q3'te satılan %d ürünün %d'inde güncel stok 0; bu ürünler Q3 adedinin %s'i, cirosunun %s'idir (çamaşır musluğu A45228, Master Slot el duşu, Integra klozet kapağı, Punto evye bataryası, Aquaheat Bliss 240)" % (ST["q3_urun"], ST["stok0"], yzd(ST["adet_pay"]), yzd(ST["ciro_pay"])),
         "%d of the %d products sold in 2026 Q3 have zero current stock; they account for %s of Q3 units and %s of revenue (washing machine valve A45228, Master Slot hand shower, Integra toilet seat, Punto kitchen tap, Aquaheat Bliss 240)" % (ST["stok0"], ST["q3_urun"], ondalik(ST["adet_pay"]) + "%", ondalik(ST["ciro_pay"]) + "%")),
        ("up", "500 TL altındaki ürünler adedin %s'ini ama cironun %s'ini; 2.000-10.000 TL bandı adedin %s'ini ve cironun %s'ini oluşturmaktadır" % (yzd(P["fiyat_bandi"][0]["adet_pay"]), yzd(P["fiyat_bandi"][0]["ciro_pay"]), yzd(P["fiyat_bandi"][3]["adet_pay"] + P["fiyat_bandi"][4]["adet_pay"]), yzd(P["fiyat_bandi"][3]["ciro_pay"] + P["fiyat_bandi"][4]["ciro_pay"])),
         "Products under 500 TL make up %s of units but %s of revenue; the 2,000-10,000 TL band makes up %s of units and %s of revenue" % (ondalik(P["fiyat_bandi"][0]["adet_pay"]) + "%", ondalik(P["fiyat_bandi"][0]["ciro_pay"]) + "%", ondalik(P["fiyat_bandi"][3]["adet_pay"] + P["fiyat_bandi"][4]["adet_pay"]) + "%", ondalik(P["fiyat_bandi"][3]["ciro_pay"] + P["fiyat_bandi"][4]["ciro_pay"]) + "%"))]),
 x("Görüntülenmeden satışa: ürün dönüşümü", "From views to sales: product conversion"), T4,
 insight("Ocak - Eylül 2026'da mağaza ürün sayfaları %s kez görüntülenmiş; sepete ekleme oranı %s, satışa dönüş %s'dir (2025'te %s ve %s). Görüntülenmenin en büyük payını banyo dolabı seti almakta ancak satışa dönüş %s'de kalmaktadır; klozet ve lavaboda da dönüşüm %%0,3'ün altındadır. Ara musluk (%s), tuvalet kağıtlığı ve banyo askısında dönüşüm %%2 civarında ve üzerindedir. %d ürünün %d'i bu dönemde hiç satış almamış ve görüntülenmenin %s'ini toplamıştır." % (
         k(D["satici_gor"]), yzd(D["sepet"], 2), yzd(D["cr"], 2), yzd(P["donusum25"]["sepet"], 2), yzd(P["donusum25"]["cr"], 2), yzd(next(r["cr"] for r in D["kat"] if r["kategori"] == "Banyo Dolabı Seti"), 2), yzd(next(r["cr"] for r in D["kat"] if r["kategori"] == "Ara Musluk"), 2), D["urun"], D["satissiz_urun"], yzd(D["satissiz_gor"])),
         "In January - September 2026 the store's product pages were viewed %s times; the add-to-basket rate is %s and conversion %s (%s and %s in 2025). Bathroom cabinet sets take the largest share of views but convert at only %s; conversion in WCs and washbasins is also below 0.3%%. Stop valves (%s), toilet roll holders and towel rails convert around 2%% or above. %d of %d products received no sale in this period and collected %s of views." % (
         k(D["satici_gor"]).replace(",", "."), ondalik(D["sepet"], 2) + "%", ondalik(D["cr"], 2) + "%", ondalik(P["donusum25"]["sepet"], 2) + "%", ondalik(P["donusum25"]["cr"], 2) + "%", ondalik(next(r["cr"] for r in D["kat"] if r["kategori"] == "Banyo Dolabı Seti"), 2) + "%", ondalik(next(r["cr"] for r in D["kat"] if r["kategori"] == "Ara Musluk"), 2) + "%", D["satissiz_urun"], D["urun"], ondalik(D["satissiz_gor"]) + "%"), "D31"),
 T4b,
 x("Müşteri profili ve sipariş yapısı", "Customer profile and order structure"), T5,
 marks([("at", "Siparişlerin %s-%s'i yeni müşteriden gelmektedir; mevcut müşteri siparişi %s-%s bandındadır" % (yzd(min(c["yeni"] for c in PR)), yzd(max(c["yeni"] for c in PR)), yzd(100 - max(c["yeni"] for c in PR)), yzd(100 - min(c["yeni"] for c in PR))),
         "%s-%s of orders come from new customers; orders from existing customers stay at %s-%s" % (ondalik(min(c["yeni"] for c in PR)) + "%", ondalik(max(c["yeni"] for c in PR)) + "%", ondalik(100 - max(c["yeni"] for c in PR)) + "%", ondalik(100 - min(c["yeni"] for c in PR)) + "%")),
        ("up", "Trendyol Plus üyelerinin sipariş payı %s'ten %s'e çıkmıştır" % (yzd(PR[0]["plus"]), yzd(PR[-1]["plus"])),
         "The order share of Trendyol Plus members rose from %s to %s" % (ondalik(PR[0]["plus"]) + "%", ondalik(PR[-1]["plus"]) + "%")),
        ("at", "5.000 TL ve üzeri siparişlerin payı %s'ten %s'e inmiştir" % (yzd(PR[0]["ust5"]), yzd(PR[-1]["ust5"])),
         "The share of orders of 5,000 TL and above fell from %s to %s" % (ondalik(PR[0]["ust5"]) + "%", ondalik(PR[-1]["ust5"]) + "%")),
        ("up", "İstanbul siparişlerin %s'i, Ankara %s, İzmir %s; 81 ilin tamamından sipariş gelmektedir; siparişlerin %s'i mağaza vitrininden, kalanı arama ve kategori listelerinden gelmektedir (2026)" % (yzd(P["il"][0]["pay"]), yzd(P["il"][1]["pay"]), yzd(P["il"][2]["pay"]), yzd(MG["vitrin_siparis_2026"])),
         "Istanbul accounts for %s of orders, Ankara %s, Izmir %s; orders come from all 81 provinces; %s of orders come from the store front, the rest from search and category lists (2026)" % (ondalik(P["il"][0]["pay"]) + "%", ondalik(P["il"][1]["pay"]) + "%", ondalik(P["il"][2]["pay"]) + "%", ondalik(MG["vitrin_siparis_2026"]) + "%")),
        ("up", "Mağaza takipçisi 1 Ocak 2025 - 29 Eylül 2026 döneminde %s'den %s'e çıkmıştır; Kasım 2025 kampanya ayında tek ayda %s takipçi kazanılmıştır" % (bin(MG["takipci_bas"]), bin(MG["takipci_son"]), bin(MG["kasim_takipci"])),
         "Store followers rose from %s to %s; %s followers were gained in the single campaign month of November 2025" % (f"{MG['takipci_bas']:,}", f"{MG['takipci_son']:,}", f"{MG['kasim_takipci']:,}"))]),
 x("Trendyol'un Enleri: kategori listelerinde VitrA (Eylül 2026)", "Trendyol Top Lists: VitrA in the category lists (September 2026)"), T6,
 insight("Dokuz kategorinin çok satan, ciro, favori, değerlendirme ve görüntülenme listelerinden okunan %s satırın %d'i VitrA veya Artema markalıdır; bunların %d'i (%s) resmi mağaza dışındaki satıcılara aittir. Resmi mağaza yalnızca klozet, klozet kapağı, rezervuar ve lavabo listelerinde yer almakta; mağaza cirosunda öne çıkan banyo mobilyası, batarya ve musluk ile duş sistemi listelerinde ve evye ile aksesuar listelerinde bulunmamaktadır. Rezervuar çok satan listesinin ikinci sırasında üçüncü taraf satıcıdaki 71 TL'lik VitrA boşaltma grubu contası yer almakta, listedeki 8 VitrA satırının 7'si conta ve iç takım parçasıdır. Resmi mağaza satırlarında buybox fiyatı ortalama satış fiyatının medyan %s altındadır. Listelerde görüntülenme en çok banyo aksesuarı ve mobilyada toplanmakta, çok satan medyan fiyatı aksesuarda 188 TL, bataryada 352 TL, duş sisteminde 285 TL'dir." % (
         bin(EO["satir"]), EO["vit"], EO["vit_3p"], yzd(EO["vit_3p"] / EO["vit"] * 100, 0), yzd(abs(EO["bb_fark_siz"]), 0)),
         "Of the %s rows read from the best-seller, revenue, favourite, review and view lists of nine categories, %d are VitrA or Artema-branded; %d of them (%s) belong to sellers other than the official store. The official store appears only in the WC, toilet seat, cistern and washbasin lists; it is absent from the bathroom furniture, taps and valves, shower system, sink and accessory lists, which produce a large part of the store's revenue. Second place in the cistern best-seller list is a 71 TL VitrA flush valve gasket at a third-party seller, and 7 of the 8 VitrA rows in that list are gasket and inner-mechanism parts. In the official store's rows the buybox price is a median %s below the average selling price. Views in the lists concentrate in bathroom accessories and furniture, and the best-seller median price is 188 TL in accessories, 352 TL in taps and 285 TL in shower systems." % (
         f"{EO['satir']:,}", EO["vit"], EO["vit_3p"], "%d%%" % round(EO["vit_3p"] / EO["vit"] * 100), "%d%%" % round(abs(EO["bb_fark_siz"]))), "D31"),
 x("Değerlendirmeler ve sorular: memnuniyet ve şikayet temaları", "Reviews and questions: satisfaction and complaint themes"), T7, T8, T8b,
 insight("%s ürün değerlendirmesinin ortalaması %s; değerlendirmelerin %s'i 5 puan, %s'i 1-2 puandır (Artema %s, VitrA %s). Olumlu yorumlar kalite, görünüm ve hediye jestinde toplanmaktadır. Düşük puanlı yorumlarda kırık ve hasarlı teslim (cam aksesuar, lavabo, klozet kapağı), eksik parça (vida, dübel, dolap ayağı, flex hortum, rozet), hasarlı üründe değişim yerine komple iade ve kargo kaynaklı hasar öne çıkmaktadır; ilan görselinde kapak ve rezervuar görünen klozetlerde kutudan yalnızca klozet çıkması da tekrar eden bir şikayettir. Ürün sorularının en büyük grubu uyumluluk ve ölçüdür; yanıtlarda farklı marka uyumluluğu paylaşılamamakta, parça talepleri pazaryeri kuralı nedeniyle Danışma Hattı'na yönlendirilmektedir. Satıcı değerlendirmesinin ortalaması %s; olumsuz etkilerde kusurlu veya hasarlı teslim, eksik ürün ve yanlış ürün ilk üç sıradadır." % (
         bin(DG["n"]), f1(DG["ort"]), yzd(DG["bes"], 0), yzd(DG["dusuk"]), f1(DG["artema"]), f1(DG["vitra"]), f1(SV["ort"])),
         "The %s product reviews average %s; %s of reviews are 5-star and %s are 1-2 stars (Artema %s, VitrA %s). Positive comments concentrate on quality, look and the gift gesture. Low-rated reviews highlight broken and damaged deliveries (glass accessories, basins, toilet seats), missing parts (screws, plugs, cabinet feet, flex hose, rosette), full returns instead of an exchange for damaged products and shipping damage; WCs whose listing image shows a seat and cistern but arrive with only the WC are also a recurring complaint. The largest group of product questions concerns compatibility and size; answers cannot share compatibility with other brands, and parts requests are referred to the Helpline because of the marketplace rule. Seller reviews average %s; defective or damaged delivery, missing products and wrong products rank first among negative effects." % (
         f"{DG['n']:,}", ondalik(DG["ort"]), "%d%%" % round(DG["bes"]), ondalik(DG["dusuk"]) + "%", ondalik(DG["artema"]), ondalik(DG["vitra"]), ondalik(SV["ort"])), "D31"),
 x("İptal, iade ve operasyon", "Cancellations, returns and operations"),
 marks([("at", "Kodlu iade nedenlerinin %s'i ölçü ve uyum (küçük / büyük geldi), %s'i kusurlu ürün; iptallerin %s'ini müşteri, %s'ini Trendyol yapmıştır" % (yzd(olcu), yzd(kusur), yzd(NE["Müşterinin İptal Ettiği"] / ipt_top * 100, 0), yzd(NE["Trendyol'un İptal Ettiği"] / ipt_top * 100, 0)),
         "%s of coded return reasons are size and fit (arrived too small / too big) and %s defective products; customers made %s of cancellations and Trendyol %s" % (ondalik(olcu) + "%", ondalik(kusur) + "%", "%d%%" % round(NE["Müşterinin İptal Ettiği"] / ipt_top * 100), "%d%%" % round(NE["Trendyol'un İptal Ettiği"] / ipt_top * 100))),
        ("at", "Hepsiburada'daki %d iptalin %s'inde neden \"müşteri daha ucuza buldu\", %s'inde \"satıcı ürünü sağlayamadı\" veya \"uzun temin süresi\"dir" % (HB["iptal_top"], yzd(ucuz), yzd((HB["iptal_neden"].get("Satıcı ürünü sağlayamadı", 0) + HB["iptal_neden"].get("Uzun temin süresi", 0)) / HB["iptal_top"] * 100)),
         "In %s of the %d cancellations on Hepsiburada the reason is \"customer found it cheaper\", in %s \"seller could not supply\" or \"long lead time\"" % (ondalik(ucuz) + "%", HB["iptal_top"], ondalik((HB["iptal_neden"].get("Satıcı ürünü sağlayamadı", 0) + HB["iptal_neden"].get("Uzun temin süresi", 0)) / HB["iptal_top"] * 100) + "%")),
        ("up", "Kargoya teslim süresi 2026'da ortalama %s saat, zamanında kargoya teslim oranı %s, müşteriye teslim %s saat; satıcı değerlendirmelerinde sipariş-teslim süresi medyanı %d gündür" % (f1(OP["2026"]["Kargoya Teslim Süresi"]), yzd(OP["2026"]["Kargoya Zamanında Teslim Oranı"]), f1(OP["2026"]["Müşteriye Teslim Süresi"]), SV["teslim_medyan"]),
         "In 2026 the average time to hand over to the carrier is %s hours, the on-time handover rate %s and delivery to the customer %s hours; the median order-to-delivery time in seller reviews is %d days" % (ondalik(OP["2026"]["Kargoya Teslim Süresi"]), ondalik(OP["2026"]["Kargoya Zamanında Teslim Oranı"]) + "%", ondalik(OP["2026"]["Müşteriye Teslim Süresi"]), SV["teslim_medyan"])),
        ("up", "Marka bilgisine göre siparişler tüm platformlarda ertesi gün, en geç 2 gün içinde kargoya verilmektedir; 30 desi altındaki ürünler Aras Kargo, 30 desi üstü ve bazı kırılabilir ürünler Ceva Lojistik ile teslim edilmektedir. Değerlendirmelerde hasar ve gecikme şikayetleri daha çok 30 desi altındaki gönderilerde anılmakta, büyük hacimli gönderilerin teslimatı olumlu değerlendirilmektedir",
         "According to the brand, orders on all platforms are handed to the carrier the next day and within 2 days at most; products under 30 desi go with Aras Kargo, those above 30 desi and some fragile products with Ceva Logistics. In reviews, damage and delay complaints are mostly mentioned for shipments under 30 desi, while deliveries of bulky items are rated positively")]),
 x("Hepsiburada: hak ediş yapısı ve görüntülenme", "Hepsiburada: settlement structure and views"),
 marks([("at", "Sipariş tutarının %s'i komisyon, %s'i kargo bedeli, %s'i tahsilat ve hizmet bedeli, %s'i kampanya indirimidir (01.08.2025 - 13.09.2026, %s sipariş, %s adet). Trendyol'da komisyon net ciroya oranla %s-%s bandındadır" % (yzd(HB["komisyon"]), yzd(HB["kargo"]), yzd(HB["tahsilat"] + HB["hizmet"]), yzd(HB["kampanya"]), bin(HB["siparis"]), bin(HB["adet"]), yzd(min(c["komisyon"] for c in P["ceyrek"])), yzd(max(c["komisyon"] for c in P["ceyrek"]))),
         "%s of order value is commission, %s shipping fees, %s collection and service fees and %s campaign discount (01.08.2025 - 13.09.2026, %s orders, %s units). On Trendyol commission is %s-%s of net revenue" % (ondalik(HB["komisyon"]) + "%", ondalik(HB["kargo"]) + "%", ondalik(HB["tahsilat"] + HB["hizmet"]) + "%", ondalik(HB["kampanya"]) + "%", f"{HB['siparis']:,}", f"{HB['adet']:,}", ondalik(min(c["komisyon"] for c in P["ceyrek"])) + "%", ondalik(max(c["komisyon"] for c in P["ceyrek"])) + "%")),
        ("at", "Hacimli ürünlerde kargo bedelinin sipariş tutarına oranı %15-30 bandına çıkmaktadır (çamaşır makinesi dolabı, aynalı dolap, hela taşı, dolap setleri)",
         "For bulky products the shipping fee rises to 15-30% of order value (washing machine cabinets, mirror cabinets, squat toilets, cabinet sets)"),
        ("at", "%s SKU'nun görüntülenme raporunda sepete ekleme %s, satışa dönüş %s; %d SKU satış almamış ve görüntülenmenin %s'ini toplamıştır (Shift T30 mat siyah batarya, Valarte ve İstanbul asma klozet, Shift T20 lavabo dolabı)" % (bin(HB["gor_sku"]), yzd(HB["sepet"]), yzd(HB["cr"], 2), HB["satissiz_sku"], yzd(HB["satissiz_gor"])),
         "In the view report for %s SKUs add-to-basket is %s and conversion %s; %d SKUs received no sale and collected %s of views (Shift T30 matt black tap, Valarte and İstanbul wall-hung WCs, Shift T20 basin unit)" % (f"{HB['gor_sku']:,}", ondalik(HB["sepet"]) + "%", ondalik(HB["cr"], 2) + "%", HB["satissiz_sku"], ondalik(HB["satissiz_gor"]) + "%")),
        ("up", "VitrA mağazası, ürünlerinin Hepsiburada'daki %s değerlendirmesinin %s'ini almaktadır; ürün puanı ortalaması %s" % (bin(HB["deg_hb"]), yzd(HB["deg_satici"] / HB["deg_hb"] * 100), f1(HB["puan"])),
         "The VitrA store receives %s of the %s reviews its products get on Hepsiburada; the average product rating is %s" % (ondalik(HB["deg_satici"] / HB["deg_hb"] * 100) + "%", f"{HB['deg_hb']:,}", ondalik(HB["puan"])))]),
 note("KISIT", "LIMITATION", ul_b([("Dönem:", "Period:", "Trendyol satış ve sipariş dağılımı 2025 Q4 - 2026 Q3 (Q3 29.09.2026'ya kadar); görüntülenme 2025 ve Ocak - Eylül 2026; ürün soruları ve Enleri listeleri Eylül 2026; Hepsiburada görüntülenme ve iptal raporları son 12 aydır.", "Trendyol sales and order distribution 2025 Q4 - 2026 Q3 (Q3 to 29.09.2026); views 2025 and January - September 2026; product questions and Top Lists September 2026; Hepsiburada view and cancellation reports cover the last 12 months."),
                                   ("Kapsam:", "Scope:", "Veriler yalnızca VitrA resmi mağazasına aittir; aynı ürünleri satan üçüncü taraf satıcıların satışı dahil değildir. Enleri listeleri kategori geneli ilk 50 ürünü gösterir, ekran görüntüsünden okunmuştur.", "The data belong only to the VitrA official store; sales of third-party sellers offering the same products are not included. Top Lists show the category-wide top 50 and were read from screenshots."),
                                   ("Sınıflandırma:", "Classification:", "Yorum ve soru temaları anahtar kelime ile sınıflandırılmıştır; bir kayıt birden fazla temaya girebilir. Satış raporunda %4,2 net adet ürün adı boş satırlardan gelmektedir, ad model koduyla eşlenmiştir.", "Review and question themes are keyword-based; a record can fall into more than one theme. 4.2% of net units in the sales report come from rows without a product name; names were matched by model code.")])),
 kaynak("Trendyol satıcı paneli (VitrA resmi mağazası): satış, sipariş dağılımı, mağaza, operasyon, favori-görüntüleme, ürün ve satıcı değerlendirmeleri, ürün ve sipariş soruları, Trendyol'un Enleri · Hepsiburada satıcı paneli: ürün performansı, görüntülenme, iptal, değerlendirme · 30.09.2026",
        "Trendyol seller panel (VitrA official store): sales, order distribution, store, operations, favourite-views, product and seller reviews, product and order questions, Trendyol Top Lists · Hepsiburada seller panel: product performance, views, cancellations, reviews · 30.09.2026", "D31"),
)
HTML = EK
