/*
eslint no-param-reassign: ["error", { "props": true, "ignorePropertyModificationsFor": ["state"] }]
*/

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    paginationPage: 1,
    searchParameters: null,
    searchResult: null,
  },
  actions: {
    getSearchQueryParameters(state) {
      return state.searchParameters;
    },
  },
  mutations: {
    nextPage(state) {
      state.paginationPage += 1;
    },
    previousPage(state) {
      state.paginationPage -= 1;
    },
    setPage(state, pageNumber) {
      state.paginationPage = pageNumber;
    },
    resetSearch(state) {
      state.paginationPage = 1;
      state.searchParameters = null;
      state.searchResult = null;
    },
  },
});
