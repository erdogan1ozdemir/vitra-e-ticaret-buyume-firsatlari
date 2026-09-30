// Cimri kategori okuyucu (Control_Chrome execute_javascript; cimri.com sekmesinde, senkron XHR, sayfalar arasi 3.3 sn).
// Urun karti: [data-module=products] .dWBEz ; baslik a[title] ; "N fiyati incele" dugmesi = fiyat (satici) sayisi ; en dusuk fiyat .JUbmF .h1Anp ; magaza = ilk logo alt metni.
// Yan menu: span "Markalar" / "Mağaza" / "Fiyat Aralığı" basliklari (.AWIGL) ve kardes .WEP8F listesi.
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function num(s){var v=parseFloat((s||'').replace(/\./g,'').replace(',','.').replace(/[^\d\.]/g,''));return isNaN(v)?null:v}
function CM(slug){
  var out={kat:slug,ts:'2026-09-30'};var rows=[];var brands=[];
  for(var p=1;p<=2;p++){
    var x=new XMLHttpRequest();x.open('GET','/'+slug+(p>1?'?page='+p:''),false);x.send();if(p==1)out.st=x.status;if(x.status!=200)break;
    var d=new DOMParser().parseFromString(x.responseText,'text/html');
    if(p==1){out.h1=(d.querySelector('h1')||{}).textContent;var m=d.body.innerText.match(/([\d\.]+)\s*Ürün/);out.toplam=m?parseInt(m[1].replace(/\./g,'')):null;out.f={};
      [].slice.call(d.querySelectorAll('.AWIGL span')).forEach(function(h){var n=h.textContent.trim();var lst=h.parentElement.parentElement.querySelectorAll('.WEP8F a[title], .WEP8F [role=checkbox]');var vs=[].slice.call(lst).map(function(e){return (e.getAttribute('aria-label')||e.textContent).trim()}).filter(function(v,i,a){return v&&a.indexOf(v)==i});if(/^(Markalar|Mağaza|Fiyat Aralığı)$/.test(n))out.f[n]=vs.slice(0,15)});
      brands=(out.f['Markalar']||[])}
    [].slice.call(d.querySelectorAll('[data-module=products] .dWBEz')).forEach(function(c,i){var a=c.querySelector('a[title]');if(!a)return;var b=c.querySelector('button');var pr=c.querySelector('.JUbmF .h1Anp');var im=c.querySelector('.JUbmF img');var t=a.getAttribute('title');
      var br=brands.filter(function(z){return t.toLowerCase().indexOf(z.toLowerCase())===0})[0]||t.split(' ')[0];
      rows.push([(p-1)*32+i+1,(a.getAttribute('href').match(/,(\d+)$/)||[])[1],br,t.slice(0,50),num(pr&&pr.textContent),parseInt((b&&b.textContent)||'0',10)||0,im?im.alt:''])});
    if(p==1)sleep(3300);
  }
  out.r=rows.map(function(r){return r[2]+'|'+r[4]+'|'+r[5]+'|'+r[6]}).join(';');
  out.top=rows.slice().sort(function(a,b){return b[5]-a[5]}).slice(0,10).map(function(r){return r[0]+'|'+r[3]+'|'+r[2]+'|'+r[4]+'|'+r[5]});
  out.vitra=rows.filter(function(r){return /vitra|artema/i.test(r[2]+r[3])}).map(function(r){return r[0]+'|'+r[1]+'|'+r[3]+'|'+r[4]+'|'+r[5]+'|'+r[6]}).slice(0,10);
  return out;
}
