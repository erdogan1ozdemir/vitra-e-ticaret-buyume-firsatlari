# -*- coding: utf-8 -*-
"""Kabuk parcalari: JS, kaynakca CSS, tema ve indirme ikonlari (Dusch-WC raporundan)."""
JS = r"""
/* JavaScript calisiyorsa :target yedegi devre disi; vurguyu scroll-spy yonetir */
document.documentElement.classList.add('js');
(function(){
  var bar=document.querySelector('.appbar'); if(!bar) return;
  function olc(){document.documentElement.style.setProperty('--apph', Math.round(bar.getBoundingClientRect().height)+'px');}
  olc(); window.addEventListener('resize', olc);
  if(window.ResizeObserver){ try{ new ResizeObserver(olc).observe(bar); }catch(e){} }
})();
/* --- Acik / koyu tema degistirici ---------------------------------------- */
(function(){
  var kok=document.documentElement, btn=document.getElementById('tema');
  if(!btn) return;
  // Rapor varsayilan olarak acik temada acilir; kullanicinin kendi secimi
  // varsa o gecerlidir.
  var kayit=null;
  try{kayit=localStorage.getItem('vitra-tema');}catch(e){}
  var aktif = (kayit === 'dark' || kayit === 'light') ? kayit : 'light';
  function basliklandir(){
    var en = kok.getAttribute('data-dil')==='en';
    btn.title = (aktif==='dark')
      ? (en ? 'Switch to light theme' : 'Açık temaya geç')
      : (en ? 'Switch to dark theme'  : 'Koyu temaya geç');
    btn.setAttribute('aria-label', en
      ? 'Switch between light and dark theme'
      : 'Açık ve koyu tema arasında geçiş yap');
  }
  function uygula(t){
    kok.setAttribute('data-theme', t);
    btn.setAttribute('aria-pressed', t==='dark' ? 'true' : 'false');
    aktif=t;
    basliklandir();
  }
  uygula(aktif);
  document.addEventListener('dilchange', basliklandir);
  btn.addEventListener('click',function(){
    var y = aktif==='dark' ? 'light' : 'dark';
    uygula(y);
    try{localStorage.setItem('vitra-tema', y);}catch(e){}
  });
})();

/* --- Tablo ustu arama grubu sekmeleri ------------------------------------ */
(function(){
  [].forEach.call(document.querySelectorAll('.tabs[role="tablist"]'),function(liste){
    var butonlar=[].slice.call(liste.querySelectorAll('button[role="tab"]'));
    function sec(btn,odak){
      butonlar.forEach(function(b){
        var acik = (b===btn);
        b.setAttribute('aria-selected', acik?'true':'false');
        b.setAttribute('tabindex', acik?'0':'-1');
        var panel=document.getElementById(b.getAttribute('aria-controls'));
        if(panel) panel.hidden = !acik;
      });
      if(odak) btn.focus();
    }
    butonlar.forEach(function(b,i){
      b.setAttribute('tabindex', b.getAttribute('aria-selected')==='true'?'0':'-1');
      b.addEventListener('click',function(){sec(b,false);});
      b.addEventListener('keydown',function(e){
        var y=null;
        if(e.key==='ArrowRight'||e.key==='ArrowDown') y=butonlar[(i+1)%butonlar.length];
        if(e.key==='ArrowLeft'||e.key==='ArrowUp') y=butonlar[(i-1+butonlar.length)%butonlar.length];
        if(e.key==='Home') y=butonlar[0];
        if(e.key==='End') y=butonlar[butonlar.length-1];
        if(y){e.preventDefault();sec(y,true);}
      });
    });
  });
})();

/* --- Sutun basligi aciklamasi ve grafik deger balonu --------------------- */
(function(){
  var tt=document.createElement('div'); tt.id='tt'; tt.hidden=true;
  document.body.appendChild(tt);
  function kac(t){return String(t).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
  function ingilizce(){return document.documentElement.getAttribute('data-dil')==='en';}
  function say(n){
    if(n===null||n===undefined) return '-';
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ingilizce() ? ',' : '.');
  }
  function goster(icerik,x,y){
    tt.innerHTML=icerik; tt.hidden=false; tt.style.left='0px'; tt.style.top='0px';
    var r=tt.getBoundingClientRect();
    var L=Math.min(Math.max(8,x-r.width/2), window.innerWidth-r.width-8);
    var T=y-r.height-12; if(T<8) T=y+20;
    tt.style.left=L+'px'; tt.style.top=T+'px'; tt.classList.add('on');
  }
  function gizle(){tt.classList.remove('on'); tt.hidden=true;}

  /* govde metnindeki terimler - dil degisince yeniden uretildiginden olay devri kullanilir */
  function termAc(el){
    var a=el.getAttribute('data-term'); if(!a) return;
    var r=el.getBoundingClientRect();
    goster('<span class="tt-b">'+kac(el.textContent.trim())+'</span>'+kac(a), r.left+r.width/2, r.top);
  }
  document.addEventListener('mouseover',function(e){ var el=e.target.closest?e.target.closest('span.term'):null; if(el) termAc(el); });
  document.addEventListener('mouseout',function(e){ var el=e.target.closest?e.target.closest('span.term'):null; if(el) gizle(); });
  document.addEventListener('focusin',function(e){ var el=e.target.closest?e.target.closest('span.term'):null; if(el) termAc(el); });
  document.addEventListener('focusout',function(e){ var el=e.target.closest?e.target.closest('span.term'):null; if(el) gizle(); });

  /* Almanca ifadeler - dil degisince yeniden uretildiginden olay devri kullanilir */
  function deAc(el){
    var en = document.documentElement.getAttribute('data-dil')==='en';
    var a = el.getAttribute(en ? 'data-de-en' : 'data-de-tr');
    if(!a) return;
    var r=el.getBoundingClientRect();
    goster('<span class="tt-b">'+kac(el.textContent.trim())+'</span>'+kac(a),
           r.left+r.width/2, r.top);
  }
  document.addEventListener('mouseover',function(e){
    var el = e.target.closest ? e.target.closest('span.de') : null;
    if(el) deAc(el);
  });
  document.addEventListener('mouseout',function(e){
    var el = e.target.closest ? e.target.closest('span.de') : null;
    if(el) gizle();
  });
  document.addEventListener('focusin',function(e){
    var el = e.target.closest ? e.target.closest('span.de') : null;
    if(el) deAc(el);
  });
  document.addEventListener('focusout',function(e){
    var el = e.target.closest ? e.target.closest('span.de') : null;
    if(el) gizle();
  });

  /* sutun basliklari */
  [].forEach.call(document.querySelectorAll('th[data-t]'),function(th){
    function ac(){
      var r=th.getBoundingClientRect();
      goster('<span class="tt-b">'+kac(th.textContent.trim())+'</span>'+kac(th.getAttribute('data-t')),
             r.left+r.width/2, r.top);
    }
    th.addEventListener('mouseenter',ac);
    th.addEventListener('focus',ac);
    th.addEventListener('mouseleave',gizle);
    th.addEventListener('blur',gizle);
    th.setAttribute('tabindex','0');
    th.setAttribute('title','');
    th.removeAttribute('title');
  });

  /* grafikler */
  [].forEach.call(document.querySelectorAll('.fig[data-grafik]'),function(fig){
    function veriOku(){
      try{return JSON.parse(fig.getAttribute('data-grafik'));}catch(e){return null;}
    }
    var d = veriOku(); if(!d) return;
    var svg=fig.querySelector('svg'); if(!svg) return;
    var hx=svg.querySelector('.hx');
    var hp=svg.querySelectorAll('.hp');
    var bantlar=svg.querySelectorAll('.hz');
    var gizli={};
    /* lejant: seriye tiklayinca grafikten kaldir / geri getir */
    [].forEach.call(fig.querySelectorAll('.legend .lg-t'),function(l){
      function cevir(){
        var k=parseInt(l.getAttribute('data-k'),10); gizli[k]=!gizli[k];
        l.classList.toggle('off',!!gizli[k]); l.setAttribute('aria-pressed',gizli[k]?'false':'true');
        var yol=svg.querySelector('path.sr[data-k="'+k+'"]'); if(yol) yol.style.display=gizli[k]?'none':'';
        if(hp[k]) hp[k].style.display='none';
      }
      l.addEventListener('click',cevir);
      l.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();cevir();}});
    });
    function svgKonum(x,y){
      var vb=svg.viewBox.baseVal, r=svg.getBoundingClientRect();
      return {x:r.left + x*r.width/vb.width, y:r.top + y*r.height/vb.height};
    }
    [].forEach.call(bantlar,function(z){
      var i=parseInt(z.getAttribute('data-i'),10);
      function ac(){
        var icerik, kx, ky;
        d = veriOku() || d;
        if(d.tip==='bar'){
          var sat=d.satirlar[i];
          var dv=Number(sat.deger), mt=Math.abs(dv).toFixed(1), isr=dv>0?'+':(dv<0?'-':'');
          var yazi=ingilizce() ? isr+mt+'%' : isr+'%'+mt.replace('.',',');
          icerik='<span class="tt-b">'+kac(sat.ad)+'</span><span class="tt-r">'
               + '<i style="background:'+sat.renk+'"></i><span>'+kac(d.olcu || (ingilizce() ? 'YoY change' : 'YoY değişim'))+'</span>'
               + '<span class="tt-n">'+yazi+'</span></span>';
          var rz=z.getBoundingClientRect();
          kx=rz.left+rz.width/2; ky=rz.top;
        } else {
          icerik='<span class="tt-b">'+kac(d.aylar[i])+'</span>';
          var enUst=null;
          for(var k=0;k<d.seriler.length;k++){
            var se=d.seriler[k], v=se.deger[i];
            if(gizli[k]){ if(hp[k]) hp[k].style.display='none'; continue; }
            icerik+='<span class="tt-r"><i style="background:'+se.renk+'"></i>'
                  + '<span>'+kac(se.ad)+'</span><span class="tt-n">'+say(v)+'</span></span>';
            if(se.py[i]!==null && (enUst===null || se.py[i]<enUst)) enUst=se.py[i];
            if(hp[k]){
              if(se.py[i]===null){hp[k].style.display='none';}
              else{
                hp[k].setAttribute('cx',d.px[i]); hp[k].setAttribute('cy',se.py[i]);
                hp[k].setAttribute('fill',se.renk); hp[k].style.display='';
              }
            }
          }
          if(hx){hx.setAttribute('x1',d.px[i]); hx.setAttribute('x2',d.px[i]); hx.style.display='';}
          var k1=svgKonum(d.px[i], enUst===null?0:enUst);
          kx=k1.x; ky=k1.y;
        }
        goster(icerik,kx,ky);
      }
      z.addEventListener('mouseenter',ac);
      z.addEventListener('mousemove',ac);
    });
    function temizle(){
      gizle();
      if(hx) hx.style.display='none';
      [].forEach.call(hp,function(c){c.style.display='none';});
    }
    svg.addEventListener('mouseleave',temizle);
    fig.addEventListener('mouseleave',temizle);
  });
  window.addEventListener('scroll',gizle,{passive:true});
})();

(function(){
  var links=[].slice.call(document.querySelectorAll('.sidenav a[href^="#"]'));
  var mobil=[].slice.call(document.querySelectorAll('.tocsheet a[href^="#"]'));
  var secs=links.map(function(a){return document.getElementById(a.getAttribute('href').slice(1));});
  function bar(){var b=document.querySelector('.appbar');return b?b.getBoundingClientRect().height:0;}
  function konum(){
    return window.pageYOffset||document.documentElement.scrollTop||document.body.scrollTop||0;
  }
  function tasi(y){
    try{window.scrollTo(0,y);}catch(e){}
    if(document.scrollingElement) document.scrollingElement.scrollTop=y;
    else{document.documentElement.scrollTop=y;document.body.scrollTop=y;}
  }
  function git(id){
    var el=document.getElementById(id); if(!el) return;
    var basla=konum();
    var y=Math.max(0,el.getBoundingClientRect().top+basla-(bar()+24));
    var yumusak=false;
    try{window.scrollTo({top:y,behavior:'smooth'});yumusak=true;}catch(e){}
    if(history.replaceState) history.replaceState(null,'','#'+id);
    setTimeout(function(){
      if(Math.abs(konum()-basla)<2 && Math.abs(y-basla)>2) tasi(y);
      isaretle();
      setTimeout(isaretle,420);
    }, yumusak?70:0);
  }
  links.concat(mobil).forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault();git(a.getAttribute('href').slice(1));});
  });

  /* mobil icindekiler sayfasi */
  var fab=document.getElementById('tocfab'), sheet=document.getElementById('tocsheet');
  if(fab&&sheet){
    var oncekiOdak=null;
    function sayfa(ac){
      sheet.classList.toggle('open',ac);
      fab.setAttribute('aria-expanded',ac?'true':'false');
      document.body.style.overflow = ac ? 'hidden' : '';
      if(ac){
        oncekiOdak=document.activeElement;
        var ilk=sheet.querySelector('a.on')||sheet.querySelector('a');
        if(ilk) ilk.focus();
      }else if(oncekiOdak&&oncekiOdak.focus){oncekiOdak.focus();}
    }
    fab.addEventListener('click',function(){sayfa(!sheet.classList.contains('open'));});
    sheet.addEventListener('click',function(e){
      if(e.target===sheet||(e.target.closest&&e.target.closest('a'))) sayfa(false);
    });
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&sheet.classList.contains('open')) sayfa(false);
    });
    window.addEventListener('resize',function(){
      if(window.innerWidth>940&&sheet.classList.contains('open')) sayfa(false);
    });
  }
  function isaretle(){
    var esik=bar()+40, akt=0;
    for(var i=0;i<secs.length;i++){
      if(secs[i] && secs[i].getBoundingClientRect().top<=esik) akt=i;
    }
    if(window.innerHeight+window.pageYOffset>=document.body.scrollHeight-4) akt=secs.length-1;
    links.forEach(function(a,i){a.classList.toggle('on',i===akt);});
    mobil.forEach(function(a,i){a.classList.toggle('on',i===akt);});
  }
  var son=0, zam=null;
  function planla(){
    var t=Date.now();
    if(t-son>80){son=t;isaretle();}
    else{clearTimeout(zam);zam=setTimeout(function(){son=Date.now();isaretle();},90);}
  }
  window.addEventListener('scroll',planla,{passive:true});
  window.addEventListener('resize',planla);
  // Bazi statik onizleme ve sandbox baglamlarinda scroll olayi tetiklenmez;
  // vurgunun orada da guncel kalmasi icin konum degisimi ayrica izlenir.
  var sonY=-1;
  setInterval(function(){
    var y=konum();
    if(y!==sonY){sonY=y;isaretle();}
  },350);
  isaretle();
  if(location.hash){var h=location.hash.slice(1);setTimeout(function(){git(h);},80);}
})();

/* tablolar: sutun basligina tiklayinca siralama, tablo ustunde kopyalama dugmesi */
(function(){
  function en(){return document.documentElement.getAttribute('data-dil')==='en';}
  function sayi(t){
    t=String(t).trim();
    if(!t||t==='-'||t==='–')return null;
    var neg=/^[-−]/.test(t)||/^-%/.test(t);
    var m=t.replace(/[+\-−%\s₺TL]/g,'').match(/^(\d[\d.,]*)([KMB])?\+?/i);
    if(!m)return null;
    var s=m[1];
    if(en()){s=s.replace(/,/g,'');}else{s=s.replace(/\./g,'').replace(',','.');}
    var v=parseFloat(s); if(isNaN(v))return null;
    var k={K:1e3,M:1e6,B:1e9}[(m[2]||'').toUpperCase()]||1;
    return (neg?-v:v)*k;
  }
  function metin(td){return (td.innerText||td.textContent||'').replace(/\s+/g,' ').trim();}
  function sirala(tbl,idx,yon){
    var tb=tbl.tBodies[0]; if(!tb)return;
    var rows=[].slice.call(tb.rows);
    var vals=rows.map(function(r,i){var td=r.cells[idx];var t=td?metin(td):'';return {r:r,i:i,t:t,n:sayi(t)};});
    var num=vals.filter(function(v){return v.t&&v.t!=='-';}).every(function(v){return v.n!==null;});
    vals.sort(function(a,b){
      var c;
      if(num){var x=a.n===null?-Infinity:a.n,y=b.n===null?-Infinity:b.n;c=x-y;}
      else{c=a.t.localeCompare(b.t,en()?'en':'tr',{numeric:true,sensitivity:'base'});}
      if(c===0)c=a.i-b.i;
      return yon==='d'?-c:c;
    });
    vals.forEach(function(v){tb.appendChild(v.r);});
  }
  [].forEach.call(document.querySelectorAll('.tw table'),function(tbl){
    var ths=tbl.tHead?tbl.tHead.rows[0].cells:[];
    [].forEach.call(ths,function(th,idx){
      th.classList.add('srt');
      function tik(){
        var yon=th.classList.contains('sa')?'d':'a';
        [].forEach.call(ths,function(o){o.classList.remove('sa','sd');o.removeAttribute('aria-sort');});
        th.classList.add(yon==='a'?'sa':'sd'); th.setAttribute('aria-sort',yon==='a'?'ascending':'descending');
        sirala(tbl,idx,yon);
      }
      th.addEventListener('click',tik);
      th.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();tik();}});
    });
  });
  var IK='<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5V3.5a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2"/></svg>';
  [].forEach.call(document.querySelectorAll('.tw'),function(tw){
    var box=document.createElement('div'); box.className='tbox';
    var bar=document.createElement('div'); bar.className='tbar';
    var b=document.createElement('button'); b.type='button'; b.className='tcopy';
    function etiket(){b.innerHTML=IK+'<span>'+(en()?'Copy table':'Tabloyu kopyala')+'</span>'; b.title=en()?'Copy the table with its columns (paste into Excel or Sheets)':'Tabloyu sütunlarıyla kopyala (Excel veya Sheets\'e yapıştırılır)';}
    etiket(); document.addEventListener('dilchange',etiket);
    b.addEventListener('click',function(){
      var tbl=tw.querySelector('table'); if(!tbl)return;
      var satirlar=[].slice.call(tbl.rows).map(function(r){return [].slice.call(r.cells).map(function(c){return metin(c).replace(/\t/g,' ');});});
      var tsv=satirlar.map(function(r){return r.join('\t');}).join('\n');
      var html='<table>'+satirlar.map(function(r,i){var tag=i===0?'th':'td';return '<tr>'+r.map(function(c){return '<'+tag+'>'+c.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</'+tag+'>';}).join('')+'</tr>';}).join('')+'</table>';
      function ok(){b.classList.add('ok');b.querySelector('span').textContent=en()?'Copied':'Kopyalandı';setTimeout(function(){b.classList.remove('ok');etiket();},1600);}
      if(navigator.clipboard&&window.ClipboardItem){
        navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([tsv],{type:'text/plain'}),'text/html':new Blob([html],{type:'text/html'})})]).then(ok,function(){navigator.clipboard.writeText(tsv).then(ok);});
      }else if(navigator.clipboard){navigator.clipboard.writeText(tsv).then(ok);}
    });
    bar.appendChild(b); tw.parentNode.insertBefore(box,tw); box.appendChild(bar); box.appendChild(tw);
  });
})();
"""

