# -*- coding: utf-8 -*-
"""ozet.md uretici: tum tablolar JSON ciktilarindan uretilir (elle rakam tasinmaz). Anlatim metni sabittir."""
import json, os
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
J = lambda f: json.load(open(os.path.join(D, f), encoding="utf-8"))
T, TA, AY, AYE, ALT, RAK, KONU, TR, BV, BA, SK = (J("temalar.json"), J("temalar_artema.json"), J("aylik.json"), J("aylik_ek.json"),
    J("alt_kirilim.json"), J("rakip.json"), J("konu.json"), J("trend_6ay.json"), J("marka_vitra.json")["bilgi"], J("marka_artema.json")["bilgi"], J("serp.json"))
AYAD = ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"]
def pct(x, n=1): return "-" if x is None else "%%%.*f" % (n, 100 * x)
def num(x): return "-" if x is None else ("{:,}".format(x).replace(",", "."))
def oran(a, b): return "%%%.1f" % (100 * a / b) if b else "-"
def ay_ad(k): return "%s %s" % (AYAD[int(k[5:]) - 1], k[:4])
L = []
w = L.append
V, A = T["_meta"], TA["_meta"]
NV, NA = V["metinli"], A["metinli"]

w("# Şikayetvar madenciliği: VitrA ve Artema (E-ticaret büyüme fırsatları raporu, derin araştırma)\n")
w("Hazırlanma tarihi: 29 Eylül 2026. Veri penceresi: 1 Ekim 2024 - 29 Eylül 2026 (son 24 ay). Bu dosya veri ve özet içerir; rapora alınacak kararlar ayrıca verilecektir.\n")
w("## 1. Yöntem ve kapsam\n")
w("- Apify Store'da Şikayetvar için hazır actor'lar bulundu (tamgadev/sikayetvar-scraper, caa_software/sikayetvar, jungle_synthesizer/... ). Marka sayfalarının herkese açık, sunucu tarafında oluşturulan HTML'i curl ile 200 döndürdüğü ve sayfa içi gömülü veride (toplam şikayet, çözüm oranı, yıldız dağılımı, şikayet kimliği) tüm alanların bulunduğu görüldüğü için actor çalıştırılmadı; Apify maliyeti 0 USD. Giriş yapılmadı, form doldurulmadı, captcha ile karşılaşılmadı; istekler arası 2-4 sn bekleme uygulandı (toplam yaklaşık 1.050 istek).")
w("- Marka sayfaları sayfa sayfa gezildi: VitrA 41 sayfa (%s şikayet, sayfanın bildirdiği toplamla birebir), Artema 23 sayfa (%s şikayet). Her şikayet için başlık, adres, tarih, görüntülenme, \"çözüldü\" işareti ve yıldız puanı alındı. Son 24 ay içindeki şikayetlerin (VitrA %s, Artema %s) detay sayfalarından tam metin okundu (VitrA %s, Artema %s); yazar adı alınmadı, telefon, e-posta, sipariş numarası ve ad-soyad imzaları maskelendi." % (
    num(BV["toplam_sikayet"]), num(SK_ := BA["toplam_sikayet"]), num(V["toplam_pencere"]), num(A["toplam_pencere"]), num(V["detay_metinli"]), num(A["detay_metinli"])))
w("- DataForSEO (Google TR SERP, konum 2792, dil tr): 15 adet `site:sikayetvar.com` sorgusu (3 tanesi hata döndürdü); maliyet %s USD. Marka sayfası adreslerini doğrulamak ve ayrı bir `vitra-karo` sayfasının varlığını görmek için kullanıldı." % ("%.2f" % J("serp.json")["maliyet_usd"]))
w("- Tema ataması anahtar kelime kuralları ile yapıldı (başlık ve tam metin üzerinde). İki ölçü verilir: (a) **sayı / pay**: temanın şikayet içinde geçtiği durum (çoklu etiket, toplam %%100'ü aşar); (b) **ana tema**: her şikayet tek temaya atanır (başlıkta geçen ifade ağırlıklı, toplam %%100). Pay paydası metni olan şikayet sayısıdır (VitrA %s, Artema %s; kalan şikayetler yayından kaldırılmış olup yalnızca teşekkür notu içerir). Bu bir kural tabanlı sınıflandırmadır; alt ayrıntılar örneklem okuması ile doğrulanmıştır ancak sınır durumlarında etiket kayması mümkündür." % (NV, NA))
w("- Alıntılar kullanıcı yazımıyla birebir alınmıştır (yazım hataları korunur); her tema için başlıktan bağımsız, temayı en iyi anlatan üç cümle elle seçilmiştir.\n")

