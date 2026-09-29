#!/usr/bin/env python3
"""Trendyol ve Hepsiburada çok satan (ilk 36) ham verisini birleştirir; cok_satan.json ve marka_pay.json üretir.

Girdi:
  veri/ham/derin/pazaryeri_fiyat/ty/*.txt  (Apify automation-lab/trendyol-scraper çıktısından aktarılan kompakt satırlar) + merchants.json
  veri/ham/derin/pazaryeri_fiyat/hb/*.json (Playwright, Hepsiburada listeleme sayfası durumundan)
Çıktı: cok_satan.json, marka_pay.json, cok_satan_ozet.json (kategori tabloları)
"""
import json, re, statistics, unicodedata
from pathlib import Path
from collections import Counter, defaultdict

DIZIN = Path(__file__).resolve().parent.parent / 'veri/ham/derin/pazaryeri_fiyat'

# (anahtar, kategori adı, TY adres, HB adres)
KATEGORILER = [
    ('klozet', 'Klozet', 'https://www.trendyol.com/sr?wc=109226&sst=BEST_SELLER', 'https://www.hepsiburada.com/klozetler-c-18021930?siralama=coksatan'),
    ('klozet_kapagi', 'Klozet kapağı', 'https://www.trendyol.com/sr?wc=109229&sst=BEST_SELLER', 'https://www.hepsiburada.com/klozet-kapaklari-c-18021958?siralama=coksatan'),
    ('lavabo', 'Lavabo', 'https://www.trendyol.com/sr?wc=109227&sst=BEST_SELLER', 'https://www.hepsiburada.com/lavabolar-c-60004458?siralama=coksatan'),
    ('banyo_dolabi', 'Banyo dolabı', 'https://www.trendyol.com/sr?wc=166314&sst=BEST_SELLER', 'https://www.hepsiburada.com/ara?q=banyo%20dolab%C4%B1&siralama=coksatan'),
    ('camasir_makinesi_dolabi', 'Çamaşır makinesi dolabı', 'https://www.trendyol.com/sr?wc=166316&sst=BEST_SELLER', 'https://www.hepsiburada.com/ara?q=%C3%A7ama%C5%9F%C4%B1r%20makinesi%20dolab%C4%B1&siralama=coksatan'),
    ('dusakabin', 'Duşakabin', 'https://www.trendyol.com/sr?wc=109333&sst=BEST_SELLER', 'https://www.hepsiburada.com/dusakabinler-c-18021979?siralama=coksatan'),
    ('banyo_bataryasi', 'Banyo bataryası', 'https://www.trendyol.com/sr?wc=143557&sst=BEST_SELLER', 'https://www.hepsiburada.com/banyo-bataryalari-c-18021947?siralama=coksatan'),
    ('lavabo_bataryasi', 'Lavabo bataryası', 'https://www.trendyol.com/sr?wc=143558&sst=BEST_SELLER', 'https://www.hepsiburada.com/banyo-lavabo-bataryalari-c-18021983?siralama=coksatan'),
    ('dus_seti', 'Duş seti', 'https://www.trendyol.com/sr?wc=105724&sst=BEST_SELLER', 'https://www.hepsiburada.com/dus-setleri-c-18021971?siralama=coksatan'),
    ('taharet_musluk', 'Taharet musluğu / ara musluk', 'https://www.trendyol.com/sr?wc=143556&sst=BEST_SELLER', 'https://www.hepsiburada.com/ara?q=taharet%20muslu%C4%9Fu&siralama=coksatan'),
    ('rezervuar_ic_takim', 'Rezervuar iç takımı', 'https://www.trendyol.com/sr?wc=144458&sst=BEST_SELLER', 'https://www.hepsiburada.com/rezervuar-ic-takimlar-c-18021929?siralama=coksatan'),
    ('gomme_rezervuar', 'Gömme rezervuar (arama)', 'https://www.trendyol.com/sr?q=g%C3%B6mme%20rezervuar&sst=BEST_SELLER', 'https://www.hepsiburada.com/ara?q=g%C3%B6mme%20rezervuar&siralama=coksatan'),
    ('banyo_aynasi', 'Banyo aynası', 'https://www.trendyol.com/sr?wc=105726&sst=BEST_SELLER', 'https://www.hepsiburada.com/banyo-aynalari-c-60000017?siralama=coksatan'),
    ('banyo_aksesuar_seti', 'Banyo aksesuar seti', 'https://www.trendyol.com/sr?wc=104210&sst=BEST_SELLER', 'https://www.hepsiburada.com/banyo-aksesuar-setleri-c-18021935?siralama=coksatan'),
]

