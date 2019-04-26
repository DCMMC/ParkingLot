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
    websock: null,
    layerNum: 1
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
      var ul = IndoorMap.getUI(this.map)
      document.body.appendChild(ul)
      this.ready = true
    })
    // if (!this.ready) {
    //   setTimeout(() => {
    //     // console.log(this.ready)
    //     // 必须要在 callback 完成之后
    //     // true 表示正在被使用中
    //     // this.map.updateParkingLotStatus('1', true)
    //     // this.map.updateParkingLotStatus('车库3', true)
    //   }, 1000)
    // }

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
      // 原来写死的 127.0.0.1 跟 cookie 的 0.0.0.0 不一致
      // channels 死活得不到正确的 scope['user'] debug 了半天...
      var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'

      // var ws_path = ws_scheme + '://' + window.location.host +
      //   '/ws/parkingLotStatus/' + this.layerNum + '/'
      var ws_path = ws_scheme + '://' + 'localhost:8080' +
        '/ws/parkingLotStatus/' + this.layerNum + '/'
      this.websock = new WebSocket(ws_path)
      this.websock.onmessage = this.websocketonmessage
      this.websock.onopen = this.websocketonopen
      this.websock.onerror = this.websocketonerror
      this.websock.onclose = this.websocketclose
    },
    websocketonopen() {
      // 连接建立之后执行send方法发送数据
      // const actions = { test: '12345' }
      // this.websocketsend(JSON.stringify(actions))
    },
    websocketonerror() {
      // 连接建立失败重连
      console.error('意外断开连接, 尝试重新连接...')
      // this.initWebSocket()
    },
    websocketonmessage(e) {
      // 数据接收
      const redata = JSON.parse(e.data)
      if (redata.code === 'updateParking') {
        console.log('updateParking')
        var t_out = 0
        if (!this.ready) {
          t_out = 1000
        }
        setTimeout(() => {
          for (var i in redata.data[this.layerNum]) {
            for (var j in redata.data[this.layerNum]['' + i]) {
              this.map.updateParkingLotStatus(i,
                redata.data[this.layerNum]['' + i]['' + j])
            }
          }
        }, t_out)
      }
      // console.log(redata)
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