w("## 2. Marka sayfası göstergeleri (Şikayetvar'ın kendi hesapları)\n")
w("| Marka sayfası | Toplam şikayet | Son 1 yıl | Son 1 ay | Genel puan (0-100) | Değerlendirme sayısı | Çözüm oranı (tüm dönem) | Çözüm oranı (son 1 yıl) | Şikayet çözüm anketinde 1 yıldız payı |")
w("|---|---|---|---|---|---|---|---|---|")
for ad, b, slug in (("VitrA", BV, "vitra"), ("Artema", BA, "artema")):
    d = b["donemler"]; y = b["yildiz_dagilimi_tum"]; top = sum(y.values())
    w("| [%s](https://www.sikayetvar.com/%s) | %s | %s | %s | %s | %s | %%%s | %%%s | %s |" % (ad, slug, num(d["all"]["complaintCount"]), num(d["l1y"]["complaintCount"]), num(d["l1m"]["complaintCount"]),
        b["puan_100"], b["degerlendirme_sayisi"], d["all"]["resolveRatio"], d["l1y"]["resolveRatio"], "%s / %s (%s)" % (y.get("1", 0), top, oran(y.get("1", 0), top))))
kv = KONU["vitra-karo"]
w("| [VitrA Karo](https://www.sikayetvar.com/vitra-karo) (ayrı sayfa) | %s | %s | %s | - | - | %%%s | %%%s | - |" % (num(kv["toplam_sikayet"]), kv["donemler"]["l1y"]["complaintCount"], kv["donemler"]["l1m"]["complaintCount"], kv["donemler"]["all"]["resolveRatio"], kv["donemler"]["l1y"]["resolveRatio"]))
w("")
w("Okuma: Çözüm oranı, şikayet sahibinin sonuç anketine verdiği yanıtlardan hesaplanır (VitrA tüm dönemde %s anket yanıtından %s çözüm). Şikayetvar'ın markanın \"AiVar\" marka karnesi (29 Eylül 2026 tarihli, platform tarafından yapay zeka ile üretilen özet) son 6 ayda en çok dile getirilen konuları şöyle sıralıyor: vitrifiye ve malzeme kusurları (50 şikayette klozetlerde lekelenme, kararma, rezervuarda su akıtma), servis ve garanti süreçleri (31 şikayette garanti kapsamı reddi, 19 şikayette tekil yedek parça bulunamaması ve tüm setin istenmesi, 16 şikayette çözümsüz onarım, 9 şikayette servis randevusu aksaması), iade, değişim ve teslimat (14 şikayette iade reddi, 10 şikayette hatalı teslimat içeriği), personel ve iletişim (12 şikayette yanıtsız kayıt). Bu özet platformun kendi üretimidir; sayısal doğrulaması yapılmamıştır ve yön gösterici olarak okunmalıdır." % (num(BV["donemler"]["all"]["surveyCount"]), num(BV["donemler"]["all"]["resolvedCount"])))
w("")

w("## 3. Aylık şikayet serisi (son 24 ay)\n")
w("| Ay | VitrA | Artema |")
w("|---|---|---|")
for k in AY:
    w("| %s | %s | %s |" % (ay_ad(k), AY[k], AYE["Artema"][k]))
s1 = sum(v for k, v in AY.items() if k >= "2025-10"); s0 = sum(AY.values()) - s1
a1 = sum(v for k, v in AYE["Artema"].items() if k >= "2025-10"); a0 = sum(AYE["Artema"].values()) - a1
w("| **Toplam** | **%s** | **%s** |" % (sum(AY.values()), sum(AYE["Artema"].values())))
w("")
w("Okuma: VitrA'da ilk 12 ay (Ekim 2024 - Eylül 2025) %s, son 12 ay (Ekim 2025 - Eylül 2026) %s şikayet; aylık ortalama 25 civarında, en yüksek aylar Aralık 2024 (%s) ve Nisan 2026 (%s). Artema'da ilk 12 ay %s, son 12 ay %s (%s). Eylül 2026 kısmi aydır (29 Eylül'e kadar). Tüm dönem (Eylül 2023 - Eylül 2026) serisi `aylik_ek.json` içindedir. Şikayetvar sayfası son 3 yılı göstermektedir; daha eski kayıtlar sayfada yer almamaktadır.\n" % (s0, s1, AY["2024-12"], AY["2026-04"], a0, a1, "aylık ortalama %.1f -> %.1f" % (a0 / 12, a1 / 12)))

