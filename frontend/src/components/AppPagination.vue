<template>
  <nav aria-label="Pagination">
    <ul class="pagination pagination-sm">
      <li class="page-item" v-bind:class="{ disabled: !hasPrevious }">
        <a class="page-link" v-on:click="previousPage()">Previous</a>
      </li>
      <li class="page-item disabled">
        <a class="page-link">{{showingResultsFromToText}}</a>
      </li>
      <li class="page-item" v-bind:class="{ disabled: !hasNext }">
        <a class="page-link" v-on:click="nextPage()">Next</a>
      </li>
    </ul>
  </nav>
</template>
<script>
  export default {
    name: 'app-pagination',
    computed: {
      showingResultsFromToText() {
        return this.$store.getters['search/showingResultsFromToText'];
      },
      hasPrevious() {
        return this.$store.getters['search/hasPreviousPage'];
      },
      hasNext() {
        return this.$store.getters['search/hasNextPage'];
      },
    },
    methods: {
      previousPage() {
        if (this.hasPrevious) {
          this.$store.commit('search/previousPage');
        }
      },
      nextPage() {
        if (this.hasNext) {
          this.$store.commit('search/nextPage');
        }
      },
    },
  };
</script>
