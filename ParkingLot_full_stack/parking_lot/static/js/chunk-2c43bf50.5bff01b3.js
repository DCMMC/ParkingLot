(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-2c43bf50"],{"2a3f":function(n,t,a){},"488a":function(n,t,a){},"678c":function(n,t,a){"use strict";a.r(t);var s=function(){var n=this,t=n.$createElement,a=n._self._c||t;return a("div",{staticClass:"components-container board"},[a("Kanban",{key:1,staticClass:"kanban todo",attrs:{list:n.list1,group:n.group,"header-text":"Todo"}}),n._v(" "),a("Kanban",{key:2,staticClass:"kanban working",attrs:{list:n.list2,group:n.group,"header-text":"Working"}}),n._v(" "),a("Kanban",{key:3,staticClass:"kanban done",attrs:{list:n.list3,group:n.group,"header-text":"Done"}})],1)},e=[],i=function(){var n=this,t=n.$createElement,a=n._self._c||t;return a("div",{staticClass:"board-column"},[a("div",{staticClass:"board-column-header"},[n._v("\n    "+n._s(n.headerText)+"\n  ")]),n._v(" "),a("draggable",n._b({staticClass:"board-column-content",attrs:{list:n.list,"set-data":n.setData}},"draggable",n.$attrs,!1),n._l(n.list,function(t){return a("div",{key:t.id,staticClass:"board-item"},[n._v("\n      "+n._s(t.name)+" "+n._s(t.id)+"\n    ")])}),0)],1)},o=[],r=a("1980"),c=a.n(r),d={name:"DragKanbanDemo",components:{draggable:c.a},props:{headerText:{type:String,default:"Header"},options:{type:Object,default:function(){return{}}},list:{type:Array,default:function(){return[]}}},methods:{setData:function(n){n.setData("Text","")}}},l=d,u=(a("c65c"),a("2877")),b=Object(u["a"])(l,i,o,!1,null,"7f55dbdb",null),m=b.exports,f={name:"DragKanbanDemo",components:{Kanban:m},data:function(){return{group:"mission",list1:[{name:"Mission",id:1},{name:"Mission",id:2},{name:"Mission",id:3},{name:"Mission",id:4}],list2:[{name:"Mission",id:5},{name:"Mission",id:6},{name:"Mission",id:7}],list3:[{name:"Mission",id:8},{name:"Mission",id:9},{name:"Mission",id:10}]}}},p=f,g=(a("efdc"),Object(u["a"])(p,s,e,!1,null,null,null));t["default"]=g.exports},c65c:function(n,t,a){"use strict";var s=a("2a3f"),e=a.n(s);e.a},efdc:function(n,t,a){"use strict";var s=a("488a"),e=a.n(s);e.a}}]);