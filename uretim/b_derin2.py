# -*- coding: utf-8 -*-
"""Derin bolumu ek: alt kategori tamamlayici tarama (57 kesit) - vitra.com.tr kategori sayfalari, pazaryeri ve fiyat karsilastirma aramalari, rakip magaza aramalari, ayni model kodunda fiyat (D30)."""
from ortak import *
import json, os, re
D2 = os.path.join(veri.V, "ham", "derin", "pazaryeri_derin2")
def L2(f): return [json.loads(l) for l in open(os.path.join(D2, f), encoding="utf-8")]
K2 = L2("kesitler.jsonl"); VS = L2("vitra_site_kategori.jsonl")
FE = json.load(open(os.path.join(D2, "fiyat_eslesme.json"), encoding="utf-8"))
ANA = {"Klozet": "WC", "Lavabo": "Washbasin", "Armatür": "Taps", "Duşlar": "Showers", "Rezervuar": "Cisterns", "Yıkanma alanları": "Bathing", "Banyo mobilyası": "Bathroom furniture", "Banyo aksesuarı": "Accessories", "Vitrifiye tamamlayıcı": "Sanitaryware accessories"}
AD2 = {"yerden-tek-klozet": ("Yerden tek klozet (ayaklı)", "Floor-standing one-piece WC"), "asma-klozet-takimi": ("Asma klozet takımı", "Wall-hung WC set"), "tuvalet-tasi-alaturka": ("Tuvalet taşı (alaturka)", "Squat toilet"), "cocuk-klozet": ("Çocuk klozet", "Children's WC"), "engelli-klozet": ("Engelli klozet", "Accessible WC"),
       "canak-lavabo": ("Çanak lavabo", "Bowl washbasins"), "monoblok-lavabo": ("Monoblok lavabo", "Monoblock basin"), "yarim-tezgah-lavabo": ("Yarım tezgah lavabo", "Semi-recessed basin"), "etajerli-lavabo": ("Etajerli lavabo", "Basin with shelf"), "ayakli-lavabo": ("Ayaklı (standart) lavabo", "Pedestal basin"), "kose-lavabo": ("Köşe lavabo", "Corner basin"), "lavabo-ayagi": ("Lavabo ayağı", "Basin pedestal"),
       "bide-bataryasi": ("Bide bataryası", "Bidet tap"), "kuvet-bataryasi": ("Küvet bataryası", "Bath filler tap"), "termostatik-batarya": ("Termostatik batarya", "Thermostatic tap"), "fotoselli-lavabo-bataryasi": ("Temassız (fotoselli) lavabo bataryası", "Touchless basin tap"), "siva-ustu-banyo-bataryasi": ("Duvardan (sıva üstü) banyo bataryası", "Exposed bath tap"),
       "yuksek-canak-lavabo-bataryasi": ("Çanak lavabo bataryası (yüksek)", "Tall bowl-basin tap"), "ankastre-stop-valf": ("Ankastre stop valf", "Concealed stop valve"), "lavabo-sifonu-susuzgeci": ("Lavabo sifon ve süzgeci", "Basin trap and waste"), "armatur-cikis-ucu-dirsek": ("Armatür tamamlayıcı (çıkış ucu, dirsek)", "Tap accessories (outlet, elbow)"),
       "dus-kolonu": ("Duş kolonu", "Shower column"), "el-dusu-takimi": ("El duşu takımı", "Hand shower set"), "surgulu-el-dusu-takimi": ("Sürgülü el duşu takımı", "Sliding-rail hand shower set"), "masajli-dus-sistemi": ("Masajlı duş sistemi", "Massage shower system"), "bataryali-dus-sistemi": ("Bataryalı duş sistemi", "Shower system with mixer"), "ankastre-dus-yonlendirici": ("Ankastre duş yönlendirici", "Concealed diverter"),
       "kumanda-paneli-mekanik": ("Kumanda paneli (mekanik)", "Flush plate (mechanical)"), "kumanda-paneli-temassiz": ("Kumanda paneli (temassız)", "Flush plate (touchless)"), "kumanda-paneli-akilli": ("Kumanda paneli (akıllı)", "Flush plate (smart)"), "tasiyici-aparat": ("Taşıyıcı aparat", "WC frame"), "duvar-onu-rezervuar": ("Duvar önü rezervuar", "Exposed cistern"), "tuvalet-tasi-rezervuari": ("Tuvalet taşı rezervuarı", "Squat toilet cistern"),
       "dus-kanali": ("Duş kanalı", "Shower channel"), "dus-unitesi": ("Duş ünitesi (kompakt kabin)", "Shower unit (compact cabin)"), "hidromasajli-kuvet": ("Hidromasajlı küvet", "Whirlpool bath"), "bagimsiz-kuvet": ("Bağımsız küvet", "Freestanding bath"), "kuvet-paneli": ("Küvet paneli", "Bath panel"), "dus-teknesi-paneli": ("Duş teknesi paneli", "Shower tray panel"), "kaydirmaz": ("Kaydırmaz", "Anti-slip mat"),
       "banyo-tezgahi": ("Banyo tezgahı", "Bathroom countertop"), "banyo-konsolu": ("Banyo konsolu", "Bathroom console"), "banyo-set-modulu": ("Banyo set modülü", "Furniture set module"), "malzemelik": ("Malzemelik", "Storage unit"), "dolap-kulpu": ("Dolap kulpu", "Cabinet handle"), "dolap-ayagi": ("Dolap ayağı", "Cabinet leg"), "makyaj-aynasi": ("Makyaj aynası", "Make-up mirror"), "aynali-dolap": ("Aynalı dolap", "Mirror cabinet"),
       "sabunluk": ("Sabunluk", "Soap dish"), "dis-fircaligi": ("Diş fırçalığı", "Toothbrush holder"), "tuvalet-kagitligi": ("Tuvalet kağıtlığı", "Toilet roll holder"), "tuvalet-fircasi": ("Tuvalet fırçası", "Toilet brush"), "banyo-askisi": ("Banyo askısı", "Robe hook"), "banyo-cop-kovasi": ("Banyo çöp kovası", "Bathroom bin"), "havluluk": ("Havluluk", "Towel rail"),
       "pisuvar-ara-bolmesi": ("Pisuvar ara bölmesi", "Urinal divider"), "pisuvar-yikama-sistemi": ("Pisuvar yıkama sistemi", "Urinal flush system")}
