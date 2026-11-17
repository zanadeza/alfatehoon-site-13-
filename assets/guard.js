/* حماية خفيفة: ردع، مش حماية مطلقة. أي كود يصل للمتصفح يمكن لمن يملك خبرة الاطلاع عليه. */
(function(){
"use strict";
var d=document,msg="⚠️ ليس مسموحاً لك بدخول أدوات المطور أو فحص الموقع. أغلقها للمتابعة.";
function box(text,lock){
 var o=d.getElementById("gd-box");
 if(!o){o=d.createElement("div");o.id="gd-box";o.setAttribute("style","position:fixed;inset:0;z-index:2147483647;display:flex;align-items:center;justify-content:center;padding:24px;background:#101820;color:#fff;font:600 1.3rem/1.8 Tahoma,Arial,sans-serif;text-align:center");(d.body||d.documentElement).appendChild(o)}
 o.textContent=text;o.style.display="flex";
 if(!lock){clearTimeout(box.t);box.t=setTimeout(function(){o.style.display="none"},2500)}
}
function hide(){var o=d.getElementById("gd-box");if(o)o.style.display="none"}
function editable(t){return t&&(t.tagName==="INPUT"||t.tagName==="TEXTAREA"||t.isContentEditable)}
addEventListener("contextmenu",function(e){if(!editable(e.target))e.preventDefault()},true);
addEventListener("keydown",function(e){
 var k=(e.key||"").toLowerCase(),c=e.ctrlKey||e.metaKey;
 if(e.key==="F12"||(c&&e.shiftKey&&"ijckm".indexOf(k)>-1)||(c&&(k==="u"||k==="s"))||(e.metaKey&&e.altKey&&"iju".indexOf(k)>-1)){e.preventDefault();e.stopPropagation();box(msg,false);return false}
},true);
if(window.top!==window.self){try{window.top.location=window.self.location}catch(x){d.documentElement.innerHTML=""}}
/* كشف أدوات المطور على الحاسوب فقط، لتفادي حجب مستخدمي الجوال */
var desktop=matchMedia("(min-width:1024px) and (pointer:fine)").matches;
if(desktop){
 var probe=new Image(),opened=false;
 Object.defineProperty(probe,"id",{get:function(){opened=true}});
 setInterval(function(){
  opened=false;
  var big=(window.outerHeight-window.innerHeight>230)||(window.outerWidth-window.innerWidth>380&&window.outerHeight-window.innerHeight>120);
  try{console.log(probe);console.clear()}catch(x){}
  if(opened||big)box(msg,true);else hide();
 },1200);
}
})();
