# Kesit, urun ve vitra.com.tr kayitlarindan bulgu/gozlem ozetleri uretir (stdout).
import json, os, re, collections, statistics, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pd2_topla import fold, is_vitra, MARKASIZ
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'veri', 'ham', 'derin', 'pazaryeri_derin2')
def oku(f): return [json.loads(l) for l in open(os.path.join(BASE, f), encoding='utf-8')]
K = oku('kesitler.jsonl'); U = oku('urunler.jsonl'); VK = oku('vitra_site_kategori.jsonl')
seg = {k['kesit']: k for k in K}

print('== Kanal satir sayilari'); c = collections.Counter(u['kanal'] for u in U); print(dict(c))
print('== Eslesen satir sayilari'); print(dict(collections.Counter(u['kanal'] for u in U if u.get('eslesme'))))

print('\n== VitrA/Artema pazaryeri varligi (adet/en iyi sira) - kesit bazli')
for k in K:
    a = []
    for ad, kod in (('TY', 'ty'), ('HB', 'hb'), ('AK', 'akakce'), ('CM', 'cimri')):
        o = k.get(kod)
        if o and o.get('eslesen'): a.append('%s %d/%d(%s)' % (ad, o.get('vitra_adet', 0), o['eslesen'], o.get('vitra_en_iyi_sira')))
    print(k['kesit'], '|', ' '.join(a))

print('\n== Satici toplamlari (TY, eslesen)')
sc = collections.Counter(); ssc = collections.defaultdict(set)
for u in U:
    if u['kanal'] == 'trendyol' and u.get('eslesme'): sc[u['satici']] += 1; ssc[u['satici']].add(u['kesit'])
print([(a, n, len(ssc[a])) for a, n in sc.most_common(15)])
print('== Satici toplamlari (HB, eslesen)')
sc = collections.Counter(); ssc = collections.defaultdict(set)
for u in U:
    if u['kanal'] == 'hepsiburada' and u.get('eslesme'): sc[u['satici']] += 1; ssc[u['satici']].add(u['kesit'])
print([(a, n, len(ssc[a])) for a, n in sc.most_common(15)])
print('== VitrA/Artema satici (TY/HB)')
for kn in ('trendyol', 'hepsiburada'):
    v = collections.Counter(); vs = collections.defaultdict(set)
    for u in U:
        if u['kanal'] == kn and is_vitra(u['marka'], u['ad']): v[u['satici']] += 1; vs[u['satici']].add(u['kesit'])
    print(kn, [(a, n, len(vs[a])) for a, n in v.most_common(12)], 'toplam', sum(v.values()))

print('\n== Marka toplamlari (TY+HB eslesen, urun sayisi)')
bt = collections.Counter(); bs = collections.defaultdict(set)
for u in U:
    if u['kanal'] in ('trendyol', 'hepsiburada') and u.get('eslesme') and fold(u['marka']) not in MARKASIZ:
        bt[u['marka'].strip()] += 1; bs[u['marka'].strip()].add(u['kesit'])
print([(a, n, len(bs[a])) for a, n in bt.most_common(25)])

print('\n== Magaza ozel/kendi markasi adaylari (marka adi magaza adini iceren)')
for kn in ('koctas', 'bauhaus', 'banyomarka', 'banyomega', 'banyoline', 'creavit'):
    b = collections.Counter(u['marka'] for u in U if u['kanal'] == kn and u.get('eslesme'))
    print(kn, b.most_common(8))

print('\n== VitrA site: stok/kampanya')
tot = sum(r.get('urun') or 0 for r in VK if 'kesit' in r and r.get('urun')); sty = sum(r.get('stokta_yok') or 0 for r in VK if 'kesit' in r and r.get('stokta_yok'))
print('toplam varyant', tot, 'stokta yok', sty)
rows = [(r['kesit'], r['urun'], r.get('stokta_yok')) for r in VK if 'kesit' in r and r.get('urun')]
print(sorted(rows, key=lambda x: -(x[2] or 0) / max(x[1], 1))[:12])
print('sepet indirimli ilk sayfa:', sum(r.get('ilk_sayfa_sepet_indirimli', 0) for r in VK if 'kesit' in r), '/', sum(r.get('ilk_sayfa_n', 0) for r in VK if 'kesit' in r))

print('\n== Fiyat karsilastirma: vitra.com.tr liste ve sepet fiyati ile pazaryeri (ayni model kodu, tam eslesme)')
vs = {}
sitek = json.load(open(os.path.join(BASE, '_ham', 'vs.json'), encoding='utf-8')) if os.path.exists(os.path.join(BASE, '_ham', 'vs.json')) else {}
for k, res in sitek.items():
    for it in res.get('items', []):
        for c in it.get('cards') or []:
            if c[2] and c[0] not in vs:
                d = float(c[7] or 0); d = d if 0 <= d < 60 else 0; vs[c[0]] = (c[2], c[2] * (1 - d / 100), k, c[1])
pats = {code: re.compile(r'(?<![a-z0-9])' + r'[\s\-]?'.join(re.escape(ch) for ch in fold(code).replace('-', '')) + r'(?![a-z0-9])') for code in vs if len(code) >= 6}
found = []
for u in U:
    if u['kanal'] in ('trendyol', 'hepsiburada', 'akakce', 'cimri') and u.get('fiyat') and is_vitra(u['marka'], u['ad']):
        nm = fold(u['ad'])
        for code, rx in pats.items():
            if rx.search(nm):
                p, e, sk, sn = vs[code]
                found.append((u['kanal'], sk, code, u['fiyat'], p, round(e), u['satici'], sn)); break
print(len(found), 'eslesme; benzersiz kod', len({f[2] for f in found}))
by = collections.defaultdict(list); by2 = collections.defaultdict(list)
for kn, sk, code, fy, p, e, sat, sn in found:
    if e <= 0 or p <= 0: continue
    by[kn].append(fy / p - 1); by2[kn].append(fy / e - 1)
for kn in by: print(kn, len(by[kn]), 'liste fiyata gore medyan %.1f%%' % (statistics.median(by[kn]) * 100), '| sepet fiyatina gore medyan %.1f%%' % (statistics.median(by2[kn]) * 100), '| pazaryeri < liste oran %.0f%%' % (sum(1 for x in by[kn] if x < 0) / len(by[kn]) * 100))
allr = [x for v in by.values() for x in v]; print('genel', len(allr), 'medyan %.1f%%' % (statistics.median(allr) * 100))
for f in sorted(found, key=lambda f: (f[3] / f[4]))[:6] + sorted(found, key=lambda f: -(f[3] / f[4]))[:6]: print(f)