KAN = {"trendyol": "Trendyol", "hepsiburada": "Hepsiburada", "akakce": "Akakçe", "cimri": "Cimri"}
def _m(o):
    f = (o or {}).get("fiyat") or {}; m = f.get("medyan")
    return bin(round(m)) if m else "-"
def pz(o, cap=False):
    """toplam · medyan (Trendyol, Hepsiburada)."""
    if not o or not o.get("okunan"): return n("-")
    t = o.get("total"); ts = "10.000+" if (cap and t == 10000) else (bin(t) if t else "-")
    return n("%s · %s" % (ts, _m(o)))
def fk(o):
    """medyan · satıcı sayısı medyanı (Akakçe, Cimri)."""
    if not o or not o.get("okunan"): return n("-")
    sm = o.get("satici_medyan"); sm = ("%g" % sm).replace(".", ",") if sm is not None else "-"
    return n("%s · %s" % (_m(o), sm))
def va(q, c):
    o = q.get(c)
    return "-" if not o or not o.get("okunan") else str(o.get("vitra_adet") or 0)
def marka1(q):
    for c in ("ty", "hb"):
        o = q.get(c) or {}
        eb = o.get("en_yuksek_yorumlu_marka")   # tum eslesen urunlerden hesaplanan en cok degerlendirilen marka
        top = [eb] if eb and eb.get("yorum") else sorted([m for m in (o.get("marka_top5") or []) if m.get("yorum")], key=lambda m: -m["yorum"])
        if top:
            mk_ = top[0]["marka"]; kn_ = {"ty": "TY", "hb": "HB"}[c]
            if mk_.strip("() ").lower() == "markasız": return x("Markasız · %s (%s)" % (yzd(top[0]["yorum_payi"]), kn_), "Unbranded · %s (%s)" % (yzd(top[0]["yorum_payi"]).replace("%", "").replace(",", ".") + "%", kn_))
            return veri_m("%s · %s (%s)" % (mk_, yzd(top[0]["yorum_payi"]), kn_))
    return n("-")
def site(q):
    v = q.get("vitra_site") or {}
    if not v.get("urun"): return n("-")
    return n("%d / %d · %s - %s" % (v["urun"], v.get("stokta_yok") or 0, bin(v["fiyat_min"]), bin(v["fiyat_max"])))
_ALAKASIZ = {"armatur-cikis-ucu-dirsek": {"marka"}, "ayakli-lavabo": {"ty", "marka"}, "lavabo-ayagi": {"ty", "marka"}, "dus-unitesi": {"akakce", "cimri"},
             "dolap-kulpu": {"cimri"}, "kumanda-paneli-akilli": {"cimri"}, "banyo-tezgahi": {"ty", "marka"}, "bagimsiz-kuvet": {"ty", "marka"}}   # listeye kesitle ilgisiz urun karisan hucreler
def _q(q, c):
    return None if c in _ALAKASIZ.get(q["kesit"], ()) else q.get(c)
def _pz2(o, cap=False):
    if not o or not o.get("okunan"): return [n("-"), n("-")]
    t = o.get("total"); ts = "10.000+" if (cap and t == 10000) else (bin(t) if t else "-")
    return [n(ts), n(_m(o))]
def _fk2(o):
    if not o or not o.get("okunan"): return [n("-"), n("-")]
    sm = o.get("satici_medyan"); sm = ("%g" % sm).replace(".", ",") if sm is not None else "-"
    return [n(_m(o)), n(sm)]
def _site2(q):
    v = q.get("vitra_site") or {}
    if not v.get("urun"): return [n("-"), n("-")]
    return [n("%d / %d" % (v["urun"], v.get("stokta_yok") or 0)), n("%s - %s" % (bin(v["fiyat_min"]), bin(v["fiyat_max"])))]
def _satir5(q):
    a, b = AD2[q["kesit"]]
    return ([x("%s > %s" % (q["ana_kategori"], a), "%s > %s" % (ANA[q["ana_kategori"]], b))] + _site2(q) + _pz2(_q(q, "ty")) + _pz2(q.get("hb"), True) + _fk2(_q(q, "akakce")) + _fk2(_q(q, "cimri")) +
            [n(" / ".join(va(q, c) for c in ("ty", "hb", "akakce", "cimri"))), (n("-") if "marka" in _ALAKASIZ.get(q["kesit"], ()) else marka1(q))])
