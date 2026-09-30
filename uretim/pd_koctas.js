// Kocatas kategori okuyucu (Control_Chrome execute_javascript; koctas.com.tr sekmesinde, senkron XHR, sayfalar arasi 3.2 sn).
// Liste: li.prd; marka/satici/fiyat = li icindeki gizli input'lar (productBrandForGTM, productSellerForGTM, productUnitPriceForGTM, productPriceWithDiscountForGTM);
// puan .prd-rating ("4.7(12)"). Siralama ?sort=bestseller-desc (Cok Satanlar). Yan menu .fbox (Marka, Satici, Kategori). Toplam "N Urun" metni.
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function pct(a,p){a=a.slice().sort(function(x,y){return x-y});if(!a.length)return null;var i=(a.length-1)*p,l=Math.floor(i),h=Math.ceil(i);return Math.round((a[l]+(a[h]-a[l])*(i-l))*100)/100}
function KT(key,path){
  var out={key:key,u:path+'?sort=bestseller-desc',ts:'2026-09-30'};var rows=[];
  var x=new XMLHttpRequest();x.open('GET',path+'?sort=bestseller-desc',false);x.send();out.st=x.status;if(x.status!=200)return out;
  var d=new DOMParser().parseFromString(x.responseText,'text/html');
  out.h1=(d.querySelector('h1')||{}).textContent.trim();var m=d.body.textContent.match(/(\d[\d\.]*)\s*Ürün/);out.toplam=m?parseInt(m[1].replace(/\./g,'')):null;out.f={};
  [].slice.call(d.querySelectorAll('.fbox')).forEach(function(b){var h=(b.querySelector('h3,h4,.fbox-title,.title,strong')||b.firstElementChild);var n=(h?h.textContent:'').trim().split('\n')[0].trim();if(!/^(Marka|Satıcı|Kategori)$/.test(n))return;var ls=[].slice.call(b.querySelectorAll('li')).filter(function(l){return !l.querySelector('li')});out.f[n]=ls.map(function(l){return l.textContent.replace(/\s+/g,' ').trim()}).filter(function(v){return v}).slice(0,n=='Kategori'?12:10)});
  var pf=[].slice.call(d.querySelectorAll('.fbox')).filter(function(b){return /Fiyat/.test(b.textContent.slice(0,40))})[0];if(pf){var ins=[].slice.call(pf.querySelectorAll('input')).map(function(i){return (i.name||i.id)+'='+(i.placeholder||i.value||i.getAttribute('data-min')||i.getAttribute('data-max')||'')});out.fiyat_inputs=ins.slice(0,4)}
  [].slice.call(d.querySelectorAll('li.prd')).forEach(function(l,i){var g=function(n){var e=l.querySelector('input[name="'+n+'"]');return e?e.value:''};var a=l.querySelector('a[href*="/p/"][title]');var ti=(a?a.getAttribute('title'):g('productNameForGTM'))||'';var cur=parseFloat(g('productPriceWithDiscountForGTM'))||parseFloat(g('productUnitPriceForGTM'))||null;var uni=parseFloat(g('productUnitPriceForGTM'))||0;var rt=(l.querySelector('.prd-rating')||{}).textContent||'';var rm=rt.replace(/\s+/g,'').match(/([\d\.]+)\((\d+)\)/);
    rows.push({s:i+1,id:g('productUniqueCode'),b:g('productBrandForGTM'),n:ti.slice(0,44),m:g('productSellerForGTM'),f:cur,o:(uni>cur?uni:0),r:rm?parseFloat(rm[1]):0,d:rm?parseInt(rm[2]):0,c:g('productCategoryForGTM')})});
  out.n=rows.length;function fm(r){return [r.s,r.id,r.b,r.n,r.m,r.f,r.o,r.r,r.d].join('|')}
  var pr=rows.map(function(r){return r.f}).filter(function(v){return v!=null});out.p={min:Math.min.apply(null,pr),p25:pct(pr,.25),med:pct(pr,.5),p75:pct(pr,.75),max:Math.max.apply(null,pr)};
  var bt={},st={},dt=0,ind=0;rows.forEach(function(r){bt[r.b]=bt[r.b]||[0,0];bt[r.b][0]++;bt[r.b][1]+=r.d;dt+=r.d;st[r.m]=(st[r.m]||0)+1;if(r.o)ind++});out.deg=dt;out.indirimli=ind;
  out.marka=Object.keys(bt).sort(function(a,b){return bt[b][0]-bt[a][0]}).slice(0,8).map(function(k){return k+':'+bt[k][0]+'/'+bt[k][1]}).join(', ');out.sat=Object.keys(st).sort(function(a,b){return st[b]-st[a]}).slice(0,6).map(function(k){return k+':'+st[k]}).join(', ');
  out.top=rows.slice().sort(function(a,b){return b.d-a.d}).slice(0,4).map(fm);out.vitra=rows.filter(function(r){return /vitra|artema/i.test(r.b)}).map(fm);
  return out;
}
