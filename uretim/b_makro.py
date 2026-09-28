# -*- coding: utf-8 -*-
"""Bolum: Makro ortam ve odeme gucu (TCMB EVDS)."""
from ortak import *
from rapor_parca1 import T, cizgi
import veri
K = A["kart"]; KA = A["kart_aylik"]; KOE = A["koe"]; TU = A["tuketici"]; KS = A["konut"]; BK = A["banka"]; HB = A["hane"]; KFE = A["kfe"]
def _koe_yoy(alan, ay):
    a, b = KOE.get("2026-%d" % ay), KOE.get("2025-%d" % ay)
    return (a[alan] / b[alan] - 1) * 100
koe_reel_ot = sum(KOE["2026-%d" % m]["genel_reel"] for m in range(1, 8)) / 7; koe_reel_ot25 = sum(KOE["2025-%d" % m]["genel_reel"] for m in range(1, 8)) / 7
koe_yoy = (koe_reel_ot / koe_reel_ot25 - 1) * 100
hane_yoy = (sum(KOE["2026-%d" % m]["hane_reel"] for m in range(1, 8)) / sum(KOE["2025-%d" % m]["hane_reel"] for m in range(1, 8)) - 1) * 100
def _tu(alan, t): return TU[t][alan]
def _ks(y): return sum(KS["%d-%d" % (y, m)]["toplam"] for m in range(1, 9))
def _ks_ip(y): return sum(KS["%d-%d" % (y, m)]["ipotekli"] for m in range(1, 9))
ks_yoy = (_ks(2026) / _ks(2025) - 1) * 100; ip_yoy = (_ks_ip(2026) / _ks_ip(2025) - 1) * 100
ip_pay26 = 100 * _ks_ip(2026) / _ks(2026)
kfe_yoy = (KFE["2026-8"]["kfe"] / KFE["2025-8"]["kfe"] - 1) * 100
aylar = veri.AYLAR
serpe = [(x("Mobilya ve dekorasyon", "Furniture and decoration"), "#E85F36", KA["mobilya_dekorasyon"]),
         (x("Yapı malzemeleri", "Building materials"), "#10332F", KA["yapi_malzemeleri"])]
GRAFIK = cizgi(serpe, y_etiket=x("Aylık kart harcaması · milyon TL", "Monthly card spending · TL million"), aylar=aylar)
def _yz(v): return yz(v)
tbl = tablo([th("Harcama kalemi", "Spending item", "BKM ve TCMB'nin haftalık sektörel kart harcama akımı; haftalar takvim ayına toplanmıştır.", "Weekly sectoral card spending flow from BKM and CBRT; weeks are summed into calendar months."),
             th("Oca-Ağu 2025", "Jan-Aug 2025", "Ocak - Ağustos 2025 toplam kart harcaması, milyar TL, nominal.", "January - August 2025 total card spending, TL billion, nominal.", True),
             th("Oca-Ağu 2026", "Jan-Aug 2026", "Ocak - Ağustos 2026 toplam kart harcaması, milyar TL, nominal.", "January - August 2026 total card spending, TL billion, nominal.", True),
             th("Değişim", "Change", "İki pencere arasındaki nominal yüzde değişim; enflasyon etkisi arındırılmamıştır.", "Nominal percentage change between the two windows; not adjusted for inflation.", True)],
            [[x(a, b), cell(K[kk]["y25"] / 1000), cell(K[kk]["y26"] / 1000), n(_yz(K[kk]["yoy"]))] for kk, a, b in
             [("toplam", "Tüm sektörler", "All sectors"), ("mobilya_dekorasyon", "Mobilya ve dekorasyon", "Furniture and decoration"), ("yapi_malzemeleri", "Yapı malzemeleri, hırdavat, nalburiye", "Building materials, hardware"),
              ("internet", "İnternet alışverişi (tüm sektörler)", "Online shopping (all sectors)"), ("elektronik", "Elektrik ve elektronik eşya", "Electrical and electronic goods"), ("market_avm", "Market ve alışveriş merkezleri", "Grocery and shopping malls")]])
guven = [(x("Tüketici güven endeksi", "Consumer confidence index"), "#10332F", [round(_tu("guven_endeksi", t), 1) for t in TU]),
         (x("Dayanıklı mal satın almaya uygunluk", "Suitability of buying durable goods"), "#E85F36", [round(_tu("dayanikli_mal_uygunluk", t), 1) for t in TU]),
         (x("Konut tamiratına harcama ihtimali", "Probability of spending on home repairs"), "#2E7D32", [round(_tu("konut_tamirat_harcama_ihtimali", t), 1) for t in TU])]
