<template>
  <v-container justify-center>
    <v-layout
      row
    >
      <v-flex>
        <v-list two-line subheader>
            <v-subheader inset>管理</v-subheader>
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

            <v-subheader inset>查看</v-subheader>

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

            <v-subheader inset>Debug</v-subheader>
            <v-form v-model="valid">
              <v-text-field
                v-model="debug_url"
                label="Debug url (start with /)"
                :rules="[(v => !!v && v[0] === '/') || 'debug url 不合法']"
                required
              ></v-text-field>
              <v-text-field
                v-model="debug_data"
                label="Debug data (Json format)"
                :rules="[(v => !!v && isJson(v)) || 'debug data 不合法']"
                required
              ></v-text-field>
              <v-select
                v-model="select_req"
                :items="req_type"
                :rules="[v => !!v || '请选择请求类型']"
                label="请求类型"
                required
              ></v-select>
              <v-btn :disabled="!valid" @click="submit">提交请求</v-btn>
            </v-form>
        </v-list>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'
  var qs = require('qs')

  export default {
    data: () => ({
      valid: false,
      debug_data: '',
      debug_url: '',
      select_req: null,
      req_type: [
        'post',
        'get',
        'post with urlencoded'
      ],
      items_manage: [
        { icon: 'assignment', iconClass: 'blue white--text', title: '添加学员数据', subtitle: '新增学员信息',
          url: '/add-student.html' },
        { icon: 'call_to_action', iconClass: 'amber white--text', title: '添加教练数据', subtitle: '新增教练信息',
          url: '/add-coach.html' }
      ],
      items_view: [
        { icon: 'assignment', iconClass: 'blue white--text', title: '查看学员数据', subtitle: '查看并且修改教练数据',
          url: '/view-student.html' },
        { icon: 'call_to_action', iconClass: 'amber white--text', title: '查看教练数据', subtitle: '查看并且修改学员数据',
          url: '/view-coach.html' }
      ]
    }),
    methods: {
      isJson (str) {
          try {
              JSON.parse(str);
          } catch (e) {
              return false;
          }
          return true;
      },
      goto (item) {
        window.location.href=item.url;
      },
      submit () {
        if (this.select_req === 'post') {
          var formData = JSON.parse(this.debug_data)
          axios.post(this.debug_url, formData, {
            headers: {}
          }).then((response) => {
            // Success
            console.log('Success POST: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          }).catch((response) => {
            // Error
            console.log('Failed POST: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          });
        } else if (this.select_req === 'get') {
          var formData = JSON.parse(this.debug_data)
          axios.get(this.debug_url, {params: formData}, {
            headers: {}
          }).then((response) => {
            // Success
            console.log('Success GET: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          }).catch((response) => {
            // Error
            console.log('Failed GET: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          });
        } else if (this.select_req === 'post with urlencoded') {
          var formData = JSON.parse(this.debug_data)
          axios.post(this.debug_url, qs.stringify(formData), {
            headers: {
              'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
            }
          }).then((response) => {
            // Success
            console.log('Success POST: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          }).catch((response) => {
            // Error
            console.log('Failed POST: ' + this.debug_url + ' with ' + this.debug_data
              + ', response: ' + response.data)
          });
        }
      }
    }
  }
</script>

<style>

</style>
