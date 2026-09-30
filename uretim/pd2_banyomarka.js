// Banyomarka (2. tur): /arama?q=<ifade>; .productItem (32 urun), marka img alt onekinden ("Marka - Urun"), fiyat .currentPrice.
function pn(s){return parseFloat((s||'').replace(/[^\d,\.]/g,'').replace(/\./g,'').replace(',','.'))}
window.__job=async function(k,q){
  var r=await fetch('/arama?q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();var d=new DOMParser().parseFromString(t,'text/html');
  var m=t.match(/Toplam (\d+) ürün/);var res={k:k,q:q,st:r.status,total:m?parseInt(m[1]):null};
  res.rows=[].slice.call(d.querySelectorAll('.productItem')).map(function(e,i){var nm=((e.querySelector('[itemprop=name]')||{}).getAttribute('content'))||'';var alt=((e.querySelector('img')||{}).getAttribute('alt'))||'';var br=alt.indexOf(' - ')>0?alt.split(' - ')[0]:'?';var cp=pn((e.querySelector('.currentPrice')||{}).textContent);var op=pn((e.querySelector('.oldPrice')||{}).textContent);return [i+1,br,nm.slice(0,70),cp,op>cp?op:0]});
  return res};