KAYNAKCA_CSS = """
sup.ref{font-size:.68em;line-height:0;margin-left:1px;white-space:normal;overflow-wrap:anywhere}
sup.ref a{color:var(--coral-deep);text-decoration:none;font-weight:600;padding:0 1px}
sup.ref a:hover,sup.ref a:focus-visible{text-decoration:underline}
ol.kaynakca{list-style:none;padding:0;margin:0;counter-reset:none}
ol.kaynakca li{display:flex;gap:12px;border-top:1px solid var(--line);padding:9px 0;font-size:12.5px;scroll-margin-top:calc(var(--appbar-h,64px) + 24px)}
ol.kaynakca li:first-child{border-top:0}
ol.kaynakca .kn{flex:0 0 30px;font-variant-numeric:tabular-nums;color:var(--muted);font-weight:600}
ol.kaynakca .kb{display:block;font-weight:600;margin-bottom:2px}
ol.kaynakca a.u{word-break:break-all;color:var(--ink-2);text-decoration-color:var(--line)}
ol.kaynakca a.u:hover{color:var(--coral-deep)}
ol.kaynakca .kt{display:block;color:var(--muted);font-size:11.5px;margin-top:2px}
ol.kaynakca li:target{background:var(--coral-tint);border-radius:6px;padding-left:6px}
.src sup.ref{font-size:.8em}
ul.kt{list-style:none;margin:4px 0 0;padding:0;display:grid;gap:12px}
ul.kt li{position:relative;padding-left:28px;line-height:1.62}
ul.kt li::before{content:"\\27A1";position:absolute;left:0;top:0;color:var(--coral-deep);font-weight:700}
ul.kt .ktl{display:block;margin:0 0 2px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--coral-deep);vertical-align:1px}
"""

TEMA = ('<button class="tema" type="button" id="tema" aria-label="Açık ve koyu tema arasında geçiş yap" '
         'title="Tema değiştir">'
         '<svg class="gunes" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4'
         'M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
         '<svg class="ay" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>'
         '</svg></button>')

IKON = ('<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
         'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M8 2v8m0 0 3-3m-3 3L5 7"/><path d="M2.5 11.5v1a1.5 1.5 0 0 0 1.5 1.5h8a1.5 1.5 0 0 0 1.5-1.5v-1"/></svg>')
