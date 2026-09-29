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
                o = dict(o, sorgu=kw)
                tum.setdefault(k, o)
    # Vitra mobilya (Isvicre) ve alakasiz kayitlari ele
    lst = [o for o in tum.values() if not re.search(r"design museum|vitra haus|mobilya sanayi", (o["title"] or "") + (o.get("kategori") or ""), re.I)]
    return lst
def il_ilce(adres, sorgu=None):
    a = adres or ""
    bulunan = [(a.rfind(il), il) for il in ILLER if il in a]
    if bulunan:
        il = max(bulunan)[1]
        m = re.search(r"([^/,]+)/" + re.escape(il), a)
        return il, (m.group(1).strip() if m else None)
    if sorgu:
        for il in ILLER:
            if sorgu.endswith(" " + il): return il, None
        if "İstanbul" in sorgu: return "İstanbul", None
    return None, None
def _eski_il_ilce(adres):
    m = re.search(r"\d{5}\s+([^/,]+)/([A-Za-zÇĞİÖŞÜçğıöşü ]+)", adres or "")
    return (m.group(2).strip(), m.group(1).strip()) if m else (None, None)
def gbp_json(ham):
    lst = ozetle(ham)
    satir = []
    for o in lst:
        il, ilce = il_ilce(o.get("adres"), o.get("sorgu"))
        baslik = o["title"] or ""
        servis = bool(re.search(r"servis", baslik, re.I))
        diger = bool(re.search(r"genel müdürl|hammade|fabrika|vitra karo|design studio|vitra türkiye$", baslik, re.I)) or (baslik.strip().lower() in ("vitra", "vitra artema") and not o.get("web"))
        ilce = re.sub(r"^\d{5}\s+", "", ilce) if ilce else ilce
        sahip = bool(re.match(r"^vitra\s+[\wçğıöşüÇĞİÖŞÜ]+\s+ma[ğg]aza", baslik, re.I)) and not re.search(r"artema|servis", baslik, re.I)
        satir.append({"ad": baslik, "tip": "mağaza dışı / belirsiz" if diger else "yetkili servis" if servis else ("VitrA mağazası (kendi adıyla)" if sahip else "satış noktası (bayi)"), "il": il, "ilce": ilce, "puan": o["puan"], "yorum": o["yorum"] or 0,
                      "kategori": o.get("kategori"), "web": o.get("web"), "adres": o.get("adres"), "telefon": o.get("telefon"), "cid": o.get("cid")})
    def ozet(x):
        y = [r for r in x if r["puan"] is not None]
        toplam = sum(r["yorum"] for r in y)
        return {"kayit": len(x), "puanli_kayit": len(y), "toplam_yorum": toplam,
                "ortalama_puan_yorum_agirlikli": round(sum(r["puan"] * r["yorum"] for r in y) / toplam, 2) if toplam else None,
                "ortalama_puan_duz": round(sum(r["puan"] for r in y) / len(y), 2) if y else None,
                "medyan_yorum": sorted(r["yorum"] for r in y)[len(y) // 2] if y else None,
                "puan_4_alti": sum(1 for r in y if r["puan"] < 4.0), "yorum_10_alti": sum(1 for r in x if r["yorum"] < 10)}
    mag = [r for r in satir if r["tip"] not in ("yetkili servis", "mağaza dışı / belirsiz")]; srv = [r for r in satir if r["tip"] == "yetkili servis"]
    iller = {}
    for r in mag:
        iller.setdefault(r["il"] or "(il okunamadı)", []).append(r)
    il_tablo = sorted([{"il": k, "satis_noktasi": len(v), "toplam_yorum": sum(x["yorum"] for x in v),
                        "ortalama_puan_yorum_agirlikli": (round(sum((x["puan"] or 0) * x["yorum"] for x in v) / max(1, sum(x["yorum"] for x in v)), 2))} for k, v in iller.items()], key=lambda z: -z["satis_noktasi"])
    en_cok = sorted(mag, key=lambda r: -r["yorum"])[:15]
    en_dusuk = sorted([r for r in mag if r["yorum"] >= 20 and r["puan"] is not None], key=lambda r: r["puan"])[:10]
    out = {"tarih": TARIH, "kaynak": "DataForSEO serp/google/maps/live/advanced · Google Maps · location_code 2792 · dil tr · %d sorgu (81 il + 22 İstanbul ilçesi) · 'vitra banyo mağazası <yer>'" % len(ham["sorgular"]),
           "yontem_notu": "Google Maps yalnızca sorgu başına ilk 20 sonucu döndürdü; kayıtlar cid ile tekilleştirildi. Sayılar Google Maps'te görünen VitrA etiketli profillerdir, resmi mağaza bulucudaki sayıyla birebir eşleşmesi beklenmez.",
           "resmi_magaza_bulucu": {"kaynak": "https://www.vitra.com.tr/servisler-ve-satis-noktalari", "satis_noktasi": 161, "servis_noktasi": 76, "toplam": 237, "erisim": TARIH},
           "magaza": ozet(mag), "servis": ozet(srv), "magaza_disi_belirsiz": len([r for r in satir if r["tip"] == "mağaza dışı / belirsiz"]), "il_dagilimi": il_tablo, "en_cok_yorum": [{k: r[k] for k in ("ad", "il", "ilce", "puan", "yorum")} for r in en_cok],
           "dusuk_puanli_20plus_yorum": [{k: r[k] for k in ("ad", "il", "ilce", "puan", "yorum")} for r in en_dusuk],
           "vitra_web_alani": {"vitra_com_tr": sum(1 for r in mag if "vitra.com.tr" in (r["web"] or "")), "web_yok": sum(1 for r in mag if not r["web"]), "diger": sum(1 for r in mag if r["web"] and "vitra.com.tr" not in r["web"])},
           "maliyet_usd": ham["maliyet"], "kayitlar": satir}
    json.dump(out, open(os.path.join(KOK, "gbp.json"), "w"), ensure_ascii=False, indent=1)
    return out
if __name__ == "__main__":
    ham = calistir()
    o = gbp_json(ham)
    print("sorgu", len(ham["sorgular"]), "maliyet", ham["maliyet"], json.dumps({k: o[k] for k in ("magaza", "servis")}, ensure_ascii=False))
