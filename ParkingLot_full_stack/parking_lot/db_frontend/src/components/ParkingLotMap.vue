<template>
  <div>
    <div
      id="indoor3d"
      style="width: 800; height: 500px;left: 0px; background-color:red;"
      @mouseenter="disable_scroll()"
      @mouseleave="enable_scroll()"
    />
    <div class="testButton">
      <ul id="controlBtn">
        <li @click="map.zoomOut(1.2)">+</li>
        <li @click="map.zoomIn(1.2)">-</li>
        <li @click="map.setDefaultView()">Default View</li>
      </ul>
    </div>
  </div>
</template>

<script>
// import THREE from '../assets/js/three.min.js'
import IndoorMap from '../assets/js/IndoorMap.js'
// import Stats from '../assets/js/stats.min.js'

// import THREE from 'three'
export default {
  data: () => ({
    params: null,
    map: null,
    websock: null
  }),
  created() {
    this.initWebSocket()
  },
  destroyed() {
    this.websock.close() // 离开路由之后断开websocket连接
  },
  mounted: function() {
    this.params = {
      mapDiv: 'indoor3d',
      dim: '3d'
    }
    this.map = IndoorMap(this.params)
    this.ready = false
    // 这个 models 是放在 django 的根目录的
    this.map.load('/models/testMapData.json', () => {
      // map.setTheme(testTheme);
      this.map.showAreaNames(true).setSelectable(false)
      this.map.showFloor(1)
      // DCMMC: 暂时去掉这个, 这个要放在组件里面
      // var ul = IndoorMap.getUI(this.map);
      // document.body.appendChild(ul);
      this.ready = true
    })
    if (!this.ready) {
      setTimeout(() => {
        // console.log(this.ready)
        // 必须要在 callback 完成之后
        this.map.updateParkingLotStatus('1', true)
        this.map.updateParkingLotStatus('车库3', true)
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
    initWebSocket() {
      // 初始化weosocket
      const wsuri = 'ws://127.0.0.1:8080'
      this.websock = new WebSocket(wsuri)
      this.websock.onmessage = this.websocketonmessage
      this.websock.onopen = this.websocketonopen
      this.websock.onerror = this.websocketonerror
      this.websock.onclose = this.websocketclose
    },
    websocketonopen() {
      // 连接建立之后执行send方法发送数据
      const actions = { test: '12345' }
      this.websocketsend(JSON.stringify(actions))
    },
    websocketonerror() {
      // 连接建立失败重连
      console.error('意外断开连接, 尝试重新连接...')
      this.initWebSocket()
    },
    websocketonmessage(e) {
      // 数据接收
      const redata = JSON.parse(e.data)
      console.log(redata)
    },
    websocketsend(Data) {
      // 数据发送
      this.websock.send(Data)
    },
    websocketclose(e) {
      // 关闭
      console.log('断开连接', e)
    },
    disable_scroll() {},
    enable_scroll() {}
  }
}
</script>

<style>
@import "../assets/css/indoor3D.css";
</style>
