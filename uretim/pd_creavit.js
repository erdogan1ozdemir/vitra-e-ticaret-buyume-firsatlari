// Creavit e-magaza (shop.creavit.com.tr, Shopify): koleksiyon products.json (limit=250) ile tam liste, fiyat dagilimi ve urun tipi dagilimi.
// Kullanim (shop.creavit.com.tr sekmesinde): SH('lavabo','lavabolar')
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function pct(a,p){a=a.slice().sort(function(x,y){return x-y});if(!a.length)return null;var i=(a.length-1)*p,l=Math.floor(i),h=Math.ceil(i);return Math.round((a[l]+(a[h]-a[l])*(i-l))*100)/100}
function SH(key,h){var x=new XMLHttpRequest();x.open('GET','/collections/'+h+'/products.json?limit=250',false);x.send();var o={key:key,u:'/collections/'+h,ts:'2026-09-30',st:x.status};if(x.status!=200)return o;var p=JSON.parse(x.responseText).products;o.toplam=p.length;
var pr=p.map(function(q){return parseFloat(q.variants[0].price)}).filter(function(v){return v>0});o.p={min:Math.min.apply(null,pr),p25:pct(pr,.25),med:pct(pr,.5),p75:pct(pr,.75),max:Math.max.apply(null,pr)};
var t={};p.forEach(function(q){t[q.product_type||'-']=(t[q.product_type||'-']||0)+1});o.tur=Object.keys(t).sort(function(a,b){return t[b]-t[a]}).slice(0,6).map(function(k){return k+':'+t[k]}).join(', ');
o.indirimli=p.filter(function(q){var c=parseFloat(q.variants[0].compare_at_price);return c>parseFloat(q.variants[0].price)}).length;
o.top=p.slice(0,3).map(function(q,i){return [i+1,q.title.slice(0,45),q.variants[0].price,q.variants[0].compare_at_price||0].join('|')});return o}
