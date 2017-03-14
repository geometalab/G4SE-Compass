<template>
  <div class="container">
    <div class="form-group row">
      <div class="col-md-12 form-group form-inline">
        <input v-model="searchTerms" @keyup.enter="searchEntered" type="search" class="form-control col-md-11" id="searchText" placeholder="Enter your search" />
        <input type="button" class="btn bg-faded" @click="searchEntered" value="Go" />
      </div>
    </div>
    <div class="row">
      <div v-show="error" class="col-12 bg-warning">
        <p>{{ error }}</p>
      </div>
    </div>
    <div v-if="searching">Searching...</div>
    <div v-if="!searching && searchResults.count > 0" class="row">
      <pagination></pagination>
      <search-result
        v-for="searchResult in searchResults.results"
        v-bind:search-result="searchResult"
      />
    </div>
    <div v-if="search !== '' && !searching && searchResults.count == 0" class="row">
      No Results found.
    </div>
  </div>
</template>
<script>
  import _ from 'lodash';
  import router from '../router';
  import AppSearchResult from './AppSearchResult';
  import AppPagination from './AppPagination';

  export default {
    name: 'app-search',
    props: {
      search: {
        type: String,
        default: '',
      },
      page: {
        type: Number,
        default: 1,
      },
      is_latest: {
        type: Boolean,
        default: false,
      },
      from_year: {
        type: Number,
        required: false,
      },
      to_year: {
        type: Number,
        required: false,
      },
    },
    data() {
      return {
        searchTerms: this.search,
        searchResults: {
          count: 0,
        },
        error: null,
        searching: false,
      };
    },
    components: {
      // <my-component> will only be available in parent's template
      'search-result': AppSearchResult,
      pagination: AppPagination,
    },
    created() {
      this.debouncedSearch();
    },
    watch: {
      // call again the method if the route changes
      $route: 'debouncedSearch',
    },
    methods: {
      getUserLanguage() {
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
        return userLanguage;
      },
      searchEntered() {
        this.searching = true;
        router.push(
          {
            name: 'search-result',
            query: this.buildQueryParameters(),
          });
      },
      getSearchParameters() {
        const query = this.buildQueryParameters();
        return Object.assign(query, {
//          DEFAULT PARAMETERS
          page_size: 10,
          language: this.getUserLanguage(),
//          ordering: this.ordering,
//          limit: 10,
        });
      },
      buildQueryParameters() {
        const query = {
          search: this.searchTerms,
          page: this.page || 1,
        };
        if (this.from_year) {
          query.from_year = this.from_year;
        }
        if (this.to_year) {
          query.to_year = this.to_year;
        }
        if (this.is_latest) {
          query.is_latest = this.is_latest;
        }
        return query;
      },
      debouncedSearch: _.debounce(
        function fetchSearchResult() {
          // eslint-disable-next-line
          console.log('here', this.getSearchParameters());
          const query = this.getSearchParameters();
          if (query.search === '') {
            this.searching = false;
            if (this.previousRequest) {
              this.previousRequest.abort();
            }
          } else {
            this.$http.get('/api/search/', { params: query }, {
              // use before callback
              before(request) {
                // abort previous request, if exists
                if (this.previousRequest) {
                  this.previousRequest.abort();
                }
                // set previous request on Vue instance
                this.previousRequest = request;
              },
            }).then((response) => {
              this.searchResults = response.body;
            }, (response) => {
              this.error = response.body.detail;
            }).then(() => {
              this.searching = false;
            });
          }
        },
        300,
      ),
    },
  };
</script>
