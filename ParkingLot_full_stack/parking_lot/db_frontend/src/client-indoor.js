import Vue from 'vue'
import './plugins/vuetify'
import ClientIndoor from './ClientIndoor.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(ClientIndoor),
}).$mount('#client-indoor')
