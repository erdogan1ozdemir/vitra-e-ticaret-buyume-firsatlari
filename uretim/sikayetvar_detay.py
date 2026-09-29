# -*- coding: utf-8 -*-
"""Son 24 aydaki sikayetlerin detay sayfalarindan tam metni ceker (2-4 sn arayla, kaldigi yerden devam eder).
PII temizligi: telefon, e-posta, uzun sayi dizileri (siparis/takip no), TC benzeri sayilar maskelenir. Yazar adi alinmaz.
Cikti: veri/ham/derin/sikayetvar/detay_<slug>.jsonl"""
import json, os, re, sys, html as _h
import sikayetvar_ortak as o
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "veri", "ham", "derin", "sikayetvar")
BASLANGIC = "2024-10-01"

def temizle(t):
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "[e-posta]", t)
    t = re.sub(r"(?:\+?90|0)?[\s-]?\(?5\d{2}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}", "[telefon]", t)
    t = re.sub(r"0?\s?\(?\d{3}\)?[\s-]?\d{3}[\s-]?\d{2}[\s-]?\d{2}\b", "[telefon]", t)
    t = re.sub(r"\b\d{9,}\b", "[no]", t)
    return t

def govde(h):
    i = h.find("selection-share")
    j = h.find("Destekle", i)
    if i < 0 or j < 0: return ""
    seg = re.sub(r"<svg.*?</svg>", "", h[i:j], flags=re.S)
    ps = re.findall(r"<p(?=[\s>])[^>]*>(.*?)</p>", seg, re.S)
    t = "\n".join(_h.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in ps)
    return temizle(re.sub(r"[ \t]+", " ", t).strip())

if __name__ == "__main__":
    for slug in (sys.argv[1:] or ["vitra", "artema"]):
        L = json.load(open(os.path.join(D, "marka_%s.json" % slug), encoding="utf-8"))["sikayetler"]
        hedef = [x for x in L if x["url"] and x["tarih"] and x["tarih"] >= BASLANGIC and not x["yayindan_kaldirildi"]]
        yol = os.path.join(D, "detay_%s.jsonl" % slug)
        var = set()
        if os.path.exists(yol):
            # onceki surumdeki SVG <path> kaynakli kirli kayitlari (yazar adi/tarih on eki) ayikla, yeniden cekilsin
            kirli = re.compile(r"(?:Vitra|Artema)\d{1,2} \w+(?: \d{4})? \d\d:\d\d|Teşekkür Mesajı")
            temiz = [j for j in (json.loads(s) for s in open(yol, encoding="utf-8")) if not kirli.search(j["metin_tam"][:150])]
            with open(yol, "w", encoding="utf-8") as f0:
                for j in temiz: f0.write(json.dumps(j, ensure_ascii=False) + "\n")
            var = {j["url"] for j in temiz}
        print(slug, "hedef", len(hedef), "var", len(var), flush=True)
        with open(yol, "a", encoding="utf-8") as f:
            for n, x in enumerate(hedef):
                if x["url"] in var: continue
                kod, h = o.cek(x["url"][len(o.BAZ):])
                if kod != 200:
                    print("durum", kod, x["url"]); continue
                f.write(json.dumps({"url": x["url"], "id": x["id"], "tarih": x["tarih"], "metin_tam": govde(h)[:2500]}, ensure_ascii=False) + "\n"); f.flush()
                if n % 25 == 0: print(slug, n, "/", len(hedef), flush=True)
