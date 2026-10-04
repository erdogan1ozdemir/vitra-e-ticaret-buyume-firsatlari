# -*- coding: utf-8 -*-
"""Alt sayfalar: genis veri setleri (arama sonuclari, kelime evreni, pazaryeri taramasi, YouTube).
Ana raporun icindekilerinde yer almaz; ust bardaki veri seti dugmeleriyle yeni sekmede acilir.
Her sayfa tek dosyadir: veri JSON olarak gomulur, tablo istemci tarafinda suzulur, siralanir ve sayfalanir.
Kisisel veri yoktur: yorumcu / soru soran / sikayet eden adi tasinmaz; satici ve kanal adlari isletme adidir."""
import json, os, html, re, csv, collections
import veri
from rapor_parca1 import VITRA, INBOUND
from ortak import ek

ANA = "VitrA_E-Ticaret_Buyume_Firsatlari.html"
E = html.escape

# ust bar ve sayfalar arasi gezinme: (dosya, TR ad, EN ad, ikon yolu)
SETLER = [
    ("yorum-soru-seti.html", "Pazaryeri Yorumları", "Marketplace Reviews", '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>'),
    ("arama-sonuclari.html", "Arama Sonuçları", "Search Results", '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>'),
    ("kelime-evreni.html", "Kelime Evreni", "Keyword Universe", '<path d="M4 7h16M4 12h10M4 17h13"/>'),
    ("pazaryeri-taramasi.html", "Pazaryeri Taraması", "Marketplace Scan", '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/>'),
    ("youtube-videolari.html", "YouTube Videoları", "YouTube Videos", '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="m10 9 5 3-5 3z"/>'),
    ("geo-promptlari.html", "GEO Promptları", "GEO Prompts", '<path d="M12 3l1.9 4.6L18.5 9l-4.6 1.9L12 15.5l-1.9-4.6L5.5 9l4.6-1.4z"/><path d="M19 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>'),
]


def T(tr, en):
    return '<span data-l="tr">%s</span><span data-l="en">%s</span>' % (tr, en)


def tr_s(v, ond=0):
    s = ("%." + str(ond) + "f") % v
    a, _, b = s.partition(".")
    a = "{:,}".format(int(a)).replace(",", ".")
    return a + ("," + b if b else "")


def en_s(v, ond=0):
    return ("{:,.%df}" % ond).format(v)


def N(v, ond=0): return T(tr_s(v, ond), en_s(v, ond))
def P(v, ond=1): return T("%" + tr_s(v, ond), en_s(v, ond) + "%")


CSS = r"""
:root{--ink:#10332F;--ink-2:#2F4E4A;--muted:#5C6B69;--line:#E0DCD5;--bg:#FBFAF8;--card:#FFFFFF;--teal:#10332F;--coral:#FF7B52;
--coral-deep:#E85F36;--coral-tint:#FFE3D8;--green:#2E7D32;--green-wash:#C8E6C9;--red:#D32F2F;--red-wash:#FFCDD2;--neutral:#F0EDE8;--zebra:#FAF8F5;
--f:"Segoe UI",Arial,Helvetica,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#EDEAE4;--ink-2:#CFD8D5;--muted:#9AA8A5;--line:#2A3E3B;--bg:#0C1917;--card:#12211F;--teal:#0B2523;--neutral:#1A2A28;--coral-tint:#3A241D;--green-wash:#1E3A24;--red-wash:#3E1F1F;--zebra:#152624}}
:root[data-theme="dark"]{--ink:#EDEAE4;--ink-2:#CFD8D5;--muted:#9AA8A5;--line:#2A3E3B;--bg:#0C1917;--card:#12211F;--teal:#0B2523;--neutral:#1A2A28;--coral-tint:#3A241D;--green-wash:#1E3A24;--red-wash:#3E1F1F;--zebra:#152624}
*{box-sizing:border-box}
html[lang="tr"] [data-l="en"],html[lang="en"] [data-l="tr"]{display:none}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 var(--f);-webkit-font-smoothing:antialiased;overflow-x:clip}
a{color:var(--coral-deep)}
.appbar{position:sticky;top:0;z-index:40;background:var(--teal);border-bottom:1px solid rgba(255,255,255,.1)}
.appbar .in{max-width:1400px;margin:0 auto;padding:12px 22px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.bb{display:flex;align-items:center;gap:11px;min-width:0}
.logo-card{background:#fff;border-radius:5px;padding:5px 10px;display:flex;align-items:center}
.logo-card img{height:22px;width:auto;display:block}
.ib img{height:22px;width:auto;display:block;filter:brightness(0) invert(1)}
.geri{color:#fff;text-decoration:none;font-size:12.5px;font-weight:600;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);border-radius:6px;padding:6px 10px;white-space:nowrap}
.geri:hover,.geri:focus-visible{background:rgba(255,255,255,.2)}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:5px;height:32px;min-width:32px;padding:0 9px;border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);color:#fff;font:650 11.5px/1 var(--f);letter-spacing:.04em}
.btn:hover{background:rgba(255,255,255,.2)}
.btn:focus-visible,.geri:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.btn svg{width:15px;height:15px}
#tema .ay{display:none}:root[data-theme="dark"] #tema .ay{display:block}:root[data-theme="dark"] #tema .gunes{display:none}
main{max-width:1320px;margin:0 auto;padding:26px 22px 60px}
.setnav{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 18px}
.setnav a{font-size:12.5px;padding:5px 12px;border-radius:999px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);text-decoration:none;white-space:nowrap}
.setnav a:hover{border-color:var(--coral-deep);color:var(--coral-deep)}
.setnav a[aria-current="page"]{background:var(--teal);border-color:var(--teal);color:#fff}
:root[data-theme="dark"] .setnav a[aria-current="page"]{background:var(--coral-deep);border-color:var(--coral-deep)}
.eyebrow{font-size:11px;letter-spacing:.14em;color:var(--coral-deep);font-weight:700;margin:0 0 6px}
h1{font-size:clamp(23px,3.4vw,32px);line-height:1.2;margin:0 0 10px;text-wrap:balance}
.lede{color:var(--ink-2);max-width:96ch;margin:0 0 18px}
h2{font-size:21px;margin:40px 0 6px;padding-bottom:0;border-bottom:1px solid var(--line)}
h2 .h2i{display:inline-block;padding-bottom:8px;margin-bottom:-1px;border-bottom:3px solid var(--coral-deep)}
.h2n{color:var(--ink-2);font-size:13.5px;margin:8px 0 12px;max-width:110ch}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:8px 0 6px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.kpi .v{font-size:24px;font-weight:700;font-variant-numeric:tabular-nums}
.kpi .k{font-size:12.5px;color:var(--muted);line-height:1.4}
.filtre{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0 10px}
.filtre select,.filtre input{font:inherit;font-size:13px;padding:6px 10px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);max-width:100%}
.filtre input[type=search]{min-width:220px;flex:1 1 240px}
.filtre .sifirla,.csv{font:inherit;font-size:12.5px;padding:6px 12px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink-2);cursor:pointer}
.filtre .sifirla:hover,.csv:hover{border-color:var(--coral-deep);color:var(--coral-deep)}
.say{font-size:12.5px;color:var(--muted);margin:0 0 8px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.tw{overflow:auto;background:var(--card);border:1px solid var(--line);border-radius:10px;max-height:72vh}
.tb{width:100%;border-collapse:collapse;font-size:13px;min-width:860px}
.tb th{position:sticky;top:0;z-index:2;background:var(--teal);color:#fff;font-weight:600;font-size:12px;text-align:left;padding:9px 10px;white-space:nowrap;cursor:pointer;user-select:none}
.tb th .q{border-bottom:1px dotted rgba(255,255,255,.55);cursor:help}
.tb th::after{content:" \2195";opacity:.45;font-size:10px}
.tb th[aria-sort="ascending"]::after{content:" \25B2";opacity:1;color:var(--coral)}
.tb th[aria-sort="descending"]::after{content:" \25BC";opacity:1;color:var(--coral)}
.tb th:focus-visible{outline:2px solid var(--coral);outline-offset:-2px}
.tb td{padding:7px 10px;border-top:1px solid var(--line);vertical-align:top}
.tb tbody tr:nth-child(even) td{background:var(--zebra)}
.tb tr.vg td{background:var(--coral-tint)!important}
.tb .n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.tb th.n{text-align:right}
.tb td.uz{min-width:260px}
.tb td.kw{white-space:nowrap}
.tb td.cv{min-width:170px}
.tb td.uz2{min-width:420px;max-width:640px}
.tb td.uz2 summary{cursor:pointer;color:var(--ink-2)}
.tb td.uz2 summary:hover{color:var(--coral-deep)}
.tb td.uz2 .ym{white-space:pre-wrap;margin-top:8px;padding:10px 12px;background:var(--neutral);border-radius:8px;font-size:12.5px;line-height:1.55;max-height:420px;overflow:auto}
.tb .u{text-decoration:none}.tb .u:hover{text-decoration:underline}
.tb .bos{color:var(--muted)}
.etk{display:inline-block;font-size:11.5px;padding:1px 8px;border-radius:999px;background:var(--neutral);color:var(--ink-2);white-space:nowrap}
.etk.e1{background:#E3F0EE;color:#10332F}.etk.e2{background:#FFE3D8;color:#B4451F}.etk.e3{background:#E8E4F5;color:#4B3B8F}.etk.e4{background:#FFF1D6;color:#8A5A00}
.etk.e5{background:#DDEBF7;color:#1D4F7A}.etk.e6{background:#F3E1EA;color:#8A2D5A}.etk.e7{background:#E2F1DD;color:#2E6B23}.etk.e8{background:#ECEAE6;color:#4A4A4A}
:root[data-theme="dark"] .etk{filter:brightness(.85) saturate(.9)}
.dahafazla{font:inherit;font-size:13px;margin:12px auto 0;display:block;padding:8px 16px;border-radius:8px;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer}
.ins{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:12px 14px;margin:12px 0;font-size:14px}
.ins::before{content:"➔ ";color:var(--coral-deep);font-weight:700}
.note{background:var(--neutral);border-radius:10px;padding:12px 14px;margin:22px 0 12px;font-size:13.5px}
.note b{color:var(--coral-deep)}
li::marker{color:#E85F36}
#tt{position:fixed;z-index:99;max-width:320px;background:var(--ink);color:var(--bg);font-size:12.5px;line-height:1.45;padding:8px 10px;border-radius:8px;pointer-events:none;opacity:0;transition:opacity .12s}
#tt.on{opacity:1}
footer{max-width:1320px;margin:0 auto;padding:10px 22px 40px;font-size:12px;color:var(--muted)}
@media(max-width:720px){.ib{display:none}.appbar .in{padding:10px 16px;gap:8px}main{padding:18px 16px 50px}.filtre input[type=search]{min-width:0}.tw{max-height:none}}
@media(max-width:520px){.geri .uzun{display:none}.kpi .v{font-size:20px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important;transition:none!important}}
@media print{.appbar,.filtre,.dahafazla,.setnav,.csv{display:none}.tw{overflow:visible;max-height:none}}
"""

