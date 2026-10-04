# -*- coding: utf-8 -*-
"""Makro bolumu ek: yillik banyo yenileme ve yeni konut banyosu tahmini, VitrA payi gostergeleri (D32). Kaynakli aralik + senaryo."""
from ortak import *
HANE = 26599261; ISKAN = 580000; BK = 1.2   # konut başına banyo: Almanya oranının (1,06-1,28) orta noktasına yakın tek değer
SEN = [(3.0, "yaklaşık 33 yıllık döngü", "about a 33-year cycle"), (4.5, "yaklaşık 22 yıllık döngü", "about a 22-year cycle"), (6.0, "yaklaşık 17 yıllık döngü", "about a 17-year cycle")]
def m(v): return ("%.1f" % (v / 1e6)).replace(".", ",")
def me(v): return "%.1f" % (v / 1e6)
rows = []
for o, d_tr, d_en in SEN:
    yen = HANE * o / 100 * BK; yk = ISKAN * BK
    rows.append([n(yzd(o)), x(d_tr, d_en), n(m(yen)), n(m(yk)), n("<b>%s</b>" % m(yen + yk))])
    x(m(yen), me(yen)); x(m(yk), me(yk)); x("<b>%s</b>" % m(yen + yk), "<b>%s</b>" % me(yen + yk))
TOP = {o: (HANE * o / 100 + ISKAN) * BK for o, _, _ in SEN}
def _dol(t):
    for a, b in (("__OE__", me(TOP[4.5])), ("__AE__", me(TOP[3.0])), ("__BE__", me(TOP[6.0])), ("__O__", m(TOP[4.5])), ("__A__", m(TOP[3.0])), ("__B__", m(TOP[6.0]))): t = t.replace(a, b)
    return t
TS = tablo([th("Yıllık yenileme oranı", "Annual renovation rate", "Konutların yılda yüzde kaçında banyonun yenilendiği varsayımı; Türkiye için ölçülmüş bir oran bulunmadığından senaryo olarak verilmiştir.", "Assumed share of homes renovating the bathroom each year; given as a scenario because no measured rate exists for Turkey.", True),
            th("Karşılığı", "Equivalent", "Oranın ima ettiği ortalama yenileme döngüsü; Almanya'da yenilenmemiş banyoların ortalama yaşı 19,5 yıldır (VDS, 2017).", "The average renovation cycle implied by the rate; in Germany unrenovated bathrooms average 19.5 years (VDS, 2017)."),
            th("Yenilenen banyo (milyon)", "Renovated bathrooms (million)", "26,6 milyon hane × oran × konut başına 1,2 banyo.", "26.6 million households × rate × 1.2 bathrooms per home.", True),
            th("Yeni konut banyosu (milyon)", "New-home bathrooms (million)", "Yılda ortalama 0,58 milyon iskanlı daire (2020 - Eylül 2024) × konut başına 1,2 banyo.", "An average of 0.58 million completed dwellings a year (2020 - Sep 2024) × 1.2 bathrooms per home.", True),
            th("Toplam (milyon banyo / yıl)", "Total (million bathrooms / year)", "Yenileme ve yeni konut toplamı.", "Renovation plus new homes.", True)], rows, "dar")
TK = tablo([th("Gösterge", "Indicator", "Tahminde kullanılan girdi.", "Input used in the estimate."), th("Değer", "Value", "Kaynaktaki değer.", "Value in the source.", True), th("Kaynak ve not", "Source and note", "Kaynak ve ölçüm türü.", "Source and type of measurement.")],
           [[x("Hane sayısı (2024)", "Households (2024)"), cell(HANE), x("TÜİK ADNKS; ölçüm", "TurkStat ABPRS; measured")],
            [x("Banyosu olan hane", "Households with a bathroom"), n("%98,8"), x("TÜİK Bina ve Konut Nitelikleri Araştırması 2021; ölçüm", "TurkStat Building and Dwelling Characteristics Survey 2021; measured")],
            [x("Konut satışları (2025)", "House sales (2025)"), cell(1760292), x("TÜİK (TCMB EVDS serisi); ilk el 570.812, ikinci el 1.189.480; ölçüm", "TurkStat (CBRT EVDS series); first-hand 570,812, second-hand 1,189,480; measured")],
            [x("İskanlı daire (2020 - Eylül 2024 ortalaması)", "Completed dwellings (2020 - Sep 2024 average)"), n("~580K"), x("TÜİK yapı izinleri; yıllık ortalama türetilmiştir", "TurkStat building permits; annual average derived")],
            [x("Seramik sağlık gereci üretimi (2023)", "Sanitaryware production (2023)"), n("21M"), x("Türkiye Seramik Federasyonu; ihracat 7,7M adet, iç pazar ~13M adet (türetilmiş)", "Turkish Ceramics Federation; exports 7.7M units, domestic market ~13M units (derived)")],
            [x("VitrA seramik sağlık gereci kapasitesi", "VitrA sanitaryware capacity"), n("5,7-6,7M"), x("Eczacıbaşı beyanı; yıllık adet", "Eczacıbaşı statement; units per year")],
            [x("VitrA pazar payı beyanı", "VitrA market share statement"), n("%30"), x("Eczacıbaşı basın bülteni, 2022; pazar tanımı (adet, değer, iç pazar) belirtilmemiştir", "Eczacıbaşı press release, 2022; market definition (units, value, domestic) not stated")]])
