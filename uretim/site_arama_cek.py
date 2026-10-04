# -*- coding: utf-8 -*-
"""vitra.com.tr site ici arama testi: herkese acik /search?q= sayfasi; sonuc sayisi ve ilk 20 urun karti.
Oturum acilmaz, form gonderilmez; istekler arasi 2 sn beklenir. Cikti: veri/ham/derin/site_arama/sonuc.json"""
import subprocess, re, html, json, time, os, urllib.parse
import veri
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
# (grup, sorgu, beklenen ifade regex'i: ilk sonuclarin ilgili sayilmasi icin ad/kategoride gecmesi gereken kok)
Q = [("Kategori", "klozet", r"klozet"), ("Kategori", "asma klozet", r"asma klozet"), ("Kategori", "lavabo", r"lavabo"), ("Kategori", "banyo dolabı", r"dolab|dolap"),
     ("Kategori", "duşakabin", r"duşakabin|duş kabin"), ("Kategori", "banyo bataryası", r"batarya"), ("Kategori", "gömme rezervuar", r"rezervuar"), ("Kategori", "havlupan", r"havlupan"),
     ("Kategori", "evye", r"evye|eviye"), ("Kategori", "duş seti", r"duş set|el duşu|duş sistem"),
     ("Yedek parça ve aksesuar", "klozet kapağı", r"kapa[kğ]"), ("Yedek parça ve aksesuar", "iç takım", r"iç takım"), ("Yedek parça ve aksesuar", "rezervuar iç takımı", r"iç takım"),
     ("Yedek parça ve aksesuar", "şamandıra", r"şamandıra|iç takım"), ("Yedek parça ve aksesuar", "klozet kapağı menteşesi", r"menteşe"), ("Yedek parça ve aksesuar", "kartuş", r"kartuş"),
     ("Yedek parça ve aksesuar", "conta", r"conta"), ("Yedek parça ve aksesuar", "kumanda paneli", r"kumanda"), ("Yedek parça ve aksesuar", "taharet musluğu", r"taharet"),
     ("Yedek parça ve aksesuar", "lavabo sifonu", r"sifon"),
     ("Yazım farkı", "klozet kapagi", r"kapa[kğ]"), ("Yazım farkı", "dusakabin", r"duşakabin|duş kabin"), ("Yazım farkı", "banyo dolabi", r"dolab|dolap"), ("Yazım farkı", "rezarvuar", r"rezervuar"),
     ("Yazım farkı", "klozed", r"klozet"), ("Yazım farkı", "batarya", r"batarya"),
     ("Ölçü ve özellik", "80 cm banyo dolabı", r"80"), ("Ölçü ve özellik", "kanalsız klozet", r"kanalsız|rim-?ex|rimless"), ("Ölçü ve özellik", "akıllı klozet", r"akıllı|v-care"),
     ("Ölçü ve özellik", "siyah klozet", r"siyah"),
     ("Seri ve ürün kodu", "metropole", r"metropole"), ("Seri ve ürün kodu", "sento", r"sento"), ("Seri ve ürün kodu", "integra", r"integra"), ("Seri ve ürün kodu", "7906B483-0090", r"7906b483|metropole"),
     ("Hizmet ve destek", "montaj", r"montaj"), ("Hizmet ve destek", "yedek parça", r"yedek|iç takım|menteşe|kartuş|conta"), ("Hizmet ve destek", "garanti", r"garanti"), ("Hizmet ve destek", "servis", r"servis")]


def cek(q):
    url = "https://www.vitra.com.tr/search?text=" + urllib.parse.quote(q)   # arama kutusunda Enter ile acilan sonuc sayfasi
    r = subprocess.run(["curl", "-sL", "-A", UA, "--max-time", "40", url], capture_output=True)
    s = r.stdout.decode("utf-8", "ignore")
    m = re.search(r'data-prd-count="(\d+)"', s)
    n = int(m.group(1)) if m else 0
    i = s.find('id="product-list"')
    urunler = []
    for js in re.findall(r"data-product='(\{.*?\})'", s[i:] if i >= 0 else "", re.S):
        try: d = json.loads(html.unescape(js))
        except Exception: continue
        urunler.append({"ad": d.get("name"), "kategori": d.get("category"), "fiyat": d.get("price"), "id": d.get("id")})
    bos = bool(re.search(r"sonuç bulunamadı|bulunamadı|eşleşen ürün yok", html.unescape(s), re.I)) and n == 0
    return {"url": url, "sonuc": n, "urunler": urunler[:20], "bos": bos, "http": len(s)}


def main():
    out = []
    for g, q, rx in Q:
        r = cek(q); r.update({"grup": g, "sorgu": q, "beklenen": rx}); out.append(r)
        print(q, r["sonuc"], [u["ad"] for u in r["urunler"][:3]]); time.sleep(2)
    json.dump({"tarih": "2026-10-04", "kaynak": "vitra.com.tr /search?text= (arama kutusunda Enter sonrası açılan sonuç sayfası)", "sorgular": out},
              open(os.path.join(veri.V, "ham/derin/site_arama/sonuc.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
