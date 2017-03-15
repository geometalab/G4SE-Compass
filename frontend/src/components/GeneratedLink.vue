<template>
  <a :href="url">{{url | shortened}}</a>
</template>
<script>
  export default {
    name: 'generated-links',
    props: {
      url: {
        type: String,
        required: true,
      },
    },
    filters: {
      shortened(value) {
        const maxLength = 40;
        if (value.length + 3 > maxLength) {
          return `${value.substring(0, maxLength / 2)}...${value.substring(value.length - (maxLength / 2), value.length)}`;
        }
        return value;
      },
    },
  };
</script>
