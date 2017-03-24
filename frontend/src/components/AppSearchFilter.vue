<template>
  <div class="col-12">
    <input type="button" @click="applyFilter" class="btn btn-sm btn-default" value="Apply Filter" />
    <input type="button" @click="resetFilter" class="btn btn-sm btn-default" value="Reset Filter" />

    <multiselect
      @selected="yearsChanged"
      :options="years"
      :collapsible="true"
      label="Years"></multiselect>

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
        this.$store.commit('search/setPublicationYears', selection);
      },
      applyFilter() {
        this.$store.commit('search/setPage', 1);
        this.$store.commit('search/setPublicationYears', this.publicationYears);
        this.$store.dispatch('search/search');
      },
      resetFilter() {
        this.$store.commit('search/setPage', 1);
        this.$store.commit('search/setPublicationYears', []);
        this.$store.dispatch('search/search');
      },
    },
    computed: {
      years() {
        return this.$store.getters['search/getChoices'].publication_year;
      },
    },
  };
</script>
<style>
</style>
