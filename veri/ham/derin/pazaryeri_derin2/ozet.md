# VitrA Türkiye e-ticaret: alt kategori taraması, 2. tur (pazaryerleri, fiyat karşılaştırma siteleri, rakip mağazalar ve vitra.com.tr)

**Erişim tarihi:** 30.09.2026 · **Kapsam:** 57 alt kategori; Trendyol, Hepsiburada, Akakçe, Cimri; Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline, Creavit e-mağaza; vitra.com.tr kategori sayfaları · **Okuma yöntemi:** kullanıcı tarayıcısı üzerinden, yavaş tempoda, girişsiz sayfa okuması

> Fiyatlar TL cinsindendir ve tarama anındaki listelere aittir. "Medyan" tabloda eşleşen ürünlerin fiyat medyanıdır. Pazaryeri "toplam" değerleri kanalın arama sonucu sayısıdır ve ilgisiz ürünleri içerebilir; kesit değerlendirmeleri eşleşen ürünler üzerinden yapılmıştır. Hepsiburada toplamı 10.000 ile sınırlı gösterildiğinden "10.000" değeri "10.000+" olarak okunmalıdır. Önceki turda taranan 42 kategori bu dosyada yer almamaktadır (`veri/ham/derin/pazaryeri_derin/ozet.md`).

## 0. Okunan hacim

| Kanal | Kesit | Okunan ürün satırı | Eşleşen satır | Not |
|---|---|---|---|---|
| Trendyol | 57 | 1.759 | 1.109 | Çok satan (BEST_SELLER) ilk sayfa, 36 ürün; 10 kesitte ikinci okuma, eşleşme oranı yüksek olan tutuldu |
| Hepsiburada | 57 | 1.806 | 1.507 | Çok satan ilk sayfa, 36 ürün |
| Akakçe | 57 | 1.314 | 1.305 | İlk sayfa, 32 ürün (en düşük fiyat ve satıcı sayısı) |
| Cimri | 40 (52 kesit açıldı) | 810 | 801 | 5 kesit okunmadı, 12 kesitte yalnızca toplam alındı (Kısıtlar) |
| Koçtaş | 57 | 1.689 | 1.261 | Çok satan ilk sayfa, 48 ürün |
| Bauhaus | 57 | 396 | 174 | Arama sonucu, en çok 24 ürün; 16 kesitte eşleşen ürün var |
| Banyomarka | 40 | 1.054 | 944 | Arama sonucu, 32 ürün |
| Banyomega | 39 | 588 | 465 | Arama sonucu, 24 ürün |
| Banyoline | 56 | 1.198 | 454 | Arama sonucu, 24 ürün |
| Creavit e-mağaza | 57 | 1.368 | 426 | Arama sonucu, 24 ürün; tek marka |
| vitra.com.tr | 55 kategori sayfası + 3 özel sayfa | 1.100 kart (771 kategori + 329 özel sayfa) | - | Sayfa toplamları 2.258 renk/varyant kartı; sayfa başına 4 istek |

Toplam 11.982 pazaryeri, fiyat karşılaştırma ve mağaza ürün satırı okunmuş, 8.446'sı kesit anahtar sözcüğüyle eşleşmiştir. Ürün satırları `urunler.jsonl`, kesit özetleri `kesitler.jsonl`, vitra.com.tr kategori kayıtları `vitra_site_kategori.jsonl` dosyalarındadır.

## 1. Yöntem

