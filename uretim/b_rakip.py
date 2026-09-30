# -*- coding: utf-8 -*-
"""Bolum: Rakip gorunurlugu ve kanal olcegi (Ahrefs)."""
from ortak import *
from rapor_parca1 import T
import veri
OR = veri.AHREFS["ahrefs_organik_rakipler_tr"]; BT = veri.AHREFS["ahrefs_batch_tr"]
TIP = {"koctas.com.tr": ("Yapı market", "DIY retailer"), "kale.com.tr": ("Banyo markası", "Bathroom brand"), "banyomarka.com": ("Pure player", "Pure player"), "creavit.com.tr": ("Banyo markası", "Bathroom brand"), "bauhaus.com.tr": ("Yapı market", "DIY retailer"),
       "yerevdekor.com": ("Pure player", "Pure player"), "yurtbayseramik.com": ("Seramik markası", "Tile brand"), "turkmenleryapi.com.tr": ("Pure player", "Pure player"), "egeseramikshop.com": ("Seramik markası", "Tile brand"), "yapilir.com": ("Pure player", "Pure player"),
       "banyomoda.com": ("Pure player", "Pure player"), "banyomoda.com.tr": ("Pure player", "Pure player"), "ngkutahyaseramik.com.tr": ("Seramik markası", "Tile brand"), "balneom.com": ("Pure player", "Pure player"), "yapimanya.com": ("Pure player", "Pure player"), "artema.com.tr": ("Grup markası", "Group brand"),
       "banyoline.com": ("Pure player", "Pure player"), "roca.com.tr": ("Banyo markası", "Bathroom brand"), "egeseramik.com": ("Seramik markası", "Tile brand"), "turkuazseramik.com.tr": ("Seramik markası", "Tile brand"), "vitra.net.tr": ("Grup sitesi", "Group site"),
       "vitra.com.tr": ("Banyo markası (VitrA)", "Bathroom brand (VitrA)"), "tekzen.com.tr": ("Yapı market", "DIY retailer"), "ikea.com.tr": ("Mobilya perakendecisi", "Furniture retailer"), "evidea.com": ("Pure player", "Pure player"), "vivense.com": ("Pure player", "Pure player"),
       "serel.com.tr": ("Banyo markası", "Bathroom brand"), "ecebanyo.com": ("Banyo markası", "Bathroom brand"), "idealstandard.com.tr": ("Banyo markası", "Bathroom brand"), "trendyol.com": ("Pazaryeri", "Marketplace"), "hepsiburada.com": ("Pazaryeri", "Marketplace"),
       "n11.com": ("Pazaryeri", "Marketplace"), "amazon.com.tr": ("Pazaryeri", "Marketplace"), "akakce.com": ("Fiyat karşılaştırma", "Price comparison"), "cimri.com": ("Fiyat karşılaştırma", "Price comparison"), "duravit.com.tr": ("Banyo markası", "Bathroom brand"),
       "geberit.com.tr": ("Banyo markası", "Bathroom brand"), "bien.com.tr": ("Seramik markası", "Tile brand")}
def tip(d): return x(*TIP.get(d, ("Diğer", "Other")))
vit = next(b for b in BT if b[0] == "vitra.com.tr")
rows = []
for d, ortak_, rk, tr_, dr, pay in OR[:15]:
    _b = {b_[0]: b_ for b_ in BT}.get(d)
    rows.append([u("https://www." + d, d), tip(d), cell(ortak_), n(yzd(100 * ortak_ / vit[2])), cell(rk), cellk(_b[4] if _b else tr_), cell(_b[1] if _b else dr)])
