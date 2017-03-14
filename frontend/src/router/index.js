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
      redirect: '/search',
    },
    {
      path: '/search',
      name: 'search-result',
      component: AppSearch,
      props: route => ({
        search: route.query.search,
        page: parseInt(route.query.page, 10),
        is_latest: route.query.is_latest,
        from_year: route.query.from_year,
        to_year: route.query.to_year,
      }),
    },
  ],
});