JS = r"""
(function(){
var V=JSON.parse(document.getElementById('veri').textContent),kok=document.documentElement,D=V.cev||{};
function dil(){return kok.lang==='en'?'en':'tr'}
function esc(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;')}
function T(tr,en){return dil()==='en'?en:tr}
function cv(s){if(s==null||s==='')return '';return dil()==='en'?(D[s]!=null?D[s]:s):s}
function sayi(v,o){if(v==null||v==='')return '';o=o||0;return Number(v).toLocaleString(dil()==='en'?'en-US':'tr-TR',{minimumFractionDigits:o,maximumFractionDigits:o})}
function yuzde(v,o){if(v==null||v==='')return '';var s=sayi(Math.abs(v),o==null?1:o),i=v>0?'+':(v<0?'-':'');return dil()==='en'?i+s+'%':i+'%'+s}
var ETK={};function etk(k,v){var a=k+'|'+v;if(!(a in ETK)){var n=Object.keys(ETK).filter(function(x){return x.indexOf(k+'|')===0}).length;ETK[a]=n%8+1}return '<span class="etk e'+ETK[a]+'">'+esc(cv(v))+'</span>'}
function once(s){if(!s||dil()!=='en')return s;var m=String(s).match(/^(\d+)\s+(yıl|ay|hafta|gün|saat|dakika)\s+önce$/);if(!m)return s;var u={'yıl':'year','ay':'month','hafta':'week','gün':'day','saat':'hour','dakika':'minute'}[m[2]];return m[1]+' '+u+(m[1]==='1'?'':'s')+' ago'}
function hucre(c,v){
 if(v==null||v===''){return '<td class="'+(c.n?'n ':'')+'bos">-</td>'}
 switch(c.tip){
  case 'sayi':return '<td class="n">'+sayi(v,c.o||0)+'</td>';
  case 'para':return '<td class="n">'+(dil()==='en'?'TRY ':'')+sayi(v,0)+(dil()==='en'?'':' TL')+'</td>';
  case 'yuzde':return '<td class="n">'+yuzde(v,c.o)+'</td>';
  case 'oran':return '<td class="n">'+(dil()==='en'?sayi(v,c.o==null?1:c.o)+'%':'%'+sayi(v,c.o==null?1:c.o))+'</td>';
  case 'uzun':var k=String(v),o=k.replace(/\s+/g,' ').slice(0,170);return '<td class="uz2"><details><summary>'+esc(o)+(k.length>170?'…':'')+'</summary><div class="ym">'+esc(k)+'</div></details></td>';
  case 'link':return '<td class="'+(c.uz?'uz':'')+'"><a class="u" href="'+esc(v[1])+'" target="_blank" rel="noopener">'+esc(v[0])+'</a></td>';
  case 'kat':return '<td>'+etk(c.k,v)+'</td>';
  case 'cev':return '<td class="cv">'+esc(cv(v))+'</td>';
  case 'once':return '<td class="n">'+esc(once(v))+'</td>';
  case 'kw':return '<td class="kw">'+esc(v)+'</td>';
  default:return '<td class="'+(c.uz?'uz':'')+'">'+esc(v)+'</td>'}}
function metinDeger(c,v){if(v==null)return '';if(c.tip==='link')return v[0];if(c.tip==='kat'||c.tip==='cev')return v+' '+cv(v);return String(v)}
function Tablo(el){
 var t=V.t[el.dataset.t],cols=t.c,rows=t.r,adim=100,goster=adim,sk=t.s?t.s[0]:null,sy=t.s?t.s[1]:'d';
 var vg=t.vg;
 var fb=el.querySelector('.filtre'),ara=fb.querySelector('input[type=search]'),sel={};
 cols.forEach(function(c,i){if(c.f){var s=document.createElement('select');s.dataset.i=i;s.setAttribute('aria-label',c.t[0]);fb.insertBefore(s,fb.querySelector('.sifirla'));sel[i]=s}});
 function secDoldur(){Object.keys(sel).forEach(function(i){var s=sel[i],c=cols[i],v=s.value,say={};rows.forEach(function(r){var x=r[i];if(x==null||x==='')return;var k=c.tip==='link'?x[0]:x;say[k]=(say[k]||0)+1});
  var ks=Object.keys(say).sort(function(a,b){return say[b]-say[a]||String(cv(a)).localeCompare(String(cv(b)),dil())});
  s.innerHTML='<option value="">'+esc(T('Tümü: ','All: ')+(dil()==='en'?c.t[1]:c.t[0]))+'</option>'+ks.map(function(k){return '<option value="'+esc(k)+'">'+esc(cv(k))+' ('+sayi(say[k])+')</option>'}).join('');s.value=v})}
 var thead=el.querySelector('thead tr');
 function basliklar(){thead.innerHTML=cols.map(function(c,i){var a=dil()==='en'?c.a[1]:c.a[0];return '<th tabindex="0" data-i="'+i+'" class="'+(c.n?'n':'')+'"'+(sk===i?' aria-sort="'+(sy==='a'?'ascending':'descending')+'"':'')+' data-tt="'+esc(a)+'"><span class="q">'+esc(dil()==='en'?c.t[1]:c.t[0])+'</span></th>'}).join('')}
 function suz(){var q=(ara.value||'').toLocaleLowerCase('tr'),fs=Object.keys(sel).filter(function(i){return sel[i].value!==''});
  return rows.filter(function(r){for(var j=0;j<fs.length;j++){var i=fs[j],x=r[i],k=cols[i].tip==='link'?(x&&x[0]):x;if(String(k)!==sel[i].value)return false}
   if(!q)return true;for(var i=0;i<cols.length;i++){if(metinDeger(cols[i],r[i]).toLocaleLowerCase('tr').indexOf(q)>=0)return true}return false})}
 function sirali(L){if(sk==null)return L;var c=cols[sk];return L.slice().sort(function(a,b){var x=a[sk],y=b[sk];if(c.tip==='link'){x=x&&x[0];y=y&&y[0]}
  if(x==null||x==='')return 1;if(y==null||y==='')return -1;var r=(typeof x==='number'&&typeof y==='number')?x-y:String(cv(x)).localeCompare(String(cv(y)),dil());return sy==='a'?r:-r})}
 var tb=el.querySelector('tbody'),sayEl=el.querySelector('.sayac'),daha=el.querySelector('.dahafazla'),son=[];
 function ciz(){son=sirali(suz());tb.innerHTML=son.slice(0,goster).map(function(r){return '<tr'+(vg!=null&&r[vg]?' class="vg"':'')+'>'+cols.map(function(c,i){return hucre(c,r[i])}).join('')+'</tr>'}).join('');
  sayEl.textContent=T(sayi(son.length)+' / '+sayi(rows.length)+' satır'+(son.length>goster?' · ilk '+sayi(goster)+' satır gösteriliyor':''),sayi(son.length)+' / '+sayi(rows.length)+' rows'+(son.length>goster?' · showing the first '+sayi(goster):''));
  daha.hidden=son.length<=goster}
 ara.addEventListener('input',function(){goster=adim;ciz()});
 Object.keys(sel).forEach(function(i){sel[i].addEventListener('input',function(){goster=adim;ciz()})});
 fb.querySelector('.sifirla').addEventListener('click',function(){ara.value='';Object.keys(sel).forEach(function(i){sel[i].value=''});goster=adim;ciz()});
 daha.addEventListener('click',function(){goster+=adim*5;ciz()});
 thead.addEventListener('click',function(e){var th=e.target.closest('th');if(!th)return;var i=+th.dataset.i;if(sk===i){sy=sy==='a'?'d':'a'}else{sk=i;sy=cols[i].n?'d':'a'}basliklar();ciz()});
 thead.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){var th=e.target.closest('th');if(th){e.preventDefault();th.click()}}});
 el.querySelector('.csv').addEventListener('click',function(){
  var L=[cols.map(function(c){return dil()==='en'?c.t[1]:c.t[0]})].concat(son.map(function(r){return cols.map(function(c,i){var v=r[i];if(v==null)return '';if(c.tip==='link')return v[0]+' ('+v[1]+')';if(c.tip==='kat'||c.tip==='cev')return cv(v);if(c.tip==='once')return once(v);return v})}));
  var s='﻿'+L.map(function(r){return r.map(function(v){v=String(v);return /[";\n,]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v}).join(';')}).join('\n');
  var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([s],{type:'text/csv;charset=utf-8'}));a.download=el.dataset.t+'.csv';document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove()},500)});
 this.dil=function(){ara.placeholder=T('Tabloda ara','Search the table');basliklar();secDoldur();ciz()};
}
var TB=[].map.call(document.querySelectorAll('.vt'),function(el){return new Tablo(el)});
/* sutun aciklama balonu */
var tt=document.getElementById('tt');
function goster(el){var s=el.getAttribute('data-tt');if(!s)return;tt.textContent=s;tt.classList.add('on');var r=el.getBoundingClientRect(),w=tt.offsetWidth,h=tt.offsetHeight;
 var x=Math.min(Math.max(8,r.left+r.width/2-w/2),window.innerWidth-w-8),y=r.top-h-8;if(y<8)y=r.bottom+8;tt.style.left=x+'px';tt.style.top=y+'px'}
function gizle(){tt.classList.remove('on')}
document.addEventListener('mouseover',function(e){var el=e.target.closest('[data-tt]');if(el)goster(el);else gizle()});
document.addEventListener('focusin',function(e){var el=e.target.closest('[data-tt]');if(el)goster(el)});
document.addEventListener('focusout',gizle);window.addEventListener('scroll',gizle,true);
/* dil ve tema */
function dilKur(l){kok.lang=l;document.getElementById('dil').querySelector('b').textContent=l==='en'?'TR':'EN';document.title=l==='en'?V.baslik[1]:V.baslik[0];TB.forEach(function(t){t.dil()})}
document.getElementById('dil').addEventListener('click',function(){var l=dil()==='en'?'tr':'en';try{localStorage.setItem('vitra-dil',l)}catch(e){}dilKur(l)});
document.getElementById('tema').addEventListener('click',function(){var d=kok.getAttribute('data-theme')==='dark'?'light':'dark';kok.setAttribute('data-theme',d);try{localStorage.setItem('vitra-tema',d)}catch(e){}});
try{var t0=localStorage.getItem('vitra-tema');if(t0)kok.setAttribute('data-theme',t0)}catch(e){}
var l0='tr';try{l0=localStorage.getItem('vitra-dil')||'tr'}catch(e){}
dilKur(l0==='en'?'en':'tr');
})();
"""

TEMA_BTN = ('<button class="btn" type="button" id="tema" aria-label="Tema değiştir" title="Tema değiştir"><svg class="gunes" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="4"/>'
            '<path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg><svg class="ay" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>')
DIL_BTN = '<button class="btn" type="button" id="dil" aria-label="Dil / Language"><b>EN</b></button>'


