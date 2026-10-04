# -*- coding: utf-8 -*-
"""SERP setindeki (set_v2) SEOmonitor takibindeki kelimeler icin 03.10.2026 mobil ilk 100 sonuc.
Cikti: veri/ham/seomonitor/top_results_2026-10-03.json"""
import json, os, urllib.request, urllib.parse, time, ssl, certifi
_CTX = ssl.create_default_context(cafile=certifi.where())
V = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veri")
SM = {k["keyword"]: k["keyword_id"] for k in json.load(open(os.path.join(V, "ham/seomonitor/kelimeler_2026-10-03.json"), encoding="utf-8"))}
SET = [s["kw"] for s in json.load(open(os.path.join(V, "ham/derin/serp/set_v2.json"), encoding="utf-8"))["kelimeler"]]
ids = [SM[k] for k in SET if k in SM]
print("takipte", len(ids), "/", len(SET))
KEY = os.environ["SEOMONITOR_API_KEY"]; out = []
for i in range(0, len(ids), 25):
    q = urllib.parse.urlencode({"campaign_id": 324384, "date": "2026-10-03", "device": "mobile", "keyword_ids": ",".join(map(str, ids[i:i + 25]))})
    rq = urllib.request.Request("https://apigw.seomonitor.com/v3/rank-tracker/v3.0/keywords/top-results?" + q, headers={"Authorization": KEY})
    for dene in range(3):
        try:
            out += json.load(urllib.request.urlopen(rq, timeout=90, context=_CTX)); break
        except Exception as e:
            print("hata", e); time.sleep(5)
for r in out:   # yalnizca ilk 20 sonuc saklanir
    r["top_100_results"] = [{k_: x.get(k_) for k_ in ("domain", "rank", "landing_page", "title")} for x in r["top_100_results"] if x.get("rank") and x["rank"] <= 20]
json.dump({"tarih": "2026-10-03", "cihaz": "mobile", "kelimeler": out}, open(os.path.join(V, "ham/seomonitor/top_results_2026-10-03.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("kaydedildi", len(out), sum(1 for r in out if r["top_100_results"]))
