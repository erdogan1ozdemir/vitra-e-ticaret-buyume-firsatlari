#!/usr/bin/env python3
"""pazaryeri_fiyat/ozet.md dosyasını üretir (tablolar cok_satan_ozet.json, marka_pay.json, urun_fiyat.json, analiz.json içinden)."""
import json
from pathlib import Path

D = Path(__file__).resolve().parent.parent / 'veri/ham/derin/pazaryeri_fiyat'
oz = json.load(open(D / 'cok_satan_ozet.json'))
cok = json.load(open(D / 'cok_satan.json'))
pay = json.load(open(D / 'marka_pay.json'))
uf = json.load(open(D / 'urun_fiyat.json'))
an = json.load(open(D / 'analiz.json'))
A = an['kanal_fiyat']
E = an['endeks']
KAT = list(cok['kategoriler'].keys())
AD = {k: cok['kategoriler'][k]['ad'] for k in KAT}


def tl(x):
    if x is None:
        return '-'
    if x >= 1000:
        return f'{x:,.0f}'.replace(',', '.')
    if abs(x - round(x)) < 0.005:
        return f'{x:.0f}'
    return f'{x:.2f}'.rstrip('0').rstrip('.')


def yz(v):
    if v is None:
        return '-'
    return f'-%{abs(v):.1f}' if v < 0 else f'%{v:.1f}'


def yz0(n, t):
    return f'%{n / t * 100:.0f}'


def md_tablo(basliklar, satirlar):
    s = '| ' + ' | '.join(basliklar) + ' |\n|' + '|'.join(['---'] * len(basliklar)) + '|\n'
    for r in satirlar:
        s += '| ' + ' | '.join(str(c) for c in r) + ' |\n'
    return s


def kategori_tablosu(kanal):
    rows = []
    for k in KAT:
        v = oz[kanal][k]
        t = v['satici_tipi']
        n = v['n']
        yapi = f"{t.get('resmi', 0)} / {t.get('3P', 0)}" + (f" / {t.get('platform', 0)}" if kanal == 'hb' else '')
        m1 = v['marka_ilk'][0]
        vit = '-' if not v['vitra_urun'] else f"{v['vitra_urun']} ürün, %{v['vitra_degerlendirme_payi']:.1f}"
        rows.append([AD[k], tl(v['medyan_fiyat']), f"{tl(v['min'])} - {tl(v['maks'])}", v['marka_sayisi'], v['satici_sayisi'], yapi, f"{m1[0]} (%{m1[3]:.1f})", vit])
    bas = ['Kategori', 'Medyan fiyat (TL)', 'Fiyat aralığı (TL)', 'Marka', 'Satıcı', 'Satıcı yapısı: marka mağazası / 3P' + (' / platform' if kanal == 'hb' else ''), 'En yüksek değerlendirme payı', 'VitrA + Artema']
    return md_tablo(bas, rows)


def marka_tablosu():
    rows = []
    for k in KAT:
        r = [AD[k]]
        for kanal in ('ty', 'hb'):
            lst = pay['kanallar'][kanal][k][:3]
            r.append('; '.join(f"{x['marka']} {x['urun_adedi']} ürün / %{x['degerlendirme_payi']:.1f}" for x in lst))
        rows.append(r)
    return md_tablo(['Kategori', 'Trendyol: ilk 3 marka (ürün adedi / değerlendirme payı)', 'Hepsiburada: ilk 3 marka (ürün adedi / değerlendirme payı)'], rows)


def vitra_konum():
    rows = []
    for k in KAT:
        r = [AD[k]]
        for kanal in ('ty', 'hb'):
            v = oz[kanal][k]
            if not v['vitra_urun']:
                r.append('yer almıyor')
            else:
                sat = f"VitrA mağazası {v['vitra_resmi_magaza']}, 3P {v['vitra_3p']}" + (f", Hepsiburada {v['vitra_urun'] - v['vitra_resmi_magaza'] - v['vitra_3p']}" if kanal == 'hb' else '')
                r.append(f"{v['vitra_urun']} ürün, sıralar {', '.join(str(s) for s in v['vitra_siralar'])}; değerlendirme payı %{v['vitra_degerlendirme_payi']:.1f}; {sat}")
        rows.append(r)
    return md_tablo(['Kategori', 'Trendyol', 'Hepsiburada'], rows)


