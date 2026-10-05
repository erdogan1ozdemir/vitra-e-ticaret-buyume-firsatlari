# -*- coding: utf-8 -*-
"""Karo (KPI ve metrik kartı) açıklama balonları: etiketin başıyla eşlenir; en uzun eşleşen anahtar kullanılır.
Her karo neyi ölçtüğünü, birimini, dönemini ve kaynağını bir iki cümlede söyler. Açıklaması bulunmayan karo kalırsa rapor üretilmez (rapor.py)."""
import re
ACIK = {}


def _sade(t):
    return re.sub(r"<[^>]+>", "", t or "").strip()


def bul(etiket_tr):
    e = _sade(etiket_tr)
    adaylar = [k for k in ACIK if e.startswith(k)]
    return ACIK[max(adaylar, key=len)] if adaylar else None


def _e(anahtar, tr, en):
    ACIK[anahtar] = (tr, en)


# --- Özet, talep, SSG ve BM ---
_e("Kategori arama talebi", "VitrA kategori ağacına eşlenen 2.299 banyo kelimesinin Google'da aylık ortalama aranma sayısının değişimidir. Ocak - Ağustos 2026 ortalaması, 2025'in aynı aylarıyla karşılaştırılmıştır; kaynak Google Ads Keyword Planner.",
   "The change in the average monthly Google searches for the 2,299 bathroom keywords mapped to the VitrA category tree. The January - August 2026 average is compared with the same months of 2025; source: Google Ads Keyword Planner.")
_e("Seramik sağlık gereçleri (SSG) talebi", "Klozet, lavabo, rezervuar ve benzeri seramik sağlık gereci aramalarının (SSG) son 12 aylık toplam hacminin üç yıl önceki 12 aya göre değişimidir (Eyl 2022 - Ağu 2023 ile Eyl 2025 - Ağu 2026). Banyo mobilyası (BM) için aynı hesap ayrıca verilmiştir.",
   "The change in total search volume for sanitaryware such as WCs, washbasins and cisterns (SSG) over the last 12 months compared with the 12 months three years earlier (Sep 2022 - Aug 2023 vs Sep 2025 - Aug 2026). The same calculation for bathroom furniture (BM) is shown alongside.")
_e("SSG talebi", "Seramik sağlık gereci (klozet, lavabo, rezervuar vb.) aramalarının Eyl 2025 - Ağu 2026 toplam hacminin Eyl 2022 - Ağu 2023 toplamına göre yüzde değişimidir; kaynak Google Ads Keyword Planner.",
   "The percentage change in total sanitaryware (WC, washbasin, cistern, etc.) search volume for Sep 2025 - Aug 2026 against Sep 2022 - Aug 2023; source: Google Ads Keyword Planner.")
_e("BM talebi", "Banyo mobilyası (banyo dolabı, lavabo dolabı, ayna, çamaşır makinesi dolabı vb.) aramalarının Eyl 2025 - Ağu 2026 toplam hacminin Eyl 2022 - Ağu 2023 toplamına göre yüzde değişimidir.",
   "The percentage change in total bathroom furniture (bathroom cabinet, washbasin cabinet, mirror, washing machine cabinet, etc.) search volume for Sep 2025 - Aug 2026 against Sep 2022 - Aug 2023.")
_e("Akıllı klozet seti", "Akıllı klozet seti alt türündeki aramaların son 12 aylık ortalama hacminin üç yıl önceki 12 aya göre değişimidir. Taban düşük olduğu için yüzde yüksek görünmektedir; parantez aylık ortalama aramayı gösterir.",
   "The change in the 12-month average search volume for the smart WC set sub-type against the 12 months three years earlier. The percentage looks high because the base is low; the brackets show average monthly searches.")
_e("Aylık iç takım ve yedek parça araması", "Rezervuar iç takımı, şamandıra, kartuş, conta, menteşe gibi yedek parça aramalarının aylık ortalama toplamıdır (Eyl 2025 - Ağu 2026). Google Ads anahtar kelime önerileriyle genişletilen 52.973 kelimelik evrenden hesaplanmıştır; vitra.com.tr'de bu aramaları karşılayan ayrı bir yedek parça kategorisi bulunmamaktadır.",
   "The total average monthly searches for spare parts such as cistern mechanisms, floats, cartridges, seals and hinges (Sep 2025 - Aug 2026). Calculated from the 52,973-keyword universe expanded with Google Ads keyword suggestions; vitra.com.tr has no separate spare-parts category for these searches.")
_e("Banyo mobilyası aramalarında perakendeci adı geçen pay", "Banyo mobilyası aramalarının yüzde kaçında Koçtaş, IKEA, Bauhaus, Trendyol gibi bir perakendeci ya da pazaryeri adı geçtiğini gösterir; VitrA adı geçen aramaların payı ayrıca verilmiştir. Genişletilmiş kelime evreni, Eyl 2025 - Ağu 2026 aylık ortalama hacim.",
   "The share of bathroom furniture searches that include the name of a retailer or marketplace such as Koçtaş, IKEA, Bauhaus or Trendyol; the share naming VitrA is shown alongside. Expanded keyword universe, average monthly volume Sep 2025 - Aug 2026.")
_e("BM aramalarında perakendeci adı geçen pay", "Banyo mobilyası (BM) aramalarının yüzde kaçında bir perakendeci ya da pazaryeri adı geçtiğini gösterir; VitrA adı geçen aramaların payı ayrıca verilmiştir. Genişletilmiş kelime evreni, Eyl 2025 - Ağu 2026.",
   "The share of bathroom furniture (BM) searches that include a retailer or marketplace name; the share naming VitrA is shown alongside. Expanded keyword universe, Sep 2025 - Aug 2026.")
_e("Aylık ortalama arama", "2.299 banyo kelimesinin Ocak - Ağustos 2026 döneminde Google'da aylık ortalama toplam aranma sayısıdır; kaynak Google Ads Keyword Planner, Türkiye, Türkçe.",
   "The average monthly total of Google searches for the 2,299 bathroom keywords in January - August 2026; source: Google Ads Keyword Planner, Türkiye, Turkish.")
_e("Toplam talep değişimi", "2.299 kelimenin Ocak - Ağustos 2026 aylık ortalama aramasının, 2025'in aynı aylarına göre yüzde değişimidir; mevsim etkisini dışarıda tutmak için aynı takvim ayları karşılaştırılmıştır.",
   "The percentage change in average monthly searches for the 2,299 keywords in January - August 2026 compared with the same months of 2025; the same calendar months are compared to exclude seasonality.")
_e("Tasarım ve model aramaları", "\"modelleri\", \"tasarım\", \"dekorasyon\", \"fikir\" gibi ifadeler içeren aramaların Ocak - Ağustos 2026 aylık ortalamasının 2025'in aynı aylarına göre değişimidir; ihtiyaç sınıfları arasında en yüksek artış bu sınıftadır.",
   "The change in the January - August 2026 monthly average of searches containing terms such as \"models\", \"design\", \"decoration\" or \"ideas\" compared with the same months of 2025; this is the fastest-growing need class.")
