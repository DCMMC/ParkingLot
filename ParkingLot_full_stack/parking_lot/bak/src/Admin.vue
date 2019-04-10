<template>
  <v-app>
    <Header/>
    <Footer/>
  </v-app>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import Footer from './components/footer'
import Header from './components/header'

export default {
  name: 'Admin',
  components: {
    Footer,
    Header
  },
  data: () => ({
  }),
  mounted () {
  },
  methods: {
  }
}
</script>