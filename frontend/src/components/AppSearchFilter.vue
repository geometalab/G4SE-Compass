<template>
  <div class="col-12">
    <input type="button" @click="applyFilter" class="btn btn-sm btn-default" value="Apply Filter" />
    <input type="button" @click="resetFilter" class="btn btn-sm btn-default" value="Reset Filter" />

    <div class="row">
      <div class="col-md-6">
        <multiselect
          @selected="yearsChanged"
          :options="years"
          :collapsible="true"
          :maxSize="10"
          label="Years"></multiselect>
      </div>
    </div>

    <input type="button" @click="applyFilter" class="btn btn-sm btn-default" value="Apply Filter" />
    <input type="button" @click="resetFilter" class="btn btn-sm btn-default" value="Reset Filter" />
  </div>
</template>
<script>
  import MultiSelect from './form_elements/MultiSelect';

  export default {
    name: 'search-filter',
    data() {
      return {
        publicationYears: this.$store.state.search.searchParameters.publication_year,
      };
    },
    components: {
      multiselect: MultiSelect,
    },
    methods: {
      yearsChanged(selection) {
        this.publicationYears = selection;
      },
      applyFilter() {
        if (this.hasValueChanged) {
          this.$store.commit('search/setPage', 1);
          this.$store.commit('search/setPublicationYears', this.publicationYears);
          this.$store.dispatch('search/search');
        }
      },
      resetFilter() {
        this.publicationYears = [];
        this.$store.commit('search/setPublicationYears', []);
        this.applyFilter();
      },
    },
    computed: {
      years() {
        return this.$store.getters['search/getChoices'].publication_year;
      },
      hasValueChanged() {
        return this.$store.state.search.searchParameters.publication_year !== this.publicationYears;
      },
    },
  };
</script>
<style>
</style>
