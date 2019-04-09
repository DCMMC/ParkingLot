<template>
  <v-container justify-center>
    <v-layout
      row
    >
      <v-flex>
        <v-list two-line subheader>
            <v-subheader inset class="headline">客户视图</v-subheader>
            <v-list-tile
              v-for="item in items_manage"
              :key="item.title"
              avatar
              @click="goto(item)"
            >
              <v-list-tile-avatar>
                <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
              </v-list-tile-content>

              <v-list-tile-action>
                <v-btn icon ripple>
                  <v-icon color="grey lighten-1">info</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>

            <v-divider inset></v-divider>

            <v-subheader inset class="headline">管理员视图</v-subheader>

            <v-list-tile
              v-for="item in items_view"
              :key="item.title"
              avatar
              @click="goto(item)"
            >
              <v-list-tile-avatar>
                <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
              </v-list-tile-avatar>

              <v-list-tile-content>
                <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
              </v-list-tile-content>

              <v-list-tile-action>
                <v-btn icon ripple>
                  <v-icon color="grey lighten-1">info</v-icon>
                </v-btn>
              </v-list-tile-action>
            </v-list-tile>

            <v-subheader inset class="headline">Debug</v-subheader>
            <Debug/>
        </v-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import Debug from './Debug'

export default {
  name: 'SelectView',
  components: {
    Debug,
  },
  data: () => ({
    items_manage: [
      { icon: 'assignment', iconClass: 'blue white--text', title: '客户界面 -- 入口', subtitle: '停车场入口处展现给客户的界面',
        url: '/client-indoor.html' },
      { icon: 'call_to_action', iconClass: 'amber white--text', title: '客户界面 -- 出口', subtitle: '停车场出口处展现给客户的界面',
        url: '/client-outdoor.html' }
    ],
    items_view: [
      { icon: 'assignment', iconClass: 'blue white--text', title: '管理员界面', subtitle: '管理员界面用于查看车库实时信息和历史记录, 需要登录',
        url: '/admin.html' },
    ]
  }),
  methods: {
    goto (item) {
      window.location.href=item.url;
    }
  }
}
</script>

<style>

</style>
