<template>
    <button
      class="btn btn-light border-dark"
      ref="hintButton"
      @pointerdown="showHint"
      @pointerup="hideHint"
      @mouseleave="hideHint"
      title="Jiävi otvietat"
    >
      <font-awesome-icon :icon="['fas', 'key']" />
    </button>
  </template>
  
  <script>
  export default {
    name: 'HintButton',
    methods: {
      showHint() {
        this.$emit('show-hint', true);
      },
      hideHint() {
        this.$emit('show-hint', false);
      }
    }
  };
  </script>
  