_e("Banyo Mobilyaları ·", "Banyo Mobilyaları ana kategorisindeki kelimelerin Ocak - Ağustos 2026 aylık ortalama aramasının 2025'in aynı aylarına göre yüzde değişimidir; sekiz ana kategori içinde en büyük daralma bu kategoridedir.",
   "The percentage change in the January - August 2026 average monthly searches for keywords in the Bathroom Furniture main category against the same months of 2025; it is the largest contraction among the eight main categories.")

# --- Organik kanal (Search Console) ---
_e("Organik click değişimi", "Ocak - Eylül 2026 organik click'inin 2025'in aynı aylarına göre yüzde değişimidir; gösterimin değişimi ayrıca verilmiştir. 2025 Ocak - Mayıs Search Console aylık dışa aktarımından, diğer aylar Search Console API'den alınmıştır (sc-domain:vitra.com.tr).",
   "The percentage change in January - September 2026 organic clicks against the same months of 2025; the change in impressions is shown alongside. January - May 2025 come from the Search Console monthly export, other months from the Search Console API (sc-domain:vitra.com.tr).")
# --- Google yapay zeka özellikleri ---
_e("Site gösterimindeki pay", "Google yapay zeka özelliklerindeki gösterimin, aynı günlerde vitra.com.tr'nin web aramasındaki toplam gösterimine oranıdır; Eylül 2026 (1-29) değeri ile Mayıs'ın son iki haftası (18-31 Mayıs) karşılaştırılmıştır (Search Console yapay zeka özellikleri raporu, filtresiz dışa aktarım).",
   "AI feature impressions as a share of vitra.com.tr's total web search impressions on the same days; the September 2026 (1-29) value is compared with the last two weeks of May (18-31 May) (Search Console AI features report, unfiltered export).")
_e("Yapay zeka özelliklerinde gösterim · site geneli", "vitra.com.tr'nin tüm sayfalarının Google'ın yapay zeka özelliklerinde (AI Overview gibi) aldığı toplam gösterimdir (18 May - 29 Eyl 2026, Search Console filtresiz dışa aktarım); blog sayfalarının bu gösterimdeki payı ayrıca verilmiştir.",
   "Total impressions all vitra.com.tr pages received in Google's AI features (such as AI Overview) (18 May - 29 Sep 2026, Search Console unfiltered export); the blog pages' share of these impressions is shown alongside.")
_e("Yapay zeka özelliklerinde gösterim", "vitra.com.tr blog sayfalarının (/ilham-veren-fikirler/) Google'ın yapay zeka özelliklerinde (AI Overview gibi) aldığı toplam gösterimdir; Search Console bu raporu 18 Mayıs 2026'dan itibaren vermektedir (18 May - 29 Eyl 2026).",
   "Total impressions vitra.com.tr blog pages (/ilham-veren-fikirler/) received in Google's AI features (such as AI Overview); Search Console provides this report from 18 May 2026 (18 May - 29 Sep 2026).")
_e("Blog sayfalarının toplam gösterimindeki pay", "Yapay zeka özelliklerindeki gösterimin, aynı günlerde blog sayfalarının web aramasındaki toplam gösterimine oranıdır; site toplam gösterimine oranı ayrıca verilmiştir (18 May - 29 Eyl 2026, Google Search Console).",
   "AI feature impressions as a share of the blog pages' total web search impressions on the same days; the share of total site impressions is shown alongside (18 May - 29 Sep 2026, Google Search Console).")
_e("Yapay zeka payı %20 ve üzeri", "Gösteriminin %20'si ve fazlası yapay zeka özelliklerinde gerçekleşen blog yazılarının (Haz-Eyl 2025'te en az 50 tık almış) 1 Haz - 29 Eyl 2026 tıkının 2025'in aynı günlerine göre değişimidir; ortalama Google sırası iki dönem için ayrıca verilmiştir.",
   "The change in 1 Jun - 29 Sep 2026 clicks against the same days of 2025 for blog articles (with at least 50 clicks in Jun-Sep 2025) where 20% or more of impressions take place in AI features; the average Google position is shown for both periods.")
_e("AI Overview çıkan", "Ahrefs'te blog sayfalarının sıralandığı ve 1 Ekim 2026 Google sonucunda AI Overview çıkan aramalarda blog sayfalarına gelen 1 Haz - 29 Eyl 2026 tıkının 2025'e göre değişimidir; AI Overview çıkmayan aramalardaki değişim ayrıca verilmiştir (Search Console ve Ahrefs).",
   "The change in 1 Jun - 29 Sep 2026 clicks to blog pages against 2025 for searches where blog pages rank in Ahrefs and an AI Overview appeared on the 1 October 2026 Google results page; the change for searches without an AI Overview is shown alongside (Search Console and Ahrefs).")
_e("Organik click", "Google arama sonuçlarından vitra.com.tr'ye gelen toplam click sayısıdır (1 Eki 2025 - 30 Eyl 2026, tüm ülkeler ve cihazlar); toplam gösterim ayrıca verilmiştir. Kaynak Google Search Console, sc-domain:vitra.com.tr.",
   "The total number of clicks from Google search results to vitra.com.tr (1 Oct 2025 - 30 Sep 2026, all countries and devices); total impressions are shown alongside. Source: Google Search Console, sc-domain:vitra.com.tr.")
_e("Ortalama CTR", "Tıklama oranı: vitra.com.tr'nin Google sonuçlarında görüntülendiği her 100 gösterimden kaçının tıkla sonuçlandığını gösterir (tık / gösterim). 1 Eki 2025 - 30 Eyl 2026, Google Search Console.",
   "Click-through rate: how many of every 100 impressions of vitra.com.tr in Google results led to a click (clicks / impressions). 1 Oct 2025 - 30 Sep 2026, Google Search Console.")
_e("Mobil click payı", "Google'dan gelen organik click'lerin yüzde kaçının mobil cihazlardan geldiğini gösterir; gösterimlerde mobil payı ayrıca verilmiştir. Mobilde gösterim payının tık payından yüksek olması, mobilde tıklama oranının daha düşük kaldığını gösterir. 1 Eki 2025 - 30 Eyl 2026, Google Search Console.",
   "The share of organic clicks from Google that come from mobile devices; the mobile share of impressions is shown alongside. A higher mobile share in impressions than in clicks means the click-through rate is lower on mobile. 1 Oct 2025 - 30 Sep 2026, Google Search Console.")
_e("Türkiye payı", "vitra.com.tr'ye Google'dan gelen organik tıkların yüzde kaçının Türkiye'deki kullanıcılardan geldiğini gösterir; ikinci sıradaki ülke ayrıca verilmiştir. 1 Eki 2025 - 30 Eyl 2026, Google Search Console.",
   "The share of organic clicks from Google to vitra.com.tr that come from users in Türkiye; the second country is shown alongside. 1 Oct 2025 - 30 Sep 2026, Google Search Console.")

# --- Marka aramaları (Google otomatik tamamlama) ---
_e("Tamir ve bakım önerileri", "Google arama kutusuna \"vitra\" ile başlayan kök ifadeler yazıldığında çıkan otomatik tamamlama önerilerinin yüzde kaçının tamir, bakım ve yedek parça içerdiğini gösterir (28.09.2026, masaüstü, Türkiye).",
   "The share of Google autocomplete suggestions for seed terms starting with \"vitra\" that relate to repair, maintenance and spare parts (28.09.2026, desktop, Türkiye).")
