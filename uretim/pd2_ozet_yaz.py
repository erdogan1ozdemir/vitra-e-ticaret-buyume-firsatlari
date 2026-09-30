# ozet.md = pd2_ozet_metin.md (sablon) + pd2_ozet.py tablolari + yontem blogu
import json, os, re, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(here, '..', 'veri', 'ham', 'derin', 'pazaryeri_derin2')
subprocess.run([sys.executable, os.path.join(here, 'pd2_ozet.py')], check=True, stdout=subprocess.DEVNULL)
t = json.load(open(os.path.join(BASE, '_ham', 'ozet_tablolar.json'), encoding='utf-8'))
m = open(os.path.join(here, 'pd2_ozet_metin.md'), encoding='utf-8').read()
y = open(os.path.join(here, 'pd2_ozet_yontem.md'), encoding='utf-8').read().strip()
for k, v in (('{YONTEM}', y), ('{ANA}', t['ana']), ('{MAGAZA}', t['magaza']), ('{VSITE}', t['vsite']), ('{OZEL}', t['ozel'])):
    m = m.replace(k, v)
open(os.path.join(BASE, 'ozet.md'), 'w', encoding='utf-8').write(m)
print(len(m))
