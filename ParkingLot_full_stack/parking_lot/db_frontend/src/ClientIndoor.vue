<template>
  <v-app>
    <Header />
    <v-content>
      <v-container fluid grid-list-md style="padding: 4px;">
        <v-layout row wrap style="height: 700px; width: 100%;">
          <v-flex d-flex shrink style="width: 20%; height: 100%;">
            <v-card color="purple" dark hover ripple>
              <v-card-title primary class="display-1">推荐停车位</v-card-title>
              <!-- <v-card-text class="title">
                TODO: 使用 expansion panels
              </v-card-text> -->
              <v-card-actions>
                <v-expansion-panel :value="panel" expand light>
                  <v-expansion-panel-content
                    v-for="(floor_region, floor_region_name) in parkings_status_unused"
                    :key="floor_region_name"
                  >
                    <template v-slot:header>
                      <div class="headline">{{ floor_region_name }}</div>
                    </template>
                    <vue-custom-scrollbar
                      id="emptyLot"
                      class="scroll-area"
                      :settings="settings"
                    >
                      <ul>
                        <li
                          v-for="(status, id) in floor_region"
                          :key="id"
                          class="headline"
                          style="display: flex; justify-content: center;"
                        >
                          {{ id }}号位
                        </li>
                      </ul>
                    </vue-custom-scrollbar>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-card-actions>
            </v-card>
          </v-flex>
          <v-flex d-flex shrink style="width: 80%;">
            <v-layout column wrap>
              <v-flex d-flex style="height: 70%;">
                <ParkingLotMap />
              </v-flex>
              <v-flex d-flex style="height: 30%;">
                <v-card
                  color="red lighten-2"
                  dark
                  hover
                  ripple
                >
                  <v-card-text class="display-1">
                    欢迎您! <br>
                    {{ license_plate }} <br>
                    推荐车位:
                    {{ recommand_parkings }}
                  </v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
// import Vue from 'vue'
// import axios from 'axios'
import Footer from './components/footer'
import Header from './components/header'
import ParkingLotMap from './components/ParkingLotMap'
import vueCustomScrollbar from 'vue-custom-scrollbar'

export default {
  name: 'ClientIndor',
  components: {
    Footer,
    ParkingLotMap,
    Header,
    vueCustomScrollbar
  },
  data: () => ({
    panel: [],
    settings: {
      maxScrollbarLength: 60
    },
    parkings_status: {},
    recommand_parkings: '',
    scrollTop: 250,
    license_plate: '',
    indoorNum: 1, // TODO
    websock: null
  }),
  computed: {
    parkings_status_unused() {
      var p = {}
      for (var i in this.parkings_status) {
          p[i] = Object.fromEntries(
              Object.entries(this.parkings_status[i]).filter(
                ([k,v]) => v === 'unused'));
      }
      return p
    }
  },
  created() {
    this.initWebSocket()
  },
  destroyed() {
    this.websock.close() // 离开路由之后断开websocket连接
  },
  mounted() {
    // TODO: 使用 scrollTop 自动滚动
    setTimeout(() => {
      var node = document.getElementById('emptyLot')
      node.scrollTop = 200; console.log('set scrollTop')
    }, 5000)
  },
  methods: {
    initWebSocket() {
      // 初始化weosocket
      var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      // var ws_path = ws_scheme + '://' + window.location.host +
      //   '/ws/indoor/' + this.indoorNum + '/'
      var ws_path = ws_scheme + '://' + 'localhost:8080' +
        '/ws/indoor/' + this.indoorNum + '/'
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
      this.initWebSocket()
    },
    websocketonmessage(e) {
      // 数据接收
      const redata = JSON.parse(e.data)
      if (redata.code === 'discover_license') {
        this.license_plate = redata.data.pstr
      } else if (redata.code === 'recommand_parkings') {
        var recomm = ''
        for (var i in redata.data) {
          recomm += (redata.data[i] + ' ')
        }
        this.recommand_parkings = recomm
      } else if (redata.code === 'all_parkings_status') {
        for (var k_f in redata.data) {
          for (var k_r in redata.data['' + k_f]) {
            var f_r_name = '' + k_f + '楼' + k_r + '区'
            var parkings = {}
            for (var p in redata.data['' + k_f]['' + k_r]) {
              parkings['' + p] =
                redata.data['' + k_f]['' + k_r]['' + p]
            }
            // console.log(this.parkings_status, f_r_name, parkings)
            // Vue 不能直接设置 data 里面的变量, 因为这样的改变
            // 不会将事件传递到 Vue 去, 必须要用 $set 或 Vue.set 方法来修改对象
            this.$set(this.parkings_status, f_r_name, parkings)
          }
        }
        // 全部展开
        // 对于 data 中的赋值, 必须要用 Object.assign 才能发出事件被 vue 捕获.
        Object.assign(this.panel, [...Array(Object.keys(this.parkings_status).length).keys()].map(_ => true))
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
      // 2s 重连, 业务必须保持一直连接状态
      // setTimeout(() => {
      //   this.initWebSocket()
      // }, 2000)
    }
  }
}
</script>

<style>
.scroll-area {
   height: 400px;
}
ul,li {
  list-style: none;
}
</style>
