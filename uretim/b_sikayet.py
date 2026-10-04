# -*- coding: utf-8 -*-
"""Bolum: Sikayetvar - satis sonrasi deneyim (VitrA ve Artema, son 24 ay)."""
from ortak import *
from grafik2 import isi, gruplu, f_pay
from rapor_parca1 import cizgi
import json, os
D = os.path.join(veri.V, "ham", "derin", "sikayetvar")
def J(f): return json.load(open(os.path.join(D, f), encoding="utf-8"))
TE = J("temalar.json"); META = TE.pop("_meta"); TA = J("temalar_artema.json"); TA.pop("_meta", None)
RK = J("rakip.json"); RK["E.C.A. / Serel"] = RK["E.C.A. (Serel dahil)"]; AY = J("aylik_ek.json"); TR6 = J("trend_6ay.json")["VitrA"]
N = META["metinli"]
TEMA_EN = {"Ürün kalitesi, sızıntı, kırılma": "Product quality, leaks, breakage", "Yetkili servis ve garanti": "Authorised service and warranty", "Montaj ve usta": "Installation and installer",
           "Mağaza ve bayi": "Store and dealer", "İletişim ve çağrı merkezi": "Contact and call centre", "Fiyat ve kampanya": "Price and campaign", "Yedek parça bulunamaması": "Spare part unavailable",
           "Pazaryeri ve üçüncü taraf satıcı": "Marketplace and third-party seller", "vitra.com.tr sipariş, teslimat ve iade": "vitra.com.tr order, delivery and returns", "Diğer / sınıflandırılamayan": "Other / unclassified"}
SIRA = sorted([k for k in TE], key=lambda k: -TE[k]["sayi"])
def alinti(a):
    m = a["metin"].strip()
    if len(m) > 150: m = m[:147].rsplit(" ", 1)[0] + "…"
    return u(a["url"], "“%s”" % m)
T_TEMA = tablo([th("Tema", "Theme", "Şikayet metnine anahtar ifadelerle atanan tema; bir şikayet birden fazla temaya girebilir.", "Theme assigned to the complaint text by key phrases; a complaint may fall into several themes."),
                th("Geçtiği şikayet", "Complaints mentioning", "Temanın geçtiği şikayet sayısı ve metinli 581 şikayet içindeki payı (çoklu etiket, toplam %100'ü aşar).", "Number of complaints mentioning the theme and its share of the 581 complaints with text (multi-label, totals exceed 100%).", True),
                th("Ana tema payı", "Main theme share", "Şikayetin tek ana teması olarak atandığı pay; tabloda yer almayan \"diğer / sınıflandırılamayan\" şikayetlerle (%5,5) birlikte toplam %100.", "Share where it is the single main theme of the complaint; together with the \"other / unclassified\" complaints not shown in the table (5.5%) the total is 100%.", True),
                th("Çözüldü işareti", "Marked resolved", "Temadaki şikayetlerde Şikayetvar'ın \"çözüldü\" işaretini taşıyan pay.", "Share of complaints in the theme carrying Şikayetvar's \"resolved\" mark.", True),
                th("Örnek şikayet", "Example complaint", "Kullanıcı yazımıyla birebir kısa alıntı; bağlantı şikayete gider.", "Short quotation with the user's own spelling; the link opens the complaint.")],
               [[x(k, TEMA_EN[k]), n("%d (%s)" % (TE[k]["sayi"], yzd(100 * TE[k]["pay"]))), n(yzd(100 * TE[k]["ana_tema_pay"])), n(yzd(100 * TE[k]["cozuldu_pay"])), alinti(TE[k]["alintilar"][0]) if TE[k]["alintilar"] else n("-")] for k in SIRA if k != "Diğer / sınıflandırılamayan"])
