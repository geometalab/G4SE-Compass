<template>
  <div id="app-header" class="container">
    <div class="row">
      <div class="col-4">
        <router-link to="/search"><img width="100px" src="../assets/logo.jpg"></router-link>
      </div>
      <div class="col-5">
        <h3>&nbsp;G4SE Geodata</h3>
      </div>
      <div class="col-3">
        <label for="search-language">search language</label>
        <select id="search-language" class="form-control form-control-sm" v-model="selectedLanguage">
          <option v-for="option in languageOptions" v-bind:value="option.value">{{ option.text }}</option>
        </select>
      </div>
    </div>
  </div>
</template>
<script>
  import router from '../router';

  export default{
    name: 'app-header',
    props: {
      language: {
        type: String,
        default: 'de',
      },
    },
    data() {
      return {
        selectedLanguage: 'de',
        languageOptions: [
            { text: 'en', value: 'en' },
            { text: 'de', value: 'de' },
            { text: 'fr', value: 'fr' },
        ],
      };
    },
    created() {
      this.selectedLanguage = this.$route.query.language || this.$store.getters['search/getUserLanguage'];
    },
    watch: {
      selectedLanguage: 'updateLanguage',
    },
    methods: {
      updateLanguage() {
        this.$store.commit('search/setLanguage', this.selectedLanguage);
        this.languageChangeConfirm();
      },
      languageChangeConfirm() {
        router.push(
          {
            name: 'search-result-paginated',
            query: {
              search: this.$store.state.search.searchParameters.search,
              language: this.$store.getters['search/getUserLanguage'],
            },
            params: {
              page: this.$store.getters['search/currentPage'],
            },
          });
      },
    },
  };
</script>
<style>
  #app-header {
    padding-top: 20px;
    padding-bottom: 20px;
  }
</style>