_B5 = [th("Ana > alt kategori", "Main > sub-category", "VitrA'nın ana kategorisi ve vitra.com.tr'deki alt kategori adı (ör. Armatürler > Sürgülü el duşu takımı). Pazaryerlerinde bu alt kategorinin adıyla arama yapılmıştır.", "VitrA's main category and the sub-category name on vitra.com.tr (e.g. Taps > Sliding hand shower set). Marketplaces were searched with this sub-category name."),
       th("vitra.com.tr ürün / stokta yok", "vitra.com.tr products / out of stock", "vitra.com.tr'de bu alt kategorinin sayfasında listelenen ürün kartı sayısı (her renk ve ölçü ayrı kart sayılır) / bunlardan stokta olmayan, \"Gelince Haber Ver\" düğmesi taşıyan kart sayısı (30.09.2026).", "Number of product cards listed on this sub-category's page on vitra.com.tr (each colour and size counts as a separate card) / of these, cards that are out of stock and carry a \"notify when available\" button (30.09.2026).", True),
       th("vitra.com.tr fiyat aralığı (TL)", "vitra.com.tr price range (TL)", "vitra.com.tr'nin bu alt kategori sayfasındaki en ucuz ve en pahalı ürünün liste fiyatı (sepette uygulanan indirim öncesi).", "List price of the cheapest and most expensive product on this vitra.com.tr sub-category page (before the basket discount).", True),
       th("Trendyol toplam", "Trendyol total", "Trendyol'da alt kategori adıyla (ör. \"sürgülü el duşu\") arama yapıldığında listelenen toplam ürün sayısı; Trendyol'da bu alt kategoride ne kadar ürün olduğunu gösterir.", "Total number of products listed when Trendyol is searched with the sub-category name (e.g. \"sürgülü el duşu\"); shows how many products Trendyol has in this sub-category.", True),
       th("Trendyol medyan (TL)", "Trendyol median (TL)", "Aynı Trendyol aramasında çok satana göre sıralanan ilk 36 ürün içinden, adında alt kategori kelimesi geçen ürünlerin medyan (medyan) fiyatı.", "Median price of the products whose name contains the sub-category keyword among the first 36 products of the same Trendyol search sorted by best sellers.", True),
       th("Hepsiburada toplam", "Hepsiburada total", "Hepsiburada'da alt kategori adıyla arama yapıldığında listelenen toplam ürün sayısı; Hepsiburada 10.000'in üzerini göstermediği için en fazla 10.000.", "Total number of products listed when Hepsiburada is searched with the sub-category name; at most 10,000 because Hepsiburada does not show more.", True),
       th("Hepsiburada medyan (TL)", "Hepsiburada median (TL)", "Aynı Hepsiburada aramasında çok satana göre sıralanan ilk 36 ürün içinden, adında alt kategori kelimesi geçenlerin medyan fiyatı.", "Median price of products whose name contains the sub-category keyword among the first 36 products of the same Hepsiburada search sorted by best sellers.", True),
       th("Akakçe medyan (TL)", "Akakçe median (TL)", "Akakçe'de alt kategori adıyla yapılan aramada eşleşen her ürün için en düşük satıcı fiyatı alınmış, bu fiyatların medyan değeri verilmiştir.", "For each matching product in an Akakçe search with the sub-category name the lowest seller price was taken; the median of these prices is shown.", True),
       th("Akakçe satıcı", "Akakçe sellers", "Akakçe'de eşleşen ürünlerde ürün başına fiyat veren satıcı sayısının medyan değeri; rekabetin ne kadar yoğun olduğunu gösterir.", "Median number of sellers offering a price per matching product on Akakçe; shows how intense competition is.", True),
       th("Cimri medyan (TL)", "Cimri median (TL)", "Cimri'de aynı yöntemle bulunan medyan en düşük fiyat; \"-\" Cimri'de bu alt kategori için sonuç bulunamadı.", "Median lowest price found on Cimri with the same method; \"-\" no result on Cimri for this sub-category.", True),
       th("Cimri satıcı", "Cimri sellers", "Cimri'de ürün başına satıcı sayısının medyan değeri; \"-\" sonuç yok.", "Median number of sellers per product on Cimri; \"-\" no result.", True),
       th("VitrA / Artema adet (TY / HB / Ak / Ci)", "VitrA / Artema count (TY / HB / Ak / Ci)", "Her kanalda alt kategoriyle eşleşen ürünler arasında VitrA veya Artema markalı ürün sayısı; sırasıyla Trendyol, Hepsiburada, Akakçe, Cimri. VitrA'nın pazaryeri listelerinde ne kadar yer aldığını gösterir.", "Number of VitrA or Artema products among the products matching the sub-category in each channel; Trendyol, Hepsiburada, Akakçe, Cimri in that order. Shows how much VitrA appears in marketplace lists.", True),
       th("En çok değerlendirilen marka", "Most-reviewed brand", "Trendyol'da (Trendyol'da sonuç yoksa Hepsiburada'da) eşleşen ürünler içinde en çok kullanıcı değerlendirmesi alan marka ve alt kategorideki değerlendirmelerin yüzde kaçını aldığı.", "The brand with the most user reviews among matching products on Trendyol (on Hepsiburada if Trendyol has no result) and its share of the sub-category's reviews.")]
from b_talep import sekmeler as _sek
_ANAS = []
for q in K2:
    if q["ana_kategori"] not in _ANAS: _ANAS.append(q["ana_kategori"])
T5 = _sek([("Tümü (%d)" % len(K2), "All (%d)" % len(K2), tablo(_B5, [_satir5(q) for q in K2], "uzun"))] +
          [("%s (%d)" % (a, sum(1 for q in K2 if q["ana_kategori"] == a)), "%s (%d)" % (ANA[a], sum(1 for q in K2 if q["ana_kategori"] == a)), tablo(_B5, [_satir5(q) for q in K2 if q["ana_kategori"] == a])) for a in _ANAS], "ttabs")
# vitra.com.tr kategori sayfalari
rows6 = []
for r in VS:
    if "kesit" not in r or r.get("urun") is None: continue
    a, b = AD2[r["kesit"]]
    st = r.get("stoklu") or 0
    rows6.append([x(a, b), u("https://www.vitra.com.tr" + r["yol"], r["yol"]), cell(r["urun"]), n("%s - %s" % (bin(r["fiyat_min"]), bin(r["fiyat_max"])) if r.get("fiyat_min") else "-"),
                  n('<span class="dn">0</span>') if not st else cell(st), cell(r.get("stokta_yok") or 0), n("%d / %d" % (r.get("ilk_sayfa_sepet_indirimli") or 0, r.get("ilk_sayfa_n") or 0)), cell(r.get("ucretsiz_montaj_liste") or 0)])
from grafik2 import yigin as _yg, f_adet as _fa
_R6 = sorted([r for r in VS if "kesit" in r and r.get("urun") is not None], key=lambda r: -(r["urun"] or 0))
_YOLAD = {"/c-banyo-batarya-cikis-uclari": ("Batarya çıkış uçları", "Tap outlets"), "/c-dus-dirsekleri": ("Duş dirsekleri", "Shower elbows"),
          "/c-hidromasajli-standart-kuvetler": ("Hidromasajlı standart küvet", "Standard whirlpool bath"), "/c-hidromasajli-bagimsiz-kuvetler": ("Hidromasajlı bağımsız küvet", "Freestanding whirlpool bath")}
