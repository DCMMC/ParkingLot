<template>
  <v-app>
    <Header />
    <v-content>
      <v-container fluid grid-list-md style="padding: 4px;">
        <v-layout row wrap style="height: 700px; width: 100%;">
          <v-flex d-flex shrink style="width: 20%; height: 100%;">
            <v-card color="purple" dark hover ripple>
              <v-card-title primary class="display-1">推荐停车位</v-card-title>
              <!-- <v-card-text class="title">
                TODO: 使用 expansion panels
              </v-card-text> -->
              <v-card-actions>
                <v-expansion-panel v-model="panel" expand light>
                  <v-expansion-panel-content
                    v-for="(item,i) in 2"
                    :key="i"
                  >
                    <template v-slot:header>
                      <div class="headline">一楼一区</div>
                    </template>
                    <vue-custom-scrollbar
                      id="emptyLot"
                      class="scroll-area"
                      :settings="settings"
                    >
                      <ul>
                        <li
                          v-for="(item,i) in 20"
                          :key="i"
                          class="headline"
                          style="display: flex; justify-content: center;"
                        >
                          {{ i }}
                        </li>
                      </ul>
                    </vue-custom-scrollbar>
                  </v-expansion-panel-content>
                </v-expansion-panel>
              </v-card-actions>
            </v-card>
          </v-flex>
          <v-flex d-flex shrink style="width: 80%;">
            <v-layout column wrap>
              <v-flex d-flex style="height: 70%;">
                <ParkingLotMap />
              </v-flex>
              <v-flex d-flex style="height: 30%;">
                <v-card
                  color="red lighten-2"
                  dark
                  hover
                  ripple
                >
                  <v-card-text class="display-1">TODO: 欢迎您! 沪A 12345</v-card-text>
                </v-card>
              </v-flex>
            </v-layout>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
    <Footer />
  </v-app>
</template>

<script>
// import Vue from 'vue'
// import axios from 'axios'
import Footer from './components/footer'
import Header from './components/header'
import ParkingLotMap from './components/ParkingLotMap'
import vueCustomScrollbar from 'vue-custom-scrollbar'

export default {
  name: 'ClientIndor',
  components: {
    Footer,
    ParkingLotMap,
    Header,
    vueCustomScrollbar
  },
  data: () => ({
    panel: [],
    items: 2,
    settings: {
      maxScrollbarLength: 60
    },
    scrollTop: 250
  }),
  mounted() {
    // 全部展开
    this.panel = [...Array(this.items).keys()].map(_ => true)
    // TODO: 使用 scrollTop 自动滚动
    var node = document.getElementById('emptyLot')
    setTimeout(() => { node.scrollTop = 200; console.log('set scrollTopr') }, 5000)
  },
  methods: {
    scrollHanle(evt) {
      console.log(evt)
    }
  }
}
</script>

<style>
.scroll-area {
   height: 200px;
}
ul,li {
  list-style: none;
}
</style>
