# -*- coding: utf-8 -*-
"""AI Overview iceren kelimeleri load_async_ai_overview=true ile yeniden ceker (referans alan adlari icin)."""
import sys, json, time, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
from serp_cek import ad
BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "serp")
OUT = os.path.join(BASE, "ham_ai"); os.makedirs(OUT, exist_ok=True)
def kelimeler():
    r = []
    for f in sorted(os.listdir(os.path.join(BASE, "ham"))):
        j = json.load(open(os.path.join(BASE, "ham", f)))
        res = j["tasks"][0]["result"][0]
        if any(i["type"] == "ai_overview" for i in res["items"]):
            r.append((res["keyword"], j["tasks"][0]["data"]["tag"]))
    return r
def is_(kt):
    k, t = kt
    d = os.path.join(OUT, ad(k) + ".json")
    if os.path.exists(d): return k, 0, "var"
    g = {"keyword": k, "location_code": 2792, "language_code": "tr", "device": "mobile", "os": "android", "depth": 20,
         "tag": t, "load_async_ai_overview": True}
    r = dfs.post("/v3/serp/google/organic/live/advanced", [g])
    json.dump(r, open(d, "w"), ensure_ascii=False)
    time.sleep(0.7)
    return k, r.get("cost", 0), r["tasks"][0]["status_code"]
if __name__ == "__main__":
    L = kelimeler()
    with ThreadPoolExecutor(3) as ex:
        sonuc = list(ex.map(is_, L))
    print("hatali:", [s for s in sonuc if s[2] not in (20000, "var")])
    print("toplam maliyet", round(sum(s[1] for s in sonuc), 4), "gorev", len(sonuc))
