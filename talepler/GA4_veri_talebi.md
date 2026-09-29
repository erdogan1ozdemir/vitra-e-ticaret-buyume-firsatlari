# VitrA e-ticaret büyüme çalışması · GA4 veri talebi

## Genel bilgiler

| Alan | Değer |
|---|---|
| Property | vitra.com.tr (GA4, Web stream) |
| Date range | **1 Sep 2024 - 31 Aug 2026** (R2, R5 ve R10 için yalnızca son 12 ay: 1 Sep 2025 - 31 Aug 2026) |
| Zaman kırılımı | Aylık: dimension olarak `Year month` |
| Para birimi | TRY (currency conversion uygulanmasın) |
| Dosya biçimi | CSV ya da Google Sheets; her talep ayrı dosya, dosya adı talep kodu ile (ör. `R1_item_performance.csv`) |
| Rapor aracı | Aksi belirtilmedikçe **Explore → Free form** |
| Öncelik | **P1:** R1, R2, R3 · **P2:** R4 - R9 · **P3:** R10 - R13 |

Kısaltmalar: *Explore* = GA4 Keşfet ekranı · *Key event* = eski adıyla Conversion.

---

## P1 · İlk teslim

### R1 · Item performance (kategori ve ürün hunisi)
Ürün ve kategori bazında view → cart → checkout → purchase oranları.

| | |
|---|---|
| Report | Explore → Free form |
| Dimensions | `Year month` · `Item ID` · `Item name` · `Item category` · `Item category 2` · `Item category 3` · `Item brand` |
| Metrics | `Items viewed` · `Items added to cart` · `Items checked out` · `Items purchased` · `Item revenue` · `Cart-to-view rate` · `Purchase-to-view rate` |
| Filter | Yok |
| Not | 10.000 satır sınırı aşılırsa dönemi iki yıla bölün (R1a: Sep 2024 - Aug 2025, R1b: Sep 2025 - Aug 2026). `Item category` alanları boş ya da tutarsızsa yine gönderin, ürün listesiyle eşleştirme bizde yapılacak. |

### R2 · Purchase funnel (cihaz ve kategori kırılımı)
Terk noktaları ve mobil / masaüstü farkı.

