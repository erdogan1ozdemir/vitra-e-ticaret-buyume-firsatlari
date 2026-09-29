#!/usr/bin/env python3
"""VitrA ürünleri için kanal fiyat karşılaştırması (urun_fiyat.csv, urun_fiyat.json).

Girdi (veri/ham/derin/pazaryeri_fiyat/urun/):
  vitra_com_tr.json  (pf_vitra_urun.py)
  ty_b*.json         (Trendyol SKU araması + ürün sayfası diğer satıcılar)
  hb_b*.json         (Hepsiburada SKU araması + ürün sayfası diğer satıcılar)
  kt_b*.json         (Koçtaş SKU araması + ürün sayfası)
Çıktı: urun_fiyat.csv, urun_fiyat.json (aynı klasörde bir üst dizin: pazaryeri_fiyat/)

Fiyat esası: ekranda görünen satış (liste) fiyatı; sepet/kampanya indirimi ayrı sütunlarda.
Karşılaştırma yalnız başlığında ürün kodu geçen ve paket/set olmayan listelemelerle yapılır.
"""
import csv, glob, json, re
from pathlib import Path

DIZIN = Path(__file__).resolve().parent.parent / 'veri/ham/derin/pazaryeri_fiyat'
URUN = DIZIN / 'urun'
VITRA_TY_ID = 144409


def yukle(desen):
    d = {}
    for f in sorted(glob.glob(str(URUN / desen))):
        d.update(json.load(open(f))['sonuc'])
    return d


def norm(s):
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


PAKET = re.compile(r'\+|\bset\b|takım|takim|gömme rezervuar|yavaş kapan|yavas kapan|soft|kumanda|klozet kapağı dahil|kapak dahil(?! değil)|slim kapak|rezervuar set|tam set|monoblok', re.I)
HARIC = re.compile(r'hariç|haric|dahil değil|dahil degil', re.I)


# vitra.com.tr'de kendisi set olan ürünler (paket filtresi uygulanmaz)
SET_URUNLER = {'9888B003-7201'}
# CSV'ye alınan 30 ürün (39 aday içinden: en az iki kanalda eşleşen 26 ürün + kapsam boşluğunu gösteren 3 BM/klozet ürünü)
SECILEN = ['7041B003-0090', '5618L003-0850', '7748B003-0559', '5505L003-0868', '5473B003-0618', '5501L003-0001',
           '60785', '66166', '67093', '75102', '60812', '60848',
           'A42484', 'A43715', 'A42923', 'A43057', 'A41994', 'A47055EXPS', 'A45200', 'A45228',
           'A49321', '800-1896', '800-2025', '768-1851-01', '121-003-909', '109-003-909', '84-003-009', '330B1314', '7783L003-0092']
KOD_AKTIF = {'kod': None}


def saf(baslik, grup):
    """Başlık tek ürünü mü tarif ediyor? Paket/set/kapak dahil listelemeler dışarıda bırakılır."""
    b = baslik or ''
    if KOD_AKTIF['kod'] in SET_URUNLER:
        return True
    if HARIC.search(b):
        return True
    if grup == 'Klozet kapağı':
        return not re.search(r'asma klozet|gömme|\+|menteşe|damper|\bset\b|takım', b, re.I)
    if grup == 'Gömme rezervuar seti':
        return not re.search(r'asma klozet\s+\d|klozet\s+\+|kumanda paneli', b, re.I)
    if grup == 'İç takım':
        return not re.search(r'\+|\bset\b|conta', b, re.I)
    if grup.startswith('Duş seti'):
        return True
    return not PAKET.search(b)


def marka_uygun(baslik, marka):
    """Marka VitrA/Artema değilse başlıkta marka adı geçmelidir (yalnız ürün kodu geçen ilgisiz listelemeleri eler)."""
    return (marka or '').lower() in ('vitra', 'artema') or bool(re.search(r'vitra|artema', baslik or '', re.I))


