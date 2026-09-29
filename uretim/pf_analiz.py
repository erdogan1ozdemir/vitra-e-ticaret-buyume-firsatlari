#!/usr/bin/env python3
"""Çok satan ve VitrA kanal fiyatı çıktılarından özet sayıları hesaplar (analiz.json). ozet.md bu sayılara dayanır."""
import json, statistics
from pathlib import Path
from collections import Counter, defaultdict

D = Path(__file__).resolve().parent.parent / 'veri/ham/derin/pazaryeri_fiyat'
oz = json.load(open(D / 'cok_satan_ozet.json'))
uf = json.load(open(D / 'urun_fiyat.json'))
tum = json.load(open(D / 'urun_fiyat_tum_adaylar.json'))

# VitrA fiyat endeksi: vitra.com.tr liste fiyat medyanı / kategori çok satan medyanı
ENDEKS = {
    'klozet': ['7041B003-0090', '5618L003-0850', '7748B003-0559', '5505L003-0868'],
    'lavabo': ['5473B003-0618', '5501L003-0001'],
    'banyo_dolabi': ['60785', '67093', '75102', '60812', '66166', '60848'],
    'lavabo_bataryasi': ['A42484', 'A43715', 'A42923'],
    'banyo_bataryasi': ['A43057', 'A41994'],
    'klozet_kapagi': ['121-003-909', '109-003-909', '84-003-009'],
    'rezervuar_ic_takim': ['330B1314'],
    'taharet_musluk': ['A45200', 'A45228'],
    'dus_seti': ['A49321'],
}
byk = {r['kod']: r for r in tum}
endeks = {}
for k, kodlar in ENDEKS.items():
    fiy = [byk[c]['vitra_com_tr'] for c in kodlar if c in byk and byk[c]['vitra_com_tr']]
    med = statistics.median(fiy)
    endeks[k] = {'urun_sayisi': len(fiy), 'vitra_com_tr_medyan': round(med), 'ty_medyan': oz['ty'][k]['medyan_fiyat'], 'hb_medyan': oz['hb'][k]['medyan_fiyat'],
                 'ty_kat': round(med / oz['ty'][k]['medyan_fiyat'], 1), 'hb_kat': round(med / oz['hb'][k]['medyan_fiyat'], 1)}

# satıcı yapısı (36'lık listeler toplamı)
yapi = {}
for kanal in ('ty', 'hb'):
    c = Counter()
    for a, v in oz[kanal].items():
        for t, n in v['satici_tipi'].items():
            c[t] += n
    yapi[kanal] = dict(c)

u = uf
has = lambda x, k: x.get(k) is not None
o2 = {'urun': len(u)}
o2['ty_eslesen'] = sum(1 for x in u if has(x, 'ty_vitra_magazasi') or has(x, 'ty_en_dusuk_3p'))
o2['hb_eslesen'] = sum(1 for x in u if has(x, 'hb_buybox'))
o2['kt_eslesen'] = sum(1 for x in u if has(x, 'koctas'))
o2['ty_vitra_magazasi_var'] = sum(1 for x in u if has(x, 'ty_vitra_magazasi'))
o2['ty_3p_var'] = sum(1 for x in u if has(x, 'ty_en_dusuk_3p'))
o2['ty_hem_magaza_hem_3p'] = sum(1 for x in u if has(x, 'ty_vitra_magazasi') and has(x, 'ty_en_dusuk_3p'))
o2['ty_3p_magazadan_dusuk'] = sum(1 for x in u if x.get('ty_3p_resmi_altinda'))
o2['ty_3p_vitracom_dan_dusuk'] = sum(1 for x in u if x.get('ty_3p_vitracom_altinda'))
o2['hb_vitracom_dan_dusuk'] = sum(1 for x in u if has(x, 'hb_buybox') and x['hb_buybox'] < x['vitra_com_tr'])
o2['kt_vitracom_dan_dusuk'] = sum(1 for x in u if has(x, 'koctas') and x['koctas'] < x['vitra_com_tr'])
o2['pazaryeri_herhangi_dusuk'] = sum(1 for x in u if x['kanal_sayisi'] > 1 and x['en_ucuz_kanal'] != 'vitra.com.tr')
o2['pazaryeri_fiyati_olan'] = sum(1 for x in u if x['kanal_sayisi'] > 1)
farklar = [x['fark_yuzde'] for x in u if x['kanal_sayisi'] > 1 and x['fark_yuzde'] is not None]
o2['fark_medyan_tum'] = round(statistics.median(farklar), 1)
poz = [x['fark_yuzde'] for x in u if x['kanal_sayisi'] > 1 and x['fark_yuzde'] and x['fark_yuzde'] > 0]
o2['fark_pozitif_n'] = len(poz)
o2['fark_pozitif_medyan'] = round(statistics.median(poz), 1) if poz else None
o2['fark_pozitif_min'] = min(poz) if poz else None
o2['fark_pozitif_maks'] = max(poz) if poz else None
if len(poz) >= 4:
    q = statistics.quantiles(poz, n=4)
    o2['fark_pozitif_ceyrek'] = [round(q[0], 1), round(q[2], 1)]
