<template>
	<div>
		<div id="indoor3d" style="width: 800; height: 500px;left: 0px; background-color:red;"
			v-on:mouseenter="disable_scroll()"
			v-on:mouseleave="enable_scroll()"></div>
		<div class="testButton">
			<ul >
			    <li v-on:click="map.zoomOut(1.2)">+</li>
			    <li v-on:click="map.zoomIn(1.2)">-</li>
			    <li v-on:click="map.setDefaultView()">Default View</li>
			</ul>
		</div>
	</div>
</template>

<script>
import THREE from '../assets/js/three.min.js'
import IndoorMap from '../assets/js/IndoorMap.js'
import Stats from '../assets/js/stats.min.js'

// import THREE from 'three'
export default {
    data: () => ({
		params: null,
    	map: null
    }),
    mounted: function () {
    	this.params = {
        	mapDiv:"indoor3d",
        	dim:"3d"
    	};
    	this.map = IndoorMap(this.params);
    	this.ready = false;
    	// 这个 models 是放在 django 的根目录的
	    this.map.load('/models/testMapData.json', () => {
	        //map.setTheme(testTheme);
	        this.map.showAreaNames(true).setSelectable(false);
	        this.map.showFloor(1);
	        var ul = IndoorMap.getUI(this.map);
	        document.body.appendChild(ul);
	        this.ready = true;
	    });
	    if (!this.ready) {
	    	setTimeout(() => {
	    		// console.log(this.ready)
	    		// 必须要在 callback 完成之后
	    		this.map.updateParkingLotStatus("1", true);
	    		this.map.updateParkingLotStatus("车库3", true);
	    	}, 1000)	
	    }

	    // debug fps 信息
	    // var stats = new Stats();
	    // stats.domElement.style.position = 'absolute';
	    // stats.domElement.style.top = '0px';
	    // document.body.appendChild(stats.domElement);
	    // animate();

	    // function animate() {
	    //     requestAnimationFrame(animate);
	    //     stats.update();
	    // }
    },
    methods: {
    	disable_scroll() {
    		// console.log('disable_scroll')
    		// let wheel = (e) => e.preventDefault;
		    // if (window.addEventListener) {
		    //     window.addEventListener('DOMMouseScroll', wheel, false);
		    // }
		    // window.onmousewheel = document.onmousewheel = wheel;
		},
		enable_scroll() {
			// console.log('enable_scroll')
			// let wheel = (e) => e.preventDefault;
		 //    if (window.removeEventListener) {
		 //        window.removeEventListener('DOMMouseScroll', wheel, false);
		 //    }
		 //    window.onmousewheel = document.onmousewheel = document.onkeydown = null;
		}
    }
}
</script>

<style>
	@import '../assets/css/indoor3D.css';
</style>