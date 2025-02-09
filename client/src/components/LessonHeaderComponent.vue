<template>
  <div v-if="lesson" class="position-relative">
    <div v-if="lesson.speech" class="audio-container">
      <audio controls class="audio-player" :key="lesson.id">
        <source :src="lesson.speech" type="audio/mpeg" />
      </audio>
    </div>
    <h4 class="border-bottom pb-2 px-2">
      {{ lesson.full_name }}
    </h4>
    <div class="d-flex align-items-center justify-content-between">
      <h3 class="px-3">
        {{ lesson.slogan }}
      </h3>
      <button class="btn mt-n1 btn-outline-secondary" @click="showPopup = true">
        <font-awesome-icon :icon="['fas', 'book']" />
      </button>
    </div>
    <SearchPopupComponent :show="showPopup" @close="showPopup = false" />
  </div>
</template>

<script>
import SearchPopupComponent from './SearchPopupComponent.vue';

export default {
  name: 'LessonHeaderComponent',
  components: {
    SearchPopupComponent,
  },
  props: {
    lesson: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showPopup: false,
    };
  },
};
</script>

<style scoped>
.audio-container {
  position: absolute;
  right: 0;
  top: -0.5rem;
  width: 22em; 
  z-index: 1000;
}

.audio-player {
  width: 100%;
  transform: scale(0.75); 
  transform-origin: top right; 
}

</style>
