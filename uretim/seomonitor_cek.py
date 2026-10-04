# -*- coding: utf-8 -*-
"""SEOmonitor (vitra.com.tr, kampanya 324384) takip edilen tum kelimeler: hacim, sira, SERP ozellikleri, AI Overview durumu.
Anahtar $SEOMONITOR_API_KEY ortam degiskeninden okunur ve hicbir ciktiya yazilmaz. Cikti: veri/ham/seomonitor/kelimeler_2026-10-03.json"""
import os, json, subprocess, time
import veri
KEY = os.environ["SEOMONITOR_API_KEY"]; B = "https://apigw.seomonitor.com/v3"
def get(path):
    r = subprocess.run(["curl", "-s", "--max-time", "120", "-H", "Authorization: " + KEY, "-H", "Accept: application/json", B + path], capture_output=True)
    return json.loads(r.stdout.decode("utf-8"))
out, off = [], 0
while True:
    d = get("/rank-tracker/v3.0/keywords?campaign_id=324384&group_id=0&start_date=2026-09-27&end_date=2026-10-03&limit=100&offset=%d" % off)
    rows = d if isinstance(d, list) else d.get("data") or d.get("keywords") or []
    if not rows: break
    out += rows; off += 100; time.sleep(0.4)
    if len(rows) < 100: break
json.dump(out, open(os.path.join(veri.V, "ham", "seomonitor", "kelimeler_2026-10-03.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(len(out))