def endeks_tablosu():
    rows = []
    ad = {'klozet': 'Klozet (asma klozet: Integra, S50, Sento, S20)', 'lavabo': 'Lavabo (S20)', 'banyo_dolabi': 'Banyo dolabı (Sento, Mia, boy dolapları)', 'lavabo_bataryasi': 'Lavabo bataryası (Artema)',
          'banyo_bataryasi': 'Banyo bataryası (Artema)', 'klozet_kapagi': 'Klozet kapağı', 'rezervuar_ic_takim': 'Rezervuar iç takımı', 'taharet_musluk': 'Taharet musluğu / ara musluk (Artema)', 'dus_seti': 'Duş seti (Artema ankastre set)'}
    for k, v in E.items():
        rows.append([ad[k], v['urun_sayisi'], tl(v['vitra_com_tr_medyan']), tl(v['ty_medyan']), f"{v['ty_kat']}x", tl(v['hb_medyan']), f"{v['hb_kat']}x"])
    return md_tablo(['VitrA ürün grubu', 'Ürün', 'vitra.com.tr medyan liste (TL)', 'Trendyol çok satan medyanı (TL)', 'Oran', 'Hepsiburada çok satan medyanı (TL)', 'Oran'], rows)


def urun_tablosu():
    rows = []
    for x in uf:
        ty3 = '-' if not x['ty_en_dusuk_3p'] else f"{tl(x['ty_en_dusuk_3p'])} ({x['ty_satici_adi']})"
        hb = '-' if not x['hb_buybox'] else f"{tl(x['hb_buybox'])} ({x['hb_satici']})"
        en = x['en_ucuz_kanal'] if x['kanal_sayisi'] > 1 else 'tek kanal'
        ad = x['urun'] if not x['seri'].startswith('Artema') or x['urun'].startswith('Artema') else 'Artema ' + x['urun']
        if x['grup'] == 'İç takım':
            ad = 'Rezervuar iç takımı'
        if x['grup'] == 'Klozet kapağı':
            ad = 'Universal klozet kapağı'
        rows.append([ad, x['kod'], tl(x['vitra_com_tr']), tl(x['ty_vitra_magazasi']), ty3, hb, tl(x['koctas']), en, yz(x['fark_yuzde']) if x['kanal_sayisi'] > 1 else '-'])
    return md_tablo(['Ürün', 'Kod', 'vitra.com.tr (liste)', 'TY VitrA mağazası', 'TY en düşük 3P (satıcı)', 'HB buybox (satıcı)', 'Koçtaş', 'En ucuz kanal', 'Fark'], rows)


def grup_tablosu():
    rows = []
    for g, (n, m) in A['grup_fark_medyan'].items():
        rows.append([g, n, yz(m)])
    return md_tablo(['Ürün grubu', 'Ürün (birden fazla kanalda fiyatı olan)', 'Fark medyanı (vitra.com.tr liste fiyatına göre en ucuz kanalın altında kalma oranı)'], rows)


kf = A
ty_yapi, hb_yapi = an['satici_yapisi']['ty'], an['satici_yapisi']['hb']
ty_tot = sum(ty_yapi.values())
hb_tot = sum(hb_yapi.values())
v_ty = oz['ty']
v_hb = oz['hb']
vt_ty = sum(x['vitra_urun'] for x in v_ty.values())
vt_hb = sum(x['vitra_urun'] for x in v_hb.values())
vr_ty = sum(x['vitra_resmi_magaza'] for x in v_ty.values())
vr_hb = sum(x['vitra_resmi_magaza'] for x in v_hb.values())
v3_ty = sum(x['vitra_3p'] for x in v_ty.values())
v3_hb = sum(x['vitra_3p'] for x in v_hb.values())
vk_ty = sum(1 for x in v_ty.values() if x['vitra_urun'])
vk_hb = sum(1 for x in v_hb.values() if x['vitra_urun'])

