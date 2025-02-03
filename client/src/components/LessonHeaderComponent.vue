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
      <h3 class="px-3">
        {{ lesson.slogan }}
      </h3>
    </div>
  </template>
  
<script>
export default {
name: 'LessonHeaderComponent',
props: {
    lesson: {
    type: Object,
    required: true,
    },
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