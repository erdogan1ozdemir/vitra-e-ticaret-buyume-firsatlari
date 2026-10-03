# -*- coding: utf-8 -*-
"""Yorum ve soru metinlerinde yalniz ad soyaddan olusan kayitlari bulmak icin yaygin Turkce adlar."""
ADLAR = set("""ahmet mehmet mustafa ali hüseyin hasan ibrahim ismail osman yusuf murat ömer ramazan halil süleyman abdullah mahmut recep salih fatih kadir emre hakan
kemal yaşar orhan metin serkan burak volkan erkan sinan cem can mert onur tolga ozan kaan berk emir eren arda baran enes furkan yunus ahmet bilal tuncay
erdoğan erdal ercan engin ilker irfan levent necati nihat oğuz okan savaş selim serdar sezgin tarık tayfun uğur ümit yavuz yılmaz zafer zeki adem cengiz
fatma ayşe emine hatice zeynep elif meryem şerife zehra sultan hanife merve özlem yasemin esra büşra kübra tuğba gamze ebru derya sevgi songül aysel
gülsüm hülya nuran nurcan pınar seda sibel sevda sema serap filiz dilek gül gülay leyla melek nur neslihan selin şeyma tülay yeliz aslı aynur canan
didem duygu ece gizem hande ipek irem melike nazlı nilay özge rabia sinem tuba yağmur buse cansu damla dilara ezgi""".split())

def yalniz_ad(metin):
    t = (metin or "").strip().replace("İ", "i").replace("I", "ı").lower().split()
    return 2 <= len(t) <= 4 and t[0] in ADLAR and all(w.isalpha() for w in t)
