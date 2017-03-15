<template>
  <div class="col-md-6 search-result">
    <div class="card">
      <div class="card-header">
        <h4 class="card-title">{{searchResult.title}}</h4>
        <h6 class="card-subtitle mb-2 text-muted"><strong>{{searchResult.service_type}}</strong> / {{searchResult.publication_year}} / {{searchResult.geography}} / {{searchResult.source}}</h6>
      </div>
      <div class="card-block">
        <p class="card-text">
          {{searchResult.abstract}}
        </p>
      </div>
      <div class="card-block">
        <router-link :to="{ path: `/metadata/${searchResult.api_id}` }">Full Details</router-link>
      </div>
    </div>
  </div>
</template>
<script>
  export default {
    name: 'app-search-result',
    props: ['searchResult'],
  };
</script>
<style scoped>
  .search-result {
    padding-bottom: 20px;
  }
</style>
