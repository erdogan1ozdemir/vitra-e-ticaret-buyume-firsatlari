# -*- coding: utf-8 -*-
"""arama.json analizi: grup, kanal, marka gorunurlugu, firsatlar. Cikti: analiz.json + arama_video_tablosu.csv"""
import json, os, sys, re, csv, collections, statistics
sys.path.insert(0, os.path.dirname(__file__)); import youtube_derin_kanal as K
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); D = os.path.join(P, "veri/ham/derin/youtube")
A = json.load(open(os.path.join(D, "arama.json"), encoding="utf-8"))["aramalar"]
GRUP_SIRA = ["Seçim ve karşılaştırma", "Montaj", "Tamir ve bakım", "İlham ve tadilat", "Marka ve rakip", "Yeni kategoriler"]
def temiz(u):
    m = re.search(r"v=([\w-]{11})", u or ""); return "https://www.youtube.com/watch?v=" + m.group(1) if m else u
BR = [("VitrA", r"vitra(?!\s*(georgia))"), ("Artema", r"artema"), ("Kale", r"\bkale\b"), ("Creavit", r"creavit"), ("Serel", r"serel"), ("E.C.A.", r"\beca\b|e\.c\.a"), ("Grohe", r"(?<!hans)grohe"),
      ("Hansgrohe", r"hansgrohe"), ("Geberit", r"geberit"), ("Duravit", r"duravit"), ("Bocchi", r"bocchi"), ("Bien", r"\bbien\b"), ("Koçtaş", r"koçtaş"), ("IKEA", r"ikea"), ("Bauhaus", r"bauhaus")]
rows = []
for k, v in A.items():
    for i, x in enumerate(v["videolar"][:20]):
        rows.append({"grup": v["grup"], "arama": k, "sira": i + 1, "baslik": x["baslik"], "kanal": x["kanal"], "izlenme": x["goruntulenme"] or 0, "yayin": x["yayin"], "sure": x["sure"],
                     "video_id": x["video_id"], "url": temiz(x["url"]), "tip": x["tip"], "kanal_url": x["kanal_url"],
                     "alakasiz": bool(K.ALAKASIZ.search(x["baslik"] + " | " + x["kanal"])), "vitra_kanali": x["kanal"] in K.VITRA_MARKA, "vitra_iliskili": x["kanal"] in K.VITRA_ILISKILI})
