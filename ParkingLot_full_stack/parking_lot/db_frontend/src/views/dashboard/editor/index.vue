<template>
  <div class="dashboard-editor-container">
    <div class="info-container">
      <span class="display_name">{{ name }}</span>
    </div>
    <el-row style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
      <ParkingLotMap />
    </el-row>
    <el-dialog
      title="收费窗口"
      :visible.sync="dialogVisible"
      :close-on-click-modal="false"
    >
      <el-form ref="ruleForm" :model="fee_cards_form">
        <el-form-item label="车牌号码" :label-width="formLabelWidth">
          <el-input
            v-model="fee_cards_form.license_plate"
            autocomplete="off"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="入口号" :label-width="formLabelWidth">
          <el-input
            v-model="fee_cards_form.indoorNum"
            autocomplete="off"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="入场时间" :label-width="formLabelWidth">
          <el-input
            v-model="fee_cards_form.date_in"
            autocomplete="off"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="出口号" :label-width="formLabelWidth">
          <el-input
            v-model="fee_cards_form.outdoorNum"
            autocomplete="off"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="结算时间" :label-width="formLabelWidth">
          <el-input
            v-model="fee_cards_form.date_out"
            autocomplete="off"
            :disabled="true"
          />
        </el-form-item>
        <el-form-item label="会员卡" :label-width="formLabelWidth">
          <el-select
            v-model="fee_cards_form.card_id"
            style="width: 500px"
            :default-first-option="true"
            @change="update_cards_select($event)"
          >
            <el-option
              v-for="(card_id, card_info) in cards"
              :key="card_info"
              :label="card_info"
              :disabled="check_value(card_id)"
              :value="card_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item
          label="消费"
          :label-width="formLabelWidth"
          :rules="[
            { required: true, message: '必须指定消费额'},
            { type: 'number', message: '消费额必须是数值'},
            { validator: validateFeeValue, trigger: 'blur' }
          ]"
        >
          <el-input
            v-model="fee_cards_form.fee_selected"
            autocomplete="off"
            :autofocus="true"
            :disabled="fee_not_editable"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="confirm_fee()">提交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import ParkingLotMap from '@/components/ParkingLotMap'

export default {
  name: 'DashboardEditor',
  components: {
    ParkingLotMap
  },
  data() {
    return {
      dialogVisible: false,
      websock: null,
      // TODO: 现在我暂时是考虑一个出口管理员管理所以出口, 所以这个
      // doorNum 现在暂时没有什么用处
      doorNum: 1,
      formLabelWidth: '120px',
      fee_cards_form: {},
      cards: {},
      fee_not_editable: false,
      card_values: {},
      fee_confirmed: null,
      validateFeeValue: (rule, value, callback) => {
        if (this.cards[this.fee_cards_form.card_id][1] === 'count' &&
          value < 0) {
          callback(Error('选用储值会员卡时, 消费额不能为负值'))
        } else if (this.cards[this.fee_cards_form.card_id][1] === 'top-up' &&
          (value > 0 || String(value).indexOf('.') > -1)) {
          callback(Error('选用记次会员卡时, 消费额不能为正值或小数'))
        }
        callback()
      }
    }
  },
  computed: {
    ...mapGetters([
      'name',
      'avatar',
      'roles'
    ])
  },
  created() {
    this.initWebSocket()
  },
  destroyed() {
    this.websock.close() // 离开路由之后断开websocket连接
  },
  mounted() {
    // setTimeout(() => {
    //   this.websocketonmessage({ 'data': JSON.stringify({
    //     'code': 'fee_cards',
    //     'data': {
    //       'fee': 25.5,
    //       'date_in': '2019/4/21, 21:26:10',
    //       'date_out': '2019/4/22, 21:26:10',
    //       'indoorNum': '1',
    //       'indoorName': '入口',
    //       'outdoorNum': '2',
    //       'outdoorName': '出口',
    //       'cards': [
    //         {'id': '456465456', 'card_type': 'count', 'value': 20},
    //         {'id': '4564564564', 'card_type': 'top-up', 'value': 45.5}
    //       ],
    //       'license_plate': '沪A12345'
    //     }
    //   })})
    // }, 5000)
  },
  methods: {
    initWebSocket() {
      // 初始化weosocket
      var ws_scheme = window.location.protocol === 'https:' ? 'wss' : 'ws'
      var ws_path = ws_scheme + '://' + window.location.host +
        '/ws/outdoor_admin/' + this.doorNum + '/'
      // var ws_path = ws_scheme + '://' + 'localhost:8080' +
      //   '/ws/outdoor_admin/' + this.doorNum + '/'
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
      console.log(redata)
      if (redata.code === 'fee_cards') {
        var dialog = redata.data
        dialog.card_id = ''
        dialog.fee_selected = dialog.fee
        var cards = { '无(非会员)': '' }
        var card_vals = {}
        for (var c in redata.data.cards) {
          var c_k = ''
          c = redata.data.cards[c]
          if (c.card_type === 'top-up') {
            c_k += '储值卡: ' + c.id + ', 余额: ' + c.value
          } else if (c.card_type === 'count') {
            c_k += '记次卡: ' + c.id + ', 剩余次数: ' + c.value
          }
          cards[c_k] = c.id
          card_vals[c.id] = [c.value, c.card_type]
        }
        this.cards = cards
        this.fee_cards_form = dialog
        this.dialogVisible = true
        this.card_values = card_vals
      } else if (redata.code === 'confirm_fee') {
        this.fee_confirmed = true
        if (redata.data.type === 'success') {
          this.$message({
            'type': 'success',
            'message': '交易成功: ' + JSON.stringify(redata.data)
          })
        } else {
          this.$message({
            'type': 'error',
            'message': '交易失败: ' + JSON.stringify(redata.data)
          })
        }
      }
    },
    websocketsend(Data) {
      // 数据发送
      this.websock.send(JSON.stringify(Data))
    },
    websocketclose(e) {
      // 关闭
      console.log('断开连接', e)
      // 2s 重连
      // setTimeout(() => {
      //   this.initWebSocket()
      // }, 2000)
    },
    confirm_fee() {
      this.$refs.ruleForm.validate((valid) => {
        if (valid) {
          this.dialogVisible = false
          var content = this.fee_cards_form
          content.doorNum = content.outdoorNum
          content = {
            'type': 'confirm_fee',
            'data': content
          }
          this.websocketsend(content)
          setTimeout(() => {
            console.log('验证提交结果, ' + this.fee_confirmed)
            if (this.fee_confirmed !== null && !this.fee_confirmed) {
              this.$message({
                'type': 'error',
                'message': '交易失败!! 服务端未响应改请求'
              })
            }
            this.fee_confirmed = null
          }, 1500)
        } else {
          console.log('表单验证不通过')
          return false
        }
      })
    },
    update_cards_select(event) {
      var selected_id = event
      if (selected_id === '') {
        this.fee_not_editable = false
        // this.$refs.fee_input.focus();
      } else {
        this.fee_not_editable = true
      }
      console.log(this.card_values[selected_id])
      if (selected_id !== '' && this.card_values[selected_id][1] === 'count') {
        this.$set(this.fee_cards_form, 'fee_selected', -1)
      } else {
        var fee = this.fee_cards_form.fee
        this.$set(this.fee_cards_form, 'fee_selected', fee)
      }
    },
    check_value(card_id) {
      if (this.card_values[card_id]) { return this.card_values[card_id][0] <= 0 } else { return false }
    }
  }
}
</script>

<style scoped>
</style>
