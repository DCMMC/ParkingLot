<template>
<v-container justify-center>
    <v-layout row>
      <v-flex>
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
	  </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import axios from 'axios'
var qs = require('qs')

export default {
	name: 'Debug',
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
		submit () {
		    if (this.select_req === 'post') {
		    	var formData = JSON.parse(this.debug_data)
		    	axios.post(this.debug_url, formData, {
		    		headers: {}
		    	}).then((response) => {
		    		// Success
					console.log('Success POST: ' + this.debug_url
						+ ' with ' + this.debug_data
						+ ', response: ' + response.data)
				}).catch((response) => {
					// Error
		        	console.log('Failed POST: ' + this.debug_url
		        		+ ' with ' + this.debug_data
		        		+ ', response: ' + response.data)
				});
		    } else if (this.select_req === 'get') {
		    	var formData = JSON.parse(this.debug_data)
		    	axios.get(this.debug_url, {params: formData}, {
		    		headers: {}
		    	}).then((response) => {
					// Success
					console.log('Success GET: ' + this.debug_url + ' with '
						+ this.debug_data + ', response: ' + response.data)
				}).catch((response) => {
					// Error
					console.log('Failed GET: ' + this.debug_url + ' with '
		        		+ this.debug_data + ', response: ' + response.data)
				});
			} else if (this.select_req === 'post with urlencoded') {
				var formData = JSON.parse(this.debug_data)
				axios.post(this.debug_url, qs.stringify(formData), {
					headers: {
						'content-type': 'application/x-www-form-urlencoded;charset=utf-8'
		      		}
				}).then((response) => {
		        	// Success
		        	console.log('Success POST: ' + this.debug_url + ' with '
		        		+ this.debug_data + ', response: ' + response.data)
				}).catch((response) => {
		        	// Error
					console.log('Failed POST: ' + this.debug_url + ' with ' + 
						this.debug_data + ', response: ' + response.data)
				});
			}
		}
	}
}
</script>

<style>
</style>