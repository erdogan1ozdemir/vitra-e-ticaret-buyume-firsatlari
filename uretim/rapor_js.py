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
  /* rapor her acilista acik temayla baslar; koyu tema yalnizca dugmeyle secilir */
  var aktif = 'light';
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

  /* isi haritasi hucreleri: hacim, degisim ve kategori payi */
  [].forEach.call(document.querySelectorAll('td[data-t], .ac[data-t]'),function(td){
    function ac(){ var r=td.getBoundingClientRect(); goster(kac(td.getAttribute('data-t')), r.left+r.width/2, r.top); }
    td.addEventListener('mouseenter',ac); td.addEventListener('mouseleave',gizle);
    td.addEventListener('focus',ac); td.addEventListener('blur',gizle);
  });

  /* tablo kaynak logolari: kaynak, kapsam ve veri donemi */
  [].forEach.call(document.querySelectorAll('.tk[data-t]'),function(tk){
    function ac(){
      var r=tk.getBoundingClientRect();
      goster('<span class="tt-b">'+kac(tk.getAttribute('aria-label')||'')+'</span>'+kac(tk.getAttribute('data-t')), r.left+r.width/2, r.top);
    }
    tk.addEventListener('mouseenter',ac); tk.addEventListener('focus',ac);
    tk.addEventListener('mouseleave',gizle); tk.addEventListener('blur',gizle);
  });

  /* karolar (KPI ve metrik kartlari): neyi olctugu, birimi, donemi ve kaynagi */
  [].forEach.call(document.querySelectorAll('.kpi[data-t], .metric[data-t]'),function(kr){
    function ac(){
      var r=kr.getBoundingClientRect(), bas=kr.querySelector('.k, .mk');
      goster('<span class="tt-b">'+kac(bas?bas.textContent.trim():'')+'</span>'+kac(kr.getAttribute('data-t')), r.left+r.width/2, r.top);
    }
    kr.addEventListener('mouseenter',ac); kr.addEventListener('focus',ac);
    kr.addEventListener('mouseleave',gizle); kr.addEventListener('blur',gizle);
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
    var gizli={}, pyO=null;
    (d.gizli||[]).forEach(function(k){gizli[k]=true;});
    function sayiYaz(v,ond){
      var en=ingilizce(), t=Number(v).toFixed(ond||0), p=t.split('.');
      p[0]=p[0].replace(/\B(?=(\d{3})+(?!\d))/g, en?',':'.');
      return p.length>1 ? p[0]+(en?'.':',')+p[1] : p[0];
    }
    function degerYaz(v){
      if(v===null||v===undefined) return '-';
      if(!d.birimk) return say(v);
      return d.birimk[ingilizce()?1:0].replace('{v}', sayiYaz(v,d.ond));
    }
    function eksen(t,ymax){
      if(t && (t>=1e6 || ymax>=d.olcek.kmax)){
        var b=t>=1e6?'M':'K', v=t>=1e6?t/1e6:t/1e3, r=(Math.round(v*10)/10).toString();
        return (ingilizce()?r:r.replace('.',','))+b;
      }
      return t===Math.round(t) ? sayiYaz(t,0) : sayiYaz(t,1);
    }
    /* acik serilere gore y eksenini yeniden kurar (yalniz olcek tanimli grafiklerde) */
    function olcekle(){
      var g=d.olcek; if(!g) return;
      var mx=0;
      d.seriler.forEach(function(se,k){ if(gizli[k]) return; se.deger.forEach(function(v){ if(v!==null && v>mx) mx=v; }); });
      if(!mx) return;
      var ymax=mx*1.08;
      function Y(v){return g.ust+g.ih-g.ih*v/ymax;}
      var adim=Math.pow(10,Math.floor(Math.log10(ymax)))/2; while(ymax/adim>6) adim*=2;
      var gy=svg.querySelector('.gy'), h='';
      for(var t=0;t<=ymax;t+=adim){
        h+='<line class="grid" x1="'+g.sol+'" y1="'+Y(t).toFixed(1)+'" x2="'+g.sag+'" y2="'+Y(t).toFixed(1)+'"/>'
          +'<text class="ax" x="'+(g.sol-8)+'" y="'+(Y(t)+4).toFixed(1)+'" text-anchor="end">'+eksen(t,ymax)+'</text>';
      }
      if(gy) gy.innerHTML=h;
      pyO=d.seriler.map(function(se){ return se.deger.map(function(v){ return v===null?null:Math.round(Y(v)*10)/10; }); });
      d.seriler.forEach(function(se,k){
        var yol=svg.querySelector('path.sr[data-k="'+k+'"]'); if(!yol) return;
        var parca=[];
        se.deger.forEach(function(v,i){ if(v!==null) parca.push((parca.length?'L':'M')+d.px[i]+' '+pyO[k][i]); });
        yol.setAttribute('d',parca.join(' '));
      });
      /* peak / base notlari ikiden fazla seri acikken ust uste binmesin diye gizlenir */
      var acik=d.seriler.filter(function(se,k){return !gizli[k];}).length;
      [].forEach.call(svg.querySelectorAll('.an'),function(a){
        var k=+a.getAttribute('data-k'), i=+a.getAttribute('data-i'), py=pyO[k][i];
        a.style.display=(!gizli[k] && acik<=2)?'':'none';
        if(py===null) return;
        a.querySelector('circle').setAttribute('cy',py);
        a.querySelector('text').setAttribute('y',(a.getAttribute('data-yer')==='ust'?py-9:py+17).toFixed(1));
      });
      /* cakisan peak / base yazilari: gorunur yazilar soldan saga taranir, ust uste binen yazi kendi yonunde kaydirilir */
      var yazilar=[].slice.call(svg.querySelectorAll('.an')).filter(function(a){return a.style.display!=='none';}).map(function(a){
        var t=a.querySelector('text'), bb=t.getBBox(); return {t:t, x0:bb.x, x1:bb.x+bb.width, y:bb.y, h:bb.height, ust:a.getAttribute('data-yer')==='ust'};
      }).sort(function(p,q){return p.x0-q.x0;});
      for(var i=0;i<yazilar.length;i++){
        for(var tur=0;tur<6;tur++){
          var cak=false;
          for(var j=0;j<i;j++){
            var p=yazilar[i], q=yazilar[j];
            if(p.x0<q.x1+2 && q.x0<p.x1+2 && p.y<q.y+q.h && q.y<p.y+p.h){
              var dy=p.ust?-(p.y+p.h-q.y+1):(q.y+q.h-p.y+1);
              p.y+=dy; p.t.setAttribute('y',(parseFloat(p.t.getAttribute('y'))+dy).toFixed(1)); cak=true;
            }
          }
          if(!cak) break;
        }
      }      etiketCiz();
    }
    /* degerler: grafik ustunde etiketler (Degerler dugmesi); cizgi grafiklerde JS ile, digerlerinde hazir .dl etiketleri */
    var cizgiTip=!!(d.seriler && d.px), dlAcik=false;
    function kisa(v){
      if(d.birimk) return sayiYaz(v,d.ond);
      var a=Math.abs(v);
      if(a>=1e6) return sayiYaz(v/1e6,1)+'M';
      if(a>=1e3) return sayiYaz(v/1e3,a<1e5?1:0)+'K';
      return sayiYaz(v,d.ond||(v%1?1:0));
    }
    function etiketCiz(){
      if(!cizgiTip) return;
      var eski=svg.querySelector('g.dlg'); if(eski) eski.parentNode.removeChild(eski);
      if(!dlAcik) return;
      var ns='http://www.w3.org/2000/svg', g=document.createElementNS(ns,'g'); g.setAttribute('class','dlg');
      d.seriler.forEach(function(se,k){
        if(gizli[k]) return;
        se.deger.forEach(function(v,i){
          if(v===null||v===undefined) return;
          var py=pyO?pyO[k][i]:se.py[i]; if(py===null) return;
          var t=document.createElementNS(ns,'text'); t.setAttribute('x',d.px[i]); t.setAttribute('y',(py-7).toFixed(1));
          t.setAttribute('text-anchor','middle'); t.setAttribute('class','dlt'); t.setAttribute('fill',se.renk); t.textContent=kisa(v); g.appendChild(t);
        });
      });
      svg.appendChild(g);
      ayir();
    }
    /* ust uste binen deger etiketleri: x sirasiyla taranir, cakisan etiket noktasinin altina ya da asagi kaydirilir */
    function ayir(){
      if(!dlAcik) return;
      var L=[].slice.call(svg.querySelectorAll('.dl, .dlt')).filter(function(t){return t.style.display!=='none' && getComputedStyle(t).display!=='none';});
      L.forEach(function(t){ if(t.hasAttribute('data-y0')) t.setAttribute('y',t.getAttribute('data-y0')); else t.setAttribute('data-y0',t.getAttribute('y')); });
      var K=L.map(function(t){var bb=t.getBBox(); return {t:t,x0:bb.x,x1:bb.x+bb.width,y:bb.y,h:bb.height};}).sort(function(p,q){return p.x0-q.x0 || p.y-q.y;});
      for(var i=0;i<K.length;i++){
        for(var tur=0;tur<5;tur++){
          var cak=false;
          for(var j=0;j<i;j++){
            var p=K[i], q=K[j];
            if(p.x0<q.x1-1 && q.x0<p.x1-1 && p.y<q.y+q.h-1 && q.y<p.y+p.h-1){
              var dy=q.y+q.h+1-p.y; p.y+=dy; p.t.setAttribute('y',(parseFloat(p.t.getAttribute('y'))+dy).toFixed(1)); cak=true;
            }
          }
          if(!cak) break;
        }
      }
    }
    if(cizgiTip || svg.querySelector('.dl')){
      var db=document.createElement('button'); db.type='button'; db.className='dlb'; db.setAttribute('aria-pressed','false');
      function dbYaz(){ db.innerHTML='<svg viewBox="0 0 16 16" width="11" height="11" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2 13h12M4 10V6M8 10V3M12 10V7"/></svg><span>'+(ingilizce()?'Values':'Değerler')+'</span>'; db.title=ingilizce()?'Show values on the chart':'Değerleri grafikte göster'; }
      dbYaz(); document.addEventListener('dilchange',function(){ dbYaz(); etiketCiz(); });
      db.addEventListener('click',function(){ dlAcik=!dlAcik; db.setAttribute('aria-pressed',String(dlAcik)); fig.classList.toggle('dl-acik',dlAcik); etiketCiz(); if(!cizgiTip) ayir(); });
      var cap=fig.querySelector('figcaption');
      if(cap){ cap.appendChild(db); } else { var sat=document.createElement('div'); sat.className='dl-satir'; sat.appendChild(db); fig.insertBefore(sat, fig.firstChild); }
    }
    if(d.olcek) olcekle();
    if(d.olcek){
      new MutationObserver(function(){ if(pyO) olcekle(); }).observe(document.documentElement,{attributes:true,attributeFilter:['data-dil']});
    }
    /* lejant: seriye tiklayinca grafikten kaldir / geri getir */
    [].forEach.call(fig.querySelectorAll('.legend .lg-t'),function(l){
      function cevir(){
        var k=parseInt(l.getAttribute('data-k'),10); gizli[k]=!gizli[k];
        l.classList.toggle('off',!!gizli[k]); l.setAttribute('aria-pressed',gizli[k]?'false':'true');
        [].forEach.call(svg.querySelectorAll('.sr[data-k="'+k+'"], .an[data-k="'+k+'"], .dl[data-k="'+k+'"]'),function(yol){yol.style.display=gizli[k]?'none':'';});
        if(hp[k]) hp[k].style.display='none';
        olcekle(); etiketCiz(); if(!cizgiTip) ayir();
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
        if(d.tip==='genel'){
          var nk=d.noktalar[i];
          icerik='<span class="tt-b">'+kac(nk.b)+'</span>';
          nk.s.forEach(function(r){
            icerik+='<span class="tt-r">'+(r.r?'<i style="background:'+r.r+'"></i>':'<i></i>')+'<span>'+kac(r.a)+'</span><span class="tt-n">'+kac(r.v)+'</span></span>';
          });
          var rg=z.getBoundingClientRect();
          kx=rg.left+rg.width/2; ky=rg.top+4;
        } else if(d.tip==='bar'){
          var sat=d.satirlar[i];
          var dv=Number(sat.deger), mt=Math.abs(dv).toFixed(1), isr=dv>0?'+':(dv<0?'-':'');
          var yazi=ingilizce() ? isr+mt+'%' : isr+'%'+mt.replace('.',',');
          icerik='<span class="tt-b">'+kac(sat.ad)+'</span><span class="tt-r">'
               + '<i style="background:'+sat.renk+'"></i><span>'+kac(d.olcu || (ingilizce() ? 'YoY change' : 'YoY değişim'))+'</span>'
               + '<span class="tt-n">'+yazi+'</span></span>';
          var rz=z.getBoundingClientRect();
          kx=rz.left+rz.width/2; ky=rz.top;
        } else {
          var ayy=String(d.aylar[i]), mm=ayy.match(/^(\d{4})-(\d{2})$/);
          if(mm){var AT=['Oca','Şub','Mar','Nis','May','Haz','Tem','Ağu','Eyl','Eki','Kas','Ara'], AE=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']; ayy=(ingilizce()?AE:AT)[parseInt(mm[2],10)-1]+' '+mm[1];}
          icerik='<span class="tt-b">'+kac(ayy)+'</span>';
          var enUst=null;
          for(var k=0;k<d.seriler.length;k++){
            var se=d.seriler[k], v=se.deger[i];
            if(gizli[k] || v===null || v===undefined){ if(hp[k]) hp[k].style.display='none'; continue; }
            icerik+='<span class="tt-r"><i style="background:'+se.renk+'"></i>'
                  + '<span>'+kac(se.ad)+'</span><span class="tt-n">'+degerYaz(v)+'</span></span>';
            var pyi = pyO ? pyO[k][i] : se.py[i];
            if(pyi!==null && (enUst===null || pyi<enUst)) enUst=pyi;
            if(hp[k]){
              if(pyi===null){hp[k].style.display='none';}
              else{
                hp[k].setAttribute('cx',d.px[i]); hp[k].setAttribute('cy',pyi);
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
  links.concat(mobil, [].slice.call(document.querySelectorAll('a.git[href^="#"]'))).forEach(function(a){
    a.addEventListener('click',function(e){e.preventDefault();git(a.getAttribute('href').slice(1));});
  });

  /* mobil icindekiler sayfasi */
  document.addEventListener('click',function(e){var im=e.target.closest('.ekranlar img');if(im)im.closest('figure').classList.toggle('acik')});
  (function(){var b=document.getElementById('altmenu-b'),p=document.getElementById('altmenu-p');if(!b||!p)return;
   function kapa(){p.hidden=true;b.setAttribute('aria-expanded','false')}
   b.addEventListener('click',function(e){e.stopPropagation();var ac=p.hidden;p.hidden=!ac;b.setAttribute('aria-expanded',ac?'true':'false');if(ac){var f=p.querySelector('a');if(f)f.focus()}});
   document.addEventListener('click',function(e){if(!p.hidden&&!p.contains(e.target))kapa()});
   document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!p.hidden){kapa();b.focus()}});
   p.addEventListener('click',function(e){if(e.target.closest('a'))kapa()})})();
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

/* acilir pencereler */
(function(){
  [].forEach.call(document.querySelectorAll('.popb[data-pop]'),function(b){
    b.addEventListener('click',function(){var d=document.getElementById(b.getAttribute('data-pop')); if(d&&d.showModal){d.showModal();}});
  });
  [].forEach.call(document.querySelectorAll('dialog.popd'),function(d){
    var x=d.querySelector('.popx'); if(x) x.addEventListener('click',function(){d.close();});
    d.addEventListener('click',function(e){ if(e.target===d) d.close(); });
  });
})();
/* tablo suzgeci: .tfilt dugmeleri hemen ardindaki tablonun satirlarini data-f degerine gore suzer */
(function(){
  [].forEach.call(document.querySelectorAll('.tfilt'),function(f){
    var el=f.nextElementSibling, tbl=null;
    while(el && !tbl){ tbl = el.tagName==='TABLE' ? el : el.querySelector('table'); el=el.nextElementSibling; }
    if(!tbl) return;
    var bs=f.querySelectorAll('button');
    [].forEach.call(bs,function(b){ b.addEventListener('click',function(){
      var v=b.getAttribute('data-f');
      [].forEach.call(bs,function(o){o.setAttribute('aria-pressed',String(o===b));});
      [].forEach.call(tbl.tBodies[0].rows,function(r){ r.style.display=(!v || r.getAttribute('data-f')===v)?'':'none'; });
    }); });
  });
})();
/* grafik turu: cizgi / cubuk gecisi */
(function(){
  [].forEach.call(document.querySelectorAll('.gcift'),function(g){
    var bs=g.querySelectorAll('.gcift-b button'), ps=g.querySelectorAll('.gcift-p');
    [].forEach.call(bs,function(b){ b.addEventListener('click',function(){
      [].forEach.call(bs,function(o){o.setAttribute('aria-pressed',String(o===b));});
      [].forEach.call(ps,function(p){p.hidden=p.getAttribute('data-g')!==b.getAttribute('data-g');});
    }); });
  });
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
  function metin(td){var dv=td.querySelector&&td.querySelector('[data-v]'); if(dv && td.querySelectorAll('[data-v]').length===1 && td.innerText.trim()===dv.innerText.trim()) return dv.getAttribute('data-v'); return (td.innerText||td.textContent||'').replace(/\s+/g,' ').trim();}
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
  /* sutun ac/kapa: ilk sutun sabit, digerleri isaretle gorunur */
  var ICOL='<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2" y="2.5" width="12" height="11" rx="1.5"/><path d="M6 2.5v11M10 2.5v11"/></svg>';
  function sutunlar(tw){
    var tbl=tw.querySelector('table'); if(!tbl||!tbl.tHead||!tbl.tHead.rows.length) return null;
    var ths=[].slice.call(tbl.tHead.rows[0].cells); if(ths.length<3) return null;
    var wrap=document.createElement('div'); wrap.className='tcolw';
    var b=document.createElement('button'); b.type='button'; b.className='tcol'; b.setAttribute('aria-expanded','false'); b.setAttribute('aria-haspopup','true');
    var pnl=document.createElement('div'); pnl.className='tcol-p'; pnl.hidden=true; pnl.setAttribute('role','group');
    var gizli={};
    function uygula(i){ var on=!gizli[i]; [].forEach.call(tbl.rows,function(r){var c=r.cells[i]; if(c) c.style.display=on?'':'none';}); b.classList.toggle('kisik',Object.keys(gizli).some(function(k){return gizli[k];})); }
    function kur(){
      b.innerHTML=ICOL+'<span>'+(en()?'Columns':'Sütunlar')+'</span>'; b.title=en()?'Show or hide table columns':'Tablo sütunlarını göster veya gizle';
      pnl.innerHTML=''; pnl.setAttribute('aria-label',en()?'Visible columns':'Görünen sütunlar');
      ths.forEach(function(th,i){ if(i===0) return;
        var l=document.createElement('label'); var c=document.createElement('input'); c.type='checkbox'; c.checked=!gizli[i];
        c.addEventListener('change',function(){gizli[i]=!c.checked; uygula(i);});
        l.appendChild(c); var s=document.createElement('span'); s.textContent=(th.textContent||'').replace(/\s+/g,' ').trim(); l.appendChild(s); pnl.appendChild(l); });
      var hep=document.createElement('button'); hep.type='button'; hep.className='tcol-all'; hep.textContent=en()?'Show all':'Tümünü göster';
      hep.addEventListener('click',function(){ ths.forEach(function(th,i){ if(i){gizli[i]=false; uygula(i);} }); kur(); pnl.hidden=false; });
      pnl.appendChild(hep);
    }
    function kapat(){pnl.hidden=true; b.setAttribute('aria-expanded','false');}
    b.addEventListener('click',function(e){e.stopPropagation(); var ac=pnl.hidden; pnl.hidden=!ac; b.setAttribute('aria-expanded',String(ac));});
    document.addEventListener('click',function(e){ if(!wrap.contains(e.target)) kapat(); });
    document.addEventListener('keydown',function(e){ if(e.key==='Escape' && !pnl.hidden){kapat(); b.focus();} });
    kur(); document.addEventListener('dilchange',kur);
    wrap.appendChild(b); wrap.appendChild(pnl); return wrap;
  }
  var IK='<svg viewBox="0 0 16 16" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="5.5" y="5.5" width="8" height="8" rx="1.5"/><path d="M10.5 5.5V3.5a1 1 0 0 0-1-1h-6a1 1 0 0 0-1 1v6a1 1 0 0 0 1 1h2"/></svg>';
  [].forEach.call(document.querySelectorAll('.tw'),function(tw){
    var box=document.createElement('div'); box.className='tbox';
    var bar=document.createElement('div'); bar.className='tbar';
    var b=document.createElement('button'); b.type='button'; b.className='tcopy';
    function etiket(){b.innerHTML=IK+'<span>'+(en()?'Copy table':'Tabloyu kopyala')+'</span>'; b.title=en()?'Copy the table with its columns (paste into Excel or Sheets)':'Tabloyu sütunlarıyla kopyala (Excel veya Sheets\'e yapıştırılır)';}
    etiket(); document.addEventListener('dilchange',etiket);
    b.addEventListener('click',function(){
      var tbl=tw.querySelector('table'); if(!tbl)return;
      var satirlar=[].slice.call(tbl.rows).filter(function(r){return r.style.display!=='none';}).map(function(r){return [].slice.call(r.cells).filter(function(c){return c.style.display!=='none';}).map(function(c){return metin(c).replace(/\t/g,' ');});});
      var tsv=satirlar.map(function(r){return r.join('\t');}).join('\n');
      var html='<table>'+satirlar.map(function(r,i){var tag=i===0?'th':'td';return '<tr>'+r.map(function(c){return '<'+tag+'>'+c.replace(/&/g,'&amp;').replace(/</g,'&lt;')+'</'+tag+'>';}).join('')+'</tr>';}).join('')+'</table>';
      function ok(){b.classList.add('ok');b.querySelector('span').textContent=en()?'Copied':'Kopyalandı';setTimeout(function(){b.classList.remove('ok');etiket();},1600);}
      if(navigator.clipboard&&window.ClipboardItem){
        navigator.clipboard.write([new ClipboardItem({'text/plain':new Blob([tsv],{type:'text/plain'}),'text/html':new Blob([html],{type:'text/html'})})]).then(ok,function(){navigator.clipboard.writeText(tsv).then(ok);});
      }else if(navigator.clipboard){navigator.clipboard.writeText(tsv).then(ok);}
    });
    var kay=tw.previousElementSibling;
    if(kay && kay.classList.contains('tkay')) bar.appendChild(kay);
    var sc=sutunlar(tw); if(sc) bar.appendChild(sc);
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
