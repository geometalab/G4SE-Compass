<template>
  <div id="app">
    <app-header></app-header>
    <div class="container">
      <router-view></router-view>
    </div>
  </div>
</template>

<script>

import AppHeader from './components/AppHeader';

export default {
  name: 'app',
  components: {
    AppHeader,
  },
};
</script>
