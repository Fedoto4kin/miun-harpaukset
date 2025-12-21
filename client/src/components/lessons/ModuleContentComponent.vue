<template>
  <div>    
    <div class="lesson-content" v-if="html_content">
      <div class="content-container">
          <div v-if="speech" class="d-flex audio-container justify-content-center mt-1 mb-1">
          <audio controls class="audio-player" :key="speech">
            <source :src="speech" type="audio/mpeg" />
          </audio>
        </div>
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

.audio-player {
  width: 50%; 
}

@media (min-width: 992px) {
  .audio-container {
    transform: scale(0.75); 
    transform-origin: center top;
  }
}

@media (max-width: 991.98px) {
  .audio-player {
    width: 100%; 
    margin-bottom: 0.5em;
  }
}

@media (max-width: 600px) {
  .module-navigation button {
    font-size: 0.8rem;
  }
}
</style>