def sayi(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def ty_teklifler(rec, kod, grup):
    """Eşleşen Trendyol listeleme sayfalarından (satıcı, fiyat, indirimli) teklifleri toplar."""
    teklif = {}
    sayfa = 0
    for l in rec.get('listeler', []):
        if not l or 'ad' not in l:
            continue
        if norm(kod) not in norm(l['ad']):
            continue
        if not saf(l['ad'], grup):
            continue
        if (l.get('marka') or '').lower() not in ('vitra', 'artema'):
            continue
        sayfa += 1
        s = l['satici']
        teklif.setdefault(s[0], (s[1], sayi(l['guncel']), sayi(l['indirimli']), l['id'], l.get('kargo'), l.get('hizli')))
        for o in l.get('diger', []):
            teklif.setdefault(o[0], (o[1], sayi(o[3]), sayi(o[4]), l['id'], o[5], None))
    return teklif, sayfa


def hb_teklifler(rec, kod, grup):
    teklif = {}
    buybox = []
    sepet = {}
    sayfa = 0
    arama = {a[0]: a for a in rec.get('arama', [])}
    for l in rec.get('listeler', []):
        if not l or 'ad' not in l:
            continue
        if norm(kod) not in norm(l['ad']):
            continue
        if not saf(l['ad'], grup):
            continue
        if not marka_uygun(l['ad'], l.get('marka')):
            continue
        sayfa += 1
        a = arama.get(l['id'])
        fiyat = sayi(l['fiyat'])
        buybox.append((fiyat, l['satici'], l['id'], a[6] if a else None, l.get('kargo'), l.get('gun'), l.get('marka')))
        teklif.setdefault(l['satici'], (fiyat, l['id']))
        for o in l.get('diger', []):
            if o[0] not in teklif:
                teklif[o[0]] = (sayi(o[1]), l['id'])
    return teklif, buybox, sayfa


def kt_teklifler(rec, kod, grup):
    out = []
    arama = {a[0]: a for a in rec.get('arama', [])}
    for l in rec.get('listeler', []):
        if norm(kod) not in norm(l['ad']):
            continue
        if not saf(l['ad'], grup):
            continue
        if not marka_uygun(l['ad'], None):
            continue
        a = arama.get(l['id'])
        fiy = (a[3] if a else [None])
        liste = l.get('ldFiyat') or (fiy[0] if fiy else None)
        sepette = fiy[1] if fiy and len(fiy) > 1 else None
        out.append({'fiyat': liste, 'sepette': sepette, 'satici': (l.get('satici') or [None])[0], 'stok': l.get('stok'), 'montaj': l.get('montajSatinAl'), 'taksit': l.get('taksit'), 'ad': l['ad'], 'url': l['url']})
    return out


def main():
    vt = json.load(open(URUN / 'vitra_com_tr.json'))['urunler']
    ty, hb, kt = yukle('ty_b*.json'), yukle('hb_b*.json'), yukle('kt_b*.json')
    satirlar = []
    for u in vt:
        kod, grup = u['kod'], u['grup']
        KOD_AKTIF['kod'] = kod
        liste = u['liste_fiyat'] or u['fiyat_ld']
        r = {'urun': u['ad'].strip(), 'kod': kod, 'grup': grup, 'seri': u['seri'], 'vitra_com_tr': liste,
             'vitra_sepette': u['sepette_fiyat'] or None, 'vitra_sepette_indirim': u['sepette_indirim_yuzde'],
             'vitra_stok': {'InStock': 'stokta', 'OutOfStock': 'stokta yok', 'PreOrder': 'ön sipariş'}.get(u['stok'], u['stok']),
             'vitra_montaj': 'Ücretsiz Montaj etiketi' if u['ucretsiz_montaj'] else ('Montaj hizmeti eklenebilir' if u['montaj_hizmeti_secenegi'] else '-'),
             'vitra_taksit': u['taksit_notu'], 'vitra_url': u['url']}
        # Trendyol
        teklif, sayfa = ty_teklifler(ty.get(kod, {}), kod, grup)
        r['ty_listeleme_sayisi'] = sayfa
        store = teklif.get(VITRA_TY_ID)
        r['ty_vitra_magazasi'] = store[1] if store else None
        r['ty_vitra_magazasi_indirimli'] = store[2] if store else None
        uc = [(v[1], v[0], k, v[2]) for k, v in teklif.items() if k != VITRA_TY_ID and v[1]]
        uc.sort()
        r['ty_3p_satici_sayisi'] = len(uc)
        r['ty_en_dusuk_3p'] = uc[0][0] if uc else None
        r['ty_satici_adi'] = uc[0][1] if uc else None
        r['ty_en_dusuk_3p_indirimli'] = uc[0][3] if uc else None
        r['ty_en_dusuk_3p_efektif'] = min([(v[2] or v[1]) for k, v in teklif.items() if k != VITRA_TY_ID and v[1]], default=None)
        r['ty_3p_medyan'] = sorted(x[0] for x in uc)[len(uc) // 2] if uc else None
        # Hepsiburada
        hteklif, buybox, hsayfa = hb_teklifler(hb.get(kod, {}), kod, grup)
        r['hb_listeleme_sayisi'] = hsayfa
        if buybox:
            buybox.sort(key=lambda x: (x[0] is None, x[0]))
            b = buybox[0]
            r['hb_buybox'] = b[0]
            r['hb_satici'] = b[1]
            r['hb_kampanya_fiyati'] = b[3]
        else:
            r['hb_buybox'] = r['hb_satici'] = r['hb_kampanya_fiyati'] = None
        hvit = [v for k, v in hteklif.items() if re.fullmatch(r'\s*vitra\s*', k or '', re.I)]
        r['hb_vitra_magazasi'] = hvit[0][0] if hvit else None
        hdiger = sorted((v[0], k) for k, v in hteklif.items() if v[0] and k != r['hb_satici'] and not re.fullmatch(r'\s*vitra\s*', k or '', re.I))
        r['hb_en_dusuk_diger'] = hdiger[0][0] if hdiger else None
        r['hb_en_dusuk_diger_satici'] = hdiger[0][1] if hdiger else None
        r['hb_satici_sayisi'] = len(hteklif)
        # Koçtaş
        kk = kt_teklifler(kt.get(kod, {}), kod, grup)
        kk = [x for x in kk if x['fiyat']]
        kk.sort(key=lambda x: x['fiyat'])
        r['koctas'] = kk[0]['fiyat'] if kk else None
        r['koctas_sepette'] = kk[0]['sepette'] if kk else None
        r['koctas_satici'] = kk[0]['satici'] if kk else None
        r['koctas_montaj_satin_al'] = kk[0]['montaj'] if kk else None
        r['koctas_url'] = ('https://www.koctas.com.tr' + kk[0]['url']) if kk else None
        # en ucuz kanal (liste fiyatı esas)
        kanal = {'vitra.com.tr': r['vitra_com_tr'], 'TY VitrA mağazası': r['ty_vitra_magazasi'], 'TY 3P (%s)' % r['ty_satici_adi']: r['ty_en_dusuk_3p'],
                 'HB buybox (%s)' % r['hb_satici']: r['hb_buybox'], 'HB diğer (%s)' % r['hb_en_dusuk_diger_satici']: r['hb_en_dusuk_diger'], 'Koçtaş': r['koctas']}
        gecerli = {k: v for k, v in kanal.items() if v}
        en = min(gecerli.items(), key=lambda kv: kv[1]) if gecerli else (None, None)
        r['en_ucuz_kanal'] = en[0]
        r['en_ucuz_fiyat'] = en[1]
        v = r['vitra_com_tr']
        r['fark_yuzde'] = round((v - en[1]) / v * 100, 1) if v and en[1] else None
        dig = [x for k, x in gecerli.items() if k != 'vitra.com.tr']
        eff = {'vitra.com.tr': r['vitra_sepette'] or r['vitra_com_tr'], 'TY VitrA mağazası': r['ty_vitra_magazasi_indirimli'] or r['ty_vitra_magazasi'], 'TY 3P': r['ty_en_dusuk_3p_efektif'],
               'HB buybox': r['hb_kampanya_fiyati'] or r['hb_buybox'], 'HB diğer': r['hb_en_dusuk_diger'], 'Koçtaş': r['koctas_sepette'] or r['koctas']}
        eff = {k: x for k, x in eff.items() if x}
        ee = min(eff.items(), key=lambda kv: kv[1]) if eff else (None, None)
        r['en_ucuz_kanal_efektif'] = ee[0]
        r['en_ucuz_efektif_fiyat'] = ee[1]
        r['vitra_efektif'] = eff.get('vitra.com.tr')
        r['fark_efektif_yuzde'] = round((eff['vitra.com.tr'] - ee[1]) / eff['vitra.com.tr'] * 100, 1) if eff.get('vitra.com.tr') and ee[1] else None
        r['yayilim_yuzde'] = round((max(gecerli.values()) - min(gecerli.values())) / min(gecerli.values()) * 100, 1) if len(gecerli) > 1 else None
        r['kanal_sayisi'] = len(gecerli)
        r['ty_3p_resmi_altinda'] = (r['ty_en_dusuk_3p'] < r['ty_vitra_magazasi']) if r['ty_en_dusuk_3p'] and r['ty_vitra_magazasi'] else None
        r['ty_3p_vitracom_altinda'] = (r['ty_en_dusuk_3p'] < v) if r['ty_en_dusuk_3p'] and v else None
        r['hb_3p_vitracom_altinda'] = ((r['hb_buybox'] if r['hb_satici'] not in ('VitrA', 'Hepsiburada') else r['hb_en_dusuk_diger'] or r['hb_buybox']) < v) if (r['hb_buybox'] and v) else None
        satirlar.append(r)
    for r in satirlar:
        r['secili'] = r['kod'] in SECILEN
    (DIZIN / 'urun_fiyat_tum_adaylar.json').write_text(json.dumps(satirlar, ensure_ascii=False, indent=1))
    satirlar = [r for r in satirlar if r['secili']]
    satirlar.sort(key=lambda r: SECILEN.index(r['kod']))
    (DIZIN / 'urun_fiyat.json').write_text(json.dumps(satirlar, ensure_ascii=False, indent=1))
    sutunlar = ['urun', 'kod', 'grup', 'vitra_com_tr', 'ty_vitra_magazasi', 'ty_en_dusuk_3p', 'ty_satici_adi', 'hb_buybox', 'hb_satici', 'koctas', 'en_ucuz_kanal', 'fark_yuzde',
                'seri', 'vitra_sepette', 'vitra_sepette_indirim', 'vitra_stok', 'vitra_montaj', 'vitra_taksit', 'ty_vitra_magazasi_indirimli', 'ty_en_dusuk_3p_indirimli', 'ty_3p_medyan',
                'ty_3p_satici_sayisi', 'ty_listeleme_sayisi', 'hb_kampanya_fiyati', 'hb_vitra_magazasi', 'hb_en_dusuk_diger', 'hb_en_dusuk_diger_satici', 'hb_satici_sayisi', 'hb_listeleme_sayisi',
                'koctas_sepette', 'koctas_satici', 'vitra_efektif', 'ty_en_dusuk_3p_efektif', 'en_ucuz_kanal_efektif', 'en_ucuz_efektif_fiyat', 'fark_efektif_yuzde', 'koctas_montaj_satin_al', 'en_ucuz_fiyat', 'yayilim_yuzde', 'kanal_sayisi', 'ty_3p_resmi_altinda', 'ty_3p_vitracom_altinda', 'hb_3p_vitracom_altinda', 'vitra_url', 'koctas_url']
    with open(DIZIN / 'urun_fiyat.csv', 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=sutunlar, extrasaction='ignore')
        w.writeheader()
        for r in satirlar:
            w.writerow({k: ('' if r.get(k) is None else r.get(k)) for k in sutunlar})
    print(len(satirlar), 'satır yazıldı')


if __name__ == '__main__':
    main()
