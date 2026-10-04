# -*- coding: utf-8 -*-
"""SEOmonitor share of clicks (mobil): tum kelimeler (son 15 gun ve gecen yil ayni donem) ve ana kategori klasorleri. Anahtar ortamdan okunur."""
import os, json, subprocess, time
import veri
KEY = os.environ["SEOMONITOR_API_KEY"]; B = "https://apigw.seomonitor.com/v3/rank-tracker/v3.0/daily-share-of-clicks"
GR = {"Tümü": None, "Vitrifiyeler": 582638, "Banyo Mobilyaları": 582499, "Armatürler": 582219, "Duşlar": 582535, "Yıkanma Alanları": 582658, "Rezervuarlar": 582605,
      "Banyo Aksesuarları": 582488, "Karo Seramik Ürünleri": 582594, "Marka": -1}
def get(s, e, g=None):
    u = B + "?campaign_id=324384&device=mobile&start_date=%s&end_date=%s" % (s, e) + ("&group_id=%d" % g if g is not None else "")
    r = subprocess.run(["curl", "-s", "--max-time", "120", "-H", "Authorization: " + KEY, "-H", "Accept: application/json", u], capture_output=True)
    return json.loads(r.stdout.decode("utf-8"))
out = {"donem": ["2026-09-19", "2026-10-03"], "onceki": ["2025-09-19", "2025-10-03"], "grup": {}}
for ad, g in GR.items():
    out["grup"][ad] = get("2026-09-19", "2026-10-03", g); time.sleep(0.5)
out["tum_onceki"] = get("2025-09-19", "2025-10-03")
json.dump(out, open(os.path.join(veri.V, "ham", "seomonitor", "share_of_clicks.json"), "w", encoding="utf-8"), ensure_ascii=False)
for ad, d in out["grup"].items():
    if not isinstance(d, list) or not d: print(ad, "VERI YOK", str(d)[:120]); continue
    son = d[-1]["domains"]; v = next((x["share_of_clicks"] for x in son if x["domain"] == "vitra.com.tr"), None)
    print(ad, len(d), "vitra", v, [(x["domain"], x["share_of_clicks"]) for x in son[:3]])
d = out["tum_onceki"]; print("onceki", len(d) if isinstance(d, list) else str(d)[:100])
if isinstance(d, list) and d: print([(x["domain"], x["share_of_clicks"]) for x in d[-1]["domains"][:5]], next((x["share_of_clicks"] for x in d[-1]["domains"] if x["domain"]=="vitra.com.tr"),None))
