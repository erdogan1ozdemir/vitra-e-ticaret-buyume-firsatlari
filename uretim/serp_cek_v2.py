# -*- coding: utf-8 -*-
"""Genisletilmis set (set_v2.json) icin Google TR mobil SERP · ilk 20 organik + SERP ozellikleri; AI Overview cikanlar load_async_ai_overview ile yeniden cekilir.
Cikti: veri/ham/derin/serp/ham_v2/, ham_ai_v2/ (kelime basina bir JSON)."""
import sys, json, time, os
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
from serp_cek import ad
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "serp")
SET = json.load(open(os.path.join(B, "set_v2.json"), encoding="utf-8"))["kelimeler"]
def cek(kw, klasor, ai=False):
    os.makedirs(os.path.join(B, klasor), exist_ok=True)
    d = os.path.join(B, klasor, ad(kw) + ".json")
    if os.path.exists(d): return kw, 0, "var"
    g = {"keyword": kw, "location_code": 2792, "language_code": "tr", "device": "mobile", "os": "android", "depth": 20}
    if ai: g["load_async_ai_overview"] = True
    for dene in range(3):
        try:
            r = dfs.post("/v3/serp/google/organic/live/advanced", [g]); break
        except Exception as e:
            time.sleep(3); r = {"tasks": [{"status_code": -1, "status_message": str(e)}]}
    if r["tasks"][0].get("status_code") == 20000: json.dump(r, open(d, "w"), ensure_ascii=False)
    time.sleep(0.5)
    return kw, r.get("cost", 0) or 0, r["tasks"][0].get("status_code")
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].startswith("ham_v2"):   # ek gozlem turu (ayni gun, ayni parametre): ham_v2b, ham_v2c
        L = [s["kw"] for s in SET]
        with ThreadPoolExecutor(12) as ex: s1 = list(ex.map(lambda k: cek(k, sys.argv[1]), L))
        print(sys.argv[1], len(s1), "hatali", [s for s in s1 if s[2] not in (20000, "var")][:10], "maliyet", round(sum(s[1] for s in s1), 4)); sys.exit(0)
    L = [s["kw"] for s in SET][: int(sys.argv[1]) if len(sys.argv) > 1 else None]
    with ThreadPoolExecutor(12) as ex: s1 = list(ex.map(lambda k: cek(k, "ham_v2"), L))
    ai = []
    for k in L:
        f = os.path.join(B, "ham_v2", ad(k) + ".json")
        if os.path.exists(f):
            res = json.load(open(f))["tasks"][0]["result"][0]
            if any(i["type"] == "ai_overview" for i in (res.get("items") or [])): ai.append(k)
    with ThreadPoolExecutor(12) as ex: s2 = list(ex.map(lambda k: cek(k, "ham_ai_v2", True), ai))
    print("serp", len(s1), "hatali", [s for s in s1 if s[2] not in (20000, "var")][:10], "maliyet", round(sum(s[1] for s in s1), 4))
    print("ai", len(s2), "hatali", [s for s in s2 if s[2] not in (20000, "var")][:10], "maliyet", round(sum(s[1] for s in s2), 4))
