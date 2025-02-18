<template>
  <component
    :is="getComponent(exercise.exercise_type)"
    :data="exercise.data"
    :hasCheck="exercise.has_answers_check"
    v-if="getComponent(exercise.exercise_type)"
  />
</template>

<script>
import FillBlankExercise from './variants/FillBlankExerciseComponent.vue';
import SyllableAssemblyExercise from './variants/SyllableAssemblyExerciseComponent.vue';
import FillBlankTextExercise from './variants/FillBlankTextExerciseComponent.vue';
import SentenceAssemblyExercise from './variants/SentenceAssemblyExerciseComponent.vue';
import SentenceAssemblyPrefilledExercise from './variants/SentenceAssemblyPrefilledComponent.vue';
import MatchPairExercise from './variants/MatchPairExerciseComponent.vue';
import FillBlankTableExercise from './variants/FillBlankTableExerciseComponent.vue';
import FillGapWithChoiceExercise from './variants/FillGapWithChoiceExerciseComponent.vue';
import FillWordExercise from './variants/FillWordExerciseComponent.vue';

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
        case 'SentenceAssemblyPrefilled':
          return SentenceAssemblyPrefilledExercise;  
        case 'MatchPair':
          return MatchPairExercise;
        case 'FillBlankTable':
          return FillBlankTableExercise;
        case 'FillGapWithChoice':
          return FillGapWithChoiceExercise;
        case 'FillWord':
          return FillWordExercise;
        default:
          return null;
      }
    },
  },
};
</script>
