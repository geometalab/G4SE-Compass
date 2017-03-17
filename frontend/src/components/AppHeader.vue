<template>
  <div id="app-header" class="container-fluid clearfix">
    <div class="float-left">
      <router-link to="/search"><img width="100px" src="../assets/logo.jpg"></router-link>
    </div>
    <h3>&nbsp;G4SE Geodata</h3>
  </div>
</template>
<script>
  export default{
    name: 'app-header',
  };
</script>
<style>
  #app-header {
    padding-top: 20px;
    padding-bottom: 20px;
  }
</style>
