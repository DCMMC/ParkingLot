<template>
  <v-toolbar app color="teal">
      <v-toolbar-title class="title">
        <span>Demo</span>
        <span> 数据库管理</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
        href="/logout_handler"
      >
        <span class="title">退出登录</span>
      </v-btn>
    </v-toolbar>
</template>

<script>
  export default {
    data () {
      return {
        }
      }
    }
</script>