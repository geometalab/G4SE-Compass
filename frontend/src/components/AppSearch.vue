<template>
    <div class="container">
        <div class="form-group row">
            <label for="searchText" class="col-md-2 col-form-label">Search</label>
            <div class="col-md-10">
                <input v-model="searchText" @keyup="searchEntered" type="text" class="form-control" id="searchText" placeholder="Search">
            </div>
        </div>
    </div>
</template>
<script>
    import _ from 'lodash'

    export default{
        name: 'app-search',
        data(){
            return{
                msg:'hello vue',
                searchText: '',
            }
        },
methods: {
    searchEntered: _.debounce(
      function () {
      // TODO: do the actual search
        console.log(this.searchText);
      },
      500
    )
},
    }
</script>
