(function(){
var d=document,b=d.body,root=d.documentElement;
function $(s){return d.querySelector(s)}
function $$(s){return [].slice.call(d.querySelectorAll(s))}
function lsGet(k){try{return localStorage.getItem(k)}catch(e){return null}}
function lsSet(k,v){try{v?localStorage.setItem(k,v):localStorage.removeItem(k)}catch(e){}}
function ssGet(k){try{return sessionStorage.getItem(k)}catch(e){return null}}
function ssSet(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}
if(location.protocol==="file:")$$('a[href$="/"]').forEach(function(a){a.setAttribute("href",a.getAttribute("href")+"index.html")});
/* side menu */
var mq=matchMedia("(min-width:1024px)"),mn=$("#menu"),cl=$("#close"),ov=$("#ov");
function isOpen(){return mq.matches?root.dataset.sb!=="off":b.classList.contains("open")}
function setNav(o){
 if(mq.matches){if(o)root.removeAttribute("data-sb");else root.dataset.sb="off";lsSet("sb",o?"":"off")}
 else b.classList.toggle("open",o);
 if(mn)mn.setAttribute("aria-expanded",o?"true":"false");
}
if(mn)mn.onclick=function(){setNav(!isOpen())};
if(cl)cl.onclick=function(){setNav(false)};
if(ov)ov.onclick=function(){setNav(false)};
d.addEventListener("keydown",function(e){if(e.key==="Escape"&&!mq.matches)setNav(false)});
addEventListener("resize",function(){if(mq.matches)b.classList.remove("open");if(mn)mn.setAttribute("aria-expanded",isOpen()?"true":"false")});
if(mn)mn.setAttribute("aria-expanded",isOpen()?"true":"false");
/* back button: يرجع للصفحة السابقة، ولو ما في صفحة سابقة من الموقع يروح للرئيسية */
var bk=$("#back");
if(bk)bk.addEventListener("click",function(e){
 var ref=d.referrer,external=false;
 try{external=ref&&new URL(ref).origin!==location.origin&&location.protocol!=="file:"}catch(x){}
 if(history.length>1&&!external){e.preventDefault();history.back()}
});
/* auto close status */
var now=new Date();
$$(".badge[data-close]").forEach(function(x){var c=x.dataset.close;
 if(c&&x.dataset.status==="open"&&new Date(c+"T23:59:59")<now){x.dataset.status="closed";x.className="badge closed";x.textContent="مغلق"}});
/* search + filters */
var q=$("#q"),cards=$$(".card,.org,.ptile"),cat="",only=false,gate=!!$("[data-gate]");
function run(){
 if(!q)return;var t=q.value.trim(),c=0;
 cards.forEach(function(el){var bd=el.querySelector(".badge"),st=bd?bd.dataset.status:"";
  var tx=!t||el.dataset.text.indexOf(t)>-1,ok=el.classList.contains("org")?tx:((!cat||el.dataset.cat===cat)&&(!only||st==="open")&&tx);if(gate&&!cat&&!el.classList.contains("org"))ok=false;el.hidden=!ok;if(ok)c++});
 var m=$("#none");if(m)m.hidden=c>0||(gate&&!cat);var gm=$("#gatemsg");if(gm)gm.hidden=!(gate&&!cat);
}
if(q){q.addEventListener("input",function(){run();var g=$("#gsl");if(g)g.href=g.getAttribute("href").split("?")[0]+(q.value.trim()?"?q="+encodeURIComponent(q.value.trim()):"")});
 $$(".chip[data-cat]").forEach(function(c){c.addEventListener("click",function(){cat=c.dataset.cat;$$(".chip[data-cat]").forEach(function(x){x.classList.toggle("on",x===c)});run()})});
 var oc=$(".open-only");if(oc)oc.addEventListener("click",function(){only=!only;oc.setAttribute("aria-pressed",only);run()});}
if(gate)run();
/* remember scroll + filters */
var key="st:"+location.pathname;
function save(){ssSet(key,JSON.stringify({y:window.scrollY,q:q?q.value:"",cat:cat,only:only}))}
var tm;addEventListener("scroll",function(){clearTimeout(tm);tm=setTimeout(save,150)},{passive:true});
addEventListener("pagehide",save);
if("scrollRestoration"in history)history.scrollRestoration="manual";
var nav=performance.getEntriesByType&&performance.getEntriesByType("navigation")[0];
function restore(){
 var s;try{s=JSON.parse(ssGet(key))}catch(e){}
 if(!s)return;
 if(q){q.value=s.q||"";cat=s.cat||"";only=!!s.only;
  $$(".chip[data-cat]").forEach(function(x){x.classList.toggle("on",x.dataset.cat===cat)});
  var oc=$(".open-only");if(oc)oc.setAttribute("aria-pressed",only);run()}
 requestAnimationFrame(function(){window.scrollTo(0,s.y||0)});
}
if(nav&&nav.type==="back_forward")restore();
addEventListener("pageshow",function(e){if(e.persisted)restore()});
/* مشاركة ونسخ الرابط */
if(location.protocol!=="file:"){var u=location.origin+location.pathname,tt=encodeURIComponent(d.title.split(" | ")[0]);
 $$("[data-share]").forEach(function(a){a.href=a.dataset.share==="wa"?"https://wa.me/?text="+tt+"%20"+encodeURIComponent(u):"https://t.me/share/url?url="+encodeURIComponent(u)+"&text="+tt})}
$$("[data-copy]").forEach(function(b){b.addEventListener("click",function(){
 var s=b.querySelector("span"),old=s.textContent,l=location.href;
 function ok(){s.textContent="تم النسخ ✓";setTimeout(function(){s.textContent=old},1800)}
 function fb(){var t=d.createElement("textarea");t.value=l;b.appendChild(t);t.select();try{d.execCommand("copy");ok()}catch(x){}b.removeChild(t)}
 if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(l).then(ok,fb);else fb();
})});
/* settings */
function mark(a,v){$$("[data-"+a+"]").forEach(function(x){x.setAttribute("aria-pressed",(x.dataset[a]||"")===(v||""))})}
mark("theme",lsGet("theme"));mark("fs",lsGet("fs"));
$$("[data-theme]").forEach(function(x){x.addEventListener("click",function(){var v=x.dataset.theme;lsSet("theme",v);v?root.dataset.theme=v:root.removeAttribute("data-theme");mark("theme",v)})});
$$("[data-fs]").forEach(function(x){x.addEventListener("click",function(){var v=x.dataset.fs;lsSet("fs",v);v?root.dataset.fs=v:root.removeAttribute("data-fs");mark("fs",v)})});
})();
