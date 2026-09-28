# -*- coding: utf-8 -*-
"""Bos donen autocomplete tohumlarini tek tek, tekrar denemeli ceker."""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__)); import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); F = os.path.join(P, "veri/ham/autocomplete_youtube.json")
d = json.load(open(F, encoding="utf-8"))
bos = [k for k, v in d["autocomplete"].items() if not v]
for k in bos:
    for deneme in range(3):
        try:
            r = dfs.post("/v3/serp/google/autocomplete/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr", "client": "chrome", "cursor_pointer": len(k)}])
            t = r["tasks"][0]; res = (t.get("result") or [{}])[0]
            s = [it.get("suggestion") for it in (res.get("items") or []) if it.get("type") == "autocomplete"]
            if s: d["autocomplete"][k] = s; break
            time.sleep(2)
        except Exception as e:
            print("hata", k, e); time.sleep(3)
    print(k, len(d["autocomplete"][k]))
json.dump(d, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("dolu:", sum(1 for v in d["autocomplete"].values() if v), "/", len(d["autocomplete"]))