GST = _yg([(x(*_YOLAD.get(r["yol"], AD2[r["kesit"]])), [r.get("stoklu") or 0, max((r["urun"] or 0) - (r.get("stoklu") or 0), 0)]) for r in _R6[:20]],
          [(x("Stoklu", "In stock"), "#2E7D32"), (x("Stokta yok", "Out of stock"), "#D32F2F")],
          x("vitra.com.tr kategori sayfalarında stoklu ve stokta olmayan kart sayısı · en çok kart listeleyen 20 sayfa, 30.09.2026", "In-stock and out-of-stock cards on vitra.com.tr category pages · the 20 pages listing the most cards, 30.09.2026"),
          bicim=_fa, sol=230, mutlak=True, bh=16, ara=8)
T6 = tablo([th("Alt kategori", "Sub-category", "vitra.com.tr'deki kategori sayfasının adı.", "Name of the category page on vitra.com.tr."), th("Sayfa yolu", "Page path", "Kategori sayfasının adresi; yeni sekmede açılır.", "Address of the category page; opens in a new tab."),
            th("Ürün kartı", "Product cards", "Sayfanın üstündeki \"N sonuç listeleniyor\" değeri. Aynı ürünün her rengi ve ölçüsü ayrı kart olarak sayılır.", "The \"N results\" value at the top of the page. Each colour and size of the same product counts as a separate card.", True),
            th("Fiyat aralığı (TL)", "Price range (TL)", "Sayfadaki en ucuz ve en pahalı kartın liste fiyatı (sepet indirimi öncesi); sayfa fiyata göre artan ve azalan sıralanarak okunmuştur.", "List price of the cheapest and most expensive card on the page (before the basket discount); read by sorting the page by ascending and descending price.", True),
            th("Stokta olan", "In stock", "Sayfadaki \"Sadece stoklu ürünleri göster\" süzgeci açıldığında kalan kart sayısı; 0 ise sayfadaki hiçbir ürün stokta değildir.", "Cards remaining when the page's \"show only in-stock products\" filter is switched on; 0 means no product on the page is in stock.", True),
            th("Stokta olmayan", "Out of stock", "Toplam kart sayısından stokta olan kartlar çıkarılarak bulunmuştur; bu kartlar fiyatıyla birlikte listelenmeye devam eder.", "Total cards minus in-stock cards; these cards keep being listed with their price.", True),
            th("İlk sayfada \"Sepette indirim\"", "\"Basket discount\" on first page", "Sayfanın ilk ekranındaki kartlardan kaçında \"Sepette %N indirim\" etiketi olduğu / ilk ekrandaki toplam kart. Bu kartlarda gösterilen fiyat, sepette ödenecek fiyattan yüksektir.", "How many cards on the page's first screen carry a \"N% off in basket\" label / total cards on the first screen. On these cards the displayed price is higher than the price paid in the basket.", True),
            th("Ücretsiz montaj (liste)", "Free installation (list)", "vitra.com.tr'nin ücretsiz montaj sayfasında (/c-ucretsiz-montaj) bu kategoriden yer alan ürün sayısı.", "Number of products from this category on vitra.com.tr's free installation page (/c-ucretsiz-montaj).", True)], rows6, "uzun")
# rakip magazalar
MAG2 = [("koctas", "Koçtaş"), ("bauhaus", "Bauhaus"), ("banyomarka", "Banyomarka"), ("banyomega", "Banyomega"), ("banyoline", "Banyoline"), ("creavit", "Creavit (e-mağaza)")]
from collections import Counter as _Cn2
_TEK7 = _Cn2((c_, ((q_.get("magazalar") or {}).get(c_) or {}).get("eslesen"), _m((q_.get("magazalar") or {}).get(c_)), ((q_.get("magazalar") or {}).get(c_) or {}).get("vitra_adet"))
             for q_ in K2 for c_, _ in MAG2 if ((q_.get("magazalar") or {}).get(c_) or {}).get("eslesen"))
def mg(o, c=None):
    if not o or not o.get("eslesen"): return n("-")
    if c and _TEK7[(c, o.get("eslesen"), _m(o), o.get("vitra_adet"))] > 1: return n("-")   # ayni arama sonucu birden fazla kesite dusmus: kesite ozgu degil
    return n("%d · %s · %s" % (o["eslesen"], _m(o), str(o.get("vitra_adet")) if o.get("vitra_adet") is not None else "-"))
rows7 = [[x(AD2[q["kesit"]][0], AD2[q["kesit"]][1])] + [mg((q.get("magazalar") or {}).get(c), c) for c, _ in MAG2] for q in K2]
T7 = tablo([th("Alt kategori", "Sub-category", "Kesit.", "Segment.")] + [th(m, m.replace("(e-mağaza)", "(e-store)"), "Mağaza aramasında kesitle eşleşen ürün sayısı · eşleşen ürünlerin medyan fiyatı (TL) · VitrA ve Artema ürün sayısı; Koçtaş çok satan sıralı, diğerleri arama sırası; Creavit'te VitrA sayısı okunmamıştır; fiyatı okunamayan hücrelerde medyan \"-\" gösterilir.", "Products matching the segment in the store search · median price (TL) of matching products · VitrA and Artema products; Koçtaş in best-seller order, others in search order; VitrA count not read at Creavit; the median shows \"-\" where prices could not be read.", True) for _, m in MAG2], rows7, "uzun")
# ayni model kodunda fiyat
def fyz2(v):
    if v is None: return n("-")
    return n(("%+.1f" % v).replace(".", ",").replace("+", "+%").replace("-", "-%") if v else "%0")
rows8 = []
for c in ("trendyol", "hepsiburada", "akakce", "cimri"):
    o = FE["kanal"][c]
    rows8.append([veri_m(KAN[c]), cell(o["n"]), cell(o["kod"]), fyz2(o["medyan_liste"]), fyz2(o["medyan_sepet"]), n(yzd(o["altinda"], 0)), n(yzd(o["ustunde_sepet"], 0))])
