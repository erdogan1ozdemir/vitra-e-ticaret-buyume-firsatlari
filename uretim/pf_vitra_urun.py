#!/usr/bin/env python3
"""VitrA ürün sitemap'inden aday SKU'ları seçer, vitra.com.tr ürün sayfasından fiyat/montaj/taksit bilgisini okur.

Çıktı: veri/ham/derin/pazaryeri_fiyat/urun/vitra_com_tr.json
Yavaş tempo: sayfa başına tek istek, istekler arası 2-4 sn.
"""
import json, re, time, random, html, subprocess, sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
SITEMAP = KOK / 'veri/ham/sitemap/vitra-products.xml'
CIKTI = KOK / 'veri/ham/derin/pazaryeri_fiyat/urun/vitra_com_tr.json'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36'

# (kod, grup, seri/not)  - kod sitemap adresindeki p-<kod> ile eşleşir (büyük/küçük harf duyarsız)
ADAYLAR = [
    ('7041B003-0090', 'Asma klozet', 'Integra'),
    ('5618L003-0850', 'Asma klozet', 'S50'),
    ('7748B003-0559', 'Asma klozet', 'Sento'),
    ('5505L003-0868', 'Asma klozet', 'S20'),
    ('7783L003-0092', 'Klozet (takım)', 'Zentrum'),
    ('9888B003-7201', 'Klozet (takım)', 'S55'),
    ('5987B003-0092', 'Klozet (takım)', 'Sento'),
    ('7703L003-0092', 'Klozet (takım)', 'S20 Round'),
    ('5473B003-0618', 'Lavabo', 'S20 tezgahaltı'),
    ('5501L003-0001', 'Lavabo', 'S20'),
    ('7065L003-0001', 'Lavabo', 'Integra'),
    ('58195', 'Banyo mobilyası (lavabo dolabı)', 'Metropole'),
    ('60812', 'Banyo mobilyası (lavabo dolabı)', 'Sento'),
    ('60785', 'Banyo mobilyası (lavabo dolabı)', 'Sento'),
    ('60848', 'Banyo mobilyası (boy dolabı)', 'Sento'),
    ('66166', 'Banyo mobilyası (boy dolabı)', 'Mia'),
    ('67093', 'Banyo mobilyası (lavabo dolabı)', 'Mia'),
    ('75102', 'Banyo mobilyası (lavabo dolabı)', 'Mia'),
    ('61364', 'Banyo mobilyası (çamaşır makinesi ünitesi)', 'Sento'),
    ('A42484', 'Armatür (lavabo bataryası)', 'Artema Solid S'),
    ('A43715', 'Armatür (lavabo bataryası)', 'Artema Shift T10'),
    ('A42722', 'Armatür (lavabo bataryası)', 'Artema Root Round'),
    ('A42923', 'Armatür (lavabo bataryası)', 'Artema Flow Round'),
    ('A43057', 'Armatür (banyo bataryası)', 'Artema Flow Round'),
    ('A41994', 'Armatür (banyo bataryası)', 'Artema Minimax S'),
    ('A47055EXPS', 'Armatür (termostatik batarya)', 'Artema AquaHeat'),
    ('A45200', 'Armatür (ara musluk)', 'Artema'),
    ('A45228', 'Armatür (çamaşır musluğu)', 'Artema'),
    ('A49321', 'Duş seti', 'Artema Flow Round ankastre'),
    ('A49324', 'Duş seti', 'Artema Minimax Round ankastre'),
    ('A47295', 'Duş seti', 'Artema Joy duş sistemi'),
    ('800-1896', 'Gömme rezervuar seti', 'V8'),
    ('800-2025', 'Gömme rezervuar seti', 'V8'),
    ('768-1851-01', 'Gömme rezervuar seti', 'V-Fix Prime 8 cm'),
    ('121-003-909', 'Klozet kapağı', 'Universal'),
    ('109-003-909', 'Klozet kapağı', 'Universal / S20'),
    ('84-003-009', 'Klozet kapağı', 'Universal'),
    ('330B1314', 'İç takım', 'Rezervuar iç takımı'),
    ('330B1510', 'İç takım', 'Rezervuar iç takımı'),
]


def url_bul(kod, urls):
    k = kod.lower()
    bulunan = [u for u in urls if re.search(r'-p-' + re.escape(k) + r'(\b|$)', u.lower())]
    return bulunan[0] if bulunan else None


