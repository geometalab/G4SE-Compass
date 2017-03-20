/*
eslint no-param-reassign: ["error", { "props": true, "ignorePropertyModificationsFor": ["state"] }]
*/

import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    paginationPage: 1,
    searchParameters: {},
    searchResults: null,
    searchError: null,
    searchInProgress: false,
  },
  actions: {
    resetSearch({ commit }) {
      commit('resetSearch');
    },
  },
  mutations: {
    searchRunning(state) {
      state.searchInProgress = true;
    },
    searchDone(state) {
      state.searchInProgress = false;
    },
    previousPage(state) {
      state.paginationPage -= 1;
      state.searchParameters.page = state.paginationPage;
    },
    nextPage(state) {
      state.paginationPage += 1;
      state.searchParameters.page = state.paginationPage;
    },
    setPage(state, pageNumber) {
      state.paginationPage = pageNumber;
      state.searchParameters.page = pageNumber;
    },
    resetSearch(state) {
      state.paginationPage = 1;
      state.searchParameters = {};
      state.searchResults = null;
    },
    setSearchParameters(state, parameters) {
      // if (this.from_year) {
      //   query.from_year = this.from_year;
      // }
      // if (this.to_year) {
      //   query.to_year = this.to_year;
      // }
      // if (this.is_latest) {
      //   query.is_latest = this.is_latest;
      // }
      state.searchParameters = Object.assign(parameters, {
        // DEFAULT PARAMETERS
        page_size: 10,
        page: state.paginationPage,
        // language: this.getUserLanguage(),
        // ordering: this.ordering,
        // limit: 10,
      });
    },
    setSearchResults(state, results, errors) {
      state.searchResults = results;
      state.searchError = errors;
    },
  },
  getters: {
    getSearchParameters(state) {
      return state.searchParameters;
    },
  },
  strict: true,
});