with open(os.path.join(D, "arama_video_tablosu.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
# grup ozeti
grup = {}
for g in GRUP_SIRA:
    r = [x for x in rows if x["grup"] == g and not x["alakasiz"]]; ar = {x["arama"] for x in rows if x["grup"] == g}
    tek = {x["video_id"]: x for x in r}
    vitra_ar = {x["arama"] for x in r if x["vitra_kanali"]}
    vsira = [min(y["sira"] for y in r if y["arama"] == a and y["vitra_kanali"]) for a in vitra_ar]
    grup[g] = {"medyan_izlenme_video": round(statistics.median(x["izlenme"] for x in tek.values())), "en_yuksek_video": max(tek.values(), key=lambda x: x["izlenme"])["baslik"][:60], "en_yuksek_video_izlenme": max(x["izlenme"] for x in tek.values()), "arama": len(ar), "video_gorunme": len(r), "tekil_video": len(tek), "toplam_izlenme_tekil": sum(x["izlenme"] for x in tek.values()),
               "ort_izlenme_arama_basi": round(sum(x["izlenme"] for x in tek.values()) / len(ar)),
               "vitra_marka_video_gorunme": sum(1 for x in r if x["vitra_kanali"]), "vitra_tekil_video": len({x["video_id"] for x in r if x["vitra_kanali"]}),
               "vitra_olan_arama": len(vitra_ar), "vitra_ort_en_iyi_sira": round(sum(vsira) / len(vsira), 1) if vsira else None,
               "vitra_izlenme_tekil": sum(x["izlenme"] for x in {y["video_id"]: y for y in r if y["vitra_kanali"]}.values())}
tum = {x["video_id"]: x for x in rows}
# kanal
kan = collections.defaultdict(lambda: {"gorunme": 0, "videolar": {}, "gruplar": collections.Counter(), "aramalar": set()})
for x in rows:
    c = kan[x["kanal"]]; c["gorunme"] += 1; c["videolar"][x["video_id"]] = x; c["gruplar"][x["grup"]] += 1; c["aramalar"].add(x["arama"])
kanal = []
for k, c in kan.items():
    bas = [x["baslik"] for x in c["videolar"].values()]
    kanal.append({"kanal": k, "tur": K.tur(k, bas), "gorunme": c["gorunme"], "arama_sayisi": len(c["aramalar"]), "tekil_video": len(c["videolar"]), "toplam_izlenme_tekil": sum(x["izlenme"] for x in c["videolar"].values()),
                  "en_cok_izlenen": max(c["videolar"].values(), key=lambda x: x["izlenme"])["baslik"][:70], "gruplar": dict(c["gruplar"]), "ort_sira": round(sum(x["sira"] for x in rows if x["kanal"] == k) / c["gorunme"], 1)})
kanal.sort(key=lambda z: (-z["gorunme"], -z["toplam_izlenme_tekil"]))
tur_oz = collections.defaultdict(lambda: {"kanal": 0, "gorunme": 0, "izlenme": 0})
for z in kanal:
    t = tur_oz[z["tur"]]; t["kanal"] += 1; t["gorunme"] += z["gorunme"]; t["izlenme"] += z["toplam_izlenme_tekil"]
# marka gorunurlugu: kanal bazli (marka kanallari)
marka_kanal = {}
for k in ["VitrA Türkiye", "VitrA Bathrooms", "Artema Türkiye", "Kale Banyo", "Creavit", "Creavit Global", "GROHE", "hansgrohe", "BOCCHI", "SEREL", "E.C.A.", "Duravit", "Bien Türkiye", "DESSONI"]:
    if k not in kan: continue
    marka_kanal[k] = {g: {"gorunme": sum(1 for x in rows if x["kanal"] == k and x["grup"] == g), "arama": len({x["arama"] for x in rows if x["kanal"] == k and x["grup"] == g})} for g in GRUP_SIRA}
    marka_kanal[k]["toplam"] = {"gorunme": kan[k]["gorunme"], "arama": len(kan[k]["aramalar"]), "tekil_video": len(kan[k]["videolar"]), "izlenme_tekil": sum(x["izlenme"] for x in kan[k]["videolar"].values())}
# marka anilan videolar (baslikta marka adi, herhangi bir kanal, marka kendi kanali disi)
marka_bahis = {}
for ad, rx in BR:
    vids = {x["video_id"]: x for x in rows if re.search(rx, x["baslik"], re.I)}
    ucuncu = {v: x for v, x in vids.items() if x["kanal"] not in K.MARKA}
    marka_bahis[ad] = {"tekil_video": len(vids), "izlenme": sum(x["izlenme"] for x in vids.values()), "ucuncu_taraf_video": len(ucuncu), "ucuncu_taraf_izlenme": sum(x["izlenme"] for x in ucuncu.values()),
                       "ucuncu_taraf_tamir_video": len([1 for x in ucuncu.values() if re.search(r"tamir|kaçır|değişim|değiştir|arıza|damlat|su dol|onarım|conta|sifon", x["baslik"], re.I)]),
                       "arama_sayisi": len({x["arama"] for x in rows if re.search(rx, x["baslik"], re.I)})}
# arama tablosu
arama = []
for k, v in A.items():
    r = [x for x in rows if x["arama"] == k]
    vit = [x for x in r if x["vitra_kanali"]]
    arama.append({"arama": k, "grup": v["grup"], "video": len(r), "toplam_izlenme": sum(x["izlenme"] for x in r), "en_yuksek_izlenme": max(x["izlenme"] for x in r), "en_yuksek_baslik": max(r, key=lambda x: x["izlenme"])["baslik"][:60],
                  "en_yuksek_kanal": max(r, key=lambda x: x["izlenme"])["kanal"], "vitra_var": bool(vit), "vitra_en_iyi_sira": min([x["sira"] for x in vit]) if vit else None, "vitra_video": len(vit),
                  "vitra_iliskili": any(x["vitra_iliskili"] for x in r), "ilk_kanal": r[0]["kanal"], "ilk_izlenme": r[0]["izlenme"]})
json.dump({"grup": grup, "kanal": kanal, "tur": tur_oz, "marka_kanal": marka_kanal, "marka_bahis": marka_bahis, "arama": arama, "toplam_tekil_video": len(tum), "toplam_kanal": len(kanal), "toplam_satir": len(rows)},
          open(os.path.join(D, "analiz.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(rows), len(tum), len(kanal))
for g, v in grup.items(): print(g, v)
print(dict(tur_oz))