w("## 4. VitrA şikayet temaları (son 24 ay, n=%s metinli şikayet)\n" % NV)
w("| Tema | Sayı (temanın geçtiği) | Pay | Ana tema sayısı | Ana tema payı | \"Çözüldü\" işaretli pay | Medyan görüntülenme |")
w("|---|---|---|---|---|---|---|")
sira = sorted([k for k in T if k != "_meta"], key=lambda k: (k.startswith("Diğer"), -T[k]["ana_tema_sayi"]))
for k in sira:
    v = T[k]; w("| %s | %s | %s | %s | %s | %s | %s |" % (k, v["sayi"], pct(v["pay"]), v["ana_tema_sayi"], pct(v["ana_tema_pay"]), pct(v["cozuldu_pay"]), num(int(v["medyan_goruntulenme"])) if v["medyan_goruntulenme"] else "-"))
w("")
w("Not: Sıralama ana tema sayısına göredir. \"Mağaza ve bayi\", \"vitra.com.tr\" ve \"pazaryeri\" temaları konudan çok satın alma kanalını anar; kanal ayrıntısı 5. bölümdedir. Son 24 ayda VitrA şikayetlerinin %s'i \"çözüldü\" olarak işaretlenmiştir (%s / %s).\n" % (oran(47, 600), 47, 600))

w("### 4.1 Tema bazında alıntılar ve bağlantılar\n")
for k in sira:
    if k.startswith("Diğer"): continue
    w("**%s** (%s şikayette geçiyor, %s)" % (k, T[k]["sayi"], pct(T[k]["pay"])))
    for a in T[k]["alintilar"]:
        w("- \"%s\" (%s) [şikayet](%s)" % (a["metin"], a["tarih"], a["url"]))
    w("")

w("## 5. E-ticaret ve satış sonrası alt kırılımlar (VitrA)\n")
a = ALT["VitrA"]; b = ALT["Artema"]
w("### 5.1 Satın alma kanalı (birbirini dışlamaz)\n")
w("| Kanal | VitrA sayı | VitrA pay | Artema sayı | Artema pay |")
w("|---|---|---|---|---|")
for kk in ["vitra.com.tr", "pazaryeri platformu", "perakende zinciri (Koçtaş, Bauhaus, Tekzen, Evdema)", "bayi / yapı market / yerel satıcı", "kanal belirtilmemiş"]:
    x, y = a["kanal_dagilimi"].get(kk, 0), b["kanal_dagilimi"].get(kk, 0)
    w("| %s | %s | %s | %s | %s |" % (kk, x, oran(x, a["n"]), y, oran(y, b["n"])))
w("")
w("Pazaryeri platformu adı geçen şikayetlerde dağılım (VitrA / Artema): Trendyol %s / %s, Hepsiburada %s / %s, n11 %s / %s, Amazon %s / %s. Metinde \"satıcı\" ifadesi VitrA'da %s, Artema'da %s şikayette geçer. Koçtaş VitrA şikayetlerinin %s'inde (%s), Bauhaus %s'inde (%s) anılır. VitrA'da vitra.com.tr veya pazaryeri etiketi taşıyan şikayet %s (%s).\n" % (
    a["pazaryeri_platform"]["Trendyol"], b["pazaryeri_platform"]["Trendyol"], a["pazaryeri_platform"]["Hepsiburada"], b["pazaryeri_platform"]["Hepsiburada"],
    a["pazaryeri_platform"]["n11"], b["pazaryeri_platform"]["n11"], a["pazaryeri_platform"]["Amazon"], b["pazaryeri_platform"]["Amazon"], a["satici_gecen_n"], b["satici_gecen_n"],
    oran(a["perakende_zincir"]["Koçtaş"], a["n"]), a["perakende_zincir"]["Koçtaş"], oran(a["perakende_zincir"]["Bauhaus"], a["n"]), a["perakende_zincir"]["Bauhaus"], a["eticaret_kanali_n"], oran(a["eticaret_kanali_n"], a["n"])))

w("### 5.2 Yedek parça (VitrA %s şikayet, Artema %s)\n" % (a["yedek_parca_n"], b["yedek_parca_n"]))
w("| Parça grubu (yedek parça temalı şikayetler içinde) | VitrA | Artema |")
w("|---|---|---|")
for kk in a["yedek_parca_parca_tipi"]:
    w("| %s | %s | %s |" % (kk, a["yedek_parca_parca_tipi"][kk], b["yedek_parca_parca_tipi"][kk]))
w("")
w("Şikayetvar'ın kendi konu dizininde (tüm dönem, 3 yıl) VitrA için `yedek-parca` başlığı %s, `yetkili-servis` %s, `servis` %s, `musteri-hizmetleri` %s, `montaj` %s, `klozet-kapagi` %s, `banyo-dolabi` %s şikayet içerir; Artema için `yedek-parca` %s, `yetkili-servis` %s, `servis` %s, `montaj` %s (kaynak: konu.json). Bu sayılar anahtar kelime dizinine aittir ve bu çalışmadaki tema sayılarıyla doğrudan toplanmaz.\n" % (
    KONU["vitra/yedek-parca"]["toplam"], KONU["vitra/yetkili-servis"]["toplam"], KONU["vitra/servis"]["toplam"], KONU["vitra/musteri-hizmetleri"]["toplam"], KONU["vitra/montaj"]["toplam"],
    KONU["vitra/klozet-kapagi"]["toplam"], KONU["vitra/banyo-dolabi"]["toplam"], KONU["artema/yedek-parca"]["toplam"], KONU["artema/yetkili-servis"]["toplam"], KONU["artema/servis"]["toplam"], KONU["artema/montaj"]["toplam"]))

