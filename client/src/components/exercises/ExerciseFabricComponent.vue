<template>
    <component :is="exerciseComponent" :exercise="exercise" />
  </template>
  
  <script>
  import FillBlankExercise from './FillBlankExerciseComponent.vue';
  import SyllableAssemblyExercise from './SyllableAssemblyExerciseComponent.vue';
  import FillBlankTextExercise from './FillBlankTextExerciseComponent.vue';
  
  export default {
    name: 'ExerciseFactory',
    props: {
      exercise: {
        type: Object,
        required: true,
      },
    },
    computed: {
      exerciseComponent() {
        switch (this.exercise.exercise_type) {
          case 'FillBlank':
            return FillBlankExercise;
          case 'SyllableAssembly':
            return SyllableAssemblyExercise;
          case 'FillBlankText':
            return FillBlankTextExercise;
          default:
            return null;
        }
      },
    },
  };
  </script>