def indir(url):
    r = subprocess.run(['curl', '-s', '-m', '40', '-A', UA, '-w', '\n%{http_code}', url], capture_output=True)
    body = r.stdout.decode('utf-8', 'replace')
    govde, _, kod = body.rpartition('\n')
    return int(kod or 0), govde


def sayi(s):
    s = s.replace('.', '').replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def ayikla(h):
    o = {}
    m = re.search(r'"@type":\s*"Product".*?</script>', h, re.S)
    blok = m.group(0) if m else ''
    for anahtar, desen in (('ad', r'"name":\s*"([^"]+)"'), ('kategori', r'"category":\s*"([^"]+)"'),
                           ('sku', r'"sku":\s*"([^"]+)"'), ('fiyat_ld', r'"price":\s*([0-9.]+)'),
                           ('stok', r'schema.org/(InStock|OutOfStock|PreOrder|LimitedAvailability)')):
        mm = re.search(desen, blok)
        o[anahtar] = mm.group(1) if mm else None
    o['fiyat_ld'] = float(o['fiyat_ld']) if o.get('fiyat_ld') else None
    metin = re.sub(r'<script.*?</script>|<style.*?</style>', '', h, flags=re.S)
    metin = html.unescape(re.sub(r'<[^>]+>', '\n', metin))
    satir = [x.strip() for x in metin.split('\n') if x.strip()]
    # ana ürün bloğu: ilk "Ürün Kodu:" ile "Benzer ürünler" arası
    try:
        bas = satir.index('Ürün Kodu:')
    except ValueError:
        bas = 0
    try:
        bit = satir.index('Benzer ürünler')
    except ValueError:
        bit = len(satir)
    blok_s = satir[bas:bit]
    o['sepette_indirim_yuzde'] = None
    o['sepette_fiyat'] = None
    o['liste_fiyat'] = None
    for i, l in enumerate(blok_s):
        if o['liste_fiyat'] is None and re.fullmatch(r'[0-9.]+(,[0-9]+)?', l) and i + 1 < len(blok_s) and blok_s[i + 1] == 'TL':
            o['liste_fiyat'] = sayi(l)
        mm = re.match(r'Sepette\s*%\s*(\d+)\s*indirim', l)
        if mm and o['sepette_indirim_yuzde'] is None:
            o['sepette_indirim_yuzde'] = int(mm.group(1))
            if i + 2 < len(blok_s) and blok_s[i + 2] == 'TL':
                o['sepette_fiyat'] = sayi(blok_s[i + 1])
    ust = ' | '.join(blok_s[:60])
    o['ucretsiz_montaj'] = 'Ücretsiz Montaj' in ust
    o['montaj_hizmeti_secenegi'] = 'Montaj Ekle' in metin or 'montaj hizmetinden faydalanmak' in metin
    o['ucretsiz_kargo'] = 'Ücretsiz kargo' in ust
    o['taksit_notu'] = next((l for l in satir[:12] if 'taksit' in l.lower()), None)
    mm = re.search(r'Brüt Liste Fiyatı\n?([^\n]+)', metin)
    o['brut_liste'] = None
    for i, l in enumerate(satir):
        if l == 'Brüt Liste Fiyatı' and i + 1 < len(satir):
            o['brut_liste'] = satir[i + 1]
            break
    return o


def main():
    urls = re.findall(r'<loc>(.*?)</loc>', SITEMAP.read_text())
    sonuc, yok = [], []
    for kod, grup, seri in ADAYLAR:
        u = url_bul(kod, urls)
        if not u:
            yok.append(kod)
            print('sitemap yok', kod, file=sys.stderr)
            continue
        time.sleep(random.uniform(2, 4))
        st, h = indir(u)
        if st != 200:
            print('HTTP', st, kod, file=sys.stderr)
            yok.append(kod)
            continue
        o = ayikla(h)
        o.update({'kod': kod, 'grup': grup, 'seri': seri, 'url': u, 'ts': time.strftime('%Y-%m-%dT%H:%M:%S')})
        sonuc.append(o)
        print(kod, o['ad'], o['liste_fiyat'], o['sepette_indirim_yuzde'], o['sepette_fiyat'], o['stok'], o['ucretsiz_montaj'])
    CIKTI.parent.mkdir(parents=True, exist_ok=True)
    CIKTI.write_text(json.dumps({'urunler': sonuc, 'bulunamayan': yok}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
