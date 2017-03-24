<template>
  <div class="col-12">
    <input type="button" @click="applyFilter" class="btn btn-sm btn-default" value="Apply Filter" />
    <input type="button" @click="resetFilter" class="btn btn-sm btn-default" value="Reset Filter" />

      <multiselect
        v-if="years && years.length !== 0"
        @selected="yearsChanged"
        :options="years"
        :collapsible="true"
        :maxSize="10"
        label="Years">
      </multiselect>
      <multiselect
        v-if="dataSetList && dataSetList.length !== 0"
        @selected="dataSetsChanged"
        :options="dataSetList"
        :collapsible="true"
        :maxSize="10"
        label="Dataset">
      </multiselect>

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
        dataSets: this.$store.state.search.searchParameters.dataset,
      };
    },
    components: {
      multiselect: MultiSelect,
    },
    methods: {
      yearsChanged(selection) {
        this.publicationYears = selection;
      },
      dataSetsChanged(selection) {
        this.dataSets = selection;
      },
      applyFilter() {
        if (this.hasValueChanged) {
          this.$store.commit('search/setPage', 1);
          this.$store.commit('search/setPublicationYears', this.publicationYears);
          this.$store.commit('search/setDataSets', this.dataSets);
          this.$store.dispatch('search/search');
        }
      },
      resetFilter() {
        this.dataSets = [];
        this.$store.commit('search/setDataSets', []);
        this.publicationYears = [];
        this.$store.commit('search/setPublicationYears', []);
        this.applyFilter();
      },
    },
    computed: {
      years() {
        return this.$store.getters['search/getChoices'].publication_year;
      },
      dataSetList() {
        return this.$store.getters['search/getChoices'].dataset;
      },
      hasValueChanged() {
        return this.$store.state.search.searchParameters.dataset !== this.dataSets ||
          this.$store.state.search.searchParameters.publication_year !== this.publicationYears;
      },
    },
  };
</script>
<style>
</style>