def setnav(aktif):
    return '<nav class="setnav" aria-label="Veri setleri">%s</nav>' % "".join(
        '<a href="%s"%s>%s</a>' % (f, ' aria-current="page"' if f == aktif else "", T(tr, en)) for f, tr, en, _ in SETLER)


def kolon(k, tr, en, a_tr, a_en, tip="metin", f=False, uz=False, o=0):
    """Tablo sutunu: k anahtar, tip metin|kw|sayi|para|yuzde|link|kat|cev|once; f suzgec; uz genis metin."""
    return {"k": k, "t": [tr, en], "a": [a_tr, a_en], "tip": tip, "f": 1 if f else 0, "n": 1 if tip in ("sayi", "para", "yuzde", "oran", "once") else 0, "uz": 1 if uz else 0, "o": o}


def tablo_html(anah):
    return ('<div class="vt" data-t="%s"><div class="filtre"><input type="search" aria-label="Ara">'
            '<button class="sifirla" type="button">%s</button></div>'
            '<div class="say"><span class="sayac"></span><button class="csv" type="button">%s</button></div>'
            '<div class="tw"><table class="tb"><thead><tr></tr></thead><tbody></tbody></table></div>'
            '<button class="dahafazla" type="button">%s</button></div>') % (anah, T("Süzgeçleri temizle", "Clear filters"), T("Görünen satırları CSV indir", "Download visible rows as CSV"), T("Daha fazla göster", "Show more"))


