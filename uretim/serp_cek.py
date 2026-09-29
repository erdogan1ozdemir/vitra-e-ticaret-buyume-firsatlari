# -*- coding: utf-8 -*-
"""Google TR mobil SERP · DataForSEO live/advanced (canli uc nokta tek gorev kabul eder) · kelime basina bir ham JSON."""
import sys, json, time, os, re
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
from serp_kelimeler import LISTE
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "serp", "ham")
os.makedirs(OUT, exist_ok=True)
def ad(k): return re.sub(r"[^0-9a-zA-Z]+", "_", k.replace("ı","i").replace("ş","s").replace("ç","c").replace("ğ","g").replace("ö","o").replace("ü","u").replace("İ","I")).strip("_")
def is_(kt):
    k, t = kt
    d = os.path.join(OUT, ad(k) + ".json")
    if os.path.exists(d): return k, 0, "var"
    g = {"keyword": k, "location_code": 2792, "language_code": "tr", "device": "mobile", "os": "android", "depth": 20, "tag": t}
    r = dfs.post("/v3/serp/google/organic/live/advanced", [g])
    json.dump(r, open(d, "w"), ensure_ascii=False)
    time.sleep(0.7)
    return k, r.get("cost", 0), r["tasks"][0]["status_code"]
if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex:
        sonuc = list(ex.map(is_, LISTE))
    print("hatali:", [s for s in sonuc if s[2] not in (20000, "var")])
    print("toplam maliyet", round(sum(s[1] for s in sonuc), 4), "gorev", len(sonuc))
