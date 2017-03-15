<template>
  <div class="container">
    <div class="form-group row">
      <div class="col-md-12 form-group input-group">
        <input v-model="searchTerms" @keyup.enter="searchEntered" type="search" class="form-control col-md-11" id="searchText" placeholder="Enter your search" />
        <span class="input-group-btn">
          <input type="button" class="btn bg-faded" @click="searchEntered" value="Go" />
        </span>
        <span class="input-group-btn">
          <input type="button" class="btn bg-faded" @click="clear" id="clearSearch" value="Clear" />
        </span>
      </div>
    </div>
    <div class="row">
      <div v-show="error" class="col-12 bg-warning">
        <p>{{ error }}</p>
      </div>
    </div>
    <div v-if="searchResults.count > 0" class="row">
      <loading v-if="loading">loading...</loading>
      <div v-else>
        <div class="col-12 row">
          <pagination :search-results="searchResults"></pagination>
        </div>
        <search-result
          v-for="searchResult in searchResults.results"
          v-bind:search-result="searchResult"
        />
      </div>
    </div>
    <div v-if="search !== '' && searchResults.count == 0" class="row">
      No Results found.
    </div>
  </div>
</template>
<script>
  // TODO: Refactor this huge hunk of a module!
  import _ from 'lodash';
  import PulseLoader from 'vue-spinner/src/PulseLoader';
  import router from '../router';
  import SearchResult from './AppSearchResult';
  import Pagination from './AppPagination';

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
        loading: false,
      };
    },
    components: {
      'search-result': SearchResult,
      pagination: Pagination,
      loading: PulseLoader,
    },
    created() {
      // This is executed on page load, we just proceed as if it were a route change.
      if (this.search && this.search !== '') {
        this.routeChanged();
      }
    },
    watch: {
      // call again the method if the route changes
      $route: 'routeChanged',
      '$store.state.paginationPage': 'changeRoute',
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
        if (this.searchTerms && this.searchTerms !== '') {
          this.$store.state.paginationPage = 1;
          this.changeRoute();
        }
      },
      clear() {
        this.$store.state.paginationPage = 1;
        this.searchTerms = '';
        this.searchResults = { count: 0 };
        router.push(
          {
            name: 'search',
          });
      },
      changeRoute() {
        router.push(
          {
            name: 'search-result',
            query: this.buildQueryParameters(),
          });
      },
      routeChanged() {
        // TODO: remove this duplication: this.searchTerms is already assigned a value
        // unless we're using browser history (back/forward)
        this.searchTerms = this.search;
        if (this.search && this.search !== '') {
          this.loading = true;
        }
        this.$store.state.paginationPage = this.page;
        this.debouncedSearch();
      },
      getSearchParameters() {
        const query = this.buildQueryParameters();
        return Object.assign(query, {
          // DEFAULT PARAMETERS
          page_size: 10,
          language: this.getUserLanguage(),
          // ordering: this.ordering,
          // limit: 10,
        });
      },
      buildQueryParameters() {
        let search = this.search;
        if (this.searchTerms && this.searchTerms !== '') {
          search = this.searchTerms;
        }
        const query = {
          search,
          page: this.$store.state.paginationPage,
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
              this.searchResults.params = query;
            }, (response) => {
              this.error = response.body.detail;
            }).then(() => {
              this.loading = false;
            });
          }
        },
        100,
      ),
    },
  };
</script>
