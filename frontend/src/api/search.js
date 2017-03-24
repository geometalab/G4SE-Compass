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
    language: null,
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
    setLanguage(state, language) {
      state.language = language;
    },
    setPublicationYears(state, yearList) {
      state.searchParameters.publication_year = yearList;
    },
    setDataSets(state, dataSetList) {
      state.searchParameters.dataset = dataSetList;
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
        language: getters.getUserLanguage,
      };
      const queryParameters = Object.assign(
        state.searchParameters,
        defaultSearchParameters,
      );
      if (!queryParameters.search) {
        return;
      }
      commit('updateResults', null, null);
      const loadingTimer = setTimeout(() => commit('startProcessing'), 150);
      Vue.http.get('/api/search/{?publication_year,dataset}', { params: queryParameters }, {
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
      }).then(() => {
        clearTimeout(loadingTimer);
        commit('endProcessing');
      });
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
    getUserLanguage(state, getters) {
      return state.language || getters.getDefaultUserLanguage;
    },
    getDefaultUserLanguage() {
      let userLanguage;
      if (navigator.languages) {
        userLanguage = navigator.languages[0];
      } else {
        userLanguage = navigator.language || navigator.userLanguage;
      }
      if (userLanguage.includes('en')) {
        userLanguage = 'en';
      }
      if (userLanguage.includes('de')) {
        userLanguage = 'de';
      }
      if (userLanguage.includes('fr')) {
        userLanguage = 'fr';
      }
      return userLanguage || 'en';
    },
    getChoices(state) {
      return state.results.result_choices;
    },
  },
};
export { search as default };
