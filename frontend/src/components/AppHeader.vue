<template>
    <div id="app-header" class="container-fluid">
        <img src="../assets/logo.png">
        <div>{{msg}}</div>
    </div>
</template>
<script>
    export default{
        name: 'app-header',
        data(){
            return{
                msg:'header vue'
            }
        }
    }
</script>
