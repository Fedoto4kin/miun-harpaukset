<template>
  <component
    :is="getComponent(exercise.exercise_type)"
    :data="exercise.data"
    :hasCheck="exercise.has_answers_check"
    v-if="getComponent(exercise.exercise_type)"
  />
</template>

<script>
import FillBlankExercise from './FillBlankExerciseComponent.vue';
import SyllableAssemblyExercise from './SyllableAssemblyExerciseComponent.vue';
import FillBlankTextExercise from './FillBlankTextExerciseComponent.vue';
import SentenceAssemblyExercise from './SentenceAssemblyExerciseComponent.vue';
import SentenceAssemblyPrefilledExercise from './SentenceAssemblyPrefilledComponent.vue';
import MatchPairExercise from './MatchPairExerciseComponent.vue';
import FillBlankTableExercise from './FillBlankTableExerciseComponent.vue';
import FillGapWithChoiceExercise from './FillGapWithChoiceExerciseComponent.vue'; // Новый компонент

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
        case 'FillGapWithChoice': // Новый тип задания
          return FillGapWithChoiceExercise;
        default:
          return null;
      }
    },
  },
};
</script>