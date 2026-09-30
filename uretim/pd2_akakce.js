// Akakce (2. tur): /arama/?q=<ifade> (bazi ifadelerde kategori sayfasina yonlenir #CPL, digerlerinde arama sayfasi #APL); ilk sayfa (32 urun): marka, en dusuk fiyat, satici sayisi (data-cp).
function num(s){var m=(s||'').match(/([\d\.]+),(\d\d)/);return m?parseFloat(m[1].replace(/\./g,'')+'.'+m[2]):null}
window.__job=async function(k,q){
  var r=await fetch('/arama/?q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();
  var d=new DOMParser().parseFromString(t,'text/html');var res={k:k,q:q,st:r.status,url:r.url.replace('https://www.akakce.com',''),h1:((d.querySelector('h1')||{}).textContent||'').trim()};
  if(r.status!=200||!d.querySelector('#CPL,#APL')&&t.length<50000){if(/captcha|robot|doğrula/i.test(t.slice(0,4000)))return{status:r.status,blocked:1};}
  res.arama_sayfasi=!d.querySelector('#CPL')?1:0;
  var m=t.match(/numberOfItems"?[:\\&quot;]*(\d+)/);res.total=m?+m[1]:null;var mt=t.match(/Toplam <b>(\d+)<\/b> marka/);res.nbrand=mt?+mt[1]:null;
  res.marka_filtre=[].slice.call(d.querySelectorAll('.mk_v8 a')).slice(0,10).map(function(a){return a.textContent.trim()});
  res.alt=[].slice.call(d.querySelectorAll('#FF_v9 a[href]')).filter(function(a){return !a.closest('.mk_v8')}).map(function(a){return a.textContent.trim()}).slice(0,8);
  res.rows=[].slice.call(d.querySelectorAll('#CPL > li, #APL > li')).filter(function(li){return li.getAttribute('data-pr')}).map(function(li,i){var a=li.querySelector('a');var pt=li.querySelector('.pt_v9')||li.querySelector('.pt_v8');return [i+1,li.getAttribute('data-pr'),li.getAttribute('data-mk')||'-',(a&&a.getAttribute('title')||'').slice(0,70),num(pt&&pt.textContent),parseInt(li.getAttribute('data-cp')||'0',10)]});
  return res};
