#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pd_analiz.py ciktilarindan ozet.md icin Markdown tablolari uretir (TR sayi bicimi).
Cikti: pazaryeri_derin/ozet_tablolar.md"""
import json, os, collections, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pd_analiz import BASE, HEDEF, HEDEF_DISI, norm, std

def rd(n):
    p = os.path.join(BASE, n)
    return [json.loads(l) for l in open(p, encoding='utf-8')] if os.path.exists(p) else []

def tr(x, d=0):
    if x is None:
        return '-'
    s = f"{x:,.{d}f}"
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')

def band(f):
    if not f or not f.get('med'):
        return '-'
    return f"{tr(f['med'])} ({tr(f['p25'])}-{tr(f['p75'])})"

ty, hb, ak, cm, mk = rd('ty_kategori.jsonl'), rd('hb_kategori.jsonl'), rd('akakce_kategori.jsonl'), rd('cimri_kategori.jsonl'), rd('rakip_magaza_kategori.jsonl')
AD = {'klozet': 'Klozet', 'asma-klozet': 'Asma klozet', 'klozet-takimi': 'Klozet takımı', 'akilli-klozet': 'Akıllı klozet', 'klozet-kapagi': 'Klozet kapağı',
      'lavabo': 'Lavabo', 'tezgah-ustu-lavabo': 'Tezgah üstü lavabo', 'tezgah-alti-lavabo': 'Tezgah altı lavabo', 'lavabo-dolabi': 'Lavabo dolabı',
      'banyo-dolabi': 'Banyo dolabı', 'boy-dolabi': 'Boy dolabı', 'aynali-dolap': 'Aynalı dolap', 'gomme-rezervuar': 'Gömme rezervuar',
      'rezervuar-ic-takimi': 'Rezervuar iç takımı', 'lavabo-bataryasi': 'Lavabo bataryası', 'banyo-bataryasi': 'Banyo bataryası',
      'ankastre-batarya': 'Ankastre batarya', 'dus-seti': 'Duş seti', 'dus-basligi': 'Duş başlığı', 'dusakabin': 'Duşakabin', 'dus-teknesi': 'Duş teknesi',
      'kuvet': 'Küvet', 'pisuvar': 'Pisuvar', 'bide': 'Bide', 'camasir-makinesi-dolabi': 'Çamaşır makinesi dolabı', 'banyo-aynasi': 'Banyo aynası',
      'ledli-ayna': 'Ledli ayna', 'boy-aynasi': 'Boy aynası', 'havlupan': 'Havlupan', 'banyo-aksesuar-seti': 'Banyo aksesuar seti', 'banyo-rafi': 'Banyo rafı',
      'taharet-musluk': 'Taharet musluğu', 'ara-musluk': 'Ara musluk', 'sifon-gider': 'Sifon ve gider', 'evye': 'Evye', 'mutfak-bataryasi': 'Mutfak bataryası',
      'su-aritma': 'Su arıtma', 'sofben': 'Şofben', 'termosifon': 'Termosifon', 'banyo-paspasi': 'Banyo paspası', 'tutunma-bari': 'Tutunma barı', 'canak-lavabo': 'Çanak lavabo', 'monoblok-lavabo': 'Monoblok lavabo', 'musluk': 'Musluk', 'banyo-dolabi-lavabolu': 'Lavabolu banyo dolabı', 'havlupan-havluluk': 'Havluluk'}


NAMEKW = {'klozet': 'klozet|wc', 'asma-klozet': 'klozet', 'klozet-takimi': 'klozet', 'akilli-klozet': 'akıllı|akilli|smart', 'klozet-kapagi': 'kapa',
          'lavabo': 'lavabo', 'tezgah-ustu-lavabo': 'lavabo|çanak', 'tezgah-alti-lavabo': 'lavabo', 'lavabo-dolabi': 'lavabo|banyo dolab',
          'banyo-dolabi': 'banyo|dolap|dolab', 'boy-dolabi': 'boy|dolap|dolab', 'aynali-dolap': 'ayna', 'gomme-rezervuar': 'rezervuar|gömme|kumanda|iç takım',
          'rezervuar-ic-takimi': 'iç takım|ic takim|rezervuar', 'lavabo-bataryasi': 'lavabo|batarya|armatür', 'banyo-bataryasi': 'banyo|batarya|armatür',
          'ankastre-batarya': 'ankastre', 'dus-seti': 'duş|dus', 'dus-basligi': 'duş|dus|tepe', 'dusakabin': 'duşakabin|duş kabin|kabin|duşakab',
          'dus-teknesi': 'tekne', 'kuvet': 'küvet|kuvet', 'pisuvar': 'pisuvar|pisuar', 'bide': 'bide'}


MINFIYAT = {'kuvet': 3000, 'lavabo': 500, 'dusakabin': 2000, 'pisuvar': 1000, 'dus-teknesi': 1500, 'tezgah-alti-lavabo': 800, 'klozet': 2000,
            'asma-klozet': 2000, 'klozet-takimi': 2000, 'lavabo-bataryasi': 400, 'banyo-bataryasi': 500, 'gomme-rezervuar': 250}
NEG = r'körüklü|sifon|hortum|fırça|paspas|koku|giderici|spiral|başlığı çıkış'


def ilk_ilgili(r, s):
    for t in (r.get('en_cok_yorum10') or []):
        ad = norm(t[1] + ' ' + t[2])
        if re.search(NAMEKW.get(s, '.'), ad) and not re.search(NEG, ad) and (t[3] or 0) >= MINFIYAT.get(s, 0):
            return t
    return None


def pick(recs, s, key=None):
    c = [r for r in recs if r.get('std') == s]
    if key:
        c = [r for r in c if r.get('kategori') == key] or c
    c = [r for r in c if r.get('fiyat')]
    return max(c, key=lambda r: ((r.get('saflik') or 100) >= 60, r.get('n') or 0)) if c else None

out = []
w = out.append
w('## TABLO A1 - Hedef kategoriler: pazaryeri fiyat bandı (medyan, p25-p75; TL)\n')
w('| Kategori | Trendyol | Hepsiburada | Akakçe | Cimri |')
w('|---|---|---|---|---|')
for s in HEDEF:
    row = [AD.get(s, s)]
    for recs in (ty, hb, ak, cm):
        r = pick(recs, s)
        row.append(('† ' if (r and (r.get('saflik') or 100) < 60) else '') + (band(r['fiyat']) if r else '-'))
    w('| ' + ' | '.join(row) + ' |')
w('\nNot: † işareti, ilk 2 sayfa sonuçlarının yarıdan fazlası ilgili kategori dışında kalan ürünlerden (aksesuar, organizer vb.) oluşuyor; fiyat bandı temsil gücü sınırlı.')
w('\n## TABLO A2 - Hedef kategoriler: kategori toplamı (ürün sayısı)\n')
w('| Kategori | Trendyol | Hepsiburada | Akakçe | Cimri |')
w('|---|---|---|---|---|')
for s in HEDEF:
    row = [AD.get(s, s)]
    for recs in (ty, hb, ak, cm):
        r = pick(recs, s)
        row.append(tr(r.get('toplam')) if r and r.get('toplam') else '-')
    w('| ' + ' | '.join(row) + ' |')

w('\n## TABLO B - Hedef kategoriler: en çok yorumlu ürün (Trendyol / Hepsiburada; ilk 2 sayfa)\n')
w('| Kategori | Kanal | Ürün | Marka | Fiyat | Yorum |')
w('|---|---|---|---|---|---|')
for s in HEDEF:
    for kn, recs in (('TY', ty), ('HB', hb)):
        r = pick(recs, s)
        if r and r.get('en_cok_yorum10'):
            t = ilk_ilgili(r, s)
            if t and (r.get('saflik') or 100) >= 60:
                w(f"| {AD.get(s, s)} | {kn} | {t[2][:55]} | {t[1]} | {tr(t[3])} | {tr(t[4])} |")

w('\n## TABLO C - VitrA/Artema: okunan ürünler içindeki adet ve en iyi sıra (Trendyol, Hepsiburada, Akakçe, Cimri)\n')
w('| Kategori | TY adet / en iyi sıra | HB adet / en iyi sıra | Akakçe adet / en iyi sıra | Cimri adet |')
w('|---|---|---|---|---|')
def vs(r):
    if not r:
        return '-'
    a = r.get('vitra_adet')
    sl = r.get('vitra_siralar') or []
    d = '†' if (r.get('saflik') or 100) < 60 else ''
    return d + (f"{a} / {min(sl)}" if a and sl else (f"{a} / -" if a else '0'))
gaps = collections.defaultdict(list)
for s in HEDEF:
    row = [AD.get(s, s)]
    for nm, recs in (('TY', ty), ('HB', hb), ('AK', ak)):
        r = pick(recs, s)
        row.append(vs(r))
        if r and not r.get('vitra_adet'):
            gaps[s].append(nm)
    r = pick(cm, s)
    row.append(str(r.get('vitra_adet')) if r else '-')
    if r and not r.get('vitra_adet'):
        gaps[s].append('CM')
    w('| ' + ' | '.join(row) + ' |')
w('\nVitrA/Artema ürünü görülmeyen kesitler: ' + '; '.join(f"{AD.get(s, s)} ({', '.join(v)})" for s, v in gaps.items()))

# VitrA yorum payi TY/HB tam kayitlar
w('\n## TABLO C2 - VitrA/Artema yorum payı (yalnızca ilk 2 sayfa okunan kayıtlar)\n')
w('| Kategori | TY yorum payı | HB yorum payı |')
w('|---|---|---|')
for s in HEDEF:
    a, b = pick(ty, s), pick(hb, s)
    f = lambda r: (('† ' if (r.get('saflik') or 100) < 60 else '') + f"%{tr(r['vitra_yorum_payi'], 1)}" if r and r.get('vitra_yorum_payi') is not None else '-')
    w(f"| {AD.get(s, s)} | {f(a)} | {f(b)} |")

w('\n## TABLO D - Hedef dışı kategoriler (Trendyol / Hepsiburada): yorum toplamı, marka yoğunluğu, markasız pay, fiyat medyanı\n')
w('| Kategori | TY toplam | TY yorum (ilk 2 sf) | TY marka sayısı | TY markasız pay | TY medyan | HB toplam | HB yorum | HB marka sayısı | HB medyan | Akakçe toplam | Cimri toplam |')
w('|---|---|---|---|---|---|---|---|---|---|---|---|')
for s in HEDEF_DISI:
    t, h, a, c = pick(ty, s), pick(hb, s), pick(ak, s), pick(cm, s)
    g = lambda r, k: tr(r.get(k)) if r and r.get(k) is not None else '-'
    w(f"| {AD.get(s, s)} | {g(t,'toplam')} | {g(t,'toplam_yorum')} | {g(t,'marka_sayisi')} | {('%'+tr(t['markasiz_pay'],1)) if t and t.get('markasiz_pay') is not None else '-'} | {tr(t['fiyat']['med']) if t and t.get('fiyat') else '-'} | {g(h,'toplam')} | {g(h,'toplam_yorum')} | {g(h,'marka_sayisi')} | {tr(h['fiyat']['med']) if h and h.get('fiyat') else '-'} | {g(a,'toplam')} | {g(c,'toplam')} |")

w('\n## TABLO E - Hedef dışı: marka top 3 (adet) Trendyol / Hepsiburada\n')
for s in HEDEF_DISI:
    t, h = pick(ty, s), pick(hb, s)
    fm = lambda r: ', '.join(f"{m['ad']} {m['adet']}" for m in (r.get('marka_adet_top5') or [])[:3]) if r else '-'
    w(f"- {AD.get(s, s)}: TY [{fm(t)}]; HB [{fm(h)}]")

# saticilar
w('\n## TABLO F - Tekrar eden satıcılar\n')
tyc, hbc = collections.Counter(), collections.Counter()
tyn, hbn = collections.Counter(), collections.Counter()
for r in ty:
    for x in r.get('satici_top5') or []:
        tyc[x['ad']] += 1
        tyn[x['ad']] += x['adet']
for r in hb:
    for x in r.get('satici_top5') or []:
        hbc[x['ad']] += 1
        hbn[x['ad']] += x['adet']
w('Trendyol (ilk 5 satıcı içinde görülme sayısı / toplam ürün):')
for a, c in tyc.most_common(12):
    w(f"- {a}: {c} kategori / {tyn[a]} ürün")
w('\nHepsiburada:')
for a, c in hbc.most_common(12):
    w(f"- {a}: {c} kategori / {hbn[a]} ürün")
tp = [r['marka_magaza_payi'] for r in ty if r.get('marka_magaza_payi') is not None and r['kapsam'] == 'hedef']
hp = [r['platform_pay'] for r in hb if r.get('platform_pay') is not None and r['kapsam'] == 'hedef']
w(f"\nTY hedef kategorilerinde VitrA resmi mağaza payı (kategori başına, %): {', '.join(str(x) for x in tp)}")
w(f"HB hedef kategorilerinde Hepsiburada (platform) satış payı (kategori başına, %): {', '.join(str(x) for x in hp)}")

# rakip magazalar
w('\n## TABLO G - Rakip perakendeci ve marka mağazaları: kategori medyanı ve VitrA/Artema yeri\n')
w('| Mağaza | Kategori | Toplam | Okunan | Medyan (p25-p75) | VitrA/Artema adet | Öne çıkan markalar |')
w('|---|---|---|---|---|---|---|')
for r in mk:
    if r.get('kapsam') == 'hedef' or r.get('kapsam') == 'hedef_disi' or r.get('std') in ('canak-lavabo', 'lavabo-dolabi'):
        f = r.get('fiyat')
        w(f"| {r['magaza']} | {AD.get(r['std'], r['std'])} | {tr(r.get('toplam')) if r.get('toplam') else '-'} | {r.get('n') or '-'} | {band(f) if f else '-'} | {r.get('vitra_adet')} | {(str(r.get('marka_dagilimi') or '-'))[:70]} |")

# ---- H: VitrA fiyat konumu (magaza) ----
def pvit(m, t):
    x = t.split('|')
    try:
        if m == 'Bauhaus':
            return float(x[4])
        if m == 'Koçtaş':
            return float(x[5])
        return float(x[2])
    except Exception:
        return None
w('\n## TABLO H - Mağazalarda VitrA/Artema satırlarının medyanı / kategori medyanı (okunan liste içinde)\n')
w('| Mağaza | Kategori | VitrA/Artema medyan | Kategori medyan | Oran |')
w('|---|---|---|---|---|')
import statistics
for r in mk:
    if r.get('kapsam') != 'hedef' or not r.get('fiyat') or not r.get('vitra_urunleri'):
        continue
    v = [pvit(r['magaza'], t) for t in r['vitra_urunleri']]
    v = [x for x in v if x and x > 0]
    if len(v) >= 2:
        med = statistics.median(v)
        w(f"| {r['magaza']} | {AD.get(r['std'], r['std'])} | {tr(med)} | {tr(r['fiyat']['med'])} | {tr(med / r['fiyat']['med'], 2)}x |")

# ---- H2: marka filtresinde VitrA sirasi ----
w('\n## TABLO H2 - Marka filtresi listesinde VitrA / Artema sırası (kanal ilk 15 marka)\n')
w('| Kategori | TY | HB | Akakçe | Cimri |')
w('|---|---|---|---|---|')
kt = rd('koctas_marka.json') if os.path.exists(os.path.join(BASE, 'koctas_marka.json')) else []
def frank(lst):
    if not lst:
        return '-'
    for i, m in enumerate(lst):
        if norm(m) in ('vitra', 'artema'):
            return str(i + 1)
    return 'yok'
for s in HEDEF:
    row = [AD.get(s, s)]
    for recs, k in ((ty, 'marka_filtre'), (hb, 'marka_filtre'), (ak, 'marka_filtre_ilk15'), (cm, 'marka_filtre_ilk15')):
        r = pick(recs, s)
        row.append(frank(r.get(k)) if r else '-')
    w('| ' + ' | '.join(row) + ' |')

open(os.path.join(BASE, 'ozet_tablolar.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('ok', len(out))
