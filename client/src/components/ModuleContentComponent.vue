<template>
  <div>
    <div class="module-navigation d-flex justify-content-between mb-4">
      {{ hasPreviousLesson }}
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
      <button 
        class="btn btn-success"
        v-if="!hasNextModule && nextLesson"
        @click="goToNextLesson"
      >{{ nextLesson?.full_name }}
      <span class="badge badge-light bg-light">
        <font-awesome-icon :icon="['fas', 'right-from-bracket']" class="text-success" />
      </span>
      </button>
    </div>
    <div class="lesson-content" v-if="moduleData.html_content">
      <div v-html="moduleData.html_content"></div>
      <div v-if="moduleData.exercises && moduleData.exercises.length > 0" class="exercise-container mt-2">
        <ExerciseFactory 
          v-for="(exercise, index) in moduleData.exercises" 
          :key="index" 
          :exercise="exercise" 
        />
      </div>
      <div v-if="moduleData.speech" class="mt-4">
        <div class="mb-3 d-flex justify-content-center">
          <audio controls class="audio-player" :key="moduleData.speech">
            <source :src="moduleData.speech" type="audio/mpeg" />
          </audio>
        </div>
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
    moduleData: Object,
    hasPreviousModule: Boolean,
    hasNextModule: Boolean,
    nextLesson: Object,
    previousLesson: Object,
  },
  methods: {
    goToPreviousModule() {
      this.$emit('previous-module');
    },
    goToNextModule() {
      this.$emit('next-module');
    },
    goToNextLesson() {
      this.$emit('next-lesson');
    },
    goToPreviousLesson() {
      this.$emit('previous-lesson');
    },
  },
};
</script>

<style scoped>
.audio-player {
  width: 100%;
}
</style>
