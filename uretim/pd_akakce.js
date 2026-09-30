// Akakce kategori okuyucu (Control_Chrome execute_javascript; akakce.com sekmesinde, senkron XHR, sayfalar arasi 3.2 sn)
// AK('klozet',1): /klozet.html ve /klozet,2.html okunur (CPL > li, 32 urun/sayfa; data-mk = marka, data-cp = fiyat/satici sayisi)
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function num(s){var m=(s||'').match(/([\d\.]+),(\d\d)/);return m?parseFloat(m[1].replace(/\./g,'')+'.'+m[2]):null}
function AK(slug,fac){
  var out={kat:slug,ts:'2026-09-30'};var rows=[];
  for(var p=1;p<=2;p++){
    var x=new XMLHttpRequest();x.open('GET','/'+slug+(p>1?','+p:'')+'.html',false);x.send();if(p==1)out.st=x.status;if(x.status!=200)break;
    var t=x.responseText,d=new DOMParser().parseFromString(t,'text/html');
    if(p==1){
      out.h1=(d.querySelector('h1')||{}).textContent.trim();
      var m=t.match(/numberOfItems"?[:\\&quot;]*(\d+)/);out.toplam=m?+m[1]:null;
      var mt=t.match(/Toplam <b>(\d+)<\/b> marka/);out.marka_sayisi=mt?+mt[1]:null;
      out.fiyat_filtre=[].slice.call(d.querySelectorAll('.fpl_v9 a[data-filter]')).map(function(a){return a.textContent.trim()});
      out.marka_filtre=[].slice.call(d.querySelectorAll('.mk_v8 a')).slice(0,15).map(function(a){return a.textContent.trim()});
      if(fac)out.alt=[].slice.call(d.querySelectorAll('#FF_v9 a[href]')).filter(function(a){return /^\/[a-z0-9\-]+\/[a-z0-9\-]+\.html$/.test(a.getAttribute('href'))&&!a.closest('.mk_v8')}).map(function(a){return a.textContent.trim()}).slice(0,14);
    }
    [].slice.call(d.querySelectorAll('#CPL > li')).forEach(function(li,i){var a=li.querySelector('a');var pt=li.querySelector('.pt_v9')||li.querySelector('.pt_v8');
      rows.push([(p-1)*32+i+1,li.getAttribute('data-pr'),li.getAttribute('data-mk')||'-',(a&&a.getAttribute('title')||'').slice(0,50),num(pt&&pt.textContent),parseInt(li.getAttribute('data-cp')||'0',10)])});
    if(p==1)sleep(3200);
  }
  out.r=rows.map(function(r){return r[2]+'|'+r[4]+'|'+r[5]}).join(';');
  out.top=rows.slice().sort(function(a,b){return b[5]-a[5]}).slice(0,10).map(function(r){return r[0]+'|'+r[1]+'|'+r[3]+'|'+r[4]+'|'+r[5]});
  out.vitra=rows.filter(function(r){return /vitra|artema/i.test(r[2]+r[3])}).map(function(r){return r[0]+'|'+r[1]+'|'+r[3]+'|'+r[4]+'|'+r[5]});
  return out;
}