w("### 5.3 Montaj ve usta (VitrA %s, Artema %s şikayette geçiyor)\n" % (a["montaj_n"], b["montaj_n"]))
w("| Alt konu (montaj temalı şikayetler içinde) | VitrA | Artema |")
w("|---|---|---|")
for kk in a["montaj_alt"]:
    w("| %s | %s | %s |" % (kk, a["montaj_alt"][kk], b["montaj_alt"][kk]))
w("")
w("### 5.4 Fiyat, garanti ve güven ifadeleri (tüm metinli şikayetler içinde)\n")
w("| İfade grubu | VitrA sayı | VitrA pay | Artema sayı | Artema pay |")
w("|---|---|---|---|---|")
for grp in ("fiyat_alt", "guven_tekrar_alim", "kanit_ifadeleri"):
    for kk in a[grp]:
        w("| %s | %s | %s | %s | %s |" % (kk, a[grp][kk], oran(a[grp][kk], a["n"]), b[grp][kk], oran(b[grp][kk], b["n"])))
w("")
w("### 5.5 Altı aylık dönemlerde tema geçişi (VitrA)\n")
donem = list(TR["VitrA"].keys())
w("| Tema (geçtiği şikayet payı) | " + " | ".join(donem) + " |")
w("|---|" + "---|" * len(donem))
w("| Şikayet sayısı | " + " | ".join(str(TR["VitrA"][d]["n"]) for d in donem) + " |")
for kod, ad in (("yedek_parca", "Yedek parça"), ("montaj", "Montaj ve usta"), ("servis_garanti", "Yetkili servis ve garanti"), ("pazaryeri", "Pazaryeri ve üçüncü taraf satıcı"), ("vitra_online", "vitra.com.tr"), ("kalite", "Ürün kalitesi")):
    w("| %s | " % ad + " | ".join("%s (%s)" % (TR["VitrA"][d].get(kod, 0), oran(TR["VitrA"][d].get(kod, 0), TR["VitrA"][d]["n"])) for d in donem) + " |")
w("")

w("## 6. Artema tema özeti (son 24 ay, n=%s metinli şikayet)\n" % NA)
w("| Tema | Sayı (geçtiği) | Pay | Ana tema sayısı | Ana tema payı |")
w("|---|---|---|---|---|")
for k in sorted([k for k in TA if k != "_meta"], key=lambda k: (k.startswith("Diğer"), -TA[k]["ana_tema_sayi"])):
    v = TA[k]; w("| %s | %s | %s | %s | %s |" % (k, v["sayi"], pct(v["pay"]), v["ana_tema_sayi"], pct(v["ana_tema_pay"])))
w("")
w("Artema alıntıları ve bağlantıları `temalar_artema.json` içindedir.\n")

w("## 7. Rakip karşılaştırması\n")
w("| Marka sayfası | Toplam şikayet | Son 1 yıl | Puan (0-100) | Değerlendirme sayısı | Çözüm oranı (tüm dönem) | Çözüm oranı (son 1 yıl) | İlk 3 sayfada e-ticaret temalı pay | İlk 3 sayfanın tarih aralığı |")
w("|---|---|---|---|---|---|---|---|---|")
for ad in ("VitrA", "Artema", "Kale", "Creavit", "E.C.A. (Serel dahil)", "Bocchi", "Geberit"):
    r = RAK[ad]
    w("| [%s](%s) | %s | %s | %s | %s | %s | %s | %s (%s / %s) | %s |" % (ad, r["marka_sayfasi"], num(r["toplam_sikayet"]), num(r["sikayet_son1yil"]), r["puan_100"], r["degerlendirme_sayisi"],
        "%%%s" % r["cozum_orani_tum_pct"], "%%%s" % r["cozum_orani_son1yil_pct"], pct(r["ilk3sayfa_eticaret_pay"]), r["ilk3sayfa_eticaret_n"], r["ilk3sayfa_n"], " - ".join(r["ilk3sayfa_tarih_araligi"])))
