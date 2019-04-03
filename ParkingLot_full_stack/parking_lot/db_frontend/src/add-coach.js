import Vue from 'vue'
import './plugins/vuetify'
import AddCoach from './AddCoach.vue'
import './assets/disable-chrome-pull-down-refresh.css'

Vue.config.productionTip = false

new Vue({
  render: h => h(AddCoach),
}).$mount('#add-coach')
