import Vue from 'vue';
import store from '../store';

export default {
  search(queryParameters) {
    console.log('searching call: ', queryParameters);
    if (!queryParameters) {
      // TODO: do not depend on this containing an object with count 0
      return;
    }
    Vue.http.get('/api/search/', { params: queryParameters }, {
      before(request) {
        this.$store.commit('searchRunning');
        if (this.previousRequest) {
          this.previousRequest.abort();
        }
        this.previousRequest = request;
      },
    }).then((response) => {
      store.commit('setSearchResults', response.body, null);
    }, (response) => {
      store.commit('setSearchResults', null, response.body.detail);
    }).then(() => {
      store.commit('searchDone');
    });
  },
};
