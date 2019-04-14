<template>
  <v-toolbar app color="teal" dense>
    <v-toolbar-title class="title">
      <span>停车场管理系统</span>
    </v-toolbar-title>
    <v-spacer />
    <screenfull id="screenfull" class="right-menu-item hover-effect" />
  </v-toolbar>
</template>

<script>
import Screenfull from '@/components/Screenfull'
export default {
  name: 'Header',
  components: {
    Screenfull
  },
  data() {
    return {
    }
  }
}
</script>

<style lang="scss" scoped>
.right-menu-item {
    display: inline-block;
    padding: 8px;
    height: 100%;
    font-size: 18px;
    color: #5a5e66;
    vertical-align: text-bottom;

    &.hover-effect {
      cursor: pointer;
      transition: background .3s;

      &:hover {
        background: rgba(0, 0, 0, .025)
      }
    }
  }
</style>
