# VitrA e-ticaret alt kategori taramasi (2. tur): ham sekme ciktilarini (_ham/*.json) kesit, urun ve vitra.com.tr kategori kayitlarina cevirir.
import json, os, re, statistics, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pd2_segmentler as S

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'veri', 'ham', 'derin', 'pazaryeri_derin2')
H = os.path.join(BASE, '_ham')
TARIH = '2026-09-30'
TR = str.maketrans('çğıöşüâîû', 'cgiosuaiu')
SCR = '/private/tmp/claude-501/-Users-Erdo-Desktop-Claude-Projects-Vitra/dbdc56cb-c768-473e-95dd-d0ee7d3212ec/scratchpad'

def fold(s):
    return (s or '').replace('İ', 'i').replace('I', 'ı').lower().translate(TR)

def yukle(k):
    p = os.path.join(H, k + '.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

def pct(a, p):
    a = sorted(a)
    if not a: return None
    i = (len(a) - 1) * p; l = int(i); h = min(l + 1, len(a) - 1)
    return round(a[l] + (a[h] - a[l]) * (i - l), 2)

def fiyat_ozeti(v):
    v = [x for x in v if x is not None and x > 0]
    if not v: return None
    return {'min': round(min(v), 2), 'p25': pct(v, .25), 'medyan': pct(v, .5), 'p75': pct(v, .75), 'maks': round(max(v), 2), 'n': len(v)}

TY_NAMES = {}
if os.path.exists(SCR + '/ty_names.json'):
    TY_NAMES.update(json.load(open(SCR + '/ty_names.json', encoding='utf-8')))
if os.path.exists(os.path.join(H, 'ty_satici_ekstra.json')):
    TY_NAMES.update(json.load(open(os.path.join(H, 'ty_satici_ekstra.json'), encoding='utf-8')))
TY_NAMES.update({'369170': 'EMEK YAPI MARKET', '887219': 'ALİKA BANYO', '1228597': 'HYGGE Banyo', '1281089': 'ICON BANYO', '1218430': 'banyo max', '1076750': 'Wons Bathroom', '383643': 'VİMAR YAPI', '287924': 'ÖzÖnal ECA Yetkili Bayi', '144409': 'VitrA (resmi mağaza)'})

MARKASIZ = {'genel markalar', 'markasız', '(markasız)', '', '-', '?', 'markasiz', '(markasiz)'}
VIT = re.compile(r'vitra|artema')

def is_vitra(marka, ad=''):
    return bool(VIT.search(fold(marka))) or bool(re.match(r'^(vitra|artema)\b', fold(ad)))

# ---------- kanal normallestiricileri: her satir -> dict ----------
def n_ty(k, res):
    out = []
    for r in res.get('rows') or []:
        mid = str(r[4]); ad = r[3]
        out.append(dict(sira=r[0], id=str(r[1]), marka=r[2], ad=ad, satici=TY_NAMES.get(mid, 'no:' + mid), fiyat=r[5], eski=r[6] or None, puan=r[7] or None, yorum=r[8], kategori=r[9],
                        url=('https://www.trendyol.com' + r[10]) if r[10] else 'https://www.trendyol.com/x/x-p-%s?merchantId=%s' % (r[1], mid)))
    return out

def n_hb(k, res):
    out = []
    for r in res.get('rows') or []:
        out.append(dict(sira=r[0], id=str(r[1]), marka=r[2], ad=r[3], satici=r[4], fiyat=r[5], eski=r[6] or None, puan=r[7] or None, yorum=r[8], kategori=r[9],
                        url=('https://www.hepsiburada.com' + r[10]) if r[10] else 'https://www.hepsiburada.com/x-p-%s' % r[1]))
    return out

def n_ak(k, res):
    return [dict(sira=r[0], id=str(r[1]), marka=r[2], ad=r[3], satici=None, fiyat=r[4], eski=None, puan=None, yorum=None, saticisayisi=r[5], kategori=res.get('h1'),
                 url='https://www.akakce.com/x/en-ucuz-x-fiyati,%s.html' % r[1]) for r in res.get('rows') or []]

def n_cm(k, res):
    return [dict(sira=r[0], id=str(r[1]), marka=r[2], ad=r[3], satici=r[6] or None, fiyat=r[4], eski=None, puan=None, yorum=None, saticisayisi=r[5], kategori=res.get('h1'),
                 url='https://www.cimri.com/x/en-ucuz-x-fiyatlari,%s' % r[1]) for r in res.get('rows') or []]

def n_kt(k, res):
    return [dict(sira=r[0], id=None, marka=r[1], ad=r[2], satici=r[3], fiyat=r[4], eski=r[5] or None, puan=r[6] or None, yorum=r[7], kategori=r[8], url=None) for r in res.get('rows') or []]

def n_bh(k, res):
    return [dict(sira=r[0], id=None, marka=r[1], ad=r[2], satici='Bauhaus', fiyat=r[3], eski=r[4] or None, puan=r[5] or None, yorum=r[6], kategori=None, url=None) for r in res.get('rows') or []]

def n_kucuk(satici):
    def f(k, res):
        return [dict(sira=r[0], id=None, marka=r[1], ad=r[2], satici=satici, fiyat=r[3], eski=r[4] or None, puan=None, yorum=None, kategori=None,
                     url=('https://shop.creavit.com.tr/products/' + r[5]) if len(r) > 5 and r[5] else None) for r in res.get('rows') or []]
    return f

KANALLAR = [  # (dosya, ad, tip, normallestirici)
    ('ty', 'trendyol', 'pazar', n_ty), ('hb', 'hepsiburada', 'pazar', n_hb), ('ak', 'akakce', 'fiyat', n_ak), ('cm', 'cimri', 'fiyat', n_cm),
    ('kt', 'koctas', 'magaza', n_kt), ('bh', 'bauhaus', 'magaza', n_bh), ('bm', 'banyomarka', 'magaza', n_kucuk('Banyomarka')),
    ('bmg', 'banyomega', 'magaza', n_kucuk('Banyomega')), ('bl', 'banyoline', 'magaza', n_kucuk('Banyoline')), ('cr', 'creavit', 'magaza', n_kucuk('Creavit e-mağaza')),
]

def marka_ozeti(rows):
    bt = collections.OrderedDict()
    for r in rows:
        m = (r['marka'] or '').strip()
        f = fold(m)
        if f in MARKASIZ: f = '(markasız)'; m = '(markasız)'
        if f.startswith('vitra') or f == 'artema': pass
        b = bt.setdefault(f, {'marka': m, 'urun': 0, 'yorum': 0})
        b['urun'] += 1; b['yorum'] += (r.get('yorum') or 0)
    n = len(rows) or 1; ty = sum(b['yorum'] for b in bt.values())
    L = sorted(bt.values(), key=lambda b: (-b['urun'], -b['yorum']))
    for b in L:
        b['urun_payi'] = round(b['urun'] / n * 100, 1); b['yorum_payi'] = round(b['yorum'] / ty * 100, 1) if ty else None
    return L

def kanal_kayit(tip, rows_all, res, seg_re):
    rx = re.compile(seg_re)
    ilg = [r for r in rows_all if rx.search(fold((r['ad'] or '') + ' ' + (r.get('kategori') or '') + ' ' + (r['marka'] or '')))]
    for r in rows_all: r['eslesme'] = r in ilg
    o = {'okunan': len(rows_all), 'eslesen': len(ilg)}
    for a in ('total', 'rel_total', 'wc', 'cands', 'u', 'url', 'h1', 'rt', 'sayfa', 'arama_sayfasi', 'st', 'err'):
        if res.get(a) is not None: o[a] = res[a]
    if res.get('f'): o['facet'] = res['f']
    if res.get('marka_filtre'): o['marka_filtre'] = res['marka_filtre']
    if not ilg:
        return o
    fy = fiyat_ozeti([r['fiyat'] for r in ilg]); o['fiyat'] = fy
    L = marka_ozeti(ilg); o['marka_top5'] = L[:5]
    if any(r.get('yorum') for r in ilg):
        yb = max(L, key=lambda b: b['yorum']); o['en_yuksek_yorumlu_marka'] = {'marka': yb['marka'], 'yorum': yb['yorum'], 'yorum_payi': yb['yorum_payi']}
        tp = max(ilg, key=lambda r: r.get('yorum') or 0)
        o['en_yuksek_yorumlu_urun'] = {'ad': tp['ad'], 'marka': tp['marka'], 'fiyat': tp['fiyat'], 'yorum': tp['yorum'], 'puan': tp['puan'], 'satici': tp['satici']}
    v = [r for r in ilg if is_vitra(r['marka'], r['ad'])]
    o['vitra_adet'] = len(v)
    o['vitra_en_iyi_sira'] = min([r['sira'] for r in v]) if v else None
    if any(r.get('yorum') for r in ilg):
        yt = sum(r.get('yorum') or 0 for r in ilg); o['vitra_yorum_payi'] = round(sum(r.get('yorum') or 0 for r in v) / yt * 100, 1) if yt else None
    o['markasiz_pay'] = round(sum(1 for r in ilg if fold(r['marka']) in MARKASIZ) / len(ilg) * 100, 1)
    if tip == 'pazar':
        sc = collections.Counter(r['satici'] for r in ilg); o['satici_top3'] = [[a, c] for a, c in sc.most_common(3)]; o['satici_sayisi'] = len(sc)
        if v: o['vitra_saticilari'] = [[a, c] for a, c in collections.Counter(r['satici'] for r in v).most_common(4)]
        ind = [r for r in ilg if r.get('eski')]; o['indirimli_pay'] = round(len(ind) / len(ilg) * 100, 1)
    if tip == 'fiyat':
        sv = [r['saticisayisi'] for r in ilg if r.get('saticisayisi') is not None]
        o['satici_medyan'] = statistics.median(sv) if sv else None; o['satici_maks'] = max(sv) if sv else None
    if tip == 'magaza':
        o['indirimli_pay'] = round(sum(1 for r in ilg if r.get('eski')) / len(ilg) * 100, 1)
        o['marka_str'] = ', '.join('%s:%d' % (b['marka'], b['urun']) for b in L[:6])
    return o

def vitra_site(vs):
    """vitra.com.tr ham sonucu -> (kesit anahtari -> ozet, ozel sayfalar)"""
    out = {}
    montaj_kat = collections.Counter(); montaj_id = set()
    oz = vs.get('ucretsiz-montaj')
    if oz:
        for c in oz['items'][0]['cards']:
            montaj_id.add(c[0]); montaj_kat[fold(c[8].split('/')[-1])] += 1
    for k, res in vs.items():
        if 'items' not in res:
            out[k] = [{'yol': (res.get('paths') or ['?'])[0], 'durum': 'okunamadı', 'hata': res.get('err')}] if k in [x[0] for x in S.SEGMENTLER] else None
            continue
        items = []
        for it in res['items']:
            if it.get('st') == 404: items.append({'yol': it['p'], 'durum': 404}); continue
            cards = it.get('cards') or []
            def fv(cs):
                return [c[2] for c in cs if c[2]]
            asc = fv(it.get('asc') or []); desc = fv(it.get('desc') or [])
            allp = fv(cards)
            mn = min(asc[:1] + allp) if (asc or allp) else None
            mx = max(desc[:1] + allp) if (desc or allp) else None
            tot = it.get('total')
            if tot is not None and tot <= len(cards):
                mn = min(allp) if allp else None; mx = max(allp) if allp else None
            stoklu = it.get('instock')
            stok_notu = None
            if stoklu is None and it.get('instock_fail') and cards and all(c[6] for c in cards):
                stoklu = 0; stok_notu = 'stoklu süzgeci yanıt vermedi; ilk sayfadaki tüm kartlar "Gelince Haber Ver" işaretli, stoklu 0 kabul edildi'
            item = {'yol': it['p'], 'baslik': it.get('h1'), 'urun': tot, 'fiyat_min': mn, 'fiyat_max': mx, 'stoklu': stoklu,
                    'stokta_yok': (tot - stoklu) if (tot is not None and stoklu is not None) else None,
                    'ilk_sayfa_n': len(cards), 'ilk_sayfa_montaj': sum(c[5] for c in cards), 'ilk_sayfa_stok_yok_isareti': sum(c[6] for c in cards),
                    'ilk_sayfa_sepet_indirimli': sum(1 for c in cards if c[7] and 0 < float(c[7]) < 60)}
            if stok_notu: item['stok_notu'] = stok_notu
            if not (asc or allp): item['fiyat_not'] = 'fiyat gösterilen ürün yok'
            # tum kategori icin ucretsiz montaj: /c-ucretsiz-montaj listesinde kategori etiketi eslesmesi
            item['ucretsiz_montaj_liste'] = montaj_kat.get(fold(it.get('h1') or ''), 0)
            items.append(item)
        out[k] = items
    return out

def main():
    ham = {a: yukle(a) for a, *_ in KANALLAR}
    # Trendyol: ikinci okuma (web kategorisi zorlamali / degisen arama) eslesme orani daha yuksekse tercih edilir
    p2 = yukle('ty_pass2')
    rgx = {x[0]: re.compile(x[4]) for x in S.SEGMENTLER}
    def oran(res, k):
        rows = res.get('rows') or []
        if not rows: return 0
        return sum(1 for r in rows if rgx[k].search(fold(r[3] + ' ' + r[9] + ' ' + r[2]))) / len(rows)
    for k, v in p2.items():
        if k in ham['ty'] and oran(v, k) > oran(ham['ty'][k], k):
            ham['ty'][k] = v
    vs = yukle('vs')
    vsite = vitra_site(vs) if vs else {}
    keslist = []; urunler = []; vkat = []
    for key, ana, alt, q, seg_re, paths in S.SEGMENTLER:
        rec = {'kesit': key, 'ana_kategori': ana, 'alt_kategori': alt, 'arama_ifadesi': q, 'tarih': TARIH}
        it = vsite.get(key)
        if paths:
            if it is None: rec['vitra_site'] = None
            else:
                tot = sum(i.get('urun') or 0 for i in it if i.get('urun') is not None)
                mins = [i['fiyat_min'] for i in it if i.get('fiyat_min')]; maxs = [i['fiyat_max'] for i in it if i.get('fiyat_max')]
                rec['vitra_site'] = {'yollar': paths, 'urun': tot if any(i.get('urun') is not None for i in it) else None, 'fiyat_min': min(mins) if mins else None, 'fiyat_max': max(maxs) if maxs else None,
                                     'ucretsiz_montaj': sum(i.get('ucretsiz_montaj_liste', 0) for i in it), 'stokta_yok': sum(i['stokta_yok'] for i in it if i.get('stokta_yok') is not None),
                                     'stoklu': sum(i['stoklu'] for i in it if i.get('stoklu') is not None), 'sayfalar': it}
                for i in it: vkat.append(dict(i, kesit=key, tarih=TARIH))
        else:
            rec['vitra_site'] = {'yollar': [], 'urun': None, 'not': 'vitra.com.tr site ağacında bu alt kategori için ayrı sayfa bulunmuyor'}
        rec['magazalar'] = {}
        for a, ad, tip, nf in KANALLAR:
            res = ham[a].get(key)
            if res is None: continue
            rows = nf(key, res)
            kr = kanal_kayit(tip, rows, res, seg_re)
            if tip == 'magaza': rec['magazalar'][ad] = kr
            else: rec[{'trendyol': 'ty', 'hepsiburada': 'hb'}.get(ad, ad)] = kr
            for r in rows:
                urunler.append({'kanal': ad, 'kesit': key, **{k: r.get(k) for k in ('sira', 'id', 'marka', 'ad', 'satici', 'fiyat', 'eski', 'puan', 'yorum', 'saticisayisi', 'kategori', 'eslesme', 'url')}})
        keslist.append(rec)
    oz = {k: v for k, v in vs.items() if v.get('items') and k in dict(S.OZEL_SAYFALAR)}
    ozel = []
    for k, v in vs.items():
        if k in dict(S.OZEL_SAYFALAR) and not v.get('items'):
            ozel.append({'sayfa': k, 'yol': dict(S.OZEL_SAYFALAR)[k], 'urun': None, 'durum': 'sayfa açılamadı: ERR_TOO_MANY_REDIRECTS (yönlendirme döngüsü)', 'okunan': 0, 'kategori_dagilimi': [], 'tarih': TARIH})
    for k, res in oz.items():
        it = res['items'][0]; cards = it['cards']
        kat = collections.Counter(c[8].split('/')[-2] + '/' + c[8].split('/')[-1] if c[8].count('/') >= 2 else c[8] for c in cards)
        ozel.append({'sayfa': k, 'yol': it['p'], 'urun': it.get('total'), 'okunan': len(cards), 'fiyat_ozeti': fiyat_ozeti([c[2] for c in cards]),
                     'stok_yok_isareti': sum(c[6] for c in cards), 'kategori_dagilimi': kat.most_common(15), 'tarih': TARIH})
    def yaz(ad, rows):
        with open(os.path.join(BASE, ad), 'w', encoding='utf-8') as f:
            for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
        print(ad, len(rows))
    yaz('kesitler.jsonl', keslist); yaz('urunler.jsonl', urunler); yaz('vitra_site_kategori.jsonl', vkat + [dict(o, tur='ozel_sayfa') for o in ozel])

if __name__ == '__main__':
    main()
