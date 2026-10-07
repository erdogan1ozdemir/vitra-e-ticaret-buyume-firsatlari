"""Yayin (Vercel) surumu: yerel tek dosyalik HTML'lerden repo/ altina hafif surum uretir.

Yerel dosyalar tek basina tasinabilir kalir (Excel, gorseller ve veri sayfanin icinde). Yayin surumunde:
  - ana rapor: gomulu Excel yerine repodaki Excel'e baglanti (icerik birebir ayni oldugu dogrulanir),
    20 KB ustu gorseller ve Ingilizce ceviri verisi (#dil-veri) ayri dosyaya alinir; ceviri yalniz EN secilince iner;
  - alt sayfalar: 30 KB ustu tablo verisi (#veri) tablo basina ayri dosyaya alinir, tablo ekrana yaklasinca iner;
    yorum-soru-seti'nde yorum (y) ve soru (s) listeleri ayri dosyadir.
Ayri dosyalar repo/v/ altinda icerik ozetli adla durur (degismeyen dosya onbellekten gelir); kullanilmayanlar silinir.
Kullanim: python3 vercel_hazirla.py   (rapor.py, excel.py ve alt sayfalar uretildikten sonra)
"""
import base64, hashlib, json, os, re, sys

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.join(KOK, "repo")
V = os.path.join(REPO, "v")
ANA = "VitrA_E-Ticaret_Buyume_Firsatlari.html"
EXCEL = "VitrA_E-Ticaret_Buyume_Firsatlari.xlsx"
ALT = ["arama-sonuclari.html", "kelime-evreni.html", "pazaryeri-taramasi.html", "youtube-videolari.html", "geo-promptlari.html"]
YORUM = "yorum-soru-seti.html"
yazilan = set()


def ozet(b): return hashlib.md5(b).hexdigest()[:10]


def dosya(ad, uzanti, icerik):
    """v/<ad>-<ozet>.<uzanti> yazar, yayindaki goreli yolu dondurur."""
    b = icerik if isinstance(icerik, bytes) else icerik.encode("utf-8")
    yol = "v/%s-%s.%s" % (ad, ozet(b), uzanti)
    tam = os.path.join(REPO, yol)
    if not os.path.exists(tam) or open(tam, "rb").read() != b:
        open(tam, "wb").write(b)
    yazilan.add(os.path.basename(yol))
    return yol


def js_json(o):
    return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def ana():
    s = open(os.path.join(KOK, ANA), encoding="utf-8").read()
    n0 = len(s)
    # 1) Excel: gomulu veri yerine repodaki dosya (birebir ayni olmali)
    xl = open(os.path.join(KOK, EXCEL), "rb").read()
    adet = 0
    def excel(m):
        nonlocal adet
        if base64.b64decode(m.group(1)) != xl:
            raise SystemExit("Gömülü Excel diskteki %s ile aynı değil; önce rapor.py yeniden çalıştırılmalı." % EXCEL)
        adet += 1
        return 'href="%s"' % EXCEL
    s = re.sub(r'href="data:application/vnd\.openxmlformats-officedocument\.spreadsheetml\.sheet;base64,([^"]+)"', excel, s)
    if not adet: raise SystemExit("Ana raporda gömülü Excel bağlantısı bulunamadı.")
    hedef_xl = os.path.join(REPO, EXCEL)   # baglanti hicbir zaman eski dosyaya gitmesin: Excel ayni adimda kopyalanir
    if not os.path.exists(hedef_xl) or open(hedef_xl, "rb").read() != xl: open(hedef_xl, "wb").write(xl)
    # 2) 20 KB ustu gorseller
    def gorsel(m):
        b = base64.b64decode(m.group(2))
        if len(b) < 20000: return m.group(0)
        return 'src="%s"' % dosya("gorsel", "jpg" if m.group(1) == "jpeg" else m.group(1), b)
    s = re.sub(r'src="data:image/(jpeg|png|webp);base64,([^"]+)"', gorsel, s)
    # 3) Ingilizce ceviri verisi: yalniz EN secilince indirilir
    m = re.search(r'<script type="application/json" id="dil-veri">(.*?)</script>', s, re.S)
    if not m: raise SystemExit("Ana raporda #dil-veri bloğu bulunamadı.")
    veri = json.loads(m.group(1))
    yol = dosya("dil-veri", "json", json.dumps(veri, ensure_ascii=False, separators=(",", ":"), sort_keys=True))   # sirali: icerik degismedikce dosya adi da degismez
    s = s[:m.start()] + '<script type="application/json" id="dil-veri" data-src="%s"></script>' % yol + s[m.end():]
    open(os.path.join(REPO, ANA), "w", encoding="utf-8").write(s)
    print("%s: %.2f MB -> %.2f MB (Excel %d bağlantı)" % (ANA, n0 / 1e6, len(s) / 1e6, adet))


def veri_blogu(s, ad):
    m = re.search(r'<script type="application/json" id="veri">(.*?)</script>', s, re.S)
    if not m: raise SystemExit("%s: #veri bloğu bulunamadı." % ad)
    return m, json.loads(m.group(1))


def alt(ad):
    s = open(os.path.join(KOK, ad), encoding="utf-8").read(); n0 = len(s)
    m, V_ = veri_blogu(s, ad)
    kok = ad[:-5]; ayrilan = []
    for k, t in list(V_.get("t", {}).items()):
        b = json.dumps(t, ensure_ascii=False, separators=(",", ":"))
        if len(b.encode()) < 30000: continue
        V_["t"][k] = {"src": dosya("%s-%s" % (kok, k), "json", b)}
        ayrilan.append(k)
    s = s[:m.start()] + '<script type="application/json" id="veri">%s</script>' % js_json(V_) + s[m.end():]
    open(os.path.join(REPO, ad), "w", encoding="utf-8").write(s)
    print("%s: %.2f MB -> %.2f MB (ayrı tablo: %s)" % (ad, n0 / 1e6, len(s) / 1e6, ", ".join(ayrilan) or "-"))


def yorum():
    s = open(os.path.join(KOK, YORUM), encoding="utf-8").read(); n0 = len(s)
    m, V_ = veri_blogu(s, YORUM)
    for k in ("y", "s"):
        V_[k] = {"src": dosya("yorum-soru-seti-%s" % k, "json", json.dumps(V_[k], ensure_ascii=False, separators=(",", ":")))}
    s = s[:m.start()] + '<script type="application/json" id="veri">%s</script>' % js_json(V_) + s[m.end():]
    open(os.path.join(REPO, YORUM), "w", encoding="utf-8").write(s)
    print("%s: %.2f MB -> %.2f MB (yorum ve soru listeleri ayrı)" % (YORUM, n0 / 1e6, len(s) / 1e6))


def main():
    os.makedirs(V, exist_ok=True)
    ana()
    for ad in ALT: alt(ad)
    yorum()
    eski = [f for f in os.listdir(V) if f not in yazilan]
    for f in eski: os.remove(os.path.join(V, f))
    print("v/: %d dosya, %.2f MB; silinen eski dosya: %d" % (len(yazilan), sum(os.path.getsize(os.path.join(V, f)) for f in yazilan) / 1e6, len(eski)))


if __name__ == "__main__":
    main()