MK = [("VitrA", "vitra"), ("Artema", "artema"), ("Kale", "kale"), ("Creavit", "creavit"), ("E.C.A. / Serel", "eca"), ("Bocchi", "bocchi"), ("Geberit", "geberit")]
T_MK = tablo([th("Marka sayfası", "Brand page", "Şikayetvar marka sayfası; bağlantı sayfaya gider.", "Şikayetvar brand page; the link opens the page."),
              th("Toplam şikayet", "Total complaints", "Sayfanın bildirdiği toplam (son 3 yıl).", "Total reported by the page (last 3 years).", True),
              th("Son 1 yıl", "Last 12 months", "Son 12 aydaki şikayet sayısı.", "Complaints in the last 12 months.", True),
              th("Şikayetvar puanı", "Şikayetvar score", "Platformun 0-100 marka puanı; incelenen markalarda son 1 yıl çözüm oranına eşittir.", "The platform's 0-100 brand score; for the brands reviewed it equals the last-year resolution rate.", True),
              th("Çözüm oranı · tüm dönem / son 1 yıl", "Resolution rate · all time / last year", "Şikayet sahibinin sonuç anketinden hesaplanan çözüm oranı; Şikayetvar marka puanı son 1 yıl çözüm oranına eşittir.", "Resolution rate calculated from the complainant's outcome survey; the Şikayetvar brand score equals the last-year resolution rate.", True),
              th("E-ticaret temalı pay (ilk 3 sayfa)", "E-commerce share (first 3 pages)", "Marka sayfasının ilk 3 sayfasında sipariş, teslimat, iade veya pazaryeri geçen şikayet payı; küçük örneklem.", "Share of complaints on the first 3 pages mentioning orders, delivery, returns or marketplaces; small sample.", True)],
             [[(("<b>%s</b>" % u("https://www.sikayetvar.com/" + s, a)) if a == "VitrA" else u("https://www.sikayetvar.com/" + s, a)), cell(RK[a]["toplam_sikayet"]), cell(RK[a]["sikayet_son1yil"]), cell(RK[a]["puan_100"]), n("%%%d / %%%d" % (RK[a]["cozum_orani_tum_pct"], RK[a]["cozum_orani_son1yil_pct"])), n(yzd(100 * RK[a]["ilk3sayfa_eticaret_pay"]))] for a, s in sorted(MK, key=lambda m_: -RK[m_[0]]["puan_100"])])
aylar = sorted(AY["VitrA"])
RA = J("rakip_aylik.json")["markalar"]   # rakip marka sayfalari, ayni yontem (marka sayfasindaki tum sikayetler)
_SR = [("VitrA", "#10332F", AY["VitrA"]), ("Artema", "#E85F36", AY["Artema"]), ("Kale", "#1F4E8C", RA["Kale"]["aylik"]), ("Creavit", "#8A6FB0", RA["Creavit"]["aylik"]),
       ("Bocchi", "#9AA8A5", RA["Bocchi"]["aylik"]), ("Geberit", "#2E7D32", RA["Geberit"]["aylik"])]