def sayfa(dosya, baslik, eyebrow, h1, lede, kpis, bolumler, tablolar, cev, yontem, kaynak):
    """bolumler: [(id, (h2 tr, en), (not tr, en), tablo anahtari, (insight tr, en) | None)]"""
    eksik = sorted({v for t in tablolar.values() for i, c in enumerate(t["c"]) if c["tip"] in ("kat", "cev")
                    for r in t["r"] for v in [r[i]] if v not in (None, "") and v not in cev})
    if eksik:
        raise SystemExit("%s · çevirisi olmayan değer: %s" % (dosya, eksik[:40]))
    govde = ""
    for id_, h2, not_, tk, ins in bolumler:
        govde += '<h2 id="%s"><span class="h2i">%s</span></h2><p class="h2n">%s</p>%s%s' % (
            id_, T(*h2), T(*not_), tablo_html(tk), ('<p class="ins">%s</p>' % T(*ins)) if ins else "")
    kpi = "".join('<div class="kpi"><div class="v">%s</div><div class="k">%s</div></div>' % (v, T(*k)) for v, k in kpis)
    VJ = json.dumps({"t": tablolar, "cev": {k: v for k, v in cev.items() if k != v}, "baslik": [baslik[0], baslik[1]]},
                    ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("—", "-").replace("–", "-")   # urun ve video adlarindaki uzun tireler
    doc = """<!doctype html>
<html lang="tr" data-theme="light"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>%(title)s</title><style>%(css)s</style></head><body>
<header class="appbar"><div class="in">
 <div class="bb"><span class="logo-card"><img src="%(vitra)s" alt="VitrA"></span>
  <a class="geri" href="%(ana)s">← <span class="uzun">%(geri)s</span></a></div>
 <div class="bb">%(dilb)s%(temab)s<span class="ib"><img src="%(inb)s" alt="Inbound"></span></div>
</div></header>
<main>
%(nav)s
<p class="eyebrow">%(eyebrow)s</p>
<h1>%(h1)s</h1>
<p class="lede">%(lede)s</p>
<div class="kpis">%(kpi)s</div>
%(govde)s
<div class="note"><b>%(yb)s</b> %(yontem)s</div>
</main>
<footer>%(kaynak)s</footer>
<div id="tt" role="tooltip"></div>
<script type="application/json" id="veri">%(veri)s</script>
<script>%(js)s</script>
</body></html>""" % {"title": E(baslik[0]), "css": CSS, "vitra": VITRA, "ana": ANA, "geri": T("Rapora dön", "Back to the report"), "dilb": DIL_BTN, "temab": TEMA_BTN,
                     "inb": INBOUND, "nav": setnav(dosya), "eyebrow": T(*eyebrow), "h1": T(*h1), "lede": T(*lede), "kpi": kpi, "govde": govde,
                     "yb": T("Yöntem:", "Method:"), "yontem": T(*yontem), "kaynak": T(*kaynak), "veri": VJ, "js": JS}
    if "—" in doc:
        raise SystemExit("%s · em dash var" % dosya)
    yol = os.path.join(veri.KOK, dosya)
    open(yol, "w", encoding="utf-8").write(doc)
    print("kaydedildi:", yol, len(doc), "karakter ·", sum(len(t["r"]) for t in tablolar.values()), "satır")
    return yol


# ====================================================================== 1. arama sonuclari
TEMA = {"SSG": ("SSG (vitrifiye)", "SSG (sanitaryware)"), "BM": ("Banyo mobilyası", "Bathroom furniture"), "Armatür-duş": ("Armatür ve duş", "Taps and showers"),
        "Yıkanma": ("Yıkanma alanları", "Bathing areas"), "Bitişik": ("Bitişik ürünler", "Adjacent products"), "Hizmet": ("Hizmet ve ilham", "Services and inspiration"),
        "Karo": ("Karo", "Tiles"), "Soru": ("Soru", "Questions"), "Marka": ("Marka", "Brand")}
TIP = {"kategori": "Category page", "pazaryeri arama/liste": "Marketplace search / listing", "sosyal/görsel": "Social / visual", "forum/şikayet": "Forum / complaint",
       "ürün": "Product page", "blog/rehber": "Blog / guide", "video": "Video", "pazaryeri ürün": "Marketplace product", "hizmet platformu": "Service platform"}
TIP_TR = {"kategori": "Kategori sayfası", "pazaryeri arama/liste": "Pazaryeri arama / liste", "sosyal/görsel": "Sosyal / görsel", "forum/şikayet": "Forum / şikayet",
          "ürün": "Ürün sayfası", "blog/rehber": "Blog / rehber", "video": "Video", "pazaryeri ürün": "Pazaryeri ürün sayfası", "hizmet platformu": "Hizmet platformu"}


def arama_sonuclari():
    import serp_ozet as S
    from b_serp import TEMA_EN
    tr_ = lambda t: ".".join(reversed(t.split("-")))
    TRH = tr_(S.TARIH)
    GRP = {g: "%s · %s" % (g, S.GRUP_AD[g][0]) for g in "ABC"}
    cev = {t: e for t, e in TEMA_EN.items() if t != e}
    cev.update({"%s · %s" % (g, S.GRUP_AD[g][0]): "%s · %s" % (g, S.GRUP_AD[g][1]) for g in "ABC"})
    cev.update({TIP_TR[k]: TIP[k] for k in TIP})
    AI = {"yok": ("Çıkmadı", "Did not appear"), "var": ("Çıktı, VitrA kaynak değil", "Appeared, VitrA not cited"), "vitra": ("Çıktı, VitrA kaynak", "Appeared, VitrA cited"),
          "icerik_yok": ("Çıktı, içerik alınamadı", "Appeared, content not retrieved")}
    cev.update({a: b for a, b in AI.values()})
    def ai_d(r):
        if not r.get("ai_ilk_cekim"): return AI["yok"][0]
        if not r.get("ai"): return AI["icerik_yok"][0]
        return AI["vitra"][0] if "vitra.com.tr" in (r["ai"].get("ref_alanlar") or []) else AI["var"][0]
    K, ILK, AIK = [], [], []
    for r in sorted(S.TUM, key=lambda r: (r["grup"], -r["hacim"])):
        top = sorted(r["top10"], key=lambda z: z["sira"])
        g = r.get("gsc") or {}
        K.append([r["kelime"], GRP[r["grup"]], r["tema"], r["hacim"], r.get("vitra_sira"), g.get("sira"), g.get("tik"),
                  top[0]["alan"] if top else None, " · ".join(z["alan"] for z in top[:3]), ai_d(r), len(r.get("paa") or []), 1 if (r.get("vitra_sira") or 99) <= 3 else 0])
        for z in top:
            ILK.append([r["kelime"], r["tema"], z["sira"], z["alan"], TIP_TR.get(z["tip"], z["tip"]), [z["url"].replace("https://", "").replace("http://", "")[:90], z["url"]], 1 if z["alan"] == "vitra.com.tr" else 0])
        if r.get("ai"):
            for d in dict.fromkeys(r["ai"].get("ref_alanlar") or []):
                AIK.append([r["kelime"], r["tema"], d, r.get("vitra_sira"), 1 if d == "vitra.com.tr" else 0])
    PQ = collections.defaultdict(list)
    for r in S.TUM:
        for q in r.get("paa") or []: PQ[q].append(r["kelime"])
    PT = {"fiyat": ("Fiyat", "Price"), "bilgi": ("Nedir / nasıl", "What / how"), "vitra": ("VitrA adıyla", "Naming VitrA"), "diger": ("Diğer", "Other")}
    cev.update({a: b for a, b in PT.values()})
    def ptip(q):
        if "vitra" in q.lower(): return PT["vitra"][0]
        if S._FIYAT.search(q): return PT["fiyat"][0]
        if S._BILGI.search(q): return PT["bilgi"][0]
        return PT["diger"][0]
    PAA = [[q, ptip(q), ", ".join(PQ[q][:4]) + (" +%d" % (len(PQ[q]) - 4) if len(PQ[q]) > 4 else ""), len(PQ[q])] for q in S.PAA_SORU]
    PAA.sort(key=lambda r: (-r[3], r[0]))
    tb = {
        "kelime": {"c": [kolon("kelime", "Kelime", "Keyword", "Google'da aranan ifade; kullanıcının yazdığı biçimde korunmuştur.", "The search term on Google, kept as the user types it.", "kw"),
                         kolon("grup", "Grup", "Group", "A · VitrA gamı (VitrA'nın sattığı kategoriler), B · yakın kategori fırsatları (VitrA'nın satmadığı ya da kısmen sattığı ürünler), C · marka ve karşılaştırma aramaları.", "A · VitrA range (categories VitrA sells), B · adjacent category opportunities (products VitrA does not sell or sells partly), C · brand and comparison searches.", "kat", True),
                         kolon("tema", "Kategori / tema", "Category / theme", "Kelimenin kategorisi (A), teması (B) ya da marka arama türü (C).", "Category (A), theme (B) or brand search type (C) of the keyword.", "kat", True),
                         kolon("hacim", "Aylık hacim", "Monthly volume", "Google Keyword Planner ortalama aylık arama hacmi, Eyl 2025 - Ağu 2026.", "Google Keyword Planner average monthly search volume, Sep 2025 - Aug 2026.", "sayi"),
                         kolon("vsira", "VitrA sırası", "VitrA position", "vitra.com.tr'nin mobil sırası (ilk 20): SEOmonitor günlük takibi 03.10.2026; takip dışı kelimelerde %s SERP gözlemi; boş: ilk 20'de yok." % TRH, "vitra.com.tr mobile position (top 20): SEOmonitor daily tracking 03.10.2026; SERP observation of %s for untracked keywords; blank: not in the top 20." % TRH, "sayi"),
                         kolon("gsira", "Search Console sırası", "Search Console position", "Search Console ortalama sırası, 1 Tem - 30 Eyl 2026, tüm cihazlar.", "Search Console average position, 1 Jul - 30 Sep 2026, all devices.", "sayi", o=1),
                         kolon("gtik", "Search Console click", "Search Console clicks", "Aynı dönemde bu sorgudan vitra.com.tr'ye gelen click.", "Clicks from this query to vitra.com.tr in the same period.", "sayi"),
                         kolon("bir", "1. sıradaki alan adı", "Domain in 1st place", "Mobil arama sonucunda ilk sıradaki organik sonucun alan adı.", "Domain of the first organic result in the mobile results.", "metin", True),
                         kolon("ilk3", "İlk 3 alan adı", "Top 3 domains", "İlk üç organik sonucun alan adları, sırasıyla.", "Domains of the first three organic results, in order.", "metin", uz=True),
                         kolon("ai", "AI Overview", "AI Overview", "Kelimede Google AI Overview çıkıp çıkmadığı ve vitra.com.tr'nin kaynak gösterilip gösterilmediği.", "Whether a Google AI Overview appeared and whether vitra.com.tr was cited.", "kat", True),
                         kolon("paa", "Diğer sorular", "People also ask", "Sonuç sayfasındaki \"Diğer sorular\" kutusunda listelenen soru sayısı.", "Number of questions in the \"People also ask\" box on the results page.", "sayi")],
                   "r": [r[:11] for r in K], "s": None},
        "ilk10": {"c": [kolon("kelime", "Kelime", "Keyword", "Google'da aranan ifade.", "The search term on Google.", "kw"),
                        kolon("tema", "Tema", "Theme", "Kelimenin teması.", "The keyword's theme.", "kat", True),
                        kolon("sira", "Sıra", "Position", "Organik sonuç sırası (1-10), %s mobil." % TRH, "Organic result position (1-10), mobile, %s." % TRH, "sayi"),
                        kolon("alan", "Alan adı", "Domain", "Sonucun alan adı.", "Domain of the result.", "metin", True),
                        kolon("tip", "Sayfa tipi", "Page type", "Sonuç sayfasının türü: kategori, pazaryeri arama veya liste, ürün, rehber, video, sosyal ve diğerleri.", "Type of the result page: category, marketplace search or listing, product, guide, video, social and others.", "kat", True),
                        kolon("url", "Adres", "URL", "Sonucun tam adresi; bağlantı sayfayı yeni sekmede açar.", "Full URL of the result; the link opens the page in a new tab.", "link", uz=True)],
                  "r": [r[:6] for r in ILK], "vg": None, "s": None},
        "paa": {"c": [kolon("soru", "Soru", "Question", "Google'ın \"Diğer sorular\" kutusundaki soru; olduğu gibi korunmuştur.", "The question in Google's \"People also ask\" box, kept as is.", "kw"),
                      kolon("tip", "Soru tipi", "Question type", "Fiyat ifadesi (kaç TL, ne kadar), bilgi ifadesi (nedir, nasıl) ya da VitrA adı içeren sorular.", "Questions with price wording (how much), information wording (what, how) or naming VitrA.", "kat", True),
                      kolon("kel", "Çıktığı kelimeler", "Keywords where it appeared", "Sorunun çıktığı arama kelimeleri (en fazla dördü yazılmıştır).", "Search keywords where the question appeared (up to four listed).", "metin", uz=True),
                      kolon("n", "Kelime sayısı", "Keyword count", "Sorunun çıktığı kelime sayısı.", "Number of keywords where the question appeared.", "sayi")],
                "r": PAA, "s": [3, "d"]},
        "aik": {"c": [kolon("kelime", "Kelime", "Keyword", "AI Overview'un çıktığı ve içeriği alınabilen arama kelimesi.", "Search keyword where an AI Overview appeared and its content was retrieved.", "kw"),
                      kolon("tema", "Tema", "Theme", "Kelimenin teması.", "The keyword's theme.", "kat", True),
                      kolon("alan", "Kaynak alan adı", "Cited domain", "AI Overview'da kaynak olarak bağlantı verilen alan adı.", "Domain linked as a source in the AI Overview.", "metin", True),
                      kolon("vs", "VitrA organik sırası", "VitrA organic position", "Aynı kelimede vitra.com.tr'nin organik sırası; boş: ilk 20'de yok.", "vitra.com.tr's organic position for the same keyword; blank: not in the top 20.", "sayi")],
                "r": [r[:4] for r in AIK], "s": None},
    }
    tb["ilk10"]["vg"] = None
    for k, L in (("kelime", K), ("ilk10", ILK), ("aik", AIK)):
        vgi = len(tb[k]["c"])
        for r_, src in zip(tb[k]["r"], L): r_.append(src[-1])
        tb[k]["vg"] = vgi
    sayfa("arama-sonuclari.html", ("VitrA | Arama Sonuçları Seti", "VitrA | Search Results Set"),
          ("VitrA TÜRKİYE · GOOGLE ARAMA SONUÇLARI", "VitrA TURKEY · GOOGLE SEARCH RESULTS"),
          ("Arama Sonuçları Seti: %d Kelime, İlk 10 Sonuç, AI Overview ve Diğer Sorular" % S.NT, "Search Results Set: %d Keywords, Top 10 Results, AI Overview and People Also Ask" % S.NT),
          ("Google Türkiye mobil arama sonuçlarında %d kelimenin ilk 10 organik sonucu, AI Overview kaynakları ve \"Diğer sorular\" kutusu; gözlem tarihi %s. Kelimeler üç grupta toplanmıştır: A · VitrA gamı (VitrA'nın sattığı her alt kategoriden en az bir baş kelime), B · yakın kategori fırsatları ve C · marka ve karşılaştırma aramaları. Google Keyword Planner'da arama hacmi olmayan kelimeler alınmamıştır. Search Console sütunları vitra.com.tr'nin aynı kelimelerdeki ortalama sırasını ve click'ini gösterir. vitra.com.tr'nin ilk 3'te olduğu satırlar vurgulanmıştır." % (S.NT, TRH),
           "The top 10 organic results, AI Overview sources and the \"People also ask\" box for %d keywords in Google Turkey mobile results; observed on %s. Keywords are grouped into three: A · VitrA range (at least one head keyword from each subcategory VitrA sells), B · adjacent category opportunities and C · brand and comparison searches. Keywords with no search volume in Google Keyword Planner were not included. The Search Console columns show vitra.com.tr's average position and clicks for the same keywords. Rows where vitra.com.tr is in the top 3 are highlighted." % (S.NT, TRH)),
          [(N(S.NT), ("kelime · A %d · B %d · C %d" % tuple(len(S.GRUP[g]) for g in "ABC"), "keywords · A %d · B %d · C %d" % tuple(len(S.GRUP[g]) for g in "ABC"))), (N(len(ILK)), ("ilk 10 organik sonuç satırı", "top-10 organic result rows")),
           (T("%d / %d" % (S.VITRA["ilk10"], S.N), "%d / %d" % (S.VITRA["ilk10"], S.N)), ("VitrA'nın ilk 10'da olduğu kelime (A grubu)", "keywords with VitrA in the top 10 (group A)")),
           (N(len(S.PAA_SORU)), ("benzersiz \"Diğer sorular\" sorusu", "unique \"People also ask\" questions")),
           (T("%d / %d" % (len(S.AI_VITRA), len(S.AI_ICERIK)), "%d / %d" % (len(S.AI_VITRA), len(S.AI_ICERIK))), ("VitrA'nın kaynak gösterildiği AI Overview", "AI Overviews citing VitrA"))],
          [("kelimeler", ("Kelimeler: hacim, VitrA sırası ve ilk 3 alan adı", "Keywords: volume, VitrA position and top 3 domains"),
            ("Her satır bir kelimedir. Grup, kategori ve AI Overview süzgeçleriyle daraltılabilir, sütun başlığına tıklanarak sıralanabilir; vitra.com.tr'nin ilk 3'te olduğu kelimeler vurgulanmıştır.", "Each row is a keyword. Narrow with the group, category and AI Overview filters, sort by clicking a column header; keywords where vitra.com.tr is in the top 3 are highlighted."), "kelime", None),
           ("ilk10", ("İlk 10 organik sonuç", "Top 10 organic results"),
            ("Her kelimenin ilk 10 organik sonucu; alan adı ve sayfa tipine göre süzülebilir, adres sayfayı yeni sekmede açar.", "The top 10 organic results for each keyword; filter by domain and page type, the URL opens the page in a new tab."), "ilk10", None),
           ("aio", ("AI Overview kaynakları", "AI Overview sources"),
            ("İçeriği alınabilen %d AI Overview bloğunda kaynak olarak bağlantı verilen alan adları; her satır bir kelime ve kaynak eşleşmesidir." % len(S.AI_ICERIK), "Domains linked as sources in the %d AI Overview blocks whose content could be retrieved; each row is a keyword and source pair." % len(S.AI_ICERIK)), "aik", None),
           ("paa", ("\"Diğer sorular\" kutusundaki sorular", "Questions in the \"People also ask\" box"),
            ("%d kelimede derlenen %d benzersiz soru; soru tipi süzgeci fiyat, bilgi ve VitrA adı içeren soruları ayırır." % (S.PAA_KELIME, len(S.PAA_SORU)), "%d unique questions collected across %d keywords; the question type filter separates price, information and VitrA questions." % (len(S.PAA_SORU), S.PAA_KELIME)), "paa", None)],
          tb, cev,
          ("Sonuçlar Google Türkiye, Türkçe, mobil (Android) için tek günlük gözlemdir ve gün içinde değişebilir. Sayfa tipi adres yapısından atanmıştır. Keyword Planner'da hacmi olmayan %d aday kelime alınmamıştır." % len(S.CIKAN),
           "Results are a single-day observation for Google Turkey, Turkish, mobile (Android) and may change within the day. Page type is assigned from the URL structure. %d candidate keywords with no Keyword Planner volume were not included." % len(S.CIKAN)),
          ("Kaynak: Google arama sonuçları, Türkiye, mobil · %s · Google Search Console sc-domain:vitra.com.tr, 1 Tem - 30 Eyl 2026 · Google Keyword Planner, Eyl 2025 - Ağu 2026" % TRH,
           "Source: Google search results, Turkey, mobile · %s · Google Search Console sc-domain:vitra.com.tr, 1 Jul - 30 Sep 2026 · Google Keyword Planner, Sep 2025 - Aug 2026" % TRH))


# ====================================================================== 2. kelime evreni
NIYET = {"Jenerik ürün": "Generic product", "Tasarım ve fikir": "Design and ideas", "Fiyat": "Price", "Ölçü ve teknik": "Size and technical", "Tamir ve bakım": "Repair and maintenance",
         "Montaj": "Installation", "Seçim ve karşılaştırma": "Selection and comparison"}
AC_GRUP = {"Kategori": "Category", "Montaj ve tamir": "Installation and repair", "Yenileme ve tasarım": "Renovation and design", "Fiyat ve ödeme": "Price and payment",
           "Rakip marka": "Competitor brand", "Perakendeci": "Retailer", "VitrA ile başlayan": "Starting with VitrA"}


K2_EN = {"Bide Bataryaları": "Bidet Mixers", "Diş Fırçalıkları": "Toothbrush Holders", "Duş Üniteleri": "Shower Units", "Ev İçi Zemin Karo Seramikleri": "Indoor Floor Tiles",
         "Porselen Karolar": "Porcelain Tiles", "Sürgülü El Duşu Takımları": "Sliding Hand Shower Sets", "Ticari & Endüstriyel Alan Karo Seramikleri": "Commercial & Industrial Tiles",
         "Vitrifiye Tamamlayıcıları": "Sanitaryware Complements"}


def kelime_evreni(EK):
    K = json.load(open(os.path.join(veri.V, "islenmis", "kelime_seti.json"), encoding="utf-8"))
    cev = dict(NIYET); cev.update({"Evet": "Yes", "Hayır": "No"}); cev.update(K2_EN)
    for r in K:
        for a in ("k1", "k2"):
            if r[a] not in cev and r[a] in EK: cev[r[a]] = EK[r[a]]
    R = []
    for r in sorted(K, key=lambda r: -(r["a26"] or 0)):
        d = (100 * (r["a26"] - r["a25"]) / r["a25"]) if r.get("a25") else None
        R.append([r["kw"], r["k1"], r["k2"], r["niyet"], "Evet" if r["markali"] else "Hayır", round(r["a26"] or 0), round(r["a25"] or 0), None if d is None else round(d, 1), r["hacim"]])
    A1 = json.load(open(os.path.join(veri.V, "ham", "autocomplete_ek.json"), encoding="utf-8"))
    A2 = json.load(open(os.path.join(veri.V, "ham", "autocomplete_youtube.json"), encoding="utf-8"))
    kg = {k: g for g, L in A1["grup"].items() for k in L}
    AC = []
    for kok_, L in A1["oneri"].items():
        for i, o in enumerate(L, 1): AC.append([kok_, kg.get(kok_, "Kategori"), i, o])
    for kok_, L in A2["autocomplete"].items():
        for i, o in enumerate(L, 1): AC.append([kok_, "VitrA ile başlayan", i, o])
    cev.update(AC_GRUP)
    a26 = sum(r[5] for r in R); a25 = sum(r[6] for r in R)
    tb = {"kel": {"c": [kolon("kw", "Kelime", "Keyword", "Google'da aranan ifade; kullanıcının yazdığı biçimde korunmuştur.", "The search term on Google, kept as the user types it.", "kw"),
                        kolon("k1", "Ana kategori", "Main category", "VitrA kategori ağacındaki ana kategori.", "Main category in VitrA's category tree.", "cev", True),
                        kolon("k2", "Alt kategori", "Subcategory", "VitrA kategori ağacındaki alt kategori.", "Subcategory in VitrA's category tree.", "cev", True),
                        kolon("niyet", "Niyet", "Intent", "Kelimenin arama niyeti: jenerik ürün, fiyat, tasarım ve fikir, ölçü ve teknik, montaj, tamir ve bakım, seçim ve karşılaştırma.", "Search intent: generic product, price, design and ideas, size and technical, installation, repair and maintenance, selection and comparison.", "kat", True),
                        kolon("marka", "Markalı", "Branded", "Kelimede marka adı geçiyor mu?", "Does the keyword contain a brand name?", "kat", True),
                        kolon("a26", "Ort. hacim 2025-26", "Avg. volume 2025-26", "Eyl 2025 - Ağu 2026 ortalama aylık arama hacmi, Google Keyword Planner.", "Average monthly search volume, Sep 2025 - Aug 2026, Google Keyword Planner.", "sayi"),
                        kolon("a25", "Ort. hacim 2024-25", "Avg. volume 2024-25", "Eyl 2024 - Ağu 2025 ortalama aylık arama hacmi.", "Average monthly search volume, Sep 2024 - Aug 2025.", "sayi"),
                        kolon("d", "Değişim", "Change", "İki 12 aylık ortalama arasındaki yüzde değişim; tek ay karşılaştırması kullanılmamıştır.", "Percentage change between the two 12-month averages; no single-month comparison is used.", "yuzde"),
                        kolon("son", "Ağu 2026 hacmi", "Aug 2026 volume", "Ağustos 2026 aylık arama hacmi.", "Search volume in August 2026.", "sayi")],
                  "r": R, "s": [5, "d"]},
          "ac": {"c": [kolon("kok", "Kök ifade", "Seed term", "Google arama kutusuna yazılan başlangıç ifadesi.", "The starting term typed into the Google search box.", "kw"),
                       kolon("grup", "Grup", "Group", "Kök ifadenin grubu: kategori, montaj ve tamir, yenileme ve tasarım, fiyat ve ödeme, rakip marka, perakendeci, VitrA ile başlayan.", "Group of the seed term: category, installation and repair, renovation and design, price and payment, competitor brand, retailer, starting with VitrA.", "kat", True),
                       kolon("sira", "Sıra", "Rank", "Önerinin listedeki sırası.", "Position of the suggestion in the list.", "sayi"),
                       kolon("oneri", "Öneri", "Suggestion", "Google'ın otomatik tamamlama önerisi; olduğu gibi korunmuştur.", "Google's autocomplete suggestion, kept as is.", "kw")],
                 "r": AC, "s": None}}
    sayfa("kelime-evreni.html", ("VitrA | Kelime Evreni", "VitrA | Keyword Universe"),
          ("VitrA TÜRKİYE · ARAMA TALEBİ", "VitrA TURKEY · SEARCH DEMAND"),
          ("Kelime Evreni: %s Kelime ve Google Önerileri" % tr_s(len(R)), "Keyword Universe: %s Keywords and Google Suggestions" % en_s(len(R))),
          ("Raporun talep bölümlerinde kullanılan kelime evreni: VitrA'nın kategori ağacına eşlenen %s kelime, niyet sınıfı ve iki 12 aylık dönemin ortalama arama hacmi. İkinci tablo, kategori, montaj, fiyat, rakip ve VitrA ile başlayan kök ifadeler için Google'ın otomatik tamamlama önerilerini listeler." % tr_s(len(R)),
           "The keyword universe used in the report's demand sections: %s keywords mapped to VitrA's category tree, intent class and average search volume for two 12-month periods. The second table lists Google's autocomplete suggestions for category, installation, price, competitor and VitrA-led seed terms." % en_s(len(R))),
          [(N(len(R)), ("kelime · 8 ana kategori", "keywords · 8 main categories")), (N(a26), ("toplam ort. aylık hacim, Eyl 2025 - Ağu 2026", "total avg. monthly volume, Sep 2025 - Aug 2026")),
           (T(("+" if a26 >= a25 else "-") + "%" + tr_s(abs(100 * (a26 - a25) / a25), 1), ("+" if a26 >= a25 else "-") + en_s(abs(100 * (a26 - a25) / a25), 1) + "%"), ("önceki 12 aya göre değişim", "change vs the previous 12 months")),
           (N(len(AC)), ("Google otomatik tamamlama önerisi", "Google autocomplete suggestions"))],
          [("kelimeler", ("Kelimeler: kategori, niyet ve arama hacmi", "Keywords: category, intent and search volume"),
            ("Ana kategori, alt kategori, niyet ve markalı süzgeçleriyle daraltılabilir; değişim, iki 12 aylık ortalama arasındadır.", "Narrow with the main category, subcategory, intent and branded filters; change is between the two 12-month averages."), "kel", None),
           ("oneriler", ("Google otomatik tamamlama önerileri", "Google autocomplete suggestions"),
            ("Kök ifade yazıldığında Google'ın gösterdiği öneriler, sırasıyla; grup süzgeci montaj, fiyat, rakip ve VitrA ile başlayan ifadeleri ayırır.", "Suggestions Google shows when the seed term is typed, in order; the group filter separates installation, price, competitor and VitrA-led terms."), "ac", None)],
          tb, cev,
          ("Hacimler Google Keyword Planner'dan alınmıştır (Türkiye, Türkçe). Kelimeler tohum ifadelerden genişletilmiş, VitrA'nın kategori ağacına kural tabanlı eşlenmiş ve niyet sınıfı atanmıştır; kategori dışı kalan ifadeler evrene alınmamıştır. Otomatik tamamlama önerileri masaüstü Chrome, Türkiye, Türkçe için 28.09.2026 tarihinde alınmıştır.",
           "Volumes are from Google Keyword Planner (Turkey, Turkish). Keywords were expanded from seed terms, mapped to VitrA's category tree with rules and given an intent class; terms outside the categories were not included. Autocomplete suggestions were collected for desktop Chrome, Turkey, Turkish on 28.09.2026."),
          ("Kaynak: Google Keyword Planner, Eyl 2024 - Ağu 2026 · Google otomatik tamamlama, 28.09.2026", "Source: Google Keyword Planner, Sep 2024 - Aug 2026 · Google autocomplete, 28.09.2026"))


# ====================================================================== 3. pazaryeri taramasi
KANAL = {"hepsiburada": "Hepsiburada", "trendyol": "Trendyol", "koctas": "Koçtaş", "creavit": "Creavit", "akakce": "Akakçe", "banyoline": "Banyoline", "banyomarka": "Banyomarka",
         "cimri": "Cimri", "banyomega": "Banyomega", "bauhaus": "Bauhaus"}
KANAL_TIP = {"hepsiburada": "Pazaryeri", "trendyol": "Pazaryeri", "koctas": "Yapı market", "bauhaus": "Yapı market", "creavit": "Marka sitesi", "akakce": "Fiyat karşılaştırma",
             "cimri": "Fiyat karşılaştırma", "banyoline": "Banyo e-ticaret sitesi", "banyomarka": "Banyo e-ticaret sitesi", "banyomega": "Banyo e-ticaret sitesi"}


def pazaryeri_taramasi(EK):
    R0 = [json.loads(l) for l in open(os.path.join(veri.V, "ham/derin/pazaryeri_derin2/urunler.jsonl"), encoding="utf-8")]
    KS = {k["kesit"]: k for k in (json.loads(l) for l in open(os.path.join(veri.V, "ham/derin/pazaryeri_derin2/kesitler.jsonl"), encoding="utf-8"))}
    cev = {"Pazaryeri": "Marketplace", "Yapı market": "DIY retailer", "Marka sitesi": "Brand site", "Fiyat karşılaştırma": "Price comparison", "Banyo e-ticaret sitesi": "Bathroom e-commerce site",
           "Evet": "Yes", "Hayır": "No"}
    cev.update(KESIT_EN)
    eksik = sorted({k[a] for k in KS.values() for a in ("ana_kategori", "alt_kategori")} - set(cev))
    R = []
    for r in R0:
        ks = KS.get(r["kesit"]) or {}
        vg = 1 if (r.get("marka") or "").lower() in ("vitra", "artema") else 0
        R.append([KANAL.get(r["kanal"], r["kanal"]), KANAL_TIP.get(r["kanal"], "Pazaryeri"), ks.get("ana_kategori"), ks.get("alt_kategori"), r["sira"], r.get("marka") or None,
                  [r["ad"], r["url"]] if r.get("url") else r["ad"], r.get("satici") or None, r.get("fiyat"), r.get("eski") if (r.get("eski") or 0) > (r.get("fiyat") or 0) else None,
                  r.get("puan"), r.get("yorum"), "Evet" if r.get("eslesme") else "Hayır", vg])
    tb = {"urun": {"c": [kolon("kanal", "Kanal", "Channel", "Taramanın yapıldığı site.", "The site where the scan was made.", "metin", True),
                         kolon("tip", "Kanal tipi", "Channel type", "Pazaryeri, yapı market, fiyat karşılaştırma, marka sitesi veya banyo e-ticaret sitesi.", "Marketplace, DIY retailer, price comparison, brand site or bathroom e-commerce site.", "kat", True),
                         kolon("ana", "Ana kategori", "Main category", "Aramanın ait olduğu ana kategori.", "Main category of the search.", "cev", True),
                         kolon("alt", "Alt kesit", "Subsegment", "Kanalda arama yapılan alt kategori ifadesi.", "The subcategory term searched on the channel.", "cev", True),
                         kolon("sira", "Sıra", "Rank", "Ürünün arama veya kategori listesindeki sırası.", "The product's position in the search or category list.", "sayi"),
                         kolon("marka", "Marka", "Brand", "Ürün kartında yazan marka.", "Brand shown on the product card.", "metin", True),
                         kolon("ad", "Ürün", "Product", "Ürün kartındaki ad; bağlantı ürün sayfasını yeni sekmede açar.", "Name on the product card; the link opens the product page in a new tab.", "link", uz=True),
                         kolon("satici", "Satıcı", "Seller", "Listede görünen satıcı (işletme adı).", "Seller shown in the list (business name).", "metin", True),
                         kolon("fiyat", "Fiyat", "Price", "Listede görünen satış fiyatı, TL, tarama günü.", "Selling price shown in the list, TRY, on the scan day.", "para"),
                         kolon("eski", "Üstü çizili fiyat", "Strikethrough price", "İndirim öncesi gösterilen fiyat, varsa.", "Price shown before discount, if any.", "para"),
                         kolon("puan", "Puan", "Rating", "Ürün puanı (5 üzerinden), varsa.", "Product rating (out of 5), if any.", "sayi", o=1),
                         kolon("yorum", "Değerlendirme", "Reviews", "Ürünün değerlendirme sayısı, varsa.", "Number of reviews on the product, if any.", "sayi"),
                         kolon("esl", "Kesitle eşleşiyor", "Matches segment", "Ürünün aranan alt kesite gerçekten ait olup olmadığı (ad ve kategori kuralı).", "Whether the product really belongs to the searched subsegment (name and category rule).", "kat", True)],
                   "r": [r[:13] for r in R], "vg": None, "s": None}}
    for r_, src in zip(tb["urun"]["r"], R): r_.append(src[13])
    tb["urun"]["vg"] = 13
    nv = sum(1 for r in R if r[13]); nk = len({r[3] for r in R})
    sayfa("pazaryeri-taramasi.html", ("VitrA | Pazaryeri Taraması", "VitrA | Marketplace Scan"),
          ("VitrA TÜRKİYE · PAZARYERİ VE KANAL TARAMASI", "VitrA TURKEY · MARKETPLACE AND CHANNEL SCAN"),
          ("Pazaryeri Taraması: %s Ürün Kartı, %d Kanal, %d Alt Kesit" % (tr_s(len(R)), len(KANAL), nk), "Marketplace Scan: %s Product Cards, %d Channels, %d Subsegments" % (en_s(len(R)), len(KANAL), nk)),
          ("Trendyol, Hepsiburada, Koçtaş, Bauhaus, Akakçe, Cimri ve banyo odaklı e-ticaret sitelerinde VitrA gamındaki alt kesitler için yapılan arama ve kategori listelerinin ilk sayfalarındaki ürün kartları: marka, satıcı, fiyat, puan ve değerlendirme sayısı. Tarama 30.09.2026 tarihlidir; VitrA ve Artema satırları vurgulanmıştır.",
           "Product cards on the first pages of search and category lists for subsegments in VitrA's range on Trendyol, Hepsiburada, Koçtaş, Bauhaus, Akakçe, Cimri and bathroom-focused e-commerce sites: brand, seller, price, rating and review count. The scan is dated 30.09.2026; VitrA and Artema rows are highlighted."),
          [(N(len(R)), ("ürün kartı", "product cards")), (N(len(KANAL)), ("kanal", "channels")), (N(nk), ("alt kesit", "subsegments")),
           (N(nv), ("VitrA ve Artema ürün kartı", "VitrA and Artema product cards"))],
          [("urunler", ("Ürün kartları", "Product cards"),
            ("Kanal, kategori, alt kesit, marka ve satıcıya göre süzülebilir; \"Kesitle eşleşiyor\" süzgeci, aramada çıkan ancak alt kesite ait olmayan ürünleri ayırır. Ürün adı ürün sayfasını yeni sekmede açar.",
             "Filter by channel, category, subsegment, brand and seller; the \"Matches segment\" filter separates products that appeared in the search but do not belong to the subsegment. The product name opens the product page in a new tab."), "urun", None)],
          tb, cev,
          ("Her kanalda alt kesit ifadesiyle arama yapılmış ya da ilgili kategori sayfası açılmış, ilk sayfadaki ürün kartları okunmuştur. Oturum açılmamış, sepete ürün eklenmemiştir. Fiyatlar kart üzerindeki satış fiyatıdır; sepette uygulanan ek indirimler kapsanmaz.",
           "On each channel a search was made with the subsegment term or the relevant category page was opened, and the product cards on the first page were read. No login was made and no product was added to the cart. Prices are the selling price on the card; additional discounts applied in the cart are not covered."),
          ("Kaynak: Trendyol, Hepsiburada, Koçtaş, Bauhaus, Akakçe, Cimri, Creavit, Banyoline, Banyomarka ve Banyomega arama ve kategori sayfaları · 30.09.2026",
           "Source: search and category pages of Trendyol, Hepsiburada, Koçtaş, Bauhaus, Akakçe, Cimri, Creavit, Banyoline, Banyomarka and Banyomega · 30.09.2026"))
    return eksik


KESIT_EN = {'Klozet': 'WC',
            'Lavabo': 'Washbasin',
            'Armatür': 'Taps',
            'Duşlar': 'Showers',
            'Rezervuar': 'Cistern',
            'Yıkanma alanları': 'Bathing areas',
            'Banyo mobilyası': 'Bathroom furniture',
            'Banyo aksesuarı': 'Bathroom accessories',
            'Vitrifiye tamamlayıcı': 'Sanitaryware complements',
            'Yerden tek klozet (ayaklı klozet)': 'Floor-standing WC',
            'Asma klozet takımı (klozet + gömme rezervuar seti)': 'Wall-hung WC set (WC + concealed cistern)',
            'Tuvalet taşı (alaturka)': 'Squat toilet',
            'Çocuk klozet': "Children's WC", 'Engelli klozet': 'Accessible WC',
            'Çanak lavabo': 'Bowl washbasins',
            'Monoblok lavabo': 'Monoblock basin',
            'Yarım tezgah lavabo': 'Semi-recessed basin',
            'Etajerli lavabo': 'Basin with shelf',
            'Ayaklı (standart) lavabo': 'Pedestal basin',
            'Köşe lavabo': 'Corner basin',
            'Lavabo ayağı': 'Basin pedestal',
            'Bide bataryası': 'Bidet tap',
            'Küvet bataryası': 'Bath filler tap',
            'Termostatik batarya': 'Thermostatic tap',
            'Temassız (fotoselli) lavabo bataryası': 'Touchless basin tap',
            'Duvardan (sıva üstü) banyo bataryası': 'Exposed bath tap',
            'Çanak lavabo bataryası (yüksek)': 'Tall bowl-basin tap',
            'Ankastre stop valf': 'Concealed stop valve',
            'Lavabo sifon ve süzgeci': 'Basin trap and waste',
            'Armatür tamamlayıcı (çıkış ucu, dirsek)': 'Tap accessories (outlet, elbow)',
            'Duş kolonu': 'Shower column',
            'El duşu takımı': 'Hand shower set',
            'Sürgülü el duşu takımı': 'Sliding-rail hand shower set',
            'Masajlı duş sistemi': 'Massage shower system',
            'Bataryalı duş sistemi': 'Shower system with mixer',
            'Ankastre duş yönlendirici': 'Concealed diverter',
            'Rezervuar kumanda paneli (mekanik)': 'Cistern flush plate (mechanical)',
            'Rezervuar kumanda paneli (temassız)': 'Cistern flush plate (touchless)',
            'Rezervuar kumanda paneli (akıllı)': 'Cistern flush plate (smart)',
            'Taşıyıcı aparat (asma klozet taşıyıcı)': 'Wall-hung WC frame',
            'Duvar önü rezervuar': 'Exposed cistern',
            'Tuvalet taşı rezervuarı': 'Squat toilet cistern',
            'Duş kanalı': 'Shower channel',
            'Duş ünitesi (kompakt duş kabini)': 'Shower unit (compact shower cabin)',
            'Hidromasajlı küvet': 'Whirlpool bath',
            'Bağımsız küvet': 'Freestanding bath',
            'Küvet paneli': 'Bath panel',
            'Duş teknesi paneli': 'Shower tray panel',
            'Kaydırmaz': 'Anti-slip mat',
            'Banyo tezgahı': 'Bathroom countertop',
            'Banyo konsolu': 'Bathroom console',
            'Banyo set modülü': 'Furniture set module',
            'Malzemelik': 'Storage unit',
            'Dolap kulpu': 'Cabinet handle',
            'Dolap ayağı': 'Cabinet leg',
            'Makyaj aynası': 'Make-up mirror',
            'Aynalı dolap': 'Mirror cabinet',
            'Sabunluk': 'Soap dish',
            'Diş fırçalığı': 'Toothbrush holder',
            'Tuvalet kağıtlığı': 'Toilet roll holder',
            'Tuvalet fırçası': 'Toilet brush',
            'Banyo askısı': 'Robe hook',
            'Banyo çöp kovası': 'Bathroom bin',
            'Havluluk': 'Towel rail',
            'Pisuvar ara bölmesi': 'Urinal divider',
            'Pisuvar yıkama sistemi': 'Urinal flush system'}


# ====================================================================== 4. YouTube
YT_GRUP = {"Marka ve rakip": "Brand and competitors", "Montaj": "Installation", "Tamir ve bakım": "Repair and maintenance", "Seçim ve karşılaştırma": "Selection and comparison",
           "Yeni kategoriler": "New categories", "İlham ve tadilat": "Inspiration and renovation"}
YT_TUR = {"Tesisatçı / usta": "Plumber / tradesperson", "Diğer": "Other", "Marka": "Brand", "Dekorasyon / iç mimar": "Decoration / interior designer", "Perakendeci": "Retailer",
          "İnceleme / teknoloji": "Review / technology"}


def youtube():
    V = list(csv.DictReader(open(os.path.join(veri.V, "ham/derin/youtube/arama_video_tablosu.csv"), encoding="utf-8-sig")))
    C = list(csv.DictReader(open(os.path.join(veri.V, "ham/derin/youtube/kanal_analizi.csv"), encoding="utf-8-sig")))
    cev = dict(YT_GRUP); cev.update(YT_TUR); cev.update({"Evet": "Yes", "Hayır": "No"})
    def i(v):
        try: return int(float(v))
        except Exception: return None
    R = [[v["grup"], v["arama"], i(v["sira"]), [v["baslik"], v["url"]], v["kanal"], i(v["izlenme"]), v["yayin"], v["sure"] or None,
          "Evet" if v["vitra_kanali"] == "True" else "Hayır", "Evet" if v["vitra_iliskili"] == "True" else "Hayır", 1 if v["vitra_kanali"] == "True" else 0]
         for v in V if v["alakasiz"] != "True"]
    K = [[c["kanal"], c["tur"], i(c["gorunme"]), i(c["arama_sayisi"]), i(c["tekil_video"]), i(c["toplam_izlenme_tekil"]), float(c["ort_sira"]) if c["ort_sira"] else None,
          c["en_cok_izlenen_video"], 1 if c["tur"] == "Marka" and "vitra" in c["kanal"].lower() else 0] for c in C]
    tb = {"vid": {"c": [kolon("grup", "Konu grubu", "Topic group", "Aramanın konu grubu: montaj, tamir ve bakım, seçim ve karşılaştırma, marka ve rakip, yeni kategoriler, ilham ve tadilat.", "Topic group of the search: installation, repair and maintenance, selection and comparison, brand and competitors, new categories, inspiration and renovation.", "kat", True),
                        kolon("arama", "Arama", "Search", "YouTube'da yapılan arama; olduğu gibi korunmuştur.", "The search made on YouTube, kept as is.", "kw", True),
                        kolon("sira", "Sıra", "Rank", "Videonun arama sonucundaki sırası.", "The video's position in the search results.", "sayi"),
                        kolon("baslik", "Video", "Video", "Video başlığı; bağlantı videoyu yeni sekmede açar.", "Video title; the link opens the video in a new tab.", "link", uz=True),
                        kolon("kanal", "Kanal", "Channel", "Videoyu yayınlayan kanal.", "The channel that published the video.", "metin", True),
                        kolon("izl", "İzlenme", "Views", "Tarama günündeki toplam izlenme.", "Total views on the scan day.", "sayi"),
                        kolon("yayin", "Yayın", "Published", "Videonun yayın zamanı (tarama gününe göre).", "When the video was published (relative to the scan day).", "once"),
                        kolon("sure", "Süre", "Length", "Video süresi.", "Video length.", "metin"),
                        kolon("vk", "VitrA kanalı", "VitrA channel", "Video VitrA'nın kendi kanalında mı?", "Is the video on VitrA's own channel?", "kat", True),
                        kolon("vi", "VitrA ile ilişkili", "VitrA related", "Başlıkta veya kanalda VitrA ya da Artema geçiyor mu?", "Does the title or channel mention VitrA or Artema?", "kat", True)],
                  "r": [r[:10] for r in R], "s": None},
          "kanal": {"c": [kolon("kanal", "Kanal", "Channel", "YouTube kanalı.", "YouTube channel.", "metin"),
                          kolon("tur", "Kanal türü", "Channel type", "Kanalın türü: marka, tesisatçı veya usta, dekorasyon, perakendeci, inceleme ve diğer.", "Channel type: brand, plumber or tradesperson, decoration, retailer, review and other.", "kat", True),
                          kolon("gor", "Görünme", "Appearances", "Kanal videolarının tüm aramalarda toplam görünme sayısı.", "Total appearances of the channel's videos across all searches.", "sayi"),
                          kolon("ar", "Arama sayısı", "Searches", "Kanalın en az bir videoyla çıktığı arama sayısı.", "Number of searches where the channel appeared with at least one video.", "sayi"),
                          kolon("tv", "Tekil video", "Unique videos", "Kanalın aramalarda çıkan farklı video sayısı.", "Number of different videos of the channel in the searches.", "sayi"),
                          kolon("izl", "Toplam izlenme", "Total views", "Tekil videoların toplam izlenmesi.", "Total views of the unique videos.", "sayi"),
                          kolon("os", "Ort. sıra", "Avg. rank", "Kanal videolarının ortalama arama sırası.", "Average search rank of the channel's videos.", "sayi", o=1),
                          kolon("en", "En çok izlenen video", "Most viewed video", "Kanalın aramalarda çıkan en çok izlenen videosu.", "The channel's most viewed video in the searches.", "metin", uz=True)],
                    "r": [r[:8] for r in K], "s": [2, "d"]}}
    for r_, src in zip(tb["vid"]["r"], R): r_.append(src[10])
    tb["vid"]["vg"] = 10
    for r_, src in zip(tb["kanal"]["r"], K): r_.append(src[8])
    tb["kanal"]["vg"] = 8
    na = len({r[1] for r in R}); nvk = sum(1 for r in R if r[10])
    sayfa("youtube-videolari.html", ("VitrA | YouTube Videoları", "VitrA | YouTube Videos"),
          ("VitrA TÜRKİYE · YOUTUBE ARAMALARI", "VitrA TURKEY · YOUTUBE SEARCHES"),
          ("YouTube Videoları: %d Arama, %s Video Sonucu, %s Kanal" % (na, tr_s(len(R)), tr_s(len(K))), "YouTube Videos: %d Searches, %s Video Results, %s Channels" % (na, en_s(len(R)), en_s(len(K)))),
          ("Montaj, tamir, ürün seçimi, marka ve ilham konularında YouTube'da yapılan %d aramanın video sonuçları ve bu sonuçlarda çıkan kanalların özeti. Konuyla ilgisiz videolar çıkarılmıştır; VitrA kanalındaki videolar vurgulanmıştır. Tarama 29.09.2026 tarihlidir." % na,
           "Video results of %d YouTube searches on installation, repair, product choice, brand and inspiration topics, and a summary of the channels appearing in them. Irrelevant videos were removed; videos on the VitrA channel are highlighted. The scan is dated 29.09.2026." % na),
          [(N(na), ("YouTube araması", "YouTube searches")), (N(len(R)), ("video sonucu", "video results")), (N(len(K)), ("kanal", "channels")),
           (N(nvk), ("VitrA kanalındaki video sonucu", "video results on the VitrA channel"))],
          [("videolar", ("Arama sonuçlarındaki videolar", "Videos in the search results"),
            ("Konu grubu, arama, kanal ve VitrA süzgeçleriyle daraltılabilir; video başlığı videoyu yeni sekmede açar.", "Narrow with the topic group, search, channel and VitrA filters; the video title opens the video in a new tab."), "vid", None),
           ("kanallar", ("Kanallar", "Channels"),
            ("Aramalarda çıkan kanalların görünme sayısı, tekil video ve izlenme toplamı; kanal türü süzgeci tesisatçı, marka ve dekorasyon kanallarını ayırır.", "Appearances, unique videos and total views of the channels in the searches; the channel type filter separates plumber, brand and decoration channels."), "kanal", None)],
          tb, cev,
          ("Aramalar Türkiye, Türkçe için yapılmış, her aramada ilk sonuç sayfasındaki videolar okunmuştur. İzlenme ve yayın zamanı tarama günündeki değerdir. Kanal türü kanal adı ve içeriğine göre atanmıştır. Video yorumları ve yorumcu adları bu sayfada yer almaz.",
           "Searches were made for Turkey, Turkish, and the videos on the first results page were read for each search. Views and publish time are values on the scan day. Channel type is assigned from the channel name and content. Video comments and commenter names are not included on this page."),
          ("Kaynak: YouTube arama sonuçları, Türkiye · 29.09.2026", "Source: YouTube search results, Turkey · 29.09.2026"))


# ====================================================================== 5. GEO promptlari (yapay zeka yanit takibi)
KLASOR = {"e-ticaret": ("E-ticaret", "E-commerce"), "montaj": ("Montaj", "Installation"), "Vitrifiyeler": ("Vitrifiyeler", "Sanitaryware"), "Armatürler": ("Armatürler", "Taps"),
          "Top 25 Keywords": ("Öncelikli 25 kelime", "Top 25 keywords"), "Banyo Mobilyaları": ("Banyo Mobilyaları", "Bathroom Furniture"), "Banyo Yenileme": ("Banyo Yenileme", "Bathroom Renovation"),
          "Rezervuar": ("Rezervuar", "Cisterns"), "Yıkanma Alanları": ("Yıkanma Alanları", "Bathing Areas"), "Duşlar": ("Duşlar", "Showers"), "Banyo Aksesuarları": ("Banyo Aksesuarları", "Bathroom Accessories")}
PTIP = {"custom": ("Genel soru", "General question"), "best": ("En iyi / öneri", "Best / recommendation"), "vs": ("Karşılaştırma", "Comparison"), "reviews": ("Yorum ve deneyim", "Reviews and experience")}
PROV = {"chatgpt": ("ChatGPT", "ChatGPT"), "gemini": ("Gemini", "Gemini"), "google_ai_overview": ("Google AI Overview", "Google AI Overview")}


def geo_promptlari():
    D = json.load(open(os.path.join(veri.V, "ham/geo/ai_promptlar.json"), encoding="utf-8"))
    cev = {a: b for a, b in list(KLASOR.values()) + list(PTIP.values()) + list(PROV.values())}
    cev.update({"Evet": "Yes", "Hayır": "No", "Geçti": "Named", "Geçmedi": "Not named"})
    ST = collections.defaultdict(dict)
    for r in D["istatistik"]:
        ST[r["pid"]][r["prov"]] = {k: (float(v) if v not in (None, "") else None) for k, v in r.items() if k not in ("pid", "prov")}
    def oran(pid, prov, k):
        s = ST[pid].get(prov)
        return round(100 * s[k] / s["n"], 1) if s and s["n"] else None
    def top(pid, k):
        n = sum(s["n"] for s in ST[pid].values()); v = sum(s[k] or 0 for s in ST[pid].values())
        return round(100 * v / n, 1) if n else None
    R = []
    for p in D["promptlar"]:
        i = p["id"]; n = int(sum(s["n"] for s in ST[i].values()))
        sl = [s["sira"] for s in ST[i].values() if s.get("sira")]
        R.append([p["content"], KLASOR.get(p["folder"], (p["folder"], p["folder"]))[0], PTIP.get(p["kategori"], (p["kategori"],))[0], "Evet" if p["markali"] else "Hayır", n,
                  oran(i, "chatgpt", "vitra"), oran(i, "gemini", "vitra"), oran(i, "google_ai_overview", "vitra"), round(sum(sl) / len(sl), 1) if sl else None,
                  top(i, "vkaynak"), top(i, "pzkaynak"), top(i, "kale"), top(i, "creavit"), 1 if (top(i, "vitra") or 0) >= 50 else 0])
    PM = {p["id"]: p for p in D["promptlar"]}
    Y = []
    for r in D["son_yanit"]:
        p = PM.get(r["pid"])
        if not p or not r.get("metin"): continue
        m = re.sub(r"\*\*(.+?)\*\*", r"\1", r["metin"]).strip()
        t_ = (r.get("tarih") or "")[:10]; t_ = ".".join(reversed(t_.split("-"))) if t_ else None
        Y.append([p["content"], PROV[r["prov"]][0], "Geçti" if r["bm"] else "Geçmedi", m, int(r["bp"]) if r.get("bp") not in (None, "") else None,
                  KLASOR.get(p["folder"], (p["folder"],))[0], t_, r.get("rakip") or None, r.get("kaynaklar") or None, 1 if r["bm"] else 0])
    Y.sort(key=lambda r: (r[5], r[0], r[1]))
    Rv = [r[:13] for r in R]; [a.append(b[13]) for a, b in zip(Rv, R)]
    Yv = [r[:9] for r in Y]; [a.append(b[9]) for a, b in zip(Yv, Y)]
    tb = {"prm": {"c": [kolon("p", "Prompt", "Prompt", "Yapay zeka platformlarına sorulan soru; olduğu gibi korunmuştur.", "The question asked to the AI platforms, kept as is.", "kw"),
                        kolon("k", "Klasör", "Folder", "Sorunun ait olduğu konu klasörü; e-ticaret ve montaj klasörleri 28.09.2026'da eklenmiştir.", "Topic folder of the question; the e-commerce and installation folders were added on 28.09.2026.", "cev", True),
                        kolon("t", "Soru tipi", "Question type", "Genel soru, en iyi / öneri, karşılaştırma ya da yorum ve deneyim sorusu.", "General, best / recommendation, comparison or reviews and experience question.", "kat", True),
                        kolon("m", "Markalı", "Branded", "Soruda VitrA adı geçiyor mu?", "Does the question name VitrA?", "kat", True),
                        kolon("n", "Yanıt", "Answers", "4 Eyl - 3 Eki 2026 arasında üç platformdan alınan toplam yanıt sayısı.", "Total answers from the three platforms, 4 Sep - 3 Oct 2026.", "sayi"),
                        kolon("g", "ChatGPT · VitrA", "ChatGPT · VitrA", "ChatGPT yanıtlarında VitrA'nın adıyla geçtiği yanıtların payı.", "Share of ChatGPT answers naming VitrA.", "oran"),
                        kolon("ge", "Gemini · VitrA", "Gemini · VitrA", "Gemini yanıtlarında VitrA'nın adıyla geçtiği yanıtların payı.", "Share of Gemini answers naming VitrA.", "oran"),
                        kolon("a", "AI Overview · VitrA", "AI Overview · VitrA", "Google AI Overview yanıtlarında VitrA'nın adıyla geçtiği yanıtların payı.", "Share of Google AI Overview answers naming VitrA.", "oran"),
                        kolon("s", "VitrA sırası", "VitrA position", "VitrA'nın adı geçtiğinde yanıttaki ortalama sırası (1: ilk anılan marka).", "VitrA's average position in the answer when named (1: first brand mentioned).", "sayi", o=1),
                        kolon("vk", "vitra.com.tr kaynak", "vitra.com.tr cited", "vitra.com.tr'nin kaynak gösterildiği yanıtların payı, üç platform birlikte.", "Share of answers citing vitra.com.tr, three platforms together.", "oran"),
                        kolon("pk", "Pazaryeri kaynak", "Marketplace cited", "Trendyol, Hepsiburada, Koçtaş, n11, Amazon, Bauhaus, Akakçe veya Cimri'nin kaynak gösterildiği yanıtların payı.", "Share of answers citing Trendyol, Hepsiburada, Koçtaş, n11, Amazon, Bauhaus, Akakçe or Cimri.", "oran"),
                        kolon("ka", "Kale", "Kale", "Kale'nin adının geçtiği yanıtların payı.", "Share of answers naming Kale.", "oran"),
                        kolon("cr", "Creavit", "Creavit", "Creavit'in adının geçtiği yanıtların payı.", "Share of answers naming Creavit.", "oran")],
                  "r": Rv, "vg": 13, "s": [4, "d"]},
          "yan": {"c": [kolon("p", "Prompt", "Prompt", "Yapay zeka platformlarına sorulan soru.", "The question asked to the AI platforms.", "kw", True),
                        kolon("pl", "Platform", "Platform", "Yanıtın alındığı platform.", "The platform the answer came from.", "kat", True),
                        kolon("v", "VitrA", "VitrA", "Yanıtta VitrA'nın adı geçti mi?", "Was VitrA named in the answer?", "kat", True),
                        kolon("y", "Yanıt metni", "Answer text", "Yapay zeka yanıtının metni; özet satıra tıklayınca tamamı açılır. Yanıtlar olduğu gibi korunmuş, yalnızca kalın yazım işaretleri kaldırılmıştır.", "Text of the AI answer; click the summary line to open it in full. Answers are kept as is; only bold markers were removed.", "uzun"),
                        kolon("vs", "VitrA sırası", "VitrA position", "VitrA'nın yanıtta anılan markalar arasındaki sırası.", "VitrA's position among the brands named in the answer.", "sayi"),
                        kolon("k", "Klasör", "Folder", "Sorunun konu klasörü.", "Topic folder of the question.", "cev", True),
                        kolon("tr", "Tarih", "Date", "Yanıtın alındığı gün (her soru ve platform için en son yanıt).", "Day the answer was received (latest answer per question and platform).", "metin"),
                        kolon("rk", "Adı geçen rakip siteler", "Competitor sites named", "Yanıtta adı geçen takip edilen rakip ve kanal alan adları.", "Tracked competitor and channel domains named in the answer.", "metin", uz=True),
                        kolon("ky", "Kaynak alan adları", "Cited domains", "Yanıtta kaynak olarak bağlantı verilen alan adları.", "Domains linked as sources in the answer.", "metin", uz=True)],
                  "r": Yv, "vg": 9, "s": None}}
    mark = [r for r in R if r[3] == "Hayır"]
    def ort(i): L = [r[i] for r in mark if r[i] is not None]; return sum(L) / len(L) if L else 0
    nv = sum(1 for r in Y if r[9])
    sayfa("geo-promptlari.html", ("VitrA | GEO Promptları", "VitrA | GEO Prompts"),
          ("VitrA TÜRKİYE · YAPAY ZEKA YANITLARI", "VitrA TURKEY · AI ANSWERS"),
          ("GEO Promptları: %d Soru, ChatGPT, Gemini ve Google AI Overview Yanıtları" % len(R), "GEO Prompts: %d Questions, ChatGPT, Gemini and Google AI Overview Answers" % len(R)),
          ("Banyo ürünleri, montaj ve online alışverişle ilgili %d soru düzenli aralıklarla ChatGPT, Gemini ve Google AI Overview'a sorulmakta; yanıtta hangi markaların adının geçtiği, VitrA'nın kaçıncı sırada anıldığı ve hangi sitelerin kaynak gösterildiği kaydedilmektedir. İlk tablo 4 Eyl - 3 Eki 2026 dönemindeki oranları, ikinci tablo her soru ve platform için en son yanıtın tam metnini içerir. Bu set, Bölüm 08'deki tek günlük Google arama gözleminden ayrıdır." % len(R),
           "%d questions on bathroom products, installation and online shopping are asked to ChatGPT, Gemini and Google AI Overview at regular intervals; which brands are named, VitrA's position and which sites are cited are recorded. The first table shows the rates for 4 Sep - 3 Oct 2026, the second the full text of the latest answer per question and platform. This set is separate from the single-day Google search observation in Section 08." % len(R)),
          [(N(len(R)), ("soru · %s VitrA adıyla" % ek(sum(1 for r in R if r[3] == "Evet"), "i"), "questions · %d naming VitrA" % sum(1 for r in R if r[3] == "Evet"))),
           (N(sum(r[4] for r in R)), ("yanıt, 4 Eyl - 3 Eki 2026", "answers, 4 Sep - 3 Oct 2026")),
           (P(ort(6)), ("markasız sorularda Gemini yanıtlarında VitrA payı (soru ortalaması)", "VitrA share in Gemini answers to unbranded questions (question average)")),
           (P(ort(5)), ("markasız sorularda ChatGPT yanıtlarında VitrA payı (soru ortalaması)", "VitrA share in ChatGPT answers to unbranded questions (question average)")),
           (N(len(Y)), ("en son yanıt metni · %s VitrA geçiyor" % ek(nv, "inde"), "latest answer texts · %d name VitrA" % nv))],
          [("promptlar", ("Promptlar: platform bazında VitrA, rakipler ve kaynaklar", "Prompts: VitrA, competitors and sources by platform"),
            ("Her satır bir sorudur. Klasör, soru tipi ve markalı süzgeçleriyle daraltılabilir; VitrA'nın yanıtların en az yarısında geçtiği sorular vurgulanmıştır.", "Each row is a question. Narrow with the folder, question type and branded filters; questions where VitrA is named in at least half of the answers are highlighted."), "prm", None),
           ("yanitlar", ("Son yanıtlar", "Latest answers"),
            ("Her soru ve platform için en son alınan yanıt; özet satıra tıklanınca metnin tamamı açılır. Prompt, platform ve \"VitrA\" süzgeçleriyle belirli bir sorunun üç platformdaki yanıtı yan yana okunabilir.", "The latest answer per question and platform; click the summary line to open the full text. Use the prompt, platform and \"VitrA\" filters to read one question's answers across the three platforms."), "yan", None)],
          tb, cev,
          ("Sorular markanın kategori ağacı, satın alma ve montaj ihtiyaçları üzerinden belirlenmiştir. Yanıtlar kişiselleştirilmemiş oturumlardan alınır; aynı soruya gün içinde farklı yanıt verilebilir, bu nedenle oranlar yön göstericidir. Markanın adı geçme ve kaynak gösterilme ayrı ölçülür: bir yanıt VitrA'yı anarken kaynak olarak pazaryerini gösterebilir.",
           "Questions were set from the brand's category tree and purchase and installation needs. Answers come from non-personalised sessions; the same question may get different answers within the day, so rates are indicative. Being named and being cited are measured separately: an answer may name VitrA while citing a marketplace as the source."),
          ("Kaynak: Yapay zeka yanıt takibi · ChatGPT, Gemini ve Google AI Overview · 4 Eyl - 3 Eki 2026", "Source: AI answer tracking · ChatGPT, Gemini and Google AI Overview · 4 Sep - 3 Oct 2026"))


def main(EK):
    arama_sonuclari()
    kelime_evreni(EK)
    eksik = pazaryeri_taramasi(EK)
    youtube()
    geo_promptlari()
    return eksik


if __name__ == "__main__":
    import ceviri
    main(getattr(ceviri, "EN", {}))