ALIAS = {'nkp': 'NKP', 'turkuazseramik': 'Turkuaz', 'ecaserel': 'Eca', 'eca': 'Eca', 'genelmarkalar': 'Markasız (Genel Markalar)', 'kale': 'Kale', 'vitra': 'VitrA', 'artema': 'Artema',
         'okyanushome': 'Okyanus Home', 'karenbanyo': 'Karen Banyo', 'sueLhouse': 'Suel House'}


def tr_norm(s):
    s = (s or '').replace('İ', 'i').replace('I', 'ı')
    s = s.lower().replace('ı', 'i').replace('ş', 's').replace('ğ', 'g').replace('ü', 'u').replace('ö', 'o').replace('ç', 'c')
    s = unicodedata.normalize('NFKD', s)
    return re.sub(r'[^a-z0-9]', '', s)


KANONIK = {}


def marka_adi(m):
    n = tr_norm(m)
    for k, v in ALIAS.items():
        if n == k.lower():
            return v
    if n.endswith('armatur') and len(n) > 9:
        n = n[:-7]
    if n in ('belirtilmemis', ''):
        return 'Belirtilmemiş'
    return KANONIK.get(n, (m or '').strip())


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', tr_norm(s)).strip('-') or 'urun'


def satici_tip(marka, satici, kanal):
    """resmi mağaza: satıcı adı marka adını içeriyor; platform: Hepsiburada'nın kendi satışı; diğerleri 3P."""
    sm, ss = tr_norm(marka), tr_norm(satici)
    if kanal == 'hb' and ss == 'hepsiburada':
        return 'platform'
    if ss == 'vitra' and sm in ('vitra', 'artema'):
        return 'resmi'
    if len(sm) >= 4 and (sm in ss or (len(ss) >= 4 and ss in sm)) and sm not in ('genelmarkalar',):
        return 'resmi'
    return '3P'


def ty_satirlari():
    merch = json.load(open(DIZIN / 'ty/merchants.json'))
    out = {}
    for anahtar, ad, tyurl, _ in KATEGORILER:
        rows = []
        for i, l in enumerate(open(DIZIN / f'ty/{anahtar}.txt', encoding='utf-8'), 1):
            p = [x.strip() for x in l.rstrip('\n').split('|')]
            if anahtar == 'klozet':
                marka, urun, fiyat, eski, satici, puan, deg, promo, pid, mid = p[:10]
            else:
                marka, urun, fiyat, eski, mid, puan, deg, promo, pid = p[:9]
                satici = merch.get(mid, '#' + mid)
            promo_l = [x for x in promo.split(';') if x and x != 'K']
            f = lambda x: float(x) if x not in ('', None) else None
            rows.append({'sira': i, 'urun': urun, 'marka': marka_adi(marka), 'marka_ham': marka, 'satici': satici, 'satici_no': int(mid),
                         'satici_tip': satici_tip(marka, satici, 'ty'), 'fiyat': f(fiyat), 'eski_fiyat': f(eski), 'puan': f(puan), 'degerlendirme': int(f(deg) or 0),
                         'etiketler': promo_l + (['350 TL ve üzeri kargo bedava'] if 'K' in promo.split(';') else []),
                         'kargo_etiketi': ('kargo bedava (satıcı karşılar)' if 'K' in promo.split(';') else None),
                         'url': f'https://www.trendyol.com/{slug(marka)}/x-p-{pid}?merchantId={mid}'})
        out[anahtar] = rows
    return out


