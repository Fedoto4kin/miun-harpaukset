<template>
  <div id="app">
    <LexiconComponent />
  </div>
</template>

<script>
import LexiconComponent from './components/LexiconComponent.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

export default {
  name: 'App',
  components: {
    LexiconComponent
  }
};
</script>

<style>
/* Ваши стили */
</style>
