# -*- coding: utf-8 -*-
"""25 secili videodan en fazla 100 yorum · DataForSEO video_comments. Cikti: veri/ham/derin/youtube/yorumlar.json"""
import json, os, sys, time
sys.path.insert(0, os.path.dirname(__file__)); import dfs
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT = os.path.join(P, "veri/ham/derin/youtube/yorumlar.json")
SEC = [("a1i0pneZhdw","A"),("8aSO7T-b650","A"),("WLG7aInsqoY","A"),("3kOkkvkj_jo","A"),("o5fbPzVIEsI","A"),("6TgHlbFCsh8","A"),("uiWwzjYYF0k","A"),("2mzVnoBKXh4","A"),("3rnivNp9ix4","A"),("ZRQ78EpYv4s","A"),
       ("DvhsVTEjPBk","B"),("eLA0UQvn-9U","B"),("IKACq0lXBOQ","B"),("ECFUBnW-Cas","B"),("y3F5pE9cXNE","B"),("s9hiDfxw15s","B"),
       ("VWU2Af0ZEms","C"),("TzDTVuaZfoE","C"),("UWz-rBE98P0","C"),("_ZRHeJrF1R4","C"),
       ("agCk6BIyN7g","A"),("6495TGVQPR4","A"),("lkfdmDjQZCc","B"),("U3uNRutqttg","E"),("l7b5Eg_of9k","E"),("oQmwX9Y4or0","E"),("gZyDQFu01GY","E"),("KY3X17-wZz4","E"),("Rcvk_z95Zxc","E"),
       ("LbIRKipqe8M","D"),("tNvspmwo5wk","D"),("welQvPLothc","D"),("a-7tzWHL098","D")]
TUR = {"A": "VitrA/Artema ürünlü tamir-montaj", "B": "Rakip marka tamir-montaj", "C": "Seçim, inceleme, satın alma", "D": "Tadilat ve ilham", "E": "Marka belirsiz tamir-montaj (yüksek izlenmeli)"}
out = json.load(open(OUT)) if os.path.exists(OUT) else {"videolar": {}, "maliyet_usd": 0.0}
for vid, tur in SEC:
    if vid in out["videolar"]: continue
    for deneme in range(3):
        try:
            r = dfs.post("/v3/serp/youtube/video_comments/live/advanced", [{"video_id": vid, "location_code": 2792, "language_code": "tr", "depth": 100}])
        except SystemExit as e:
            print("hata", vid, str(e)[:80]); time.sleep(3); continue
        t = r["tasks"][0]; res = (t.get("result") or [None])[0]
        out["maliyet_usd"] += t.get("cost", 0) or 0
        if res and res.get("items"):
            out["videolar"][vid] = {"tur": tur, "tur_ad": TUR[tur], "baslik": res.get("title"), "toplam_yorum": res.get("comments_count"),
                "yorumlar": [{"metin": i.get("text"), "yazar": i.get("author_name"), "begeni": i.get("likes_count"), "yanit": i.get("reply_count"), "tarih": i.get("timestamp"), "goreli": i.get("publication_date")} for i in res["items"]]}
            print("ok", vid, res.get("comments_count"), len(res["items"]), flush=True); break
        print("bos", vid, t.get("status_message"), flush=True); time.sleep(3)
    json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    time.sleep(2.5)
print("bitti", len(out["videolar"]), round(out["maliyet_usd"], 4), flush=True)
