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
                <v-expansion-panel v-model="panel" expand light>
                  <v-expansion-panel-content
                    v-for="(item,i) in 2"
                    :key="i"
                  >
                    <template v-slot:header>
                      <div class="headline">一楼一区</div>
                    </template>
                    <vue-custom-scrollbar
                      id="emptyLot"
                      class="scroll-area"
                      :settings="settings"
                    >
                      <ul>
                        <li
                          v-for="(item,i) in 20"
                          :key="i"
                          class="headline"
                          style="display: flex; justify-content: center;"
                        >
                          {{ i }}
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
                    {{ license_plate }}
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
    items: 2,
    settings: {
      maxScrollbarLength: 60
    },
    scrollTop: 250,
    license_plate: 'Unknown',
    indoorNum: 1,
    websock: null
  }),
  created() {
    this.initWebSocket()
  },
  destroyed() {
    this.websock.close() // 离开路由之后断开websocket连接
  },
  mounted() {
    // 全部展开
    this.panel = [...Array(this.items).keys()].map(_ => true)
    // TODO: 使用 scrollTop 自动滚动
    var node = document.getElementById('emptyLot')
    setTimeout(() => { node.scrollTop = 200; console.log('set scrollTop') }, 5000)
  },
  methods: {
    scrollHanle(evt) {
      console.log(evt)
    },
    initWebSocket() {
      // 初始化weosocket
      var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      var ws_path = ws_scheme + '://' + window.location.host +
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
      // console.error('意外断开连接, 尝试重新连接...')
      // this.initWebSocket()
    },
    websocketonmessage(e) {
      // 数据接收
      const redata = JSON.parse(e.data)
      this.license_plate = redata.message.pstr
      console.log(redata)
    },
    websocketsend(Data) {
      // 数据发送
      this.websock.send(Data)
    },
    websocketclose(e) {
      // 关闭
      console.log('断开连接', e)
    }
  }
}
</script>

<style>
.scroll-area {
   height: 200px;
}
ul,li {
  list-style: none;
}
</style>