| | |
|---|---|
| Report | Explore → Funnel exploration · **Open funnel** · Show elapsed time: açık |
| Steps (event name) | 1 `view_item_list` → 2 `view_item` → 3 `add_to_cart` → 4 `begin_checkout` → 5 `add_shipping_info` → 6 `add_payment_info` → 7 `purchase` |
| Breakdown | Çalıştırma A: `Device category` · Çalıştırma B: `Item category` |
| Date range | Son 12 ay |
| Çıktı | Adım başına `Active users`, completion rate, abandonment rate (funnel tablosunun export'u) |

### R3 · Site search
Kullanıcının sitede ne aradığı ve aramanın dönüşüme etkisi.

| | |
|---|---|
| Report | Explore → Free form |
| Tablo A · Dimensions | `Year month` · `Search term` |
| Tablo A · Metrics | `Event count` (event name = `view_search_results`) · `Total users` · `Sessions` |
| Tablo B · Segment karşılaştırması | Segment 1: `view_search_results` olayı olan sessions · Segment 2: olmayan sessions |
| Tablo B · Metrics | `Sessions` · `Session key event rate` (key event = `purchase`) · `Ecommerce purchases` · `Total revenue` |
| Not | Sonuç dönmeyen aramalar ayrıca izleniyorsa (ör. `search_results_count = 0` parametresi ya da ayrı bir event) Tablo C olarak ekleyin. İzlenmiyorsa "izlenmiyor" yazmanız yeterli. |

---

## P2 · İkinci teslim

### R4 · Channel performance

| | |
|---|---|
| Report | Explore → Free form |
| Dimensions | Tablo A: `Year month` · `Session default channel group` · Tablo B: `Year month` · `Session source / medium` |
| Metrics | `Sessions` · `Engaged sessions` · `Engagement rate` · `Total users` · `Key events` (purchase) · `Ecommerce purchases` · `Total revenue` |

### R5 · Landing page performance

| | |
|---|---|
| Report | Explore → Free form |
| Dimensions | `Landing page + query string` · `Session default channel group` |
| Metrics | `Sessions` · `Engagement rate` · `Key events` (purchase) · `Total revenue` |
| Date range | Son 12 ay |
| Kapsam | `Sessions` değerine göre ilk 1.000 satır |

### R6 · Device and region

| | |
|---|---|
| Tablo A | Dimensions: `Year month` · `Device category` → Metrics: `Sessions` · `Ecommerce purchases` · `Total revenue` · `Average purchase revenue` |
| Tablo B | Dimensions: `Region` (son 12 ay) → Metrics: `Sessions` · `Ecommerce purchases` · `Total revenue` · `Average purchase revenue` |
| Kullanım | Bayi yönlendirmesi, montaj ve keşif hizmetinin il bazında kapsamı |

### R7 · New vs returning users, repeat purchase

| | |
|---|---|
| Tablo A | Report: Free form · Dimensions: `Year month` · `New / established` → Metrics: `Sessions` · `Ecommerce purchases` · `Total revenue` |
| Tablo B | Report: Explore → **Cohort exploration** · Cohort inclusion: first `purchase` · Return criteria: `purchase` · Granularity: monthly → cohort tablosunun export'u |
| Tablo B yedeği | Cohort kurulamazsa: Free form · Metrics: `Total purchasers` · `First time purchasers` · `Ecommerce purchases` (aylık) |

### R8 · Payment and shipping parameters

| | |
|---|---|
| Tablo A | Event `add_payment_info` · Dimension: `Payment type` (parametre `payment_type`) · Metric: `Event count` · aylık |
| Tablo B | Event `add_shipping_info` · Dimension: `Shipping tier` (parametre `shipping_tier`) · Metric: `Event count` · aylık |
| Tablo C | Taksit sayısı ayrı bir parametre ya da event ile izleniyorsa: dimension olarak o parametre · Metrics: `Event count` · `Ecommerce purchases` |
| Not | `payment_type` ve `shipping_tier` custom dimension olarak tanımlı değilse Explore'da görünmez. Bu durumda "tanımlı değil" bilgisi yeterli. |

### R9 · Lead and contact events
Satın alma dışındaki talep olayları. Site üzerinde şu akışlar bulunmaktadır: **"Banyomu Yenilemek İstiyorum" (VitrA Banyo Asistanı, 4 adımlı form)**, keşif hizmeti (ETIC_KESIF), montaj hizmetleri (ETIC_MTJ), WhatsApp düğmesi, servis ve satış noktaları sayfası.

| | |
|---|---|
| Report | Explore → Free form |
| Dimensions | `Year month` · `Event name` |
| Metrics | `Event count` · `Total users` |
| İstenen event'ler | Banyo Asistanı: açılış, adım 1-4 tamamlama, form gönderimi (`generate_lead` ya da özel event adı) ve seçilen görüşme kanalı (telefon / mağaza / görüntülü, parametre olarak izleniyorsa) · WhatsApp tıklaması · `tel:` tıklaması · servis ve satış noktası sayfası görüntüleme ve tıklamaları · canlı destek açılışı |
| Not | Event adları bilinmiyorsa **Admin → Data display → Events** ekranının tam export'u yeterli, seçim bizde yapılacak. Banyo Asistanı adımları event olarak izlenmiyorsa ayrıca belirtilmesi önemli. |

---

## P3 · Üçüncü teslim

### R10 · Content to product

| | |
|---|---|
| Tablo A | Dimension: `Page path and screen class` → Metrics: `Views` · `Total users` · `Key events` (purchase) · son 12 ay · ilk 1.000 satır (blog, ilham, koleksiyon sayfaları dahil) |
| Tablo B | Explore → **Path exploration** · Starting point: `/ilham` ve `/blog` altındaki sayfalar · sonraki 3 adım (page path) |

### R11 · Promotions and coupons

| | |
|---|---|
| Dimensions | `Year month` · `Item promotion name` · `Coupon` |
| Metrics | `Items viewed in promotion` · `Items clicked in promotion` · `Ecommerce purchases` · `Total revenue` |

### R12 · Service item attach rate (montaj ve keşif)
Montaj ve keşif hizmetlerinin ürünle birlikte ne sıklıkla satın alındığı.

| | |
|---|---|
| Report | Explore → Free form |
| Dimensions | `Year month` · `Item ID` · `Item name` |
| Filter | `Item ID` başlangıcı `ETIC_` (montaj: `ETIC_MTJ(...)`, keşif: `ETIC_KESIF`) |
| Metrics | `Items added to cart` · `Items purchased` · `Item revenue` |
| Ek | Mümkünse aynı siparişte hizmetle birlikte alınan ürün kategorisi (`Transaction ID` bazında export) |

### R13 · Overview (kontrol tablosu)

| | |
|---|---|
| Dimensions | `Year month` |
| Metrics | `Sessions` · `Total users` · `Ecommerce purchases` · `Total revenue` · `Average purchase revenue` · `Session key event rate` |
| Amaç | Diğer tabloların toplamlarını doğrulamak |

---

## GA4 dışı veri (VitrA ekibinden)

| Kod | Veri | Kapsam |
|---|---|---|
| V1 | Ürün listesi | SKU · ürün adı · kategori ve alt kategori · liste fiyatı · satış kanalları (site, Trendyol, Hepsiburada, bayi) · stok durumu · ürün grubu (SSG, BM vb.) |
| V2 | İade nedenleri | Kategori bazında, son 12 ay |
| V3 | Müşteri hizmetleri konuları | En sık konu başlıkları ve payları |
| V4 | Trendyol ve Hepsiburada mağaza verisi | Ürün / kategori bazında görüntülenme, sepete ekleme, satın alma, iade; müşteri yorumları ve soruları; kargo süreci (önceki mailde istendi) |
| V5 | Banyo Asistanı talepleri | Aylık talep sayısı, seçilen görüşme kanalı, talebin satışa dönüş oranı (CRM tarafında izleniyorsa) |

---

## Teslim kontrol listesi
- [ ] Her dosyada `Year month` kolonu var (R2, R5, R10 hariç)
- [ ] Gelir TRY, currency conversion yok
- [ ] Sampling uyarısı çıkan raporlar dönem bölünerek alındı
- [ ] İzlenmeyen event ya da parametreler için "izlenmiyor" notu eklendi (R3 Tablo C, R8, R9)
- [ ] Dosya adları talep koduyla başlıyor