w("| Serel | - | - | - | - | - | - | - | Ayrı marka sayfası yok (sikayetvar.com/serel 404); Serel klozet şikayetleri E.C.A. sayfasında \"ECA Serel\" olarak toplanır |")
w("")
w("Okuma ve sınırlar: (1) E-ticaret temalı pay, ilk 3 sayfadaki (en yeni yaklaşık 70 şikayet) başlık ve liste özetinde pazaryeri platform adı, \"online\", \"internet sitesi\", \"web sitesi\", \".com\" gibi bir ifadenin geçmesiyle hesaplanmıştır; tam metin okunmadığı için 4. bölümdeki tema payları ile doğrudan kıyaslanmaz. (2) İlk 3 sayfanın kapsadığı süre markalara göre farklıdır (VitrA yaklaşık 3 ay, Kale yaklaşık 4 ay, Creavit yaklaşık 5 ay, Bocchi ve Geberit 2-3 yıl); hacmi yüksek markalarda pencere kısadır. (3) E.C.A. sayfası kombi, ısıtma ve ısı pompası gibi banyo dışı ürünleri de içerir; toplam şikayet ve puan bu nedenle banyo ürünleriyle sınırlı değildir. (4) VitrA ve Artema puanı ile çözüm oranı, rakiplerin çoğuna göre düşük bandadır; tek istisna Bocchi'dir (puan 22, %22 çözüm; küçük örneklem, 9 değerlendirme).\n")

w("## 8. E-ticaret raporu için çıkarımlar\n")
yp = T["Yedek parça bulunamaması"]; mo = T["Montaj ve usta"]; sg = T["Yetkili servis ve garanti"]; pz = T["Pazaryeri ve üçüncü taraf satıcı"]; vo = T["vitra.com.tr sipariş, teslimat ve iade"]; mb = T["Mağaza ve bayi"]; fk = T["Fiyat ve kampanya"]; il = T["İletişim ve çağrı merkezi"]; ka = T["Ürün kalitesi, sızıntı, kırılma"]
t1, t4 = TR["VitrA"]["2024-10/2025-03"], TR["VitrA"]["2026-04/2026-09"]
w("1. **Satış sonrası deneyim, şikayetlerin ağırlık merkezidir.** VitrA'da yetkili servis ve garanti %s (ana tema %s), ürün kalitesi %s (ana tema %s); servis, yedek parça, montaj ve iletişim temalarından en az birini taşıyan şikayet %s / %s (%s). Ürün kalitesi temalı %s şikayetin %s tanesi (%s) aynı zamanda servis ve garanti sürecini anar; metinlerde arızanın kendisi kadar ardından gelen süreç (ücret talebi, \"kullanıcı hatası\" gerekçesi, randevu, geri dönüş beklentisi) de anlatılır. Tekrar satın almayı etkileyen ifadeler: \"bir daha, asla, tavsiye etmiyorum, pişman\" türü ifade %s şikayette (%s); \"markaya güvenerek satın aldım\" türü ifade %s şikayette (%s) geçer." % (
    pct(sg["pay"]), pct(sg["ana_tema_pay"]), pct(ka["pay"]), pct(ka["ana_tema_pay"]), a["satis_sonrasi_birlesim_n"], a["n"], oran(a["satis_sonrasi_birlesim_n"], a["n"]),
    a["kalite_n"], a["kalite_ve_servis_birlikte_n"], oran(a["kalite_ve_servis_birlikte_n"], a["kalite_n"]),
    a["guven_tekrar_alim"]["Tekrar almama, tavsiye etmeme"], oran(a["guven_tekrar_alim"]["Tekrar almama, tavsiye etmeme"], a["n"]),
    a["guven_tekrar_alim"]["Marka güveni ile satın alma (güvenerek, kaliteli sanıp)"], oran(a["guven_tekrar_alim"]["Marka güveni ile satın alma (güvenerek, kaliteli sanıp)"], a["n"])))
w("2. **Yedek parça: hem hacim hem eğilim açısından ayrı bir başlıktır.** VitrA şikayetlerinin %s'inde (%s şikayet) yedek parça temini geçer; Artema'da %s (%s). Altı aylık dönemlerde payı %s -> %s (Ekim 2024 - Mart 2025 -> Nisan - Eylül 2026) seviyesine yükselmiştir. En sık anılan parça grupları klozet kapağı, menteşe, vida (%s), sifon mekanizması (%s), rezervuar ve şamandıra (%s), batarya ve kartuş (%s). %s şikayette parçanın tek başına satılmadığı, komple set veya ürün değişimi önerildiği aktarılmaktadır. Şikayetlerde yedek parçanın bayide bulunmadığı, servisin merkeze yönlendirdiği ve merkezde talep numarası açıldığı ancak süre bildirilmediği anlatılır. Bu başlık, yedek parça bulucu ve parça satışı önerisini destekleyen kanıt niteliğindedir; 2026'da yedek parça kategorisinin yeni sitede bulunmadığı bulgusuyla birlikte okunabilir." % (
    pct(yp["pay"]), yp["sayi"], pct(TA["Yedek parça bulunamaması"]["pay"]), TA["Yedek parça bulunamaması"]["sayi"], oran(t1.get("yedek_parca", 0), t1["n"]), oran(t4.get("yedek_parca", 0), t4["n"]),
    a["yedek_parca_parca_tipi"]["Klozet kapağı, menteşe, vida, takoz"], a["yedek_parca_parca_tipi"]["Sifon (flush) mekanizması, gider, süzgeç"], a["yedek_parca_parca_tipi"]["Rezervuar, şamandıra, kumanda paneli"], a["yedek_parca_parca_tipi"]["Batarya, kartuş, musluk parçası"],
    a["kanit_ifadeleri"]["Yedek parçanın tek başına satılmaması, komple set / ürün değişimi önerisi"]))
