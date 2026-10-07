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
# Kart harcaması grafiği: BKM/TCMB haftalık akımı takvim ayına toplanır; ay içindeki hafta sayısı 4 ya da 5 olduğundan ham aylık toplam
# 5 haftalı aylarda yapay zirve üretir. Grafikte her ay haftalık ortalama x (ayın gün sayısı / 7) ile aylığa çevrilir.
import calendar
_KH = veri.EVDS["kart_harcama_aylik_mnTL"]
KART_AY = ["%d-%02d" % (y_, m_) for y_ in (2023, 2024, 2025, 2026) for m_ in range(1, 13) if (y_, m_) <= (2026, 8)]
def _aylik(kk, ay):
    r = _KH[ay]; y_, m_ = map(int, ay.split("-"))
    return round(r[kk] / r["hafta"] * calendar.monthrange(y_, m_)[1] / 7 / 1000, 1)
KART_SERI = [("mobilya_dekorasyon", ("Mobilya ve dekorasyon", "Furniture and decoration"), "#E85F36"),
             ("yapi_malzemeleri", ("Yapı malzemeleri", "Building materials"), "#3E8F86"),
             ("elektronik", ("Elektronik eşya", "Electronic goods"), "#F5A623"),
             ("market_avm", ("Market ve AVM", "Grocery and malls"), "#2E7D32"),
             ("internet", ("İnternet alışverişi", "Online shopping"), "#7A8C89"),
             ("toplam", ("Tüm sektörler", "All sectors"), "#B9A6D6")]
serpe = [(x(*ad), renk, [_aylik(kk, a_) for a_ in KART_AY]) for kk, ad, renk in KART_SERI]
_nt = []
for _sk, (_, _, _s) in enumerate(serpe):
    for _y in (2023, 2024, 2025, 2026):
        _ix = [i for i, a_ in enumerate(KART_AY) if a_.startswith("%d-" % _y)]
        _p = max(_ix, key=lambda i: _s[i]); _b = min(_ix, key=lambda i: _s[i])
        for _i2, _tur, _yer in ((_p, "peak", "ust"), (_b, "base", "alt")):
            _v = ("%.1f" % _s[_i2]); _nt.append((_sk, _i2, x("%s %s" % (_v.replace(".", ","), _tur), "%s %s" % (_v, _tur)), _yer))
GRAFIK = cizgi(serpe, yukseklik=290, aylar=KART_AY, notlar=_nt, gizli=(2, 3, 4, 5), olcek=True, birim=("₺{v} milyar", "₺{v} billion"), ondalik=1,
               y_etiket=x("Aylık kart harcaması · milyar ₺, nominal · peak: yılın en yüksek ayı, base: en düşük ayı (2026: Oca - Ağu) · diğer harcama kalemleri lejanttan açılabilir",
                          "Monthly card spending · ₺ billion, nominal · peak: highest month of the year, base: lowest month (2026: Jan - Aug) · other spending items can be switched on in the legend"))
def _yz(v): return yz(v)
def _pt(v): return ("+" if v > 0 else ("-" if v < 0 else "")) + "%" + ("%.1f" % abs(v)).replace(".", ",")
def _pe(v): return ("+" if v > 0 else ("-" if v < 0 else "")) + ("%.1f" % abs(v)) + "%"
_AYAD = {1: ("Ocak", "January"), 2: ("Şubat", "February"), 3: ("Mart", "March"), 4: ("Nisan", "April"), 5: ("Mayıs", "May"), 6: ("Haziran", "June"), 7: ("Temmuz", "July"), 8: ("Ağustos", "August"), 9: ("Eylül", "September"), 10: ("Ekim", "October"), 11: ("Kasım", "November"), 12: ("Aralık", "December")}
def _donem(k_, en=False):
    y_, p_ = k_.split("-")
    if p_.startswith("Q"): return "%s %s" % (y_, p_)
    return "%s %s" % (_AYAD[int(p_)][1 if en else 0], y_)
