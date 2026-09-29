# -*- coding: utf-8 -*-
"""Tamamlayici: DataForSEO Google SERP (TR, konum 2792, dil tr) ile site:sikayetvar.com sorgulari.
Amac: (1) marka sayfasi adreslerini dogrulamak, (2) tema bazli sikayet basliklari toplamak. Cikti: veri/ham/derin/sikayetvar/serp.json"""
import sys, json, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dfs
CIKTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
Q = ["vitra klozet", "vitra yedek parça", "vitra montaj", "vitra yetkili servis", "vitra trendyol", "vitra hepsiburada",
     "vitra online iade", "vitra sipariş teslimat", "artema", "vitra kampanya fiyat", "vitra bayi mağaza",
     "serel", "serel seramik", "vitra çağrı merkezi", "vitra banyo dolabı"]
if __name__ == "__main__":
    out = []; maliyet = 0
    for q in Q:
        g = {"keyword": "site:sikayetvar.com " + q, "location_code": 2792, "language_code": "tr", "device": "desktop", "depth": 30}
        r = dfs.post("/v3/serp/google/organic/live/regular", [g])
        maliyet += r.get("cost", 0)
        t = r["tasks"][0]
        items = (t.get("result") or [{}])[0].get("items") or []
        for it in items:
            if it.get("type") == "organic":
                out.append({"sorgu": q, "sira": it.get("rank_absolute"), "url": it.get("url"), "baslik": it.get("title"), "aciklama": it.get("description")})
        print(q, t["status_code"], len(items), flush=True); time.sleep(0.7)
    json.dump({"maliyet_usd": round(maliyet, 4), "sonuclar": out}, open(os.path.join(CIKTI, "serp.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("maliyet", round(maliyet, 4), "sonuc", len(out))
