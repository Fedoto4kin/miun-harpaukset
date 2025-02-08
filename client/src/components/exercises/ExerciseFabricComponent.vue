<template>
  <component
    :is="getComponent(exercise.exercise_type)"
    :data="exercise.data"
    v-if="getComponent(exercise.exercise_type)"
  />
</template>

<script>
import FillBlankExercise from './FillBlankExerciseComponent.vue';
import SyllableAssemblyExercise from './SyllableAssemblyExerciseComponent.vue';
import FillBlankTextExercise from './FillBlankTextExerciseComponent.vue';
import SentenceAssemblyExercise from './SentenceAssemblyExerciseComponent.vue';
import MatchPairExercise from './MatchPairExerciseComponent.vue';

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
        case 'MatchPair':
          return MatchPairExercise;
        default:
          return null;
      }
    },
  },
};
</script>
