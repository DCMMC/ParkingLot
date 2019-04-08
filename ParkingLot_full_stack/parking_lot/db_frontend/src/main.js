import Vue from 'vue'
import './plugins/axios'
import './plugins/vuetify'
import App from './App.vue'
// import './assets/disable-chrome-pull-down-refresh.css'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#home')