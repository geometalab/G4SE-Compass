<template>
  <div id="app">
    <app-header></app-header>
      <app-search></app-search>
  </div>
</template>

<script>

import AppHeader from './components/AppHeader.vue'
import AppSearch from './components/AppSearch.vue'

export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  components: {
    AppHeader,
    AppSearch,
  }
}
</script>
