<template>
  <div class="container">
    <div class="card">
      <div class="card-block">
        <div class="row">
          <!-- Short list -->
          <div class="col-sm-4">
            <h4>{{searchResult.title}}</h4>
          </div>
          <div class="col-sm-3">
            <div class="row">
              Publication Year: {{searchResult.publication_year}}
            </div>
            <div class="row">
              Service Type: {{searchResult.service_type}}
            </div>
          </div>
          <div class="col-sm-4">
            <div class="row">
              Geographical Coverage: {{searchResult.geography}}
            </div>
            <div class="row">
              Source of original data: {{searchResult.source}}
            </div>
          </div>
        </div>
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
