(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1fd7d138"],{"3ed0":function(e,t,i){"use strict";var l=i("96cb"),d=i.n(l);d.a},"96cb":function(e,t,i){},c974:function(e,t,i){"use strict";i.r(t);var l=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",[i("sticky",{attrs:{"z-index":10,"class-name":"sub-navbar"}},[i("el-dropdown",{attrs:{trigger:"click"}},[i("el-button",{attrs:{plain:""}},[e._v("\n        Platform"),i("i",{staticClass:"el-icon-caret-bottom el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{staticClass:"no-border",attrs:{slot:"dropdown"},slot:"dropdown"},[i("el-checkbox-group",{staticStyle:{padding:"5px 15px"},model:{value:e.platforms,callback:function(t){e.platforms=t},expression:"platforms"}},e._l(e.platformsOptions,function(t){return i("el-checkbox",{key:t.key,attrs:{label:t.key}},[e._v("\n            "+e._s(t.name)+"\n          ")])}),1)],1)],1),e._v(" "),i("el-dropdown",{attrs:{trigger:"click"}},[i("el-button",{attrs:{plain:""}},[e._v("\n        Link"),i("i",{staticClass:"el-icon-caret-bottom el-icon--right"})]),e._v(" "),i("el-dropdown-menu",{staticClass:"no-padding no-border",staticStyle:{width:"300px"},attrs:{slot:"dropdown"},slot:"dropdown"},[i("el-input",{attrs:{placeholder:"Please enter the content"},model:{value:e.url,callback:function(t){e.url=t},expression:"url"}},[i("template",{slot:"prepend"},[e._v("\n            Url\n          ")])],2)],1)],1),e._v(" "),i("div",{staticClass:"time-container"},[i("el-date-picker",{attrs:{"picker-options":e.pickerOptions,type:"datetime",format:"yyyy-MM-dd HH:mm:ss",placeholder:"Release time"},model:{value:e.time,callback:function(t){e.time=t},expression:"time"}})],1),e._v(" "),i("el-button",{staticStyle:{"margin-left":"10px"},attrs:{type:"success"}},[e._v("\n      publish\n    ")])],1),e._v(" "),i("div",{staticClass:"components-container"},[i("code",[e._v("Sticky header, "+e._s(e.$t("components.stickyTips")))]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("sticky",{attrs:{"sticky-top":200}},[i("el-button",{attrs:{type:"primary"}},[e._v(" placeholder")])],1),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")]),e._v(" "),i("div",[e._v("placeholder")])],1)],1)},d=[],o=i("0a0d"),v=i.n(o),a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{style:{height:e.height+"px",zIndex:e.zIndex}},[i("div",{class:e.className,style:{top:e.isSticky?e.stickyTop+"px":"",zIndex:e.zIndex,position:e.position,width:e.width,height:e.height+"px"}},[e._t("default",[i("div",[e._v("sticky")])])],2)])},c=[],n=(i("c5f6"),{name:"Sticky",props:{stickyTop:{type:Number,default:0},zIndex:{type:Number,default:1},className:{type:String,default:""}},data:function(){return{active:!1,position:"",width:void 0,height:void 0,isSticky:!1}},mounted:function(){this.height=this.$el.getBoundingClientRect().height,window.addEventListener("scroll",this.handleScroll),window.addEventListener("resize",this.handleReize)},activated:function(){this.handleScroll()},destroyed:function(){window.removeEventListener("scroll",this.handleScroll),window.removeEventListener("resize",this.handleReize)},methods:{sticky:function(){this.active||(this.position="fixed",this.active=!0,this.width=this.width+"px",this.isSticky=!0)},handleReset:function(){this.active&&this.reset()},reset:function(){this.position="",this.width="auto",this.active=!1,this.isSticky=!1},handleScroll:function(){var e=this.$el.getBoundingClientRect().width;this.width=e||"auto";var t=this.$el.getBoundingClientRect().top;t<this.stickyTop?this.sticky():this.handleReset()},handleReize:function(){this.isSticky&&(this.width=this.$el.getBoundingClientRect().width+"px")}}}),r=n,s=i("2877"),p=Object(s["a"])(r,a,c,!1,null,null,null),h=p.exports,_={name:"StickyDemo",components:{Sticky:h},data:function(){return{time:"",url:"",platforms:["a-platform"],platformsOptions:[{key:"a-platform",name:"platformA"},{key:"b-platform",name:"platformB"},{key:"c-platform",name:"platformC"}],pickerOptions:{disabledDate:function(e){return e.getTime()>v()()}}}}},u=_,m=(i("3ed0"),Object(s["a"])(u,l,d,!1,null,"09c06fe0",null));t["default"]=m.exports}}]);