_e("Fiyat önerileri", "\"vitra\" ile başlayan kök ifadelerin otomatik tamamlama önerilerinde fiyat, indirim, kampanya ve \"ne kadar\" içerenlerin payıdır (28.09.2026). Pay, seçilen kök ifadelere de bağlıdır.",
   "The share of autocomplete suggestions for seed terms starting with \"vitra\" that contain price, discount, campaign or \"how much\" (28.09.2026). The share also depends on the seed terms chosen.")
_e("Montaj önerileri", "\"vitra\" ile başlayan kök ifadelerin otomatik tamamlama önerilerinde montaj, montaj aparatı, montaj ücreti ve taktırma içerenlerin payıdır (28.09.2026).",
   "The share of autocomplete suggestions for seed terms starting with \"vitra\" that contain installation, installation kit, installation fee or having it fitted (28.09.2026).")
_e("Perakendeci adı geçen öneri", "Otomatik tamamlama önerilerinde bir perakendeci ya da pazaryeri adının geçtiği öneri sayısıdır; perakendeci adıyla başlayan kök ifadeler sayıma alınmamıştır (28.09.2026).",
   "The number of autocomplete suggestions that name a retailer or marketplace; seed terms that start with a retailer name are excluded (28.09.2026).")

# --- Google SERP ve AI Overview ---
_e("VitrA gamındaki arama hacminin VitrA'nın ilk 10'da olduğu", "VitrA'nın sattığı ürünlerle ilgili kelimelerin (A grubu) toplam aylık arama hacminin yüzde kaçının, vitra.com.tr'nin Google mobil sonuçlarında ilk 10'da yer aldığı kelimelerden geldiğini gösterir. Sıralar 03-04.10.2026 gözlemidir; hacim Keyword Planner ortalamasıdır.",
   "The share of total monthly search volume for keywords tied to products VitrA sells (group A) that comes from keywords where vitra.com.tr is in Google's mobile top 10. Positions observed on 03-04.10.2026; volume is the Keyword Planner average.")
_e("Trendyol'un ilk 10'da olduğu kelime payı", "VitrA gamındaki kelimelerin yüzde kaçında trendyol.com'un Google mobil sonuçlarında ilk 10'da yer aldığını gösterir; Trendyol'un 1. sırada olduğu kelime sayısı ayrıca verilmiştir (03-04.10.2026).",
   "The share of VitrA-range keywords where trendyol.com is in Google's mobile top 10; the number of keywords where Trendyol ranks first is shown alongside (03-04.10.2026).")
_e("Pazaryeri, yapı market ve fiyat karşılaştırma sitelerinin ilk 3", "VitrA gamındaki kelimelerde Google'ın ilk üç organik sonucunun yüzde kaçını pazaryerleri, yapı marketler ve fiyat karşılaştırma sitelerinin aldığını gösterir; parantezde toplam yuva ve bu sitelerin aldığı yuva sayısı verilmiştir (03-04.10.2026).",
   "The share of Google's top three organic results for VitrA-range keywords taken by marketplaces, DIY retailers and price comparison sites; the brackets show the total slots and those taken by these sites (03-04.10.2026).")
_e("VitrA gamında VitrA'nın kaynak gösterildiği AI Overview", "Google'ın arama sonucunun üstünde gösterdiği yapay zeka özetinde (AI Overview) vitra.com.tr'nin kaynak olarak bağlantı aldığı kelime sayısı / özet çıkan kelime sayısıdır. Yakın kategoriler ile marka ve karşılaştırma gruplarının değerleri ayrıca verilmiştir (04.10.2026).",
   "The number of keywords where vitra.com.tr is linked as a source in Google's AI Overview / the number of keywords that show an overview. Values for adjacent categories and the brand and comparison group are shown alongside (04.10.2026).")
_e("VitrA gamındaki aramalarda VitrA'nın kaynak gösterildiği AI Overview", "Google'ın yapay zeka özetinde (AI Overview) vitra.com.tr'nin kaynak gösterildiği kelime sayısı / özet çıkan kelime sayısıdır; VitrA gamı ve üç grubun toplamı verilmiştir. Bölüm 08'deki Google gözlemi, 04.10.2026.",
   "The number of keywords where vitra.com.tr is cited as a source in Google's AI Overview / the number of keywords that show an overview, for the VitrA range and for all three groups. Google observation in Section 08, 04.10.2026.")

# --- YouTube ---
_e("VitrA Türkiye kanalı", "İlk taramadaki 30 YouTube aramasının ilk sayfa sonuçlarında VitrA Türkiye kanalına ait tekil video sayısıdır; bu videoların toplam izlenmesi ayrıca verilmiştir (29.09.2026).",
   "The number of unique VitrA Türkiye channel videos in the first-page results of the 30 YouTube searches in the first scan; their total views are shown alongside (29.09.2026).")
_e("Tamir aramalarında VitrA", "Dört genel tamir aramasının (\"rezervuar su kaçırıyor\", \"klozet su kaçırıyor\", \"gömme rezervuar tamiri\", \"klozet tıkanıklığı\") YouTube ilk sayfa sonuçlarında VitrA kanalına ait video sayısıdır (29.09.2026).",
   "The number of VitrA channel videos in YouTube first-page results for four general repair searches (\"cistern leaking\", \"WC leaking\", \"concealed cistern repair\", \"WC blockage\") (29.09.2026).")
_e("Tamir aramalarının toplam izlenmesi", "Aynı dört genel tamir aramasının YouTube ilk sayfalarındaki 82 tekil videonun toplam izlenme sayısıdır; bu ilginin hangi kanallara gittiğini gösterir (29.09.2026).",
   "The total views of the 82 unique videos on YouTube's first pages for the same four general repair searches; it shows which channels receive this attention (29.09.2026).")
_e("\"vitra gömme klozet su kaçırıyor\"", "Bu aramada YouTube'da 1. sırada çıkan videonun izlenme sayısıdır; video bir tesisatçı kanalına aittir, VitrA'nın kendi kanalı aynı aramada daha alt sıradadır (29.09.2026).",
   "The view count of the video ranked first on YouTube for this search; it belongs to a plumber's channel, while VitrA's own channel ranks lower for the same search (29.09.2026).")
_e("VitrA Türkiye görünmesi", "Genişletilmiş YouTube taramasında (68 arama, ilk 20 sonuç) VitrA Türkiye kanalının sonuçlarda görünme sayısıdır; kaç aramada ve kaç tekil videoyla göründüğü ayrıca verilmiştir.",
   "The number of times the VitrA Türkiye channel appears in the expanded YouTube scan (68 searches, top 20 results); the number of searches and unique videos is shown alongside.")
_e("Tesisatçı ve usta kanallarının görünme payı", "Genişletilmiş YouTube taramasındaki tüm sonuçların yüzde kaçının tesisatçı ve usta kanallarına ait olduğunu gösterir; taramada görülen tekil kanal sayısı ayrıca verilmiştir.",
   "The share of all results in the expanded YouTube scan that belong to plumber and tradesperson channels; the number of unique channels seen is shown alongside.")
_e("İlham, tadilat ve yeni kategori aramalarında VitrA kanalı", "Banyo ilhamı, tadilat ve yeni kategori niyetli 16 YouTube aramasından kaçında VitrA kanalının ilk 20 sonuçta göründüğünü gösterir.",
   "In how many of 16 YouTube searches with bathroom inspiration, renovation and new-category intent the VitrA channel appears in the top 20 results.")
