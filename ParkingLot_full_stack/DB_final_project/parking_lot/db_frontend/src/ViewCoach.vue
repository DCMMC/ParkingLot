<template>
  <v-app>
    <BooomHeader>
    </BooomHeader>
    <v-dialog
      v-model="loading" 
      persistent
      max-width="200"
      transition="dialog-transition"
    >
      <v-card>
      <v-container justify-center>
        <v-card-title class="headline">正在加载</v-card-title>
        <v-card-text>
        <v-progress-circular
          indeterminate
          color="purple"
        ></v-progress-circular>
      </v-card-text>
      </v-container>
    </v-card>
    </v-dialog>
    <v-dialog v-model="query_res" fullscreen hide-overlay transition="dialog-bottom-transition">
      <!-- <v-container justify-center> -->
        <v-layout row>
          <v-flex>
            <v-dialog
              v-model="edit_dialog" 
              persistent
              max-width="300"
              transition="dialog-transition">
                <v-card>
                <v-container justify-center>
                  <v-card-title class="headline">{{edit_title}}</v-card-title>
                  <v-card-text>
                    {{edit_msg}}
                </v-card-text>
                <v-card-actions>
                  <v-btn color="green darken-1" flat @click="edit(false)">取消</v-btn>
                  <v-spacer></v-spacer>
                  <v-btn color="green darken-1" flat @click="edit(true)">确认</v-btn>
                </v-card-actions>
                </v-container>
              </v-card>
            </v-dialog>
            <!-- <v-container justify-center> -->
              <v-img
                :src="headphoto"
                max-height="500px"
                contain
                class="grey"
              >
                <v-layout
                  column
                  fill-height
                >
                  <v-card-title>
                    <v-btn dark round large color="primary" @click.native="query_res = false">
                      <v-icon clss="">chevron_left</v-icon>
                      返回
                    </v-btn>

                    <v-spacer></v-spacer>

                    <v-btn dark class="mr-3" color="pink" large @click.native="confirm()">
                      <v-icon class="">edit</v-icon>
                      提交修改
                    </v-btn>
                  </v-card-title>
                </v-layout>
              </v-img>
              <v-layout row style="background-color: white">
                <v-flex xs10 offset-xs1>
                  <v-card>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>头像</v-subheader>
                      <file-pond
                        style="padding: 0px 24px;"
                        name="headphoto"
                        ref="pond"
                        label-idle="点击选择文件或者把头像文件拖到这里"
                        allow-multiple="false"
                        accepted-file-types="image/jpeg, image/png"
                        allowImageResize="true"
                        imageResizeUpscale="false"
                        imageResizeTargetWidth="600"
                        max-files="1" />
                    </v-list>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>姓名</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="name"
                      v-validate="'required|max:10'"
                      :error-messages="errors.collect('name')"
                      data-vv-name="name"
                      label="姓名"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>NFC 卡号</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="cardId"
                      v-validate="'required'"
                      :error-messages="errors.collect('card')"
                      data-vv-name="card"
                      label="NFC卡号"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>手机号</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="mobile"
                      v-validate="'required|digits:11'"
                      :error-messages="errors.collect('mobile')"
                      data-vv-name="mobile"
                      label="手机号"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>密码</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="password"
                      v-validate="{required: true, regex: /^[0-9a-zA-Z]{6,16}$/}"
                      :error-messages="errors.collect('password')"
                      label="密码"
                      data-vv-name="password"
                      required
                    ></v-text-field>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="password_confirm"
                      v-validate="{required: true, confirmed:password, regex: /^[0-9a-zA-Z]{6,16}$/}"
                      :error-messages="errors.collect('password_confirmation')"
                      data-vv-as="password"
                      data-vv-name="password_confirmation"
                      label="确认密码"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>性别</v-subheader>
                    </v-list>
                    <v-select
                      style="padding: 0px 24px;"
                      v-validate="'required'"
                      :items="['男', '女']"
                      v-model="sex"
                      :error-messages="errors.collect('select_sex')"
                      label="性别"
                      data-vv-name="select_sex"
                      required
                    ></v-select>
                  </v-card>
                </v-flex>
              </v-layout>
            <!-- </v-container> -->
            <b></b>
            <BooomFooter/>
          </v-flex>
        </v-layout>
      <!-- </v-container> -->
    </v-dialog>
    <v-dialog v-model="err_dialog" scrollable persistent max-width="600">
      <v-card>
        <v-card-title class="headline">错误</v-card-title>
        <v-card-text>{{msg}}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click.native="err_dialog = false">了解</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-content v-if="query_res == false">
      <v-container justify-center>
        <v-layout row >
          <v-flex>
          <div class="headline">查看教练信息</div>
          <v-select
              v-validate="'required'"
              :items="['NFC卡号', '手机号']"
              v-model="type"
              :error-messages="errors.collect('select')"
              label="查询方式"
              data-vv-name="select"
              required
            ></v-select>
            <v-text-field
                v-model="number"
                v-validate="'required|decimal:0'"
                :error-messages="errors.collect('number')"
                data-vv-name="number"
                label="NFC 卡号/手机号"
                required
              ></v-text-field>
            <v-btn @click="submit">确认</v-btn>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <BooomFooter/>
  </v-app>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import VeeValidate from 'vee-validate'
