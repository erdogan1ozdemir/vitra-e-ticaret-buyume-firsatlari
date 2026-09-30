# -*- coding: utf-8 -*-
"""Sayilara kesme isaretiyle eklenen Turkce ekleri sayinin okunusuna gore duzeltir.
Ornek: %73'si -> %73'ü · %39,6'i -> %39,6'sı · 86'inde -> 86'sında · %9,7'ten -> %9,7'den · 126.619'e -> 126.619'a
"""
import re

_BIRLER = {1: "bir", 2: "iki", 3: "üç", 4: "dört", 5: "beş", 6: "altı", 7: "yedi", 8: "sekiz", 9: "dokuz"}
_ONLAR = {1: "on", 2: "yirmi", 3: "otuz", 4: "kırk", 5: "elli", 6: "altmış", 7: "yetmiş", 8: "seksen", 9: "doksan"}
_SERT = set("fstkçşhp")
_UNLU = "aeıioöuü"


def son_kelime(tam, ondalik=None, olcek=None):
    if olcek == "K":
        return "bin"
    if olcek == "M":
        return "milyon"
    if ondalik:
        return son_kelime(int(ondalik))
    n = tam
    if n == 0:
        return "sıfır"
    if n % 10:
        return _BIRLER[n % 10]
    if (n // 10) % 10:
        return _ONLAR[(n // 10) % 10]
    if (n // 100) % 10:
        return "yüz"
    if n % 1_000_000:
        return "bin"
    if n % 1_000_000_000:
        return "milyon"
    return "milyar"


def _unlu(k):
    return [c for c in k if c in _UNLU][-1]


def _H(k):  # dortlu unlu
    return {"a": "ı", "ı": "ı", "o": "u", "u": "u", "e": "i", "i": "i", "ö": "ü", "ü": "ü"}[_unlu(k)]


def _A(k):  # ikili unlu
    return "a" if _unlu(k) in "aıou" else "e"


# yazilmis ek -> (iyelik mi, hal)
_IYELIK = re.compile(r"^(?:s|n)?[iıuü]")
_HAL = [
    (re.compile(r"^n[iıuü]$"), "BEL"), (re.compile(r"^nd[ae]n$"), "AYR"), (re.compile(r"^nd[ae]$"), "BUL"),
    (re.compile(r"^n[ae]$"), "YON"), (re.compile(r"^n[iıuü]n$"), "ILG"), (re.compile(r"^[dt][iıuü]r$"), "KOP"),
]
_YALIN = [
    (re.compile(r"^y?[ae]$"), "YON"), (re.compile(r"^[dt][ae]$"), "BUL"), (re.compile(r"^[dt][ae]n$"), "AYR"),
    (re.compile(r"^[dt][iıuü]r$"), "KOP"), (re.compile(r"^n?[iıuü]n$"), "ILG"), (re.compile(r"^y?l[ae]$"), "ILE"),
    (re.compile(r"^y[iıuü]$"), "BELY"), (re.compile(r"^l[iıuü]k$"), "LIK"), (re.compile(r"^l[ae]r$"), "COK"), (re.compile(r"^l[ae]rd[ae]$"), "COKBUL"),
]


def cozumle(ek):
    """Yazilmis eki (iyelik, hal) cozumler; taninmazsa None."""
    for rx, hal in _YALIN:
        if rx.match(ek):
            return (False, hal)
    m = re.match(r"^(s?)([iıuü])(.*)$", ek)
    if m:
        kalan = m.group(3)
        if kalan == "":
            return (True, None)
        for rx, hal in _HAL:
            if rx.match(kalan):
                return (True, hal)
    return None


def uret(kelime, iyelik, hal):
    son = kelime[-1]; unlu_son = son in _UNLU; sert = son in _SERT
    if iyelik:
        g = ("s" if unlu_son else "") + _H(kelime)
        k2 = kelime + g  # iyelikten sonra kelime unluyle biter
        if hal is None:
            return g
        return g + {"BEL": "n" + _H(k2), "AYR": "nd" + _A(k2) + "n", "BUL": "nd" + _A(k2), "YON": "n" + _A(k2),
                    "ILG": "n" + _H(k2) + "n", "KOP": "d" + _H(k2) + "r"}[hal]
    if hal == "YON":
        return ("y" if unlu_son else "") + _A(kelime)
    if hal == "BUL":
        return ("t" if sert else "d") + _A(kelime)
    if hal == "AYR":
        return ("t" if sert else "d") + _A(kelime) + "n"
    if hal == "KOP":
        return ("t" if sert else "d") + _H(kelime) + "r"
    if hal == "ILG":
        return ("n" if unlu_son else "") + _H(kelime) + "n"
    if hal == "ILE":
        return ("y" if unlu_son else "") + "l" + _A(kelime)
    if hal == "BELY":
        return ("y" if unlu_son else "") + _H(kelime)
    if hal == "LIK":
        return "l" + _H(kelime) + "k"
    if hal == "COK":
        return "l" + _A(kelime) + "r"
    if hal == "COKBUL":
        return "l" + _A(kelime) + "rd" + _A("l" + _A(kelime) + "r")
    return None


_DESEN = re.compile(
    r"(?<![\w.,%])(%?[+\-]?)(\d{1,3}(?:\.\d{3})+|\d+)(?:,(\d+))?([KM])?((?:</[a-z]+>)*)(['’])([a-zçğıöşü]+)(?![a-zçğıöşü])")


def duzelt(metin):
    if "'" not in metin and "’" not in metin:
        return metin

    def f(m):
        on, tam, ond, olc, kap, kes, ek = m.groups()
        c = cozumle(ek)
        if not c:
            return m.group(0)
        try:
            kel = son_kelime(int(tam.replace(".", "")), ond, olc)
        except ValueError:
            return m.group(0)
        yeni = uret(kel, *c)
        if not yeni:
            return m.group(0)
        return "%s%s%s%s%s%s%s" % (on, tam, ("," + ond) if ond else "", olc or "", kap, kes, yeni)

    return _DESEN.sub(f, metin)


if __name__ == "__main__":
    for t in ["%73'si", "%39,6'i", "%52,4'i", "%26,7'ini", "%9,7'ten", "%0,9'dir", "86'inde", "126.619'e", "%71,1'sı",
              "%89,9'ünde", "192'ünde", "%22,2'ini", "%8,3'ini", "%5,4'inde", "%26,7'idir", "%0,83'dir", "%0,14'de",
              "1.429'i", "%95,6'i", "%20,6'ten", "%42,0'ten", "%33,0'i", "126.619'e", "%77'i", "%15,0'i", "%5,9'i",
              "%1,0'i", "%14,4'inde", "2025'te", "2026'da", "<b>%73</b>'si", "117K'yı", "4,7M'ye", "%15,2'i", "10'u", "40'ta", "%100'ü"]:
        print(t, "->", duzelt(t))


_MARKA_YAZIM = re.compile(r"(?<![\w./@-])(?:Vitra|VITRA|VİTRA)(?![\w-]|\.(?:com|net|de|co)\b)")


def marka(metin):
    """Marka adi her zaman VitrA; alan adlari ve kucuk harfli arama kelimeleri korunur."""
    if not metin or ("itra" not in metin and "ITRA" not in metin and "İTRA" not in metin):
        return metin
    return _MARKA_YAZIM.sub("VitrA", metin)


_MARKA_TEK = [(re.compile(r"(?<![\w.])(?:Eca|ECA)(?![\w.])"), "E.C.A."), (re.compile(r"\bVİOSA\b"), "Viosa"), (re.compile(r"\bIstanbul(?= )"), "İstanbul"),
              (re.compile(r"(?<![\w./-])BAUHAUS(?![\w.-])"), "Bauhaus"), (re.compile(r"(?<![\w./-])GROHE(?![\w.-])"), "Grohe")]


def marka_tek(metin):
    """Ayni markanin farkli yazimlarini tek yazima ceker (veri hucreleri icin)."""
    if not metin: return metin
    for rx, y in _MARKA_TEK:
        metin = rx.sub(y, metin)
    return metin
