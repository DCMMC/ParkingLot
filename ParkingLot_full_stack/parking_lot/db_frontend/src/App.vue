<template>
  <v-app>
    <v-toolbar app color="primary">
      <v-toolbar-title class="title white--text">
        <span>停车场管理系统 -- 导航页</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        v-if="logged"
        flat
        href="/logout_handler"
      >
        <span class="title">退出登录</span>
      </v-btn>
      <v-btn
        v-else
        flat
        href="/login/index.html">
        <span class="title">登录</span>
      </v-btn>
    </v-toolbar>
    <v-content>
      <SelectView/>
    </v-content>
    <Footer/>
  </v-app>
</template>

<script>
import SelectView from './components/SelectView'
import Footer from './components/footer'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    SelectView,
    Footer
  },
  data() {
    return {
      logged: false
    }
  },
  // here is code that should be done first before vue render all data
  mounted: function () {
    axios.get('/log_state').then(res => {
      this.logged = res.data.result  
    })
  }
}
</script>
