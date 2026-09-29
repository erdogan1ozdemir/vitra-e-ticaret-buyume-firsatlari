# -*- coding: utf-8 -*-
"""Fiyat manzarasi ortak yardimcilar (kimlik dfs.py uzerinden, ciktiya basilmaz)."""
import json, os, subprocess, time, random, re
import dfs
KOK = "/Users/Erdo/Desktop/Claude Projects/Vitra/11_e-ticaret-buyume/veri/ham/derin/fiyat_manzarasi/"
os.makedirs(KOK, exist_ok=True)
def bekle(a=3, b=6): time.sleep(random.uniform(a, b))
def dfs_get(path):
    for i in range(3):
        r = subprocess.run(["curl","-s","-m","120","-u","%s:%s"%(dfs._U,dfs._P),"https://api.dataforseo.com"+path],capture_output=True,text=True)
        try: return json.loads(r.stdout)
        except Exception: time.sleep(4)
    raise SystemExit("get basarisiz "+path)
KATEGORILER = ["klozet","asma klozet","klozet kapağı","akıllı klozet","lavabo","çanak lavabo","lavabo dolabı","banyo dolabı",
 "çamaşır makinesi dolabı","boy dolabı","banyo aynası","ledli banyo aynası","duşakabin","duş teknesi","küvet","banyo bataryası",
 "lavabo bataryası","duş seti","ankastre batarya","taharet musluğu","gömme rezervuar","rezervuar iç takımı","klozet takımı",
 "havlupan","banyo aksesuar seti","evye","mutfak bataryası","vitra klozet","vitra lavabo","vitra batarya"]
VITRA_URUNLER = ["vitra s20 asma klozet","vitra integra asma klozet","vitra integra klozet kapağı","vitra root lavabo dolabı",
 "vitra sento asma klozet","vitra metropole asma klozet","vitra shift asma klozet","vitra nest trendy asma klozet",
 "artema solid s lavabo bataryası","artema minimax s lavabo bataryası","artema flo s banyo bataryası","vitra sento lavabo dolabı"]
# ürün tipi eşlemesi (kategori kelimesi -> ürün tipi)
TIP = {"klozet":"Klozet","asma klozet":"Klozet","klozet kapağı":"Klozet kapağı","akıllı klozet":"Akıllı klozet","lavabo":"Lavabo",
 "çanak lavabo":"Lavabo","lavabo dolabı":"Banyo mobilyası","banyo dolabı":"Banyo mobilyası","çamaşır makinesi dolabı":"Banyo mobilyası",
 "boy dolabı":"Banyo mobilyası","banyo aynası":"Ayna","ledli banyo aynası":"Ayna","duşakabin":"Duşakabin & duş teknesi",
 "duş teknesi":"Duşakabin & duş teknesi","küvet":"Küvet","banyo bataryası":"Batarya","lavabo bataryası":"Batarya","duş seti":"Duş seti",
 "ankastre batarya":"Batarya","taharet musluğu":"Batarya","gömme rezervuar":"Rezervuar","rezervuar iç takımı":"Rezervuar",
 "klozet takımı":"Klozet","havlupan":"Aksesuar & havlupan","banyo aksesuar seti":"Aksesuar & havlupan","evye":"Mutfak (evye & batarya)",
 "mutfak bataryası":"Mutfak (evye & batarya)","vitra klozet":"Klozet","vitra lavabo":"Lavabo","vitra batarya":"Batarya"}
MARKALAR = ["VitrA","Artema","Kale","Creavit","Turkuaz","ECA","Grohe","Hansgrohe","Duravit","Serel","Seramiksan","Bocchi","Güral","Vitra Bad",
 "Newarc","Geberit","Roca","Villeroy","Ideal Standard","Grohe","Franke","Blanco","Teka","Alvit","Bien","Baymak","Isvea","Eca","Nova","Bauhaus"]
def marka_bul(baslik):
    b = baslik.lower()
    for m,anah in [("VitrA",["vitra","v-flush","integra","sento","s20 "]),("Artema",["artema"]),("Kale",["kale "]),("Creavit",["creavit"]),
                   ("Turkuaz",["turkuaz"]),("ECA",["eca ","e.c.a"]),("Grohe",["grohe"]),("Hansgrohe",["hansgrohe"]),("Duravit",["duravit"]),
                   ("Serel",["serel"]),("Seramiksan",["seramiksan"]),("Bocchi",["bocchi"]),("Güral",["güral","gural"]),("Newarc",["newarc"]),
                   ("Geberit",["geberit"]),("Roca",["roca"]),("Villeroy & Boch",["villeroy"]),("Ideal Standard",["ideal standard"]),
                   ("Franke",["franke"]),("Blanco",["blanco"]),("Teka",["teka "]),("Bien",["bien "]),("Baymak",["baymak"]),("Shower",["shower "]),("Durul",["durul"]),("Fause",["fause"]),("Nkp",["nkp "]),("Visam",["visam"]),("Isvea",["isvea"]),("Roomart",["roomart"]),("Rani",["rani "]),("Kohler",["kohler"])]:
        if any(a in b+" " for a in anah): return m
    return "Diğer markalar"
