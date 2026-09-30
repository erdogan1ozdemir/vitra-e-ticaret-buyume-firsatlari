#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ozet_tablolar.md bolumlerini anlatim metniyle birlestirip pazaryeri_derin/ozet.md uretir.
Once pd_analiz.py ve pd_tablo.py calistirilir."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pd_analiz import BASE

T = open(os.path.join(BASE, 'ozet_tablolar.md'), encoding='utf-8').read()
S = {}
for s in re.split(r'\n(?=## TABLO )', T):
    m = re.match(r'## TABLO (\S+) - ', s)
    if m:
        body = s.split('\n', 1)[1] if '\n' in s else ''
        S[m.group(1)] = body.strip('\n')

# Tablo G: yalnizca hedef kategori satirlari
g_lines = S['G'].split('\n')
head, rows = g_lines[:2], g_lines[2:]
hedef_ad = ['Klozet', 'Asma klozet', 'Klozet takımı', 'Akıllı klozet', 'Klozet kapağı', 'Lavabo', 'Tezgah üstü lavabo', 'Tezgah altı lavabo', 'Çanak lavabo',
            'Lavabo dolabı', 'Banyo dolabı', 'Boy dolabı', 'Aynalı dolap', 'Gömme rezervuar', 'Rezervuar iç takımı', 'Lavabo bataryası', 'Banyo bataryası',
            'Ankastre batarya', 'Duş seti', 'Duş başlığı', 'Duşakabin', 'Küvet', 'Pisuvar']
G = '\n'.join(head + [r for r in rows if r.split('|')[2].strip() in hedef_ad])
G = re.sub(r'\| canak-lavabo \|', '| Çanak lavabo |', G)