tbl = tablo([th("Alan adı", "Domain", "vitra.com.tr ile aynı kelimelerde sıralanan alan adı; Ahrefs organik rakipler raporu, Türkiye.", "Domain ranking for the same keywords as vitra.com.tr; Ahrefs organic competitors report, Turkey."),
             th("Tip", "Type", "Sitenin iş modeli.", "The site's business model."),
             th("Ortak kelime", "Common keywords", "İki sitenin birlikte sıralandığı kelime sayısı.", "Number of keywords both sites rank for.", True),
             th("VitrA kelimelerine oranı", "Share of VitrA keywords", "Ortak kelime / vitra.com.tr'nin toplam sıralanan kelimesi (%s)." % bin(vit[2]), "Common keywords / vitra.com.tr's total ranking keywords (%s)." % f"{vit[2]:,}", True),
             th("Yalnız rakibin kelimesi", "Competitor-only keywords", "Rakibin sıralandığı, vitra.com.tr'nin sıralanmadığı kelime sayısı (Ahrefs organik rakipler raporu).", "Keywords the competitor ranks for and vitra.com.tr does not (Ahrefs organic competitors report).", True),
             th("Organik trafik", "Organic traffic", "Ahrefs tahmini aylık organik ziyaret (Batch Analysis, alttaki kanal tablosuyla aynı kaynak).", "Ahrefs estimated monthly organic visits (Batch Analysis, same source as the channel table below).", True),
             th("DR", "DR", "Domain Rating, 0-100.", "Domain Rating, 0-100.", True)], rows, "uzun")
SIRA = ["trendyol.com", "hepsiburada.com", "akakce.com", "amazon.com.tr", "ikea.com.tr", "koctas.com.tr", "n11.com", "vivense.com", "vitra.com.tr", "bauhaus.com.tr", "kale.com.tr", "evidea.com", "creavit.com.tr", "tekzen.com.tr", "artema.com.tr", "roca.com.tr", "duravit.com.tr", "geberit.com.tr", "bien.com.tr", "serel.com.tr", "ecebanyo.com", "idealstandard.com.tr"]
bt = {b[0]: b for b in BT}
rows2 = []
for d in sorted([d_ for d_ in SIRA if d_ in bt], key=lambda d_: -bt[d_][4]):
    if d not in bt: continue
    b = bt[d]
    rows2.append([u("https://www." + d, d), tip(d), cell(b[1]), cellk(b[2]), cellk(b[3]), cellk(b[4]), cellk(b[5]), cellk(b[6])])
tbl2 = tablo([th("Alan adı", "Domain", "Ahrefs Batch Analysis, Türkiye, alt alan adları dahil.", "Ahrefs Batch Analysis, Turkey, subdomains included."),
              th("Tip", "Type", "Sitenin iş modeli.", "The site's business model."),
              th("DR", "DR", "Domain Rating.", "Domain Rating.", True),
              th("Organik kelime", "Organic keywords", "Türkiye'de sıralanan kelime sayısı.", "Number of ranking keywords in Turkey.", True),
              th("İlk 3", "Top 3", "İlk üç sırada yer alan kelime sayısı.", "Number of keywords ranking in the top three.", True),
              th("Organik trafik", "Organic traffic", "Tahmini aylık organik ziyaret.", "Estimated monthly organic visits.", True),
              th("Paid trafik", "Paid traffic", "Tahmini aylık Google Ads ziyareti.", "Estimated monthly Google Ads visits.", True),
              th("Paid kelime", "Paid keywords", "Reklam verilen kelime sayısı.", "Number of advertised keywords.", True)], rows2, "uzun")
