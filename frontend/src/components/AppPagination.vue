<template>
  <nav aria-label="Page Navigation">
    <ul class="pagination pagination-sm">
      <li class="page-item disabled">
        <a class="page-link" href="#">Previous</a>
      </li>
      <li class="page-item"><a class="page-link" href="#">1</a></li>
      <li class="page-item"><a class="page-link" href="#">current_page</a></li>
      <li class="page-item"><a class="page-link" href="#">3</a></li>
      <li class="page-item">
        <a class="page-link" href="#">Next</a>
      </li>
    </ul>
  </nav>
</template>
<script>
  export default {
    name: 'app-pagination',
    props: {
      current_page: {
        type: Number,
        required: true,
      },
    },
    data() {
      return {
        msg: 'header vue',
      };
    },
  };
</script>
