import Vue from 'vue';
import Router from 'vue-router';
import AppSearch from 'components/AppSearch';
import VueResource from 'vue-resource';

Vue.use(Router);
Vue.use(VueResource);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'AppSearch',
      component: AppSearch,
    },
  ],
});