az = max(b[4] for b in BT)
marka = [b for b in BT if b[4] > 0 and b[0] in ("vitra.com.tr", "kale.com.tr", "creavit.com.tr", "artema.com.tr", "roca.com.tr", "duravit.com.tr", "geberit.com.tr", "serel.com.tr", "ecebanyo.com", "idealstandard.com.tr", "bien.com.tr")]
RANK = rank_list([(u("https://www." + b[0], b[0]), b[4]) for b in sorted(marka, key=lambda b: -b[4])], max(b[4] for b in marka), you=lambda e: "vitra.com.tr" in e)
koc = bt["koctas.com.tr"]; ik = bt["ikea.com.tr"]; bh = bt["bauhaus.com.tr"]; ty = bt["trendyol.com"]; hb = bt["hepsiburada.com"]
_pp = [r_ for r_ in OR[:15] if TIP.get(r_[0], ("",))[0] == "Pure player"]
_pp_dr = ("%s-%s" % (int(min(r_[4] for r_ in _pp)), int(max(r_[4] for r_ in _pp))),) * 2
_pp_max = max(r_[1] for r_ in _pp)
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
%s
""" % (
 x("Benchmark seti üç halkadan oluşmaktadır: vitra.com.tr ile aynı aramalarda görünen organik rakipler, banyo sektörünün marka siteleri ve ürünün satıldığı pazaryeri ile yapı market kanalları. Ölçüm Ahrefs Türkiye verisiyle yapılmıştır; organik trafik değerleri tahmindir.",
   "The benchmark set consists of three rings: organic competitors that appear in the same searches as vitra.com.tr, the bathroom sector's brand sites, and the marketplace and DIY channels where the product is sold. Measurement uses Ahrefs Turkey data; organic traffic values are estimates."),
 kpi_kart(k(vit[4]), "vitra.com.tr tahmini aylık organik ziyaret · DR %d" % vit[1], "vitra.com.tr estimated monthly organic visits · DR %d" % vit[1]),
 kpi_kart(k(koc[4]), "koctas.com.tr organik ziyareti vitra.com.tr'nin ~%dx'i" % round(koc[4] / vit[4]), "koctas.com.tr organic visits are ~%dx vitra.com.tr's" % round(koc[4] / vit[4])),
 kpi_kart(bin(OR[0][1]), "Koçtaş ile ortak kelime · VitrA kelimelerinin %s" % yzd(100 * OR[0][1] / vit[2]), "Keywords shared with Koçtaş · %s of VitrA keywords" % (yzd(100 * OR[0][1] / vit[2]).replace("%", "") + "%")),
 kpi_kart(k(vit[5]), "vitra.com.tr tahmini aylık paid ziyaret · %d kelime" % vit[6], "vitra.com.tr estimated monthly paid visits · %d keywords" % vit[6]),
 x("Aynı aramalarda görünen siteler", "Sites appearing in the same searches"),
 tbl,
 insight("vitra.com.tr'nin sıralandığı %s kelimenin %s'inde Koçtaş da sıralanmaktadır; ikinci sıradaki Kale'nin ortak kelime sayısı bunun yarısından azdır. Organik rakip listesinde yapı marketler (Koçtaş, Bauhaus), marka siteleri (Kale, Creavit) ve banyo pure player'ları (Banyomarka, Yerevdekor, Banyomoda) birlikte yer almaktadır. Pure player'ların DR değerleri %s bandında ve trafikleri sınırlıdır; buna karşılık VitrA ile ortak kelime sayıları %s'e ulaşmaktadır. Kategori aramalarında VitrA'nın doğrudan rakibi marka siteleri değil, çok markalı perakendecilerdir." % (bin(vit[2]), yzd(100 * OR[0][1] / vit[2]), _pp_dr[0], bin(_pp_max)),
         "Koçtaş also ranks for %s of the %s keywords vitra.com.tr ranks for; Kale in second place shares fewer than half that number. The organic competitor list contains DIY retailers (Koçtaş, Bauhaus), brand sites (Kale, Creavit) and bathroom pure players (Banyomarka, Yerevdekor, Banyomoda) together. The pure players' DR values sit in the %s band and their traffic is limited, yet their common keyword counts with VitrA reach %s. In category searches VitrA's direct competitors are multi-brand retailers, not brand sites." % (yzd(100 * OR[0][1] / vit[2]), bin(vit[2]), _pp_dr[1], "{:,}".format(_pp_max)), "D5"),
 x("Kanal ölçeği: pazaryeri, yapı market, pure player ve marka siteleri", "Channel scale: marketplaces, DIY retailers, pure players and brand sites"),
 tbl2,
 insight("Trendyol (%s) ve Hepsiburada (%s) tahmini aylık organik ziyaretle vitra.com.tr'nin sırasıyla ~%sx ve ~%sx'i ölçeğinde çalışmaktadır; Akakçe (%s) fiyat karşılaştırma tarafında öne çıkmakta, IKEA (%s) ve Koçtaş (%s) mobilya ve yapı market tarafında VitrA'nın ~%sx ve ~%sx'idir. Marka siteleri içinde vitra.com.tr %s organik ziyaretle belirgin biçimde öndedir; Kale %s, Creavit %s ile izlemektedir. Paid tarafta Bauhaus %s ziyaretle organik trafiğini aşan bir reklam yatırımı yapmaktadır; VitrA'nın paid ziyareti %s ile organik trafiğinin %s'i seviyesindedir." % (k(ty[4]), k(hb[4]), "%.0f" % (ty[4] / vit[4]), "%.0f" % (hb[4] / vit[4]), k(bt["akakce.com"][4]), k(ik[4]), k(koc[4]), ("%.0f" % (ik[4] / vit[4])), ("%.0f" % (koc[4] / vit[4])), k(vit[4]), k(bt["kale.com.tr"][4]), k(bt["creavit.com.tr"][4]), k(bh[5]), k(vit[5]), yzd(100 * vit[5] / vit[4])),
         "Trendyol (%s) and Hepsiburada (%s) operate at ~%sx and ~%sx the scale of vitra.com.tr in estimated monthly organic visits; Akakçe (%s) stands out on the price comparison side, and IKEA (%s) and Koçtaş (%s) are ~%sx and ~%sx VitrA on the furniture and DIY side. Among brand sites vitra.com.tr leads clearly with %s organic visits; Kale follows with %s and Creavit with %s. On the paid side Bauhaus makes an advertising investment that exceeds its organic traffic at %s visits; VitrA's paid visits of %s stand at %s of its organic traffic." % (k(ty[4]), k(hb[4]), "%.0f" % (ty[4] / vit[4]), "%.0f" % (hb[4] / vit[4]), k(bt["akakce.com"][4]), k(ik[4]), k(koc[4]), ("%.0f" % (ik[4] / vit[4])), ("%.0f" % (koc[4] / vit[4])), k(vit[4]), k(bt["kale.com.tr"][4]), k(bt["creavit.com.tr"][4]), k(bh[5]), k(vit[5]), yzd(100 * vit[5] / vit[4])), "D5"),
 x("Marka siteleri arasında organik ziyaret", "Organic visits among brand sites"),
 RANK,
 insight("Marka siteleri arasında VitrA'nın organik liderliği, kategori aramalarındaki görünürlüğün kendi kanalına çevrilebilmesi için elverişli bir başlangıç noktasıdır. Buna karşılık kullanıcı, autocomplete önerilerinde görüldüğü gibi (\"vitra klozet fiyatları koçtaş\"), VitrA ürününü yapı marketten almayı da düşünmektedir. VitrA'nın kendi kanalındaki avantajı fiyat üzerinden değil; ürün derinliği, yedek parça, montaj ve garanti bütünlüğü üzerinden kurulabilir.",
         "VitrA's organic leadership among brand sites is a favourable starting point for converting category search visibility into its own channel. At the same time, as seen in the autocomplete suggestions (\"vitra klozet fiyatları koçtaş\"), the user also considers buying the VitrA product from a DIY store. VitrA's own channel can differentiate not on price but on product depth, spare parts, installation and warranty as one offer."),
 kaynak("Ahrefs Site Explorer · organik rakipler ve Batch Analysis · Türkiye · alt alan adları dahil · 27.09.2026", "Ahrefs Site Explorer · organic competitors and Batch Analysis · Turkey · subdomains included · 27.09.2026", "D5"),
)