_e("Başlığında VitrA geçen marka dışı kanal videosu", "Genişletilmiş taramada VitrA dışındaki kanallara ait olup başlığında VitrA adı geçen video sayısıdır; bu videoların toplam izlenmesi ayrıca verilmiştir.",
   "The number of videos from channels other than VitrA whose title names VitrA in the expanded scan; their total views are shown alongside.")

# --- Şikayetvar ---
_e("VitrA şikayeti", "Şikayetvar'da VitrA markasına yazılan şikayet sayısıdır (Eki 2024 - Eyl 2026); aylık ortalama ve en yüksek ay ayrıca verilmiştir.",
   "The number of complaints filed against the VitrA brand on Şikayetvar (Oct 2024 - Sep 2026); the monthly average and the peak month are shown alongside.")
_e("Şikayetvar marka puanı", "Şikayetvar'ın markanın şikayetlere yanıt verme ve çözme performansı ile kullanıcı değerlendirmelerinden hesapladığı 0-100 arası memnuniyet puanıdır; rakip markaların puanları ayrıca verilmiştir (29.09.2026).",
   "The 0-100 satisfaction score Şikayetvar calculates from the brand's complaint response and resolution performance and user ratings; competitors' scores are shown alongside (29.09.2026).")
_e("Servis ve garanti sürecinin geçtiği şikayet payı", "VitrA şikayetlerinin yüzde kaçında servis ya da garanti sürecinin anıldığını gösterir; bir şikayet birden fazla temaya girebildiğinden paylar toplamı 100'ü aşar (Eki 2024 - Eyl 2026).",
   "The share of VitrA complaints that mention the service or warranty process; a complaint can fall into more than one theme, so shares add up to more than 100 (Oct 2024 - Sep 2026).")
_e("Yedek parça temasının payı", "Yedek parça temasına giren şikayetlerin toplam VitrA şikayetleri içindeki payının iki altı aylık dönem arasındaki değişimidir (Eki 2024 - Mar 2025 ile Nis - Eyl 2026).",
   "The change in the share of complaints in the spare-parts theme within all VitrA complaints between two six-month periods (Oct 2024 - Mar 2025 vs Apr - Sep 2026).")

# --- Set ve ürün + hizmet ---
_e("Usta ve tesisatçı aramaları", "Usta, tesisatçı ve montaj hizmeti arayan aramaların aylık ortalama toplamıdır (Eyl 2025 - Ağu 2026); üç yıllık değişim ayrıca verilmiştir. Genişletilmiş kelime evreni, Google Ads Keyword Planner.",
   "The total average monthly searches for tradespeople, plumbers and installation services (Sep 2025 - Aug 2026); the three-year change is shown alongside. Expanded keyword universe, Google Ads Keyword Planner.")
_e("Banyo tasarımı ve planlama", "Banyo tasarımı, planlama ve tasarım programı aramalarının aylık ortalama toplamıdır (Eyl 2025 - Ağu 2026); önceki 12 aya göre değişim ayrıca verilmiştir.",
   "The total average monthly searches for bathroom design, planning and design software (Sep 2025 - Aug 2026); the change against the previous 12 months is shown alongside.")
_e("Banyo tadilatı ve yenileme", "Banyo tadilatı, yenileme ve tadilat fiyatı aramalarının aylık ortalama toplamıdır (Eyl 2025 - Ağu 2026); önceki 12 aya göre değişim ayrıca verilmiştir.",
   "The total average monthly searches for bathroom renovation, refurbishment and renovation prices (Sep 2025 - Aug 2026); the change against the previous 12 months is shown alongside.")
_e("Banyo seti ve takımı", "\"banyo seti\" ve \"banyo takımı\" içeren aramaların aylık ortalama toplamıdır (Eyl 2025 - Ağu 2026). Bu aramaların önemli kısmı tekstil ve aksesuar seti anlamındadır; komple banyo talebi olarak okunmamalıdır.",
   "The total average monthly searches containing \"banyo seti\" and \"banyo takımı\" (Sep 2025 - Aug 2026). A large part of these searches means textile and accessory sets and should not be read as complete-bathroom demand.")

# --- Rakip görünürlüğü ve ölçek ---
_e("vitra.com.tr tahmini aylık organik ziyaret", "Ahrefs'in, sitenin Google sıralamaları, kelime hacimleri ve tahmini tıklama oranından hesapladığı aylık organik ziyaret tahminidir (Türkiye, 27-28.09.2026). DR (Domain Rating), sitenin bağlantı profilinin gücünü 0-100 arasında gösteren Ahrefs puanıdır.",
   "Ahrefs' estimate of monthly organic visits, calculated from the site's Google rankings, keyword volumes and estimated click-through rates (Türkiye, 27-28.09.2026). DR (Domain Rating) is Ahrefs' 0-100 score for the strength of the site's link profile.")
_e("koctas.com.tr organik ziyareti", "Ahrefs'in tahmini aylık organik ziyaret değerine göre koctas.com.tr'nin vitra.com.tr'ye oranıdır (Türkiye, 27-28.09.2026); Koçtaş'ın tüm kategorilerini kapsar.",
   "The ratio of koctas.com.tr to vitra.com.tr by Ahrefs' estimated monthly organic visits (Türkiye, 27-28.09.2026); it covers all of Koçtaş's categories.")
_e("Koçtaş ile ortak kelime", "vitra.com.tr'nin Google'da sıralandığı kelimelerden Koçtaş'ın da sıralandığı kelime sayısıdır; VitrA kelimelerinin içindeki payı ayrıca verilmiştir (Ahrefs, 27-28.09.2026).",
   "The number of keywords where both vitra.com.tr and Koçtaş rank on Google; its share of VitrA's keywords is shown alongside (Ahrefs, 27-28.09.2026).")
_e("vitra.com.tr tahmini aylık paid ziyaret", "Ahrefs'in, Google reklamlarında görülen kelimelerden hesapladığı aylık ücretli arama ziyareti tahminidir; reklam görülen kelime sayısı ayrıca verilmiştir (27-28.09.2026). Gerçek reklam harcaması ya da tık verisi değildir.",
   "Ahrefs' estimate of monthly paid search visits, calculated from keywords where Google ads were seen; the number of such keywords is shown alongside (27-28.09.2026). It is not actual ad spend or click data.")
_e("vitra.com.tr aylık ortalama ziyaret", "Similarweb'in herkese açık site sayfasındaki tahmini aylık ziyaret sayısıdır; Haziran - Ağustos 2026 ortalaması, tüm ülkeler ve cihazlar.",
   "Similarweb's estimated monthly visits from its public site page; June - August 2026 average, all countries and devices.")
_e("Organik arama payı", "Similarweb'e göre vitra.com.tr ziyaretlerinin yüzde kaçının organik aramadan geldiğini gösterir; doğrudan (Direct) ziyaret payı ayrıca verilmiştir (Haz - Ağu 2026).",
   "The share of vitra.com.tr visits coming from organic search according to Similarweb; the direct visit share is shown alongside (Jun - Aug 2026).")
