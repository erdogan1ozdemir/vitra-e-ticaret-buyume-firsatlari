# -*- coding: utf-8 -*-
"""Marka + kategori aramaları: kök ifadeyi (marka sonrası) VitrA kategori ağacına eşler. Kaynak eşleme: kelime evreni kaynak listesi
(sezonsallık listesi + ek baş kelimeler); bulunamayan yazım varyantlarında Türkçe karakter sadeleştirme, sonra baş isim kuralı."""
import json, os, re
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(P, "veri/kaynak/sezon_dashboard.js"), encoding="utf-8").read(); d = json.loads(s[s.index("{"):s.rindex("}") + 1])
KAT = {k["kw"].strip().lower(): k["k1"] for k in d["keywords"]}
for k in json.load(open(os.path.join(P, "veri/kaynak/ek_kelimeler.json"), encoding="utf-8")): KAT[k["kw"]] = k["k1"]
_TR = str.maketrans("çğıöşüâÇĞİÖŞÜ", "cgiosuaCGIOSU")
KAT_A = {}
for k, v in KAT.items(): KAT_A.setdefault(k.translate(_TR), v)
KURAL = [(r"duşakabin|duşa kabin|duş kabin|duş tekne|teknesi|tekneli|teknesiz|küvet|kuvet|jakuzi|yer süzgeci|süzgeç|duş kanal|gider", "Yıkanma Alanları"),
         (r"rezervuar|rezarvuar|kumanda paneli|iç takım|şamandıra|sifon", "Rezervuarlar"),
         (r"batarya|musluk|armatür|çeşme|ara musluk|stop val|vana", "Armatürler"),   # "lavabo bataryası", "eviye bataryası" armatürdür; vitrifiyeden önce bakılır
         (r"klozet|lavabo|pisuvar|pisuar|pisivar|bide|tuvalet taşı|hela|wc|evye|eviye|vitrifiye", "Vitrifiyeler"),
         (r"duş seti|duş başlı|el duşu|tepe duş|duş kolon|duş paneli|yağmur", "Duşlar"),
         (r"banyo dolab|dolap|ayna|mobilya|tezgah|etajer|konsol|kulp", "Banyo Mobilyaları"),
         (r"fayans|fanyas|seramik|karo|granit|porselen|süpürgelik|mozaik", "Karo Seramik Ürünleri"),
         (r"havlu|sabunluk|kağıtlık|fırça|askı|raf|çöp|peçete|aksesuar|tutunma|tutamak", "Banyo Aksesuarları")]
def kategori(kok):
    k = kok.strip().lower()
    if k in KAT: return KAT[k]
    if k.translate(_TR) in KAT_A: return KAT_A[k.translate(_TR)]
    for rx, ad in KURAL:
        if re.search(rx, k): return ad
    return None
