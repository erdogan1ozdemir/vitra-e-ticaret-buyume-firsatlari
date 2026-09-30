# -*- coding: utf-8 -*-
"""Makro bolumu ek: yillik banyo yenileme ve yeni konut banyosu tahmini, VitrA payi gostergeleri (D32). Kaynakli aralik + senaryo."""
from ortak import *
HANE = 26599261; ISKAN = (400000, 600000); BK = (1.1, 1.3)
SEN = [(3.0, "yaklaşık 33 yıllık döngü", "about a 33-year cycle"), (4.5, "yaklaşık 22 yıllık döngü", "about a 22-year cycle"), (6.0, "yaklaşık 17 yıllık döngü", "about a 17-year cycle")]
def m(v): return ("%.1f" % (v / 1e6)).replace(".", ",")
def me(v): return "%.1f" % (v / 1e6)
rows = []
for o, d_tr, d_en in SEN:
    yen = (HANE * o / 100 * BK[0], HANE * o / 100 * BK[1]); yk = (ISKAN[0] * BK[0], ISKAN[1] * BK[1])
    rows.append([n(yzd(o)), x(d_tr, d_en), n("%s - %s" % (m(yen[0]), m(yen[1]))), n("%s - %s" % (m(yk[0]), m(yk[1]))), n("<b>%s - %s</b>" % (m(yen[0] + yk[0]), m(yen[1] + yk[1])))])
    x("%s - %s" % (m(yen[0]), m(yen[1])), "%s - %s" % (me(yen[0]), me(yen[1]))); x("%s - %s" % (m(yk[0]), m(yk[1])), "%s - %s" % (me(yk[0]), me(yk[1]))); x("<b>%s - %s</b>" % (m(yen[0] + yk[0]), m(yen[1] + yk[1])), "<b>%s - %s</b>" % (me(yen[0] + yk[0]), me(yen[1] + yk[1])))
TS = tablo([th("Yıllık yenileme oranı", "Annual renovation rate", "Konutların yılda yüzde kaçında banyonun yenilendiği varsayımı; Türkiye için ölçülmüş bir oran bulunmadığından senaryo olarak verilmiştir.", "Assumed share of homes renovating the bathroom each year; given as a scenario because no measured rate exists for Turkey.", True),
            th("Karşılığı", "Equivalent", "Oranın ima ettiği ortalama yenileme döngüsü; Almanya'da yenilenmemiş banyoların ortalama yaşı 19,5 yıldır (VDS, 2017).", "The average renovation cycle implied by the rate; in Germany unrenovated bathrooms average 19.5 years (VDS, 2017)."),
            th("Yenilenen banyo (milyon)", "Renovated bathrooms (million)", "26,6 milyon hane × oran × konut başına 1,1-1,3 banyo.", "26.6 million households × rate × 1.1-1.3 bathrooms per home.", True),
            th("Yeni konut banyosu (milyon)", "New-home bathrooms (million)", "Yılda 0,4-0,6 milyon iskanlı daire × 1,1-1,3 banyo.", "0.4-0.6 million completed dwellings a year × 1.1-1.3 bathrooms.", True),
            th("Toplam (milyon banyo / yıl)", "Total (million bathrooms / year)", "Yenileme ve yeni konut toplamı.", "Renovation plus new homes.", True)], rows, "dar")
TK = tablo([th("Gösterge", "Indicator", "Tahminde kullanılan girdi.", "Input used in the estimate."), th("Değer", "Value", "Kaynaktaki değer.", "Value in the source.", True), th("Kaynak ve not", "Source and note", "Kaynak ve ölçüm türü.", "Source and type of measurement.")],
           [[x("Hane sayısı (2024)", "Households (2024)"), cell(HANE), x("TÜİK ADNKS; ölçüm", "TurkStat ABPRS; measured")],
            [x("Banyosu olan hane", "Households with a bathroom"), n("%98,8"), x("TÜİK Bina ve Konut Nitelikleri Araştırması 2021; ölçüm", "TurkStat Building and Dwelling Characteristics Survey 2021; measured")],
            [x("Konut satışları (2025)", "House sales (2025)"), cell(1688910), x("TÜİK; ilk el 540.786, ikinci el 1.148.124; ölçüm", "TurkStat; first-hand 540,786, second-hand 1,148,124; measured")],
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
 insight("Türkiye'de yıllık banyo yenileme adedini doğrudan ölçen bir kaynak bulunmamaktadır; tahmin hane sayısı, yeni konut ve yenileme döngüsü üzerinden kurulmuştur. 26,6 milyon hane, yılda 0,4-0,6 milyon iskanlı daire ve konut başına 1,1-1,3 banyo varsayımıyla yıllık banyo sayısı %4,5 yenileme oranında 1,8-2,3 milyon, %3 ile %6 arasında 1,3-2,9 milyon bandındadır. Seramik sağlık gereci iç pazarı (~13 milyon adet, 2023) bir banyo takımı 4 parça kabul edildiğinde yaklaşık 3 milyon banyo eşdeğerine karşılık gelmekte ve tahminle aynı büyüklük sınıfında kalmaktadır; proje ve tekil parça değişimi bu farkı açıklayabilir. VitrA payı için kamuya açık gösterge şirketin %30 beyanı ile seramik sağlık gereci kapasitesinin 2022-2023 sektör üretimine (21-25 milyon adet) oranıdır (%22-32).",
         "No source directly measures annual bathroom renovations in Turkey; the estimate is built from households, new homes and the renovation cycle. Assuming 26.6 million households, 0.4-0.6 million completed dwellings a year and 1.1-1.3 bathrooms per home, the annual bathroom count is 1.8-2.3 million at a 4.5% renovation rate and 1.3-2.9 million between 3% and 6%. The domestic sanitaryware market (~13 million units, 2023) corresponds to about 3 million bathroom equivalents if a set is four pieces, the same order of magnitude as the estimate; project demand and single-part replacement may explain the gap. For VitrA's share, the public indicators are the company's 30% statement and its sanitaryware capacity relative to 2022-2023 sector output (21-25 million units) (22-32%).", "D32"),
 TS, TK,
 note("NOT", "NOTE", ul_b([("Senaryo:", "Scenario:", "Yenileme oranı ölçüm değil varsayımdır; tablo yön göstermek için verilmiştir. Konut başına banyo sayısı Türkiye için bulunamamış, Almanya oranından (1,06-1,28) türetilmiştir.", "The renovation rate is an assumption, not a measurement; the table is indicative. Bathrooms per home could not be found for Turkey and is derived from the German ratio (1.06-1.28).")])),
 kaynak("TÜİK ADNKS, konut satış ve yapı izin istatistikleri, Bina ve Konut Nitelikleri Araştırması 2021 · Türkiye Seramik Federasyonu ve Sanayi Bakanlığı seramik sektörü notu · Eczacıbaşı basın bülteni ve faaliyet raporları · VDS-Forsa (Almanya) · 30.09.2026",
        "TurkStat ABPRS, house sales and building permit statistics, Building and Dwelling Characteristics Survey 2021 · Turkish Ceramics Federation and Ministry of Industry ceramics note · Eczacıbaşı press release and annual reports · VDS-Forsa (Germany) · 30.09.2026", "D32"),
)
