<template>
  <nav aria-label="Pagination">
    <ul class="pagination pagination-sm">
      <li class="page-item" v-bind:class="{ disabled: !hasPrevious() }">
        <a class="page-link" v-on:click="previousPage()">Previous</a>
      </li>
      <li class="page-item disabled">
        <a class="page-link">Showing {{currentShowStart()}}-{{currentShowEnd()}} of total {{searchResults.count}} results.</a>
      </li>
      <li class="page-item" v-bind:class="{ disabled: !hasNext() }">
        <a class="page-link" v-on:click="nextPage()">Next</a>
      </li>
    </ul>
  </nav>
</template>
<script>
  export default {
    name: 'app-pagination',
    props: {
      searchResults: {
        type: Object,
        required: true,
      },
    },
    methods: {
      previousPage() {
        if (this.hasPrevious()) {
          this.$store.commit('previousPage');
        }
      },
      nextPage() {
        if (this.hasNext()) {
          this.$store.commit('nextPage');
        }
      },
      hasPrevious() {
        return this.searchResults.params.page > 1;
      },
      hasNext() {
        return (this.searchResults.params.page * this.searchResults.params.page_size)
          <= this.searchResults.count;
      },
      currentShowStart() {
        const previousPage = this.searchResults.params.page - 1;
        const itemsPerPage = this.searchResults.params.page_size;
        const itemsDisplayed = previousPage * itemsPerPage;
        return itemsDisplayed + 1;
      },
      currentShowEnd() {
        const max = this.searchResults.params.page * this.searchResults.params.page_size;
        if (max < this.searchResults.count) {
          return max;
        }
        return this.searchResults.count;
      },
    },
  };
</script>