_e("Ücretli arama payı", "Similarweb'e göre vitra.com.tr ziyaretlerinin yüzde kaçının ücretli aramadan (Google reklamları) geldiğini gösterir; rakip marka sitelerinin değerleri ayrıca verilmiştir (Haz - Ağu 2026).",
   "The share of vitra.com.tr visits coming from paid search (Google ads) according to Similarweb; competitor brand sites' values are shown alongside (Jun - Aug 2026).")
_e("Sosyal medya payı", "Similarweb'e göre vitra.com.tr ziyaretlerinin yüzde kaçının sosyal medyadan geldiğini gösterir; rakip sitelerin değerleri ayrıca verilmiştir (Haz - Ağu 2026).",
   "The share of vitra.com.tr visits coming from social media according to Similarweb; competitor sites' values are shown alongside (Jun - Aug 2026).")

# --- Marka sitelerinde trafik ---
_e("vitra.com.tr tahmini aylık organik trafik", "Ahrefs'in Google sıralamalarından hesapladığı aylık organik ziyaret tahminidir; Türkiye'deki banyo ve seramik marka siteleri arasında en yüksek değerdir (27-28.09.2026).",
   "Ahrefs' estimate of monthly organic visits calculated from Google rankings; it is the highest among bathroom and ceramics brand sites in Türkiye (27-28.09.2026).")
_e("Klozet temasında VitrA'nın organik trafiği", "Klozet temalı sayfalara gelen Ahrefs tahmini organik trafikte vitra.com.tr'nin en yakın marka sitesine (Creavit) oranıdır (27-28.09.2026).",
   "The ratio of vitra.com.tr to the closest brand site (Creavit) in Ahrefs' estimated organic traffic to WC-themed pages (27-28.09.2026).")
_e("Karo temasında Kale'nin organik trafiği", "Karo temalı sayfalara gelen Ahrefs tahmini organik trafikte kale.com.tr'nin vitra.com.tr'ye oranıdır (27-28.09.2026).",
   "The ratio of kale.com.tr to vitra.com.tr in Ahrefs' estimated organic traffic to tile-themed pages (27-28.09.2026).")
_e("Banyomarka'nın en yüksek trafikli 90 sayfasında", "Banyomarka.com'un Ahrefs'e göre en çok organik trafik alan 90 sayfasının toplam trafiği içinde VitrA ve Artema ürün sayfalarının payıdır; parantezde tahmini aylık ziyaret verilmiştir (27-28.09.2026).",
   "The share of VitrA and Artema product pages in the total traffic of banyomarka.com's 90 highest-traffic pages according to Ahrefs; the brackets show estimated monthly visits (27-28.09.2026).")

# --- Pazaryeri ve çok satanlar ---
_e("Trendyol banyo kategorilerinin aylık organik trafiği", "Ahrefs'in trendyol.com'un banyo kategori sayfalarına Google'dan gelen aylık organik ziyaret tahminidir; yalnızca izlenen kategori sayfalarını kapsadığı için alt sınır olarak okunmalıdır (27-28.09.2026).",
   "Ahrefs' estimate of monthly organic visits from Google to trendyol.com's bathroom category pages; it only covers the tracked category pages and should be read as a lower bound (27-28.09.2026).")
_e("VitrA'nın Trendyol klozet kategorisindeki listeleme payı", "Trendyol klozet kategorisindeki toplam ürün listelemesinin yüzde kaçının VitrA ürünü olduğunu gösterir; lavabo ve banyo dolabı payları ayrıca verilmiştir (29.09.2026).",
   "The share of all product listings in Trendyol's WC category that are VitrA products; washbasin and bathroom cabinet shares are shown alongside (29.09.2026).")
_e("Hepsiburada'da VitrA ürünlerinde buybox", "Buybox, bir ürün sayfasında \"sepete ekle\" düğmesini kazanan satıcıdır. Hepsiburada'daki 210 VitrA ürününün yüzde kaçında bu düğmenin üçüncü taraf bir satıcıda olduğunu gösterir (29.09.2026).",
   "The buybox is the seller that wins the \"add to basket\" button on a product page. It shows for what share of 210 VitrA products on Hepsiburada this button belongs to a third-party seller (29.09.2026).")
_e("Pazaryerindeki VitrA ürünlerinin medyan fiyatının", "Trendyol ve Hepsiburada'da VitrA ürünlerinin medyan fiyatının, aynı kategorinin çok satan ilk sayfasındaki ürünlerin medyan fiyatına oranıdır; 2x, VitrA ürünlerinin tipik olarak iki kat pahalı olduğunu gösterir (29.09.2026).",
   "The ratio of the median price of VitrA products on Trendyol and Hepsiburada to the median price of the category's first best-seller page; 2x means VitrA products are typically twice as expensive (29.09.2026).")

# --- Alt kategori derinliği ---
_e("Duşakabin çok satan listelerinde VitrA ürünü bulunan kanal", "Duşakabin çok satan listesinin incelendiği yedi kanaldan (pazaryeri, fiyat karşılaştırma ve yapı market siteleri) kaçında VitrA ürünü bulunduğunu gösterir; küvet için değer ve Trendyol'da yorumların marka dağılımı ayrıca verilmiştir (30.09.2026).",
   "In how many of the seven channels where the shower enclosure best-seller list was reviewed (marketplace, price comparison and DIY retail sites) a VitrA product appears; the value for bathtubs and the brand split of Trendyol reviews are shown alongside (30.09.2026).")
_e("Hepsiburada gömme rezervuar çok satanlarında VitrA yorum payı", "Hepsiburada gömme rezervuar çok satan listesindeki ürünlerin toplam yorum sayısının yüzde kaçının VitrA ürünlerine ait olduğunu gösterir; yorum sayısı satış hacmine yakın bir gösterge olarak kullanılmıştır (30.09.2026).",
   "The share of total review counts for products in Hepsiburada's concealed cistern best-seller list that belongs to VitrA products; review count is used as a proxy for sales volume (30.09.2026).")
_e("Trendyol lavabo çok satanlarında VitrA yorum payı", "Trendyol lavabo çok satan listesindeki ürünlerin toplam yorum sayısının yüzde kaçının VitrA ürünlerine ait olduğunu gösterir; listedeki VitrA ürün sayısı ve sırası ayrıca verilmiştir (30.09.2026).",
   "The share of total review counts for products in Trendyol's washbasin best-seller list that belongs to VitrA products; the number and rank of VitrA products in the list are shown alongside (30.09.2026).")
_e("Trendyol banyo rafı ilk 72 ürünün toplam değerlendirmesi", "VitrA'nın hedef gamı dışında kalan banyo rafı kesitinde Trendyol çok satan ilk 72 ürünün toplam değerlendirme sayısıdır; kategorinin talebini gösteren bir ölçek olarak kullanılmıştır. Medyan fiyat ve diğer kesitlerin değerleri ayrıca verilmiştir (30.09.2026).",
   "The total review count of the top 72 Trendyol best-sellers in the bathroom shelf segment, which is outside VitrA's target range; it is used as a scale of category demand. The median price and other segments' values are shown alongside (30.09.2026).")
_e("vitra.com.tr'de incelenen 55 alt kategori sayfası", "vitra.com.tr'de incelenen 55 alt kategori sayfasındaki ürün varyant kartlarının yüzde kaçının \"stoktakiler\" süzgecinin dışında kaldığını, yani o an satın alınamadığını gösterir (30.09.2026).",
   "The share of product variant cards on the 55 subcategory pages reviewed on vitra.com.tr that fall outside the \"in stock\" filter, i.e. could not be bought at that moment (30.09.2026).")
