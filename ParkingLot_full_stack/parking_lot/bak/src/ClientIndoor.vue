<template>
  <v-app>
    <Header/>
    <v-content>
      <ParkingLotMap/>
    </v-content>
    <Footer/>
  </v-app>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import Footer from './components/footer'
import Header from './components/header'
import ParkingLotMap from './components/ParkingLotMap'

export default {
  name: 'ClientIndor',
  components: {
      Footer,
      ParkingLotMap,
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
