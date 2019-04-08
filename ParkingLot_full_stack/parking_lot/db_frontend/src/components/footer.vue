<template>
  <v-footer
      height="auto"
      color="primary lighten-1"
      style="padding-top: 50px;"
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
    data () {
      return {
          links: [
            ['首页', '/'],
            ['关于我们', '/404/404.html'],
            ['查看学员信息', '/view-student.html'],
            ['查看教练信息', '/view-coach.html'],
            ['添加学员信息', '/add-student.html'],
            ['添加教练信息', '/add-coach.html']
          ],
        }
      }
    }
</script>