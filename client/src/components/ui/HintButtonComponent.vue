<template>
  <button
    class="btn border-dark"
    :class="isActive ? 'btn-secondary' : 'btn-light'"
    ref="hintButton"
    @click="toggleHint"
    title="Jiävi otvietat"
  >
    <font-awesome-icon :icon="['fas', 'key']" />
  </button>
</template>

<script>
export default {
  name: 'HintButton',
  data() {
    return {
      isActive: false,
      clickListener: null
    };
  },
  methods: {
    toggleHint() {
      this.isActive = !this.isActive;
      this.$emit('show-hint', this.isActive);
      
      if (this.isActive) {
        // Добавляем обработчик клика по всему документу
        this.clickListener = (e) => {
          // Если клик не по кнопке подсказки
          if (!this.$refs.hintButton.contains(e.target)) {
            this.deactivateHint();
          }
        };
        
        // Добавляем обработчик с небольшой задержкой, чтобы не сработал сразу
        setTimeout(() => {
          document.addEventListener('click', this.clickListener);
        }, 100);
      } else {
        this.removeClickListener();
      }
    },
    
    deactivateHint() {
      this.isActive = false;
      this.$emit('show-hint', false);
      this.removeClickListener();
    },
    
    removeClickListener() {
      if (this.clickListener) {
        document.removeEventListener('click', this.clickListener);
        this.clickListener = null;
      }
    }
  },
  
  beforeUnmount() {
    this.removeClickListener();
  }
};
</script>