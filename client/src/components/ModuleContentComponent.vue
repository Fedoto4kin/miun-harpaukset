<template>
  <div>
    <div class="module-navigation d-flex justify-content-between mb-4">
      <button 
        class="btn btn-primary"
        :style="{ visibility: hasPreviousModule ? 'visible' : 'hidden' }"
        @click="goToPreviousModule"
      >
        <span class="badge badge-light bg-light">
          <font-awesome-icon :icon="['fas', 'arrow-left']" class="text-primary" />
        </span>
        Tagah
      </button>
      <button 
        class="btn btn-primary"
        :style="{ visibility: hasNextModule ? 'visible' : 'hidden' }"
        @click="goToNextModule"
      >
        Edeh 
        <span class="badge badge-light bg-light">
          <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-primary" />
        </span>
      </button>
    </div>
    <div class="lesson-content" v-if="moduleData.html_content">
      <div v-html="moduleData.html_content"></div>
      <div v-if="moduleData.speech" class="mt-4">
        <div class="mb-3 d-flex justify-content-center">
          <audio controls class="audio-player" :key="moduleData.speech">
            <source :src="moduleData.speech" type="audio/mpeg" />
          </audio>
        </div>
      </div>
      <div v-if="moduleData.exercises && moduleData.exercises.length > 0" class="exercise-container mt-4">
        <ExerciseFactory 
          v-for="(exercise, index) in moduleData.exercises" 
          :key="index" 
          :exercise="exercise" 
        />
      </div>
    </div>
    <div class="lesson-content" v-else>
      ...tulošša piäh
    </div>
  </div>
</template>

<script>
import ExerciseFactory from '@/components/exercises/ExerciseFabricComponent.vue';

export default {
  name: 'ModuleContentComponent',
  components: {
    ExerciseFactory,
  },
  props: {
    moduleData: {
      type: Object,
      required: true,
    },
    hasPreviousModule: {
      type: Boolean,
      required: true,
    },
    hasNextModule: {
      type: Boolean,
      required: true,
    },
  },
  methods: {
    goToPreviousModule() {
      this.$emit('previous-module');
    },
    goToNextModule() {
      this.$emit('next-module');
    },
  },
};
</script>

<style scoped>
.audio-player {
  width: 100%;
}
</style>