tu_aylar = ["%s-%02d" % tuple(map(int, t.split("-"))) for t in TU]
GRAFIK2 = cizgi(guven, y_etiket=x("Endeks (100 = nötr)", "Index (100 = neutral)"), aylar=tu_aylar)
son_t = list(TU)[-1]; onceki_t = list(TU)[-13]
bk = list(BK)[-1]; bk1 = list(BK)[-2]
HTML = """
<p class="lede">%s</p>
<div class="metrics">%s%s%s%s</div>
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
""" % (
 x("Banyo yenilemesi, dayanıklı mal harcamaları ve konut hareketliliğiyle birlikte hareket eden bir karar alanıdır. Bu bölümde TCMB EVDS üzerinden kart harcamaları, tüketici eğilimi, konut satışları ve banka kredi koşulları izlenmektedir; kategori talebindeki daralma (Bölüm 03) bu ortamla birlikte okunmalıdır.",
   "Bathroom renovation is a decision that moves together with durable goods spending and housing activity. This section tracks card spending, consumer tendency, house sales and bank lending conditions through CBRT EVDS; the contraction in category demand (Section 03) should be read alongside this environment."),
 metric("Mobilya ve dekorasyon kart harcaması", "Furniture and decoration card spending", yz(K["mobilya_dekorasyon"]["yoy"]), "Oca-Ağu 2026 / Oca-Ağu 2025, nominal; tüm sektörler %s" % yzd(K["toplam"]["yoy"]).replace("%", "+%"), "Jan-Aug 2026 / Jan-Aug 2025, nominal; all sectors +%s" % yzd(K["toplam"]["yoy"]).replace("%", "") + "%"),
 metric("Kartlı ödeme endeksi (reel)", "Card payment index (real)", yz(koe_yoy), "Oca-Tem 2026 / Oca-Tem 2025 ortalaması, enflasyondan arındırılmış; hane halkı %s" % ("+" + yzd(hane_yoy)), "Jan-Jul 2026 / Jan-Jul 2025 average, inflation-adjusted; households +%s" % yzd(hane_yoy).replace("%", "") + "%"),
 metric("Konut tamiratına harcama ihtimali", "Probability of spending on home repairs", ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t)).replace(".", ","), "Eylül 2026, endeks; bir yıl önce %s" % ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t)).replace(".", ","), "September 2026, index; one year earlier %s" % ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t))),
 metric("Konut satışları", "House sales", yz(ks_yoy), "Oca-Ağu 2026 / Oca-Ağu 2025; ipotekli satışlar %s, ipotekli payı %s" % (("+" if ip_yoy > 0 else "") + yzd(ip_yoy), yzd(ip_pay26)), "Jan-Aug 2026 / Jan-Aug 2025; mortgaged sales %s, mortgaged share %s" % (("+" if ip_yoy > 0 else "") + yzd(ip_yoy).replace("%", "") + "%", yzd(ip_pay26).replace("%", "") + "%")),
 x("Kart harcamaları: banyo ile ilişkili sektörler", "Card spending: bathroom-related sectors"),
 GRAFIK, tbl,
 insight("Mobilya ve dekorasyon harcaması Ocak - Ağustos 2026'da nominal olarak %s artarken tüm sektörler toplamı %s büyümüştür; banyo ile ilişkili iki kalem genel harcamanın gerisinde kalmıştır. Reel kartlı ödeme endeksinin aynı dönemde yalnızca %s artması, nominal büyümenin büyük bölümünün fiyat etkisi olduğunu göstermektedir. Kategori arama talebindeki daralma bu ortamla tutarlıdır: hane halkı harcamayı sürdürmekte, ancak yenileme kararı ertelenmektedir." % ("+" + yzd(K["mobilya_dekorasyon"]["yoy"]), "+" + yzd(K["toplam"]["yoy"]), "+" + yzd(koe_yoy)),
         "Furniture and decoration spending grew %s in nominal terms in January - August 2026 while the all-sector total grew %s; the two bathroom-related items lagged overall spending. The real card payment index rose only %s in the same period, which shows that most of the nominal growth is a price effect. The contraction in category search demand is consistent with this environment: households keep spending, but the renovation decision is being postponed." % ("+" + yzd(K["mobilya_dekorasyon"]["yoy"]).replace("%", "") + "%", "+" + yzd(K["toplam"]["yoy"]).replace("%", "") + "%", "+" + yzd(koe_yoy).replace("%", "") + "%"), "D6", "D10"),
 x("Tüketici eğilimi ve yenileme niyeti", "Consumer tendency and renovation intent"),
 GRAFIK2,
 insight("Tüketici güven endeksi Eylül 2026'da %s ile son iki yılın en yüksek seviyesine ulaşmıştır; dayanıklı mal satın almaya uygunluk göstergesi %s ve konut tamiratına harcama ihtimali %s seviyesindedir. Konut tamiratı göstergesi 2026 boyunca 40'ın üzerinde seyretmiş, bir yıl öncesine göre yaklaşık %s puan yükselmiştir. Ertelenen yenileme talebinin 2026 Q4 ve 2027 Q1 döneminde kademeli olarak geri gelebileceği değerlendirilebilir; e-ticaret kanalının bu dönemde taksit ve teslimat vaadiyle hazır olması fırsat sunmaktadır." % (("%.1f" % _tu("guven_endeksi", son_t)).replace(".", ","), ("%.1f" % _tu("dayanikli_mal_uygunluk", son_t)).replace(".", ","), ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t)).replace(".", ","), ("%.1f" % (_tu("konut_tamirat_harcama_ihtimali", son_t) - _tu("konut_tamirat_harcama_ihtimali", onceki_t))).replace(".", ",")),
         "The consumer confidence index reached %s in September 2026, its highest level in two years; the suitability of buying durable goods stands at %s and the probability of spending on home repairs at %s. The home repair indicator stayed above 40 throughout 2026 and rose about %s points year on year. Postponed renovation demand may return gradually in 2026 Q4 and 2027 Q1; the e-commerce channel being ready with instalment and delivery promises in that window presents an opportunity." % ("%.1f" % _tu("guven_endeksi", son_t), "%.1f" % _tu("dayanikli_mal_uygunluk", son_t), "%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t), "%.1f" % (_tu("konut_tamirat_harcama_ihtimali", son_t) - _tu("konut_tamirat_harcama_ihtimali", onceki_t))), "D7"),
 x("Konut hareketliliği ve kredi koşulları", "Housing activity and credit conditions"),
 tablo([th("Gösterge", "Indicator", "TCMB EVDS'den alınan seri.", "Series taken from CBRT EVDS."),
        th("Değer", "Value", "Belirtilen dönem için değer.", "Value for the stated period.", True),
        th("Karşılaştırma", "Comparison", "Bir önceki dönem veya bir yıl önceki değer.", "Previous period or year-earlier value.", True),
        th("Okuma", "Reading", "Banyo kategorisi açısından kısa yorum.", "Brief reading from the bathroom category's perspective.")],
       [[x("Konut satışları · Oca-Ağu 2026", "House sales · Jan-Aug 2026"), cell(_ks(2026)), n(x("Oca-Ağu 2025: %s (%s)" % (bin(_ks(2025)), "+" + yzd(ks_yoy)), "Jan-Aug 2025: %s (+%s)" % (bin(_ks(2025)), yzd(ks_yoy).replace("%", "") + "%"))), x("El değiştiren her konut banyo yenileme adayıdır; ikinci el satış payı %s" % yzd(100 * sum(KS["2026-%d" % m]["ikinci_el"] for m in range(1, 9)) / _ks(2026)), "Every home that changes hands is a bathroom renovation candidate; second-hand share %s" % (yzd(100 * sum(KS["2026-%d" % m]["ikinci_el"] for m in range(1, 9)) / _ks(2026)).replace("%", "") + "%"))],
        [x("İpotekli satışlar · Oca-Ağu 2026", "Mortgaged sales · Jan-Aug 2026"), cell(_ks_ip(2026)), n(x("Oca-Ağu 2025: %s (%s)" % (bin(_ks_ip(2025)), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy)), "Jan-Aug 2025: %s (%s)" % (bin(_ks_ip(2025)), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy).replace("%", "") + "%"))), x("Krediyle alınan konutta yenileme bütçesi sınırlı kalmakta; taksit ve set fiyatı bu segmentte belirleyici olabilir", "Renovation budgets stay limited in credit-financed homes; instalments and set prices can be decisive in this segment")],
        [x("Konut fiyat endeksi · Ağu 2026", "House price index · Aug 2026"), n(("%.1f" % KFE["2026-8"]["kfe"]).replace(".", ",")), n(x("Yıllık %s" % ("+" + yzd(kfe_yoy)), "Annual +%s" % (yzd(kfe_yoy).replace("%", "") + "%"))), x("Fiyat artışı yeni konut alımını sınırlarken mevcut konutun yenilenmesini görece cazip kılmaktadır", "Price increases limit new home purchases while making renovation of the existing home relatively attractive")],
        [x("Bireysel kredi standartları · %s" % bk, "Consumer credit standards · %s" % bk), n(("%.1f" % BK[bk]["diger_bireysel_standart"]).replace(".", ",")), n(x("%s: %s" % (bk1, ("%.1f" % BK[bk1]["diger_bireysel_standart"]).replace(".", ",")), "%s: %s" % (bk1, "%.1f" % BK[bk1]["diger_bireysel_standart"]))), x("Net yüzde; negatif değer bankaların ihtiyaç kredisi koşullarını gevşettiğini gösterir", "Net percentage; a negative value indicates banks eased consumer loan conditions")],
        [x("Bireysel kredi talebi · %s" % bk, "Consumer credit demand · %s" % bk), n(("%.1f" % BK[bk]["diger_bireysel_talep"]).replace(".", ",")), n(x("%s: %s" % (bk1, ("%.1f" % BK[bk1]["diger_bireysel_talep"]).replace(".", ",")), "%s: %s" % (bk1, "%.1f" % BK[bk1]["diger_bireysel_talep"]))), x("Dayanıklı mal harcamasının talep üzerindeki etkisi %s; talep tarafında belirgin bir ivme görülmemektedir" % ("%.1f" % BK[bk]["dayanikli_mal_etkisi"]).replace(".", ","), "Effect of durable goods spending on demand %s; no marked momentum is visible on the demand side" % ("%.1f" % BK[bk]["dayanikli_mal_etkisi"]))],
        [x("Hane halkı 12 ay enflasyon beklentisi · %s" % list(HB)[-1], "Household 12-month inflation expectation · %s" % list(HB)[-1]), n(yzd(HB[list(HB)[-1]]["enflasyon_beklenti_12ay"])), n(x("Dayanıklı mal fiyatı artacak diyenlerin payı %s" % yzd(HB[list(HB)[-1]]["dayanikli_fiyat_artacak_pay"]), "Share expecting durable goods prices to rise %s" % (yzd(HB[list(HB)[-1]]["dayanikli_fiyat_artacak_pay"]).replace("%", "") + "%"))), x("Fiyat artışı beklentisi öne çekilmiş alımı destekleyebilir; \"fiyat sabit\" ve \"taksit\" mesajları bu beklentiyle örtüşmektedir", "Expectation of price increases can support pulled-forward purchases; \"price locked\" and \"instalment\" messages align with this expectation")]]),
 kaynak("TCMB EVDS · kart harcamaları BKM haftalık akım (KT1, KT17, KT23, KT50, KT8, KT16); kartlı ödeme endeksi; Tüketici Eğilim Anketi; konut satış ve fiyat istatistikleri; Banka Kredileri Eğilim Anketi; hane halkı beklentileri · erişim %s" % veri.TARIH,
        "CBRT EVDS · card spending BKM weekly flow (KT1, KT17, KT23, KT50, KT8, KT16); card payment index; Consumer Tendency Survey; house sales and price statistics; Bank Lending Survey; household expectations · accessed %s" % veri.TARIH, "D6", "D7", "D8", "D9", "D10"),
 insight("Makro göstergeler birlikte okunduğunda tablo şu şekildedir: harcama nominal olarak büyümekte, reel olarak yatay seyretmekte; konut el değiştirme hızı artmakta; güven ve tamirat niyeti yükselmekte; kredi koşulları gevşemekte ancak kredi talebi henüz canlanmamıştır. Bu bileşim, ertelenmiş yenileme talebinin biriktiğine işaret etmektedir. E-ticaret kanalı için öncelik, talep geri geldiğinde ilk temas noktası olmayı sağlayacak fiyat, taksit ve teslimat netliğidir.",
         "Read together, the macro indicators show the following: spending grows in nominal terms and moves sideways in real terms; housing turnover is rising; confidence and repair intent are climbing; credit conditions are easing but credit demand has not yet revived. This combination points to accumulated, postponed renovation demand. The priority for the e-commerce channel is price, instalment and delivery clarity that will make it the first point of contact when demand returns."),
)
