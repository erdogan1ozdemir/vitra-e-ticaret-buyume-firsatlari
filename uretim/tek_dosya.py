"""Teslim icin tek dosya: ana rapor + 6 veri seti sayfasi tek HTML'de.

Alt sayfalar gzip + base64 olarak ana raporun sonuna gomulur (script type="application/octet-stream" data-alt="...").
Raporda bir veri seti baglantisina tiklaninca sayfa acilir (DecompressionStream) ve raporun ustunde tam ekran gosterilir;
alt sayfadaki "Rapora don" ve diger veri seti baglantilari ayni katmanda calisir, tarayicinin geri tusu katmani kapatir.
Ana rapor (cok dosyali surum) ve Vercel surumu degismez. Cikti: teslim/VitrA_E-Ticaret_Buyume_Firsatlari.html
Kullanim: python3 tek_dosya.py   (rapor.py, excel.py ve alt sayfalar uretildikten sonra)
"""
import base64, gzip, os, re

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANA = "VitrA_E-Ticaret_Buyume_Firsatlari.html"
ALT = ["yorum-soru-seti.html", "arama-sonuclari.html", "kelime-evreni.html", "pazaryeri-taramasi.html", "youtube-videolari.html", "geo-promptlari.html"]
CIKTI = os.path.join(KOK, "teslim", ANA)

# alt sayfaya eklenen yonlendirici: sayfa ici .html baglantilari ve dil degisimi ana rapora iletilir
ALT_JS = r"""<script>(function(){
 function ilet(o){ try{ parent.postMessage(o,'*'); }catch(e){} }
 document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href]'); if(!a) return;
  var m=(a.getAttribute('href')||'').match(/^([a-z0-9_.-]+\.html)(#.*)?$/i); if(!m) return;
  e.preventDefault(); e.stopPropagation(); ilet({vitraGit:m[1], hash:m[2]||''});
 },true);
 document.addEventListener('click',function(e){ if(e.target.closest&&e.target.closest('#dil')) setTimeout(function(){ ilet({vitraDil:document.documentElement.lang}); },0); });
 window.addEventListener('message',function(e){ var d=e.data||{}; if(d.vitraHedef){ var el=document.getElementById(String(d.vitraHedef).replace(/^#/,'')); if(el) el.scrollIntoView(); } });
})();</script>"""

ANA_CSS = """<style>
#altkatman{position:fixed;inset:0;z-index:400;background:var(--bg,#fff)}
#altkatman[hidden]{display:none}
#altkatman iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:var(--bg,#fff)}
#altkatman .altkat-yuk{position:absolute;top:45%;left:0;right:0;text-align:center;color:var(--muted,#666);font-size:14px}
html.altkat-acik,html.altkat-acik body{overflow:hidden}
@media print{#altkatman{display:none!important}}
</style>"""