_e("Stoklu ürün bulunmayan alt kategori sayfası", "vitra.com.tr'de \"stoktakiler\" süzgeci uygulandığında hiç ürün kalmayan alt kategori sayfası sayısıdır; sayfalardaki toplam kart sayısı parantezde verilmiştir (30.09.2026).",
   "The number of vitra.com.tr subcategory pages with no products left when the \"in stock\" filter is applied; the total card count on these pages is shown in brackets (30.09.2026).")
_e("Aynı model kodunda pazaryeri fiyatının", "Aynı model koduyla hem pazaryerinde hem vitra.com.tr'de satılan ürünlerde, pazaryeri fiyatının vitra.com.tr liste fiyatından yüzde kaç farklı olduğunun medyanıdır; negatif değer pazaryerinin daha ucuz olduğunu gösterir. Sepet fiyatına göre fark ayrıca verilmiştir (30.09.2026).",
   "For products sold under the same model code on both marketplaces and vitra.com.tr, the median percentage difference between the marketplace price and the vitra.com.tr list price; a negative value means the marketplace is cheaper. The difference against the basket price is shown alongside (30.09.2026).")
_e("Dört listede (Trendyol, Hepsiburada, Akakçe, Cimri)", "İncelenen 57 alt kesitten kaçında dört kanalın çok satan listelerinde hiç VitrA ya da Artema ürünü görülmediğini gösterir; bunların kaçında vitra.com.tr'de ürün sayfası olduğu ayrıca verilmiştir (30.09.2026).",
   "In how many of the 57 segments reviewed no VitrA or Artema product appears in the best-seller lists of the four channels; how many of them have a product page on vitra.com.tr is shown alongside (30.09.2026).")

# --- Resmi mağaza paneli (Trendyol) ---
_e("2026 Q3 net satış adedi", "VitrA'nın Trendyol resmi mağazasında iptal ve iadeler düşüldükten sonraki satış adedinin, 2025 Q4'e göre kaç kat olduğunu gösterir; parantezde iki çeyreğin adedi verilmiştir. Kaynak VitrA satıcı paneli dışa aktarımı (Q3, 29.09.2026'ya kadar).",
   "How many times the net units sold (after cancellations and returns) in VitrA's official Trendyol store in 2026 Q3 are relative to 2025 Q4; the brackets show both quarters' units. Source: VitrA seller panel export (Q3 up to 29.09.2026).")
_e("Ortalama net satış fiyatı", "Trendyol resmi mağazasında net satış tutarının net satış adedine bölünmesiyle bulunan ürün başına ortalama fiyattır; 2025 Q4 ve 2026 Q3 karşılaştırılmıştır. Düşüş, satışın daha düşük fiyatlı tamamlayıcı ürünlere kaymasından kaynaklanmaktadır.",
   "The average price per item in the official Trendyol store, found by dividing net sales value by net units; 2025 Q4 and 2026 Q3 are compared. The fall comes from sales shifting to lower-priced complementary products.")
_e("Eylül 2026 kategori listelerinde resmi mağazanın", "Trendyol'un kategori bazlı \"Enleri\" listelerinde (her kategoride ilk 50 ürün) VitrA resmi mağazasının hiç ürünle yer almadığı kategori sayısı / incelenen kategori sayısıdır (Eylül 2026).",
   "The number of categories in Trendyol's category \"Top Lists\" (top 50 products per category) where the VitrA official store has no product / the number of categories reviewed (September 2026).")
_e("Ortalama ürün puanı", "Trendyol resmi mağazasındaki VitrA ürünlerine verilen 1-5 yıldızlı değerlendirmelerin ortalamasıdır (son 12 ay); düşük puanlı ürün grupları ayrıca verilmiştir.",
   "The average of 1-5 star ratings given to VitrA products in the official Trendyol store (last 12 months); lower-rated product groups are shown alongside.")

# --- Yorumlar ve soru-cevap ---
_e("VitrA yorumlarında olumsuz pay", "Trendyol ve Hepsiburada'daki VitrA ürün yorumlarının yüzde kaçının olumsuz olduğunu gösterir (1-2 yıldız ya da olumsuz ifade); Artema ve rakip markaların değeri ayrıca verilmiştir.",
   "The share of VitrA product reviews on Trendyol and Hepsiburada that are negative (1-2 stars or negative wording); the values for Artema and competitor brands are shown alongside.")
_e("VitrA ortalama puanı", "Trendyol ve Hepsiburada'daki VitrA ürün yorumlarının 1-5 yıldız ortalamasıdır; Artema'nın ortalaması ve incelenen VitrA yorumu sayısı ayrıca verilmiştir.",
   "The 1-5 star average of VitrA product reviews on Trendyol and Hepsiburada; Artema's average and the number of VitrA reviews examined are shown alongside.")
_e("Banyo dolabında VitrA ve Artema olumsuz payı", "Banyo dolabı yorumlarında VitrA ve Artema ürünlerine yazılan yorumların yüzde kaçının olumsuz olduğunu gösterir; rakip markaların aynı kategorideki değeri ayrıca verilmiştir.",
   "The share of negative reviews among VitrA and Artema bathroom cabinet reviews; competitor brands' value in the same category is shown alongside.")
_e("VitrA sorularında uyumluluk ve kullanım yeri payı", "Trendyol ve Hepsiburada'da VitrA ürünlerine sorulan soruların yüzde kaçının ürünün başka parçalarla uyumu ve hangi yere uygun olduğuyla ilgili olduğunu gösterir.",
   "The share of questions asked about VitrA products on Trendyol and Hepsiburada that concern compatibility with other parts and where the product fits.")

# --- Fiyat ve satıcı manzarası ---
_e("VitrA sitesinin kategori kelimelerindeki Shopping listeleme payı", "Google Shopping'de 27 kategori kelimesi için okunan ilanların yüzde kaçının vitra.com.tr'ye ait olduğunu gösterir; vitra.com.tr'nin kaç kelimede göründüğü ayrıca verilmiştir (29.09.2026, masaüstü).",
   "The share of Google Shopping listings read for 27 category keywords that belong to vitra.com.tr; the number of keywords where vitra.com.tr appears is shown alongside (29.09.2026, desktop).")
_e("Aynı üründe resmi mağaza fiyatının en düşük satıcı fiyatına medyan farkı", "Google Shopping'de aynı ürünü birden çok satıcının sattığı listelerde, resmi mağaza fiyatının en ucuz satıcıya göre yüzde kaç yüksek olduğunun medyanıdır; incelenen liste sayısı ve fark aralığı parantezdedir (29.09.2026).",
   "In Google Shopping listings where several sellers offer the same product, the median percentage by which the official store price exceeds the cheapest seller; the number of lists and the range are in brackets (29.09.2026).")
_e("En ucuz satıcının bağımsız banyo ve yapı mağazası olduğu ürün listesi", "Google Shopping satıcı listelerinden kaçında en ucuz fiyatı bağımsız bir banyo ya da yapı malzemesi mağazasının verdiğini gösterir; Hepsiburada'nın en ucuz olduğu liste sayısı ayrıca verilmiştir (29.09.2026).",
   "In how many Google Shopping seller lists the cheapest price comes from an independent bathroom or building materials store; the number of lists where Hepsiburada is cheapest is shown alongside (29.09.2026).")
