import Vue from 'vue';
import Router from 'vue-router';
import AppSearch from 'components/AppSearch';
import MetadataItem from 'components/MetadataSingle';

Vue.use(Router);

export default new Router({
  // mode: 'history',
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
        is_latest: route.query.is_latest,
        from_year: route.query.from_year,
        to_year: route.query.to_year,
      }),
    },
    {
      path: '/search/:page',
      name: 'search-result-paginated',
      component: AppSearch,
      props: route => ({
        page: parseInt(route.params.page, 10) || 1,
        search: route.query.search,
        is_latest: route.query.is_latest,
        from_year: route.query.from_year,
        to_year: route.query.to_year,
      }),
    },
    {
      path: '/metadata/:id',
      component: MetadataItem,
      props: true,
    },
  ],
});
