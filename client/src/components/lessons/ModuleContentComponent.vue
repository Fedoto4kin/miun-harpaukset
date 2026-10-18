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
        <GrammarCommentsComponent 
          v-if="grammar_comment"
          :comment="grammar_comment"
        />
      </div>
    </div>
    <div class="lesson-content" v-else>
      ...tulošša piäh
    </div>
  </div>
</template>

<script>
import ExerciseFactory from '@/components/lessons/exercises/ExerciseFabricComponent.vue';
import GrammarCommentsComponent from '@/components/lessons/GrammarCommentsComponent.vue';

export default {
  name: 'ModuleContentComponent',
  components: {
    ExerciseFactory,
    GrammarCommentsComponent,
  },
  props: {
    html_content: String,
    speech: String,
    exercises: Array,
    grammar_comment: Object,
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
  width: 97%;
}

@media (max-width: 600px) {
  .module-navigation button {
    font-size: 0.8rem;
  }
}
</style>