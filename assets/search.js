/* البحث المتقدم: عربي + إنجليزي، يطبّع الحروف، يتسامح مع الأخطاء، ويفهم المرادفات */
(function(){
"use strict";
var d=document,root=d.body.getAttribute("data-root")||"",file=location.protocol==="file:";
function $(s){return d.querySelector(s)}
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function nz(s){return String(s==null?"":s).replace(/[\u0660-\u0669]/g,function(c){return String(c.charCodeAt(0)-1632)}).replace(/[\u06F0-\u06F9]/g,function(c){return String(c.charCodeAt(0)-1776)}).replace(/[أإآٱ]/g,"ا").replace(/ى/g,"ي").replace(/ة/g,"ه").replace(/ؤ/g,"و").replace(/ئ/g,"ي").toLowerCase().replace(/[\u064B-\u065F\u0670\u0640]/g,"")}
function words(s){return nz(s).split(/[^a-z0-9\u0621-\u064A]+/).filter(Boolean)}
function stem(w){
 var p=w;
 if(p.length>4&&/^(وال|بال|كال|فال)/.test(p))p=p.slice(3);
 else if(p.length>3&&p.indexOf("لل")===0)p=p.slice(2);
 else if(p.length>3&&p.indexOf("ال")===0)p=p.slice(2);
 if(p.length>4&&/(ات|ون|ين)$/.test(p))p=p.slice(0,-2);
 if(p.length>3&&p.charAt(p.length-1)==="ه")p=p.slice(0,-1);
 return p}
function toks(s){return words(s).map(stem)}
function lev(a,b){var m=a.length,n=b.length,i,j,p=[],c;for(j=0;j<=n;j++)p[j]=j;
 for(i=1;i<=m;i++){var t=p[0];p[0]=i;for(j=1;j<=n;j++){c=p[j];p[j]=Math.min(p[j]+1,p[j-1]+1,t+(a.charAt(i-1)===b.charAt(j-1)?0:1));t=c}}return p[n]}
function mt(ws,q,fz){var b=0,n=q.length;
 for(var i=0;i<ws.length;i++){var w=ws[i];
  if(w===q)return 1;
  if(n>=2&&w.indexOf(q)===0){if(b<.9)b=.9}
  else if(n>=3&&w.indexOf(q)>-1){if(b<.6)b=.6}
  else if(fz&&n>=4&&Math.abs(w.length-n)<=2&&b<.5&&lev(w,q)<=(n>=8?2:1))b=.5}
 return b}
var DATA,META,SYN,ST={open:"مفتوح",soon:"قريباً",closed:"مغلق"},ready=false,today=new Date().toISOString().slice(0,10);
function init(){
 if(ready)return;ready=true;DATA=window.SEARCH_DATA||[];META=window.SEARCH_META||{};
 SYN=(window.SEARCH_SYN||[]).map(function(g){return g.map(function(t){return toks(t)})});
 DATA.forEach(function(x){
  x._t=toks(x.t);x._o=toks(x.o);x._a=toks(x.a);x._m=toks((META[x.k]?META[x.k].t:"")+" "+(x.c||""));
  x._l=toks((x.l||"").replace(/https?:\/\//g," "));x._sm=toks(x.sm);x._tn=nz(x.t);x._bn=nz(x.b);
  x._bs={};toks(x.b).forEach(function(w){x._bs[w]=1});x._id=String(x.id||"");
  x._st=(x.st==="open"&&x.cd&&x.cd<today)?"closed":x.st;
 })}
function expand(qs){
 return qs.map(function(q){var alts=[{q:q,w:1}],seen={};seen[q]=1;
  SYN.forEach(function(g){var hit=g.some(function(t){return t.some(function(w){return w===q||(q.length>=3&&w.length>=3&&(w.indexOf(q)===0||q.indexOf(w)===0))})});
   if(hit)g.forEach(function(t){t.forEach(function(w){if(!seen[w]){seen[w]=1;alts.push({q:w,w:.55})}})})});
  return alts})}
function scoreDoc(x,qs,alts,nq){
 var tot=0,hit=0;
 for(var i=0;i<qs.length;i++){var best=0;
  for(var j=0;j<alts[i].length;j++){var al=alts[i][j],q=al.q,s=Math.max(10*mt(x._t,q,1),8*mt(x._o,q,1),7*mt(x._a,q,1),4*mt(x._m,q,0),2*mt(x._l,q,0),3*mt(x._sm,q,0));
   if(!s){if(x._bs[q])s=1;else if(q.length>=3&&x._bn.indexOf(q)>-1)s=.5}
   if(/^\d+$/.test(q)&&x._id===q)s=Math.max(s,14);
   s*=al.w;if(s>best)best=s}
  if(best>0)hit++;tot+=best}
 if(!hit)return null;
 var full=hit===qs.length,sc=full?tot:tot*.35;
 if(nq.length>=3&&x._tn.indexOf(nq)>-1)sc+=20;
 if(x._st==="open")sc+=1;if(x._st==="closed")sc-=2;if(x.k==="orgs")sc+=1;
 return {x:x,s:sc,full:full}}
function search(raw,f,onlyOpen){
 init();var nq=nz(raw).replace(/\s+/g," ").trim(),qs=toks(raw).filter(function(w){return w.length>0});
 var sw={"في":1,"من":1,"علي":1,"الي":1,"عن":1,"لدي":1,"مع":1,"و":1,"او":1,"هل":1,"ما":1,"the":1,"a":1,"an":1,"in":1,"of":1,"to":1,"for":1,"and":1,"on":1,"at":1},q2=qs.filter(function(w){return !sw[w]});if(q2.length)qs=q2;
 if(!qs.length)return {list:[],qs:[],hs:[],partial:false};
 var alts=expand(qs),res=[];
 DATA.forEach(function(x){
  if(f&&x.k!==f)return;if(onlyOpen&&x._st!=="open")return;
  var r=scoreDoc(x,qs,alts,nq);if(r)res.push(r)});
 var anyFull=res.some(function(r){return r.full});
 if(anyFull)res=res.filter(function(r){return r.full});
 res.sort(function(a,b){return b.s-a.s||(b.x.d||"").localeCompare(a.x.d||"")});
 var hs=[];alts.forEach(function(a){a.forEach(function(o){if(o.w===1&&hs.indexOf(o.q)<0)hs.push(o.q)})});
 return {list:res.map(function(r){return r.x}),qs:qs,hs:hs,partial:!anyFull&&res.length>0}}
function hl(t,hs){
 var n=nz(t),r=[];
 hs.forEach(function(h){if(h.length<2)return;var p=0;while((p=n.indexOf(h,p))>-1){r.push([p,p+h.length]);p+=h.length}});
 if(!r.length||n.length!==String(t).length)return esc(t);
 r.sort(function(a,b){return a[0]-b[0]});
 var out="",pos=0;
 r.forEach(function(m){if(m[1]<=pos)return;var s=Math.max(m[0],pos);out+=esc(t.slice(pos,s))+"<mark>"+esc(t.slice(s,m[1]))+"</mark>";pos=m[1]});
 return out+esc(t.slice(pos))}
function snippet(x,hs){
 var b=x.b||x.sm||"";if(!b)return "";var nb=nz(b),pos=-1;
 hs.forEach(function(h){var p=nb.indexOf(h);if(p>-1&&(pos<0||p<pos))pos=p});
 var st=pos<0?0:Math.max(0,pos-55);
 return (st>0?"… ":"")+b.substr(st,170)+(st+170<b.length?" …":"")}
function href(u){return root+u+(file&&/\/$/.test(u)?"index.html":"")}
function row(x,hs){
 var m=META[x.k]||META.page||{t:"",i:"",c:""},st=x._st?'<span class="badge '+x._st+'">'+ST[x._st]+"</span>":"",sn=snippet(x,hs);
 return '<a class="card res '+m.c+'" href="'+href(x.u)+'"><h3><span class="mini">'+m.i+"</span>"+hl(x.t,hs)+"</h3>"+(sn?"<p>"+hl(sn,hs)+"</p>":"")+
 '<div class="meta">'+st+(x.o&&x.k!=="orgs"?"<span>"+esc(x.o)+"</span>":"")+"<span>"+esc(m.t)+"</span>"+(x.id?"<span>رقم "+x.id+"</span>":"")+"</div></a>"}
/* فحص الروابط */
function isUrl(s){return /^(https?:\/\/)?(www\.)?[a-z0-9-]+(\.[a-z0-9-]+)+(\/\S*)?$/i.test(s.trim())}
function normUrl(s){return s.trim().toLowerCase().replace(/^https?:\/\//,"").replace(/^www\./,"").replace(/[?#].*$/,"").replace(/\/+$/,"")}
function checkUrl(s){
 init();var u=normUrl(s),host=u.split("/")[0],exact=[],same=[];
 DATA.forEach(function(x){(x.l||"").split(" ").forEach(function(l){if(!l)return;var n=normUrl(l);if(n===u)exact.push(x);else if(n.split("/")[0]===host)same.push(x)})});
 return {exact:exact,same:same}}
/* الواجهة */
function lsGet(k){try{return JSON.parse(localStorage.getItem(k)||"[]")}catch(e){return []}}
function lsSet(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function load(cb){
 if(window.SEARCH_DATA){init();cb();return}
 var s=d.createElement("script");s.src=root+"assets/search-data.js";s.onload=function(){init();cb()};d.head.appendChild(s)}
function remember(q){q=q.trim();if(q.length<2)return;var a=lsGet("rs").filter(function(x){return x!==q});a.unshift(q);lsSet("rs",a.slice(0,6))}
window.GSearch={search:search,checkUrl:checkUrl,nz:nz,stem:stem};
var gq=$("#gq");if(!gq)return;
var mode=gq.getAttribute("data-gs"),tm;
if(mode==="drop"){
 var box=$("#gdrop");
 function close(){box.hidden=true}
 function go(){var q=gq.value.trim();if(q){remember(q);location.href=root+"search/"+(file?"index.html":"")+"?q="+encodeURIComponent(q)}}
 function upd(){var q=gq.value.trim();if(!q){close();return}
  load(function(){var r=search(q,"",false),h="";
   r.list.slice(0,6).forEach(function(x){var m=META[x.k]||META.page;h+='<a class="'+m.c+'" href="'+href(x.u)+'"><span class="mini">'+m.i+'</span><span><b>'+hl(x.t,r.hs)+'</b><small>'+esc(m.t)+(x.o&&x.k!=="orgs"?" · "+esc(x.o):"")+"</small></span></a>"});
   if(!r.list.length)h='<p class="sempty">لا توجد نتائج مطابقة. اضغط Enter للبحث الموسّع.</p>';
   h+='<a class="all" href="'+root+"search/"+(file?"index.html":"")+"?q="+encodeURIComponent(q)+'">عرض كل النتائج ('+r.list.length+")</a>";
   box.innerHTML=h;box.hidden=false})}
 gq.addEventListener("input",function(){clearTimeout(tm);tm=setTimeout(upd,120)});
 gq.addEventListener("focus",function(){load(function(){});if(gq.value.trim())upd()});
 gq.addEventListener("keydown",function(e){if(e.key==="Enter"){e.preventDefault();go()}if(e.key==="Escape")close()});
 d.addEventListener("click",function(e){if(!box.contains(e.target)&&e.target!==gq)close()});
}else{
 var res=$("#gres"),cnt=$("#gcount"),note=$("#gnote"),f="",onlyOpen=false,openBtn=$("#gopen");
 var params=new URLSearchParams(location.search);
 gq.value=params.get("q")||"";f=params.get("f")||"";onlyOpen=params.get("open")==="1";
 function sync(){
  document.querySelectorAll("[data-f]").forEach(function(c){c.classList.toggle("on",(c.dataset.f||"")===f)});
  if(openBtn)openBtn.setAttribute("aria-pressed",onlyOpen)}
 function empty(){
  var a=lsGet("rs"),h="";
  if(a.length)h+='<h2 class="h">عمليات بحث سابقة</h2><div class="chips">'+a.map(function(q){return '<button class="chip" data-q="'+esc(q)+'">'+esc(q)+"</button>"}).join("")+"</div>";
  var pop=window.SEARCH_POP||[];
  if(pop.length)h+='<h2 class="h">الأكثر بحثاً</h2><div class="chips">'+pop.map(function(q){return '<button class="chip" data-q="'+esc(q)+'">'+esc(q)+"</button>"}).join("")+"</div>";
  res.innerHTML=h;cnt.textContent="";note.innerHTML=""}
 function render(){
  var q=gq.value.trim();sync();
  var u=new URLSearchParams();if(q)u.set("q",q);if(f)u.set("f",f);if(onlyOpen)u.set("open","1");
  try{history.replaceState(null,"",location.pathname+(u.toString()?"?"+u.toString():""))}catch(e){}
  if(!q){empty();return}
  var t0=performance.now(),r=search(q,f,onlyOpen),h="",nh="";
  if(isUrl(q)){var c=checkUrl(q);
   if(c.exact.length)nh='<div class="note okn"><span>هذا الرابط مدرج في الموقع. ومع ذلك تأكد أن اسم الموقع بالمتصفح مطابق لما هو مكتوب هنا قبل إدخال بياناتك.</span></div>';
   else if(c.same.length)nh='<div class="note"><span>الموقع مدرج عندنا لكن بصفحة أخرى. تأكد أنك على الرابط الصحيح من صفحة المؤسسة.</span></div>';
   else nh='<div class="note"><span>هذا الرابط غير مدرج في قوائمنا. هذا لا يعني أنه مزيف، لكن تحقق منه من الصفحة الرسمية للمؤسسة قبل إدخال بياناتك. <a href="'+href("warning/")+'">كيف تتحقق</a></span></div>';
   var ex=c.exact.concat(c.same);if(ex.length){r={list:ex,hs:[],qs:[],partial:false}}}
  note.innerHTML=nh;
  if(!r.list.length){
   var secs=Object.keys(META).filter(function(k){return META[k].u}).map(function(k){return '<a class="chip" href="'+href(META[k].u)+'">'+esc(META[k].t)+"</a>"}).join("");
   res.innerHTML='<div class="empty"><p>لا توجد نتائج لـ «'+esc(q)+'».</p><p>جرّب كلمة أقصر، أو اسم المؤسسة بالإنجليزي، أو أزل الفلاتر. أو تصفح الأقسام:</p><div class="chips">'+secs+"</div></div>";
   cnt.textContent="";return}
  r.list.slice(0,60).forEach(function(x){h+=row(x,r.hs)});
  res.innerHTML=h;
  cnt.textContent=(r.partial?"نتائج قريبة: ":"")+r.list.length+" نتيجة"+(r.list.length>60?" (عرض أول 60)":"")+" · "+Math.max(1,Math.round(performance.now()-t0))+" ملّي ثانية"}
 gq.addEventListener("input",function(){clearTimeout(tm);tm=setTimeout(render,120)});
 gq.addEventListener("keydown",function(e){if(e.key==="Enter")remember(gq.value)});
 document.querySelectorAll("[data-f]").forEach(function(c){c.addEventListener("click",function(){f=c.dataset.f||"";render()})});
 if(openBtn)openBtn.addEventListener("click",function(){onlyOpen=!onlyOpen;render()});
 res.addEventListener("click",function(e){var b=e.target.closest("[data-q]");if(b){gq.value=b.dataset.q;render();return}if(e.target.closest("a.res"))remember(gq.value)});
 load(function(){render();
  var nav=performance.getEntriesByType&&performance.getEntriesByType("navigation")[0];
  if(nav&&nav.type==="back_forward"){try{var s=JSON.parse(sessionStorage.getItem("st:"+location.pathname));if(s&&s.y)requestAnimationFrame(function(){window.scrollTo(0,s.y)})}catch(e){}}
  else if(!gq.value)gq.focus()})}
})();
