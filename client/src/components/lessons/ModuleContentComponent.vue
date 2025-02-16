<template>
  <div>    
    <div class="lesson-content" v-if="html_content">
      <div class="content-container">
        <div v-if="speech" class="mb-lg-3">
          <div class="d-flex justify-content-start audio-container">
          
          </div>
        </div>
        <div class="table-responsive" v-html="html_content"></div>
        <div v-if="exercises && exercises.length > 0" class="exercise-container mt-2">
          <ExerciseFactory 
            v-for="(exercise, index) in exercises" 
            :key="index" 
            :exercise="exercise" 
          />
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

.lesson-content {
  overflow-x: auto;
}

.content-container {
  display: flex;
  flex-direction: column;
}

.exercise-container {
  min-width: 700px;
  width: 95%;
}

@media (max-width: 600px) {
  .module-navigation button {
    font-size: 0.8rem;
  }
}
</style>