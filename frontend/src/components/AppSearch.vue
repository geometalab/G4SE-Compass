<template>
  <div>
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
    <div v-if="searchResults && searchResults.count > 0" class="row">
      <loading v-if="loadingInProgress">loading...</loading>
      <div v-else>
        <div class="col-12 row">
          <pagination :search-results="searchResults"></pagination>
        </div>
        <div class="row">
          <search-result
            v-for="searchResult in searchResults.results"
            v-bind:search-result="searchResult"
          />
        </div>
        <div class="col-12 row">
          <pagination :search-results="searchResults"></pagination>
        </div>
      </div>
    </div>
    <div v-if="searchResults && searchResults.count == 0" class="row">
      No Results found.
    </div>
  </div>
</template>
<script>
  // TODO: Refactor this huge hunk of a module!
  import { mapState } from 'vuex';
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
      };
    },
    computed: mapState({
      loadingInProgress: state => state.search.processing,
      searchResults: state => state.search.results,
      error: state => state.search.errors,
    }),
    components: {
      'search-result': SearchResult,
      pagination: Pagination,
      loading: PulseLoader,
    },
    created() {
      // This is executed on page load, we just proceed as if it were a route change.
      this.routeChanged();
    },
    watch: {
      // call again the method if the route changes
      $route: 'routeChanged',
      '$store.state.search.searchParameters.page': 'changeRoute',
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
          this.$store.commit('search/setPage', 1);
          this.changeRoute();
        }
      },
      clear() {
        this.$store.commit('search/reset');
        this.searchTerms = '';
        this.changeRoute();
      },
      changeRoute() {
        router.push(
          {
            name: 'search-result-paginated',
            query: {
              search: this.searchTerms,
            },
            params: {
              page: this.$store.getters['search/currentPage'],
            },
          });
      },
      routeChanged() {
        if (this.search && this.search !== '') {
          this.searchTerms = this.search;
          this.$store.commit('search/setPage', this.page);
          this.doSearch();
        }
      },
      doSearch() {
        this.$store.commit('search/updateSearchParameters', {
          search: this.searchTerms,
          page: this.page,
        });
        this.$store.dispatch('search/search');
      },
    },
  };
</script>