metin = f"""# Trendyol ve Hepsiburada · çok satanlar, marka payı ve VitrA kanal fiyatları

Kaynak: Trendyol, Hepsiburada, vitra.com.tr, Koçtaş · gözlem tarihi 29.09.2026 · Türkiye

## Kapsam ve yöntem

- **Kapsam:** Ahrefs'te Trendyol ve Hepsiburada'da en çok organik trafik alan banyo alt kategorilerinden 14 kategori: klozet, klozet kapağı, lavabo, banyo dolabı, çamaşır makinesi dolabı, duşakabin, banyo bataryası, lavabo bataryası, duş seti, taharet musluğu / ara musluk, rezervuar iç takımı, gömme rezervuar, banyo aynası ve banyo aksesuar seti. Her kategori için her iki kanalda "çok satan" sıralamasındaki ilk 36 ürün alındı: **{len(KAT)} kategori × 36 ürün × 2 kanal = 1.008 kayıt**. Önceki tur özetleri (`veri/ham/derin/trendyol`, `veri/ham/derin/hepsiburada`) yalnızca ilk 10 ürünü ve sınırlı alanları içeriyordu; bu turda ilk 36 ürün, satıcı adı, indirim öncesi fiyat, sepet fiyatı, puan, değerlendirme sayısı, teslimat etiketi ve ürün adresiyle genişletildi.
- **Trendyol:** Apify `automation-lab/trendyol-scraper` aktörü; her kategori ayrı çalıştırma (`sr?wc=<kategori>&sst=BEST_SELLER`, en fazla 3 eş zamanlı, çalıştırma başına 36 ürün). Aktör satıcı adı yerine satıcı numarası döndürdüğü için 180 satıcı numarası Trendyol mağaza sayfalarından (mağaza sayfası başlığı) adlandırıldı (istekler arası 3-6 sn). Gömme rezervuar listesi arama tabanlıdır (`sr?q=`).
- **Hepsiburada:** Apify mağazasında Hepsiburada aktörleri bulunuyor (ör. `fatihtahta/hepsiburada-scraper`); aktör çalıştırması Apify hesabında kalan kullanım kredisi (0.047 USD) yeterli olmadığı için başlatılamadı. Bu nedenle kategori sayfasındaki `siralama=coksatan` sıralaması, açık tarayıcı oturumundan (Playwright) sayfa durumu okunarak alındı: kategori başına tek sayfa yüklemesi, istekler arası 3-6 sn. Giriş, form, sepet işlemi ve captcha çözümü yapılmadı; engel veya captcha ile karşılaşılmadı. Banyo dolabı, çamaşır makinesi dolabı, taharet musluğu ve gömme rezervuar için ayrı kategori adresi bulunmadığından arama sayfası (`ara?q=`) kullanıldı.
- **VitrA ürün fiyatları:** vitra.com.tr ürün sitemap'inden (7.804 adres) 39 aday SKU belirlendi (S20, S50, S55, Integra, Sento, Zentrum, Metropole, Mia; Artema Solid S, Minimax S, Flow, Root, Shift, AquaHeat, Joy). Fiyat ürün sayfasındaki liste fiyatı ve "Sepette %X indirim" etiketinden okundu. Her SKU kodu ile Trendyol, Hepsiburada ve Koçtaş'ta aranıp ürün sayfalarındaki diğer satıcı listeleri okundu (istek arası 3-6 sn). Karşılaştırma yalnızca başlığında ürün kodu geçen ve set/paket olmayan listelemelerle yapıldı. 39 adaydan en az iki kanalda eşleşen 26 ürün ve kapsam boşluğunu gösteren 3 ürün olmak üzere **29 ürün** tabloya alındı.
- **Fiyat esası:** Ekranda görünen satış (liste) fiyatı. Trendyol'da aktörün `price` alanı sepet promosyonu uygulanmış tutarı verebildiği için (ör. VitrA Integra 7041B003-0090: liste 12.027 TL, "Sepette %20 indirim" ile 9.621.6 TL) ürün karşılaştırmasında liste fiyatı ve sepet/kampanya fiyatı ayrı sütunlarda tutuldu.
- **Değerlendirme sayısı satışa yaklaşık bir göstergedir**, satış adedi değildir. "Marka payı" ilk 36 içindeki ürün adedi payı ve değerlendirme sayısı payı olarak verilmiştir.
- **Satıcı yapısı tanımı:** marka mağazası = satıcı adı marka adıyla örtüşüyor (ör. Durul, Karen Banyo, VitrA); platform = Hepsiburada'nın kendi satışı; 3P = diğer satıcılar (distribütör, bayi ve pazaryeri satıcıları).

## 1. Kategori bazında çok satanlar

Medyan fiyat ilk 36 ürünün ortancasıdır; aksesuar ve yedek parça ağırlıklı listelerde (duş seti, taharet musluğu, iç takım, aksesuar seti) medyan düşük seviyede kalmaktadır.

### Trendyol

{kategori_tablosu('ty')}
### Hepsiburada

{kategori_tablosu('hb')}
➔ Duşakabin listelerinde iki kanalda da tek marka belirgin biçimde öne çıkıyor (Durul: Trendyol 18 ürün / %{pay['kanallar']['ty']['dusakabin'][0]['degerlendirme_payi']:.1f} değerlendirme payı, Hepsiburada 27 ürün / %{pay['kanallar']['hb']['dusakabin'][0]['degerlendirme_payi']:.1f}); lavabo listelerinde Turkuaz aynı örüntüyü gösteriyor (Trendyol %{pay['kanallar']['ty']['lavabo'][0]['degerlendirme_payi']:.1f}, Hepsiburada %{pay['kanallar']['hb']['lavabo'][0]['degerlendirme_payi']:.1f}). Banyo mobilyası tarafında ilk 36 marka mağazalarından oluşuyor (Karen Banyo, Özceden, Bofigo, Remaks, Aeka).

## 2. Marka payı (ilk 36 içinde ürün adedi ve değerlendirme payı)

{marka_tablosu()}
## 3. Satıcı yapısı

- **Trendyol:** 504 listelemenin {ty_yapi.get('resmi', 0)}'i ({yz0(ty_yapi.get('resmi', 0), ty_tot)}) marka mağazası, {ty_yapi.get('3P', 0)}'i ({yz0(ty_yapi.get('3P', 0), ty_tot)}) 3P satıcı.
- **Hepsiburada:** 504 listelemenin {hb_yapi.get('resmi', 0)}'i ({yz0(hb_yapi.get('resmi', 0), hb_tot)}) marka mağazası, {hb_yapi.get('platform', 0)}'i ({yz0(hb_yapi.get('platform', 0), hb_tot)}) Hepsiburada'nın kendi satışı, {hb_yapi.get('3P', 0)}'i ({yz0(hb_yapi.get('3P', 0), hb_tot)}) 3P satıcı.
- Seramik sağlık gereçleri (klozet, klozet kapağı, lavabo, rezervuar iç takımı) Trendyol'da %78-89 oranında 3P satıcılardan; banyo mobilyası, çamaşır makinesi dolabı ve duşakabin listelerinde ise marka mağazaları öne çıkıyor (Trendyol'da sırasıyla %78, %86 ve %97). Hepsiburada'da klozet ve lavabo listelerinde satışın %50-53'ü Hepsiburada'nın kendi stokundan geliyor.
- En büyük tek satıcılar: Trendyol'da duşakabinde Durul (18/36), aksesuar setinde Okyanus Home (13/36), lavaboda New Banyostyle (12/36), klozette Hace Yapı Malzemeleri (6/36); Hepsiburada'da duşakabinde Durul (27/36), klozet ve lavabo listelerinde Hepsiburada (sırasıyla 18/36 ve 19/36).

## 4. VitrA ve Artema'nın konumu

{vitra_konum()}
➔ VitrA ve Artema ürünleri Trendyol'da {vk_ty} kategoride toplam {vt_ty} listelemeyle, Hepsiburada'da {vk_hb} kategoride toplam {vt_hb} listelemeyle ilk 36'da yer alıyor. Trendyol'daki {vt_ty} listelemenin {vr_ty}'i, Hepsiburada'daki {vt_hb} listelemenin {vr_hb}'si VitrA mağazasından; Trendyol'da {v3_ty}, Hepsiburada'da {v3_hb} listeleme 3P satıcıda, Hepsiburada'da kalan {vt_hb - vr_hb - v3_hb} listeleme Hepsiburada'nın kendi satışında bulunuyor.
➔ Görünürlük rezervuar iç takımı, conta ve klozet kapağı gibi yedek parça ve tamamlayıcı ürünlerde yoğunlaşıyor (Hepsiburada'da rezervuar iç takımı listesinde değerlendirme payı %{v_hb['rezervuar_ic_takim']['vitra_degerlendirme_payi']:.1f}, gömme rezervuar aramasında %{v_hb['gomme_rezervuar']['vitra_degerlendirme_payi']:.1f}). Lavabo, banyo dolabı, çamaşır makinesi dolabı, duşakabin, duş seti ve aksesuar seti listelerinde iki kanalda da VitrA veya Artema ürünü ilk 36 içinde bulunmuyor; klozet listesinde Trendyol'da 3 (sıra 10, 22, 23), Hepsiburada'da 9 listeleme yer alıyor.

## 5. Fiyat konumu

vitra.com.tr liste fiyatı medyanının kategori çok satan medyanına oranı (VitrA ürün grubu, aynı kategoriyle eşleştirilmiş):

{endeks_tablosu()}
➔ Oran klozet ve taharet musluğu / ara musluk gruplarında 0.9x-1.5x aralığında; lavabo, klozet kapağı, iç takım ve armatür gruplarında 1.7x-4.7x aralığında. Banyo dolabında kıyas Hepsiburada listesinin arama sonucu kaynaklı olarak organizer ağırlıklı olması nedeniyle (medyan 924 TL) sınırlı bilgi taşıyor; duş seti oranı, Artema ankastre set ile duş başlığı ağırlıklı listeyi karşılaştırdığı için kıyas amacıyla kullanılmamıştır.

## 6. VitrA ürünlerinde kanal fiyat farkı

Karşılaştırma tabanı: ekranda görünen liste fiyatı (TL). Fark = vitra.com.tr liste fiyatından en ucuz kanalın liste fiyatına düşüş oranı; vitra.com.tr en ucuz kanalsa %0.0.

{urun_tablosu()}
### Özet

- **Kapsam:** {A['urun']} üründen {A['ty_eslesen']}'inde Trendyol, {A['hb_eslesen']}'inde Hepsiburada, {A['kt_eslesen']}'inde Koçtaş listelemesi eşleşti; {A['pazaryeri_fiyati_olan']} üründe vitra.com.tr dışında en az bir kanalda fiyat bulundu.
- **Nerede daha ucuz:** Bu {A['pazaryeri_fiyati_olan']} üründen {A['pazaryeri_herhangi_dusuk']}'unda en ucuz kanal vitra.com.tr dışında (Hepsiburada buybox {A['en_ucuz_kanal_dagilimi'].get('HB buybox', 0)}, Trendyol 3P satıcı {A['en_ucuz_kanal_dagilimi'].get('TY 3P', 0)}, Koçtaş {A['en_ucuz_kanal_dagilimi'].get('Koçtaş', 0)}); {A['en_ucuz_kanal_dagilimi'].get('vitra.com.tr', 0)} üründe vitra.com.tr en ucuz kanal.
- **Fark bandı:** vitra.com.tr dışında daha ucuz kanal bulunan {A['fark_pozitif_n']} üründe fark medyanı {yz(A['fark_pozitif_medyan'])} (çeyrekler {yz(A['fark_pozitif_ceyrek'][0])} - {yz(A['fark_pozitif_ceyrek'][1])}; en düşük {yz(A['fark_pozitif_min'])}, en yüksek {yz(A['fark_pozitif_maks'])}). En belirgin farklar armatürde (Artema Flow Round banyo bataryası A43057 %41.1, Shift T10 lavabo bataryası A43715 %36.5, Flow Round lavabo bataryası A42923 %36.3) ve gömme rezervuar setinde (800-1896 %35.1) görülüyor.
- **Trendyol 3P ve VitrA mağazası:** VitrA mağazası {A['ty_vitra_magazasi_var']} üründe listeleniyor ve {A['ty_magaza_liste_esit']} üründe vitra.com.tr liste fiyatıyla aynı; VitrA mağazası ile 3P satıcının birlikte bulunduğu {A['ty_hem_magaza_hem_3p']} ürünün {A['ty_3p_magazadan_dusuk']}'sında 3P satıcı VitrA mağazasından daha düşük fiyatla listeleniyor (fark {yz(A['ty_magaza_3p_fark'][0])} - {yz(A['ty_magaza_3p_fark'][2])}, medyan {yz(A['ty_magaza_3p_fark'][1])}). 3P satıcının bulunduğu {A['ty_3p_var']} üründe {A['ty_alti'][0]}'sinde en düşük 3P fiyatı vitra.com.tr liste fiyatının altında (medyan {yz(A['ty_alti'][1])}; {yz(A['ty_alti'][2])} - {yz(A['ty_alti'][3])}).
- **Hepsiburada:** {A['hb_eslesen']} üründe buybox satıcısı VitrA mağazası {A['hb_buybox_satici'].get('VitrA mağazası', 0)}, Hepsiburada {A['hb_buybox_satici'].get('Hepsiburada', 0)}, 3P satıcı {A['hb_buybox_satici'].get('3P', 0)} üründe; {A['hb_alti'][0]} üründe buybox fiyatı vitra.com.tr liste fiyatının altında (medyan {yz(A['hb_alti'][1])}; {yz(A['hb_alti'][2])} - {yz(A['hb_alti'][3])}); buybox fiyatının vitra.com.tr liste fiyatından yüksek olduğu ürünlerde tek ve yüksek fiyatlı 3P kaydı bulunuyor (Sento asma klozet 7748B003-0559: 36.765 TL, liste 14.767 TL).
- **Koçtaş:** {A['kt_eslesen']} ürünün tamamı Koçtaş'ın kendi satışı yerine 3P satıcı listelemesi (Evdema, Evdeniste, Banyoline, Banyoatelier, Hace Yapı vb.); {A['kt_alti'][0]} üründe vitra.com.tr liste fiyatından düşük (medyan {yz(A['kt_alti'][1])}; {yz(A['kt_alti'][2])} - {yz(A['kt_alti'][3])}); tüm eşleşmelerde medyanda Koçtaş fiyatı vitra.com.tr liste fiyatından {yz(abs(A['kt_vitracom_fark'][1]))} daha yüksek.
- **Sepet ve kampanya fiyatı:** vitra.com.tr ürün sayfalarında "Sepette %10 veya %15 indirim" etiketi bulunuyor ({A['vitra_sepette_indirim_dagilimi'].get('10', 0)} üründe %10, {A['vitra_sepette_indirim_dagilimi'].get('15', 0)} üründe %15). VitrA'nın Trendyol mağazasında listelenen 7 üründen 6'sında %20-23, Hepsiburada mağazasında %10-20 düzeyinde sepet indirimi görülüyor; bu nedenle sepet fiyatı esasında {A['en_ucuz_kanal_efektif_dagilimi'].get('TY VitrA mağazası', 0)} üründe VitrA'nın Trendyol mağazası en ucuz kanal olarak öne çıkıyor. Sepet/kampanya fiyatlarıyla fark medyanı {yz(A['efektif_fark_pozitif_medyan'])} ({A['efektif_fark_pozitif_n']} ürün; {yz(A['efektif_fark_pozitif_min'])} - {yz(A['efektif_fark_pozitif_maks'])}). Kampanya süreleri sınırlı olabileceğinden karşılaştırmada liste fiyatı esas alınmıştır.
- **Stok ve hizmet notu:** vitra.com.tr'de {A['vitra_stokta_yok']} ürün gözlem anında "stokta yok" durumundaydı (fiyat gösterilmeye devam ediyor). Ürün sayfasında "Ücretsiz Montaj" etiketi {A['vitra_ucretsiz_montaj_etiketi']} üründe (Sento lavabo dolabı 60785) görüldü; Koçtaş'ta 6 ürün sayfasında "Montaj Satın Al" seçeneği bulunuyor. vitra.com.tr'de taksit notu "tüm ürünlerde vade farksız 6 ay taksit ve ücretsiz kargo", Trendyol ve Koçtaş'ta 9 taksit.

Ürün grubu bazında fark medyanı:

{grup_tablosu()}
## 7. Bulgular

➔ Seramik sağlık gereçleri ve tamamlayıcı ürünlerde satış Trendyol'da 3P satıcılarda, Hepsiburada'da ise 3P satıcılar ve Hepsiburada'nın kendi stokunda toplanıyor; VitrA mağazası bu listelerde sınırlı sayıda ürünle görünüyor (Trendyol'da {vr_ty}, Hepsiburada'da {vr_hb} listeleme).
➔ Banyo mobilyası ve duşakabin listeleri marka mağazalarıyla (Durul, Karen Banyo, Özceden, Bofigo, Remaks, Aeka, Okyanus Home) örgütlenmiş görünüyor; VitrA ürünü bu listelerin ilk 36'sında yer almıyor ve 8 banyo mobilyası adayından 4'ü için (Metropole 58195, Sento 60812, 60848 ve 61364) Trendyol ve Hepsiburada'da kod eşleşmesi bulunamadı.
➔ VitrA ve Artema armatür, iç takım ve klozet kapağı ürünlerinde aynı SKU için Trendyol'da 4-21 3P satıcı listelemesi görülüyor (A45228 için 21, A42923 için 16, A41994 için 15, A45200 için 15, 330B1314 için 12 satıcı); aynı üründe satıcılar arasındaki fiyat farkı belirgin (ör. Flow Round banyo bataryası A43057 için 4.190 TL ile 7.199 TL arası).
➔ Distribütör düzeyindeki büyük 3P satıcılar (Evdema gibi) vitra.com.tr liste fiyatına yakın fiyatlarla listeleme yapıyor (Integra 7041B003-0090 için %1.5 fark); diğer 3P satıcıların ve Hepsiburada'nın armatür, gömme rezervuar ve klozet kapağı listelemeleri liste fiyatının %14-41 altında kalıyor.
➔ Hepsiburada'da aynı ürün için birden fazla katalog kaydı bulunuyor (A41994 için 4 kayıt ve 7 satıcı, A43057 için 3 kayıt ve 8 satıcı); bazı kayıtlarda fiyat vitra.com.tr liste fiyatının 2.5 katına çıkıyor (7748B003-0559 için 36.765 TL, liste 14.767 TL). Bu durum fiyat algısının kayıtlar arasında parçalı oluşmasına yol açabilir.

## 8. Kısıtlar

- Satış adedi paylaşılmadığından çok satan sıralaması platformun kendi algoritmasına dayanıyor; değerlendirme sayısı yaklaşık gösterge olarak kullanıldı.
- Hepsiburada'da her kategori için yalnızca ilk sayfa (36 ürün) okundu. Arama tabanlı dört liste (banyo dolabı, çamaşır makinesi dolabı, taharet musluğu, gömme rezervuar) kategori sonuçlarına göre daha geniş bir ürün kümesi içeriyor ve aksesuar / yedek parça ağırlıklı.
- Trendyol'da satıcı adı Apify çıktısında yer almadığı için satıcı numaraları mağaza sayfalarından adlandırıldı; satıcı sayfası başlığı ticari unvandan farklı olabilir. Trendyol kargo / hızlı teslimat etiketi yalnızca klozet listesinde (satıcı zenginleştirmeli ilk çalıştırma; 36 ürünün tamamında "350 TL ve üzeri kargo bedava, satıcı karşılar") ve VitrA ürün eşleşmelerinde okundu; diğer kategorilerde bu alan aktör çıktısında bulunmadığından boş bırakıldı. Hepsiburada'da hızlı teslimat (jet / express) etiketi listelerde gelmediği için teslimat bilgisi kargoya veriliş gününden ("aynı gün / ertesi gün kargo", "N gün içinde kargo") türetildi.
- Liste ve sepet fiyatı farkı: Trendyol'da aktör fiyatı, Hepsiburada'da listeleme fiyatı esas alındı; Hepsiburada "Sepete özel" ve "Premium ile" fiyatları ayrı alanda (`sepet_fiyati`) tutuldu. Kampanya tarihleri (ör. Trendyol Integra kampanyası 30.09.2026'da bitiyor) tek günlük gözlemdir.
- Tek gün gözlemi: fiyatlar ve satıcı sıraları gün içinde değişebilir.
- SKU eşleşmesi başlıkta ürün kodu geçen listelemelerle yapıldı; başlığında kod bulunmayan listelemeler kapsam dışında kaldı. Zentrum takım klozet 7783L003-0092 ve Sento banyo mobilyası 60812 ile 60848 için üç kanalda eşleşme bulunamadı. Koçtaş ve Hepsiburada'da aynı ürün için birden fazla katalog kaydı bulunduğundan "buybox" değeri, eşleşen kayıtlar içindeki en düşük buybox fiyatıdır.
- vitra.com.tr fiyatları ürün sayfasından okundu; 15 ürün gözlem anında "stokta yok" durumundaydı.
- Apify hesabında bu çalıştırmalardan sonra kalan kullanım kredisi 0.047 USD düzeyindedir; yeni Apify çalıştırması için kredi yenilemesi (fatura dönemi veya plan yükseltme) gerekmektedir.
- Marka adları listelemelerdeki yazımdan normalize edildi (aynı markanın farklı yazımları birleştirildi); markasız listelemeler "Markasız (Genel Markalar)" adıyla ayrı sayıldı.

## 9. Maliyet

- Apify: 14 çalıştırma (Trendyol, kategori başına 1), 504 kayıt; olay fiyatlarıyla (çalıştırma başlangıcı 0.005 USD, kayıt başına 0.0028 USD) yaklaşık **1.50 USD** (3 USD sınırının altında). Hepsiburada, Koçtaş ve VitrA ürün eşleşmeleri Apify dışında (Playwright ve doğrudan istek) okundu, ek Apify maliyeti yoktur.

## 10. Dosyalar

- `cok_satan.json`: kanal × kategori × ilk 36 ürün (ürün adı, marka, satıcı, satıcı tipi, fiyat, eski fiyat, sepet fiyatı, puan, değerlendirme, teslimat etiketi, adres).
- `marka_pay.json`: kanal × kategori marka payı (ürün adedi ve değerlendirme payı) ve kanal geneli.
- `cok_satan_ozet.json`: kategori bazlı özet metrikler (medyan fiyat, satıcı yapısı, VitrA konumu).
- `urun_fiyat.csv` ve `urun_fiyat.json`: 29 VitrA ürünü için kanal fiyatları (39 adayın tamamı `urun_fiyat_tum_adaylar.json` içinde).
- `analiz.json`: bu özetteki sayıların türetildiği hesaplar.
- `ty/`, `hb/`, `urun/`: ham veri. `ty/*.txt` Apify veri kümelerinden alan seçilerek aktarılan kompakt satırlardır (ürün no ve fiyat değerleri veri kümeleriyle yeniden karşılaştırıldı, 504 satırda sapma bulunmadı); çalıştırma ve veri kümesi kimlikleri `ty/apify_calistirmalar.json`, satıcı numarası-ad eşlemesi `ty/merchants.json` içindedir. `hb/*.json` Hepsiburada listeleme sayfası durumu, `urun/` SKU arama çıktılarıdır (vitra_com_tr.json, ty_b*.json, hb_b*.json, kt_b*.json).
- Betikler: `uretim/pf_*.py` ve `uretim/pf_*.js`.
"""
(D / 'ozet.md').write_text(metin, encoding='utf-8')
print(len(metin), 'karakter')
