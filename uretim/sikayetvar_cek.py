# -*- coding: utf-8 -*-
"""VitrA ve Artema Sikayetvar marka sayfalarini sayfa sayfa gezer; sikayet basligi, tarih, goruntulenme, cozuldu, kisa metin.
Kullanim: python3 sikayetvar_cek.py [slug ...]   (varsayilan: vitra artema). Cikti: veri/ham/derin/sikayetvar/marka_<slug>.json"""
import json, os, sys, math
import sikayetvar_ortak as o
CIKTI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
os.makedirs(CIKTI, exist_ok=True)

def marka(slug, azami=80):
    kod, h = o.cek("/" + slug, bekle=False)
    if kod != 200:
        print(slug, "durum", kod); return None
    bilgi = o.marka_bilgi(h)
    n = min(bilgi.get("sayfa_sayisi") or math.ceil((bilgi.get("toplam_sikayet") or 24) / 24), azami)
    liste = []; gorulen = set()
    for p in range(1, n + 1):
        if p > 1:
            kod, h = o.cek("/%s?page=%d" % (slug, p))
            if kod != 200:
                print(slug, p, "durum", kod); break
        kartlar = o.sikayetler(h)
        yeni = 0
        for k in kartlar:
            anahtar = k["id"] or k["url"] or (k["tarih_ham"], k["metin"][:60])
            if anahtar in gorulen: continue
            gorulen.add(anahtar); k["sayfa"] = p; k["marka"] = slug; liste.append(k); yeni += 1
        print(slug, "sayfa", p, "/", n, "kart", len(kartlar), "yeni", yeni, "son tarih", kartlar[-1]["tarih"] if kartlar else None, flush=True)
        if not kartlar: break
    bilgi["cekilen_sikayet"] = len(liste)
    d = {"slug": slug, "bilgi": bilgi, "sikayetler": liste}
    json.dump(d, open(os.path.join(CIKTI, "marka_%s.json" % slug), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return d

if __name__ == "__main__":
    for s in (sys.argv[1:] or ["vitra", "artema"]):
        marka(s)
