/*
eslint no-param-reassign: ["error", { "props": true, "ignorePropertyModificationsFor": ["state"] }]
*/

import Vue from 'vue';
import Vuex from 'vuex';
import search from './api/search';

Vue.use(Vuex);

export default new Vuex.Store({
  modules: {
    search,
  },
  strict: true,
});