T8 = tablo([th("Kanal", "Channel", "Pazaryeri ya da fiyat karşılaştırma sitesi; Akakçe ve Cimri'de ürünün en düşük teklifi alınmıştır.", "Marketplace or price comparison site; on Akakçe and Cimri the product's lowest offer is used."),
            th("Eşleşme", "Matches", "Ürün adında vitra.com.tr model kodu birebir geçen VitrA ve Artema satırı.", "VitrA and Artema rows whose product name contains a vitra.com.tr model code verbatim.", True),
            th("Model kodu sayısı", "Model codes", "Benzersiz model kodu sayısı.", "Number of unique model codes.", True),
            th("Liste fiyatına göre medyan fark", "Median gap to list price", "Pazaryeri fiyatı ile vitra.com.tr liste fiyatı arasındaki yüzde farkın medyanı; negatif değer pazaryerinin daha düşük olduğunu gösterir.", "Median percentage gap between the marketplace price and the vitra.com.tr list price; a negative value means the marketplace is lower.", True),
            th("Sepet fiyatına göre medyan fark", "Median gap to basket price", "Aynı fark, vitra.com.tr \"Sepette %N indirim\" uygulanmış fiyata göre.", "The same gap measured against the vitra.com.tr price after the \"N% off in basket\" label is applied.", True),
            th("Liste fiyatının altında pay", "Share below list price", "Eşleşmelerin yüzde kaçında pazaryeri fiyatı liste fiyatının altındadır.", "Percentage of matches where the marketplace price is below the list price.", True),
            th("Sepet fiyatının üstünde pay", "Share above basket price", "Eşleşmelerin yüzde kaçında pazaryeri fiyatı sepet fiyatının üstündedir.", "Percentage of matches where the marketplace price is above the basket price.", True)], rows8, "dar")
def _ad(s): return re.sub(r"\s+", " ", s or "").strip()
def _sat(s): return "-" if not s or s.startswith("no:") else s
rows9 = []
for e in FE["en_yuksek"][:6] + FE["en_dusuk"][:4]:
    rows9.append([veri_m(_ad(e["site_ad"])), veri_m(e["kod"]), veri_m("%s · %s" % (KAN[e["kanal"]], _sat(e["satici"]))), n("%s / %s" % (bin(e["liste"]), bin(e["sepet"]))), cell(round(e["pazar"])), fyz2(round((e["pazar"] / e["liste"] - 1) * 100, 1))])
T9 = tablo([th("Ürün (vitra.com.tr adı)", "Product (vitra.com.tr name)", "vitra.com.tr kategori kartındaki ürün adı.", "Product name on the vitra.com.tr category card."), th("Model kodu", "Model code", "vitra.com.tr kartındaki model kodu; pazaryeri ürün adında birebir geçmektedir.", "Model code on the vitra.com.tr card; appears verbatim in the marketplace product name."),
            th("Kanal · satıcı", "Channel · seller", "Pazaryeri ve ilan satıcısı; Akakçe'de en düşük teklif, satıcı adı okunmamıştır.", "Marketplace and listing seller; on Akakçe the lowest offer, seller name not read."),
            th("vitra.com.tr liste / sepet (TL)", "vitra.com.tr list / basket (TL)", "Liste fiyatı / \"Sepette %N indirim\" uygulanmış fiyat.", "List price / price after the \"N% off in basket\" label.", True),
            th("Pazaryeri fiyatı (TL)", "Marketplace price (TL)", "İlanın 30.09.2026 tarihli fiyatı.", "Listing price on 30.09.2026.", True), th("Liste fiyatına göre fark", "Gap to list price", "Pazaryeri fiyatının liste fiyatına göre yüzde farkı.", "Percentage gap of the marketplace price to the list price.", True)], rows9, "dar")
