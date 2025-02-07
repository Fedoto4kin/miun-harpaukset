<template>
  <component
    :is="getComponent(exercise.exercise_type)"
    :exercise="exercise"
    v-if="getComponent(exercise.exercise_type)"
  />
</template>

<script>
import FillBlankExercise from './FillBlankExerciseComponent.vue';
import SyllableAssemblyExercise from './SyllableAssemblyExerciseComponent.vue';
import FillBlankTextExercise from './FillBlankTextExerciseComponent.vue';
import SentenceAssemblyExercise from './SentenceAssemblyExerciseComponent.vue';

export default {
  name: 'ExerciseFactory',
  props: {
    exercise: {
      type: Object,
      required: true,
    },
  },
  methods: {
    getComponent(type) {
      switch (type) {
        case 'FillBlank':
          return FillBlankExercise;
        case 'SyllableAssembly':
          return SyllableAssemblyExercise;
        case 'FillBlankText':
          return FillBlankTextExercise;
        case 'SentenceAssembly':
          return SentenceAssemblyExercise;
        default:
          return null;
      }
    },
  },
};
</script>
