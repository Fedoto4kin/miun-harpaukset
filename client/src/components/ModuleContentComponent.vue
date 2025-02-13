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
        <div v-if="speech" class="mt-4">
          <div class="mb-3 d-flex justify-content-center">
            <audio controls class="audio-player" :key="speech">
              <source :src="speech" type="audio/mpeg" />
            </audio>
          </div>
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
    html_content: String,
    speech: String,
    exercises: Array,
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

.lesson-content {
  overflow-x: auto;
}

.content-container {
  display: flex;
  flex-direction: column;
}

.exercise-container {
  min-width: 650px;
}

@media (max-width: 600px) {
  .module-navigation button {
    font-size: 0.8rem;
  }
}
</style>
