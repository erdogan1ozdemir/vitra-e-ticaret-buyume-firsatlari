// Cimri (2. tur): /arama?q=<ifade> (uygun kategori sayfasina yonlenir); ilk sayfa (32 urun): baslik, en dusuk fiyat, "N fiyati incele" ile satici sayisi.
function num(s){var v=parseFloat((s||'').replace(/\./g,'').replace(',','.').replace(/[^\d\.]/g,''));return isNaN(v)?null:v}
window.__job=async function(k,q){
  var r=await fetch('/arama?q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();
  var d=new DOMParser().parseFromString(t,'text/html');var res={k:k,q:q,st:r.status,url:r.url.replace('https://www.cimri.com',''),h1:((d.querySelector('h1')||{}).textContent||'').trim()};
  var m=d.body.innerText.match(/([\d\.]+)\s*Ürün/);res.total=m?parseInt(m[1].replace(/\./g,'')):null;
  var brands=[];[].slice.call(d.querySelectorAll('.AWIGL span')).forEach(function(h){if(/^Markalar$/.test(h.textContent.trim())){var lst=h.parentElement.parentElement.querySelectorAll('.WEP8F a[title], .WEP8F [role=checkbox]');brands=[].slice.call(lst).map(function(e){return (e.getAttribute('aria-label')||e.textContent).trim()}).filter(function(v,i,a){return v&&a.indexOf(v)==i})}});res.marka_filtre=brands.slice(0,10);
  res.rows=[].slice.call(d.querySelectorAll('[data-module=products] .dWBEz')).map(function(c,i){var a=c.querySelector('a[title]');if(!a)return null;var b=c.querySelector('button');var pr=c.querySelector('.JUbmF .h1Anp');var im=c.querySelector('.JUbmF img');var ti=a.getAttribute('title');
    var br=brands.filter(function(z){return ti.toLowerCase().indexOf(z.toLowerCase())===0})[0]||ti.split(' ')[0];
    return [i+1,(a.getAttribute('href').match(/,(\d+)$/)||[])[1],br,ti.slice(0,70),num(pr&&pr.textContent),parseInt((b&&b.textContent)||'0',10)||0,im?im.alt:'']}).filter(function(x){return x});
  return res};
