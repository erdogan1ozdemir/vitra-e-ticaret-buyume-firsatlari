// Bauhaus TR (2. tur): /search?q=<ifade>; ul.prodList li (.prodName, .subInfo marka, .priceBox fiyat, .starCount yorum). Siralama secenegi yok (alaka sirasi).
function nums(s){return (s.match(/\d[\d\.]*(?:,\d+)?/g)||[]).map(function(v){return parseFloat(v.replace(/\./g,'').replace(',','.'))})}
window.__job=async function(k,q){
  var r=await fetch('/search?q='+encodeURIComponent(q),{credentials:'include'});if(r.status==429)return{status:429};var t=await r.text();
  var d=new DOMParser().parseFromString(t,'text/html');var res={k:k,q:q,st:r.status,rt:((d.querySelector('.resultTxt')||{}).textContent||'').trim().slice(0,40)};
  res.rows=[].slice.call(d.querySelectorAll('ul.prodList li')).filter(function(l){return l.querySelector('.prodName')}).map(function(l,i){var ti=(l.querySelector('.prodName').textContent||'').trim();var br=((l.querySelector('.subInfo')||{}).textContent||'').trim();var pn=nums((l.querySelector('.priceBox')||{}).textContent||'');var st=l.querySelector('.stars.percentage');var w=st?parseFloat((st.getAttribute('style')||'').replace(/[^\d\.]/g,'')):0;var sc=((l.querySelector('.starCount')||{}).textContent||'').replace(/\D/g,'');
    return [i+1,br||'(markasız)',ti.slice(0,70),pn.length?Math.min.apply(null,pn):null,pn.length>1?Math.max.apply(null,pn):0,Math.round(w/20*10)/10,parseInt(sc||'0')]});
  return res};