tbl = tablo([th("Harcama kalemi", "Spending item", "BKM ve TCMB'nin haftalık sektörel kart harcama akımı; haftalar takvim ayına toplanmıştır.", "Weekly sectoral card spending flow from BKM and CBRT; weeks are summed into calendar months."),
             th("Oca-Ağu 2025 (milyar TL)", "Jan-Aug 2025 (TL billion)", "Ocak - Ağustos 2025 toplam kart harcaması, milyar TL, nominal.", "January - August 2025 total card spending, TL billion, nominal.", True),
             th("Oca-Ağu 2026 (milyar TL)", "Jan-Aug 2026 (TL billion)", "Ocak - Ağustos 2026 toplam kart harcaması, milyar TL, nominal.", "January - August 2026 total card spending, TL billion, nominal.", True),
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
 x("Banyo ürünlerine olan talebi etkileyen <b>genel ekonomik koşullar</b> dört gösterge grubuyla izlenmiştir; bu gruplar insanların <b>kartla ne kadar harcadığını</b>, <b>ekonomiye güvenlerini ve evlerini tamir ettirme niyetlerini</b>, <b>konut alım-satımını</b> ve <b>bankaların kredi verme koşullarını</b> kapsamaktadır. Banyo yenilemesi ertelenebilen bir harcama olduğu için bu göstergeler, kategori aramalarındaki daralmanın (Bölüm [[b:talep]]) arka planını açıklamaya yardımcı olmaktadır. Veriler Türkiye Cumhuriyet Merkez Bankası'nın veri sisteminden (TCMB EVDS) alınmıştır.",
   "The <b>general economic conditions</b> that affect demand for bathroom products are tracked with four indicator groups covering <b>how much people spend by card</b>, <b>their confidence in the economy and intention to have their homes repaired</b>, <b>house sales</b> and <b>banks' lending conditions</b>. Because bathroom renovation is a spending that can be postponed, these indicators help explain the background to the contraction in category searches (Section [[b:talep]]). The data come from the Central Bank of the Republic of Türkiye's data system (CBRT EVDS)."),
 metric("Mobilya ve dekorasyon kart harcaması · nominal değişim", "Furniture and decoration card spending · nominal change", yz(K["mobilya_dekorasyon"]["yoy"]),
        "Oca-Ağu 2026 / Oca-Ağu 2025, TL tutarı; tüm sektörler %s" % yzd(K["toplam"]["yoy"]).replace("%", "+%"), "Jan-Aug 2026 / Jan-Aug 2025, TL amount; all sectors +%s" % yzd(K["toplam"]["yoy"]).replace("%", "") + "%",
        ac=("Banka ve kredi kartlarıyla mobilya ve dekorasyon sektöründe yapılan harcamanın TL tutarıdır (BKM ve TCMB haftalık verisi). Ocak - Ağustos 2026 toplamı ₺%s milyar, 2025'in aynı aylarında ₺%s milyar'dır. Değişim nominaldir: fiyat artışı arındırılmadığı için artışın önemli bir bölümü enflasyondan kaynaklanmaktadır." % (bin(round(K["mobilya_dekorasyon"]["y26"] / 1000)), bin(round(K["mobilya_dekorasyon"]["y25"] / 1000))),
            "The TL amount spent by bank and credit card in the furniture and decoration sector (BKM and CBRT weekly data). The January - August 2026 total is ₺%s billion, against ₺%s billion in the same months of 2025. The change is nominal: price increases are not removed, so a large part of the rise comes from inflation." % (bin(round(K["mobilya_dekorasyon"]["y26"] / 1000)).replace(".", ","), bin(round(K["mobilya_dekorasyon"]["y25"] / 1000)).replace(".", ",")))),
 metric("Kartlı ödeme endeksi · enflasyondan arındırılmış (reel) değişim", "Card payment index · inflation-adjusted (real) change", yz(koe_yoy),
        "Oca-Tem 2026 ortalaması / Oca-Tem 2025 ortalaması; hane halkı alt endeksi %s" % ("+" + yzd(hane_yoy)), "Jan-Jul 2026 average / Jan-Jul 2025 average; household sub-index +%s" % yzd(hane_yoy).replace("%", "") + "%",
        ac=("TCMB'nin Kartlı Ödeme Endeksi, banka ve kredi kartlarıyla yapılan ödemelerin tutarını izlemektedir. Nominal seri TL tutarını olduğu gibi gösterir; reel seri aynı tutarı enflasyon etkisinden arındırır, yani fiyatlar sabit kalsaydı harcamanın ne kadar değişeceğini gösterir. %s: Ocak - Temmuz 2026 ortalaması, 2025'in aynı aylarının ortalamasından fiyat etkisi dışında bu oranda yüksektir. Hane halkı alt endeksi hanelerin kart ödemelerini kapsar (%s)." % ("+" + yzd(koe_yoy), "+" + yzd(hane_yoy)),
            "The CBRT Card Payments Index tracks the amount of payments made by bank and credit card. The nominal series shows the TL amount as it is; the real series removes the effect of inflation, showing how much spending would have changed at constant prices. %s: the January - July 2026 average is this much higher than the average of the same months of 2025, beyond the price effect. The household sub-index covers households' card payments (%s)." % ("+" + yzd(koe_yoy).replace("%", "") + "%", "+" + yzd(hane_yoy).replace("%", "") + "%"))),
 metric("Konut tamiratına harcama ihtimali · endeks (0-200)", "Probability of spending on home repairs · index (0-200)", ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t)).replace(".", ","),
        "Eylül 2026; 100'ün altı harcama düşünmeyenlerin ağır bastığını gösterir; bir yıl önce %s" % ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t)).replace(".", ","), "September 2026; below 100 means those not planning to spend outweigh the others; one year earlier %s" % ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t)),
        ac=("TÜİK-TCMB Tüketici Eğilim Anketi'nde hanelere önümüzdeki 12 ayda konutlarının tamiratına para harcama ihtimali sorulmaktadır; TCMB seri tanımında ısıtma sistemi, boya, mutfak ve banyo tamiri gibi harcamalar anılmaktadır. Yanıtlar 0-200 arasında bir endekse çevrilir: 100, harcama yapacağını ve yapmayacağını söyleyenlerin dengede olduğunu; 100'ün altı, yapmayacağını söyleyenlerin ağır bastığını gösterir. %s düşük bir düzeydir, ancak bir yıl önceki %s seviyesinden yükselmiştir." % (("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t)).replace(".", ","), ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t)).replace(".", ",")),
            "In the TURKSTAT-CBRT Consumer Tendency Survey, households are asked how likely they are to spend money on repairing their home over the next 12 months; the CBRT series definition mentions heating systems, painting and kitchen or bathroom repairs. Answers are converted into an index from 0 to 200: 100 means those who will spend and those who will not are balanced; below 100 means those who will not spend outweigh the others. %s is a low level, but it has risen from %s a year earlier." % ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t), "%.1f" % _tu("konut_tamirat_harcama_ihtimali", onceki_t)))),
 metric("Satılan konut sayısı · değişim", "Number of homes sold · change", yz(ks_yoy),
        "Oca-Ağu 2026: %s konut, 2025: %s; ipotekli satışlar %s, ipotekli payı %s" % (bin(_ks(2026)), bin(_ks(2025)), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy), yzd(ip_pay26)),
        "Jan-Aug 2026: %s homes, 2025: %s; mortgaged sales %s, mortgaged share %s" % (bin(_ks(2026)).replace(".", ","), bin(_ks(2025)).replace(".", ","), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy).replace("%", "") + "%", yzd(ip_pay26).replace("%", "") + "%"),
        ac=("TÜİK konut satış istatistiğidir (TCMB EVDS üzerinden). Ocak - Ağustos 2026'da Türkiye'de satılan konut sayısı, 2025'in aynı dönemine göre bu oranda değişmiştir. İpotekli satış, banka kredisiyle ve konut üzerine ipotek kurularak yapılan satıştır; payı, krediyle alınan konutların oranını gösterir.",
            "TURKSTAT house sales statistics (via CBRT EVDS). The number of homes sold in Türkiye in January - August 2026 changed by this rate compared with the same period of 2025. A mortgaged sale is one financed by a bank loan with a mortgage on the home; its share shows the proportion of homes bought on credit.")),
 x("Kart harcamaları: banyo ile ilişkili sektörler", "Card spending: bathroom-related sectors"),
 GRAFIK, tbl,
 insight("Mobilya ve dekorasyon harcaması Ocak - Ağustos 2026'da nominal olarak %s artarken tüm sektörler toplamı %s büyümüştür; banyo ile ilişkili iki kalem genel harcamanın gerisinde kalmıştır. Reel kartlı ödeme endeksinin Ocak - Temmuz döneminde yalnızca %s artması, nominal büyümenin büyük bölümünün fiyat etkisi olduğunu göstermektedir. Kategori arama talebindeki daralma bu ortamla tutarlıdır: hane halkının harcamayı sürdürdüğü, ancak yenileme kararını ertelediği değerlendirilebilir." % ("+" + yzd(K["mobilya_dekorasyon"]["yoy"]), "+" + yzd(K["toplam"]["yoy"]), "+" + yzd(koe_yoy)),
         "Furniture and decoration spending grew %s in nominal terms in January - August 2026 while the all-sector total grew %s; the two bathroom-related items lagged overall spending. The real card payment index rose only %s in January - July, which shows that most of the nominal growth is a price effect. The contraction in category search demand is consistent with this environment: households appear to keep spending while postponing the renovation decision." % (_pe(K["mobilya_dekorasyon"]["yoy"]), _pe(K["toplam"]["yoy"]), yzd(koe_yoy).replace("%", "") + "%"), "D6", "D10"),
 x("Tüketici eğilimi ve yenileme niyeti", "Consumer tendency and renovation intent"),
 GRAFIK2,
 insight("Tüketici güven endeksi Eylül 2026'da %s ile son iki yılın en yüksek seviyesine ulaşmıştır; dayanıklı mal satın almaya uygunluk göstergesi %s ve konut tamiratına harcama ihtimali %s seviyesindedir. Konut tamiratı göstergesi Mart 2026'dan bu yana 40'ın üzerinde seyretmiş, bir yıl öncesine göre yaklaşık %s puan yükselmiştir. Güven ve tamirat niyetindeki bu iyileşme henüz kategori aramalarına yansımamıştır (Bölüm [[b:talep]]); bu göstergeler talebin toparlanma zamanlaması için izlenebilir ve e-ticaret kanalının taksit ve teslimat vaadiyle hazır olması fırsat sunmaktadır." % (("%.1f" % _tu("guven_endeksi", son_t)).replace(".", ","), ("%.1f" % _tu("dayanikli_mal_uygunluk", son_t)).replace(".", ","), ("%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t)).replace(".", ","), ("%.1f" % (_tu("konut_tamirat_harcama_ihtimali", son_t) - _tu("konut_tamirat_harcama_ihtimali", onceki_t))).replace(".", ",")),
         "The consumer confidence index reached %s in September 2026, its highest level in two years; the suitability of buying durable goods stands at %s and the probability of spending on home repairs at %s. The home repair indicator has stayed above 40 since March 2026 and rose about %s points year on year. Postponed renovation demand may return gradually in 2026 Q4 and 2027 Q1; the e-commerce channel being ready with instalment and delivery promises in that window presents an opportunity." % ("%.1f" % _tu("guven_endeksi", son_t), "%.1f" % _tu("dayanikli_mal_uygunluk", son_t), "%.1f" % _tu("konut_tamirat_harcama_ihtimali", son_t), "%.1f" % (_tu("konut_tamirat_harcama_ihtimali", son_t) - _tu("konut_tamirat_harcama_ihtimali", onceki_t))), "D7"),
 x("Konut hareketliliği ve kredi koşulları", "Housing activity and credit conditions"),
 tablo([th("Gösterge", "Indicator", "TCMB EVDS'den alınan seri; birimi parantez içinde verilmiştir.", "Series taken from CBRT EVDS; the unit is given in brackets."),
        th("Değer", "Value", "Belirtilen dönem için değer.", "Value for the stated period.", True),
        th("Karşılaştırma", "Comparison", "Bir önceki dönem veya bir yıl önceki değer.", "Previous period or year-earlier value.", True),
        th("Okuma", "Reading", "Banyo kategorisi açısından kısa yorum.", "Brief reading from the bathroom category's perspective.")],
       [[x("Satılan konut sayısı (adet) · Oca-Ağu 2026", "Number of homes sold (units) · Jan-Aug 2026"), cell(_ks(2026)), n(x("Oca-Ağu 2025: %s (%s)" % (bin(_ks(2025)), _pt(ks_yoy)), "Jan-Aug 2025: %s (%s)" % (bin(_ks(2025)), _pe(ks_yoy)))), x("El değiştiren konutlar banyo yenilemesi için aday olarak değerlendirilebilir; ikinci el satış payı %s" % yzd(100 * sum(KS["2026-%d" % m]["ikinci_el"] for m in range(1, 9)) / _ks(2026)), "Homes that change hands can be seen as bathroom renovation candidates; second-hand share %s" % (yzd(100 * sum(KS["2026-%d" % m]["ikinci_el"] for m in range(1, 9)) / _ks(2026)).replace("%", "") + "%"))],
        [x("İpotekli satılan konut sayısı (adet) · Oca-Ağu 2026", "Number of mortgaged home sales (units) · Jan-Aug 2026"), cell(_ks_ip(2026)), n(x("Oca-Ağu 2025: %s (%s)" % (bin(_ks_ip(2025)), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy)), "Jan-Aug 2025: %s (%s)" % (bin(_ks_ip(2025)), ("+" if ip_yoy > 0 else "") + yzd(ip_yoy).replace("%", "") + "%"))), x("Krediyle alınan konutta yenileme bütçesi sınırlı kalabilir; taksit ve set fiyatı bu segmentte belirleyici olabilir", "Renovation budgets may stay limited in credit-financed homes; instalments and set prices can be decisive in this segment")],
        [x("Konut fiyat endeksi (2023 = 100) · Ağu 2026", "House price index (2023 = 100) · Aug 2026"), n(("%.1f" % KFE["2026-8"]["kfe"]).replace(".", ",")), n(x("Yıllık %s" % _pt(kfe_yoy), "Annual %s" % _pe(kfe_yoy))), x("Fiyat artışı yeni konut alımını sınırlarken mevcut konutun yenilenmesini görece cazip kılabilir", "Price increases limit new home purchases while making renovation of the existing home relatively more attractive")],
        [x("Bireysel kredi standartları (net yüzde) · %s" % _donem(bk), "Consumer credit standards (net percentage) · %s" % _donem(bk, True)), n(("%.1f" % BK[bk]["diger_bireysel_standart"]).replace(".", ",")), n(x("%s: %s" % (_donem(bk1), ("%.1f" % BK[bk1]["diger_bireysel_standart"]).replace(".", ",")), "%s: %s" % (_donem(bk1, True), "%.1f" % BK[bk1]["diger_bireysel_standart"]))), x("Net yüzde; negatif değer bankaların ihtiyaç kredisi koşullarını gevşettiğini gösterir", "Net percentage; a negative value indicates banks eased consumer loan conditions")],
        [x("Bireysel kredi talebi (net yüzde) · %s" % _donem(bk), "Consumer credit demand (net percentage) · %s" % _donem(bk, True)), n(("%.1f" % BK[bk]["diger_bireysel_talep"]).replace(".", ",")), n(x("%s: %s" % (_donem(bk1), ("%.1f" % BK[bk1]["diger_bireysel_talep"]).replace(".", ",")), "%s: %s" % (_donem(bk1, True), "%.1f" % BK[bk1]["diger_bireysel_talep"]))), x("Net yüzde; kredi talebini etkileyen faktörlerden dayanıklı mal harcamasının katkısı %s, talep tarafında belirgin bir ivme görülmemektedir" % ("%.1f" % BK[bk]["dayanikli_mal_etkisi"]).replace(".", ","), "Net percentage; the contribution of durable goods spending among factors affecting loan demand is %s, and no marked momentum is visible on the demand side" % ("%.1f" % BK[bk]["dayanikli_mal_etkisi"]))],
        [x("Hane halkı 12 ay enflasyon beklentisi · %s" % _donem(list(HB)[-1]), "Household 12-month inflation expectation · %s" % _donem(list(HB)[-1], True)), n(yzd(HB[list(HB)[-1]]["enflasyon_beklenti_12ay"])), n(x("Ocak 2026: %s; fiyatı en çok artacak gruplar arasında dayanıklı malları gösterenlerin payı %s (Ocak 2026: %s)" % (yzd(HB["2026-1"]["enflasyon_beklenti_12ay"]), yzd(HB[list(HB)[-1]]["dayanikli_fiyat_artacak_pay"]), yzd(HB["2026-1"]["dayanikli_fiyat_artacak_pay"])), "January 2026: %s; share naming durable goods among the groups whose prices will rise most %s (January 2026: %s)" % (("%.1f" % HB["2026-1"]["enflasyon_beklenti_12ay"]) + "%", ("%.1f" % HB[list(HB)[-1]]["dayanikli_fiyat_artacak_pay"]) + "%", ("%.1f" % HB["2026-1"]["dayanikli_fiyat_artacak_pay"]) + "%"))), x("Enflasyon beklentisi ve dayanıklı mal payı yılbaşından bu yana gerilemiştir; fiyat beklentisi alımları öne çekecek düzeyde görünmemektedir", "The inflation expectation and the durable goods share have fallen since the start of the year; price expectations do not appear strong enough to pull purchases forward")]]),
 kaynak("TCMB EVDS · kart harcamaları BKM haftalık akım (KT1, KT17, KT23, KT50, KT8, KT16), grafikte haftalık ortalama × ayın gün sayısı / 7 ile aylığa çevrilmiş, tabloda Ocak - Ağustos toplamı (iki yılda da 35 hafta); kartlı ödeme endeksi; Tüketici Eğilim Anketi; konut satış ve fiyat istatistikleri; Banka Kredileri Eğilim Anketi; hane halkı beklentileri",
        "CBRT EVDS · card spending BKM weekly flow (KT1, KT17, KT23, KT50, KT8, KT16), converted to months in the chart as weekly average × days in the month / 7, January - August total in the table (35 weeks in both years); card payment index; Consumer Tendency Survey; house sales and price statistics; Bank Lending Survey; household expectations", "D6", "D7", "D8", "D9", "D10"),
 insight("Harcama nominal olarak büyümekte, reel olarak sınırlı artmaktadır (kartlı ödeme endeksi %s); toplam konut satışları %s gerilerken ipotekli satışlar %s artmaktadır; güven ve tamirat niyeti yükselmekte, kredi koşulları gevşemekte ancak kredi talebi henüz canlanmamıştır. Bu bileşim, yenileme talebinin ertelenmiş olabileceği şeklinde okunabilir. E-ticaret kanalı için talep geri geldiğinde ilk temas noktası olabilmek adına fiyat, taksit ve teslimat netliği öncelik olarak değerlendirilebilir." % (_pt(koe_yoy), _pt(ks_yoy), _pt(ip_yoy)),
         "Spending grows in nominal terms and rises only modestly in real terms (card payment index %s); total house sales fell %s while mortgaged sales rose %s; confidence and repair intent are climbing, and credit conditions are easing but credit demand has not yet revived. This combination points to accumulated, postponed renovation demand. For the e-commerce channel, price, instalment and delivery clarity can be treated as priorities so that it becomes the first point of contact when demand returns." % (_pe(koe_yoy), ("%.1f" % abs(ks_yoy)) + "%", _pe(ip_yoy))),
)

from b_yenileme import EK as _EK
HTML = HTML + _EK