MD = f"""# VitrA Türkiye e-ticaret: kategori ve alt kategori taraması (pazaryerleri, fiyat karşılaştırma siteleri, rakip mağazalar)

**Erişim tarihi:** 30.09.2026 · **Kapsam:** Trendyol, Hepsiburada, Akakçe, Cimri; Koçtaş, Bauhaus, Creavit e-mağaza, Banyomarka, Banyomega, Banyoline ve IKEA TR (Kale fiyat göstermediği için kapsam dışıdır) · **Okuma yöntemi:** kullanıcı tarayıcısı üzerinden, yavaş tempoda, girişsiz sayfa okuması

> Yorum ve fiyat verileri tarama anındaki listelere aittir; fiyatlar TL cinsindendir. Tablolardaki "medyan (p25-p75)" ifadesi ilk okunan sayfalardaki ürünlerin fiyat dağılımını gösterir. Kategori toplamı sütunları kanalın kendi gösterdiği ürün sayısıdır.

## 0. Okunan hacim

| Kanal | Kategori kaydı | Okunan ürün satırı | Not |
|---|---|---|---|
| Trendyol | 42 (25 hedef, 17 hedef dışı) | 2.226 | Çok satan sıralaması, ilk 2 sayfa (72 ürün) |
| Hepsiburada | 40 (23 hedef, 17 hedef dışı) | 2.592 | Çok satan sıralaması, ilk 2 sayfa (72 ürün) |
| Akakçe | 42 (21 hedef, 21 hedef dışı) + 8 marka sayfası | 2.568 + 200 | Popülerlik sıralaması, ilk 2 sayfa |
| Cimri | 30 (16 hedef, 14 hedef dışı) | 1.459 | Popülerlik sıralaması, tekrar eden 2. sayfalar ayıklandı |
| Koçtaş | 19 | 914 | Çok satan sıralaması, ilk 48 ürün |
| Bauhaus | 16 | 364 | Varsayılan sıralama, ilk 24 ürün |
| Banyomarka | 20 | 640 | Varsayılan sıralama, ilk 32 ürün |
| Banyoline | 18 | 337 | Varsayılan sıralama, ilk 24 ürün |
| Banyomega | 17 | 303 | Varsayılan sıralama, ilk 18 ürün |
| Creavit e-mağaza | 20 koleksiyon | koleksiyonların tamamı | Koleksiyon toplamı ve fiyat dağılımı |
| IKEA TR | 1 not | - | Ürün listesi alınamadı, Bölüm 5.3'te açıklanmıştır |

Toplam 9.000+ pazaryeri / fiyat karşılaştırma satırı ve 2.500+ rakip mağaza satırı okunmuştur. Ürün düzeyindeki satırlar `urunler.jsonl`, `rakip_magaza_urunler.jsonl` ve `akakce_vitra_urun.jsonl` dosyalarında; kategori düzeyindeki özetler `ty_kategori.jsonl`, `hb_kategori.jsonl`, `akakce_kategori.jsonl`, `cimri_kategori.jsonl` ve `rakip_magaza_kategori.jsonl` dosyalarında bulunmaktadır.

## 1. Kategori x kanal fiyat bandı ve en çok yorumlu ürünler (a)

➔ Klozet ailesinde dört kanalın medyanı 7.500-8.200 TL bandında toplanırken (Trendyol 7.682, Hepsiburada 7.518, Akakçe 7.999, Cimri 8.200), lavabo bataryasında Akakçe ve Cimri medyanı (3.715 ve 3.094) Trendyol medyanının (1.022) 3,0-3,6x düzeyindedir. Trendyol çok satan listelerinde markasız ve düşük fiyatlı armatürlerin yoğunluğu bu farkı açıklamaktadır.

### 1.1 Fiyat bandı (medyan, p25-p75; TL)

{S['A1']}

Kaynak: Trendyol ve Hepsiburada çok satan listeleri, Akakçe ve Cimri popülerlik listeleri | 30.09.2026

### 1.2 Kategori toplamı (kanalın gösterdiği ürün sayısı)

{S['A2']}

Kaynak: ilgili kanalın kategori sayfası | 30.09.2026. Hepsiburada toplamı 10.000 ile sınırlı gösterilmektedir; bu değer "10.000+" olarak okunmalıdır.

➔ Ürün sayısı en yüksek kesitler duşakabin (Akakçe 28.232), duş seti (Trendyol 21.717) ve banyo dolabı (Trendyol 12.244) olmuştur. Buna karşılık pisuvar (96-389), küvet (265-4.693) ve bide (Akakçe 49, Cimri 62, Hepsiburada 1.013) daha dar katalog yapısı sergilemektedir.

### 1.3 En çok yorumlu ürün (Trendyol ve Hepsiburada, ilk 2 sayfa)

{S['B']}

Kaynak: Trendyol ve Hepsiburada çok satan listeleri | 30.09.2026. Aksesuar ve yan ürün karışması nedeniyle ilgili kategoriyle eşleşen ilk ürün alınmıştır; eşleşme bulunmayan kesitler tabloya yazılmamıştır.

➔ Yorum sayısı en yüksek ürünler klozet kapağı (3.456-3.628 yorum), duş seti (7.429), lavabo ve banyo bataryası (2.039-2.702) gibi 150-900 TL bandındaki tamamlayıcı ürünlerde yoğunlaşırken; klozet, duşakabin ve dolap kesitlerinde 1.350-6.500 TL bandındaki ürünler öne çıkmaktadır. Bu durum, çok satan listelerinde yorum hacminin düşük fiyatlı ürünlerde toplandığına işaret etmektedir.

## 2. VitrA/Artema'nın yeri ve kategori boşlukları (b)

### 2.1 Okunan ürünler içinde adet ve en iyi sıra

{S['C']}

`*` işareti, ilk 2 sayfa sonuçlarının yarıdan fazlasının ilgili kategori dışında kalan ürünlerden oluştuğu kesitleri belirtir. Sayılar sıra bilgisi yerine varlık göstergesi olarak okunmalıdır.

Kaynak: Trendyol, Hepsiburada, Akakçe, Cimri | 30.09.2026

### 2.2 Yorum payı (ilk 2 sayfa)

{S['C2']}

Kaynak: Trendyol ve Hepsiburada çok satan listeleri | 30.09.2026. Boş hücreler ilgili kanalda marka bazlı yorum bilgisinin bulunmadığı kesitleri, `*` işareti aksesuar karışımı içeren kesitleri göstermektedir.

### 2.3 Marka filtresinde VitrA/Artema sırası

{S['H2']}

Kaynak: kanalların marka filtresi listeleri (ilk 15 marka) | 30.09.2026. "yok" ilk 15 marka içinde görünmediği anlamına gelir; "-" ilgili kesit için filtre listesinin okunmadığını gösterir.

### 2.4 Değerlendirme

➔ Klozet ailesinde (klozet, asma klozet, klozet takımı, klozet kapağı), rezervuar tarafında (gömme rezervuar, iç takım) ve pisuvarda VitrA/Artema hem ürün adedi hem sıralama açısından belirgin biçimde görünmektedir. Hepsiburada'da klozet kategorisinde 72 ürünün 17'si, iç takım kategorisinde 20'si, gömme rezervuar kategorisinde 18'i VitrA/Artema ürünüdür; yorum payı iç takımda %34,4, gömme rezervuarda %39,7 olmuştur. Akakçe'de gömme rezervuar ve iç takım listelerinde 18'er VitrA ürünü bulunmakta; ilk sıra gömme rezervuarda, ikinci sıra iç takımda VitrA'ya aittir. Artema tarafında ankastre bataryada Hepsiburada'da 36 ürünün 16'sı VitrA/Artema olup yorum payı %70,9, lavabo bataryasında 11 ürün ve %28,0 düzeyindedir.

➔ Lavabo kategorisinde tablo tersine dönmektedir: Trendyol'da 72 ürünün 1'i (sıra 40), Hepsiburada'da 1'i (sıra 61) VitrA'dır; yorum payı Trendyol'da %0,4, Hepsiburada'da %0,0'dır. Aynı kategoride Turkuaz yorumların %62,8'ini (Trendyol) ve %61,5'ini (Hepsiburada) almaktadır. Akakçe'de tezgah altı (Hilton) lavabo listesinde 13 VitrA ürünü, sıra 3'te yer almakta; bu alt kategori VitrA'nın en görünür lavabo tipi olarak okunmaktadır.

➔ Dolap ailesinde (banyo dolabı, lavabo dolabı, boy dolabı, aynalı dolap) pazaryeri listelerinde VitrA görünürlüğü sınırlı kalmıştır: Trendyol banyo dolabı listesinde 1 ürün (sıra 68), Hepsiburada banyo dolabı (aksesuar karışımlı liste) ve boy dolabı listelerinde 0 ürün; Hepsiburada lavabo dolabı (3 ürün, yorum payı %24,0) ve aynalı dolap (3 ürün, yorum payı %23,2) kesitleri istisnadır. Bu kesitlerde yorum hacmi Karen Banyo, Özceden, Roomart, Dmz Home Concept ve Tetto Elagante gibi markalarda toplanmaktadır. Banyomarka'da lavabo dolabı, boy dolabı ve aynalı dolap listelerinin okunan ürünlerinin tamamına yakını VitrA olduğundan, dolap ürün ailesinin pazaryerinde görünürlüğü ile marka mağazası görünürlüğü arasında belirgin fark bulunmaktadır.

**VitrA/Artema ürününün hiç görülmediği kesitler**

- Duşakabin: Trendyol, Hepsiburada, Akakçe, Cimri, Koçtaş, Bauhaus, Banyomega (7 kanalın tamamı). Yorumların Trendyol'da %90,9'u, Hepsiburada'da %95,8'i tek markaya (Durul) aittir.
- Küvet: Trendyol, Hepsiburada, Akakçe, Cimri, Banyomega. Trendyol'da Waterway (%60,9), Hepsiburada'da Aquacan (%39,4) yorum payında öndedir.
- Boy dolabı: Trendyol ve Hepsiburada (Koçtaş'ta 1, Banyomarka'da 31 ürün).
- Bide: Akakçe ve Cimri (Hepsiburada'da 1 ürün, sıra 24).
- Duş seti: Trendyol (Hepsiburada'da 4 ürün, sıra 50 ve sonrası; Akakçe'de 18 ürün, sıra 5).
- Duş teknesi: Cimri; diğer kanallarda 1-2 ürün ve alt sıralarda.
- Alt kategori düzeyinde: Trendyol'da arkadan çıkışlı klozet takımı ve lavabo dolabı kesitleri ile Hepsiburada klozet takımı kesiti aksesuar sonuçlarıyla karıştığı için VitrA varlığı değerlendirilememiştir.

Kaynak: Trendyol, Hepsiburada, Akakçe, Cimri, rakip mağazalar | 30.09.2026

### 2.5 Akakçe VitrA marka sayfaları

Akakçe'de VitrA marka sayfaları: klozet 309, lavabo 297, klozet kapağı 179, banyo dolabı 297, rezervuar 46 ürün göstermektedir; ilk 40 ürünün satıcı sayısı medyanı klozette 3, lavaboda 4, klozet kapağında 4, banyo dolabında 2 ve rezervuarda 1'dir. Satıcı sayısı en yüksek ürünler klozet kapağında VitrA S10 Yavaş Kapanan (47 satıcı, 1.176 TL) ve VitrA 121 003 909 (33 satıcı, 1.427 TL) olmuştur.

➔ Klozet ve lavabo ürünleri 3-4 satıcı ile sınırlı bir fiyat rekabeti gösterirken, klozet kapağında aynı ürün 33-47 satıcıda listelenmekte ve fiyat karşılaştırması belirgin biçimde yoğunlaşmaktadır. Bu bulgu VitrA banyo dolabı ürünlerinde satıcı çeşitliliğinin (medyan 2) düşük kaldığını da göstermektedir.

Kaynak: Akakçe VitrA marka sayfaları | 30.09.2026

## 3. Hedef dışı kategorilerde hacim ve fiyat sinyali (c)

### 3.1 Yorum hacmi, marka yoğunluğu, markasız pay

{S['D']}

"TY yorum" ve "HB yorum", çok satan listelerinin ilk 2 sayfasındaki (72 ürün) toplam yorum sayısıdır; kategori genelindeki satış hacminin değil, listelerin yorum yoğunluğunun göstergesidir. Markasız pay, Trendyol'da "Genel Markalar" olarak listelenen ürünlerin oranını gösterir.

Kaynak: Trendyol, Hepsiburada, Akakçe, Cimri | 30.09.2026

### 3.2 Öne çıkan markalar (ilk 2 sayfada ürün adedine göre ilk 3)

{S['E']}

Kaynak: Trendyol ve Hepsiburada çok satan listeleri | 30.09.2026

### 3.3 Değerlendirme

➔ Yorum hacmi en yüksek hedef dışı kesitler banyo rafı (Trendyol 202.768), boy aynası (132.368), banyo paspası (70.023), banyo aksesuar seti (69.138) ve mutfak bataryası (53.076) olmuştur; ledli ayna (32.062) ve havlupan (24.535) bu kesitleri izlemektedir. Bu kesitlerin medyan fiyatı Trendyol'da 180-1.650 TL bandındadır (ledli ayna 1.009, boy aynası 1.650, banyo aynası 689, havlupan 180); Hepsiburada'da bu değerler 1.331-3.990 TL bandına çıkmaktadır (banyo aynası 1.949, ledli ayna 3.990, boy aynası 1.990, havlupan 1.331).

➔ Marka yoğunluğu ile markasız ürün payı ayrışmaktadır. Aynalar, raflar ve aksesuar setlerinde markasız pay %0-%4 düzeyindedir ancak Trendyol'da 22-46 farklı marka listelenmektedir; hacim tek bir markada toplanmamaktadır. Taharet musluğu, şofben, tutunma barı, sifon ve gider, mutfak bataryası ve ara musluk kesitlerinde ise markasız (Genel Markalar) pay %12,5-%19,4 bandındadır; bu kesitler marka bilinirliğinin görece düşük kaldığı alanlar olarak okunabilir.

➔ Tek marka yoğunlaşması iki kesitte belirgindir: boy aynasında Effe Yapı Dekor (Trendyol 72 ürünün 31'i, Hepsiburada 43'ü), termosifonda Baymak (Trendyol 22, Hepsiburada 25) ve Demirdöküm (14 ve 12). Termosifon ve şofben, su arıtma ile birlikte VitrA'nın mevcut ürün ailesinden uzak kategoriler olarak değerlendirilmektedir.

**VitrA'nın üretip satabileceği tipte kesitler (değerlendirme)**

- Artema bataryası ailesine yakın tamamlayıcı ürünler: ara musluk (Hepsiburada'da Artema 72 ürünün 14'ü ile ilk sırada, Trendyol'da 7), mutfak bataryası (Hepsiburada'da Artema 13 ürün ile ilk sırada), taharet musluğu ve sifon. Hacim ve fiyat medyanı düşük olmakla birlikte (Trendyol ara musluk 385 TL, sifon ve gider 190 TL), mevcut marka görünürlüğü Hepsiburada'da bu kesitlerde hazır bulunmaktadır.
- Banyo mobilyası ailesine yakın ürünler: çamaşır makinesi dolabı (Trendyol 1.688, Hepsiburada 1.654 ürün; medyan 3.281 ve 2.700 TL; Trendyol'da 9.335 yorum), banyo aynası ve ledli ayna (Trendyol medyan 689-1.009 TL, Hepsiburada 1.949-3.990 TL) ve banyo rafı. Bu kesitlerde marka sayısı çok, tek marka payı düşüktür.
- Aksesuar tarafında havlupan (Akakçe 9.767, Cimri 8.011 ürün), banyo aksesuar seti ve tutunma barı hacim ve marka çeşitliliği açısından değerlendirilebilir; havlupan Hepsiburada'da E.C.A. gibi armatür markalarının da listelendiği bir kesittir.
- Şofben, termosifon, su arıtma ve banyo paspası, mevcut VitrA ürün ailesinin dışında kaldığı için üretim ve satış açısından öncelik taşımamaktadır.

## 4. Satıcı yapısı: marka mağazası ve 3P (d)

{S['F']}

Kaynak: Trendyol ve Hepsiburada çok satan listeleri | 30.09.2026. Trendyol'da satıcı adı çözülemeyen mağazalar "no:" öneki ile bırakılmıştır.

➔ Trendyol'da VitrA resmi mağazası, okunan 72'lik listelerde ürünlerin en fazla %4,2'sini (klozet kapağı ve gömme rezervuar) oluşturmaktadır; klozet, lavabo ve banyo dolabında %1,4, duşakabin ve küvette %0'dır. Küçük listelerde (tezgah altı lavabo 4 ürün, bide 5 ürün) yüksek görünen pay örneklem küçüklüğünden kaynaklanmaktadır. Trendyol listelerini tekrar eden 3P satıcılar doldurmaktadır: Hace Yapı Malzemeleri (6 kategori), New Banyostyle (5 kategori, 50 ürün), VİOSA ELITE (5 kategori, 53 ürün), KUSTAR, yapibu, Karen Banyo ve Kurtuluş Teknik.

➔ Hepsiburada'da platformun kendi satışı kategoriden kategoriye belirgin biçimde değişmektedir: lavabo %59,7, tezgah üstü lavabo %52,8, asma klozet %47,2, klozet %45,8; duşakabin, küvet, duş teknesi, banyo dolabı ve boy dolabında %0. Bu kesitlerde satış marka mağazası veya 3P satıcılar üzerinden yürümektedir (örneğin duşakabinde DURUL ve MONAQUA mağazaları). VitrA'nın Hepsiburada mağazası ise iki kategoride, toplam 6 ürünle listelerde görünmektedir.

➔ Marka mağazası yapısı duşakabin (Durul), kuvet (Waterway), banyo dolabı (Roomart, Özceden, Balneom) ve armatür (KUSTAR, VİOSA ELITE, Sardıcı) kesitlerinde net biçimde okunmaktadır: satıcı adı ile marka adı aynı olan mağazalar listenin büyük bölümünü doldurmaktadır. Duş teknesinde ise marka adı ile satıcı ayrıştığı için (ALİKA BANYO, ICON BANYO, HYGGE Banyo) bayi tipi 3P yapısı öne çıkmaktadır.

➔ Akakçe ve Cimri'de satıcı sayısı medyanı, kategorinin fiyat rekabeti yoğunluğuna işaret etmektedir: lavabo bataryası (26) ve banyo bataryası (26,5) yüksek; klozet (3), lavabo (4), banyo dolabı (3) düşük; duş teknesi (1) ve küvet (1) neredeyse tek satıcılı, duşakabin Akakçe'de tek (1), Cimri'de 11 satıcı medyanıyla ayrışmaktadır. Cimri mağaza filtresinde en sık görülen satıcılar Hepsiburada, PttAVM, idefix, Yapıdeko, Amazon, Banyoistanbul, Trendruum ve Bauhaus'tur.

## 5. Rakip perakendeci ve marka mağazaları

### 5.1 Kategori medyanı ve VitrA/Artema yeri

{G}

Kaynak: ilgili mağazanın kategori sayfası | 30.09.2026. "Okunan" sütunu ilk sayfadaki ürün sayısıdır. Marka sütununda Koçtaş ve Bauhaus için "ad:ürün/yorum", diğer mağazalar için "ad:ürün" biçimi kullanılmıştır. Banyomarka toplamları model varyantlarını da içerdiğinden kategori genişliği için üst sınır niteliğindedir. Banyomega ve Banyoline için kategori toplamı sayfada gösterilmemektedir. Koçtaş'ta çok satan, Bauhaus, Banyomarka, Banyoline ve Banyomega'da varsayılan sıralama esas alınmıştır; Creavit e-mağazası koleksiyon toplamlarının tamamını kapsamaktadır ve VitrA/Artema ürünü satmamaktadır.

### 5.2 VitrA/Artema satırlarının kategori medyanına oranı

{S['H']}

Kaynak: ilgili mağazanın kategori sayfası | 30.09.2026. Oran, okunan listedeki VitrA/Artema ürünlerinin fiyat medyanının aynı listedeki tüm ürünlerin medyanına bölümüdür; en az 2 VitrA/Artema fiyatı bulunan kesitler alınmıştır.

➔ VitrA/Artema ürünleri Koçtaş'ta kategori medyanının çoğunlukla üzerinde konumlanmaktadır: klozet 1,66x, lavabo 1,99x, klozet kapağı 1,50x, asma klozet 1,19x, klozet takımı 1,16x, pisuvar 4,35x; batarya, gömme rezervuar ve rezervuar iç takımında 0,88-1,19x aralığındadır. Bauhaus'ta oran 0,86-1,17x bandında kalmakta, VitrA/Artema klozet takımında ve bataryalarda kategori medyanıyla örtüşmektedir. Banyoline'da klozet, tezgah altı lavabo, gömme rezervuar ve batarya kesitlerinde 1,16-2,34x aralığında olan oran (pisuvarda 0,77x), Banyomarka'da 0,34-1,16x bandına düşmektedir; Banyomarka'da VitrA/Artema ağırlıklı listelerde kategori medyanı kısmen VitrA'nın kendi fiyat seviyesini yansıtmaktadır.

### 5.3 Mağaza bazlı notlar

- **Koçtaş:** çok satan sıralamasında ilk 48 ürünün tamamı (banyo dolabında 47'si) Koçtaş satışlıdır. Klozet listesinde Creavit 19, Kale 7, VitrA 4 ürünle yer almakta; yorum hacmi Kale (125) ve Norm (80) ürünlerinde toplanmaktadır. Gömme rezervuar (VitrA 17 ürün), rezervuar iç takımı (VitrA 7 ürün, 73 yorum) ve klozet kapağı (VitrA 7 ürün, 56 yorum) VitrA'nın Koçtaş'ta en görünür kesitleridir. Duşakabinde İskit Duşakabin (16) ve Durul (11), banyo dolabında Karen Banyo (14 ürün, 255 yorum) ve Roomart (8) öne çıkmaktadır; VitrA bu iki kesitte listelerde yer almamaktadır. Norm/NORMO, Housera ve Roomart gibi markalar yalnızca bu mağaza listelerinde belirgin olduğundan Koçtaş'a özgü konumlanma gösteren markalar olarak not edilmiştir; bunların mağaza özel markası olup olmadığı bu taramada doğrulanmamıştır.
- **Bauhaus:** klozet takımında ilk 24 ürünün 8'i VitrA (sıra 2-23), klozet kapağında 6'sı VitrA; lavabo ve duşakabinde VitrA görülmemektedir. Banyo dolabında Fly (13) ve Karen Banyo (9) öne çıkmakta, VitrA Ora 80 cm ürünü 25.990 TL ile kategori medyanının (7.777 TL) yaklaşık 3,3 katında listelenmektedir. Duşakabin ve küvet/duş teknesi listeleri tamamen Er-Duş markasındandır; bataryalarda Artema, Grohe ve E.C.A. yan yana yer almaktadır. Fly, Penta, Adell, Admiral, Poseidon ve Serel markalarının mağaza özel markası olup olmadığı doğrulanmamıştır.
- **Creavit e-mağaza (shop.creavit.com.tr):** tek marka; klozet ailesinde koleksiyon toplamları klozet 85 (çoğu kumanda paneli ve kapak), asma klozet 44, klozet takımı 11, lavabo 90, lavabo dolabı 113, banyo dolabı seti 30, boy dolabı 31, banyo bataryası 30, lavabo bataryası 49 ürün olup tüm ürünler indirimli (liste fiyatının yaklaşık %35-%50 altında) gösterilmektedir. Lavabo medyanı 7.848, asma klozet medyanı 13.894, lavabo dolabı medyanı 16.170 TL'dir. Yorum ve puan bilgisi mağaza listesinde bulunmadığından sıralama varsayılan koleksiyon sırasına göredir.
- **Banyomarka:** VitrA ağırlıklı bir mağaza olarak lavabo dolabı (okunan 32 ürünün 32'si), boy dolabı (31), aynalı dolap (31), tezgah üstü lavabo (19), tezgah altı lavabo (18) ve tek klozet (28) listelerini doldurmaktadır. Klozet takımı ve asma klozette Duravit, akıllı klozette Geberit (14 ürün) VitrA'nın yanında öne çıkmaktadır; batarya kesitlerinde Grohe önde, Artema 3-8 ürünle izlenmektedir.
- **Banyomega:** klozet takımında Creavit (10/18), asma klozette Lena (15/18), lavaboda Duravit (12/18), banyo dolabı ve boy dolabında Aquanil, duş ve batarya kesitlerinde Grohe, Fontana ve Penta öne çıkmaktadır. VitrA klozet kapağında 11, gömme rezervuarda 6 ürünle görünmekte; lavabo, lavabo bataryası, boy dolabı ve duşakabinde görünmemektedir. Fiyat düzeyi diğer mağazalardan belirgin biçimde yüksektir (asma klozet medyanı 32.850 TL).
- **Banyoline:** Turkuaz Seramik lavabo listelerini (24/24) doldururken VitrA klozet (16/24), asma klozet (18/24), klozet kapağı, gömme rezervuar ve pisuvar (3/4) kesitlerinde ve Artema batarya, ankastre duş seti kesitlerinde görünmektedir. Banyo dolabı ve boy dolabı listelerinde yalnızca Orka ve Denko yer almaktadır.
- **IKEA TR:** kategori sayfaları ürün listesi yerine tanıtım içeriği göstermektedir; görünen ürünler banyo duvar dolabı (2.699-3.299 TL), lavabo dolabı (9.000-14.000 TL) ve lavabo bataryası (HAMNSKÄR 5.999 TL) ile sınırlıdır. Klozet, seramik lavabo ve duşakabin kategorisi görülmemiştir. Banyo mobilyası serileri (ANGSJÖN, HAVBÄCK, TÄNNFORSEN, ENHET, HEMNES, NYSJÖN, IVOSJÖN) kategori içinde dolap odaklı bir portföy sunmaktadır.

## 6. Sınırlılıklar (e)

- Trendyol ve Hepsiburada çok satan listelerinde aksesuar ve yan ürün karışması bulunmaktadır (klozet takımı aramasında banyo paspası, dolap aramalarında organizer ürünleri). Karışan kesitler tablolarda `*` ile işaretlenmiş, fiyat bandı temsil gücü sınırlı olan hücrelerde aynı işaret kullanılmıştır. Akakçe ve Cimri kategori yapısı bu açıdan daha temizdir.
- Hepsiburada kategori toplamı 10.000 ile sınırlı gösterilmektedir. Akakçe kategori toplamı sayfanın `numberOfItems` değerinden alınmıştır. Cimri ikinci sayfaları çoğu kategoride ilk sayfayı tekrarladığından ürün kimliğiyle ayıklanmıştır; bu nedenle Cimri'de okunan ürün sayısı kategoriye göre 4-64 aralığında değişmektedir.
- Akakçe ankastre batarya kesitinde tek bir Grohe ürünü 3.492.478 TL olarak listelendiğinden fiyat istatistiğinden çıkarılmıştır.
- Trendyol satıcı adları kısmen çözülebilmiştir (191 satıcı kimliği + 8 mağaza sayfasından eşleştirme). Çözülemeyen satıcılar `no:` önekiyle belirtilmiştir.
- Trendyol ve Hepsiburada yan menü (alt kategori) listeleri ürün sayısı içermemektedir; alt kategori dağılımı sıralı ürün örnekleri üzerinden okunmuştur.
- Koçtaş, Bauhaus, Banyomarka, Banyoline ve Banyomega'da çok satan sıralaması bulunmadığı ya da kullanılamadığı için (Koçtaş dışında) varsayılan sıralamanın ilk sayfası okunmuştur; bu sıralama satış hacmini yansıtmayabilir. Banyomega ve Banyoline için kategori toplamı sayfada gösterilmemektedir; Banyomarka'da model varyantları toplamı şişirmektedir. Banyomarka'da "eski fiyat" alanı tutarsız değerler içerebildiğinden indirim oranı yorumlanmamıştır.
- IKEA TR ürün listesine erişilememiştir (Bölüm 5.3). Kale sitesi fiyat göstermediğinden kapsam dışıdır.
- Koçtaş sifon ve mutfak bataryası kesitleri okunmamıştır.
- Bauhaus'ta yorum ve puan bilgisi az sayıda üründe bulunduğundan yorum payı hesaplanmamıştır.
- Fiyatlar tarama anına aittir; kampanya dönemleri (özellikle Creavit e-mağazasındaki tüm ürünlerin indirimli gösterilmesi) fiyat bandını etkileyebilir.
"""

# Marka yazimi ve simge duzeltmeleri
MD = MD.replace('†', '*')
MD = re.sub(r'\bVitra\b', 'VitrA', MD)
MD = MD.replace('VİTRA', 'VitrA')
assert '—' not in MD and '–' not in MD
open(os.path.join(BASE, 'ozet.md'), 'w', encoding='utf-8').write(MD)
print('ozet.md', len(MD))
