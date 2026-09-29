# -*- coding: utf-8 -*-
KEL = {
"SSG": "klozet, klozet fiyatları, asma klozet, akıllı klozet, klozet kapağı, klozet iç takımı, gömme rezervuar, gömme rezervuar iç takımı, lavabo, çanak lavabo, lavabo modelleri, pisuvar, bide, tuvalet taşı, kanalsız klozet, klozet takımı",
"BM": "banyo dolabı, banyo dolabı modelleri, lavabo dolabı, lavabolu banyo dolabı, boy dolabı, aynalı banyo dolabı, banyo aynası, ledli ayna, çamaşır makinesi dolabı, kurutma makinesi dolabı, banyo tezgahı, suya dayanıklı banyo dolabı, 80 cm banyo dolabı, banyo rafı, dolap kulpu",
"Armatür-duş": "banyo bataryası, lavabo bataryası, eviye bataryası, termostatik batarya, ankastre batarya, taharet musluğu, duş seti, duş başlığı, robot duş seti, ara musluk, sifon, kartuş, musluk başlığı",
"Yıkanma": "duşakabin, duşakabin fiyatları, küvet, jakuzi, duş teknesi, duş kanalı",
"Bitişik": "evye, granit evye, arıtmalı batarya, su arıtma cihazı, havlupan, elektrikli havlupan, şofben, termosifon, mutfak tezgahı, seramik yapıştırıcı, derz dolgu, bornoz, banyo paspası, çamaşır sepeti, klozet adaptörü, bebek küveti, engelli klozet, tutunma barı, yer süzgeci, banyo lambası, taharet aparatı, ısıtmalı klozet kapağı, şamandıra, klozet kapağı menteşesi",
"Hizmet": "banyo tadilatı, banyo tadilat fiyatları, banyo yenileme, banyo tasarım, küçük banyo tasarımı, banyo modelleri, küçük banyo modelleri, banyo dekorasyonu, banyo seti, komple banyo, klozet montajı, klozet montaj ücreti, gömme rezervuar montajı, tesisatçı",
"Karo": "fayans, fayans fiyatları, seramik, porselen karo, banyo fayans modelleri",
"Soru": "klozet ölçüleri, banyo dolabı ölçüleri, en iyi klozet markası, hangi klozet alınmalı, gömme rezervuar mı dış rezervuar mı, akıllı klozet nedir, klozet su kaçırıyor",
"Marka": "vitra klozet, vitra banyo dolabı, vitra gömme rezervuar, vitra lavabo, artema batarya, kale klozet, creavit klozet, geberit gömme rezervuar, grohe batarya",
}
LISTE = []
for t, s in KEL.items():
    for k in [x.strip() for x in s.split(",")]:
        LISTE.append((k, t))
if __name__ == "__main__":
    print(len(LISTE), len(set(k for k,_ in LISTE)))
