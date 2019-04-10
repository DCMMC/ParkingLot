import Vue from 'vue'
import './plugins/vuetify'
import ClientOutdoor from './ClientOutdoor.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(ClientOutdoor),
}).$mount('#client-outdoor')
