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
                      <v-subheader>高位下拉力</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="f1"
                      v-validate="'required|between:1,80'"
                      :error-messages="errors.collect('f1')"
                      data-vv-name="f1"
                      label="高位下拉力( 1 ~ 80 千克)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>高位下拉起始高度</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="x1"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('x1')"
                      data-vv-name="x1"
                      label="高位下拉起始高度( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>深蹲最高点</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="xmax"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('xmax')"
                      data-vv-name="xmax"
                      label="深蹲最高点( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>深蹲最低点</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="xmin"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('xmin')"
                      data-vv-name="xmin"
                      label="深蹲最低点( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>深蹲力</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="f2"
                      v-validate="'required|between:1,80'"
                      :error-messages="errors.collect('f2')"
                      data-vv-name="f2"
                      label="深蹲力( 1 ~ 80 千克)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>深蹲起始高度</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="x2"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('x2')"
                      data-vv-name="x2"
                      label="深蹲起始高度( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>硬拉力</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="f3"
                      v-validate="'required|between:1,80'"
                      :error-messages="errors.collect('f3')"
                      data-vv-name="f3"
                      label="硬拉力( 1 ~ 80 千克)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>硬拉起始高度</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="x3"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('x3')"
                      data-vv-name="x3"
                      label="硬拉起始高度( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>直立划船力</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="f4"
                      v-validate="'required|between:1,80'"
                      :error-messages="errors.collect('f4')"
                      data-vv-name="f4"
                      label="直立划船力( 1 ~ 80 千克)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>直立划船起始高度</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="x4"
                      v-validate="'required|between:30,180'"
                      :error-messages="errors.collect('x4')"
                      data-vv-name="x4"
                      label="直立划船起始高度( 30 ~ 180 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>身高</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="height"
                      v-validate="'required|between:50,230'"
                      :error-messages="errors.collect('height')"
                      data-vv-name="height"
                      label="身高( 50 ~ 230 厘米)"
                      required
                    ></v-text-field>
                    <v-divider inset></v-divider>
                    <v-list subheader>
                      <v-subheader>体重</v-subheader>
                    </v-list>
                    <v-text-field
                      style="padding: 0px 24px;"
                      v-model="weight"
                      v-validate="'required|between:1,300'"
                      :error-messages="errors.collect('weight')"
                      data-vv-name="weight"
                      label="体重( 1 ~ 300 千克)"
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
          <div class="headline">查看学员信息</div>
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
  name: 'ViewStudent',
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
      height: '',
      weight: '',
      f1: '', // 高位下拉力
      x1: '', // 高位下拉起始高度
      f2: '', // 深蹲力
      x2: '', // 深蹲起始高度
      xmax: '', // 深蹲最高点
      xmin: '', // 深蹲最低点
      f3: '', // 硬拉力
      x3: '', //硬拉起始高度
      f4: '', // 直立划船力
      x4: '', // 直立划船起始高度
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
          },
          f1: {
            required: () => '不能为空',
            between: () => '请输入 1 ~ 80 的值'
          },
          x1: {
            required: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          f2: {
            required: () => '不能为空',
            between: () => '请输入 1 ~ 80 的值'
          },
          x2: {
            required: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          f3: {
            required: () => '不能为空',
            between: () => '请输入 1 ~ 80 的值'
          },
          x3: {
            required: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          f4: {
            required: () => '不能为空',
            between: () => '请输入 1 ~ 80 的值'
          },
          x4: {
            required: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          xmin: {
            require: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          xmax: {
            require: () => '不能为空',
            between: () => '请输入 30 ~ 180 的值'
          },
          height: {
            require: () => '身高不能为空',
            between: () => '请输入 50 ~ 230 的值'
          },
          weight: {
            require: () => '体重不能为空',
            between: () => '请输入 1 ~ 300 的值'
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
          var data = {'target': 'student'}
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
              this.height = res.data.data.height
              this.weight = res.data.data.weight
              this.f1 = res.data.data.f1
              this.x1 = res.data.data.x1
              this.xmax = res.data.data.xmax
              this.xmin  = res.data.data.xmin
              this.f2 = res.data.data.f2
              this.x2 = res.data.data.x2
              this.f3 = res.data.data.f3
              this.x3 = res.data.data.x3
              this.f4 = res.data.data.f4
              this.x4 = res.data.data.x4
              if (res.data.data.sex == 'male') {
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
          this.sex = 'male'
        } else if (this.sex === '女') {
          this.sex = 'female'
        }
        const formData = new FormData();
        if (this.$refs.pond.getFiles().length > 0) {
          const file = this.$refs.pond.getFile()
          formData.append('headphoto', file.file, this.mobile + '.' + file.fileExtension)
        } else {
          console.log('no headphoto')
        }
        formData.append('target', 'student')
        formData.append('name', this.name)
        formData.append('sex', this.sex)
        formData.append('cardId', this.cardId)
        formData.append('mobile', this.mobile)
        formData.append('update', true)
        formData.append('password', this.password)
        formData.append('origin_cardId', this.origin_cardId)
        formData.append('origin_mobile', this.origin_mobile)
        formData.append('height', this.height)
        formData.append('weight', this.weight)
        formData.append('f1', this.f1)
        formData.append('x1', this.x1)
        formData.append('xmin', this.xmin)
        formData.append('xmax', this.xmax)
        formData.append('f2', this.f2)
        formData.append('x2', this.x2)
        formData.append('f3', this.f3)
        formData.append('x3', this.x3)
        formData.append('f4', this.f4)
        formData.append('x4', this.x4)
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