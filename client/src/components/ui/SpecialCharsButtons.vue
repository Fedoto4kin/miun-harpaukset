<template>
  <span v-for="char in specialChars" :key="char" :class="btnClass" :data-char="char" class="btn"
    @click="handleDiacrtButtonClick">{{ char }}</span>
</template>

<script>

export default {
  name: 'SpecialCharsButtons',
  data() {
    return {
      specialChars: ['č', 'š', 'ž', 'ä', 'ö']
    };
  },
  props: {
    btnClass: {
      default: ['btn-secondary']
    } 
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