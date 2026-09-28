# -*- coding: utf-8 -*-
"""Google autocomplete ve YouTube arama sonuclari · TR · DataForSEO."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__)); import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(P, "veri/ham"); os.makedirs(OUT, exist_ok=True)
AUTO = ["vitra", "vitra klozet", "vitra lavabo", "vitra banyo dolabı", "vitra batarya", "vitra gömme rezervuar", "vitra gömme", "vitra duşakabin", "vitra küvet",
        "vitra akıllı klozet", "vitra rezervuar", "vitra klozet kapağı", "vitra servis", "vitra yedek parça", "vitra bayi", "vitra taksit", "vitra indirim", "vitra outlet",
        "klozet", "asma klozet", "akıllı klozet", "lavabo", "banyo dolabı", "banyo bataryası", "lavabo bataryası", "duş seti", "duşakabin", "küvet", "gömme rezervuar",
        "klozet kapağı", "banyo aksesuar", "banyo seti", "banyo takımı", "banyo yenileme", "banyo tadilat", "klozet fiyat", "banyo dolabı fiyat", "klozet montaj", "gömme rezervuar tamir",
        "klozet tamir", "lavabo tıkanıklığı", "banyo dolabı montaj", "klozet taksit", "banyo dolabı taksit", "artema", "artema batarya", "creavit klozet", "kale klozet", "ece klozet"]
YT = ["vitra klozet", "vitra gömme rezervuar", "vitra gömme klozet su kaçırıyor", "vitra rezervuar tamiri", "vitra banyo dolabı montajı", "vitra akıllı klozet", "vitra v care", "vitra lavabo",
      "klozet montajı nasıl yapılır", "asma klozet montajı", "gömme rezervuar montajı", "gömme rezervuar tamiri", "klozet kapağı montajı", "klozet kapağı nasıl değiştirilir", "lavabo bataryası montajı",
      "banyo bataryası nasıl takılır", "banyo dolabı montajı", "duşakabin montajı", "duş seti montajı", "rezervuar su kaçırıyor", "klozet su kaçırıyor", "klozet tıkanıklığı nasıl açılır",
      "banyo yenileme", "banyo tadilatı", "küçük banyo dekorasyonu", "akıllı klozet inceleme", "en iyi klozet markası", "banyo dolabı tavsiye", "banyo dolabı inceleme", "klozet alırken nelere dikkat"]
def top(path, gorevler):
    return dfs.post(path, gorevler)
out = {"autocomplete": {}, "youtube": {}}
for i in range(0, len(AUTO), 20):
    r = top("/v3/serp/google/autocomplete/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr", "client": "chrome"} for k in AUTO[i:i+20]])
    for t in r["tasks"]:
        k = t["data"]["keyword"]; res = (t.get("result") or [{}])[0]
        out["autocomplete"][k] = [it.get("suggestion") for it in (res.get("items") or []) if it.get("type") == "autocomplete"]
    print("auto", i, r["tasks"][0]["status_message"])
for i in range(0, len(YT), 10):
    r = top("/v3/serp/youtube/organic/live/advanced", [{"keyword": k, "location_code": 2792, "language_code": "tr"} for k in YT[i:i+10]])
    for t in r["tasks"]:
        k = t["data"]["keyword"]; res = (t.get("result") or [{}])[0]
        out["youtube"][k] = [{"baslik": it.get("title"), "kanal": it.get("channel_name"), "kanal_url": it.get("channel_url"), "url": it.get("url"), "goruntulenme": it.get("views_count"),
                              "yayin": it.get("publication_date"), "sure": it.get("duration_time"), "sira": it.get("rank_absolute"), "tip": it.get("type")}
                             for it in (res.get("items") or []) if it.get("type") in ("youtube_video", "youtube_shorts")]
    print("yt", i, r["tasks"][0]["status_message"], "cost", sum(t.get("cost", 0) for t in r["tasks"]))
json.dump(out, open(os.path.join(OUT, "autocomplete_youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("auto", len(out["autocomplete"]), "yt", len(out["youtube"]))
