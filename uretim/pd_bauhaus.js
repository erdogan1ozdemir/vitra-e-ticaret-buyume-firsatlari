// Bauhaus TR kategori okuyucu (Control_Chrome execute_javascript; bauhaus.com.tr sekmesinde, senkron XHR, kategoriler arasi 3.2 sn).
// Kart: ul.prodList li (a[title] + .prodName); marka .subInfo; fiyat .priceBox; puan .stars.percentage; yorum .starCount. Siralama yok, ilk sayfa 24 urun.
// Kullanim: BH('klozet-takimi','/bauhaus-banyo-klozet-ve-klozet-kapaklari-klozet-ve-takimlari')
function sleep(ms){var t=Date.now();while(Date.now()-t<ms){}}
function nums(s){return (s.match(/\d[\d\.]*(?:,\d+)?/g)||[]).map(function(v){return parseFloat(v.replace(/\./g,'').replace(',','.'))})}
function pct(a,p){a=a.slice().sort(function(x,y){return x-y});if(!a.length)return null;var i=(a.length-1)*p,l=Math.floor(i),h=Math.ceil(i);return Math.round((a[l]+(a[h]-a[l])*(i-l))*100)/100}
function BH(key,path){
  var out={key:key,u:path,ts:'2026-09-30'};var rows=[];
  var x=new XMLHttpRequest();x.open('GET',path,false);x.send();out.st=x.status;if(x.status!=200)return out;
  var d=new DOMParser().parseFromString(x.responseText,'text/html');
  out.h1=(d.querySelector('h1')||{}).textContent.trim();var rt=(d.querySelector('.resultTxt')||{}).textContent;out.toplam=rt?parseInt(rt.replace(/\D/g,'')):null;
  var fb=[].slice.call(d.querySelectorAll('[class*=filter] li,[class*=filter] label')).map(function(e){return e.textContent.replace(/\s+/g,' ').trim()}).filter(function(v,i,a){return v&&v.length<30&&a.indexOf(v)==i});out.filtre=fb.slice(8,26);
  var k=0;[].slice.call(d.querySelectorAll('ul.prodList li')).forEach(function(l){var a=l.querySelector('a[title]');if(!a||!l.querySelector('.prodName'))return;k++;var ti=(a.getAttribute('title')||'').trim();var br=((l.querySelector('.subInfo')||{}).textContent||'').trim();var pb=(l.querySelector('.priceBox')||{}).textContent||'';var pn=nums(pb);var st=l.querySelector('.stars.percentage');var w=st?parseFloat((st.getAttribute('style')||'').replace(/[^\d\.]/g,'')):0;var sc=((l.querySelector('.starCount')||{}).textContent||'').replace(/\D/g,'');var skn=l.querySelector('[data-sku]');var sku=skn&&skn.getAttribute('data-sku');
    rows.push({s:k,id:sku,b:br||'(markasız)',n:ti.slice(0,44),f:pn.length?Math.min.apply(null,pn):null,o:pn.length>1?Math.max.apply(null,pn):0,r:Math.round(w/20*10)/10,d:parseInt(sc||'0')})});
  out.n=rows.length;function fm(r){return [r.s,r.id,r.b,r.n,r.f,r.o,r.r,r.d].join('|')}
  var pr=rows.map(function(r){return r.f}).filter(function(v){return v!=null&&v>50});out.p={min:Math.min.apply(null,pr),p25:pct(pr,.25),med:pct(pr,.5),p75:pct(pr,.75),max:Math.max.apply(null,pr)};
  var bt={},dt=0,ind=0;rows.forEach(function(r){bt[r.b]=bt[r.b]||[0,0];bt[r.b][0]++;bt[r.b][1]+=r.d;dt+=r.d;if(r.o)ind++});out.deg=dt;out.indirimli=ind;
  out.marka=Object.keys(bt).sort(function(a,b){return bt[b][0]-bt[a][0]}).slice(0,8).map(function(k){return k+':'+bt[k][0]+'/'+bt[k][1]}).join(', ');
  out.top=rows.slice().sort(function(a,b){return b.d-a.d}).slice(0,2).map(fm);out.vitra=rows.filter(function(r){return /vitra|artema/i.test(r.b+r.n)}).map(fm).slice(0,10);
  return out;
}
