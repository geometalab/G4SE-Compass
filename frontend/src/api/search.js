/*
 eslint no-param-reassign: ["error", { "props": true, "ignorePropertyModificationsFor": ["state"] }]
 */

import Vue from 'vue';

const search = {
  namespaced: true,
  state: {
    processing: false,
    results: null,
    errors: null,
    searchParameters: {
      page: 1,
    },
  },
  mutations: {
    updateResults(state, results, errors) {
      state.results = results;
      state.errors = errors;
    },
    updateSearchParameters(state, changedParameters) {
      state.searchParameters = Object.assign(state.searchParameters, changedParameters);
    },
    startProcessing(state) {
      state.processing = true;
    },
    endProcessing(state) {
      state.processing = false;
    },
    setPage(state, page) {
      state.searchParameters.page = page;
    },
    previousPage(state) {
      state.searchParameters.page -= 1;
    },
    nextPage(state) {
      state.searchParameters.page += 1;
    },
    reset(state) {
      state.processing = false;
      state.results = null;
      state.errors = null;
      state.searchParameters = {
        page: 1,
      };
    },
  },
  actions: {
    search({ state, commit, getters }) {
      const defaultSearchParameters = {
        page_size: getters.pageSize,
      };
      const queryParameters = Object.assign(
        state.searchParameters,
        defaultSearchParameters,
      );
      console.log('searching call: ', queryParameters);
      if (!queryParameters.search) {
        return;
      }
      commit('startProcessing');
      Vue.http.get('/api/search/', { params: queryParameters }, {
        before(request) {
          if (this.previousRequest) {
            this.previousRequest.abort();
          }
          this.previousRequest = request;
        },
      }).then((response) => {
        commit('updateResults', response.body, null);
      }, (response) => {
        commit('updateResults', null, response.body.detail);
      });
      commit('endProcessing');
    },
  },
  getters: {
    pageSize() {
      // return default size
      return 10;
    },
    maxPage(state, getters) {
      return Math.floor(state.results.count / getters.pageSize);
    },
    hasNextPage(state, getters) {
      return (state.searchParameters.page) < getters.maxPage;
    },
    hasPreviousPage(state) {
      return state.searchParameters.page > 1;
    },
    currentPage(state) {
      return state.searchParameters.page;
    },
    resultsTotal(state) {
      console.log('total: ', state.results.count);
      return state.results.count;
    },
    showingResultsFromToText(state, getters) {
      const totalResults = getters.resultsTotal;
      const previousPage = getters.currentPage - 1;
      const itemsPerPage = getters.pageSize;
      const itemsNumberStart = (previousPage * itemsPerPage) + 1;
      let itemsNumberEnd = getters.pageSize * getters.currentPage;
      if (!getters.hasNextPage) {
        itemsNumberEnd = totalResults;
      }
      return `Showing ${itemsNumberStart}-${itemsNumberEnd} of 
      total ${totalResults} results.`;
    },
  },
};
export { search as default };
