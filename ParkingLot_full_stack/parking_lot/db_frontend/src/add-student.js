import Vue from 'vue'
import './plugins/vuetify'
import AddStudent from './AddStudent.vue'
import './assets/disable-chrome-pull-down-refresh.css'

Vue.config.productionTip = false

new Vue({
  render: h => h(AddStudent),
}).$mount('#add-student')