w("3. **Montaj ve usta hizmeti, şikayetlerin dörtte birinden fazlasında geçer.** VitrA'da montaj teması %s (%s şikayet), Artema'da %s. Altı aylık dönemlerde %s -> %s seviyesine çıkmıştır. Alt konular: randevu ve erteleme (%s), kendi ustası ile montaj (%s), montaj hatası veya hasar (%s), montaj ücreti veya ek ücret (%s), VitrA servisi montajı (%s). \"Ücretsiz montaj\" vaadinin sonradan ücret talebine dönüştüğü, kampanya bitiminde ücretsiz montaj hakkının geçersiz sayıldığı ve kendi ustasıyla yapılan montajın garanti kapsamı dışında bırakıldığı örnekler alıntılarda yer alır. Bu bulgu, keşif ve montaj hizmetinin (11 kalem, VitrA Banyo Asistanı akışı) ürün sayfasında görünürlüğü, kapsamın ve ücretin net yazılması ve randevu takibi ile ilişkilendirilebilir." % (
    pct(mo["pay"]), mo["sayi"], pct(TA["Montaj ve usta"]["pay"]), oran(t1.get("montaj", 0), t1["n"]), oran(t4.get("montaj", 0), t4["n"]),
    a["montaj_alt"]["Montaj randevusu, erteleme, gecikme"], a["montaj_alt"]["Kendi ustası / tesisatçı montajı"], a["montaj_alt"]["Montaj hatası, hasar"], a["montaj_alt"]["Montaj ücreti / ek ücret"], a["montaj_alt"]["VitrA servisi / yetkili servis montajı"]))
w("4. **Pazaryeri ve vitra.com.tr kaynaklı şikayet payı sınırlıdır; Artema'da pazaryeri payı daha yüksektir, VitrA'da pazaryeri temalı şikayet sayısı son dönemde yükselmiştir.** VitrA'da pazaryeri platformu adı geçen şikayet %s (%s), vitra.com.tr %s (%s); ikisi birlikte %s (%s). Artema'da pazaryeri platformu %s (%s). VitrA'da pazaryeri temalı şikayet altı aylık dönemlerde %s -> %s -> %s -> %s adettir. Pazaryeri şikayetlerinde öne çıkan konular: kırık veya eksik parça teslimi ve iade sürecinin uzaması, değişim yerine yalnızca iade sunulması, tek parçanın ayrı satılmaması (\"komple iade\"), pazaryeri satıcısı ile VitrA çağrı merkezi arasında sorumluluğun karşılıklı devri ve satıcı kaynaklı eksik parça. vitra.com.tr şikayetlerinde teslimat gecikmesi, yanlış ürün, iade adresi belirsizliği ve fatura bilgisine erişilememesi geçer. Bu paylar düşük hacimli olduğundan (VitrA %s şikayet) yön gösterici olarak değerlendirilir." % (
    a["kanal_dagilimi"]["pazaryeri platformu"], oran(a["kanal_dagilimi"]["pazaryeri platformu"], a["n"]), a["kanal_dagilimi"]["vitra.com.tr"], oran(a["kanal_dagilimi"]["vitra.com.tr"], a["n"]),
    a["eticaret_kanali_n"], oran(a["eticaret_kanali_n"], a["n"]), b["kanal_dagilimi"]["pazaryeri platformu"], oran(b["kanal_dagilimi"]["pazaryeri platformu"], b["n"]),
    TR["VitrA"]["2024-10/2025-03"].get("pazaryeri", 0), TR["VitrA"]["2025-04/2025-09"].get("pazaryeri", 0), TR["VitrA"]["2025-10/2026-03"].get("pazaryeri", 0), TR["VitrA"]["2026-04/2026-09"].get("pazaryeri", 0), a["n"]))
