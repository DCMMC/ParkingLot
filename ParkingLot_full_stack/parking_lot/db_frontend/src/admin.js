import Vue from 'vue'
import './plugins/vuetify'
import Admin from './Admin.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(Admin),
}).$mount('#admin')