import BooomFooter from './components/footer'
import BooomHeader from './components/header'
import vueFilePond from 'vue-filepond';
import 'filepond/dist/filepond.min.css';
import 'filepond-plugin-image-preview/dist/filepond-plugin-image-preview.min.css';
import FilePondPluginFileValidateType from 'filepond-plugin-file-validate-type';
import FilePondPluginImagePreview from 'filepond-plugin-image-preview';
import FilePondPluginImageResize from 'filepond-plugin-image-resize';
const FilePond = vueFilePond(FilePondPluginFileValidateType, FilePondPluginImagePreview, FilePondPluginImageResize);
Vue.use(VeeValidate)

export default {
  name: 'ViewCoach',
  $_veeValidate: {
      validator: 'new'
  },
  components: {
    BooomFooter,
    FilePond,
    BooomHeader
  },
  data: () => ({
      type: '',
      number: '',
      name: '',
      mobile: '',
      origin_mobile: '',
      cardId: '',
      origin_cardId: '',
      sex: '',
      password: '',
      password_confirm: '',
      query_res: false,
      msg: '',
      err_dialog: false,
      loading: false,
      edit_dialog: false,
      edit_msg: '',
      edit_title: '',
      headphoto: '',
      dictionary: {
        attributes: {
        },
        custom: {
          select: {
            required: () => '请选择查询方式'
          },
          number: {
            required: () => '请输入手机号/ NFC 卡号',
            digits: () => '请输入 11 位手机号'
          },
          name: {
            required: () => '名字不能为空',
            max: '名字不能多于 10 个字符'
          },
          mobile: {
            required: () => '请输入手机号',
          },
          select_sex: {
            required: () => '请选择性别'
          },
          card: {
            required: () => '请输出NFC卡号'
          },
          password: {
            required: () => '请输入密码',
            regex: () => '请输入 6~16 位数字和大/小写英文字母组成的密码'
          },
          password_confirmation: {
            required: () => '不能为空',
            confirmed: () => '请重复输入密码',
            regex: () => '请输入 6~16 位数字和大/小写英文字母组成的密码'
          }
        }
      }
  }),
  mounted () {
      this.$validator.localize('zh_cn', this.dictionary)
  },
  methods: {
    submit () {
      Promise.all([
        this.$validator.validate('select'),
        this.$validator.validate('number')
      ]).then( (res) => {
        var areValid = true;
        res.forEach(function (a) {
          if (a == false) {
            areValid = false
          }
        })
        if (areValid) {
          this.loading = true
          var data = {'target': 'coach'}
          if (this.type == 'NFC卡号') {
            data.type = 'cardId'
            data.cardId = this.number
          } else if (this.type == '手机号') {
            data.type = 'mobile'
            data.mobile = this.number
          }
          axios.post('/query', data).then((res) => {
            if (res.data.code > 0) {
              this.loading = false
              this.msg = res.data.msg
              console.log('err' + res.data.msg)
              this.err_dialog = true
            } else {
              this.loading = false
              this.name = res.data.data.name
              this.mobile = res.data.data.mobile
              this.origin_mobile = this.mobile
              this.cardId = res.data.data.cardId
              this.origin_cardId = this.cardId
              this.headphoto = res.data.data.headphoto
              this.password = res.data.data.password
              this.password_confirm = res.data.data.password
              if (res.data.data.sex == true) {
                this.sex = '男'
              } else {
                this.sex = '女'
              }
              this.query_res = true
            }
          }).catch(error => {
            this.loading = false
            this.msg = error
            console.log('error: ' + error)
            this.err_dialog = true
          });
        }
      })
    },
    confirm() {
      if (confirm) {
        this.edit_dialog = false
        Promise.all([
          this.$validator.validate('name'),
          this.$validator.validate('mobile'),
          this.$validator.validate('card'),
          this.$validator.validate('select_sex'),
          this.$validator.validate('password'),
          this.$validator.validate('password_confirmation'),
        ]).then( (res) => {
          var areValid = true;
          res.forEach(function (a) {
            if (a == false) {
              areValid = false
            }
          })
          if (areValid) {
            this.edit_title = '确认'
            this.edit_msg = '是否确认更新教练信息?'
            this.edit_dialog = true
          }
        })
      }
    },
    edit(confirm) {
      if (this.edit_title == '成功' || this.edit_title == '失败') {
        this.edit_dialog = false
        return
      }
      if (confirm) {
        this.edit_dialog = false
        if (this.sex === '男') {
          this.sex = true
        } else if (this.sex === '女') {
          this.sex = false
        }
        const formData = new FormData();
        if (this.$refs.pond.getFiles().length > 0) {
          const file = this.$refs.pond.getFile()
          formData.append('headphoto', file.file, this.mobile + '.' + file.fileExtension)
        } else {
          console.log('no headphoto')
        }
        formData.append('target', 'coach')
        formData.append('name', this.name)
        formData.append('sex', this.sex)
        formData.append('cardId', this.cardId)
        formData.append('mobile', this.mobile)
        formData.append('update', true)
        formData.append('password', this.password)
        formData.append('origin_cardId', this.origin_cardId)
        formData.append('origin_mobile', this.origin_mobile)
        axios.post('/addData', formData, { headers: 
          { 'Content-Type': 'multipart/form-data' } 
        }).then((response) => {
          // Success
          this.edit_msg = response.data["msg"]
          if (parseInt(response.data["code"]) > 0) {
            this.edit_title = '失败'
          } else {
            this.edit_title = '成功'
          }
          this.edit_dialog = true
          this.query_res = false
        }).catch((response) => {
            // Error
            console.log('errors: ' + response)
            this.edit_msg = response.data
            this.edit_title = '错误'
            this.edit_dialog = true
        });
      } else {
        this.edit_dialog = false
      }
    }
  }
}
</script>
