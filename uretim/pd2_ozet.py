# ozet.md: yontem + tablolar (kesitler.jsonl, vitra_site_kategori.jsonl'den) + elle yazilan anlati (ozet_anlati.md) birlestirilir.
import json, os, collections
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'veri', 'ham', 'derin', 'pazaryeri_derin2')
def oku(f): return [json.loads(l) for l in open(os.path.join(BASE, f), encoding='utf-8')]
K = oku('kesitler.jsonl'); VK = oku('vitra_site_kategori.jsonl')

def n(x):
    if x is None: return '-'
    return '{:,.0f}'.format(x).replace(',', '.')
def p(x):
    return '-' if x is None else '%' + ('{:.1f}'.format(x).replace('.', ',').replace(',0', ''))

def med(o):
    return n(o['fiyat']['medyan']) if o and o.get('fiyat') else None

def hucre_pazar(o):
    if not o: return '-'
    if not o.get('eslesen'): return 'eşleşme yok'
    t = o.get('total')
    yon = 'k+a' if o.get('wc') else 'a'
    return '%s · %s (%s; %d/%d)' % (n(t) if t is not None else '-', med(o), yon, o['eslesen'], o['okunan'])

def hucre_fiyat(o, ad):
    if not o: return '-'
    yon = 'a' if str(o.get('url', '')).startswith('/arama') else 'k'
    if not o.get('okunan'):
        return ('%s · liste okunamadı (%s)' % (n(o.get('total')), yon)) if o.get('total') else 'okunamadı'
    if not o.get('eslesen'):
        return '%s · eşleşen yok (%s; 0/%d)' % (n(o.get('total')), yon, o['okunan'])
    return '%s · %s · %s (%s; %d/%d)' % (n(o.get('total')), med(o), n(o.get('satici_medyan')), yon, o['eslesen'], o['okunan'])

def hucre_vitra(k):
    a = []
    for ad, kod in (('TY', 'ty'), ('HB', 'hb'), ('AK', 'akakce'), ('CM', 'cimri')):
        o = k.get(kod)
        if not o or not o.get('eslesen'): continue
        v = o.get('vitra_adet', 0)
        a.append('%s %d' % (ad, v) + (' (%d)' % o['vitra_en_iyi_sira'] if v else ''))
    return ' · '.join(a) if a else '-'

def hucre_marka(k):
    for ad, kod in (('TY', 'ty'), ('HB', 'hb')):
        o = k.get(kod)
        if o and o.get('en_yuksek_yorumlu_marka') and o['en_yuksek_yorumlu_marka']['yorum'] > 0:
            m = o['en_yuksek_yorumlu_marka']; return '%s %s %s' % (ad, m['marka'], p(m['yorum_payi']))
    return '-'

def vsite_hucre(k):
    v = k.get('vitra_site')
    if not v or not v.get('yollar'): return 'sayfa yok'
    if v.get('urun') is None: return 'okunamadı'
    fr = '%s-%s' % (n(v['fiyat_min']), n(v['fiyat_max'])) if v.get('fiyat_min') else 'fiyat yok'
    return '%s ürün · %s' % (n(v['urun']), fr)

def tablo_ana():
    L = ['| Ana kategori > alt kategori | vitra.com.tr ürün ve fiyat aralığı (TL) | TY toplam · medyan | HB toplam · medyan | Akakçe toplam · medyan · satıcı | Cimri toplam · medyan · satıcı | VitrA/Artema adet (en iyi sıra) | En yüksek yorumlu marka (yorum payı) |', '|---|---|---|---|---|---|---|---|']
    for k in K:
        L.append('| %s > %s | %s | %s | %s | %s | %s | %s | %s |' % (k['ana_kategori'], k['alt_kategori'], vsite_hucre(k), hucre_pazar(k.get('ty')), hucre_pazar(k.get('hb')),
                                                                   hucre_fiyat(k.get('akakce'), 'ak'), hucre_fiyat(k.get('cimri'), 'cm'), hucre_vitra(k), hucre_marka(k)))
    return '\n'.join(L)

def tablo_magaza():
    ad = [('koctas', 'Koçtaş'), ('bauhaus', 'Bauhaus'), ('banyomarka', 'Banyomarka'), ('banyomega', 'Banyomega'), ('banyoline', 'Banyoline'), ('creavit', 'Creavit e-mağaza')]
    L = ['| Alt kategori | ' + ' | '.join(a for _, a in ad) + ' |', '|---|' + '---|' * len(ad)]
    for k in K:
        c = []
        for kod, _ in ad:
            o = k['magazalar'].get(kod)
            if not o or not o.get('eslesen'): c.append('-'); continue
            c.append('%d · %s%s' % (o['eslesen'], med(o) or '-', (' · V%d' % o['vitra_adet']) if o.get('vitra_adet') else ''))
        if any(x != '-' for x in c):
            L.append('| %s | %s |' % (k['alt_kategori'], ' | '.join(c)))
    return '\n'.join(L)

def tablo_vsite():
    L = ['| Alt kategori | Site sayfası | Ürün (varyant) | Fiyat aralığı (TL) | Stoklu | Stokta yok | Ücretsiz Montaj (liste) | İlk sayfada Ücretsiz Montaj | İlk sayfada "Sepette indirim" |', '|---|---|---|---|---|---|---|---|---|']
    seg = {k['kesit']: k for k in K}
    for r in VK:
        if r.get('tur') == 'ozel_sayfa' or 'kesit' not in r: continue
        k = seg[r['kesit']]
        if r.get('durum') == 404:
            L.append('| %s | %s | 404 | - | - | - | - | - | - |' % (k['alt_kategori'], r['yol'])); continue
        L.append('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (k['alt_kategori'], r['yol'], n(r.get('urun')), ('%s-%s' % (n(r['fiyat_min']), n(r['fiyat_max']))) if r.get('fiyat_min') else '-',
                                                                  n(r.get('stoklu')), n(r.get('stokta_yok')), n(r.get('ucretsiz_montaj_liste')), '%d/%d' % (r['ilk_sayfa_montaj'], r['ilk_sayfa_n']), '%d/%d' % (r['ilk_sayfa_sepet_indirimli'], r['ilk_sayfa_n'])))
    return '\n'.join(L)

def tablo_ozel():
    L = ['| Sayfa | Yol | Ürün (varyant) | Fiyat medyanı (TL) | Kategori dağılımı (ilk 6) |', '|---|---|---|---|---|']
    for r in VK:
        if r.get('tur') != 'ozel_sayfa': continue
        fo = r.get('fiyat_ozeti') or {}
        L.append('| %s | %s | %s | %s | %s |' % (r['sayfa'], r['yol'], n(r['urun']), n(fo.get('medyan')), ', '.join('%s: %d' % (a.split('/')[-1], c) for a, c in r['kategori_dagilimi'][:6])))
    return '\n'.join(L)

if __name__ == '__main__':
    kanal_say = collections.OrderedDict()
    U = oku('urunler.jsonl')
    for u in U: kanal_say[u['kanal']] = kanal_say.get(u['kanal'], 0) + 1
    hazir = {'ana': tablo_ana(), 'magaza': tablo_magaza(), 'vsite': tablo_vsite(), 'ozel': tablo_ozel(), 'kanal_say': dict(kanal_say)}
    json.dump(hazir, open(os.path.join(BASE, '_ham', 'ozet_tablolar.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(json.dumps(kanal_say, ensure_ascii=False)); print(len(hazir['ana']), len(hazir['magaza']), len(hazir['vsite']))