_e("Klozet ilanlarında VitrA ve Artema payı", "Google Shopping'de klozet kelimeleri için okunan ilanların yüzde kaçının VitrA ve Artema ürünü olduğunu gösterir; diğer kategorilerin değeri ayrıca verilmiştir (29.09.2026).",
   "The share of Google Shopping listings read for WC keywords that are VitrA and Artema products; other categories' values are shown alongside (29.09.2026).")
_e("En ucuz fiyatın vitra.com.tr dışındaki bir kanalda bulunduğu ürün", "vitra.com.tr, Trendyol, Hepsiburada ve Koçtaş'ta birlikte bulunan 29 üründen kaçında en düşük fiyatın vitra.com.tr dışındaki bir kanalda olduğunu gösterir (29.09.2026).",
   "Of the 29 products found together on vitra.com.tr, Trendyol, Hepsiburada and Koçtaş, in how many the lowest price is on a channel other than vitra.com.tr (29.09.2026).")
_e("Bu ürünlerde vitra.com.tr liste fiyatı ile en ucuz kanal arasındaki fark medyanı", "En ucuz fiyatın başka kanalda bulunduğu ürünlerde vitra.com.tr liste fiyatının en ucuz kanaldan yüzde kaç yüksek olduğunun medyanıdır (29.09.2026).",
   "For products whose lowest price is on another channel, the median percentage by which the vitra.com.tr list price exceeds the cheapest channel (29.09.2026).")
_e("Gözlem anında vitra.com.tr ürün sayfasında stokta olmayan ürün", "Karşılaştırılan 29 üründen kaçının gözlem anında vitra.com.tr ürün sayfasında satın alınamadığını (stok dışı) gösterir (29.09.2026).",
   "Of the 29 products compared, how many could not be bought (out of stock) on their vitra.com.tr product page at the time of observation (29.09.2026).")

# --- Kanal politikaları ---
_e("Google TR mobil sonuçlarında Shopping veya ürün bloğu çıkan kategori kelimesi", "Google Türkiye mobil arama sonuçlarında incelenen 15 kategori kelimesinden kaçında Shopping reklamı ya da ürün bloğu çıktığını gösterir (29.09.2026).",
   "In how many of the 15 category keywords reviewed in Google Türkiye mobile results a Shopping ad or product block appears (29.09.2026).")
_e("vitra.com.tr'de taksit bilgisinin farklı biçimde yer aldığı yüzey", "vitra.com.tr'de taksit bilgisinin birbirinden farklı yazıldığı yüzey sayısıdır; parantezde her yüzeyde gösterilen taksit sayısı verilmiştir (29.09.2026).",
   "The number of places on vitra.com.tr where instalment information is written differently; the brackets show the instalment count on each (29.09.2026).")
_e("Google Maps'te VitrA etiketli satış noktası profili", "Google Maps'te adında ya da kategorisinde VitrA geçen satış noktası ve bayi profili sayısıdır; profillerdeki toplam yorum ve ortalama puan ayrıca verilmiştir (29.09.2026).",
   "The number of shop and dealer profiles on Google Maps with VitrA in their name or category; total reviews and the average rating of these profiles are shown alongside (29.09.2026).")
_e("VitrA Türkiye YouTube abonesi", "VitrA Türkiye YouTube kanalının abone sayısıdır; incelenen rakip marka kanallarının toplam abonesinden yüksektir (29.09.2026).",
   "The subscriber count of the VitrA Türkiye YouTube channel; it is higher than the combined subscribers of the competitor brand channels reviewed (29.09.2026).")

# --- Satın alma yolculuğu ---
_e("Üyeliksiz alışverişte", "vitra.com.tr'de üye olmadan alışverişte, sepetteki \"Sepeti Onayla\" düğmesinden adres girme adımına kadar gereken tıklama sayısıdır; aradaki iki ekran ayrıca belirtilmiştir (04.10.2026, masaüstü).",
   "The number of clicks needed on vitra.com.tr, when shopping without an account, from the basket's \"Confirm Basket\" button to the address step; the two screens in between are noted (04.10.2026, desktop).")
_e("Anlık sonuçlarda bulunup Enter sonrası", "vitra.com.tr site içi aramasında test edilen 38 ifadeden kaçında, yazarken açılan anlık sonuçlarda ilgili ürün bulunurken Enter'a basıldıktan sonraki sonuç sayfasının boş ya da ilgisiz döndüğünü gösterir (04.10.2026).",
   "Of the 38 terms tested in vitra.com.tr's site search, in how many the instant results shown while typing contain a relevant product but the results page after pressing Enter is empty or irrelevant (04.10.2026).")
_e("İki yolda da ilgili ürün ya da destek sayfası dönmeyen arama", "Test edilen 38 ifadeden kaçında ne anlık sonuçlarda ne de sonuç sayfasında ilgili ürün ya da destek sayfasının çıktığını gösterir; parantezde örnek ifadeler verilmiştir (04.10.2026).",
   "Of the 38 terms tested, in how many neither the instant results nor the results page show a relevant product or support page; example terms are in brackets (04.10.2026).")

# --- AI arama ve GEO ---
_e("Rehber içerik tıklarının montaj, tamir ve temizlik yazılarından gelen payı", "vitra.com.tr'nin rehber ve ilham içeriklerine Google'dan gelen tıkların yüzde kaçının montaj, tamir ve temizlik konulu yazılardan geldiğini gösterir; bu yazıların sayfa sayısındaki payı ayrıca verilmiştir (1 Eki 2025 - 30 Eyl 2026, Google Search Console).",
   "The share of Google clicks to vitra.com.tr's guide and inspiration content that comes from installation, repair and cleaning articles; these articles' share of pages is shown alongside (1 Oct 2025 - 30 Sep 2026, Google Search Console).")
_e("Soru sorgularında CTR", "\"nasıl\", \"neden\", \"kaç\" gibi soru biçimindeki aramalarda vitra.com.tr'nin tıklama oranıdır (tık / gösterim); ortalama Google sırası ayrıca verilmiştir (1 Eki 2025 - 30 Eyl 2026, Google Search Console).",
   "vitra.com.tr's click-through rate (clicks / impressions) for question-style searches such as \"how\", \"why\" or \"how much\"; the average Google position is shown alongside (1 Oct 2025 - 30 Sep 2026, Google Search Console).")
_e("Sayfa başlığı ve soru-cevap işaretlemesi eksik destek SSS sayfası", "vitra.com.tr destek bölümündeki 23 SSS sayfasından kaçında sayfa başlığının gerçek içeriği yansıtmadığını ve sorulara soru-cevap işaretlemesinin (FAQPage) eklenmediğini gösterir; işaretleme, arama motorlarına ve yapay zeka sistemlerine sayfadaki soruları tanıtır (04.10.2026).",
   "Of the 23 FAQ pages in vitra.com.tr's support section, how many have a page title that does not reflect the content and no question-answer markup (FAQPage); the markup tells search engines and AI systems which questions the page answers (04.10.2026).")