- **Okuma yolu:** Kullanıcının Chrome tarayıcısı üzerinden (Control_Chrome: sayfa açma ve sayfa içi JavaScript), giriş, form, sepet ve captcha kullanılmadan, yavaş tempoda: her sekmede istekler arası 3,3 sn, her alan adı için tek sekme. Sekmeler iş bitiminde kapatılmamıştır. Sayfalar aynı kökenli `fetch` istekleriyle okunmuş, ilk sayfadaki ürün kartları ayrıştırılmıştır. Kişisel veri alınmamıştır (Trendyol ürün sayfalarından yalnızca satıcı mağaza adı okunmuştur).
- **Kesit tanımı:** 57 alt kategori, 9 ana kategori (Klozet 5, Lavabo 7, Armatür 9, Duşlar 6, Rezervuar 6, Yıkanma alanları 7, Banyo mobilyası 8, Banyo aksesuarı 7, Vitrifiye tamamlayıcı 2). Önceki turda taranan 42 kategori (klozet, asma klozet, klozet takımı, akıllı klozet, klozet kapağı, lavabo, tezgah üstü ve altı lavabo, dolap ailesi, gömme rezervuar, iç takım, lavabo ve banyo bataryası, ankastre batarya, duş seti, duş başlığı, duşakabin, duş teknesi, küvet, pisuvar, bide vb.) tekrar taranmamıştır. Aynalı dolap tek istisnadır (Trendyol'da önceki turda aksesuar karışımlı okunduğu için).
- **Arama işareti:** Pazaryerlerinde bu alt kategoriler için birebir kategori sayfası çoğunlukla bulunmadığından her kesit arama ifadesiyle okunmuştur. Tabloda `a` = arama sonucu, `k+a` = arama ifadesi + kanalın web kategorisi süzgeci (yalnız Trendyol), `k` = Akakçe ve Cimri aramasının kendiliğinden ilgili kategori sayfasına yönlenmesi. Parantezdeki `e/o` değeri, okunan `o` ürün içinde kesit anahtar sözcüğüyle eşleşen `e` ürün sayısıdır; tüm fiyat, marka ve VitrA/Artema hesapları yalnızca eşleşen ürünler üzerinden yapılmıştır.
- **Kanal ayrıntısı:** Trendyol: önce alaka sırasında arama ile çözümlenen web kategorisi adayları okunmuş, uygun aday varsa `wc=<kategori>&q=<ifade>&sst=BEST_SELLER`, yoksa `q=<ifade>&sst=BEST_SELLER` ile ilk sayfa (36 ürün) alınmıştır; eşleşme oranı düşük 10 kesitte ikinci bir okuma yapılıp eşleşme oranı yüksek olan sonuç tutulmuştur. Hepsiburada: `/ara?q=<ifade>&siralama=coksatan` ilk sayfa (36 ürün). Akakçe: `/arama/?q=<ifade>` ilk sayfa (32 ürün), en düşük fiyat ve satıcı sayısı (`data-cp`). Cimri: `/arama?q=<ifade>` ilk sayfa (32 ürün), en düşük fiyat ve "N fiyatı incele" satıcı sayısı. Rakip mağazalar: kendi arama sayfalarının ilk sonuç sayfası (Koçtaş 48, Bauhaus 15-24, Banyomarka 32, Banyomega 24, Banyoline 24, Creavit e-mağaza 24 ürün; Koçtaş için `sort=bestseller-desc`, diğerleri mağazanın varsayılan arama sırası).
- **vitra.com.tr:** her alt kategori için sitemap'teki kategori sayfası (`/c-...`) ve sayfa başına dört istek: varsayılan sıra (En Çok Satanlar, ilk 20 kart), "Fiyata Göre Artan" ve "Fiyata Göre Azalan" (fiyat aralığı), "Sadece stoklu ürünleri göster" süzgeci (stoklu sayı). Ürün sayısı sayfadaki "N sonuç listeleniyor" metninden alınmıştır ve renk/varyant kartlarını içerir. "Stokta yok" = sayfa toplamı - stoklu süzgeç toplamı. "Ücretsiz Montaj" sayısı `/c-ucretsiz-montaj` listesinin tüm sayfalarından (kart kategori etiketi eşleştirilerek) ve kategori ilk sayfasındaki kart etiketlerinden okunmuştur. Fiyat aralığı liste fiyatıdır; kartlarda ayrıca "Sepette %N indirim" etiketi görülmektedir.
- **VitrA/Artema tespiti:** marka alanı ya da ürün adının başında VitrA veya Artema geçen satırlar. Yorum payı, eşleşen ürünlerin toplam değerlendirme sayısı içindeki VitrA/Artema değerlendirme oranıdır; "en iyi sıra" okunan listedeki en üst VitrA/Artema sırasıdır.

## 2. Kesit tablosu

Sütun okuma: Trendyol ve Hepsiburada "toplam · medyan (yöntem; eşleşen/okunan)"; Akakçe ve Cimri "toplam · en düşük fiyat medyanı · satıcı sayısı medyanı (yöntem; eşleşen/okunan)". Yöntem: `k+a` web kategorisi + arama, `a` arama, `k` kategoriye yönlenen arama. "VitrA/Artema adet (en iyi sıra)" eşleşen ürünler içindeki adet ve okunan listedeki en üst sıradır. "Yorum payı" eşleşen ürünlerin toplam değerlendirme sayısı içindeki paydır.

| Ana kategori > alt kategori | vitra.com.tr ürün ve fiyat aralığı (TL) | TY toplam · medyan | HB toplam · medyan | Akakçe toplam · medyan · satıcı | Cimri toplam · medyan · satıcı | VitrA/Artema adet (en iyi sıra) | En yüksek yorumlu marka (yorum payı) |
|---|---|---|---|---|---|---|---|
| Klozet > Yerden tek klozet (ayaklı klozet) | 13 ürün · 8.393-51.510 | 975 · 9.622 (k+a; 19/36) | 225 · 3.993 (a; 14/36) | 10 · 15.564 · 3 (k; 10/10) | 148 · 6.600 · 6 (a; 3/5) | TY 2 (5) · HB 1 (11) · AK 0 · CM 1 (3) | TY Turavit %60,8 |
| Klozet > Asma klozet takımı (klozet + gömme rezervuar seti) | 3 ürün · 26.111-44.390 | 2 · 13.319 (k+a; 2/2) | 449 · 6.525 (a; 26/36) | - · 8.926 · 1 (a; 31/32) | 4 · 6.923 · 7 (a; 1/1) | TY 0 · HB 8 (1) · AK 5 (1) · CM 0 | HB VitrA %90,4 |
| Klozet > Tuvalet taşı (alaturka) | 2 ürün · 5.420-5.420 | 1.010 · 1.600 (a; 8/36) | 13 · 1.392 (a; 13/13) | - · 828 · 1 (a; 15/15) | 18 · liste okunamadı (a) | TY 0 · HB 0 · AK 2 (1) | TY g'lly %37 |
| Klozet > Çocuk klozet | sayfa yok | 2.238 · 484 (a; 19/36) | 1.659 · 625 (a; 34/36) | - · 3.184 · 1 (a; 22/22) | 1.281 · 1.482 · 1 (a; 31/31) | TY 0 · HB 0 · AK 0 · CM 1 (5) | TY Babylike %34,7 |
| Klozet > Engelli klozet | sayfa yok | 43 · 2.137 (k+a; 36/36) | 135 · 3.259 (a; 34/36) | - · 2.275 · 1 (a; 32/32) | 133 · 38.000 · 2 (a; 18/18) | TY 0 · HB 0 · AK 0 · CM 1 (3) | TY MEDİLABS %45,7 |
| Lavabo > Çanak lavabo | 163 ürün · 5.680-26.707 | 1.420 · 3.500 (k+a; 25/36) | 2.711 · 3.925 (a; 32/36) | 1.718 · 4.396 · 4 (k; 32/32) | 908 · 6.267 · 2 (k; 24/29) | TY 0 · HB 9 (9) · AK 5 (6) · CM 7 (3) | TY Turkuaz %96,4 |
| Lavabo > Monoblok lavabo | 8 ürün · 92.019-134.580 | eşleşme yok | 106 · 26.877 (a; 36/36) | 100 · 30.888 · 3 (k; 32/32) | 219 · 34.204 · 1 (k; 28/28) | HB 1 (33) · AK 0 · CM 2 (18) | HB Turavit %76,5 |
| Lavabo > Yarım tezgah lavabo | 2 ürün · 6.100-7.014 | 12 · 6.779 (a; 10/12) | 13 · 6.199 (a; 13/13) | - · 5.500 · 1 (a; 11/11) | 30 · 4.469 · 2 (a; 5/5) | TY 0 · HB 0 · AK 0 · CM 0 | HB Raymer %100 |
| Lavabo > Etajerli lavabo | 47 ürün · 4.801-26.872 | 996 · 4.092 (k+a; 5/36) | 655 · 3.430 (a; 36/36) | 605 · 3.253 · 4 (k; 32/32) | 487 · 3.608 · 3 (k; 31/31) | TY 0 · HB 1 (15) · AK 1 (11) · CM 1 (29) | TY Turkuaz %100 |
| Lavabo > Ayaklı (standart) lavabo | 101 ürün · 2.966-16.330 | 1.281 · 199 (a; 2/36) | 800 · 6.528 (a; 36/36) | - · 6.014 · 1 (a; 32/32) | 379 · 6.410 · 1 (a; 11/11) | TY 0 · HB 0 · AK 1 (25) · CM 2 (4) | TY Fame Kıtchen %92,8 |
| Lavabo > Köşe lavabo | sayfa yok | 1.341 · 184 (a; 16/36) | 2.172 · 2.650 (a; 16/36) | - · 1.628 · 1 (a; 32/32) | 473 · 2.650 · 1 (a; 5/5) | TY 0 · HB 0 · AK 0 · CM 0 | TY Turkuaz %42,2 |
| Lavabo > Lavabo ayağı | sayfa yok | 1.585 · 199 (a; 3/36) | 5 · 1.435 (a; 2/5) | - · 1.979 · 2 (a; 1/5) | 41 · 3.599 · 2 (k; 12/14) | TY 0 · HB 1 (3) · AK 1 (2) · CM 0 | TY Fame Kıtchen %73,7 |
| Armatür > Bide bataryası | 33 ürün · 6.355-40.779 | 236 · 1.524 (a; 22/36) | 1.159 · 1.827 (a; 36/36) | 49 · 6.025 · 2 (k; 32/32) | 93 · 4.740 · 1 (a; 14/14) | TY 0 · HB 1 (24) · AK 8 (2) · CM 5 (3) | TY İZYAPI %53 |
| Armatür > Küvet bataryası | 61 ürün · 29.882-84.199 | 1.045 · 1.523 (a; 30/36) | 1.731 · 6.620 (a; 36/36) | - · 59.878 · 4 (a; 32/32) | 731 · 44.285 · 3 (a; 29/29) | TY 2 (22) · HB 3 (8) · AK 4 (9) · CM 3 (1) | TY (markasız) %57,6 |
| Armatür > Termostatik batarya | 110 ürün · 10.775-68.515 | 1.106 · 9.404 (a; 4/36) | 2.624 · 6.300 (a; 13/36) | - · 17.120 · 1 (a; 32/32) | 492 · 16.973 · 3 (a; 32/32) | TY 0 · HB 1 (6) · AK 0 · CM 7 (8) | TY OXYAQUA %96,3 |
| Armatür > Temassız (fotoselli) lavabo bataryası | 63 ürün · 11.902-49.996 | 994 · 5.425 (a; 2/36) | 588 · 8.425 (a; 34/36) | 362 · 7.703 · 7 (k; 32/32) | 465 · 9.554 · 4 (a; 30/30) | TY 0 · HB 4 (9) · AK 2 (7) · CM 1 (27) | TY STECELL %60 |
| Armatür > Duvardan (sıva üstü) banyo bataryası | 100 ürün · 7.736-38.545 | 381 · 3.193 (a; 36/36) | 878 · 5.781 (a; 36/36) | - · 3.293 · 6 (a; 32/32) | 301 · 3.934 · 3 (a; 28/28) | TY 19 (1) · HB 23 (1) · AK 13 (2) · CM 7 (2) | TY VitrA %83,8 |
| Armatür > Çanak lavabo bataryası (yüksek) | 68 ürün · 9.610-36.489 | 255 · 3.411 (k+a; 36/36) | 184 · 4.815 (a; 36/36) | - · 4.350 · 4 (a; 32/32) | 284 · 4.445 · 2 (a; 30/30) | TY 0 · HB 0 · AK 6 (1) · CM 2 (3) | TY RENA DESIGN %30,9 |
| Armatür > Ankastre stop valf | 32 ürün · 759-4.183 | 1.010 · 657 (a; 8/36) | 443 · 968 (a; 36/36) | - · 819 · 6 (a; 32/32) | 481 · 1.460 · 4 (k; 31/31) | TY 2 (26) · HB 21 (1) · AK 22 (1) · CM 20 (1) | TY Eca %91,6 |
| Armatür > Lavabo sifon ve süzgeci | 54 ürün · 1.203-60.892 | 249 · 325 (a; 36/36) | 462 · 997 (a; 36/36) | - · 422 · 1 (a; 32/32) | 307 · 1.511 · 2 (a; 6/6) | TY 3 (6) · HB 4 (17) · AK 1 (8) · CM 1 (2) | TY BİTERSE %32,5 |
| Armatür > Armatür tamamlayıcı (çıkış ucu, dirsek) | 106 ürün · 1.079-12.209 | 2 · 629 (a; 2/2) | 6 · 2.148 (a; 4/6) | - · 5.178 · 6 (a; 5/5) | 2 · liste okunamadı (a) | TY 0 · HB 0 · AK 4 (1) | TY EGZOZCUM %100 |
| Duşlar > Duş kolonu | 23 ürün · 10.310-52.660 | 1.233 · 1.370 (a; 32/36) | 442 · 6.900 (a; 36/36) | - · 7.015 · 6 (a; 32/32) | 683 · 15.360 · 2 (a; 30/30) | TY 2 (25) · HB 18 (1) · AK 12 (2) · CM 14 (1) | TY (markasız) %34 |
| Duşlar > El duşu takımı | 64 ürün · 1.924-21.039 | 1.378 · 1.499 (a; 9/36) | 10.000 · 2.000 (a; 17/36) | - · 2.883 · 6 (a; 32/32) | 887 · 2.508 · 3 (a; 31/31) | TY 3 (6) · HB 7 (4) · AK 27 (1) · CM 16 (1) | TY (markasız) %38,5 |
| Duşlar > Sürgülü el duşu takımı | 30 ürün · 3.504-15.726 | 69 · 3.788 (a; 36/36) | 562 · 3.250 (a; 33/36) | - · 3.695 · 4 (a; 32/32) | 263 · 3.510 · 3 (a; 32/32) | TY 26 (1) · HB 21 (2) · AK 25 (1) · CM 16 (1) | TY Artema %95,6 |
| Duşlar > Masajlı duş sistemi | 2 ürün · 18.642-18.642 | 1.298 · 350 (a; 25/36) | 1.110 · 6.410 (a; 30/36) | - · 11.861 · 1 (a; 32/32) | 53 · 17.972 · 4 (a; 6/6) | TY 2 (35) · HB 4 (1) · AK 9 (1) · CM 5 (1) | TY (markasız) %52,4 |
| Duşlar > Bataryalı duş sistemi | 56 ürün · 9.217-113.050 | 146 · 13.905 (a; 35/36) | 182 · 16.140 (a; 36/36) | - · 23.962 · 1 (a; 32/32) | 114 · 45.684 · 2 (a; 20/20) | TY 5 (3) · HB 4 (5) · AK 4 (1) · CM 0 | TY TİTAK HAYATIN KOLAY YANI %87,5 |
| Duşlar > Ankastre duş yönlendirici | 36 ürün · 1.938-23.955 | 30 · 13.356 (a; 30/30) | 98 · 7.348 (a; 36/36) | - · 830 · 1 (a; 9/9) | 6 · 22.808 · 3 (a; 1/1) | TY 11 (4) · HB 4 (3) · AK 3 (2) · CM 1 (1) | TY Ceyus %92,7 |
| Rezervuar > Rezervuar kumanda paneli (mekanik) | 35 ürün · 1.158-15.048 | 3 · 2.000 (a; 3/3) | 17 · 1.500 (a; 17/17) | - · 1.500 · 2 (a; 7/7) | 2 · liste okunamadı (a) | TY 2 (1) · HB 9 (2) · AK 3 (3) | TY VitrA %100 |
| Rezervuar > Rezervuar kumanda paneli (temassız) | 6 ürün · 12.515-15.312 | 9 · 11.037 (a; 9/9) | 4 · 12.444 (a; 4/4) | - · 10.482 · 3 (a; 7/7) | 1 · liste okunamadı (a) | TY 9 (1) · HB 4 (1) · AK 6 (1) | HB VitrA %100 |
| Rezervuar > Rezervuar kumanda paneli (akıllı) | 2 ürün · 29.729-29.729 | 2 · 26.752 (a; 2/2) | 7 · 4.932 (a; 7/7) | - · 11.952 · 1 (a; 5/5) | 8.879 · 388 · 3 (a; 27/27) | TY 2 (1) · HB 3 (1) · AK 0 · CM 0 | - |
| Rezervuar > Taşıyıcı aparat (asma klozet taşıyıcı) | 3 ürün · 9.662-10.637 | 1.657 · 1.938 (a; 7/36) | 2.738 · 16.760 (a; 2/36) | - · 6.750 · 26 (a; 5/5) | 2.918 · 10.144 · 2 (a; 30/30) | TY 0 · HB 2 (14) · AK 3 (3) · CM 7 (8) | TY Creavit %50 |
| Rezervuar > Duvar önü rezervuar | 8 ürün · 33.563-40.552 | 6 · 14.760 (a; 6/6) | 10 · 9.000 (a; 10/10) | - · 7.500 · 1 (a; 11/11) | 107 · 9.550 · 2 (a; 11/11) | TY 1 (1) · HB 0 · AK 0 · CM 0 | HB Geberit %66,7 |
| Rezervuar > Tuvalet taşı rezervuarı | 2 ürün · 4.566-4.566 | 27 · 707 (a; 13/27) | 15 · 3.000 (a; 4/15) | - · 3.000 · 1 (a; 7/7) | 3 · 2.800 · 3 (a; 1/1) | TY 0 · HB 0 · AK 1 (1) · CM 0 | - |
| Yıkanma alanları > Duş kanalı | 172 ürün · 659-15.070 | 1.103 · 305 (a; 21/36) | 1.876 · 697 (a; 36/36) | - · 671 · 2 (a; 32/32) | 1.142 · 2.244 · 2 (k; 30/30) | TY 1 (26) · HB 0 · AK 7 (2) · CM 11 (2) | TY Amentes %85 |
| Yıkanma alanları > Duş ünitesi (kompakt duş kabini) | 119 ürün · 47.680-160.889 | eşleşme yok | eşleşme yok | - · 1.155 · 1 (a; 32/32) | 5.496 · 1.399 · 1 (a; 19/19) | AK 0 · CM 0 | - |
| Yıkanma alanları > Hidromasajlı küvet | 84 ürün · 64.636-404.490 | 337 · 47.531 (a; 6/36) | 94 · 90.408 (a; 36/36) | - · 32.999 · 2 (a; 1/1) | 100 · liste okunamadı (a) | TY 0 · HB 0 · AK 0 | TY Waterway %100 |
| Yıkanma alanları > Bağımsız küvet | 44 ürün · 72.646-112.913 | 1.012 · 954 (a; 36/36) | 10.000 · 107.900 (a; 27/36) | - · 101.595 · 1 (a; 32/32) | 33 · liste okunamadı (a) | TY 0 · HB 1 (34) · AK 0 | TY Zuu Baby %97,6 |
| Yıkanma alanları > Küvet paneli | 9 ürün · 3.859-22.686 | 137 · 15.698 (a; 14/36) | 406 · 22.166 (a; 11/36) | - · 654 · 8 (a; 6/6) | 177 · liste okunamadı (a) | TY 0 · HB 0 · AK 0 | TY Waterway %66,7 |
| Yıkanma alanları > Duş teknesi paneli | 1 ürün · 1.960-1.960 | 501 · 6.543 (a; 36/36) | 262 · 10.205 (a; 36/36) | - · 8.459 · 1 (a; 6/6) | 1 · liste okunamadı (a) | TY 0 · HB 0 · AK 0 | TY Shower %36,8 |
| Yıkanma alanları > Kaydırmaz | 1 ürün · 758-758 | 1.174 · 357 (a; 36/36) | 667 · 800 (a; 35/36) | - · 439 · 1 (a; 32/32) | 880 · 279 · 1 (a; 3/3) | TY 0 · HB 0 · AK 0 · CM 0 | TY MappleHome %21,1 |
| Banyo mobilyası > Banyo tezgahı | 102 ürün · 1.006-127.618 | 13.959 · 227 (a; 31/36) | 10.000 · 2.720 (a; 26/36) | - · 1.965 · 1 (a; 32/32) | 4.761 · 4.632 · 2 (a; 7/7) | TY 0 · HB 1 (19) · AK 0 · CM 0 | TY zabata %34,4 |
| Banyo mobilyası > Banyo konsolu | 1 ürün · 9.214-9.214 | 2.020 · 1.320 (a; 14/36) | 811 · 2.146 (a; 24/36) | - · 2.999 · 29 (a; 5/5) | 259 · liste okunamadı (a) | TY 0 · HB 0 · AK 0 | TY nysamo %43,1 |
| Banyo mobilyası > Banyo set modülü | 18 ürün · 8.745-17.779 | 218 · 7.500 (k+a; 35/36) | 632 · 8.399 (a; 36/36) | - · 1.499 · 1 (a; 5/5) | 1 · liste okunamadı (a) | TY 0 · HB 3 (4) · AK 0 | TY Haus Modüler %84 |
| Banyo mobilyası > Malzemelik | 5 ürün · 801-3.747 | 4 · 5.838 (a; 4/4) | 10.000 · 4.999 (a; 1/36) | - · 390 · 2 (a; 5/5) | 4 · liste okunamadı (a) | TY 2 (1) · HB 0 · AK 0 | HB Özceden %100 |
| Banyo mobilyası > Dolap kulpu | 5 ürün · 455-1.139 | 2.012 · 50 (a; 35/36) | 853 · 97 (a; 36/36) | - · 69 · 4 (a; 32/32) | 1.111 · 15.354 · 1 (a; 4/4) | TY 0 · HB 0 · AK 0 · CM 0 | TY MASALL %37,1 |
| Banyo mobilyası > Dolap ayağı | 4 ürün · 1.454-1.838 | 1.423 · 110 (a; 35/36) | 241 · 716 (a; 29/36) | - · 1.519 · 2 (a; 1/5) | 62 · liste okunamadı (a) | TY 0 · HB 0 · AK 0 | TY Meleni Home %40,2 |
| Banyo mobilyası > Makyaj aynası | 15 ürün · 1.371-16.123 | 14.016 · 237 (a; 31/36) | 10.000 · 232 (a; 36/36) | 5.274 · 593 · 2 (k; 32/32) | 9.870 · 1.039 · 3 (a; 29/29) | TY 0 · HB 0 · AK 0 · CM 2 (14) | TY Acarlar Ticaret %20 |
| Banyo mobilyası > Aynalı dolap | 180 ürün · 9.526-67.142 | 1.514 · 1.175 (a; 11/36) | 766 · 2.950 (a; 23/36) | 1.433 · 7.200 · 3 (k; 32/32) | 1.240 · 7.399 · 2 (k; 31/31) | TY 0 · HB 1 (30) · AK 1 (28) · CM 0 | TY TETTO ELAGANTE %37 |
| Banyo aksesuarı > Sabunluk | 70 ürün · 611-25.014 | 16.533 · 199 (k+a; 36/36) | 10.000 · 341 (a; 36/36) | - · 571 · 2 (a; 32/32) | 5.194 · 410 · 1 (a; 30/30) | TY 0 · HB 0 · AK 0 · CM 0 | TY Okyanus Home %24,9 |
| Banyo aksesuarı > Diş fırçalığı | 18 ürün · 611-6.993 | 557 · 279 (k+a; 36/36) | 1.873 · 934 (a; 36/36) | - · 687 · 2 (a; 32/32) | 1.341 · 1.965 · 1 (a; 30/30) | TY 3 (6) · HB 6 (2) · AK 4 (9) · CM 12 (2) | TY Toptanpro %79 |
| Banyo aksesuarı > Tuvalet kağıtlığı | 47 ürün · 854-5.085 | 8.397 · 184 (a; 36/36) | 10.000 · 225 (a; 36/36) | 3.894 · 1.733 · 8 (k; 32/32) | 7.301 · 1.013 · 4 (a; 30/30) | TY 0 · HB 2 (22) · AK 9 (3) · CM 6 (1) | TY zabata %41,6 |
| Banyo aksesuarı > Tuvalet fırçası | 27 ürün · 1.402-15.070 | 4.271 · 197 (k+a; 36/36) | 10.000 · 200 (a; 36/36) | 3.158 · 770 · 4 (k; 32/32) | 4.573 · 891 · 2 (a; 30/30) | TY 0 · HB 0 · AK 10 (2) · CM 0 | TY Kitchen Beauty %14,2 |
| Banyo aksesuarı > Banyo askısı | 37 ürün · 397-6.627 | 31.054 · 149 (a; 21/36) | 10.000 · 150 (a; 36/36) | 2.472 · 551 · 8 (k; 32/32) | - | TY 0 · HB 1 (31) · AK 10 (1) | TY zabata %32,8 |
| Banyo aksesuarı > Banyo çöp kovası | 10 ürün · 1.634-20.199 | 4.963 · 299 (a; 21/36) | 10.000 · 1.094 (a; 36/36) | 554 · 1.027 · 6 (k; 32/32) | - | TY 0 · HB 0 · AK 3 (24) | TY origa %15 |
| Banyo aksesuarı > Havluluk | 43 ürün · 611-18.617 | 14.326 · 166 (a; 8/36) | 10.000 · 199 (a; 36/36) | 3.011 · 1.177 · 6 (k; 32/32) | - | TY 0 · HB 1 (8) · AK 11 (3) | TY zabata %48 |
| Vitrifiye tamamlayıcı > Pisuvar ara bölmesi | 1 ürün · 4.059-4.059 | 29 · 5.199 (k+a; 29/29) | 41 · 4.775 (a; 36/36) | - · 3.229 · 3 (a; 11/11) | - | TY 1 (22) · HB 1 (17) · AK 0 | - |
| Vitrifiye tamamlayıcı > Pisuvar yıkama sistemi | 12 ürün · 7.412-12.468 | 13 · 12.437 (a; 13/13) | 71 · 14.949 (a; 36/36) | - · 10.656 · 1 (a; 31/31) | - | TY 7 (1) · HB 9 (2) · AK 5 (1) | - |

Kaynak: Trendyol, Hepsiburada, Akakçe, Cimri arama ve kategori listeleri; vitra.com.tr kategori sayfaları | 30.09.2026

## 3. Rakip mağazalar (eşleşen ürün sayısı · fiyat medyanı · VitrA/Artema adedi)

Hücre biçimi: `eşleşen · medyan · V<adet>`. "-" ilgili mağazanın aramasında eşleşen ürün bulunmadığını gösterir. Koçtaş çok satan sıralamasını, diğer mağazalar arama sırasını yansıtır; Bauhaus ve Banyomega sonuçları kısıtlıdır.

| Alt kategori | Koçtaş | Bauhaus | Banyomarka | Banyomega | Banyoline | Creavit e-mağaza |
|---|---|---|---|---|---|---|
| Yerden tek klozet (ayaklı klozet) | - | - | 5 · 3.625 | - | 1 · 950 | 17 · 8.085 |
| Asma klozet takımı (klozet + gömme rezervuar seti) | 1 · 11.620 | - | - | - | 18 · 14.425 · V11 | 14 · 8.283 |
| Tuvalet taşı (alaturka) | 1 · 5.869 · V1 | - | - | - | 5 · 2.905 · V1 | 1 · 3.729 |
| Çocuk klozet | 3 · 1.200 | - | 29 · 11.425 · V13 | 7 · 8.000 · V3 | 1 · 819 | 1 · 21.186 |
| Engelli klozet | 15 · 40.000 | 1 · 13.500 | 25 · 18.372 · V13 | 7 · 13.969 · V6 | 6 · 418 | - |
| Çanak lavabo | 22 · 5.315 | 9 · 7.500 | 32 · 13.595 · V9 | 22 · 15.340 | 12 · 3.293 · V1 | 24 · 7.686 |
| Monoblok lavabo | 39 · 37.500 | - | 31 · 60.025 · V11 | 24 · 21.168 | - | - |
| Yarım tezgah lavabo | 2 · 3.346 | - | 30 · 11.150 · V21 | 1 · 5.794 | 6 · 4.295 | - |
| Etajerli lavabo | 48 · 11.385 · V2 | - | 32 · 10.850 · V25 | 24 · 10.808 · V6 | 17 · 7.468 | 7 · 5.031 |
| Ayaklı (standart) lavabo | 34 · 7.716 | - | 27 · - · V12 | 2 · 41.850 | 21 · 7.989 | - |
| Köşe lavabo | 15 · 3.165 | - | 23 · 18.950 · V19 | 22 · 5.334 | 11 · 1.684 · V1 | - |
| Lavabo ayağı | 1 · 1.459 | - | 23 · 3.100 · V10 | - | 3 · 4.992 | 1 · 9.720 |
| Bide bataryası | 5 · 13.516 · V2 | - | 32 · 11.385 · V7 | 6 · 6.318 | - | - |
| Küvet bataryası | 48 · 31.673 · V2 | - | 32 · 53.875 · V13 | 21 · 41.400 · V9 | 14 · 4.271 · V7 | - |
| Termostatik batarya | 26 · 27.954 · V1 | 4 · 11.790 | 26 · 31.950 · V3 | 23 · 49.020 · V3 | 2 · 25.627 · V2 | 4 · 29.160 |
| Temassız (fotoselli) lavabo bataryası | 47 · 14.700 · V9 | 2 · 14.990 | 29 · 16.450 · V7 | 24 · 39.645 · V17 | 17 · 7.178 | - |
| Duvardan (sıva üstü) banyo bataryası | 30 · 7.419 · V8 | - | 26 · 8.575 · V9 | 6 · 8.110 · V4 | 10 · 3.646 · V9 | - |
| Çanak lavabo bataryası (yüksek) | 47 · 5.601 | - | 1 · - | 14 · 17.590 · V3 | 24 · 5.605 · V10 | 24 · 7.350 |
| Ankastre stop valf | 1 · 1.104 | 11 · 1.490 · V2 | 32 · 1.800 · V10 | 24 · 2.052 · V6 | 8 · 1.280 · V3 | 13 · 1.890 |
| Lavabo sifon ve süzgeci | 48 · 996 · V8 | - | 15 · - | 2 · 1.994 | 13 · 760 · V7 | 22 · 1.800 |
| Armatür tamamlayıcı (çıkış ucu, dirsek) | 41 · 6.020 · V10 | - | - | - | 7 · 3.650 · V7 | 1 · 8.172 |
| Duş kolonu | 40 · 11.164 · V14 | 4 · 6.390 · V1 | 24 · 20.075 · V4 | 15 · 39.700 · V3 | 6 · 6.131 · V3 | 10 · 16.200 |
| El duşu takımı | 48 · 3.250 · V20 | 2 · 1.845 · V1 | 32 · 1.950 · V9 | 6 · 4.455 | 16 · 2.571 · V14 | 4 · 1.944 |
| Sürgülü el duşu takımı | 46 · 3.808 · V33 | - | 32 · 8.550 · V32 | 2 · 18.110 | 14 · 5.600 · V11 | 6 · 3.348 |
| Masajlı duş sistemi | 14 · 17.684 · V9 | - | 16 · 17.311 · V9 | 5 · 17.442 · V4 | 2 · 14.937 · V2 | - |
| Bataryalı duş sistemi | 32 · 16.700 · V2 | - | 29 · 32.185 | 23 · 68.880 | 7 · 10.502 · V5 | 19 · 9.396 |
| Ankastre duş yönlendirici | 1 · 5.707 · V1 | - | 5 · - · V5 | - | 21 · 4.937 · V15 | 3 · 11.880 |
| Rezervuar kumanda paneli (mekanik) | 3 · 3.500 · V2 | - | - | 1 · 2.540 · V1 | 5 · 3.355 · V3 | 24 · 1.728 |
| Rezervuar kumanda paneli (temassız) | 3 · 11.246 · V3 | - | - | - | 5 · 3.355 · V3 | 24 · 1.728 |
| Rezervuar kumanda paneli (akıllı) | 43 · 3.584 · V4 | - | - | - | 5 · 3.355 · V3 | 24 · 1.728 |
| Taşıyıcı aparat (asma klozet taşıyıcı) | - | - | - | - | 4 · 5.083 | 3 · 7.920 |
| Duvar önü rezervuar | 5 · 6.899 | - | 26 · 11.678 · V7 | 6 · 20.222 | 21 · 6.606 · V8 | 10 · 7.425 |
| Tuvalet taşı rezervuarı | 4 · 8.155 · V1 | - | - | - | 3 · 2.793 · V1 | 7 · 6.930 |
| Duş kanalı | 2 · 6.013 | - | 31 · 3.650 | 17 · 2.384 | 15 · 1.375 · V2 | - |
| Duş ünitesi (kompakt duş kabini) | 1 · 135 | - | - | - | - | - |
| Hidromasajlı küvet | 48 · 27.782 | - | 31 · 254.250 · V17 | - | 6 · 418 | - |
| Bağımsız küvet | 4 · 17.812 | - | - | 13 · 150.552 | 6 · 418 | - |
| Küvet paneli | 6 · 7.175 | - | - | - | 11 · 3.213 · V8 | 24 · 1.728 |
| Duş teknesi paneli | 3 · 14.783 | - | - | - | 6 · 4.011 · V4 | 10 · 1.200 |
| Kaydırmaz | 3 · 699 | - | - | - | - | - |
| Banyo tezgahı | 3 · 9.399 | - | - | 24 · 3.263 | - | 21 · 4.680 |
| Banyo konsolu | 16 · 7.199 | - | 2 · - | - | - | - |
| Banyo set modülü | 19 · 10.189 · V1 | - | - | - | 19 · 12.040 · V10 | 19 · 11.484 |
| Malzemelik | 1 · 7.199 | - | - | - | 24 · 30.432 · V1 | 4 · 21.978 |
| Dolap kulpu | 48 · 120 | - | - | - | - | - |
| Dolap ayağı | 1 · 5.699 | - | - | - | 3 · 4.992 | - |
| Makyaj aynası | 22 · 8.757 | 5 · 1.690 | 32 · 6.598 · V4 | - | - | 24 · 9.212 |
| Aynalı dolap | 35 · 6.035 | 24 · 6.890 · V2 | 27 · - · V16 | - | 24 · 16.213 | 10 · 7.012 |
| Sabunluk | 48 · 454 · V1 | 24 · 759 | 31 · 2.502 · V10 | 24 · 2.677 · V1 | 3 · 303 · V1 | 7 · 2.100 |
| Diş fırçalığı | 48 · 4.894 · V8 | 1 · 459 | 32 · 2.375 · V22 | 10 · 1.493 · V1 | 3 · 1.386 · V2 | 5 · 1.344 |
| Tuvalet kağıtlığı | 48 · 441 · V3 | 20 · 890 | 32 · 2.800 · V10 | 24 · 3.257 · V6 | 8 · 1.721 · V8 | 13 · 2.310 |
| Tuvalet fırçası | 48 · 998 | 24 · 1.209 | 32 · 3.990 | 18 · 12.176 | 3 · 3.895 · V3 | 8 · 2.328 |
| Banyo askısı | 46 · 824 | 6 · 984 | - | 9 · 2.776 | - | 1 · 1.596 |
| Banyo çöp kovası | 36 · 974 · V1 | 24 · 1.290 | 23 · 4.100 · V8 | 1 · 7.624 | - | 4 · 4.788 |
| Havluluk | 48 · 620 · V1 | 13 · 469 | 31 · 3.550 · V6 | 22 · 3.829 | 12 · 1.114 · V8 | 13 · 1.890 |
| Pisuvar ara bölmesi | 9 · 3.750 | - | - | 14 · 4.487 | 1 · 4.345 · V1 | - |
| Pisuvar yıkama sistemi | 5 · 3.199 · V1 | - | 26 · 5.055 · V10 | 2 · 23.070 · V1 | 5 · 6.450 · V3 | - |

Kaynak: ilgili mağazanın arama sayfası (ilk sonuç sayfası) | 30.09.2026

## 4. vitra.com.tr kategori sayfaları

Ürün sayısı sayfadaki "N sonuç listeleniyor" değeridir ve renk/varyant kartlarını içerir. Fiyat aralığı liste fiyatıdır ("Fiyata Göre Artan/Azalan" sıralamalarının ilk kartları). "Stokta yok" sayfa toplamı ile "Sadece stoklu ürünleri göster" süzgeci toplamı arasındaki farktır; kartlarda bu ürünler "Gelince Haber Ver" düğmesiyle görünür. "Ücretsiz Montaj (liste)" `/c-ucretsiz-montaj` listesinde kategori etiketiyle eşleşen ürün sayısıdır.

| Alt kategori | Site sayfası | Ürün (varyant) | Fiyat aralığı (TL) | Stoklu | Stokta yok | Ücretsiz Montaj (liste) | İlk sayfada Ücretsiz Montaj | İlk sayfada "Sepette indirim" |
|---|---|---|---|---|---|---|---|---|
| Yerden tek klozet (ayaklı klozet) | /c-yerden-tek-klozetler | 13 | 8.393-51.510 | 3 | 10 | 0 | 0/13 | 8/13 |
| Asma klozet takımı (klozet + gömme rezervuar seti) | /c-asma-klozet-takimlari | 3 | 26.111-44.390 | 1 | 2 | 1 | 1/3 | 3/3 |
| Tuvalet taşı (alaturka) | /c-tuvalet-tasi | 2 | 5.420-5.420 | 1 | 1 | 0 | 0/2 | 1/2 |
| Çanak lavabo | /c-canak-lavabolar | 163 | 5.680-26.707 | 72 | 91 | 0 | 0/20 | 20/20 |
| Monoblok lavabo | /c-monoblok-lavabolar | 8 | 92.019-134.580 | 3 | 5 | 0 | 0/8 | 3/8 |
| Yarım tezgah lavabo | /c-yarim-tezgah-lavabolar | 2 | 6.100-7.014 | 0 | 2 | 0 | 0/2 | 2/2 |
| Etajerli lavabo | /c-etajerli-lavabolar | 47 | 4.801-26.872 | 9 | 38 | 0 | 0/20 | 20/20 |
| Ayaklı (standart) lavabo | /c-standart-lavabo-ve-ayaklari | 101 | 2.966-16.330 | 13 | 88 | 0 | 0/20 | 19/20 |
| Bide bataryası | /c-bide-bataryalari | 33 | 6.355-40.779 | 0 | 33 | 0 | 0/20 | 8/20 |
| Küvet bataryası | /c-kuvet-bataryalari | 61 | 29.882-84.199 | 7 | 54 | 0 | 0/20 | 12/20 |
| Termostatik batarya | /c-termostatik-bataryalar | 110 | 10.775-68.515 | 24 | 86 | 0 | 0/20 | 18/20 |
| Temassız (fotoselli) lavabo bataryası | /c-temassiz-lavabo-bataryalari | 63 | 11.902-49.996 | 16 | 47 | 12 | 10/20 | 16/20 |
| Duvardan (sıva üstü) banyo bataryası | /c-duvardan-banyo-bataryalari | 100 | 7.736-38.545 | 25 | 75 | 0 | 0/20 | 20/20 |
| Çanak lavabo bataryası (yüksek) | /c-canak-lavabo-bataryalari | 68 | 9.610-36.489 | 37 | 31 | 0 | 0/20 | 20/20 |
| Ankastre stop valf | /c-ankastre-stop-valfler | 32 | 759-4.183 | 22 | 10 | 0 | 0/20 | 20/20 |
| Lavabo sifon ve süzgeci | /c-lavabo-sifon-ve-suzgecleri | 54 | 1.203-60.892 | 32 | 22 | 0 | 0/20 | 20/20 |
| Armatür tamamlayıcı (çıkış ucu, dirsek) | /c-banyo-batarya-cikis-uclari | 75 | 4.222-12.209 | 43 | 32 | 0 | 0/20 | 20/20 |
| Armatür tamamlayıcı (çıkış ucu, dirsek) | /c-dus-dirsekleri | 31 | 1.079-2.359 | 18 | 13 | 0 | 0/20 | 18/20 |
| Duş kolonu | /c-dus-kolonlari | 23 | 10.310-52.660 | 21 | 2 | 0 | 0/20 | 20/20 |
| El duşu takımı | /c-el-dusu-takimlari | 64 | 1.924-21.039 | 57 | 7 | 0 | 0/20 | 20/20 |
| Sürgülü el duşu takımı | /c-surgulu-el-dusu-takimlari | 30 | 3.504-15.726 | 26 | 4 | 0 | 0/20 | 20/20 |
| Masajlı duş sistemi | /c-masajli-dus-sistemleri | 2 | 18.642-18.642 | 0 | 2 | 0 | 0/2 | 0/2 |
| Bataryalı duş sistemi | /c-bataryali-dus-sistemleri | 56 | 9.217-113.050 | 15 | 41 | 0 | 0/20 | 12/20 |
| Ankastre duş yönlendirici | /c-ankastre-dus-yonlendiriciler | 36 | 1.938-23.955 | 16 | 20 | 0 | 0/20 | 17/20 |
| Rezervuar kumanda paneli (mekanik) | /c-mekanik-kumanda-panelleri | 35 | 1.158-15.048 | 21 | 14 | 0 | 0/20 | 20/20 |
| Rezervuar kumanda paneli (temassız) | /c-temassiz-kumanda-panelleri | 6 | 12.515-15.312 | 2 | 4 | 0 | 0/6 | 6/6 |
| Rezervuar kumanda paneli (akıllı) | /c-akilli-kumanda-panelleri | 2 | 29.729-29.729 | 1 | 1 | 0 | 0/2 | 1/2 |
| Taşıyıcı aparat (asma klozet taşıyıcı) | /c-tasiyici-aparatlar | 3 | 9.662-10.637 | 0 | 3 | 0 | 0/3 | 3/3 |
| Duvar önü rezervuar | /c-duvar-onu-rezervuarlar | 8 | 33.563-40.552 | 0 | 8 | 0 | 0/8 | 4/8 |
| Tuvalet taşı rezervuarı | /c-tuvalet-taslari-icin-gomme-rezervuarlar | 2 | 4.566-4.566 | 1 | 1 | 0 | 0/2 | 2/2 |
| Duş kanalı | /c-dus-kanallari | 172 | 659-15.070 | 15 | 157 | 0 | 0/20 | 19/20 |
| Duş ünitesi (kompakt duş kabini) | /c-dus-uniteleri | 119 | 47.680-160.889 | 0 | 119 | 0 | 0/20 | 20/20 |
| Hidromasajlı küvet | /c-hidromasajli-bagimsiz-kuvetler | 23 | 122.097-404.490 | 0 | 23 | 0 | 0/20 | 20/20 |
| Hidromasajlı küvet | /c-hidromasajli-standart-kuvetler | 61 | 64.636-244.857 | 1 | 60 | 0 | 0/20 | 20/20 |
| Bağımsız küvet | /c-hidromasajsiz-bagimsiz-kuvetler | 44 | 72.646-112.913 | 0 | 44 | 0 | 0/20 | 20/20 |
| Küvet paneli | /c-kuvet-panelleri | 9 | 3.859-22.686 | 1 | 8 | 0 | 0/9 | 9/9 |
| Duş teknesi paneli | /c-dus-teknesi-panelleri | 1 | 1.960-1.960 | 0 | 1 | 0 | 0/1 | 1/1 |
| Kaydırmaz | /c-vitra-kaydirmaz | 1 | 758-758 | 0 | 1 | 0 | 0/1 | 1/1 |
| Banyo tezgahı | /c-banyo-tezgahlari | 102 | 1.006-127.618 | 6 | 96 | 1 | 1/20 | 20/20 |
| Banyo konsolu | /c-banyo-konsollari | 1 | 9.214-9.214 | 0 | 1 | 0 | 0/1 | 1/1 |
| Banyo set modülü | /c-banyo-set-modulleri | 18 | 8.745-17.779 | 3 | 15 | 0 | 0/18 | 18/18 |
| Malzemelik | /c-banyo-malzemelikleri | 5 | 801-3.747 | 2 | 3 | 0 | 0/5 | 5/5 |
| Dolap kulpu | /c-banyo-dolabi-kulplari | 5 | 455-1.139 | 3 | 2 | 1 | 1/5 | 5/5 |
| Dolap ayağı | /c-banyo-dolap-ayaklari | 4 | 1.454-1.838 | 0 | 4 | 1 | 1/4 | 4/4 |
| Makyaj aynası | /c-makyaj-aynalari-ve-diger-aksesuarlar | 15 | 1.371-16.123 | 7 | 8 | 0 | 0/15 | 15/15 |
| Aynalı dolap | /c-aynali-banyo-dolabi | 180 | 9.526-67.142 | 21 | 159 | 15 | 8/20 | 20/20 |
| Sabunluk | /c-sabunluklar | 70 | 611-25.014 | 21 | 49 | 8 | 4/20 | 20/20 |
| Diş fırçalığı | /c-dis-fircaliklari | 18 | 611-6.993 | 8 | 10 | 0 | 0/18 | 11/18 |
| Tuvalet kağıtlığı | /c-tuvalet-kagitliklari | 47 | 854-5.085 | 21 | 26 | 0 | 0/20 | 18/20 |
| Tuvalet fırçası | /c-tuvalet-fircalari | 27 | 1.402-15.070 | 12 | 15 | 0 | 0/20 | 13/20 |
| Banyo askısı | /c-banyo-askilari | 37 | 397-6.627 | 15 | 22 | 0 | 0/20 | 18/20 |
| Banyo çöp kovası | /c-banyo-cop-kovalari | 10 | 1.634-20.199 | 4 | 6 | 0 | 0/10 | 10/10 |
| Havluluk | /c-havluluklar | 43 | 611-18.617 | 26 | 17 | 0 | 0/20 | 19/20 |
| Pisuvar ara bölmesi | /c-pisuvar-ara-bolmeleri | 1 | 4.059-4.059 | 0 | 1 | 0 | 0/1 | 1/1 |
| Pisuvar yıkama sistemi | /c-pisuvar-yikama-sistemleri | 12 | 7.412-12.468 | 0 | 12 | 0 | 0/12 | 12/12 |

Özel sayfalar:

| Sayfa | Yol | Ürün (varyant) | Fiyat medyanı (TL) | Kategori dağılımı (ilk 6) |
|---|---|---|---|---|
| online-ozel | /c-online-ozel | - | - |  |
| kampanyali-urunler | /c-kampanyali-urunler | 413 | 5.468 | Ankastre Bataryalar: 23, Tek Armatür Delikli Lavabo Bataryaları: 21, Lavabo Sifon ve Süzgeçleri: 20, Ankastre Stop Valfler: 17, Ankastre Lavabo Bataryaları: 16, Çanak Lavabo Bataryaları: 16 |
| ucretsiz-montaj | /c-ucretsiz-montaj | 89 | 30.771 | Lavabo Dahil Lavabo Dolapları: 27, Aynalı Banyo Dolabı: 15, Temassız Lavabo Bataryaları: 12, Banyo Boy Dolapları: 10, Sabunluklar: 8, Düz Aynalar: 4 |

Kaynak: vitra.com.tr kategori sayfaları | 30.09.2026. `/c-online-ozel` sayfası tarayıcıda "redirected you too many times" (ERR_TOO_MANY_REDIRECTS) yanıtı vermiştir (çerezsiz istekte de aynı); sayfa sitemap'te listelenmektedir. `/c-kampanyali-urunler` toplamı 413 varyanttır, ilk 240 kart okunmuştur.

## 5. Bulgular

➔ **VitrA/Artema, duş ve batarya tamamlayıcılarında pazaryeri listelerinin büyük bölümünü doldurmaktadır.** Sürgülü el duşu takımında Trendyol 36 ürünün 26'sı (sıra 1; VitrA/Artema yorum payı %96,9), Hepsiburada 33'ün 21'i, Akakçe 32'nin 25'i, Cimri 32'nin 16'sı VitrA/Artema'dır. Ankastre stop valfte Hepsiburada 36'nın 21'i, Akakçe 32'nin 22'si, Cimri 31'in 20'si (üç kanalda da sıra 1); duvardan (sıva üstü) banyo bataryasında Trendyol 36'nın 19'u (VitrA/Artema yorum payı %89,7) ve Hepsiburada 36'nın 23'ü (sıra 1); temassız kumanda panelinde Trendyol 9/9, Hepsiburada 4/4, Akakçe 6/7 ürün VitrA/Artema'dır. El duşu takımında Akakçe 27/32 ve Cimri 16/31 ile öne çıkmaktadır.

➔ **11 alt kategoride dört listede (Trendyol, Hepsiburada, Akakçe, Cimri) hiç VitrA/Artema ürünü görülmemiştir:** yarım tezgah lavabo, köşe lavabo, duş ünitesi, hidromasajlı küvet, küvet paneli, duş teknesi paneli, kaydırmaz, banyo konsolu, dolap kulpu, dolap ayağı ve sabunluk. Bunlardan 10'unda vitra.com.tr'de ürün sayfası bulunmaktadır (sabunluk 70, duş ünitesi 119, hidromasajlı küvet 84, küvet paneli 9, dolap kulpu 5, dolap ayağı 4, yarım tezgah lavabo 2, duş teknesi paneli, kaydırmaz ve banyo konsolu 1'er varyant); köşe lavabo için ayrı sayfa yoktur. VitrA/Artema ürünleri Banyomarka'da listelenmektedir (yarım tezgah lavabo 21, köşe lavabo 19, sabunluk 10 eşleşen ürün), yani ürünün kendisi başka bir kanalda satışta görünmektedir.

➔ **vitra.com.tr'de taranan 55 kategori sayfasında 2.258 renk/varyant kartının 1.606'sı (%71,1) stoklu süzgecinin dışında kalmaktadır ve 13 alt kategoride stoklu ürün bulunmamaktadır** (kartların tamamı "Gelince Haber Ver"): yarım tezgah lavabo (2), bide bataryası (33), masajlı duş sistemi (2), taşıyıcı aparat (3), duvar önü rezervuar (8), duş ünitesi (119), bağımsız küvet (44), duş teknesi paneli (1), kaydırmaz (1), banyo konsolu (1), dolap ayağı (4), pisuvar ara bölmesi (1), pisuvar yıkama sistemi (12); hidromasajlı küvette 84 kartın yalnızca 1'i stoklu. Ürün sayısı ≥20 olan kategorilerde stokta yok oranı %80 üzerinde olanlar: duş kanalı 157/172, aynalı dolap 159/180, banyo tezgahı 96/102, ayaklı lavabo 88/101, küvet bataryası 54/61, etajerli lavabo 38/47. Pazaryerinde görünmeyen 11 kesitin birçoğu bu tabloyla örtüşmektedir.

➔ **Aynı model kodunda pazaryeri fiyatları vitra.com.tr liste fiyatının altında, "Sepette %N indirim" fiyatına yakın ya da üstünde okunmaktadır.** 122 model kodu için 193 eşleşmede (tam kod eşleşmesi) pazaryeri fiyatı liste fiyatının medyan %14,1 altındadır: Akakçe -%17,7 (57 eşleşme), Cimri -%14,2 (40), Trendyol -%14,0 (44), Hepsiburada -%2,7 (52). Sitedeki "Sepette" fiyatına (liste fiyatı x (1 - indirim oranı)) göre fark Akakçe -%8,0, Cimri -%2,0, Trendyol -%0,8 ve Hepsiburada +%10,0'dır. Örnekler: temassız kumanda paneli 768-0880 Akakçe 6.406 TL / site 12.515 TL; ankastre stop valf A41441 Akakçe ve Cimri (PttAVM) 450 TL / site 759 TL; mekanik kumanda paneli 740-2211 Akakçe 998 TL, Hepsiburada 999 TL / site 1.678 TL.

➔ **Sekiz kesitte tek marka değerlendirme hacminin %85'inden fazlasını toplamaktadır.** Çanak lavabo (Trendyol) Turkuaz %96,4 ve etajerli lavabo (Hepsiburada) Turkuaz %94,2; sürgülü el duşu takımında Artema (Trendyol %95,6, Hepsiburada %88,3); ankastre duş yönlendiricide Ceyus (Trendyol %92,7, Hepsiburada %90,2); bağımsız küvette Zuu Baby (Trendyol %97,6) ve Flora (Hepsiburada %87,5); duş kanalında Amentes (Trendyol %85,0); küvet panelinde Sırduş (Hepsiburada %100). VitrA çanak lavabo aramasında Trendyol'da eşleşen 25 üründe yer almazken Hepsiburada'da 9 ürünle (en iyi sıra 9), Akakçe'de 5 (sıra 6), Cimri'de 7 (sıra 3) ürünle görünmektedir.

➔ **Satıcı yapısı iki kanalda farklıdır.** Trendyol'da VitrA/Artema satırlarının %35'i (124 satırın 43'ü) VitrA resmi mağazasından, kalanı 37 farklı satıcıdan gelmektedir (EnarHome 16 satır ve 6 kesit; AL-BA HOME, uygunyapimarket 5'er satır). Hepsiburada'da VitrA mağazası %12 (198 satırın 23'ü), Hepsiburada platformu %11 (22) ve 69 farklı satıcı yer almaktadır (GEYLANİ DAYANIKLI TÜKETİM 10, EnarHome 10, uygunyapimarket 7, VİMAR YAPI 6, BANYO MARE 6). VitrA resmi mağazası Trendyol'da 16 kesitte, Hepsiburada'da 13 kesitte görülmektedir.

➔ **Rakip mağazalarda VitrA, Banyomarka ve Banyoline'da geniş, Bauhaus'ta sınırlı yer almaktadır.** Banyomarka'da 249 eşleşen VitrA satırı (28 kesit; Grohe 203, Artema 96, Duravit 64), Banyoline'da 125 (32 kesit), Koçtaş'ta VitrA 84 (25 kesit) ve Artema 64 satır; Bauhaus'ta VitrA 3, Artema 3 satır. Banyomarka'da sürgülü el duşu takımında eşleşen 32 ürünün 32'si, yarım tezgah lavabo kesitinde 30'un 21'i, etajerli lavabo kesitinde 32'nin 25'i VitrA/Artema'dır; yarım tezgah lavabo pazaryeri listelerinde hiç görünmemekte, etajerli lavabo Hepsiburada, Akakçe ve Cimri'de 1'er ürünle sınırlı kalmaktadır. Creavit e-mağazasında listelenen 426 eşleşen ürünün 419'u indirimli (medyan indirim %40,0); Banyomarka'da 307 ürünün tamamı indirimli (medyan %44,5, eski fiyat alanı tutarsız olabilmektedir), Koçtaş'ta %4, Trendyol'da %13 (medyan indirim %5,2), Hepsiburada'da %5 (%4,0).

➔ **vitra.com.tr'de çocuk klozet, engelli klozet, köşe lavabo ve lavabo ayağı için ayrı kategori sayfası bulunmazken pazaryeri aramaları bu alanlarda hacim göstermektedir.** Çocuk klozet aramasında Trendyol 2.238, Hepsiburada 1.659 sonuç (listelerin büyük bölümü klozet adaptörü ve oturak ürünüdür; Trendyol'da 36 ürünün 19'u eşleşmiştir); engelli klozeti Trendyol'da 43 ürünlük ayrı bir web kategorisidir (en yüksek yorumlu marka MEDİLABS %45,7); köşe lavabo aramasında Trendyol 1.341, Hepsiburada 2.172 sonuç bulunmaktadır. Banyomarka'da VitrA çocuk klozeti (Arkitekt Kurbağa, Sento çocuk serisi), Bedensel Engelli Klozeti (Integra, Conforma; 14 ürün) ve Arkitekt Köşe Lavabo listelenmektedir; pazaryeri listelerinde bu kesitlerde yalnızca Cimri'de 1'er VitrA ürünü görülmüştür.

## 6. Rapor geneli için gözlemler

- **Fiyat tutarsızlığı, iki yönde:** Aynı model kodunda 3P satıcılarda vitra.com.tr liste fiyatının 2 ila 2,5 katı fiyatlar okunmuştur: pisuvar yıkama sistemi 310-2521 site 7.412 TL, Hepsiburada'da üç satıcıda 14.848-15.923 TL; Root Round küvet bataryası A42743 site 29.882 TL, Hepsiburada EKM Store 65.948 TL; Arkitekta köşe malzemelik A44051 site 3.747 TL, Trendyol'da 10.129 TL. Akakçe ve Cimri tarafında ise site fiyatının %40 altında teklifler görülmektedir (bkz. Bulgular). Ürün adında model kodu verilmeyen satırlar karşılaştırmaya girmemiştir.
- **Stok:** vitra.com.tr'de 13 alt kategoride hiç stoklu ürün yoktur ve `/c-ucretsiz-montaj` listesindeki 89 ürünün 42'si (%47) "Gelince Haber Ver" durumundadır. Kartlarda fiyat gösterilmeye devam ettiğinden (fiyatsız kart 771 kategori kartında 15) stokta olmayan ürünler fiyat aralığına ve ürün sayısına dahildir.
- **Kampanya etiketleri:** vitra.com.tr'de taranan 771 kategori kartının 693'ünde (%89,9) "Sepette %N indirim" etiketi bulunmaktadır; oranlar %10 (358 kart), %14 (237) ve %15 (98) düzeyindedir; `/c-kampanyali-urunler` 413 varyantla listelenmekte ve ilk 240 kartta %14 (122), %10 (77), %15 (38) görülmektedir. İncelenen kartlarda sayfa veri katmanındaki `unit_sale_price` değeri liste fiyatına eşittir; sepet fiyatı yalnızca kart metninde yer almaktadır. Ücretsiz Montaj etiketi lavabo dolapları (27), aynalı banyo dolabı (15), temassız lavabo bataryası (12), boy dolabı (10) ve sabunluk (8) ağırlıklıdır.
- **Rakip özel markaları ve indirim yapısı:** Koçtaş'ta "Koçtaş Basic" markası sabunluk kesitinde 7 ürün ve %72 yorum payıyla görülmektedir; Bauhaus sonuçlarında Primanova 68 satırla (5 kesit; sabunluk aramasında 24 ürünün 24'ü) öne çıkmaktadır (mağaza özel markası olup olmadığı doğrulanmamıştır). Creavit e-mağazası tek marka olarak tüm listelenen ürünleri liste fiyatının yaklaşık %40 altında göstermektedir. Trendyol'da markasız ("Genel Markalar") pay duş kolonunda %21,9, küvet bataryasında %20,0, bide bataryasında %18,2 ile en yüksek düzeydedir.
- **Pazaryerinde VitrA'yı kim satıyor:** Trendyol'da VitrA resmi mağazası %35, Hepsiburada'da VitrA mağazası %12 ve Hepsiburada platformu %11 paya sahiptir; kalan satırlar 3P satıcılara aittir (Trendyol 37, Hepsiburada 69 farklı satıcı). Trendyol'da "VitrA ATEŞ İNŞAAT" gibi mağaza adında marka geçen bayi tipi satıcılar da bulunmaktadır.
- **Tekrar eden satıcılar:** Trendyol'da yapibu (33 satır, 8 kesit), New Banyostyle (20), Zabata Türkiye (18), MEDAS E-TİCARET (16), ZuuBaby (16), EnarHome (16, 6 kesit), Hace Yapı Malzemeleri (15). Hepsiburada'da Hepsiburada platformu (110 satır, 24 kesit), EMEK YAPI MARKET (41), YAPIBU (31), Banyostyle (21), BanyoVit Ulumak Yapı Market (20), yapikurdu (20). Trendyol satıcı kimliklerinin 613'ü (1.759 satır içinde) çözümlenememiş ve `no:` önekiyle bırakılmıştır.
- **Kategori adlandırma farkları:** vitra.com.tr "Duvardan banyo bataryaları" ile pazaryerinde "sıva üstü banyo bataryası", "Tuvalet taşı" ürün adı "Helataşı" ile "alaturka tuvalet taşı", "Temassız lavabo bataryası" ile "fotoselli batarya" (Trendyol 994, Hepsiburada 588 sonuç), "Standart lavabo ve ayakları" ile "ayaklı lavabo" (Trendyol aramasında 36 üründen yalnızca 2'si eşleşmiştir), "Hidromasajlı küvet" ile Hepsiburada'nın "Jakuzi" kategorisi, "Duş kolonu" ile Trendyol'un "Duş Sistemi" ve Hepsiburada'nın "Duş Seti" kategorileri farklı adlarla anılmaktadır. Rezervuar kumanda paneli Trendyol'da "Rezervuar" web kategorisinde, Hepsiburada'da "Kumanda Paneli" ürün çeşidinde listelenmektedir.
- **Ürün sayfası ve site eksikleri:** `/c-online-ozel` sayfası yönlendirme döngüsüne girmektedir (ERR_TOO_MANY_REDIRECTS) ve sitemap'te listelenmektedir. Çocuk klozet, engelli klozet, köşe lavabo ve lavabo ayağı için ayrı kategori sayfası yoktur. 13 alt kategori sayfasında tüm ürünler "Gelince Haber Ver" durumundadır. "Sepette %N indirim" fiyatı sayfa veri katmanına yansımadığından fiyat karşılaştırma sitelerinin ve pazaryeri akışlarının okuyacağı fiyat liste fiyatıdır.
- **Rakip mağaza fiyat konumu:** Banyomega ve Banyomarka fiyat düzeyi diğer mağazalardan belirgin biçimde yüksektir (çanak lavabo medyanı Banyomega 15.340 TL, Banyomarka 13.595, Creavit e-mağaza 7.686, Koçtaş 5.315, Banyoline 3.293); Banyomarka'da monoblok lavabo medyanı 60.025 TL ve hidromasajlı küvet medyanı 254.250 TL ile yüksek fiyat bandındadır.

## 7. Kısıtlar

- **Cimri:** 60 saniye arayla iki denemede de 429 yanıtı alındığından site bırakılmıştır. 5 kesit hiç okunmamıştır (banyo askısı, banyo çöp kovası, havluluk, pisuvar ara bölmesi, pisuvar yıkama sistemi). Arama sayfası kart düzeni farklı olan 12 kesitte (tuvalet taşı, armatür tamamlayıcı, mekanik ve temassız kumanda paneli, hidromasajlı küvet, bağımsız küvet, küvet paneli, duş teknesi paneli, banyo konsolu, banyo set modülü, malzemelik, dolap ayağı) yalnızca toplam alınmış, ürün satırı okunamamıştır.
- **vitra.com.tr:** `/c-online-ozel` sayfası yönlendirme döngüsü nedeniyle okunamamıştır. 14 kategori sayfasında "Sadece stoklu ürünleri göster" süzgeci sonuç dönmediğinden (sıfır sonuçlu süzgeç yanıt vermemektedir) bu kategorilerde stoklu sayı 0 kabul edilmiş, ilk sayfadaki tüm kartların "Gelince Haber Ver" işaretli olması dayanak alınmıştır. `/c-kampanyali-urunler` için 12 sayfa üst sınırıyla ilk 240 kart okunmuştur. Ürün sayısı renk/varyant kartlarını içerdiğinden model sayısından yüksektir. Fiyat aralığı liste fiyatıdır; "Sepette" fiyatı dahil değildir. Model kodu eşleştirmesi yalnızca okunan 1.100 site kartındaki (771 kategori kartı + özel sayfalar) kodlar için yapılabilmiştir.
- **Arama tabanlı kesitler:** Pazaryerlerinde ve mağazalarda bu alt kategoriler için birebir kategori sayfası çoğunlukla bulunmadığından sonuçlar arama sırasına bağlıdır; arama ifadesi çok kelimeli olduğunda bazı kanallar kelimelerden herhangi birini eşleştirmektedir (ör. Creavit e-mağaza, Trendyol, Hepsiburada toplamları). Eşleşme, ürün adında ya da kategori adında kesit anahtar sözcüğünün geçmesiyle belirlenmiştir; yakın anlamlı adlandırmalar (ör. "helataşı") eşleşme dışında kalabilmektedir. Eşleşen ürün sayısı düşük kesitlerde (5'in altı) medyan ve pay değerleri sınırlı temsil gücü taşımaktadır.
- **Trendyol:** 10 kesitte ikinci bir okuma yapılmış, eşleşme oranı yüksek olan tutulmuştur; yine de monoblok lavabo aramasında Trendyol'da eşleşen ürün bulunamamıştır. Satıcı adları için 85 ürün sayfasından yalnızca mağaza adı okunmuştur; kalan satıcı kimlikleri çözümlenmemiştir.
- **Hepsiburada:** toplam değer 11 kesitte 10.000 üst sınırındadır. Akakçe arama sayfalarında toplam ürün sayısı gösterilmemektedir (kategoriye yönlenen 12 kesit hariç).
- **Rakip mağazalar:** Koçtaş dışında mağazalarda çok satan sıralaması bulunmadığından arama sırası kullanılmıştır. Bauhaus aramaları çok sınırlı ürün döndürmüştür (16 kesitte eşleşen ürün). Banyomarka, Banyomega ve Banyoline'da bazı kesitlerde fiyat gösterilmeyen ürünler medyana dahil edilmemiştir. Banyomarka'da "eski fiyat" alanı tutarsız olabildiğinden indirim oranı yorum gerektirir. Kale fiyat göstermediğinden ve IKEA TR ürün listesi vermediğinden bu turda da kapsam dışıdır.
- **Zaman:** fiyatlar, stoklar ve kampanya etiketleri 30.09.2026 tarama anına aittir.
