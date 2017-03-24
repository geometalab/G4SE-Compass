<template>
  <div class="col-12">
    <input type="button" @click="applyFilter" class="btn btn-sm btn-default" value="Apply Filter" />
    <input type="button" @click="resetFilter" class="btn btn-sm btn-default" value="Reset Filter" />

    <div class="col-12">
      <label class="form-check-label">
        <input class="form-check-input" type="checkbox" id="checkbox" v-model="isLatest">
        <label for="checkbox">Exclude not latest entries (where available) [{{ isLatest }}]</label>
      </label>
    </div>

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
        isLatest: this.$store.state.search.searchParameters.is_latest || false,
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
          this.$store.commit('search/setLatestOnly', this.isLatest);
          this.$store.dispatch('search/search');
        }
      },
      resetFilter() {
        this.dataSets = [];
        this.$store.commit('search/setDataSets', []);
        this.publicationYears = [];
        this.$store.commit('search/setPublicationYears', []);
        this.isLatest = false;
        this.$store.commit('search/setLatestOnly', false);
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
        return this.$store.state.search.searchParameters.is_latest !== this.isLatest ||
          this.$store.state.search.searchParameters.dataset !== this.dataSets ||
          this.$store.state.search.searchParameters.publication_year !== this.publicationYears;
      },
    },
  };
</script>
<style>
</style>
