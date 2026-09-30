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

{YONTEM}

## 2. Kesit tablosu

Sütun okuma: Trendyol ve Hepsiburada "toplam · medyan (yöntem; eşleşen/okunan)"; Akakçe ve Cimri "toplam · en düşük fiyat medyanı · satıcı sayısı medyanı (yöntem; eşleşen/okunan)". Yöntem: `k+a` web kategorisi + arama, `a` arama, `k` kategoriye yönlenen arama. "VitrA/Artema adet (en iyi sıra)" eşleşen ürünler içindeki adet ve okunan listedeki en üst sıradır. "Yorum payı" eşleşen ürünlerin toplam değerlendirme sayısı içindeki paydır.

{ANA}

Kaynak: Trendyol, Hepsiburada, Akakçe, Cimri arama ve kategori listeleri; vitra.com.tr kategori sayfaları | 30.09.2026

## 3. Rakip mağazalar (eşleşen ürün sayısı · fiyat medyanı · VitrA/Artema adedi)

Hücre biçimi: `eşleşen · medyan · V<adet>`. "-" ilgili mağazanın aramasında eşleşen ürün bulunmadığını gösterir. Koçtaş çok satan sıralamasını, diğer mağazalar arama sırasını yansıtır; Bauhaus ve Banyomega sonuçları kısıtlıdır.

{MAGAZA}

Kaynak: ilgili mağazanın arama sayfası (ilk sonuç sayfası) | 30.09.2026

## 4. vitra.com.tr kategori sayfaları

Ürün sayısı sayfadaki "N sonuç listeleniyor" değeridir ve renk/varyant kartlarını içerir. Fiyat aralığı liste fiyatıdır ("Fiyata Göre Artan/Azalan" sıralamalarının ilk kartları). "Stokta yok" sayfa toplamı ile "Sadece stoklu ürünleri göster" süzgeci toplamı arasındaki farktır; kartlarda bu ürünler "Gelince Haber Ver" düğmesiyle görünür. "Ücretsiz Montaj (liste)" `/c-ucretsiz-montaj` listesinde kategori etiketiyle eşleşen ürün sayısıdır.

{VSITE}

Özel sayfalar:

{OZEL}

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
