# Tarayici sekmesinden buyuk cikti olarak kaydedilen sonucu (@@BEGIN@@ ... @@END@@) _ham/<kanal>.json dosyasina ayirir.
import json, sys, os
src, kanal = sys.argv[1], sys.argv[2]
t = open(src, encoding='utf-8').read()
i = t.index('@@BEGIN@@') + len('@@BEGIN@@'); j = t.index('@@END@@')
raw = t[i:j]
# aracin dis kaplamasi (JSON-kacisli metin) varsa ac
try:
    d = json.loads(raw)
except Exception:
    d = json.loads(json.loads('"' + raw + '"'))
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'veri', 'ham', 'derin', 'pazaryeri_derin2', '_ham')
os.makedirs(D, exist_ok=True)
json.dump(d, open(os.path.join(D, kanal + '.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print(kanal, len(d), 'kesit')
