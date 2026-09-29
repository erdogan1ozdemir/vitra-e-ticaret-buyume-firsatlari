# -*- coding: utf-8 -*-
"""Kesik donen SERP'leri (ilk 20 organik yerine <13 organik sonuc) yeniden ceker; en fazla 3 deneme, en cok organik sonuc donen yanit ham/ altinda tutulur.
Ilk yanit ham_ilk/, tum yeniden denemeler ham_tekrar/ altinda saklanir."""
import sys, json, time, os, shutil
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
from serp_cek import ad
from serp_kelimeler import LISTE
S = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "serp")
for d in ("ham_ilk", "ham_tekrar"): os.makedirs(os.path.join(S, d), exist_ok=True)
def norg(j): return sum(1 for i in j["tasks"][0]["result"][0]["items"] if i["type"] == "organic")
def is_(kt):
    k, t = kt
    f = os.path.join(S, "ham", ad(k) + ".json")
    j = json.load(open(f))
    if norg(j) >= 13 or os.path.exists(os.path.join(S, "ham_ilk", ad(k) + ".json")): return k, None, None
    shutil.copy(f, os.path.join(S, "ham_ilk", ad(k) + ".json"))
    en_iyi, n_iyi = j, norg(j)
    for dn in range(1, 4):
        time.sleep(2)
        r = dfs.post("/v3/serp/google/organic/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr", "device": "mobile", "os": "android", "depth": 20, "tag": t}])
        json.dump(r, open(os.path.join(S, "ham_tekrar", "%s_%d.json" % (ad(k), dn)), "w"), ensure_ascii=False)
        n = norg(r)
        if n > n_iyi: en_iyi, n_iyi = r, n
        if n >= 15: break
    json.dump(en_iyi, open(f, "w"), ensure_ascii=False)
    return k, norg(j), n_iyi
if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex:
        for x in ex.map(is_, LISTE):
            if x[1] is not None: print(x)
