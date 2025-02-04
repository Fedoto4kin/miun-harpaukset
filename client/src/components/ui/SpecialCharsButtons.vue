<template>
      <span
            v-for="char in specialChars"
            :key="char"
            :data-char="char"
            class="btn btn-secondary"
            @click="handleDiacrtButtonClick"
        >{{ char }}</span>
  </template>
  
  <script>
  
  export default {
    name: 'SpecialCharsButtons',
    props: {
      searchText: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        specialChars: ['č', 'š', 'ž', 'ä', 'ö']
      };
    },
    emits: ['diacrt-click'],
    methods: {
      handleDiacrtButtonClick(event) {
        this.$emit('diacrt-click', event);
      },
    },
  };
  </script>
  
  <style scoped>
  .btn-group {
    display: flex;
    gap: 0.5rem;
  }
  </style>
  