EK = """
<h3>%s</h3>
%s
<div class="two"><div>%s</div><div>%s</div></div>
%s
%s
""" % (
 x("Yıllık banyo yenileme ve yeni konut banyosu tahmini", "Estimate of annual bathroom renovations and new-home bathrooms"),
 insight(_dol("Türkiye'de yıllık banyo yenileme adedini doğrudan ölçen bir kaynak bulunmamaktadır; tahmin hane sayısı, yeni konut ve yenileme döngüsü üzerinden kurulmuştur. 26,6 milyon hane, yılda ortalama 0,58 milyon iskanlı daire ve konut başına 1,2 banyo varsayımıyla yıllık banyo sayısı %4,5 yenileme oranında yaklaşık __O__ milyon, %3 ile %6 arasında __A__-__B__ milyon bandındadır. Seramik sağlık gereci iç pazarı (~13 milyon adet, 2023) bir banyo takımı 4 parça kabul edildiğinde yaklaşık 3 milyon banyo eşdeğerine karşılık gelmekte ve tahminle aynı büyüklük sınıfında kalmaktadır; proje ve tekil parça değişimi bu farkı açıklayabilir. VitrA için kamuya açık iki gösterge bulunmaktadır: şirketin %30 pazar payı beyanı ve seramik sağlık gereci kapasitesinin 2023 sektör üretimine (21 milyon adet) oranı (%27-32); kapasite üretimle aynı şey değildir ve sektör üretimi ihracatı da içerdiğinden bu oran iç pazar payı olarak okunmamalıdır."),
         _dol("No source directly measures annual bathroom renovations in Turkey; the estimate is built from households, new homes and the renovation cycle. Assuming 26.6 million households, an average of 0.58 million completed dwellings a year and 1.2 bathrooms per home, the annual bathroom count is about __OE__ million at a 4.5% renovation rate and __AE__-__BE__ million between 3% and 6%. The domestic sanitaryware market (~13 million units, 2023) corresponds to about 3 million bathroom equivalents if a set is four pieces, the same order of magnitude as the estimate; project demand and single-part replacement may explain the gap. Two public indicators exist for VitrA: the company's 30% market share statement and its sanitaryware capacity relative to 2023 sector output (21 million units) (27-32%); capacity is not production and sector output includes exports, so this ratio should not be read as a domestic market share."), "D32"),
 TS, TK,
 note("NOT", "NOTE", ul_b([("Senaryo:", "Scenario:", "Yenileme oranı ölçüm değil varsayımdır; tablo yön göstermek için verilmiştir. Konut başına banyo sayısı Türkiye için bulunamadığından Almanya'daki oranın (1,06-1,28) ortasına yakın 1,2 kullanılmıştır.", "The renovation rate is an assumption, not a measurement; the table is indicative. As bathrooms per home could not be found for Turkey, 1.2 is used, close to the middle of the German ratio (1.06-1.28).")])),
 kaynak("TÜİK ADNKS, konut satış ve yapı izin istatistikleri, Bina ve Konut Nitelikleri Araştırması 2021 · Türkiye Seramik Federasyonu ve Sanayi Bakanlığı seramik sektörü notu · Eczacıbaşı basın bülteni ve faaliyet raporları · VDS-Forsa (Almanya) · 30.09.2026",
        "TurkStat ABPRS, house sales and building permit statistics, Building and Dwelling Characteristics Survey 2021 · Turkish Ceramics Federation and Ministry of Industry ceramics note · Eczacıbaşı press release and annual reports · VDS-Forsa (Germany) · 30.09.2026", "D32"),
)
