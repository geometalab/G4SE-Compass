import Vue from 'vue'
import App from './App.vue'

let VueResource = require('vue-resource');

Vue.use(VueResource);

new Vue({
  el: '#app',
  render: h => h(App)
})
