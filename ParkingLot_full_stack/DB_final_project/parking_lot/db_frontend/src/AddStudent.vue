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
    <v-dialog v-model="dialog_msg" scrollable persistent max-width="400">
      <v-card>
        <v-card-title class="headline">{{status}}</v-card-title>
        <v-card-text>{{msg}}</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" flat @click.native="dialog_msg = false">了解</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-content>
      <v-container justify-center>
        <v-layout row>
          <v-flex>
            <div class="headline">添加学员信息</div>
            <v-form>
              <v-text-field
                v-model="name"
                v-validate="'required|max:10'"
                :error-messages="errors.collect('name')"
                data-vv-name="name"
                label="姓名"
                required
              ></v-text-field>
              <v-text-field
                v-model="cardId"
                v-validate="'required'"
                :error-messages="errors.collect('card')"
                data-vv-name="card"
                label="NFC卡号"
                required
              ></v-text-field>
              <v-text-field
                v-model="mobile"
                v-validate="'required|digits:11'"
                :error-messages="errors.collect('mobile')"
                data-vv-name="mobile"
                label="手机号"
                required
              ></v-text-field>
              <v-text-field
                v-model="password"
                v-validate="{required: true, regex: /^[0-9a-zA-Z]{6,16}$/}"
                :error-messages="errors.collect('password')"
                label="密码"
                data-vv-name="password"
                required
              ></v-text-field>
              <v-text-field
                v-model="password_confirm"
                v-validate="{required: true, confirmed:password, regex: /^[0-9a-zA-Z]{6,16}$/}"
                :error-messages="errors.collect('password_confirmation')"
                data-vv-as="password"
                data-vv-name="password_confirmation"
                label="确认密码"
                required
              ></v-text-field>
              <v-text-field
                v-model="f1"
                v-validate="'required|between:1,80'"
                :error-messages="errors.collect('f1')"
                data-vv-name="f1"
                label="高位下拉力( 1 ~ 80 千克)"
                required
              ></v-text-field>
              <v-text-field
                v-model="x1"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('x1')"
                data-vv-name="x1"
                label="高位下拉起始高度( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="xmax"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('xmax')"
                data-vv-name="xmax"
                label="深蹲最高点( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="xmin"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('xmin')"
                data-vv-name="xmin"
                label="深蹲最低点( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="f2"
                v-validate="'required|between:1,80'"
                :error-messages="errors.collect('f2')"
                data-vv-name="f2"
                label="深蹲力( 1 ~ 80 千克)"
                required
              ></v-text-field>
              <v-text-field
                v-model="x2"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('x2')"
                data-vv-name="x2"
                label="深蹲起始高度( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="f3"
                v-validate="'required|between:1,80'"
                :error-messages="errors.collect('f3')"
                data-vv-name="f3"
                label="硬拉力( 1 ~ 80 千克)"
                required
              ></v-text-field>
              <v-text-field
                v-model="x3"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('x3')"
                data-vv-name="x3"
                label="硬拉起始高度( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="f4"
                v-validate="'required|between:1,80'"
                :error-messages="errors.collect('f4')"
                data-vv-name="f4"
                label="直立划船力( 1 ~ 80 千克)"
                required
              ></v-text-field>
              <v-text-field
                v-model="x4"
                v-validate="'required|between:30,180'"
                :error-messages="errors.collect('x4')"
                data-vv-name="x4"
                label="直立划船起始高度( 30 ~ 180 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="height"
                v-validate="'required|between:50,230'"
                :error-messages="errors.collect('height')"
                data-vv-name="height"
                label="身高( 50 ~ 230 厘米)"
                required
              ></v-text-field>
              <v-text-field
                v-model="weight"
                v-validate="'required|between:1,300'"
                :error-messages="errors.collect('weight')"
                data-vv-name="weight"
                label="体重( 1 ~ 300 千克)"
                required
              ></v-text-field>
              <v-select
                v-validate="'required'"
                :items="['男', '女']"
                v-model="sex"
                :error-messages="errors.collect('select')"
                label="性别"
                data-vv-name="select"
                required
              ></v-select>
              <file-pond
                name="headphoto"
                ref="pond"
                label-idle="点击选择文件或者把头像文件拖到这里"
                allow-multiple="false"
                accepted-file-types="image/jpeg, image/png"
                allowImageResize="true"
                imageResizeUpscale="false"
                imageResizeTargetWidth="600"
                max-files="1"
                />
              <v-btn @click="submit">确认</v-btn>
              <v-btn @click="clear">清除</v-btn>
            </v-form>
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
  name: 'AddCoach',
  $_veeValidate: {
      validator: 'new'
  },
  components: {
      BooomFooter,
      FilePond,
      BooomHeader
  },
  data: () => ({
      name: '',
      mobile: '',
      sex: '',
      cardId: '',
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
      headphoto_file: [],
      dialog_msg: false,
      loading: false,
      msg: '',
      status: '',
      dictionary: {
        attributes: {
        },
        custom: {
          name: {
            required: () => '名字不能为空',
            max: '名字不能多于 10 个字符'
          },
          mobile: {
            required: () => '请输入手机号',
            digits: () => '请输入 11 位手机号'
          },
          select: {
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
        this.$validator.validateAll().then(res => {
          if (res) {
            this.loading = true
            if (this.sex === '男') {
              this.sex = 'male'
            } else if (this.sex === '女') {
              this.sex = 'female'
            }
            const formData = new FormData();
            this.headphoto_file = this.$refs.pond.getFiles()
            if (this.headphoto_file.length > 0) {
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
            formData.append('update', false)
            formData.append('password', this.password)
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
            axios.post('/addData', formData, { headers: { 'Content-Type': 'multipart/form-data' } }).then((response) => {
                this.loading = false
                // Success
                this.msg = response.data["msg"]
                if (parseInt(response.data["code"]) > 0) {
                  this.status = '失败'
                } else {
                  this.status = '成功'
                }
                this.dialog_msg = true
              }
            ).catch((response) => {
                  this.loading = false
                  this.msg = response
                  this.status = '错误'
                  // Error
                  console.log('errors')
                  this.dialog_msg = true
              })
          }
        })
      },
      clear () {
        this.name = ''
        this.mobile = ''
        this.sex = ''
        this.cardId = ''
        this.password = ''
        this.password_confirm = ''
        this.$validator.reset()
      }
    }
}
</script>
