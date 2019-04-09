<template>
  <v-footer
      height="auto"
      color="primary lighten-1"
    >
    <v-layout
      justify-center
      row
      wrap
    >
      <v-btn
        v-for="link in links"
        :key="link[0]"
        color="white"
        flat
        round
        :href="link[1]"
      >
        {{ link[0] }}
      </v-btn>
      <v-flex
        primary
        lighten-2
        py-3
        text-xs-center
        white--text
        xs12
      >
        &copy;2018 — <strong>DCMMC</strong>
      </v-flex>
    </v-layout>
  </v-footer>
</template>

<script>
  export default {
    name: 'Footer',
    data () {
      return {
          links: [
            ['首页', '/'],
            ['关于我们', '/404/404.html'],
            ['入口界面', '/client-indoor.html'],
            ['出口界面', '/client-outdoor.html'],
            ['管理员界面', '/admin.html']
          ],
        }
      }
    }
</script>