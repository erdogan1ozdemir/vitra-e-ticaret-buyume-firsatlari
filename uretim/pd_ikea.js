// IKEA TR (ikea.com.tr): kategori sayfalari urun listesi yerine tanitim icerigi (shoppable gorsel) verir; .product-bottom bloklarindan gorunen urunler okunur.
// Sayfalanan liste (#listeleme) bu yontemle acilmadi; sonuc yalnizca gorunen urunlerle sinirlidir.
function pn(s){return parseFloat((s||'').replace(/[^\d,\.]/g,'').replace(/\./g,'').replace(',','.'))}
function IK(key,p){var o={key:key,u:p,ts:'2026-09-30'};var x=new XMLHttpRequest();x.open('GET',p,false);x.send();o.st=x.status;var d=new DOMParser().parseFromString(x.responseText,'text/html');var seen={},rows=[];
[].slice.call(d.querySelectorAll('.product-bottom')).forEach(function(b){var a=b.querySelector('a[href*="/urun/"]');if(!a)return;var h=a.getAttribute('href');if(seen[h])return;seen[h]=1;var nm=(b.querySelector('h3')||{}).textContent||'';var nw=b.querySelector('.new'),od=b.querySelector('.old');var f=nw?pn(nw.textContent):null;var ol=od?pn(od.textContent):0;rows.push([nm.replace(/\s+/g,' ').trim().slice(0,60),f,ol||0].join('|'))});
o.n=rows.length;o.rows=rows.slice(0,12);return o}