_ECA = ("E.C.A. (Serel dahil)", "#B98B2E", RA["E.C.A. (Serel dahil)"]["aylik"])
from b_talep import sekmeler as _sek
def _gr(sl): return cizgi([(x(a, a), r, [d.get(m, 0) for m in aylar]) for a, r, d in sl], y_etiket=x("Aylık şikayet sayısı · Şikayetvar", "Monthly complaints · Şikayetvar"), aylar=aylar)
GRAFIK = _sek([("Banyo markaları", "Bathroom brands", _gr(_SR)), ("E.C.A. dahil (kombi ve ısıtma şikayetleri de içerir)", "Including E.C.A. (also covers boiler and heating complaints)", _gr(_SR + [_ECA]))], "gtabs")
def _t12(d, i): return sum(d.get(m, 0) for m in aylar[i * 12:(i + 1) * 12])
DON = [("2024-10/2025-03", "Eki 2024 - Mar 2025", "Oct 2024 - Mar 2025"), ("2025-04/2025-09", "Nis - Eyl 2025", "Apr - Sep 2025"), ("2025-10/2026-03", "Eki 2025 - Mar 2026", "Oct 2025 - Mar 2026"), ("2026-04/2026-09", "Nis - Eyl 2026", "Apr - Sep 2026")]
KOD = [("kalite", "Ürün kalitesi", "Product quality"), ("servis_garanti", "Servis ve garanti", "Service and warranty"), ("montaj", "Montaj ve usta", "Installation and installer"), ("iletisim", "İletişim", "Contact"), ("magaza_bayi", "Mağaza ve bayi", "Store and dealer"), ("yedek_parca", "Yedek parça", "Spare parts"), ("fiyat_kampanya", "Fiyat ve kampanya", "Price and campaign"), ("pazaryeri", "Pazaryeri", "Marketplace"), ("vitra_online", "vitra.com.tr", "vitra.com.tr")]
def pd(k, d): v = TR6[d].get(k, 0); return n("%d (%s)" % (v, yzd(100 * v / TR6[d]["n"])))
T_DON = tablo([th("Tema", "Theme", "Temanın geçtiği şikayet sayısı ve dönem içindeki payı.", "Number of complaints mentioning the theme and its share within the period.")] +
              [th(a, b, "Dönemdeki metinli şikayet sayısı: %d." % TR6[k]["n"], "Complaints with text in the period: %d." % TR6[k]["n"], True) for k, a, b in DON],
              [[x(a, b)] + [pd(k, d) for d, _, _ in DON] for k, a, b in KOD], "dar")
KAN = [("vitra.com.tr", 22, 3.8, 0, 0.0), ("Pazaryeri platformu (Trendyol, Hepsiburada, n11, Amazon)", 21, 3.6, 33, 11.3), ("Perakende zinciri (Koçtaş, Bauhaus, Tekzen, Evdema)", 74, 12.7, 57, 19.6), ("Bayi, yapı market, yerel satıcı", 82, 14.1, 14, 4.8), ("Kanal belirtilmemiş", 395, 68.0, 189, 64.9)]
KAN_EN = {"vitra.com.tr": "vitra.com.tr", "Pazaryeri platformu (Trendyol, Hepsiburada, n11, Amazon)": "Marketplace platform (Trendyol, Hepsiburada, n11, Amazon)", "Perakende zinciri (Koçtaş, Bauhaus, Tekzen, Evdema)": "Retail chain (Koçtaş, Bauhaus, Tekzen, Evdema)", "Bayi, yapı market, yerel satıcı": "Dealer, DIY store, local seller", "Kanal belirtilmemiş": "Channel not stated"}
T_KAN = tablo([th("Satın alma kanalı", "Purchase channel", "Şikayet metninde anılan satın alma kanalı; bir şikayet birden fazla kanalı anabileceğinden satırların toplamı metinli şikayet sayısını aşabilir.", "Purchase channel mentioned in the complaint text; as a complaint can mention more than one channel, the rows can add up to more than the number of complaints with text."),
               th("VitrA", "VitrA", "Şikayet sayısı ve metinli şikayetler içindeki pay.", "Number of complaints and share of complaints with text.", True),
               th("Artema", "Artema", "Şikayet sayısı ve pay (n=291).", "Number of complaints and share (n=291).", True)],
              [[x(a, KAN_EN[a]), n("%d (%s)" % (b, yzd(c))), n("%d (%s)" % (d, yzd(e)))] for a, b, c, d, e in KAN], "dar")
