# -*- coding: utf-8 -*-
"""Sikayetvar konu sayfalari (marka/konu): Sikayetvar'in kendi konu dizininden toplam sikayet sayisi. Ilk sayfa okunur.
Ek marka sayfalari: vitra-karo. Cikti: veri/ham/derin/sikayetvar/konu.json"""
import json, os, re
import sikayetvar_ortak as o
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
KONULAR = ["yedek-parca", "montaj", "yetkili-servis", "servis", "garanti", "musteri-hizmetleri", "iade", "kargo", "siparis", "teslimat",
           "trendyol", "hepsiburada", "n11", "amazon", "fiyat", "kampanya", "indirim", "taksit", "bayi", "magaza", "koctas", "bauhaus",
           "usta", "su-kaciriyor", "catlak", "leke", "kirik", "sizinti", "kanalsiz-klozet", "banyo-dolabi", "klozet-kapagi", "ayna", "akilli-klozet"]
if __name__ == "__main__":
    out = {}
    for marka in ["vitra", "artema"]:
        for k in KONULAR:
            kod, h = o.cek("/%s/%s" % (marka, k))
            if kod != 200: out["%s/%s" % (marka, k)] = {"durum": kod}; print(marka, k, kod); continue
            m = re.search(r">([\d.]+) şikayet<", h)
            out["%s/%s" % (marka, k)] = {"toplam": int(m.group(1).replace(".", "")) if m else None, "baslik": re.search(r"<title>([^<]*)", h).group(1)}
            print(marka, k, out["%s/%s" % (marka, k)]["toplam"], flush=True)
    kod, h = o.cek("/vitra-karo")
    b = o.marka_bilgi(h); b.pop("aivar_ozet", None); out["vitra-karo"] = b
    json.dump(out, open(os.path.join(D, "konu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
