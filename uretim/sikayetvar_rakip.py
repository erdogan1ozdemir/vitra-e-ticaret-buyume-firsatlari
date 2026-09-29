# -*- coding: utf-8 -*-
"""Rakip marka sayfalari: toplam sikayet, puan, cozum orani, donem sikayetleri ve ilk 3 sayfada e-ticaret temali pay.
Kullanim: python3 sikayetvar_rakip.py [slug ...]. Cikti: veri/ham/derin/sikayetvar/rakip_ham.json (rakip.json analizde uretilir)."""
import json, os, re, sys
import sikayetvar_ortak as o, sikayetvar_tema as T
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
SLUGLAR = ["kale", "creavit", "eca", "bocchi", "geberit"]
SAYFA = 3

def eticaret(baslik, metin):
    t = T.kucuk((baslik or "") + " " + (metin or ""))
    pl = re.search("|".join(T.PLATFORMLAR.values()), t)
    onl = re.search(r"online|internet sitesi|web sitesi|\.com\.tr|\.com\b|siteden|internetten|sitesinden|e-ticaret|üzerinden sipariş|üzerinden aldı|üzerinden satın|üzerinden ver", t)
    return bool(pl or onl)

if __name__ == "__main__":
    yol = os.path.join(D, "rakip_ham.json")
    out = json.load(open(yol, encoding="utf-8")) if os.path.exists(yol) else {}
    for slug in (sys.argv[1:] or SLUGLAR):
        kod, h = o.cek("/" + slug, bekle=False)
        if kod != 200:
            out[slug] = {"durum": kod}; print(slug, "durum", kod); continue
        b = o.marka_bilgi(h); b.pop("aivar_ozet", None)
        kartlar = o.sikayetler(h)
        for p in range(2, SAYFA + 1):
            kod, h = o.cek("/%s?page=%d" % (slug, p))
            if kod == 200: kartlar += o.sikayetler(h)
        kartlar = [k for k in kartlar if k["baslik"]]
        for k in kartlar:
            k["eticaret"] = eticaret(k["baslik"], k["metin"])
            k.pop("metin", None) if False else None
        out[slug] = {"bilgi": b, "ilk3sayfa": [{"baslik": k["baslik"], "url": k["url"], "tarih": k["tarih"], "eticaret": k["eticaret"], "cozuldu": k["cozuldu"]} for k in kartlar]}
        print(slug, b.get("toplam_sikayet"), b.get("puan_100"), len(kartlar), sum(k["eticaret"] for k in kartlar), flush=True)
        json.dump(out, open(yol, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
