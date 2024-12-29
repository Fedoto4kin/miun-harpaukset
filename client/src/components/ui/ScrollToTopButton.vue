<template>
    <button 
      v-show="visible" 
      @click="scrollToTop" 
      class="scroll-to-top-btn btn btn-primary"
    >
      <font-awesome-icon icon="arrow-up" />
    </button>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount } from 'vue';
  
  export default {
    name: 'ScrollToTopButton',
    setup() {
      const visible = ref(false);
  
      const scrollToTop = () => {
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      };
  
      const handleScroll = () => {
        visible.value = window.scrollY > 100;
      };
  
      onMounted(() => {
        window.addEventListener('scroll', handleScroll);
      });
  
      onBeforeUnmount(() => {
        window.removeEventListener('scroll', handleScroll);
      });
  
      return {
        visible,
        scrollToTop
      };
    }
  };
  </script>
  
  <style scoped>
  .scroll-to-top-btn {
    position: fixed;
    bottom: 1%;
    right: 1%;
    padding: 10px 15px;
    z-index: 1000;
  }
  </style>