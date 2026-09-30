#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pazaryeri_derin: _ham/*.jsonl dosyalarindan konsolide kategori/urun ciktilarini uretir.

Girdi : veri/ham/derin/pazaryeri_derin/_ham/*.jsonl (Chrome uzerinden okunan ham satirlar)
Cikti : veri/ham/derin/pazaryeri_derin/
        ty_kategori.jsonl, hb_kategori.jsonl, akakce_kategori.jsonl, cimri_kategori.jsonl,
        akakce_vitra_urun.jsonl, urunler.jsonl,
        rakip_magaza_kategori.jsonl, rakip_magaza_urunler.jsonl, ozet_tablolar.json
Kullanim: python3 pd_analiz.py
"""
import json, os, re, statistics, collections, sys

BASE = os.path.expanduser('~/Desktop/Claude Projects/Vitra/11_e-ticaret-buyume/veri/ham/derin/pazaryeri_derin')
HAM = os.path.join(BASE, '_ham')
TARIH = '2026-09-30'

HEDEF = ['klozet', 'asma-klozet', 'klozet-takimi', 'akilli-klozet', 'klozet-kapagi', 'lavabo', 'tezgah-ustu-lavabo',
         'tezgah-alti-lavabo', 'lavabo-dolabi', 'banyo-dolabi', 'boy-dolabi', 'aynali-dolap', 'gomme-rezervuar',
         'rezervuar-ic-takimi', 'lavabo-bataryasi', 'banyo-bataryasi', 'ankastre-batarya', 'dus-seti', 'dus-basligi',
         'dusakabin', 'dus-teknesi', 'kuvet', 'pisuvar', 'bide']
# hedef disi
HEDEF_DISI = ['camasir-makinesi-dolabi', 'banyo-aynasi', 'ledli-ayna', 'boy-aynasi', 'havlupan', 'banyo-aksesuar-seti',
              'banyo-rafi', 'taharet-musluk', 'ara-musluk', 'sifon-gider', 'evye', 'mutfak-bataryasi', 'su-aritma',
              'sofben', 'termosifon', 'banyo-paspasi', 'tutunma-bari']

# kanal ici ad -> standart ad
ALIAS = {
    'klozet-takimi-duvara-sifir': 'klozet-takimi', 'klozet-takimi-arkadan-cikisli': 'klozet-takimi',
    'klozet/asma': 'asma-klozet', 'klozet/akilli-klozet': 'akilli-klozet', 'klozet/duvara-sifir': 'klozet-takimi',
    'klozet/arkadan-cikisli': 'klozet-takimi', 'dus-tekneleri': 'dus-teknesi', 'rezervuar': 'gomme-rezervuar',
    'rezervuar-aksesuari': 'rezervuar-ic-takimi', 'banyo-dolabi/lavabolu-banyo-dolabi': 'banyo-dolabi-lavabolu',
    'banyo-aynasi/led-banyo-aynasi': 'ledli-ayna', 'ayna/boy': 'boy-aynasi', 'musluk/taharet': 'taharet-musluk',
    'musluk/ara-musluk': 'ara-musluk', 'lavabo-sifonu': 'sifon-gider', 'sifon': 'sifon-gider',
    'su-aritma-cihazi': 'su-aritma', 'havluluk': 'havlupan-havluluk', 'lavabo/tezgah-alti-lavabo': 'tezgah-alti-lavabo',
    'lavabo/canak': 'canak-lavabo', 'lavabo/monoblok-lavabo': 'monoblok-lavabo',
    'banyo-bataryasi/ankastre-banyo-bataryasi': 'ankastre-batarya', 'banyo-seti': 'banyo-aksesuar-seti',
    'musluk': 'musluk', 'rezervuar-ic-takim': 'rezervuar-ic-takimi', 'aynali-dolap': 'aynali-dolap',
    'rezervuar-kumanda': 'gomme-rezervuar', 'rezervuar-seti': 'gomme-rezervuar', 'klozet-asma': 'asma-klozet',
    'klozet-duvara-sifir': 'klozet-takimi', 'lavabo-canak': 'canak-lavabo', 'banyo-boy-dolabi': 'boy-dolabi',
    'ust-dolap-ayna': 'aynali-dolap', 'ayna-dolapli-ayna': 'aynali-dolap', 'takim-klozetler': 'klozet-takimi',
}

TR_MAP = str.maketrans({'I': 'ı', 'İ': 'i'})


def norm(s):
    return (s or '').translate(TR_MAP).lower()


def std(k):
    return ALIAS.get(k, k)


def is_vitra(brand, name=''):
    b = norm(brand)
    return b in ('vitra', 'artema') or (b in ('', '-', '?', 'genel markalar') and re.search(r'vitra|artema', norm(name)) is not None)


def pctl(a, p):
    a = sorted(a)
    if not a:
        return None
    i = (len(a) - 1) * p
    lo = int(i)
    hi = min(lo + 1, len(a) - 1)
    return round(a[lo] + (a[hi] - a[lo]) * (i - lo), 2)


def stats(prices):
    pr = [x for x in prices if x and x > 0]
    if not pr:
        return None
    return {'min': round(min(pr), 2), 'p25': pctl(pr, .25), 'med': pctl(pr, .5), 'p75': pctl(pr, .75), 'max': round(max(pr), 2)}


def fnum(x):
    try:
        return float(x)
    except Exception:
        return 0.0


def read(name):
    p = os.path.join(HAM, name)
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p, encoding='utf-8') if l.strip()]


def write(name, rows):
    with open(os.path.join(BASE, name), 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(name, len(rows))


# ---------------- Trendyol merchant adlari ----------------
TY_NAMES = {}
for cand in ['/private/tmp/claude-501/-Users-Erdo-Desktop-Claude-Projects-Vitra/dbdc56cb-c768-473e-95dd-d0ee7d3212ec/scratchpad/ty_names.json']:
    if os.path.exists(cand):
        TY_NAMES.update(json.load(open(cand, encoding='utf-8')))
TY_NAMES.update({'369170': 'EMEK YAPI MARKET', '887219': 'ALİKA BANYO', '1228597': 'HYGGE Banyo', '1281089': 'ICON BANYO',
                 '1218430': 'banyo max', '1076750': 'Wons Bathroom', '383643': 'VİMAR YAPI', '287924': 'ÖzÖnal ECA Yetkili Bayi',
                 '144409': 'VitrA (resmi mağaza)'})


def parse_rows(r):
    out = []
    for x in (r or '').split(';'):
        if x.strip():
            out.append(x.split('|'))
    return out


def parse_tally(s):
    """'a:3/12, b:2/5' -> [(a,3,12)]  ya da 'a:3, b:2' -> [(a,3,0)]"""
    res = []
    for part in (s or '').split(', '):
        m = re.match(r'^(.*):(\d+)(?:/(\d+))?$', part.strip())
        if m:
            res.append((m.group(1), int(m.group(2)), int(m.group(3) or 0)))
    return res


UNBRANDED = {'genel markalar', 'markasız', '(markasız)', '', '-', '?'}


KW = {'klozet': 'klozet', 'asma-klozet': 'klozet', 'klozet-takimi': 'klozet', 'akilli-klozet': 'klozet', 'klozet-kapagi': 'kapa',
      'lavabo': 'lavabo', 'tezgah-ustu-lavabo': 'lavabo', 'tezgah-alti-lavabo': 'lavabo', 'lavabo-dolabi': 'dolab|dolap|mobilya',
      'banyo-dolabi': 'dolab|dolap|mobilya', 'boy-dolabi': 'dolab|dolap|mobilya', 'aynali-dolap': 'dolab|dolap|mobilya|ayna',
      'gomme-rezervuar': 'rezervuar|kumanda', 'rezervuar-ic-takimi': 'rezervuar', 'lavabo-bataryasi': 'batarya|armatür',
      'banyo-bataryasi': 'batarya|armatür', 'ankastre-batarya': 'batarya|duş', 'dus-seti': 'duş', 'dus-basligi': 'duş',
      'dusakabin': 'duş|kabin', 'dus-teknesi': 'tekne|duş', 'kuvet': 'küvet', 'pisuvar': 'pisuvar|pisuar', 'bide': 'bide'}


def saflik(key, kat):
    """Ilk 2 sayfa sonuclarinin beklenen kategoriyle ilgili yuzdesi (kat dagilimi yoksa 100)."""
    if not kat:
        return 100.0
    kw = KW.get(std(key))
    tl = parse_tally(kat)
    tot = sum(c for a, c, d in tl)
    if not kw or not tot:
        return None
    ok = sum(c for a, c, d in tl if re.search(kw, norm(a)))
    return round(100.0 * ok / tot, 1)


def share(items, total):
    return [{'ad': a, 'adet': c, 'pay': round(100.0 * c / total, 1) if total else None} for a, c in items]


def kanal_kayit(kanal, r, urun_out):
    """TY veya HB kaydi -> normalize kategori kaydi."""
    key = r.get('key')
    mod = r.get('mod') or ('tam' if 'r' in r else 'ozet')
    is_ty = kanal == 'trendyol'
    rec = {'kanal': kanal, 'kategori': key, 'std': std(key), 'kapsam': 'hedef' if std(key) in HEDEF else 'hedef_disi',
           'tarih': TARIH, 'url': r.get('u'), 'toplam': r.get('total'), 'mod': mod,
           'alt_kategoriler': r.get('f', {}).get('Kategori') or r.get('f', {}).get('Türü') or r.get('f', {}).get('Ürün Tipi'),
           'fiyat_filtre': r.get('f', {}).get('Fiyat') or r.get('f', {}).get('Fiyat Aralığı'),
           'marka_filtre': (r.get('f', {}) or {}).get('Marka'), 'not': r.get('not'), 'kat_dagilimi': r.get('kat'),
           'saflik': saflik(key, r.get('kat'))}
    if mod == 'tam' and 'r' in r:
        rows = parse_rows(r['r'])
        P = []
        for x in rows:
            if len(x) < 9:
                continue
            s, pid, brand, name, sel, price, old, score, rev = x[:9]
            P.append({'s': int(s), 'id': pid, 'b': brand, 'n': name, 'sel': sel, 'f': fnum(price), 'o': fnum(old),
                      'r': fnum(score), 'd': int(fnum(rev))})
        rec['n'] = len(P)
        rec['fiyat'] = stats([p['f'] for p in P])
        bc, br = collections.Counter(), collections.Counter()
        for p in P:
            bc[p['b'] or '-'] += 1
            br[p['b'] or '-'] += p['d']
        totrev = sum(br.values())
        rec['toplam_yorum'] = totrev
        rec['marka_sayisi'] = len(bc)
        rec['marka_adet_top5'] = share(bc.most_common(5), len(P))
        rec['marka_yorum_top5'] = [{'ad': a, 'yorum': c, 'pay': round(100.0 * c / totrev, 1) if totrev else None} for a, c in br.most_common(5)]
        rec['markasiz_pay'] = round(100.0 * sum(c for a, c in bc.items() if norm(a) in UNBRANDED) / len(P), 1) if P else None
        sc = collections.Counter(p['sel'] for p in P)
        rec['satici_sayisi'] = len(sc)
        if is_ty:
            rec['satici_top5'] = [{'ad': TY_NAMES.get(a, 'no:' + a), 'no': a, 'adet': c} for a, c in sc.most_common(5)]
            rec['marka_magaza_payi'] = round(100.0 * sum(1 for p in P if p['sel'] == '144409') / len(P), 1) if P else None
        else:
            rec['satici_top5'] = [{'ad': a, 'adet': c} for a, c in sc.most_common(5)]
            rec['platform_pay'] = round(100.0 * sc.get('Hepsiburada', 0) / len(P), 1) if P else None
        top = sorted(P, key=lambda p: -p['d'])[:10]
        rec['en_cok_yorum10'] = [[p['s'], p['b'], p['n'], p['f'], p['d'], p['r'], (TY_NAMES.get(p['sel'], p['sel']) if is_ty else p['sel'])] for p in top]
        vit = [p for p in P if is_vitra(p['b'], p['n'])]
        rec['vitra_adet'] = len(vit)
        rec['vitra_siralar'] = [p['s'] for p in vit]
        rec['vitra_yorum_payi'] = round(100.0 * sum(p['d'] for p in vit) / totrev, 1) if totrev else None
        for p in P:
            urun_out.append({'kanal': kanal, 'kategori': key, 'sira': p['s'], 'id': p['id'], 'marka': p['b'], 'ad': p['n'],
                             'satici': (TY_NAMES.get(p['sel'], 'no:' + p['sel']) if is_ty else p['sel']), 'fiyat': p['f'],
                             'eski_fiyat': p['o'] or None, 'puan': p['r'] or None, 'yorum': p['d'],
                             'url': (f"https://www.trendyol.com/x/x-p-{p['id']}?merchantId={p['sel']}" if is_ty else f"https://www.hepsiburada.com/x-p-{p['id']}")})
    else:
        rec['n'] = r.get('n')
        rec['fiyat'] = r.get('p')
        tl = parse_tally(r.get('marka'))
        totrev = r.get('deg') or 0
        rec['toplam_yorum'] = totrev
        rec['marka_sayisi'] = r.get('nbrand')
        rec['marka_adet_top5'] = share([(a, c) for a, c, d in sorted(tl, key=lambda t: -t[1])[:5]], r.get('n') or 0)
        rec['marka_yorum_top5'] = [{'ad': a, 'yorum': d, 'pay': round(100.0 * d / totrev, 1) if totrev else None} for a, c, d in sorted(tl, key=lambda t: -t[2])[:5]]
        rec['markasiz_pay'] = round(100.0 * sum(c for a, c, d in tl if norm(a) in UNBRANDED) / r['n'], 1) if r.get('n') else None
        sl = parse_tally(r.get('sat'))
        rec['satici_sayisi'] = r.get('nsat')
        if is_ty:
            rec['satici_top5'] = [{'ad': TY_NAMES.get(a, 'no:' + a), 'no': a, 'adet': c} for a, c, d in sl[:5]]
            rec['marka_magaza_payi'] = round(100.0 * sum(c for a, c, d in sl if a == '144409') / r['n'], 1) if r.get('n') else None
        else:
            rec['satici_top5'] = [{'ad': a, 'adet': c} for a, c, d in sl[:5]]
            rec['platform_pay'] = round(100.0 * sum(c for a, c, d in sl if a == 'Hepsiburada') / r['n'], 1) if r.get('n') else None
            rec['platform_sayisi'] = r.get('plat')
        top = []
        for t in r.get('top', []):
            x = t.split('|')
            if len(x) >= 9:
                top.append([int(x[0]), x[2], x[3], fnum(x[5]), int(fnum(x[8])), fnum(x[7]), (TY_NAMES.get(x[4], x[4]) if is_ty else x[4])])
                urun_out.append({'kanal': kanal, 'kategori': key, 'sira': int(x[0]), 'id': x[1], 'marka': x[2], 'ad': x[3],
                                 'satici': (TY_NAMES.get(x[4], 'no:' + x[4]) if is_ty else x[4]), 'fiyat': fnum(x[5]),
                                 'eski_fiyat': fnum(x[6]) or None, 'puan': fnum(x[7]) or None, 'yorum': int(fnum(x[8])),
                                 'url': (f"https://www.trendyol.com/x/x-p-{x[1]}?merchantId={x[4]}" if is_ty else f"https://www.hepsiburada.com/x-p-{x[1]}")})
        rec['en_cok_yorum10'] = top
        vit = []
        for t in r.get('vitra', []):
            x = t.split('|')
            if len(x) >= 9:
                vit.append(int(x[0]))
                urun_out.append({'kanal': kanal, 'kategori': key, 'sira': int(x[0]), 'id': x[1], 'marka': x[2], 'ad': x[3],
                                 'satici': (TY_NAMES.get(x[4], 'no:' + x[4]) if is_ty else x[4]), 'fiyat': fnum(x[5]),
                                 'eski_fiyat': fnum(x[6]) or None, 'puan': fnum(x[7]) or None, 'yorum': int(fnum(x[8])),
                                 'url': (f"https://www.trendyol.com/x/x-p-{x[1]}?merchantId={x[4]}" if is_ty else f"https://www.hepsiburada.com/x-p-{x[1]}")})
        tv = [(c, d) for a, c, d in tl if norm(a) in ('vitra', 'artema')]
        rec['vitra_adet'] = max(len(vit), sum(c for c, d in tv))
        rec['vitra_siralar'] = vit
        rec['vitra_yorum_payi'] = round(100.0 * sum(d for c, d in tv) / totrev, 1) if totrev and tv else None
    return rec


def akakce_kayit(r):
    key = r.get('kat')
    rec = {'kanal': 'akakce', 'kategori': key, 'std': std(key), 'kapsam': 'hedef' if std(key) in HEDEF else 'hedef_disi', 'tarih': TARIH,
           'toplam': r.get('toplam'), 'marka_sayisi': r.get('marka_sayisi'), 'fiyat_filtre': r.get('fiyat_filtre'),
           'marka_filtre_ilk15': r.get('marka_filtre'), 'alt_kategoriler': r.get('alt') or r.get('ozellik'), 'not': r.get('not')}
    rows = []
    if r.get('r'):
        for x in parse_rows(r['r']):
            if len(x) >= 3:
                rows.append((x[0], fnum(x[1]), int(fnum(x[2]))))
    elif r.get('urun'):
        for u in r['urun']:
            rows.append((u[2], fnum(u[4]), int(u[5])))
    if rows:
        # asiri uc (ornek: 3.4M TL) fiyatlari istatistikten cikar
        pr = [p for b, p, s in rows if 0 < p < 1000000]
        rec['n'] = len(rows)
        rec['fiyat'] = stats(pr)
        bc = collections.Counter(b for b, p, s in rows)
        rec['marka_adet_top5'] = share(bc.most_common(5), len(rows))
        sv = [s for b, p, s in rows if s]
        rec['satici_sayisi_medyan'] = statistics.median(sv) if sv else None
        rec['satici_sayisi_max'] = max(sv) if sv else None
        rec['vitra_adet'] = sum(1 for b, p, s in rows if norm(b) in ('vitra', 'artema'))
        rec['vitra_siralar'] = [i + 1 for i, (b, p, s) in enumerate(rows) if norm(b) in ('vitra', 'artema')]
    rec['en_cok_satici10'] = r.get('top') or ([f"{u[0]}|{u[3]}|{u[2]}|{u[4]}|{u[5]}" for u in sorted(r['urun'], key=lambda u: -u[5])[:10]] if r.get('urun') else None)
    rec['vitra_urunleri'] = r.get('vitra') or [f"{u[0]}|{u[3]}|{u[2]}|{u[4]}|{u[5]}" for u in (r.get('urun') or []) if norm(u[2]) in ('vitra', 'artema')]
    return rec


def cimri_kayit(r):
    key = r.get('kat')
    mod = r.get('mod') or 'tam'
    rec = {'kanal': 'cimri', 'kategori': key, 'std': std(key), 'kapsam': 'hedef' if std(key) in HEDEF else 'hedef_disi', 'tarih': TARIH,
           'toplam': r.get('toplam'), 'mod': mod, 'marka_filtre_ilk15': (r.get('f') or {}).get('Markalar'),
           'magaza_filtre': (r.get('f') or {}).get('Mağaza'), 'not': r.get('not'), 'tekrar_atlanan': r.get('dup')}
    if mod == 'ozet' and r.get('p'):
        rec['n'] = r.get('n')
        rec['fiyat'] = r.get('p')
        rec['marka_adet_top5'] = [{'ad': a, 'adet': c} for a, c, d in parse_tally(r.get('marka'))[:5]]
        rec['magaza_top5'] = [{'ad': a, 'adet': c} for a, c, d in parse_tally(r.get('mag'))[:5]]
        rec['satici_sayisi_medyan'] = r.get('nf_med')
        rec['satici_sayisi_max'] = r.get('nf_max')
        rec['satici_sayisi_toplam'] = r.get('nf_sum')
    else:
        rows = []
        for x in parse_rows(r.get('r')):
            if len(x) >= 4:
                rows.append((x[0], fnum(x[1]), int(fnum(x[2])), x[3]))
        rec['n'] = len(rows)
        rec['fiyat'] = stats([p for b, p, s, m in rows if p < 1000000])
        bc = collections.Counter(b for b, p, s, m in rows)
        rec['marka_adet_top5'] = share(bc.most_common(5), len(rows)) if rows else None
        mc = collections.Counter(m for b, p, s, m in rows)
        rec['magaza_top5'] = [{'ad': a, 'adet': c} for a, c in mc.most_common(5)]
        sv = [s for b, p, s, m in rows if s]
        rec['satici_sayisi_medyan'] = statistics.median(sv) if sv else None
        rec['satici_sayisi_max'] = max(sv) if sv else None
        rec['satici_sayisi_toplam'] = sum(sv) if sv else None
    rec['en_cok_saticili10'] = r.get('top')
    rec['vitra_urunleri'] = r.get('vitra')
    rec['vitra_adet'] = len(r.get('vitra') or [])
    return rec


# ---------------- Rakip magazalar ----------------
def magaza_kayitlari():
    kat, urun = [], []

    def add(magaza, r, key=None, extra=None):
        key = key or r.get('key')
        rec = {'magaza': magaza, 'kategori': key, 'std': std(key), 'kapsam': 'hedef' if std(key) in HEDEF else ('hedef_disi' if std(key) in HEDEF_DISI else 'diger'),
               'tarih': TARIH, 'url': r.get('u'), 'toplam': r.get('toplam'), 'n': r.get('n'), 'fiyat': r.get('p'), 'marka_dagilimi': r.get('marka') or r.get('tur'),
               'indirimli': r.get('indirimli'), 'vitra_adet': r.get('vitra_n', len(r.get('vitra') or [])), 'vitra_urunleri': r.get('vitra'),
               'alt_kategoriler': (r.get('f') or {}).get('Kategori') if isinstance(r.get('f'), dict) else r.get('filtre'), 'not': r.get('not')}
        if extra:
            rec.update(extra)
        kat.append(rec)
        for src in ('vitra', 'top'):
            for t in (r.get(src) or []):
                urun.append({'magaza': magaza, 'kategori': key, 'liste': src, 'ham': t})
    for r in read('koctas_ham.jsonl'):
        add('Koçtaş', r, extra={'satici_dagilimi': r.get('sat'), 'toplam_yorum': r.get('deg')})
    for r in read('bauhaus_ham.jsonl'):
        add('Bauhaus', r, extra={'toplam_yorum': r.get('deg')})
    for r in read('creavit_ham.jsonl'):
        add('Creavit (e-mağaza)', r, extra={'not_marka': 'Tek marka: Creavit; VitrA/Artema ürünü bulunmuyor'})
    for r in read('banyomarka_ham.jsonl'):
        add('Banyomarka', r)
    for r in read('banyomega_ham.jsonl'):
        add('Banyomega', r)
    for r in read('banyoline_ham.jsonl'):
        add('Banyoline', r)
    for r in read('ikea_ham.jsonl'):
        kat.append({'magaza': 'IKEA TR', 'kategori': r.get('key'), 'tarih': TARIH, 'not': r.get('not'), 'seriler': r.get('seriler'), 'gorunen': r.get('gorunen')})
    p = os.path.join(HAM, 'kale_not.json')
    if os.path.exists(p):
        k = json.load(open(p, encoding='utf-8'))
        kat.append({'magaza': 'Kale', 'kategori': 'kale-not', 'kapsam': 'kapsam_disi', 'tarih': TARIH, 'not': 'Fiyat yok, kapsam dışı', 'fiyat_gosterimi': k['fiyat_gosterimi']})
    return kat, urun


def main():
    urunler = []
    ty = [kanal_kayit('trendyol', r, urunler) for r in read('ty_ham.jsonl') if 'key' in r]
    hb = [kanal_kayit('hepsiburada', r, urunler) for r in read('hb_ham.jsonl') if 'key' in r]
    ak = [akakce_kayit(r) for r in read('akakce_ham.jsonl')]
    cm = [cimri_kayit(r) for r in read('cimri_ham.jsonl')]
    write('ty_kategori.jsonl', ty)
    write('hb_kategori.jsonl', hb)
    write('akakce_kategori.jsonl', ak)
    write('cimri_kategori.jsonl', cm)
    write('urunler.jsonl', urunler)
    av = []
    for r in read('akakce_vitra_ham.jsonl'):
        for u in r['u']:
            x = u.split('|')
            if len(x) >= 5:
                av.append({'sayfa': r['kat'], 'sayfa_toplam': r['toplam'], 'sira': int(x[0]), 'id': x[1], 'ad': x[2], 'en_dusuk_fiyat': fnum(x[3]),
                           'satici_sayisi': int(fnum(x[4])), 'tarih': TARIH})
    write('akakce_vitra_urun.jsonl', av)
    mk, mu = magaza_kayitlari()
    write('rakip_magaza_kategori.jsonl', mk)
    write('rakip_magaza_urunler.jsonl', mu)
    return ty, hb, ak, cm, mk, av


if __name__ == '__main__':
    main()
