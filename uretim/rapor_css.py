# -*- coding: utf-8 -*-
CSS = """
:root{
  --ink:#10332F; --ink-2:#2F4E4A; --muted:#5C6B69; --line:#E0DCD5;
  --bg:#FBFAF8; --card:#FFFFFF; --teal:#10332F; --coral:#FF7B52;
  --coral-deep:#E85F36; --coral-tint:#FFE3D8; --green:#2E7D32; --green-wash:#C8E6C9;
  --red:#D32F2F; --red-wash:#FFCDD2; --gold:#F5A623; --neutral:#F0EDE8;
  --appbar:64px; --maxw:1400px; --toc:322px;
}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){
  --ink:#EDEAE4; --ink-2:#CFD8D5; --muted:#9AA8A5; --line:#2A3E3B;
  --bg:#0C1917; --card:#12211F; --teal:#0B2523; --neutral:#1A2A28; --coral-tint:#3A241D;
}}
:root[data-theme="dark"]{
  --ink:#EDEAE4; --ink-2:#CFD8D5; --muted:#9AA8A5; --line:#2A3E3B;
  --bg:#0C1917; --card:#12211F; --teal:#0B2523; --neutral:#1A2A28; --coral-tint:#3A241D;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
  font:15px/1.62 "Segoe UI",Arial,Helvetica,sans-serif;-webkit-font-smoothing:antialiased}
.appbar{position:sticky;top:0;z-index:40;background:var(--teal);border-bottom:1px solid rgba(255,255,255,.10)}
.appbar .in{max-width:var(--maxw);margin:0 auto;padding:12px 22px;display:flex;align-items:center;
  justify-content:space-between;gap:18px}
.brandbit{display:flex;align-items:center;gap:11px;min-width:0}
.brandbit .lbl{font-size:9.5px;letter-spacing:.13em;color:rgba(255,255,255,.55);
  text-transform:none;white-space:nowrap}
.logo-card{background:#fff;border-radius:5px;padding:5px 10px;display:flex;align-items:center}
.logo-card img{height:22px;width:auto;display:block}
.ib img{height:22px;width:auto;display:block;filter:brightness(0) invert(1)}
.wrap{max-width:var(--maxw);margin:0 auto;padding:0 22px;display:grid;
  grid-template-columns:var(--toc) minmax(0,1fr);gap:38px;align-items:start}
.sidenav{position:sticky;top:calc(var(--apph, var(--appbar)) + 6px);align-self:start;padding:6px 0;overflow:hidden}
/* Icindekiler her ekran yuksekliginde kaydirmasiz sigar: satir birimi (--tu) gorunur yukseklikten
   turetilir; aralik, yazi ve numara rozeti bu birime gore olceklenir. */
.tocbox{--tu:calc((min(100vh, 1260px) - var(--apph, var(--appbar)) - 40px) / 36.5);
  background:var(--card);border:1px solid var(--line);border-radius:13px;
  padding:calc(var(--tu) * .45) 10px calc(var(--tu) * .3);
  height:calc(100vh - var(--apph, var(--appbar)) - 14px);max-height:1200px;overflow:hidden;
  display:flex;flex-direction:column}
.sidenav .grp{font-size:clamp(8.5px, calc(var(--tu) * .47), 11px);letter-spacing:.13em;color:var(--ink-2);font-weight:700;
  margin:0;padding:0 8px calc(var(--tu) * .14);text-transform:none;flex:1.75 1 0;min-height:0;max-height:74px;
  display:flex;align-items:flex-end;line-height:1.1}
.sidenav .grp:first-child{flex:0 0 auto;padding-top:0}
.sidenav ul.tocg{display:contents;list-style:none;margin:0;padding:0}
.sidenav ul.tocg li{margin:0;flex:1 1 0;min-height:0;max-height:40px;display:flex;align-items:center}
.sidenav ul.tocg li a{flex:1;min-width:0}
.sidenav a{display:flex;align-items:center;gap:9px;padding:clamp(0px, calc(var(--tu) * .1), 3px) 9px;
  font-size:clamp(8px, calc(var(--tu) * .56), 12.5px);
  color:var(--ink-2);text-decoration:none;border-radius:8px;line-height:1.22;
  transition:background .12s,color .12s}
.sidenav a .no{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;
  width:clamp(16px, calc(var(--tu) * .88), 21px);height:clamp(10px, calc(var(--tu) * .72), 18px);border-radius:5px;
  background:var(--neutral);color:var(--muted);
  font-size:clamp(6.5px, calc(var(--tu) * .41), 9.5px);font-weight:700;font-variant-numeric:tabular-nums;letter-spacing:.01em;
  transition:background .12s,color .12s}
.sidenav a .tx{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sidenav a:hover,.sidenav a:focus,.sidenav a:active{text-decoration:none;background:var(--neutral);color:var(--ink)}
.sidenav a:hover .no{background:var(--line);color:var(--ink)}
.sidenav a:focus-visible{outline:2px solid var(--coral);outline-offset:1px}
.sidenav a.on{background:var(--coral-tint);color:var(--ink);font-weight:640}
.sidenav a.on .no{background:var(--teal);color:#fff}

:root[data-theme="dark"] .sidenav a.on,
:root:not([data-theme="light"]) .sidenav a.on{background:rgba(255,123,82,.16)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .sidenav a.on{background:var(--coral-tint)}}
:root[data-theme="dark"] .sidenav a.on .no,
:root:not([data-theme="light"]) .sidenav a.on .no{background:var(--coral-deep);color:#fff}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .sidenav a.on .no{background:var(--teal)}}
main{padding:26px 0 90px;min-width:0}
.hero{padding:6px 0 22px;border-bottom:1px solid var(--line);margin-bottom:30px}
.eyebrow{font-size:10.5px;letter-spacing:.15em;color:var(--coral-deep);margin:0 0 9px}
h1{font-size:29px;line-height:1.22;margin:0 0 12px;font-weight:650;letter-spacing:-.01em}
.sub{color:var(--muted);font-size:13.5px;margin:0}
section{scroll-margin-top:calc(var(--appbar) + 22px);padding:34px 0;border-top:1px solid var(--line)}
section:first-of-type{border-top:0;padding-top:4px}
h2{font-size:20.5px;margin:0 0 6px;font-weight:640;letter-spacing:-.005em}
h2 .no{color:var(--muted);font-weight:640;font-size:inherit;letter-spacing:inherit;
  margin-right:11px;font-variant-numeric:tabular-nums}
h3{font-size:15.5px;margin:26px 0 9px;font-weight:640}
p{margin:0 0 13px}
.lede{color:var(--muted);font-size:13.5px;margin:0 0 20px}
ul{margin:0 0 14px;padding-left:19px}li{margin:0 0 7px}
/* Kendi isaretini tasiyan listelerde tarayici madde imi kapatilir; aksi halde
   nokta ile ✓/▲ yan yana basilir ve madde imi ciftlenir. */
ul.marks{list-style:none;padding-left:0;margin:0 0 14px}
ul.marks li{position:relative;padding-left:23px;margin:0 0 8px}
ul.marks li .mk{position:absolute;left:0;top:0;font-weight:700;font-size:13px;line-height:1.62}
ul.marks li .mk.up{color:var(--green)}
ul.marks li .mk.at{color:var(--coral-deep)}

b,strong{font-weight:650}
.term{border-bottom:1px dotted var(--coral-deep);cursor:help}
.term:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
a .term,th .term{border-bottom:0;cursor:inherit}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(186px,1fr));gap:13px;margin:0 0 22px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:15px 16px}
.kpi .v{font-size:25px;font-weight:660;letter-spacing:-.02em;line-height:1.12}
.kpi .k{font-size:11.5px;color:var(--muted);margin-top:6px;line-height:1.42}
.kpi .d{font-size:12px;font-weight:640;margin-top:7px}
.up{color:var(--green)}.dn{color:var(--red)}.hi{color:var(--coral-deep)}
.box{background:var(--card);border:1px solid var(--line);border-radius:9px;padding:17px 19px;margin:0 0 20px}
.box .bt{font-size:10.5px;letter-spacing:.14em;color:var(--coral-deep);margin:0 0 9px}
.box p:last-child{margin-bottom:0}
.insight{background:var(--card);border:1px solid var(--line);border-radius:9px;
  padding:14px 17px 14px 40px;position:relative;margin:0 0 16px}
.insight::before{content:"\\27A1";position:absolute;left:16px;top:13px;color:var(--coral-deep);
  font-size:15px;line-height:1.5}
.insight p:last-child{margin-bottom:0}
.tw{overflow:auto;border:1px solid var(--line);border-radius:9px;background:var(--card);
  margin:0 0 16px;max-height:none}
.tw.uzun{max-height:min(560px,72vh)}
.tw.uzun thead th{position:sticky;top:0;z-index:2}
.tw::-webkit-scrollbar{width:10px;height:10px}
.tw::-webkit-scrollbar-thumb{background:var(--line);border-radius:5px}
.tw::-webkit-scrollbar-thumb:hover{background:var(--muted)}
table{border-collapse:collapse;width:100%;font-size:13px;min-width:640px}
th{background:var(--teal);color:#fff;text-align:left;padding:10px 13px;font-weight:600;
  font-size:11.5px;letter-spacing:.03em;vertical-align:middle;border-bottom:1px solid var(--line)}
td{padding:10px 13px;border-top:1px solid var(--line);vertical-align:middle;line-height:1.5}
tbody tr:first-child td{border-top:0}
td.n,th.n{text-align:center}
.badge{display:inline-block;padding:2px 9px;border-radius:11px;font-size:11px;font-weight:640;white-space:nowrap}
.b-var{background:var(--green-wash);color:var(--green)}
.b-yok{background:var(--red-wash);color:var(--red)}
.b-kis{background:var(--coral-tint);color:var(--coral-deep)}
.b-o1{background:var(--gold);color:#10332F}
.b-o2{background:var(--coral-tint);color:var(--coral-deep)}
.b-o3{background:var(--neutral);color:var(--muted)}
.fig{margin:0 0 8px;background:var(--card);border:1px solid var(--line);border-radius:9px;padding:15px 16px 10px}
.figcap{font-size:11px;color:var(--muted);margin:0 0 6px}
.chart{width:100%;height:auto;display:block}
.chart .grid{stroke:var(--line);stroke-width:1}
.chart .grid.yr{stroke-dasharray:3 4}
.chart .ax{fill:var(--muted);font-size:10.5px;font-family:inherit}
.chart .bl{fill:var(--ink);font-size:12px;font-family:inherit}
.chart .bv{fill:var(--muted);font-size:11.5px;font-family:inherit}
.chart .anl{font-size:10.5px;font-weight:700;font-family:inherit;paint-order:stroke;stroke:var(--card);stroke-width:3px;stroke-linejoin:round}
.legend{display:flex;flex-wrap:wrap;gap:14px;font-size:11.5px;color:var(--muted);padding:4px 2px 2px}
.legend i{display:inline-block;width:11px;height:3px;border-radius:2px;margin-right:6px;vertical-align:middle}
.src{font-size:11.5px;color:var(--muted);margin:0 0 20px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin:0 0 18px}
.two .tw table{min-width:0}
.tw table.dar{min-width:0}
.two>.box{margin:0}
footer{border-top:1px solid var(--line);margin-top:20px;padding:22px 0 60px;
  font-size:11.5px;color:var(--muted)}
.gl{display:grid;grid-template-columns:186px minmax(0,1fr);gap:8px 20px;font-size:13px}
.gl dt{font-weight:640}.gl dd{margin:0;color:var(--muted)}
/* --- Mobil icindekiler: yuzen dugme + alt sayfa --------------------------- */
.tocfab{display:none;position:fixed;right:16px;bottom:16px;z-index:120;width:52px;height:52px;
  border-radius:50%;background:var(--teal);color:#fff;border:none;cursor:pointer;
  box-shadow:0 8px 26px rgba(0,0,0,.28);place-items:center;padding:0}
.tocfab svg{width:22px;height:22px}
.tocfab:focus-visible{outline:2px solid var(--coral);outline-offset:3px}
:root[data-theme="dark"] .tocfab,
:root:not([data-theme="light"]) .tocfab{background:var(--coral-deep)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .tocfab{background:var(--teal)}}
.tocsheet{position:fixed;inset:0;background:rgba(8,18,22,.6);z-index:130;display:none;
  align-items:flex-end}
.tocsheet.open{display:flex}
.tocsheet__in{--tu:calc((100vh - 64px) / 37.5);--tu:calc((100dvh - 64px) / 37.5);
  background:var(--card);width:100%;height:calc(100vh - 16px);height:calc(100dvh - 16px);overflow:hidden;
  display:flex;flex-direction:column;
  border-radius:18px 18px 0 0;padding:6px 12px calc(var(--tu) * .5)}
.tocsheet__tut{flex:0 0 auto;width:42px;height:4px;border-radius:2px;background:var(--line);
  margin:4px auto calc(var(--tu) * .35)}
.tocsheet .grp{font-size:clamp(8.5px, calc(var(--tu) * .5), 11px);letter-spacing:.14em;color:var(--ink-2);font-weight:700;
  margin:0;padding:0 10px calc(var(--tu) * .14);flex:1.75 1 0;min-height:0;max-height:64px;display:flex;align-items:flex-end;line-height:1.1}
.tocsheet .grp:first-of-type{flex:0 0 auto}
.tocsheet ul.tocg{display:contents;list-style:none;margin:0;padding:0}
.tocsheet ul.tocg li{flex:1 1 0;min-height:0;max-height:46px;display:flex;align-items:center}
.tocsheet ul.tocg li a{flex:1;min-width:0}
.tocsheet a{display:flex;align-items:center;gap:10px;padding:clamp(0px, calc(var(--tu) * .12), 8px) 11px;border-radius:10px;
  color:var(--ink-2);font-size:clamp(9px, calc(var(--tu) * .62), 14px);font-weight:600;text-decoration:none;line-height:1.2}
.tocsheet a .tx{min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tocsheet a .no{flex:0 0 auto;display:inline-flex;align-items:center;justify-content:center;
  width:clamp(17px, calc(var(--tu) * 1), 24px);height:clamp(12px, calc(var(--tu) * .8), 22px);border-radius:6px;background:var(--neutral);color:var(--muted);
  font-size:clamp(7px, calc(var(--tu) * .44), 10px);font-weight:700;font-variant-numeric:tabular-nums}
/* Yatay telefon: panel iki sutuna bolunur, yine kaydirma gerekmez */
@media (orientation:landscape) and (max-height:540px){
  .tocsheet__in{--tu:calc((100vh - 40px) / 22);--tu:calc((100dvh - 40px) / 22);display:grid;grid-auto-flow:column;
    grid-template-columns:1fr 1fr;grid-template-rows:auto repeat(18, minmax(0, 1fr));column-gap:26px}
  .tocsheet__tut{grid-column:1 / -1;grid-row:1;margin:2px auto 4px}
  .tocsheet ul.tocg li,.tocsheet .grp,.tocsheet .grp:first-of-type{max-height:none;min-height:0}
}
}
.tocsheet a:hover,.tocsheet a:focus{background:var(--neutral);color:var(--ink);text-decoration:none}
.tocsheet a.on{background:var(--coral-tint);color:var(--ink)}
.tocsheet a.on .no{background:var(--teal);color:#fff}
:root[data-theme="dark"] .tocsheet a.on,
:root:not([data-theme="light"]) .tocsheet a.on{background:rgba(255,123,82,.16)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .tocsheet a.on{background:var(--coral-tint)}}
:root[data-theme="dark"] .tocsheet a.on .no,
:root:not([data-theme="light"]) .tocsheet a.on .no{background:var(--coral-deep)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .tocsheet a.on .no{background:var(--teal)}}

/* --- Excel indirme butonu ------------------------------------------------- */
.dl{display:inline-flex;align-items:center;gap:7px;font:inherit;font-size:12px;font-weight:600;
  line-height:1.2;padding:7px 13px;border-radius:6px;text-decoration:none;white-space:nowrap;
  border:1px solid rgba(255,255,255,.28);background:rgba(255,255,255,.10);color:#fff;
  transition:background .12s,border-color .12s}
.dl:hover,.dl:focus{background:rgba(255,255,255,.20);border-color:rgba(255,255,255,.5);
  text-decoration:none;color:#fff}
.dl:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.dl svg{width:14px;height:14px;flex:0 0 auto}
.tema{display:inline-flex;align-items:center;justify-content:center;width:32px;height:32px;
  border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,.28);
  background:rgba(255,255,255,.10);color:#fff;padding:0}
.tema:hover{background:rgba(255,255,255,.20);border-color:rgba(255,255,255,.5)}
.tema:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.tema svg{width:15px;height:15px;display:block}
.tema .ay{display:none}
:root[data-theme="dark"] .tema .ay{display:block}
:root[data-theme="dark"] .tema .gunes{display:none}
.dilbtn{display:inline-flex;align-items:center;justify-content:center;gap:5px;height:32px;
  padding:0 9px;border-radius:6px;cursor:pointer;border:1px solid rgba(255,255,255,.28);
  background:rgba(255,255,255,.10);color:#fff;font:650 11.5px/1 var(--f);letter-spacing:.04em}
.dilbtn:hover{background:rgba(255,255,255,.20);border-color:rgba(255,255,255,.5)}
.dilbtn:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.dilbtn svg{width:14px;height:14px;display:block;opacity:.9}
.de{border-bottom:1px dotted var(--coral-deep);cursor:help}
.de:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
th .de,.pk .de,.bt .de{border-bottom-color:rgba(255,255,255,.55)}
a .de{border-bottom:0;cursor:inherit}
.dl .dl-alt{font-weight:400;opacity:.72}
.appbar .in{gap:14px}
.dl-foot{border-color:var(--line);background:var(--card);color:var(--ink);margin-top:12px}
.dl-foot:hover,.dl-foot:focus{background:var(--neutral);border-color:var(--coral);color:var(--ink)}
@media(max-width:720px){
  .dl .dl-alt{display:none}
  .brandbit .lbl{display:none}
}

/* --- Dis baglantilar ----------------------------------------------------- */
a.dis{color:var(--ink);text-decoration:none;border-bottom:1px solid var(--line);
  transition:border-color .12s,color .12s;word-break:break-word}
a.dis:hover,a.dis:focus{color:var(--coral-deep);border-bottom-color:var(--coral)}
a.dis:focus-visible{outline:2px solid var(--coral);outline-offset:2px;border-radius:2px}
a.dis::after{content:"\\2197";font-size:.78em;margin-left:3px;color:var(--muted);vertical-align:super}
a.dis:hover::after{color:var(--coral-deep)}
td a.dis{font-weight:500}
.srclist{list-style:none;padding:0;margin:0}
.srclist li{border-top:1px solid var(--line);padding:11px 0}
.srclist li:first-child{border-top:0}
.srclist .sk{font-weight:640;font-size:13px}
.srclist .sa{color:var(--muted);font-size:12.5px;margin-top:2px}
.srclist .sl{margin-top:4px;font-size:12.5px}
/* --- Tablo ustu grup sekmeleri ------------------------------------------- */
.tabs{display:flex;flex-wrap:wrap;gap:7px;margin:0 0 11px}
.tabs button{font:inherit;font-size:12.5px;padding:6px 13px;border-radius:20px;cursor:pointer;
  border:1px solid var(--line);background:var(--card);color:var(--ink-2);line-height:1.3}
.tabs button:hover{border-color:var(--coral);color:var(--ink)}
.tabs button:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
.tabs button[aria-selected="true"]{background:var(--teal);border-color:var(--teal);color:#fff;font-weight:600}
:root[data-theme="dark"] .tabs button[aria-selected="true"],
:root:not([data-theme="light"]) .tabs button[aria-selected="true"]{background:var(--coral-deep);border-color:var(--coral-deep)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .tabs button[aria-selected="true"]{background:var(--teal);border-color:var(--teal)}}
.tabnote{font-size:12px;color:var(--muted);margin:0 0 11px}
.orneklabel{font-size:10.5px;letter-spacing:.1em;color:var(--coral-deep);margin:0 0 6px;font-weight:600}
.kwlist{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.kwlist .kw{display:inline-block;font-size:12px;padding:3px 10px;border-radius:5px;
  background:var(--neutral);color:var(--ink);border:1px solid var(--line);
  font-family:"SFMono-Regular",Consolas,monospace}
.olcek{display:block;position:relative;height:11px;border-radius:6px;background:var(--neutral);
  min-width:74px;overflow:hidden}
.bar-mini{display:block;height:100%;border-radius:6px;background:var(--teal);min-width:3px}
:root[data-theme="dark"] .bar-mini,:root:not([data-theme="light"]) .bar-mini{background:var(--coral-deep)}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) .bar-mini{background:var(--teal)}}
.pay{white-space:nowrap;font-variant-numeric:tabular-nums}

/* --- Sutun basligi aciklamasi ve grafik deger balonu --------------------- */
/* Balon .tw{overflow-x:auto} sarmalayicisi tarafindan kirpilmasin diye
   position:fixed tek bir ogeden yonetilir; th ve grafikler ayni ogeyi kullanir. */
th[data-t]{cursor:help}
.kpi[data-t],.metric[data-t]{cursor:help}
.kpi[data-t] .k,.metric[data-t] .mk{text-decoration:underline dotted;text-decoration-color:color-mix(in srgb,currentColor 45%,transparent);text-underline-offset:3px}
.kpi[data-t]:focus-visible,.metric[data-t]:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
th[data-t] span.q{border-bottom:1px dotted rgba(255,255,255,.55);padding-bottom:1px}
#tt{position:fixed;z-index:80;max-width:290px;background:var(--teal);color:#fff;
  font-size:11.5px;line-height:1.45;padding:8px 11px;border-radius:6px;
  box-shadow:0 6px 22px rgba(0,0,0,.22);pointer-events:none;opacity:0;
  transition:opacity .12s ease}
#tt.on{opacity:1}
#tt .tt-b{font-weight:650;display:block;margin-bottom:3px}
#tt .tt-r{display:flex;align-items:center;gap:7px;justify-content:space-between;
  white-space:nowrap;margin-top:2px}
#tt .tt-r i{display:inline-block;width:9px;height:3px;border-radius:2px;flex:0 0 auto}
#tt .tt-r .tt-n{margin-left:auto;font-weight:650;font-variant-numeric:tabular-nums}
:root[data-theme="dark"] #tt,
:root:not([data-theme="light"]) #tt{background:#1D3F3B}
@media (prefers-color-scheme:light){:root:not([data-theme="dark"]) #tt{background:var(--teal)}}
.chart .hz{fill:transparent}
.chart .hx{stroke:var(--muted);stroke-width:1;stroke-dasharray:3 3}
.chart .hp{stroke:var(--card);stroke-width:1.6}

.tocbtn{display:none}
@media(max-width:1080px){
  :root{--toc:280px}
  .wrap{gap:26px}
  .sidenav a{font-size:min(clamp(8px, calc(var(--tu) * .56), 12.5px), 1.14vw)}
}
@media(max-width:940px){
  .wrap{grid-template-columns:1fr;gap:0;padding:0 16px}
  .sidenav{display:none}
  .tocfab{display:grid}
  main{padding:18px 0 84px}
  .two{grid-template-columns:1fr}
  h1{font-size:23px}
  .hero{padding:2px 0 16px;margin-bottom:22px}
  .sub{font-size:12.5px}
  section{padding:26px 0}
  h2{font-size:18.5px}
  h2 .no{margin-right:9px}
  h3{font-size:14.5px;margin:20px 0 8px}
  .kpis{grid-template-columns:repeat(auto-fit,minmax(148px,1fr));gap:10px}
  .kpi{padding:13px 13px}
  .kpi .v{font-size:21px}
  .kpi .k{font-size:11px}
  .box,.insight{padding:14px 15px}
  .insight{padding-left:36px}
  .insight::before{left:14px}
  table{font-size:12.5px;min-width:560px}
  th{padding:9px 10px;font-size:11px}
  td{padding:9px 10px}
  .tw.uzun{max-height:min(460px,64vh)}
  .tabs{gap:6px}
  .tabs button{font-size:12px;padding:5px 11px}
  .fig{padding:12px 12px 8px;overflow-x:auto}
  .fig .chart{min-width:520px}
  .fig .legend{min-width:520px}
  .gl{grid-template-columns:1fr;gap:2px 0}
  .gl dt{margin-top:10px}
  .appbar .in{padding:10px 16px;gap:10px}
  .logo-card img,.ib img{height:19px}
}
@media(max-width:720px){
  .dl .dl-alt{display:none}
  .brandbit .lbl{display:none}
  .appbar .in{gap:8px}
  .tocfab{right:14px;bottom:14px;width:48px;height:48px}
}
@media(max-width:520px){
  .wrap{padding:0 13px}
  h1{font-size:20px}
  h2{font-size:17px}
  .kpis{grid-template-columns:1fr 1fr}
  .kpi .v{font-size:19px}
  .dl{padding:6px 10px;font-size:11.5px}
  .tema{width:30px;height:30px}
  .dilbtn{height:30px;padding:0 7px;font-size:11px}
  .dilbtn svg{display:none}
  .srclist .sl{word-break:break-all}
  .kwlist .kw{font-size:11px;padding:3px 8px}
}
@media(max-width:430px){
  .appbar .in{padding:9px 12px;gap:6px}
  .brandbit{gap:6px !important;min-width:0}
  .logo-card{padding:4px 7px}
  .logo-card img,.ib img{height:17px}
  .appbar .dl{padding:6px 8px;gap:0}
  .appbar .dl > .t{display:none}
  .tema{width:28px;height:28px}
  .dilbtn{height:28px;padding:0 6px}
}
@media (prefers-reduced-motion:reduce){
  *{scroll-behavior:auto!important;transition-duration:.01ms!important}
}
@media print{
  .appbar,.sidenav,.tocfab,.tocsheet,.dl,.tema,.dilbtn{display:none!important}
  .wrap{grid-template-columns:1fr;max-width:none;padding:0}
  section{break-inside:avoid;padding:14px 0}
  .tw.uzun{max-height:none}
  a.dis::after{content:" (" attr(href) ")";font-size:.75em;color:#555}
}
"""