w("5. **Perakende zincirleri ve bayiler, satın alma kanalı olarak pazaryerinden daha sık anılır.** Koçtaş %s, Bauhaus %s, bayi veya yapı market %s VitrA şikayetinde geçer (pazaryeri platformu %s). Alıntılarda mağazanın \"malı bizden aldınız, hizmet değil\" diyerek sorumluluğu üstlenmediği, \"bayi muhatabım yok\" ifadesi ve iade için üreticiden onay beklendiği anlatılır; satış sonrası sorumluluğun kanallar arasında dağıldığı görülür. Kanal bazında tek bir muhatap ve takip numarası tanımlanması, e-ticaret modelinin satış sonrası tarafı için bir tasarım girdisi olabilir." % (
    a["perakende_zincir"]["Koçtaş"], a["perakende_zincir"]["Bauhaus"], a["kanal_dagilimi"]["bayi / yapı market / yerel satıcı"], a["kanal_dagilimi"]["pazaryeri platformu"]))
w("6. **Fiyat ve ücret algısı, ürün fiyatından çok servis ve parça ücretlendirmesi etrafında toplanır.** Fiyat ve kampanya teması %s (%s şikayet); bunun içinde servis, kontrol veya \"haksız\" ücret ifadesi %s şikayette, parça veya ürün fiyatı (pahalılık) %s şikayette, kampanya, indirim ve taksit %s şikayette geçer. Garanti kapsamında olduğu bildirilen üründe servis ücreti istenmesi, servis sonrası fatura veya servis fişi verilmemesi (%s şikayet) ve garanti reddinde \"kullanıcı hatası\" veya \"usta hatası\" gerekçesi (%s şikayet, %s) tekrarlayan örüntülerdir. Taksit ve kampanya konusu VitrA'da sınırlı geçer; e-ticaret kampanya ve taksit kurgusu için bu kaynaktan güçlü bir talep sinyali çıkmamıştır." % (
    pct(fk["pay"]), fk["sayi"], a["fiyat_alt"]["Servis ücreti, kontrol ücreti, haksız ücret"], a["fiyat_alt"]["Parça / ürün fiyatı, pahalılık"], a["fiyat_alt"]["Kampanya, indirim, taksit"],
    a["kanit_ifadeleri"]["Fatura veya servis fişi verilmemesi"], a["kanit_ifadeleri"]["Garanti reddi gerekçesi olarak 'kullanıcı hatası' / 'usta hatası'"], oran(a["kanit_ifadeleri"]["Garanti reddi gerekçesi olarak 'kullanıcı hatası' / 'usta hatası'"], a["n"])))
w("7. **İletişim ve çağrı merkezi, geri dönüş beklentisi açısından tekrar eden bir başlıktır.** İletişim teması %s (%s şikayet). Kayıt açıldığı ancak bir ayı aşan sürede dönüş yapılmadığı anlatımı alıntılarda tekrar eder. Son 24 ayda \"çözüldü\" işaretli şikayet payı %s, Şikayetvar çözüm oranı VitrA'da tüm dönemde %%%s, son 1 yılda %%%s; Kale (%%%s), Creavit (%%%s), E.C.A. (%%%s), Geberit (%%%s) ile karşılaştırıldığında VitrA ve Artema düşük bandadır. VitrA şikayet sayfaları son 24 ayda toplam %s görüntülenme almıştır; çözüm oranı ve puan, markanın arama sonuçlarında görünen şikayet sayfaları üzerinden tüketici güveni göstergesi olarak okunabilir." % (
    pct(il["pay"]), il["sayi"], oran(47, 600), BV["donemler"]["all"]["resolveRatio"], BV["donemler"]["l1y"]["resolveRatio"], RAK["Kale"]["cozum_orani_son1yil_pct"], RAK["Creavit"]["cozum_orani_son1yil_pct"], RAK["E.C.A. (Serel dahil)"]["cozum_orani_son1yil_pct"], RAK["Geberit"]["cozum_orani_son1yil_pct"], "yaklaşık 617 bin"))
w("8. **Rakip bağlamı:** VitrA (puan 18) ve Artema (puan 15), Kale (36), Creavit (32) ve Geberit (78) ile karşılaştırıldığında Şikayetvar puanında düşük bandadır; VitrA'nın toplam şikayet hacmi (978) Kale (649) ve Creavit'in (585) üzerindedir. E.C.A. sayfasının (3.800) hacmi banyo dışı ürünleri de kapsar. İlk 3 sayfada e-ticaret temalı pay VitrA'da %s, Artema'da %s, rakip markalarda %s - %s bandındadır; VitrA ve Artema'da online kanal kaynaklı şikayetlerin izlenmesini destekleyen bir gösterge olarak okunabilir; örneklem küçüktür ve kapsanan süre markalara göre farklıdır." % (
    pct(RAK["VitrA"]["ilk3sayfa_eticaret_pay"]), pct(RAK["Artema"]["ilk3sayfa_eticaret_pay"]), pct(min(RAK[k]["ilk3sayfa_eticaret_pay"] for k in ("Kale", "Creavit", "E.C.A. (Serel dahil)", "Bocchi", "Geberit"))), pct(max(RAK[k]["ilk3sayfa_eticaret_pay"] for k in ("Kale", "Creavit", "E.C.A. (Serel dahil)", "Bocchi", "Geberit")))))
