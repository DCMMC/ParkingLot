<template>
  <v-app>
    <Header />
    <v-content>
      <v-container fluid grid-list-md style="padding: 4px;">
        <v-layout row wrap style="height: 700px; width: 100%;">
          <v-flex d-flex shrink style="width: 20%; height: 100%;">
            <v-card color="purple" dark hover ripple>
              <v-card-title primary class="headline">公告</v-card-title>
              <v-card-text class="title">也许加点 Ads 吧...</v-card-text>
            </v-card>
          </v-flex>
          <v-flex d-flex shrink style="width: 80%;">
            <v-layout column wrap>
              <v-flex d-flex style="height: 70%;">
                <v-card color="blue" dark hover ripple>
                  <v-card-title primary class="headline">收费信息</v-card-title>
                  <v-card-text class="title">{{ fee_info }}</v-card-text>
                </v-card>
              </v-flex>
              <v-flex d-flex style="height: 30%;">
                <v-card
                  color="red lighten-2"
                  dark
                  hover
                  ripple
                >
                  <v-card-text class="headline">一路顺风! <br>{{ license_plate }}</v-card-text>
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
import Footer from './components/footer'
import Header from './components/header'

export default {
  name: 'ClientOutdoor',
  components: {
    Footer,
    Header
  },
  data: () => ({
    license_plate: '',
    outdoorNum: 1,
    websock: null,
    fee_info: ''
  }),
  created() {
    this.initWebSocket()
  },
  destroyed() {
    this.websock.close() // 离开路由之后断开websocket连接
  },
  mounted() {
  },
  methods: {
    initWebSocket() {
      // 初始化weosocket
      var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      // var ws_path = ws_scheme + '://' + window.location.host +
      //   '/ws/indoor/' + this.indoorNum + '/'
      var ws_path = ws_scheme + '://' + 'localhost:8080' +
        '/ws/outdoor/' + this.outdoorNum + '/'
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
      console.log(redata)
      var info = ''
      if (redata.code === 'discover_license') {
        this.license_plate = redata.data.pstr
        if (this.license_plate.length === 0) {
          // 把收费区域置空
          this.fee_info = ''
        }
      } else if (redata.code === 'fee_cards') {
        info += ('出口号: ' + redata.data.doorNum + '<br/>')
        info += ('入场时间: ' + redata.data.date_in + '<br/>')
        info += ('出场时间: ' + redata.data.date_out + '<br/>')
        info += ('计时费用: ' + redata.data.fee + '<br/>')
        if (redata.data.cards && redata.data.cards.length > 0) {
          info += ('您持有以下会员卡: <br/>')
          for (var card in redata.data.cards) {
            var card_t = ''
            var value_prompt = ''
            if (card.card_type === 'count') {
              card_t = '记次卡'
              value_prompt = '剩余次数'
            } else if (card.card_type === 'top-up') {
              card_t = '储值卡'
              value_prompt = '余额'
            }
            info += ('卡号: ' + card.id + ', 类型: ' + card_t +
              ', ' + value_prompt + ': ' + card.value)
            info += '<br/>'
          }
        }
        info += '如果您持有其他会员卡, 请向管理员说明卡号<br/>'
        this.fee_info = info
      } else if (redata.code === 'confirm_fee') {
        info += '收费成功 <br/>'
        info += ('管理员: ' + redata.data.admin_info + '<br/>')
        info += ('出口号: ' + redata.data.doorNum + '<br/>')
        if (info.card_id !== '') {
          if (redata.data.fee <= 0) {
            info += ('记次卡消费, 卡号: ' + redata.data.card_id + '<br/>')
          } else {
            info += ('储值卡消费 ' + redata.data.fee + ' 元, 卡号: ' +
              redata.data.card_id + '<br/>')
          }
        } else {
          info += ('现金支付: ' + redata.data.fee + '<br/>')
        }
        this.fee_info = info
      }
    },
    websocketsend(Data) {
      // 数据发送
      this.websock.send(Data)
    },
    websocketclose(e) {
      // 关闭
      console.log('断开连接', e)
      // 2s 重连
      // setTimeout(() => {
      //   this.initWebSocket()
      // }, 2000)
    }
  }
}
</script>
