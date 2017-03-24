<template>
  <div class="form-group">
    <label for="multiselect" v-if="collapsible" @click="collapsed=!collapsed">
      <span v-if="collapsed" title="expand"><strong>&#x2B07;</strong> {{label}}</span>
      <span v-if="!collapsed" title="collapse"><strong>&#x2B06;</strong> {{label}}</span>
    </label>
    <label for="multiselect" v-else>{{label}}</label>

    <select v-model="selectedOptions"
            v-show="!collapsed"
            class="form-control"
            id="multiselect"
            :size="options.length"
            multiple>
      <option v-for="opt in options" :value="opt">{{opt}}</option>
    </select>
  </div>
</template>
<script>
  export default {
    name: 'multiselect',
    props: {
      options: {
        type: Array,
        required: true,
      },
      selected: {
        type: Array,
        default: null,
      },
      label: {
        type: String,
        required: true,
      },
      collapsible: {
        type: Boolean,
        default: false,
      },
    },
    watch: {
      selectedOptions: 'selectedOptionsChanged',
    },
    data() {
      return {
        collapsed: false,
        selectedOptions: this.$store.state.search.searchParameters.publication_year || [],
      };
    },
    methods: {
      selectedOptionsChanged() {
        this.$emit('selected', this.selectedOptions);
      },
    },
  };
</script>
<style>
</style>