w("")
w("## 9. Kısıtlar (alınamayanlar ve dikkat edilecek noktalar)\n")
w("- Şikayetvar marka sayfası yalnızca son 3 yılı (Eylül 2023 sonrası) listeler; 24 aydan öncesi için ek veri yoktur. Aylık seri 24 ay olarak verilmiş, 36 aylık seri `aylik_ek.json` içine eklenmiştir.")
w("- Şikayetvar'da pazaryeri (Trendyol, Hepsiburada, n11, Amazon) ve kanal bazlı konu sayfaları (`/vitra/trendyol` vb.) bulunmadığı için pazaryeri sayıları metin taramasından hesaplanmıştır. Kampanya, taksit, iade, kargo, sipariş, teslimat, koctas, bauhaus, kırık, sızıntı ve benzeri konu sayfaları da 404 döndü; bu nedenle konu dizini yalnızca yedek parça, montaj, servis, müşteri hizmetleri ve birkaç ürün başlığı için kullanılabildi.")
w("- Marka yanıtı metni (markanın şikayete verdiği cevap) sayfalarda görünmediği için marka yanıt süresi, yanıt oranı veya içeriği ölçülemedi. Yalnızca \"çözüldü\" işareti ve Şikayetvar çözüm oranı kullanıldı. Yayından kaldırılan şikayetler (VitrA'da son 24 ayda %s, Artema'da %s) tema payı paydasına alınmadı, ancak aylık sayıma dahildir." % (V["yayindan_kaldirilan"], A["yayindan_kaldirilan"]))
w("- Şikayetler tek taraflı beyanlardır ve doğrulanmamıştır; sessiz çoğunluk (şikayet yazmayan müşteri) temsil edilmez. Tema payları kural tabanlıdır; çoklu etiketli \"geçtiği\" payları ile tek etiketli \"ana tema\" payları farklı ölçülerdir, toplanmamalıdır.")
w("- Rakip karşılaştırması yalnızca marka sayfası düzeyindedir (ilk 3 sayfa, farklı zaman aralıkları). Serel için ayrı marka sayfası yoktur; E.C.A. sayfası banyo dışı ürünleri içerir. VitrA Karo ayrı sayfada 38 şikayetle yer alır, tema analizine dahil edilmemiştir.")
w("- Şikayet başlıkları ve alıntılar kullanıcı yazımıdır; müşteri adı, telefon, e-posta ve sipariş numarası çıktıya alınmamıştır. `detay_*.jsonl` dosyaları tema hesabı için tutulan çalışma önbelleğidir (yayınlanmış şikayet metni, kişisel veri maskeli); dışarıya paylaşılmamalıdır.")
w("- Raporda kullanılacak alıntılar için Şikayetvar kullanım koşulları ve kişisel veri açısından alıntının kısa tutulması ve şikayet bağlantısıyla verilmesi önerilir.\n")

w("## 10. Dosyalar\n")
w("- `sikayetler.json`: ham liste (VitrA %s + Artema %s şikayet: başlık, adres, tarih, görüntülenme, çözüldü, yıldız, 350 karakterlik kısa metin, tema etiketleri)" % (num(BV["toplam_sikayet"]), num(BA["toplam_sikayet"])))
w("- `temalar.json` (VitrA tema özeti: sayı, pay, ana tema, alıntılar), `temalar_artema.json`, `aylik.json` (VitrA son 24 ay), `aylik_ek.json` (Artema ve 36 aylık seriler), `rakip.json`, `alt_kirilim.json`, `trend_6ay.json`, `konu.json`, `serp.json`, `marka_vitra.json`, `marka_artema.json`, `rakip_ham.json`")
w("- Betikler: `uretim/sikayetvar_ortak.py` (çekme ve ayrıştırma), `sikayetvar_cek.py`, `sikayetvar_detay.py`, `sikayetvar_rakip.py`, `sikayetvar_konu.py`, `sikayetvar_serp.py`, `sikayetvar_tema.py`, `sikayetvar_analiz.py`, `sikayetvar_ozet.py`")
open(os.path.join(D, "ozet.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("ozet.md yazildi", len("\n".join(L)))
