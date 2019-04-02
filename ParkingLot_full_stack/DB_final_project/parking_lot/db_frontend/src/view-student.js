import Vue from 'vue'
import './plugins/vuetify'
import ViewStudent from './ViewStudent.vue'
import './assets/disable-chrome-pull-down-refresh.css'

Vue.config.productionTip = false

// preventPullDownRefresh
function preventPullToRefresh(element) {
    var prevent = false;

    document.querySelector(element).addEventListener('touchstart', function(e){
      if (e.touches.length !== 1) { return; }

      var scrollY = window.pageYOffset || document.body.scrollTop || document.documentElement.scrollTop;
      prevent = (scrollY === 0);
    });

    document.querySelector(element).addEventListener('touchmove', function(e){
      if (prevent) {
        prevent = false;
        e.preventDefault();
      }
    }, { passive: false });
  }

if (navigator.userAgent.toLowerCase().indexOf('chrome') > -1) {
  preventPullToRefresh('#body-view-student')
}

new Vue({
  render: h => h(ViewStudent),
}).$mount('#view-student')
