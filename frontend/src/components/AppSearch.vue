<template>
    <div class="container">
        <div class="form-group row">
            <label for="searchText" class="col-md-2 col-form-label">Search</label>
            <div class="col-md-10">
                <input v-model="searchText" type="text" class="form-control" id="searchText" placeholder="Search">
            </div>
        </div>
        <div class="row">
            <div v-show="error" class="col-12 bg-warning">
                <p>{{ error }}</p>
            </div>
        </div>
        <div v-show="searching">Searching...</div>
        <div v-if="searchResults.count > 0" class="row">
            Results: {{ searchResults.count }}
                <search-result
                        v-for="searchResult in searchResults.results"
                        v-bind:search-result="searchResult"></search-result>
        </div>
        <div v-if="searchResults.count == 0" class="row">
            No Results found.
        </div>
    </div>
</template>
<script>
    import _ from 'lodash';
    import AppSearchResult from './AppSearchResult.vue';

    export default{
        name: 'app-search',
        components: {
            // <my-component> will only be available in parent's template
            'search-result': AppSearchResult,
        },
        data: function(){
            return {
                searchText: '',
                searchParams: {
                    search: '',
                    language: 'en',
//                    ordering: '',
//                    limit: 10,
                    page_size: 10,
                    page: 1,
                    from_year: null,
                    to_year: null,
                    is_latest: false,
                },
                searchResults: {
                    count: 0
                },
                error: null,
                searching: false,
            }
        },
        watch: {
            searchText: function(oldVal, newVal) {
                console.log(oldVal, newVal);
                this.searchEntered();
            }
        },
        methods: {
            searchEntered: function () {
              this.searching = true;
              this.clearResults();
              this.debouncedSearch();
            },
            clearResults: function() {
                this.searchResults = {count: 0};
                this.error = null;
            },
            debouncedSearch: _.debounce(
                function () {
                    this.searchParams.search = this.searchText;
                    if (this.searchParams.search == '') {
                        this.searching = false;
                        if (this.previousRequest) {
                            this.previousRequest.abort();
                        }
                    } else {
                        this.$http.get('/api/search/', {params: this.searchParams}, {
                            // use before callback
                            before(request) {
                                // abort previous request, if exists
                                if (this.previousRequest) {
                                    this.previousRequest.abort();
                                }
                                // set previous request on Vue instance
                                this.previousRequest = request;
                            }
                        }).then(response => {
                            // success callback
                            this.searchResults = response.body;
                        }, response => {
                            this.error = response.body.detail;
                        }).then(function() {
                            this.searching = false;
                        });
                    }
                },
                300
            )
        },
    }
</script>