# KPI degerleri
vk = [r for r in VS if "kesit" in r and r.get("urun") is not None]
top_kart = sum(r["urun"] for r in vk); top_yok = sum(r.get("stokta_yok") or 0 for r in vk)
sifir = sorted({r["kesit"] for r in vk if all(not (q.get("stoklu") or 0) for q in vk if q["kesit"] == r["kesit"])})
sepet_n = sum(r.get("ilk_sayfa_sepet_indirimli") or 0 for r in vk); sepet_t = sum(r.get("ilk_sayfa_n") or 0 for r in vk)
vitrasiz = [q["kesit"] for q in K2 if not any((q.get(c) or {}).get("vitra_adet") for c in ("ty", "hb", "akakce", "cimri"))]
G = FE["genel"]; KA = FE["kanal"]
def fz(v): return ("%+.1f" % v).replace(".", ",").replace("+", "+%").replace("-", "-%")
def fz_en(v): return ("%+.1f%%" % v)
EK = """
<h3>%s</h3>
<div class="kpis">%s%s%s%s</div>
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
%s
%s
%s
""" % (
 x("Alt kesitler: vitra.com.tr, pazaryeri ve fiyat karşılaştırma siteleri", "Sub-segments: vitra.com.tr, marketplaces and price comparison sites"),
 kpi_kart(yzd(top_yok / top_kart * 100), "vitra.com.tr'de incelenen 55 alt kategori sayfasındaki %s varyant kartının stoklu süzgeci dışında kalan payı (lavabo dolabı, boy dolabı, asma klozet ve karo ana listeleri hariç) (%s kart \"Gelince Haber Ver\")" % (bin(top_kart), bin(top_yok)), "Share of the %s variant cards on the 55 vitra.com.tr sub-category pages reviewed (excluding the main basin unit, tall cabinet, wall-hung WC and tile lists) outside the in-stock filter (%s cards \"notify when available\")" % (k(top_kart), k(top_yok)), "dn"),
 kpi_kart(str(len(sifir)), "Stoklu ürün bulunmayan alt kategori sayfası (14 sayfa): duş ünitesi 119, bağımsız küvet 44, bide bataryası 33, pisuvar yıkama sistemi 12 kart", "Sub-category pages without any in-stock product (14 pages): shower unit 119, freestanding bath 44, bidet tap 33, urinal flush system 12 cards", "dn"),
 kpi_kart(fz(G["medyan_liste"]), "Aynı model kodunda pazaryeri fiyatının vitra.com.tr liste fiyatına göre medyan farkı (%s eşleşme, %s model kodu); sepet fiyatına göre Trendyol %s, Hepsiburada %s" % (FE["toplam_eslesme"], FE["benzersiz_kod"], fz(KA["trendyol"]["medyan_sepet"]), fz(KA["hepsiburada"]["medyan_sepet"])),
          "Median gap of the marketplace price to the vitra.com.tr list price for the same model code (%s matches, %s model codes); against the basket price Trendyol %s, Hepsiburada %s" % (FE["toplam_eslesme"], FE["benzersiz_kod"], fz_en(KA["trendyol"]["medyan_sepet"]), fz_en(KA["hepsiburada"]["medyan_sepet"])), "dn"),
 kpi_kart("%d / 57" % len(vitrasiz), "Dört listede (Trendyol, Hepsiburada, Akakçe, Cimri) hiç VitrA ya da Artema ürünü görülmeyen alt kesit; 10'unda vitra.com.tr'de ürün sayfası var", "Sub-segments with no VitrA or Artema product in any of the four lists (Trendyol, Hepsiburada, Akakçe, Cimri); 10 of them have product pages on vitra.com.tr", "hi"),
 T5,
 insight("VitrA ve Artema, duş ve armatür tamamlayıcılarında pazaryeri listelerinin büyük bölümünü doldurmaktadır: sürgülü el duşu takımında Trendyol'da eşleşen 36 ürünün 26'sı, Hepsiburada'da 33'ün 21'i, Akakçe'de 32'nin 25'i ve Cimri'de 32'nin 16'sı VitrA ya da Artema'dır; Trendyol'da kesit değerlendirmelerinin %95,6'sı Artema'ya aittir. Ankastre stop valfte Hepsiburada 36'nın 21'i, Akakçe 32'nin 22'si, Cimri 31'in 20'si; taşıyıcı aparatta Hepsiburada değerlendirmelerinin %100'ü VitrA'dadır. Seramik, küvet ve tamamlayıcı kesitlerde ise VitrA görünürlüğü sınırlıdır: 11 alt kesitte (yarım tezgah lavabo, köşe lavabo, duş ünitesi, hidromasajlı küvet, küvet paneli, duş teknesi paneli, kaydırmaz, banyo konsolu, dolap kulpu, dolap ayağı ve sabunluk) dört listenin çok satan ve arama sonuçlarında VitrA ürünü görülmemekte, bunların 10'unda vitra.com.tr'de ürün sayfası bulunmaktadır (sabunluk 70, duş ünitesi 119, hidromasajlı küvet 84 kart). Çanak lavaboda Trendyol değerlendirmelerinin %96,4'ü ve etajerli lavaboda Hepsiburada'nın %94,2'si Turkuaz'da toplanmakta; bağımsız küvette Trendyol listesi bebek küveti ürünleriyle (Zuu Baby %97,6) dolmaktadır. Çocuk klozeti aramasında Trendyol 2.238 ve Hepsiburada 1.659 sonuç, engelli klozeti için Trendyol'da 43 ürünlük ayrı kategori bulunurken vitra.com.tr'de bu iki başlık ile köşe lavabo ve lavabo ayağı için ayrı kategori sayfası yoktur.",
         "VitrA and Artema fill most of the marketplace lists in shower and tap accessories: in sliding-rail hand shower sets 26 of the 36 matching products on Trendyol, 21 of 33 on Hepsiburada, 25 of 32 on Akakçe and 16 of 32 on Cimri are VitrA or Artema; on Trendyol 95.6% of the segment's reviews belong to Artema. In concealed stop valves 21 of 36 on Hepsiburada, 22 of 32 on Akakçe and 20 of 31 on Cimri; in WC frames 100% of Hepsiburada reviews are VitrA's. In ceramic, bath and accessory segments VitrA's visibility is limited: in 11 sub-segments (semi-recessed basin, corner basin, shower unit, whirlpool bath, bath panel, shower tray panel, anti-slip mat, bathroom console, cabinet handle, cabinet leg and soap dish) no VitrA product appears in the best-seller and search results of the four lists, and 10 of them have product pages on vitra.com.tr (soap dish 70, shower unit 119, whirlpool bath 84 cards). In bowl basins 96.4% of Trendyol reviews and in basins with shelf 94.2% of Hepsiburada reviews sit with Turkuaz; the Trendyol freestanding bath list is filled with baby bath products (Zuu Baby 97.6%). The children's WC search returns 2,238 results on Trendyol and 1,659 on Hepsiburada, and Trendyol has a separate 43-product category for accessible WCs, while vitra.com.tr has no separate category page for these two headings or for corner basins and basin pedestals."),
 x("vitra.com.tr kategori sayfaları: ürün, fiyat aralığı ve stok", "vitra.com.tr category pages: products, price range and stock"), GST + T6,
 insight("Taranan 55 kategori sayfasındaki %s renk ve varyant kartının %s'sı (%s) stoklu süzgecinin dışında kalmaktadır ve %d alt kategoride (14 sayfa) hiç stoklu ürün bulunmamaktadır: duş ünitesi (119 kart), bağımsız küvet (44), bide bataryası (33), pisuvar yıkama sistemi (12), duvar önü rezervuar (8), taşıyıcı aparat (3) ve yedi kesit daha. Kartlarda fiyat gösterilmeye devam ettiğinden stokta olmayan ürünler kategori sayfasının ürün sayısına ve fiyat aralığına dahil kalmaktadır; %s listesindeki 89 ürünün 42'si de \"Gelince Haber Ver\" durumundadır. İlk sayfadaki %s kartın %s'ünde (%s) \"Sepette %%N indirim\" etiketi bulunmaktadır; oranlar %%10 (358 kart), %%14 (237) ve %%15 (98) düzeyindedir ve %s sayfası 413 varyantla listelenmektedir. Yönlendirme döngüsüne giren %s sayfası sitemap'te listelenmeye devam etmektedir." % (bin(top_kart), yzd(top_yok / top_kart * 100), bin(top_yok), len(sifir), u("https://www.vitra.com.tr/c-ucretsiz-montaj", "/c-ucretsiz-montaj"), bin(sepet_t), yzd(sepet_n / sepet_t * 100), bin(sepet_n), u("https://www.vitra.com.tr/c-kampanyali-urunler", "/c-kampanyali-urunler"), veri_m("/c-online-ozel")),
         "Of the %s colour and variant cards on the 55 category pages scanned, %s (%s) fall outside the in-stock filter and %d sub-categories (14 pages) have no in-stock product at all: shower unit (119 cards), freestanding bath (44), bidet tap (33), urinal flush system (12), exposed cistern (8), WC frame (3) and seven more segments. Because the cards keep showing a price, out-of-stock products remain in the category page's product count and price range; 42 of the 89 products in the %s list are also \"notify when available\". Of the %s first-page cards, %s (%s) carry an \"N%% off in basket\" label; the rates are 10%% (358 cards), 14%% (237) and 15%% (98), and the %s page lists 413 variants. The %s page, which enters a redirect loop, is still listed in the sitemap." % ("{:,}".format(top_kart), yzd(top_yok / top_kart * 100).replace("%", "").replace(",", ".") + "%", "{:,}".format(top_yok), len(sifir), u("https://www.vitra.com.tr/c-ucretsiz-montaj", "/c-ucretsiz-montaj"), "{:,}".format(sepet_t), yzd(sepet_n / sepet_t * 100).replace("%", "").replace(",", ".") + "%", "{:,}".format(sepet_n), u("https://www.vitra.com.tr/c-kampanyali-urunler", "/c-kampanyali-urunler"), veri_m("/c-online-ozel"))),
 x("Alt kesitlerde rakip mağazalar", "Competitor stores in the sub-segments"), T7,
 insight("Banyomarka (28 kesitte 249 VitrA satırı; Artema ile birlikte 30 kesitte 351) ve Banyoline (32 kesitte 125 VitrA satırı, 84 tekil ürün; Artema ile birlikte 34 kesitte 178 satır, 124 tekil ürün) alt kesitlerde de VitrA'yı geniş listeleyen mağazalardır; Koçtaş'ta VitrA 84 ve Artema 64 satır (26 kesit) bulunurken Bauhaus'ta VitrA ve Artema üçer satırla sınırlı kalmaktadır. Banyomarka'da sürgülü el duşu takımında eşleşen 32 ürünün 32'si VitrA ya da Artema'dır; markanın Grohe (203 satır), Artema (96) ve Duravit (64) ile birlikte listelendiği görülmektedir. Fiyat düzeyi mağazaya göre belirgin biçimde ayrışmaktadır: çanak lavaboda medyan Banyomega'da 15.340 TL, Banyomarka'da 13.595 TL, Creavit e-mağazasında 7.686 TL, Koçtaş'ta 5.315 TL ve Banyoline'da 3.293 TL'dir; Banyomarka'da monoblok lavabo medyanı 60.025 TL ve hidromasajlı küvet medyanı 254.250 TL ile yüksek fiyat bandındadır. Koçtaş'ın \"Koçtaş Basic\" markası sabunluk kesitinde 7 ürün ve %72 değerlendirme payıyla, Bauhaus sonuçlarında Primanova 68 satırla (sabunluk aramasında 24 ürünün 24'ü) yer almaktadır.",
         "Banyomarka (249 VitrA rows in 28 segments; 351 in 30 segments together with Artema) and Banyoline (125 VitrA rows, 84 unique products, in 32 segments; 178 rows, 124 unique products, in 34 segments with Artema) are also the stores listing VitrA widely in the sub-segments; Koçtaş carries 84 VitrA and 64 Artema rows (26 segments), while Bauhaus is limited to three VitrA and three Artema rows. At Banyomarka all 32 matching sliding-rail hand shower sets are VitrA or Artema; the brand is listed alongside Grohe (203 rows), Artema (96) and Duravit (64). Price levels differ clearly by store: the bowl basin median is 15,340 TL at Banyomega, 13,595 TL at Banyomarka, 7,686 TL at the Creavit e-store, 5,315 TL at Koçtaş and 3,293 TL at Banyoline; at Banyomarka the monoblock basin median of 60,025 TL and the whirlpool bath median of 254,250 TL sit in the high price band. Koçtaş's \"Koçtaş Basic\" brand appears in the soap dish segment with 7 products and a 72% review share, and Primanova appears in Bauhaus results with 68 rows (24 of 24 products in the soap dish search)."),
 x("Aynı model kodunda vitra.com.tr ve pazaryeri fiyatı", "vitra.com.tr and marketplace price for the same model code"), T8, T9,
 insight("Ürün adında vitra.com.tr model kodu birebir geçen %s eşleşmede (%s model kodu) pazaryeri fiyatı liste fiyatının medyan %s altındadır: Akakçe %s (%s eşleşme), Cimri %s (%s), Trendyol %s (%s) ve Hepsiburada %s (%s). \"Sepette %%N indirim\" uygulanmış fiyata göre fark Trendyol'da %s, Cimri'de %s ve Akakçe'de %s seviyesine daralmakta; Hepsiburada'da ise %s ile pazaryeri fiyatı sitenin sepet fiyatının üzerine çıkmaktadır. Pazaryeri fiyatı sitenin sepet fiyatına yakın seyretmekte, liste fiyatı ise kategori sayfasında görünen fiyat olmaya devam etmektedir. Fark iki yönde de açılabilmektedir: üçüncü taraf satıcılarda pisuvar yıkama sistemi 310-2521 (site 7.412 TL) Hepsiburada'da üç satıcıda 14.848 - 15.923 TL, Root Round küvet bataryası A42743 (site 29.882 TL) 65.948 TL, Arkitekta köşe malzemelik A44051 (site 3.747 TL) Trendyol'da 10.129 TL ile liste fiyatının 2-3x'i fiyatla listelenmiştir; %s eşleşmede pazaryeri fiyatı liste fiyatının 1,5x'ini aşmaktadır. Trendyol'da VitrA ve Artema satırlarının 105'inden 33'ü resmi mağazadan, Hepsiburada'da 180 satırın 19'u VitrA mağazasından ve 21'i Hepsiburada'nın kendi satışından gelmekte, kalan satırlar 37 ve 69 farklı üçüncü taraf satıcıya dağılmaktadır." % (FE["toplam_eslesme"], FE["benzersiz_kod"], yzd(abs(G["medyan_liste"])), fz(KA["akakce"]["medyan_liste"]), KA["akakce"]["n"], fz(KA["cimri"]["medyan_liste"]), KA["cimri"]["n"], fz(KA["trendyol"]["medyan_liste"]), KA["trendyol"]["n"], fz(KA["hepsiburada"]["medyan_liste"]), KA["hepsiburada"]["n"], fz(KA["trendyol"]["medyan_sepet"]), fz(KA["cimri"]["medyan_sepet"]), fz(KA["akakce"]["medyan_sepet"]), fz(KA["hepsiburada"]["medyan_sepet"]), FE["ustu_1_5x"]),
         "In the %s matches (%s model codes) whose product name contains a vitra.com.tr model code verbatim, the marketplace price is a median %s below the list price: Akakçe %s (%s matches), Cimri %s (%s), Trendyol %s (%s) and Hepsiburada %s (%s). Against the price after the \"N%% off in basket\" label the gap narrows to %s on Trendyol, %s on Cimri and %s on Akakçe, while on Hepsiburada the marketplace price rises above the site's basket price at %s. The marketplace price tracks the site's basket price, while the list price remains the price shown on the category page. The gap opens in both directions: at third-party sellers the urinal flush system 310-2521 (site 7,412 TL) is listed at 14,848 - 15,923 TL by three Hepsiburada sellers, the Root Round bath filler A42743 (site 29,882 TL) at 65,948 TL and the Arkitekta corner storage unit A44051 (site 3,747 TL) at 10,129 TL on Trendyol, 2-3x the list price; in %s matches the marketplace price exceeds 1.5x the list price. On Trendyol 33 of the 105 VitrA and Artema rows come from the official store, on Hepsiburada 19 of 180 rows from the VitrA store and 21 from Hepsiburada's own sales, with the remaining rows spread over 37 and 69 different third-party sellers." % (FE["toplam_eslesme"], FE["benzersiz_kod"], ("%.1f%%" % abs(G["medyan_liste"])), fz_en(KA["akakce"]["medyan_liste"]), KA["akakce"]["n"], fz_en(KA["cimri"]["medyan_liste"]), KA["cimri"]["n"], fz_en(KA["trendyol"]["medyan_liste"]), KA["trendyol"]["n"], fz_en(KA["hepsiburada"]["medyan_liste"]), KA["hepsiburada"]["n"], fz_en(KA["trendyol"]["medyan_sepet"]), fz_en(KA["cimri"]["medyan_sepet"]), fz_en(KA["akakce"]["medyan_sepet"]), fz_en(KA["hepsiburada"]["medyan_sepet"]), FE["ustu_1_5x"])),
 note("KISIT", "LIMITATION", ul_b([("Arama tabanlı kesitler:", "Search-based segments:", "pazaryerlerinde ve mağazalarda bu alt kategoriler için birebir kategori sayfası çoğunlukla bulunmadığından sonuçlar arama sırasına bağlıdır; eşleşme, ürün ya da kategori adında kesit anahtar sözcüğünün geçmesiyle yapılmıştır ve toplam değerleri aramanın tüm sonuçlarını kapsar.", "marketplaces and stores mostly have no exact category page for these sub-categories, so results depend on search order; matching is based on the segment keyword appearing in the product or category name, and totals cover all search results."),
                                   ("Cimri:", "Cimri:", "17 kesitte veri bulunmamaktadır (banyo askısı, banyo çöp kovası, havluluk, pisuvar ara bölmesi, pisuvar yıkama sistemi ve 12 kesit daha).", "no data for 17 segments (robe hook, bathroom bin, towel rail, urinal divider, urinal flush system and 12 more)."),
                                   ("vitra.com.tr stok sayımı:", "vitra.com.tr stock count:", "14 sayfada \"Sadece stoklu ürünleri göster\" süzgeci sonuç döndürmemektedir; bu sayfalarda ilk sayfadaki tüm kartlar \"Gelince Haber Ver\" işaretli olduğu için stoklu sayı 0 olarak gösterilmiştir. Sepet indirimi liste fiyatı üzerinden hesaplanmıştır.", "on 14 pages the \"show only in-stock products\" filter returns no results; as every first-page card on these pages is marked \"notify when available\", the in-stock count is shown as 0. The basket discount is calculated from the list price."),
                                   ("Toplam değerleri:", "Totals:", "Hepsiburada 11 kesitte 10.000 üst sınırındadır; Akakçe arama sayfalarında toplam gösterilmemektedir; Koçtaş dışındaki mağazalarda çok satan sıralaması bulunmamaktadır. Fiyat, stok ve etiketler 30.09.2026 tarama anına aittir.", "Hepsiburada is capped at 10,000 in 11 segments; Akakçe search pages show no total; stores other than Koçtaş have no best-seller order. Prices, stock and labels belong to the 30.09.2026 scan.")])),
 kaynak("vitra.com.tr 55 kategori ve 3 özel sayfa · Trendyol, Hepsiburada, Akakçe ve Cimri aramaları (57 kesit) · Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline ve Creavit e-mağaza aramaları · 30.09.2026", "vitra.com.tr 55 category and 3 special pages · Trendyol, Hepsiburada, Akakçe and Cimri searches (57 segments) · Koçtaş, Bauhaus, Banyomarka, Banyomega, Banyoline and Creavit e-store searches · 30.09.2026", "D30"),
)