def hb_satirlari():
    out, meta = {}, {}
    for anahtar, ad, _, hburl in KATEGORILER:
        d = json.load(open(DIZIN / f'hb/{anahtar}.json'))
        meta[anahtar] = {'toplam': d.get('total'), 'baslik': d.get('h1')}
        rows = []
        for r in d['rows']:
            marka = marka_adi(r['marka'] if r['marka'] and r['marka'] != 'Belirtilmemiş' else 'Belirtilmemiş')
            eski = r['eski'] if r['eski'] and r['fiyat'] and r['eski'] > r['fiyat'] else None
            gun = r.get('gun')
            teslimat = None
            if gun is not None:
                teslimat = 'aynı gün / ertesi gün kargo' if gun <= 1 else f'{gun} gün içinde kargo'
            rows.append({'sira': r['sira'], 'urun': r['ad'], 'marka': marka, 'marka_ham': r['marka'], 'satici': r['satici'], 'satici_tip': satici_tip(r['marka'], r['satici'], 'hb'),
                         'fiyat': r['fiyat'], 'eski_fiyat': eski, 'sepet_fiyati': r['sepet'], 'sepet_etiketi': r['sepetTip'], 'puan': r['puan'], 'degerlendirme': r['deg'] or 0,
                         'coksatici': r['coksatici'], 'kargo_etiketi': teslimat, 'etiketler': [x for x in r['etiket'] if not x.startswith('Peşin fiyatına')][:4],
                         'url': 'https://www.hepsiburada.com' + r['url']})
        out[anahtar] = rows
    return out, meta


