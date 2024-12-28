<template>
    <div class="container">
      <div class="row my-4">
        <h1 class="mt-4 col-6">
          <font-awesome-icon :icon="['fas', 'star']" class="text-success" />
          {{ title }}
        </h1>
      </div>
      <div>
        <h3>
        <font-awesome-icon :icon="['fas', 'spinner']" spin />
          tulošša piäh...
        </h3>
      </div>
    </div>
  </template>
  
  <script>
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  
  export default {
    name: 'LessonsComponent',
    components: {
      FontAwesomeIcon
    },
    data() {
      return {
        title: 'Urokat',
        loading: false,
      };
    },
    mounted() {
      document.title = 'Urokat';
    }
  };
  </script>
  
  <style scoped>
  .container {
    margin-top: 20px;
  }
  
  .fa-spinner {
    margin-right: 16px;
  }
  </style>
  