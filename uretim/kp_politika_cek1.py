# -*- coding: utf-8 -*-
"""Baslik 1-3: odeme, kargo/iade ve garanti/servis sayfalarini curl ile ceker (onbellekli); metinleri metinler/ altina yazar."""
import json, os, re, sys
from kp_politika_ortak import *
SAYFALAR = {
 "vitra": ["https://www.vitra.com.tr/odeme-rehberi","https://www.vitra.com.tr/teslimat-rehberi","https://www.vitra.com.tr/degisim-iade-rehberi","https://www.vitra.com.tr/support/faq","https://www.vitra.com.tr/servisler-ve-satis-noktalari","https://www.vitra.com.tr/c-montaj-hizmeti","https://www.vitra.com.tr/kampanyalar"],
 "bauhaus": ["https://www.bauhaus.com.tr/taksit-secenekleri","https://www.bauhaus.com.tr/ucretsiz-kargo","https://www.bauhaus.com.tr/iade","https://www.bauhaus.com.tr/urun-iade-garantisi","https://www.bauhaus.com.tr/urun-garantisi","https://www.bauhaus.com.tr/servisler"],
 "ikea": ["https://www.ikea.com.tr/odeme-secenekleri","https://www.ikea.com.tr/montaj-hizmeti","https://www.ikea.com.tr/iade-politikasi","https://www.ikea.com.tr/musteri-hizmetleri/garanti-kosullari","https://www.ikea.com.tr/musteri-hizmetleri/sikca-sorulan-sorular","https://www.ikea.com.tr/ikea-onemli-bilgilendirme","https://www.ikea.com.tr/ikea-kurumsal"],
 "kale": ["https://www.kale.com.tr/sikca-sorulan-sorular","https://www.kale.com.tr/yetkili-servisler-ve-hizmetler","https://www.kale.com.tr/iletisim"],
 "banyomarka": ["https://www.banyomarka.com/musteri-hizmetleri.xhtml","https://www.banyomarka.com/teslimat-kosullari.shtm","https://www.banyomarka.com/garanti-ve-iade-kosullari.shtm","https://www.banyomarka.com/satis-sozlesmesi.shtm"],
 "banyoline": ["https://www.banyoline.com/montaj-hizmeti","https://www.banyoline.com/mesafeli-satis-sozlesmesi","https://www.banyoline.com/kampanyalar","https://www.banyoline.com/Iletisim"],
}
if __name__ == "__main__":
    hedef = sys.argv[1:] or list(SAYFALAR)
    durum = {}
    for site in hedef:
        for u in SAYFALAR[site]:
            k, h = cek(u)
            durum[u] = k
            print(k, len(h), u, flush=True)
    d = os.path.join(KOK, "durum_cek1.json")
    eski = json.load(open(d)) if os.path.exists(d) else {}
    eski.update(durum); json.dump(eski, open(d, "w"), indent=1)
