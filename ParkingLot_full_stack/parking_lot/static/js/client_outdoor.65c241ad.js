(function(t){function e(e){for(var n,l,i=e[0],c=e[1],u=e[2],d=0,f=[];d<i.length;d++)l=i[d],a[l]&&f.push(a[l][0]),a[l]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(t[n]=c[n]);s&&s(e);while(f.length)f.shift()();return o.push.apply(o,u||[]),r()}function r(){for(var t,e=0;e<o.length;e++){for(var r=o[e],n=!0,i=1;i<r.length;i++){var c=r[i];0!==a[c]&&(n=!1)}n&&(o.splice(e--,1),t=l(l.s=r[0]))}return t}var n={},a={client_outdoor:0},o=[];function l(e){if(n[e])return n[e].exports;var r=n[e]={i:e,l:!1,exports:{}};return t[e].call(r.exports,r,r.exports,l),r.l=!0,r.exports}l.m=t,l.c=n,l.d=function(t,e,r){l.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:r})},l.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},l.t=function(t,e){if(1&e&&(t=l(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var r=Object.create(null);if(l.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var n in t)l.d(r,n,function(e){return t[e]}.bind(null,n));return r},l.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return l.d(e,"a",e),e},l.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},l.p="/";var i=window["webpackJsonp"]=window["webpackJsonp"]||[],c=i.push.bind(i);i.push=e,i=i.slice();for(var u=0;u<i.length;u++)e(i[u]);var s=c;o.push([3,"chunk-vendors","chunk-common"]),r()})({3:function(t,e,r){t.exports=r("bb9e")},bb9e:function(t,e,r){"use strict";r.r(e);r("cadf"),r("551c"),r("f751"),r("097d");var n=r("2b0e"),a=(r("402c"),function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-app",[r("Header"),t._v(" "),r("v-content",[r("v-container",{staticStyle:{padding:"4px"},attrs:{fluid:"","grid-list-md":""}},[r("v-layout",{staticStyle:{height:"700px",width:"100%"},attrs:{row:"",wrap:""}},[r("v-flex",{staticStyle:{width:"20%",height:"100%"},attrs:{"d-flex":"",shrink:""}},[r("v-card",{attrs:{color:"purple",dark:"",hover:"",ripple:""}},[r("v-card-title",{staticClass:"headline",attrs:{primary:""}},[t._v("TODO:")]),t._v(" "),r("v-card-text",{staticClass:"title"},[t._v("也许加点 Ads 吧...")])],1)],1),t._v(" "),r("v-flex",{staticStyle:{width:"80%"},attrs:{"d-flex":"",shrink:""}},[r("v-layout",{attrs:{column:"",wrap:""}},[r("v-flex",{staticStyle:{height:"70%"},attrs:{"d-flex":""}},[r("v-card",{attrs:{color:"blue",dark:"",hover:"",ripple:""}},[r("v-card-title",{staticClass:"headline",attrs:{primary:""}},[t._v("TODO:")]),t._v(" "),r("v-card-text",{staticClass:"title"},[t._v("收费信息")])],1)],1),t._v(" "),r("v-flex",{staticStyle:{height:"30%"},attrs:{"d-flex":""}},[r("v-card",{attrs:{color:"red lighten-2",dark:"",hover:"",ripple:""}},[r("v-card-text",{staticClass:"headline"},[t._v("TODO: "),r("br"),t._v(" 一路顺风! 沪A 12345")])],1)],1)],1)],1)],1)],1)],1),t._v(" "),r("Footer")],1)}),o=[],l=(r("bc3a"),r("076e")),i=r("71c2"),c={name:"ClientOutdoor",components:{Footer:l["a"],Header:i["a"]},data:function(){return{}},mounted:function(){},methods:{}},u=c,s=r("2877"),d=r("6544"),f=r.n(d),p=r("7496"),v=r("b0af"),h=r("99d9"),b=r("12b2"),y=r("a523"),x=r("549c"),_=r("0e8f"),g=r("a722"),m=Object(s["a"])(u,a,o,!1,null,null,null),O=m.exports;f()(m,{VApp:p["a"],VCard:v["a"],VCardText:h["b"],VCardTitle:b["a"],VContainer:y["a"],VContent:x["a"],VFlex:_["a"],VLayout:g["a"]});r("985d");n["default"].config.productionTip=!1,new n["default"]({render:function(t){return t(O)}}).$mount("#client-outdoor")}});