PAR = [("Sifon mekanizması, gider, süzgeç", "Flush mechanism, drain, strainer", 25, 14), ("Klozet kapağı, menteşe, vida", "Toilet seat, hinge, screw", 20, 1), ("Rezervuar, şamandıra, kumanda paneli", "Cistern, float, flush plate", 14, 0), ("Batarya, kartuş, musluk parçası", "Tap, cartridge, valve part", 12, 23), ("Duş başlığı, hortum, duş seti parçası", "Shower head, hose, shower set part", 9, 7), ("Mobilya menteşesi, çekmece, ayna", "Furniture hinge, drawer, mirror", 3, 0)]
T_PAR = tablo([th("Parça grubu", "Part group", "Yedek parça temalı şikayetlerde anılan parça grubu.", "Part group mentioned in spare-part themed complaints."), th("VitrA", "VitrA", "Şikayet sayısı (59 yedek parça şikayeti içinde).", "Number of complaints (within 59 spare-part complaints).", True), th("Artema", "Artema", "Şikayet sayısı (33 içinde).", "Number of complaints (within 33).", True)],
              [[x(a, b), cell(c), cell(d)] for a, b, c, d in PAR], "dar")
IFA = [("Servis, kontrol veya \"haksız\" ücret", "Service, inspection or \"unfair\" fee", 75, 12.9), ("Garanti reddi gerekçesi: kullanıcı veya usta hatası", "Warranty refusal reason: user or installer error", 75, 12.9), ("Tekrar almama, tavsiye etmeme", "Will not buy again, will not recommend", 92, 15.8), ("Parça veya ürün fiyatı", "Part or product price", 62, 10.7), ("Marka güveniyle satın alma", "Purchase on brand trust", 57, 9.8), ("İade ve para iadesi süresi", "Return and refund period", 24, 4.1), ("Yedek parçanın tek satılmaması, komple set önerisi", "Spare part not sold alone, complete set suggested", 11, 1.9), ("Ücretsiz montaj vaadi sonrası ücret talebi", "Fee requested after free installation promise", 7, 1.2)]
T_IFA = tablo([th("İfade grubu", "Statement group", "Şikayet metinlerinde geçen ifade grubu (anahtar kelimeyle).", "Statement group appearing in complaint texts (by keyword)."), th("Şikayet", "Complaints", "VitrA metinli şikayetleri içinde sayı.", "Count within VitrA complaints with text.", True), th("Pay", "Share", "Metinli 581 şikayet içindeki pay.", "Share of the 581 complaints with text.", True)],
              [[x(a, b), cell(c), n(yzd(d))] for a, b, c, d in sorted(IFA, key=lambda t_: -t_[2])], "dar")
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
<div class="two"><div><h3>%s</h3>%s%s</div><div><h3>%s</h3>%s</div></div>
%s
<h3>%s</h3>
%s
%s
%s
""" % (
 x("Şikayetvar'daki VitrA (978) ve Artema (544) marka sayfaları okunmuş; son 24 aydaki 600 VitrA ve 294 Artema şikayetinden yayından kaldırılmamış 581 VitrA ve 291 Artema şikayetinin metni tema, satın alma kanalı ve ifade grupları için taranmıştır. Şikayetler tek taraflı beyanlardır ve şikayet yazmayan çoğunluğu temsil etmez; paylar yön gösterir, kesin ölçüm değildir. Alıntılar kullanıcının yazımıyla birebir korunmuş, ad ve iletişim bilgileri çıkarılmıştır.",
   "The VitrA (978) and Artema (544) brand pages on Şikayetvar were read; the text of the 581 VitrA and 291 Artema complaints still published, out of 600 and 294 from the last 24 months, was scanned for themes, purchase channel and statement groups. Complaints are one-sided statements and do not represent the majority who do not write complaints; shares indicate direction, not exact measurement. Quotations keep the user's own spelling; names and contact details were removed."),
 kpi_kart(k(META["toplam_pencere"]), "VitrA şikayeti · Eki 2024 - Eyl 2026 · aylık 25 civarı, tepe Ara 2024 (39)", "VitrA complaints · Oct 2024 - Sep 2026 · about 25 per month, peak Dec 2024 (39)"),
 kpi_kart("%d / 100" % RK["VitrA"]["puan_100"], "Şikayetvar marka puanı · Kale %d, Creavit %d, Geberit %d" % (RK["Kale"]["puan_100"], RK["Creavit"]["puan_100"], RK["Geberit"]["puan_100"]), "Şikayetvar brand score · Kale %d, Creavit %d, Geberit %d" % (RK["Kale"]["puan_100"], RK["Creavit"]["puan_100"], RK["Geberit"]["puan_100"]), "dn"),
 kpi_kart(yzd(100 * TE["Yetkili servis ve garanti"]["pay"]), "Servis ve garanti sürecinin geçtiği şikayet payı · ürün kalitesi %s" % yzd(100 * TE["Ürün kalitesi, sızıntı, kırılma"]["pay"]), "Share of complaints mentioning the service and warranty process · product quality %s" % yzd(100 * TE["Ürün kalitesi, sızıntı, kırılma"]["pay"]).replace("%", "").replace(",", ".") + "%", "hi"),
 kpi_kart("%8,1 → %17,8", "Yedek parça temasının payı · Eki 2024 - Mar 2025'ten Nis - Eyl 2026'ya", "Share of the spare-part theme · from Oct 2024 - Mar 2025 to Apr - Sep 2026", "hi"),
 x("Marka sayfası göstergeleri ve rakipler", "Brand page indicators and competitors"), T_MK,
 insight("VitrA'nın Şikayetvar puanı 18, Artema'nın 15'tir; Kale 36, Creavit 32 ve Geberit 78 puandadır. VitrA'nın toplam şikayet hacmi (978) Kale (649) ve Creavit'in (585) üzerindedir (şikayet sayıları satış hacmine göre normalize edilmemiştir); E.C.A. sayfası (3.800) kombi ve ısıtma ürünlerini de kapsadığı için doğrudan karşılaştırılmaz. Çözüm oranı VitrA'da tüm dönemde %31, son 12 ayda %18'e inmiştir. E-ticaret temalı şikayet payı ilk 3 sayfada VitrA'da %10,0 ve Artema'da %14,3 ile rakiplerin (%1,4 - %5,9) üzerindedir; örneklem küçüktür ve dönemler markaya göre değişir. İncelenen 6 VitrA şikayet sayfasında marka yanıtı bloğu bulunmamakta; VitrA ve Artema marka sayfalarında yanıt oranı ve ortalama yanıt süresi göstergesi de yer almamaktadır (Geberit sayfasında %13 yanıt oranı ve 63 saat görünmektedir).",
         "VitrA's Şikayetvar score is 18 and Artema's 15; Kale scores 36, Creavit 32 and Geberit 78. VitrA's total complaint volume (978) exceeds Kale (649) and Creavit (585) (complaint counts are not normalised for sales volume); the E.C.A. page (3,800) also covers boilers and heating and is not directly comparable. VitrA's resolution rate is 31% over the whole period and fell to 18% in the last 12 months. The share of e-commerce themed complaints on the first 3 pages is 10.0% for VitrA and 14.3% for Artema, above the competitors (1.4% - 5.9%); the sample is small and the periods differ by brand. None of the 6 VitrA complaint pages examined carries a brand reply block, and the VitrA and Artema brand pages show no reply rate or average reply time indicator (the Geberit page shows a 13% reply rate and 63 hours).", "D24", "D28"),
 x("Aylık şikayet serisi", "Monthly complaint series"), GRAFIK,
 insight("VitrA'da ilk 12 ay ve son 12 ay 300'er şikayetle yataydır; tepe aylar Aralık 2024 (39) ve Nisan 2026 (38), en düşük ay Kasım 2025 (14)'tür. Artema'da seri Ekim 2024'teki 24'ten 2026'da 4-16 bandına gerilemiştir. Rakiplerde son 12 ayda Kale %d (önceki 12 ay %d), Creavit %d (%d), Bocchi %d (%d) ve Geberit %d (%d) şikayet almıştır; Kale ve Geberit'te şikayet sayısı hafif artarken Creavit ve Bocchi'de azalmıştır. Aylık şikayet sayısı satış hacmine göre normalize edilmediği için sezon etkisi ayrıştırılamamaktadır." % (_t12(RA["Kale"]["aylik"], 1), _t12(RA["Kale"]["aylik"], 0), _t12(RA["Creavit"]["aylik"], 1), _t12(RA["Creavit"]["aylik"], 0), _t12(RA["Bocchi"]["aylik"], 1), _t12(RA["Bocchi"]["aylik"], 0), _t12(RA["Geberit"]["aylik"], 1), _t12(RA["Geberit"]["aylik"], 0)),
         "For VitrA the first 12 and the last 12 months are flat at 300 complaints each; the peak months are December 2024 (39) and April 2026 (38), the lowest November 2025 (14). For Artema the series has fallen from 24 in October 2024 to a 4-16 band in 2026. Among competitors, in the last 12 months Kale received %d complaints (previous 12 months %d), Creavit %d (%d), Bocchi %d (%d) and Geberit %d (%d); complaints rose slightly at Kale and Geberit and fell at Creavit and Bocchi. Monthly counts are not normalised by sales volume, so seasonal effects cannot be separated." % (_t12(RA["Kale"]["aylik"], 1), _t12(RA["Kale"]["aylik"], 0), _t12(RA["Creavit"]["aylik"], 1), _t12(RA["Creavit"]["aylik"], 0), _t12(RA["Bocchi"]["aylik"], 1), _t12(RA["Bocchi"]["aylik"], 0), _t12(RA["Geberit"]["aylik"], 1), _t12(RA["Geberit"]["aylik"], 0)), "D24"),
 x("Şikayet temaları ve örnek alıntılar", "Complaint themes and example quotations"), T_TEMA,
 insight("Satış sonrası deneyim şikayetlerin ağırlık merkezidir: servis, yedek parça, montaj ve iletişim temalarından en az birini taşıyan şikayet 447 / 581'dir (%76,9). Ürün kalitesi temalı 380 şikayetin 223'ü (%58,7) aynı zamanda servis ve garanti sürecini anlatmaktadır; arızanın ardından yaşanan süreç de şikayetin önemli bir parçasıdır. vitra.com.tr siparişi (22) ve pazaryeri (tema olarak 24, satın alma kanalı olarak 21) temalı şikayetler sınırlıdır; perakende zinciri (74) ve bayi (82) daha sık anılmaktadır. Yalnızca 3 temada çözüldü işareti %8'i aşmaktadır; marka sayfasındaki çözüm oranı (%31 / %18) ise yalnızca sonuç anketini yanıtlayan şikayet sahiplerinden hesaplandığı için daha yüksektir.",
         "The after-sales experience is the centre of gravity: 447 of 581 complaints (76.9%) carry at least one of the service, spare part, installation and contact themes. 223 of the 380 product quality complaints (58.7%) also describe the service and warranty process; the process after the fault is also a significant part of the complaint. vitra.com.tr order (22) and marketplace (24 as a theme, 21 as a purchase channel) themed complaints are limited; retail chains (74) and dealers (82) are mentioned more often. The resolved mark exceeds 8% in only 3 themes; the resolution rate on the brand page (31% / 18%) is higher because it is calculated only from complainants who answered the outcome survey.", "D24"),
 x("Altı aylık dönemlerde tema geçişi", "Theme shift by six-month period"), isi(T_DON),
 insight("Eki 2024 - Mar 2025 döneminden Nis - Eyl 2026 dönemine yedek parça teması %8,1'den %17,8'e, montaj ve usta teması %27,0'dan %48,5'e yükselmiştir; yedek parçadaki artış son altı aylık dönemde (%7,9'dan %17,8'e) yoğunlaşmaktadır. Pazaryeri temalı şikayet 2'den 9'a çıkmış, vitra.com.tr teması 5-6 bandında kalmıştır. 11 şikayette parçanın tek başına satılmadığı ve komple set önerildiği anlatılmaktadır; bu bulgu, sitede yedek parça kategorisinin bulunmaması ve eski yedek parça sayfasının tek ürünlü bir kategoriye yönlenmesiyle birlikte okunabilir.",
         "From Oct 2024 - Mar 2025 to Apr - Sep 2026 the spare-part theme rose from 8.1% to 17.8% and the installation and installer theme from 27.0% to 48.5%; the spare-part increase is concentrated in the last six-month period (7.9% to 17.8%). Marketplace themed complaints rose from 2 to 9 while the vitra.com.tr theme stayed in the 5-6 band. In 11 complaints the part is described as not sold on its own with a complete set suggested; this finding can be read together with the absence of a spare-parts category on the site and the old spare-parts page redirecting to a one-product category.", "D24"),
 x("Satın alma kanalı", "Purchase channel"), T_KAN,
 insight("Koçtaş 48, Bauhaus 18 ve bayi veya yapı market 82 VitrA şikayetinde geçmektedir; pazaryeri platformu 21'de. Alıntılarda mağazanın \"malı bizden aldınız, hizmet değil\" diyerek sorumluluk almadığı, \"bayi muhatabım yok\" ifadesi ve iade için üreticiden onay beklendiği anlatılmaktadır. Artema'da pazaryeri payı (%11,3) VitrA'nın ~3x'idir.",
         "Koçtaş appears in 48, Bauhaus in 18 and dealers or DIY stores in 82 VitrA complaints; marketplace platforms in 21. The quotations describe stores declining responsibility (\"malı bizden aldınız, hizmet değil\" - you bought the goods from us, not the service), the statement \"bayi muhatabım yok\" (I have no dealer to turn to) and waiting for the manufacturer's approval for returns. Artema's marketplace share (11.3%) is ~3x VitrA's.", "D24"),
 x("Yedek parça: hangi parçalar?", "Spare parts: which parts?"), T_PAR,
 insight("Yedek parçada en sık anılan gruplar sifon mekanizması (25), klozet kapağı ve menteşe (20) ile rezervuar ve şamandıradır (14); Artema'da batarya kartuşu (23) öndedir.",
         "The most mentioned spare-part groups are the flush mechanism (25), toilet seat and hinge (20) and cistern and float (14); for Artema tap cartridges (23) lead.", "D24"),
 x("Ücret, garanti ve güven ifadeleri", "Fee, warranty and trust statements"), T_IFA,
 insight("Ücret algısında servis ve parça ücretlendirmesi, ürün fiyatıyla birlikte öne çıkmaktadır: servis, kontrol veya \"haksız\" ücret 75 şikayette, \"kullanıcı hatası\" veya \"usta hatası\" gerekçesiyle garanti reddi de 75 şikayette geçmektedir. 92 şikayet (%15,8) tekrar almama veya tavsiye etmeme ifadesi taşımaktadır; 57 şikayet markaya güvenerek satın alındığını belirtmektedir. Kampanya, indirim ve taksit ifadeleri 15 şikayetle sınırlı kalırken parça veya ürün fiyatı 62 şikayette anılmaktadır.",
         "In fee perception, service and part charges stand out alongside product price: a service, inspection or \"unfair\" fee appears in 75 complaints, and warranty refusal on the grounds of \"user error\" or \"installer error\" also in 75. 92 complaints (15.8%) carry a will-not-buy-again or will-not-recommend statement; 57 state the purchase was made on trust in the brand. Campaign, discount and instalment statements are limited to 15 complaints, while part or product price is mentioned in 62.", "D24"),
 kaynak("Şikayetvar marka sayfaları /vitra ve /artema · son 24 ay şikayet metinleri · marka göstergeleri sayfanın bildirdiği değerler · 29.09.2026 · rakip marka sayfaları aylık seri 03.10.2026", "Şikayetvar brand pages /vitra and /artema · complaint texts of the last 24 months · brand indicators as reported by the page · 29.09.2026 · competitor brand pages monthly series 03.10.2026", "D24"),
)