# --- AI arama ve GEO (yeniden kurgulanan karolar) ---
_e("Yapay zeka yanıt takibi ·", "ChatGPT, Gemini ve Google AI Overview'a düzenli aralıklarla sorulan 125 sorudan marka adı içermeyen 111'ine verilen yanıtlarda VitrA'nın adıyla geçtiği yanıtların payıdır; en düşük oran ChatGPT'de, en yüksek oran Gemini'dedir (4 Eyl - 3 Eki 2026). Soru kullanıcının yapay zekaya yazdığı doğal dildeki uzun sorudur.",
   "The share of answers naming VitrA among the answers to the 111 of 125 questions without a brand name, asked at regular intervals to ChatGPT, Gemini and Google AI Overview; the lowest rate is on ChatGPT and the highest on Gemini (4 Sep - 3 Oct 2026). A question is the long natural-language question a user would type into an AI tool.")
_e("SEOmonitor takibi ·", "vitra.com.tr için SEOmonitor'de günlük takip edilen 2.140 ana kelimeden Google mobil sonucunda AI Overview çıkanlarda, vitra.com.tr'nin kaynak olarak bağlantı aldığı kelimelerin payıdır (03.10.2026).",
   "Among the 2,140 main keywords tracked daily in SEOmonitor for vitra.com.tr, the share of those showing an AI Overview in Google mobile results where vitra.com.tr is linked as a source (03.10.2026).")
_e("Rapor hedef kelimeleri ·", "Bu rapor için seçilen hedef kelimelerin VitrA'nın sattığı ürünlerle ilgili olanlarında (Bölüm 08, A grubu) içeriği alınabilen AI Overview sayısı içinde vitra.com.tr'nin kaynak gösterildiği AI Overview sayısıdır (Google mobil, aynı gün üç gözlem, 04.10.2026).",
   "Among the report's target keywords related to products VitrA sells (Section 08, group A), the number of AI Overviews citing vitra.com.tr out of the AI Overviews whose content could be retrieved (Google mobile, three observations on the same day, 04.10.2026).")
_e("vitra.com.tr destek bölümündeki", "vitra.com.tr'nin destek bölümünde 23 sık sorulan sorular (SSS) sayfası bulunmaktadır. Bunların 4'ünde sayfa başlığı içeriği anlatmayan şablon metin (\"Accelerator Title\") olarak kalmıştır ve sorulara soru-cevap işaretlemesi (FAQPage) eklenmemiştir; bu işaretleme arama motorlarına ve yapay zeka sistemlerine sayfadaki soruları tanıtır. Ayrıca lavabo, banyo mobilyası, yıkanma alanları ve aksesuar için ikişer ayrı SSS sayfası bulunmaktadır (04.10.2026).",
   "vitra.com.tr's support section has 23 frequently asked questions (FAQ) pages. In 4 of them the page title is still template text that does not describe the content (\"Accelerator Title\") and no question-answer markup (FAQPage) has been added; this markup tells search engines and AI systems which questions the page answers. Washbasins, bathroom furniture, bathing areas and accessories also each have two separate FAQ pages (04.10.2026).")

# --- Marka aramaları (Keyword Planner) ---
_e("\"vitra\" + kategori aramaları", "\"vitra\" ile birlikte bir ürün ya da kategori ifadesi içeren aramaların (ör. \"vitra klozet\", \"vitra gömme rezervuar\") Ocak - Ağustos 2026 aylık ortalama toplamıdır; yakın yazım varyantları tek sayılmıştır. Değişim, Ocak - Ağustos 2023 ortalamasına göredir (Google Ads Keyword Planner).",
   "The average monthly total, January - August 2026, of searches containing \"vitra\" together with a product or category phrase (e.g. \"vitra klozet\", \"vitra gömme rezervuar\"); close spelling variants are counted once. The change is against the January - August 2023 average (Google Ads Keyword Planner).")
_e("VitrA'nın 26 üretici marka", "26 üretici markanın marka + kategori aramalarının (Oca-Ağu 2026 aylık ortalama) toplamı içinde VitrA'nın payıdır; rakipler VitrA'da arama hacmi olan aynı kategori ifadeleriyle ve Ahrefs'te sıralandıkları marka ifadeleriyle ölçülmüştür. VitrA grubundaki Artema ile birlikte pay ayrıca verilmiştir.",
   "VitrA's share of the total brand + category searches (January - August 2026 monthly average) of 26 manufacturer brands; competitors are measured with the same category phrases that have search volume for VitrA and with the brand phrases they rank for in Ahrefs. The share together with Artema, part of the VitrA group, is shown alongside.")
_e("VitrA'nın armatür marka aramalarındaki payı", "Armatür kategorisinde (batarya, musluk, taharet musluğu vb.) marka adıyla yapılan aramaların toplamı içinde VitrA'nın payıdır; bu kategoride en çok aranan markalar E.C.A. ve Artema'dır (Oca-Ağu 2026, Google Ads Keyword Planner).",
   "VitrA's share of the total searches made with a brand name in the taps and mixers category (mixers, taps, bidet taps, etc.); the most searched brands in this category are E.C.A. and Artema (Jan - Aug 2026, Google Ads Keyword Planner).")
_e("\"vitra\" yalın marka araması", "Google'da yalnızca \"vitra\" yazılarak yapılan aramaların Ocak - Ağustos 2026 aylık ortalamasıdır; değişim Ocak - Ağustos 2023 ortalamasına göredir (Google Ads Keyword Planner).",
   "The January - August 2026 monthly average of Google searches for \"vitra\" alone; the change is against the January - August 2023 average (Google Ads Keyword Planner).")

# --- GA4 ---
_e("E-ticaret geliri · Oca-Eyl 2026", "vitra.com.tr'nin Ocak - Eylül 2026 toplam e-ticaret geliridir (GA4 Total revenue, TL); değişim 2025'in aynı aylarına göredir. Mağaza her iki dönemde de aynı GA4 mülkünde olduğu için gelir kıyaslanabilir.",
   "vitra.com.tr's total e-commerce revenue for January - September 2026 (GA4 Total revenue, TL); the change is against the same months of 2025. As the shop was in the same GA4 property in both periods, revenue is comparable.")
_e("E-ticaret satın alma · Oca-Eyl 2026", "Ocak - Eylül 2026'da tamamlanan e-ticaret satın alma sayısıdır (GA4 Ecommerce purchases); değişim 2025'in aynı aylarına göredir.",
   "The number of e-commerce purchases completed in January - September 2026 (GA4 Ecommerce purchases); the change is against the same months of 2025.")
_e("Ortalama sipariş tutarı · Oca-Eyl 2026", "Ocak - Eylül 2026 gelirinin satın alma sayısına bölümüdür (TL); 2025 değeri aynı aylardan hesaplanmıştır (GA4).",
   "January - September 2026 revenue divided by the number of purchases (TL); the 2025 value is calculated from the same months (GA4).")
_e("Organik aramanın gelir payı · Oca-Eyl 2026", "GA4'te Organic Search kanalının Ocak - Eylül 2026 toplam e-ticaret gelirindeki payıdır; 2025 değeri aynı aylardan hesaplanmıştır. Aralık 2025'ten itibaren www.vitra.com.tr'ye gelen organik trafik mağazayla aynı sitededir.",
   "The Organic Search channel's share of total e-commerce revenue for January - September 2026 in GA4; the 2025 value is calculated from the same months. From December 2025 the organic traffic to www.vitra.com.tr is on the same site as the shop.")
