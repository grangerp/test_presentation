/**
* @preserve HTML5 Shiv 3.7.2 | @afarkas @jdalton @jon_neal @rem | MIT/GPL2 Licensed
  includes printshiv	
*/
(function(e,t){function c(e,t){var n=e.createElement("p"),r=e.getElementsByTagName("head")[0]||e.documentElement;n.innerHTML="x<style>"+t+"</style>";return r.insertBefore(n.lastChild,r.firstChild)}function h(){var e=b.elements;return typeof e=="string"?e.split(" "):e}function p(e,t){var n=b.elements;if(typeof n!="string"){n=n.join(" ")}if(typeof e!="string"){e=e.join(" ")}b.elements=n+" "+e;y(t)}function d(e){var t=f[e[u]];if(!t){t={};a++;e[u]=a;f[a]=t}return t}function v(e,n,r){if(!n){n=t}if(l){return n.createElement(e)}if(!r){r=d(n)}var o;if(r.cache[e]){o=r.cache[e].cloneNode()}else if(s.test(e)){o=(r.cache[e]=r.createElem(e)).cloneNode()}else{o=r.createElem(e)}return o.canHaveChildren&&!i.test(e)&&!o.tagUrn?r.frag.appendChild(o):o}function m(e,n){if(!e){e=t}if(l){return e.createDocumentFragment()}n=n||d(e);var r=n.frag.cloneNode(),i=0,s=h(),o=s.length;for(;i<o;i++){r.createElement(s[i])}return r}function g(e,t){if(!t.cache){t.cache={};t.createElem=e.createElement;t.createFrag=e.createDocumentFragment;t.frag=t.createFrag()}e.createElement=function(n){if(!b.shivMethods){return t.createElem(n)}return v(n,e,t)};e.createDocumentFragment=Function("h,f","return function(){"+"var n=f.cloneNode(),c=n.createElement;"+"h.shivMethods&&("+h().join().replace(/[\w\-:]+/g,function(e){t.createElem(e);t.frag.createElement(e);return'c("'+e+'")'})+");return n}")(b,t.frag)}function y(e){if(!e){e=t}var n=d(e);if(b.shivCSS&&!o&&!n.hasCSS){n.hasCSS=!!c(e,"article,aside,dialog,figcaption,figure,footer,header,hgroup,main,nav,section{display:block}"+"mark{background:#FF0;color:#000}"+"template{display:none}")}if(!l){g(e,n)}return e}function x(e){var t,n=e.getElementsByTagName("*"),r=n.length,i=RegExp("^(?:"+h().join("|")+")$","i"),s=[];while(r--){t=n[r];if(i.test(t.nodeName)){s.push(t.applyElement(T(t)))}}return s}function T(e){var t,n=e.attributes,r=n.length,i=e.ownerDocument.createElement(E+":"+e.nodeName);while(r--){t=n[r];t.specified&&i.setAttribute(t.nodeName,t.nodeValue)}i.style.cssText=e.style.cssText;return i}function N(e){var t,n=e.split("{"),r=n.length,i=RegExp("(^|[\\s,>+~])("+h().join("|")+")(?=[[\\s,>+~#.:]|$)","gi"),s="$1"+E+"\\:$2";while(r--){t=n[r]=n[r].split("}");t[t.length-1]=t[t.length-1].replace(i,s);n[r]=t.join("}")}return n.join("{")}function C(e){var t=e.length;while(t--){e[t].removeNode()}}function k(e){function o(){clearTimeout(r._removeSheetTimer);if(t){t.removeNode(true)}t=null}var t,n,r=d(e),i=e.namespaces,s=e.parentWindow;if(!S||e.printShived){return e}if(typeof i[E]=="undefined"){i.add(E)}s.attachEvent("onbeforeprint",function(){o();var r,i,s,u=e.styleSheets,a=[],f=u.length,l=Array(f);while(f--){l[f]=u[f]}while(s=l.pop()){if(!s.disabled&&w.test(s.media)){try{r=s.imports;i=r.length}catch(h){i=0}for(f=0;f<i;f++){l.push(r[f])}try{a.push(s.cssText)}catch(h){}}}a=N(a.reverse().join(""));n=x(e);t=c(e,a)});s.attachEvent("onafterprint",function(){C(n);clearTimeout(r._removeSheetTimer);r._removeSheetTimer=setTimeout(o,500)});e.printShived=true;return e}var n="3.7.2";var r=e.html5||{};var i=/^<|^(?:button|map|select|textarea|object|iframe|option|optgroup)$/i;var s=/^(?:a|b|code|div|fieldset|h1|h2|h3|h4|h5|h6|i|label|li|ol|p|q|span|strong|style|table|tbody|td|th|tr|ul)$/i;var o;var u="_html5shiv";var a=0;var f={};var l;(function(){try{var e=t.createElement("a");e.innerHTML="<xyz></xyz>";o="hidden"in e;l=e.childNodes.length==1||function(){t.createElement("a");var e=t.createDocumentFragment();return typeof e.cloneNode=="undefined"||typeof e.createDocumentFragment=="undefined"||typeof e.createElement=="undefined"}()}catch(n){o=true;l=true}})();var b={elements:r.elements||"abbr article aside audio bdi canvas data datalist details dialog figcaption figure footer header hgroup main mark meter nav output picture progress section summary template time video",version:n,shivCSS:r.shivCSS!==false,supportsUnknownElements:l,shivMethods:r.shivMethods!==false,type:"default",shivDocument:y,createElement:v,createDocumentFragment:m,addElements:p};e.html5=b;y(t);var w=/^$|\b(?:all|print)\b/;var E="html5shiv";var S=!l&&function(){var n=t.documentElement;return!(typeof t.namespaces=="undefined"||typeof t.parentWindow=="undefined"||typeof n.applyElement=="undefined"||typeof n.removeNode=="undefined"||typeof e.attachEvent=="undefined")}();b.type+=" print";b.shivPrint=k;k(t)})(this,document)