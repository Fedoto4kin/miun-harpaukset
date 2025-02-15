<template>
  <div>    
    <div class="lesson-content" v-if="html_content">
      <div class="content-container">
        <div class="table-responsive" v-html="html_content"></div>
        <div v-if="exercises && exercises.length > 0" class="exercise-container mt-2">
          <ExerciseFactory 
            v-for="(exercise, index) in exercises" 
            :key="index" 
            :exercise="exercise" 
          />
        </div>
        <div v-if="speech" class="mt-4">
          <div class="mb-3 d-flex justify-content-center">
            <audio controls class="audio-player" :key="speech">
              <source :src="speech" type="audio/mpeg" />
            </audio>
          </div>
        </div>
      </div>
    </div>

    <div class="lesson-content" v-else>
      ...tulošša piäh
    </div>
  </div>
</template>

<script>
import ExerciseFactory from '@/components/lessons/exercises/ExerciseFabricComponent.vue';

export default {
  name: 'ModuleContentComponent',
  components: {
    ExerciseFactory,
  },
  props: {
    html_content: String,
    speech: String,
    exercises: Array,
  },
};
</script>

<style scoped>
.audio-player {
  width: 100%;
}

.lesson-content {
  overflow-x: auto;
}

.content-container {
  display: flex;
  flex-direction: column;
}

.exercise-container {
  min-width: 700px;
  width: 90%;
}

@media (max-width: 600px) {
  .module-navigation button {
    font-size: 0.8rem;
  }
}
</style>