def ozet(rows):
    fiyat = [r['fiyat'] for r in rows if r['fiyat']]
    puan = [r['puan'] for r in rows if r['puan']]
    deg = sum(r['degerlendirme'] for r in rows)
    marka = defaultdict(lambda: [0, 0])
    for r in rows:
        marka[r['marka']][0] += 1
        marka[r['marka']][1] += r['degerlendirme']
    tip = Counter(r['satici_tip'] for r in rows)
    satici = Counter(r['satici'] for r in rows)
    vitra = [r for r in rows if r['marka'] in ('VitrA', 'Artema')]
    o = {'n': len(rows), 'medyan_fiyat': round(statistics.median(fiyat)) if fiyat else None, 'min': min(fiyat) if fiyat else None, 'maks': max(fiyat) if fiyat else None,
         'marka_sayisi': len(marka), 'satici_sayisi': len(satici), 'en_buyuk_satici': satici.most_common(1)[0], 'satici_tipi': dict(tip),
         'medyan_puan': round(statistics.median(puan), 1) if puan else None, 'toplam_degerlendirme': deg,
         'indirimli_urun': sum(1 for r in rows if r['eski_fiyat']),
         'vitra_urun': len(vitra), 'vitra_degerlendirme': sum(r['degerlendirme'] for r in vitra),
         'vitra_siralar': [r['sira'] for r in vitra], 'vitra_medyan_fiyat': round(statistics.median([r['fiyat'] for r in vitra])) if vitra else None,
         'vitra_resmi_magaza': sum(1 for r in vitra if r['satici_tip'] in ('resmi', 'platform') and tr_norm(r['satici']) == 'vitra'),
         'vitra_3p': sum(1 for r in vitra if r['satici_tip'] == '3P')}
    o['vitra_degerlendirme_payi'] = round(o['vitra_degerlendirme'] / deg * 100, 1) if deg else 0
    o['marka_ilk'] = [[m, v[0], v[1], round(v[1] / deg * 100, 1) if deg else 0] for m, v in sorted(marka.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[:6]]
    return o, marka


def kanonik_kur():
    """Aynı markanın farklı yazımlarını (Nkp/NKP, KAREN BANYO/Karen Banyo) tek biçime indirir: en sık geçen yazım kullanılır."""
    sayac = defaultdict(Counter)
    for anahtar, *_ in KATEGORILER:
        for l in open(DIZIN / f'ty/{anahtar}.txt', encoding='utf-8'):
            m = l.split('|')[0]
            n = tr_norm(m)
            n = n[:-7] if n.endswith('armatur') and len(n) > 9 else n
            sayac[n][m] += 1
        for r in json.load(open(DIZIN / f'hb/{anahtar}.json'))['rows']:
            m = r['marka'] or ''
            n = tr_norm(m)
            n = n[:-7] if n.endswith('armatur') and len(n) > 9 else n
            sayac[n][m] += 1
    for n, c in sayac.items():
        # tamamı büyük harf olmayan yazımı tercih et
        adaylar = sorted(c.items(), key=lambda kv: (kv[0].isupper(), -kv[1]))
        KANONIK[n] = adaylar[0][0].strip()


def main():
    kanonik_kur()
    ty = ty_satirlari()
    hb, hbmeta = hb_satirlari()
    cok = {'kaynak': {'ty': 'Trendyol · Apify automation-lab/trendyol-scraper · sst=BEST_SELLER · ilk 36 · 29.09.2026', 'hb': 'Hepsiburada · siralama=coksatan · ilk 36 (ilk sayfa) · 29.09.2026'},
           'not': 'fiyat: listelemede görünen güncel fiyat (Trendyol\'da sepet indirimi uygulanmış olabilir, promosyon metni etiketler alanında); eski_fiyat: üstü çizili fiyat varsa. Değerlendirme sayısı satışa yaklaşık bir göstergedir.',
           'kategoriler': {}}
    pay = {'aciklama': 'Marka payı: ilk 36 içinde ürün adedi payı ve değerlendirme sayısı payı (yüzde). Markasız listelemeler Genel Markalar olarak ayrı gösterilir.', 'kanallar': {'ty': {}, 'hb': {}}, 'genel': {}}
    ozetler = {'ty': {}, 'hb': {}}
    toplam = {'ty': defaultdict(lambda: [0, 0]), 'hb': defaultdict(lambda: [0, 0])}
    for anahtar, ad, tyurl, hburl in KATEGORILER:
        cok['kategoriler'][anahtar] = {'ad': ad, 'trendyol': {'adres': tyurl, 'urunler': ty[anahtar]}, 'hepsiburada': {'adres': hburl, 'sonuc_sayisi': hbmeta[anahtar]['toplam'], 'urunler': hb[anahtar]}}
        for kanal, rows in (('ty', ty[anahtar]), ('hb', hb[anahtar])):
            o, marka = ozet(rows)
            ozetler[kanal][anahtar] = o
            tot = o['toplam_degerlendirme']
            pay['kanallar'][kanal][anahtar] = [{'marka': m, 'urun_adedi': v[0], 'urun_payi': round(v[0] / len(rows) * 100, 1), 'degerlendirme': v[1], 'degerlendirme_payi': round(v[1] / tot * 100, 1) if tot else 0}
                                               for m, v in sorted(marka.items(), key=lambda kv: (-kv[1][1], -kv[1][0]))]
            for m, v in marka.items():
                toplam[kanal][m][0] += v[0]
                toplam[kanal][m][1] += v[1]
    for kanal in ('ty', 'hb'):
        n = sum(v[0] for v in toplam[kanal].values())
        d = sum(v[1] for v in toplam[kanal].values())
        pay['genel'][kanal] = [{'marka': m, 'urun_adedi': v[0], 'urun_payi': round(v[0] / n * 100, 1), 'degerlendirme': v[1], 'degerlendirme_payi': round(v[1] / d * 100, 1)} for m, v in sorted(toplam[kanal].items(), key=lambda kv: (-kv[1][1], -kv[1][0]))[:40]]
    (DIZIN / 'cok_satan.json').write_text(json.dumps(cok, ensure_ascii=False, indent=1))
    (DIZIN / 'marka_pay.json').write_text(json.dumps(pay, ensure_ascii=False, indent=1))
    (DIZIN / 'cok_satan_ozet.json').write_text(json.dumps(ozetler, ensure_ascii=False, indent=1))
    print('tamam', sum(len(v) for v in ty.values()), sum(len(v) for v in hb.values()))


if __name__ == '__main__':
    main()
