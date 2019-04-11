<template>
  <v-app>
    <Header>
    </Header>
    <v-content>
    <v-container fluid grid-list-md>
      <!-- <v-layout row style="height: 8%;">
        <v-flex d-flex> -->
          
        <!-- </v-flex>
      </v-layout> -->
      <v-layout row wrap style="height: 700px; width: 100%;">
        <v-flex d-flex shrink style="width: 20%; height: 100%;">
          <v-card color="purple" dark hover ripple>
            <v-card-title primary class="headline">TODO:</v-card-title>
            <v-card-text class="title">也许加点 Ads 吧...</v-card-text>
          </v-card>
        </v-flex>
        <v-flex d-flex shrink style="width: 80%;">
          <v-layout column wrap>
            <v-flex d-flex style="height: 70%;">
              <v-card color="blue" dark hover ripple>
                <v-card-title primary class="headline">TODO:</v-card-title>
                <v-card-text class="title">收费信息</v-card-text>
              </v-card>
            </v-flex>
            <v-flex d-flex style="height: 30%;">
              <v-card
                color="red lighten-2"
                dark
                hover
                ripple
              >
                <v-card-text class="headline">TODO: <br/> 一路顺风! 沪A 12345</v-card-text>
              </v-card>
            </v-flex>
          </v-layout>
        </v-flex>
      </v-layout>
    <!-- <v-content>
      <ParkingLotMap/>
    </v-content> -->
    </v-container>
  </v-content>
    <Footer>
    </Footer>
  </v-app>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import Footer from './components/footer'
import Header from './components/header'

export default {
  name: 'ClientOutdoor',
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
