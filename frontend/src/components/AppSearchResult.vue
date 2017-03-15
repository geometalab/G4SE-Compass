<template>
  <div class="col-sm-6 search-result">
    <div class="card">
      <div class="card-header">
        <h4 class="card-title">{{searchResult.title}}</h4>
        <h6 class="card-subtitle mb-2 text-muted">{{searchResult.publication_year}} / {{searchResult.service_type}}</h6>
      </div>
      <div class="card-block" @click="toggleText">
        <p class="card-text" v-if="showFullText">
          {{searchResult.abstract}}
        </p>
        <p class="card-text" v-else>
          {{searchResult.abstract | shortenText}}
        </p>
      </div>
      <ul class="list-group list-group-flush">
        <li class="list-group-item">Geography: {{searchResult.geography}}</li>
        <li class="list-group-item">Source: {{searchResult.source}}</li>
      </ul>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'app-search-result',
    props: ['searchResult'],
    data() {
      return {
        showFullText: false,
      };
    },
    methods: {
      toggleText() {
        this.showFullText = !this.showFullText;
      },
    },
    filters: {
      shortenText(text) {
        if (text.length + 3 > 100) {
          let shortenedText = text.substring(0, 100);
          shortenedText += '...';
          return shortenedText;
        }
        return text;
      },
    },
  };
</script>
<style scoped>
  .search-result {
    padding-bottom: 20px;
  }
</style>
