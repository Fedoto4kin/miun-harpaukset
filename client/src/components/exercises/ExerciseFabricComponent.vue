<template>
    <component :is="exerciseComponent" :exercise="exercise" />
  </template>
  
  <script>
  import FillBlankExercise from './FillBlankExerciseComponent.vue';
  
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
          // Добавьте другие типы заданий здесь
          default:
            return null;
        }
      },
    },
  };
  </script>