ef = [x['fark_efektif_yuzde'] for x in u if x['kanal_sayisi'] > 1 and x.get('fark_efektif_yuzde') is not None]
efp = [v for v in ef if v > 0]
o2['efektif_fark_pozitif_n'] = len(efp)
o2['efektif_fark_pozitif_medyan'] = round(statistics.median(efp), 1) if efp else None
o2['efektif_fark_pozitif_min'] = min(efp) if efp else None
o2['efektif_fark_pozitif_maks'] = max(efp) if efp else None
o2['en_ucuz_kanal_dagilimi'] = dict(Counter(x['en_ucuz_kanal'].split(' (')[0] for x in u if x['kanal_sayisi'] > 1))
o2['en_ucuz_kanal_efektif_dagilimi'] = dict(Counter(x['en_ucuz_kanal_efektif'] for x in u if x['kanal_sayisi'] > 1 and x.get('en_ucuz_kanal_efektif')))
gaplar = [(x['ty_vitra_magazasi'] - x['ty_en_dusuk_3p']) / x['ty_vitra_magazasi'] * 100 for x in u if x.get('ty_3p_resmi_altinda')]
o2['ty_magaza_3p_fark'] = [round(min(gaplar), 1), round(statistics.median(gaplar), 1), round(max(gaplar), 1), len(gaplar)] if gaplar else None
g3 = [(x['vitra_com_tr'] - x['ty_en_dusuk_3p']) / x['vitra_com_tr'] * 100 for x in u if x.get('ty_en_dusuk_3p')]
o2['ty_3p_vitracom_fark'] = [round(min(g3), 1), round(statistics.median(g3), 1), round(max(g3), 1), len(g3)]
gh = [(x['vitra_com_tr'] - x['hb_buybox']) / x['vitra_com_tr'] * 100 for x in u if x.get('hb_buybox')]
o2['hb_vitracom_fark'] = [round(min(gh), 1), round(statistics.median(gh), 1), round(max(gh), 1), len(gh)]
def alti(anahtar):
    v = [(x['vitra_com_tr'] - x[anahtar]) / x['vitra_com_tr'] * 100 for x in u if x.get(anahtar) and x[anahtar] < x['vitra_com_tr']]
    return [len(v), round(statistics.median(v), 1) if v else None, round(min(v), 1) if v else None, round(max(v), 1) if v else None]
o2['ty_alti'] = alti('ty_en_dusuk_3p')
o2['hb_alti'] = alti('hb_buybox')
o2['kt_alti'] = alti('koctas')
gk = [(x['vitra_com_tr'] - x['koctas']) / x['vitra_com_tr'] * 100 for x in u if x.get('koctas')]
o2['kt_vitracom_fark'] = [round(min(gk), 1), round(statistics.median(gk), 1), round(max(gk), 1), len(gk)]
hbs = Counter()
for x in u:
    if x.get('hb_satici'):
        s = x['hb_satici'].strip().lower()
        hbs['VitrA mağazası' if s == 'vitra' else 'Hepsiburada' if s == 'hepsiburada' else '3P'] += 1
o2['hb_buybox_satici'] = dict(hbs)
o2['koctas_satici'] = dict(Counter((x.get('koctas_satici') or '-') for x in u if x.get('koctas')))
grp = defaultdict(list)
for x in u:
    if x['kanal_sayisi'] > 1 and x.get('fark_yuzde') is not None:
        grp[x['grup'].split(' (')[0]].append(x['fark_yuzde'])
o2['grup_fark_medyan'] = {g: [len(v), round(statistics.median(v), 1)] for g, v in grp.items()}
o2['vitra_stokta_yok'] = sum(1 for x in u if x['vitra_stok'] == 'stokta yok')
o2['vitra_ucretsiz_montaj_etiketi'] = sum(1 for x in u if x['vitra_montaj'].startswith('Ücretsiz'))
o2['vitra_sepette_indirim_dagilimi'] = dict(Counter(x['vitra_sepette_indirim'] for x in u))
# vitra.com.tr liste fiyatı ile TY VitrA mağazası ve HB VitrA mağazası aynı mı
o2['ty_magaza_liste_esit'] = sum(1 for x in u if has(x, 'ty_vitra_magazasi') and abs(x['ty_vitra_magazasi'] - x['vitra_com_tr']) < 1)
o2['hb_vitra_liste_esit'] = sum(1 for x in u if (x.get('hb_satici') or '').strip().lower() == 'vitra' and abs(x['hb_buybox'] - x['vitra_com_tr']) < 1)
out = {'endeks': endeks, 'satici_yapisi': yapi, 'kanal_fiyat': o2}
json.dump(out, open(D / 'analiz.json', 'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
