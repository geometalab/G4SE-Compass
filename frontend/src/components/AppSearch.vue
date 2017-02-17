<template>
  <div class="container">
    <div class="form-group row">
      <div class="col-md-12 form-group form-inline">
        <input v-model="searchText" @keyup.enter="searchEntered" type="search" class="form-control col-md-11" id="searchText" placeholder="Enter your search" />
        <input type="button" class="btn bg-faded" @click="searchEntered" value="Go" />
      </div>
    </div>
    <div class="row">
      <div v-show="error" class="col-12 bg-warning">
        <p>{{ error }}</p>
      </div>
    </div>
    <div v-show="searching">Searching...</div>
    <div v-if="searchResults.count > 0" class="row">
      <pagination></pagination>
      <search-result
        v-for="searchResult in searchResults.results"
        v-bind:search-result="searchResult"
      />
    </div>
    <div v-if="searchResults.count == 0" class="row">
      No Results found.
    </div>
  </div>
</template>
<script>
  import _ from 'lodash';
  import AppSearchResult from './AppSearchResult';
  import AppPagination from './AppPagination';

  export default {
    name: 'app-search',
    components: {
      // <my-component> will only be available in parent's template
      'search-result': AppSearchResult,
      pagination: AppPagination,
    },
    data() {
      return {
        searchText: '',
        searchParams: {
          search: '',
          language: this.getUserLanguage(),
//          ordering: '',
//          limit: 10,
          page_size: 10,
          page: 1,
          from_year: null,
          to_year: null,
          is_latest: false,
        },
        searchResults: {
          count: 0,
        },
        error: null,
        searching: false,
      };
    },
    watch: {
      searchText() {
//                TODO: type-ahead!!!
      },
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
        this.clearResults();
        this.debouncedSearch();
      },
      clearResults() {
        this.searchResults = { count: 0 };
        this.error = null;
      },
      debouncedSearch: _.debounce(
        function fetchSearchResult() {
          // eslint-disable-next-line
          console.log(this.searchParams.language);
          this.searchParams.search = this.searchText;
          if (this.searchParams.search === '') {
            this.searching = false;
            if (this.previousRequest) {
              this.previousRequest.abort();
            }
          } else {
            this.$http.get('/api/search/', { params: this.searchParams }, {
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
              // success callback
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