ANA_JS = r"""<script>(function(){
 var P={}; [].forEach.call(document.querySelectorAll('script[type="application/octet-stream"][data-alt]'),function(s){ P[s.getAttribute('data-alt')]=s; });
 if(!Object.keys(P).length) return;
 var kok=document.documentElement, kat=document.createElement('div'); kat.id='altkatman'; kat.hidden=true;
 kat.innerHTML='<div class="altkat-yuk" role="status"></div>'; document.body.appendChild(kat);
 /* her acilista yeni cerceve: cercevenin icerik degisimi tarayici gecmisine kayit eklemesin (geri tusu yalniz katmani yonetir) */
 var fr=null, yuk=kat.querySelector('.altkat-yuk'), onbellek={}, acik=null, kaydirma=0;
 function cerceveSil(){ if(fr){ fr.parentNode && fr.parentNode.removeChild(fr); fr=null; } }
 function en(){ return kok.getAttribute('data-dil')==='en'; }
 function coz(ad){
  if(onbellek[ad]) return Promise.resolve(onbellek[ad]);
  var b=atob(P[ad].textContent.trim()), u=new Uint8Array(b.length); for(var i=0;i<b.length;i++) u[i]=b.charCodeAt(i);
  return new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'))).text().then(function(t){ onbellek[ad]=t; return t; });
 }
 function ac(ad,hedef,gecmis){
  if(!window.DecompressionStream){ alert(en()?'This browser cannot open the embedded data sets; a current version of Chrome, Edge, Safari or Firefox can be used.':'Bu tarayıcı gömülü veri setlerini açamıyor; Chrome, Edge, Safari ya da Firefox\'un güncel sürümü kullanılabilir.'); return; }
  if(!acik) kaydirma=window.scrollY;
  yuk.textContent=en()?'Opening the data set…':'Veri seti açılıyor…'; kat.hidden=false; kok.classList.add('altkat-acik');
  try{ localStorage.setItem('vitra-dil', en()?'en':'tr'); localStorage.setItem('vitra-tema', kok.getAttribute('data-theme')||'light'); }catch(e){}
  coz(ad).then(function(html){
   acik=ad; cerceveSil();
   var f=document.createElement('iframe'); f.title=ad; f.srcdoc=html;
   f.onload=function(){ yuk.textContent=''; if(hedef) try{ f.contentWindow.postMessage({vitraHedef:hedef},'*'); }catch(e){} try{ f.focus(); }catch(e){} };
   kat.appendChild(f); fr=f;
  });
  if(gecmis!==false) try{ history.pushState({vitraAlt:ad,hedef:hedef||''},'','#veri-seti-'+ad.replace(/\.html$/,'')); }catch(e){}
 }
 function kapat(){ kat.hidden=true; kok.classList.remove('altkat-acik'); cerceveSil(); acik=null; window.scrollTo(0,kaydirma); }
 document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href]'); if(!a) return;
  var m=(a.getAttribute('href')||'').match(/^([a-z0-9-]+\.html)(#.*)?$/i); if(!m || !P[m[1]]) return;
  e.preventDefault(); e.stopPropagation(); ac(m[1], m[2]||'');
 },true);
 window.addEventListener('message',function(e){
  if(!fr || e.source!==fr.contentWindow) return; var d=e.data||{};
  if(d.vitraGit){ if(P[d.vitraGit]) ac(d.vitraGit, d.hash||''); else { try{ history.back(); }catch(x){ kapat(); } } }
  if(d.vitraDil && d.vitraDil!==(en()?'en':'tr')){ var b=document.getElementById('dil'); if(b) b.click(); }
 });
 window.addEventListener('popstate',function(e){
  var s=e.state||{};
  if(s.vitraAlt && P[s.vitraAlt]) ac(s.vitraAlt, s.hedef, false); else if(acik) kapat();
 });
 function adrestenAc(){   /* #veri-seti-<ad> adresiyle gelinirse ilgili veri seti acilir */
  var h=location.hash.match(/^#veri-seti-([a-z0-9-]+)$/i); if(!h || !P[h[1]+'.html'] || acik===h[1]+'.html') return;
  try{ history.replaceState({vitraAlt:h[1]+'.html'},'',location.hash); }catch(e){} ac(h[1]+'.html','',false);
 }
 window.addEventListener('hashchange',adrestenAc); adrestenAc();
})();</script>"""


def main():
    s = open(os.path.join(KOK, ANA), encoding="utf-8").read()
    if 'type="application/octet-stream" data-alt=' in s: raise SystemExit("Ana rapor zaten gömülü alt sayfa taşıyor.")
    paket, top = [], 0
    for ad in ALT:
        h = open(os.path.join(KOK, ad), encoding="utf-8").read()
        if "</body>" not in h: raise SystemExit("%s: </body> bulunamadı." % ad)
        h = h.replace("</body>", ALT_JS + "</body>", 1)
        z = gzip.compress(h.encode("utf-8"), 9, mtime=0); top += len(z)
        paket.append('<script type="application/octet-stream" data-alt="%s">%s</script>' % (ad, base64.b64encode(z).decode()))
    eksik = sorted(set(re.findall(r'href="([a-z0-9-]+\.html)(?:#[^"]*)?"', s)) - set(ALT) - {ANA})
    if eksik: raise SystemExit("Raporda gömülmeyen sayfa bağlantısı: %s" % eksik)
    s = s.replace("</head>", ANA_CSS + "</head>", 1).replace("</body>", "\n".join(paket) + ANA_JS + "</body>", 1)
    os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
    open(CIKTI, "w", encoding="utf-8").write(s)
    print("tek dosya: %s · %.1f MB (gömülü veri setleri %.1f MB sıkıştırılmış)" % (CIKTI, os.path.getsize(CIKTI) / 1e6, top / 1e6))


if __name__ == "__main__":
    main()
