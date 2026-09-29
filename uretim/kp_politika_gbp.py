# -*- coding: utf-8 -*-
"""Baslik 5: Google Business Profile · VitrA magazalari (DataForSEO serp/google/maps/live/advanced, location_code 2792, dil tr).
Cikti: kanal_politikalari/gbp_ham.json (tum maps ogeleri) ve gbp.json (VitrA ozeti). Kimlik bilgisi yazilmaz."""
import json, os, re, time
import dfs
from kp_politika_ortak import KOK, TARIH
ILLER = ["Adana","Adıyaman","Afyonkarahisar","Ağrı","Aksaray","Amasya","Ankara","Antalya","Ardahan","Artvin","Aydın","Balıkesir","Bartın","Batman","Bayburt","Bilecik","Bingöl","Bitlis","Bolu","Burdur","Bursa","Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Düzce","Edirne","Elazığ","Erzincan","Erzurum","Eskişehir","Gaziantep","Giresun","Gümüşhane","Hakkari","Hatay","Iğdır","Isparta","İstanbul","İzmir","Kahramanmaraş","Karabük","Karaman","Kars","Kastamonu","Kayseri","Kilis","Kırıkkale","Kırklareli","Kırşehir","Kocaeli","Konya","Kütahya","Malatya","Manisa","Mardin","Mersin","Muğla","Muş","Nevşehir","Niğde","Ordu","Osmaniye","Rize","Sakarya","Samsun","Şanlıurfa","Siirt","Sinop","Sivas","Şırnak","Tekirdağ","Tokat","Trabzon","Tunceli","Uşak","Van","Yalova","Yozgat","Zonguldak"]
ILCELER = ["Kadıköy","Ataşehir","Ümraniye","Üsküdar","Kartal","Pendik","Maltepe","Beşiktaş","Şişli","Bakırköy","Esenyurt","Başakşehir","Avcılar","Beylikdüzü","Sarıyer","Kağıthane","Bahçelievler","Sancaktepe","Çekmeköy","Tuzla","Bağcılar","Küçükçekmece"]
HAM = os.path.join(KOK, "gbp_ham.json")
def calistir(azami_maliyet=0.7):
    ham = json.load(open(HAM)) if os.path.exists(HAM) else {"sorgular": {}, "maliyet": 0.0}
    sorgular = ["vitra banyo mağazası %s" % il for il in ILLER] + ["vitra banyo mağazası %s İstanbul" % i for i in ILCELER]
    for kw in sorgular:
        if kw in ham["sorgular"]: continue
        if ham["maliyet"] > azami_maliyet: print("maliyet siniri"); break
        r = dfs.post("/v3/serp/google/maps/live/advanced", [{"keyword": kw, "location_code": 2792, "language_code": "tr", "depth": 20}])
        t = r["tasks"][0]
        ham["maliyet"] = round(ham["maliyet"] + (t.get("cost") or 0), 4)
        ogeler = []
        if t.get("result"):
            for it in t["result"][0].get("items") or []:
                if it.get("type") != "maps_search": continue
                rt = it.get("rating") or {}
                ogeler.append({"rank": it.get("rank_absolute"), "title": it.get("title"), "cid": it.get("cid"), "place_id": it.get("place_id"),
                               "puan": rt.get("value"), "yorum": rt.get("votes_count"), "adres": it.get("address"), "kategori": it.get("category"),
                               "telefon": it.get("phone"), "web": it.get("domain"), "url": it.get("url"), "calisma": (it.get("work_time") or {}).get("work_hours", {}).get("current_status") if it.get("work_time") else None,
                               "lat": it.get("latitude"), "lon": it.get("longitude")})
        ham["sorgular"][kw] = ogeler
        json.dump(ham, open(HAM, "w"), ensure_ascii=False)
        time.sleep(0.8)
    return ham
def ozetle(ham):
    tum = {}
    for kw, ogeler in ham["sorgular"].items():
        for o in ogeler:
            if re.search(r"vitra", o["title"] or "", re.I) and re.search(r"banyo|vitra|artema|seramik|yapı|tesisat|hırdavat|karo|mobilya|dekor", (o.get("kategori") or "") + (o["title"] or ""), re.I):
                k = o.get("cid") or o.get("place_id") or (o["title"], o["adres"])
                tum.setdefault(k, o)
    # Vitra mobilya (Isvicre) ve alakasiz kayitlari ele
    lst = [o for o in tum.values() if not re.search(r"design museum|vitra haus|mobilya sanayi", (o["title"] or "") + (o.get("kategori") or ""), re.I)]
    return lst
if __name__ == "__main__":
    ham = calistir()
    print("sorgu", len(ham["sorgular"]), "maliyet", ham["maliyet"])
