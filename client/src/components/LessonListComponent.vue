<template>
    <h1 class="mt-2 mb-4">
      <img src="/android-chrome-192x192.png" width="52" alt="">
      <span class="align-bottom">&nbsp;{{ title }}</span>
    </h1>
    <div v-if="loading">
      <h3 class="m-5">
        <font-awesome-icon :icon="['fas', 'spinner']" spin />
      </h3>
    </div>
    <div v-else>
      <div class="accordion pb-5" id="lessonsAccordion">
        <div class="accordion-item" v-for="lesson in lessons" :key="lesson.id">
          <h2 class="accordion-header" :id="'heading' + lesson.id">
            <button
              class="accordion-button"
              :class="{ collapsed: !isLessonActive(lesson), disabled: !lesson.is_enabled }"
              type="button"
              @click="toggleLesson(lesson)"
              :disabled="!lesson.is_enabled"
            >
              <div class="d-flex flex-column">
                <small class="text-muted" v-html="formatDescription(lesson)"></small>
              </div>
            </button>
          </h2>
          <div
            :id="'collapse' + lesson.id"
            class="accordion-collapse collapse"
            :class="{ show: isLessonActive(lesson) }"
            :aria-labelledby="'heading' + lesson.id"
          >
            <div class="accordion-body p-0" v-if="lesson.is_enabled">
              <div v-if="isModulesByLessonLoading">
                <font-awesome-icon :icon="['fas', 'spinner']" spin />
              </div>
              <ModuleList
                v-else
                :modules="modules"
                :selected-module-id="selectedModuleId"
                @module-clicked="loadModuleContent"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import ModuleList from '@/components/ModuleListComponent.vue';

export default {
  name: 'LessonListComponent',
  components: {
    FontAwesomeIcon,
    ModuleList,
  },
  props: {
    title: String,
    loading: Boolean,
    lessons: Array,
    isLessonActive: Function,
    toggleLesson: Function,
    formatDescription: Function,
    isModulesByLessonLoading: Boolean,
    modules: Array,
    selectedModuleId: Number,
  },
  methods: {
    loadModuleContent(moduleId) {
      this.$emit('module-clicked', moduleId);
    },
  },
};
</script>

<style scoped>

.accordion-button {
  font-weight: bold;
  background-color: #d4edda;
  /* Green color for accordion button */
  color: #155724;
  /* Dark green text color */
  display: flex;
  align-items: flex-start;
  padding: 1rem;
}

.accordion-button:not(.collapsed) {
  background-color: #fff3cd;
  /* Yellow color for active button */
  color: #856404;
  /* Dark yellow text color */
}

.accordion-button.disabled {
  background-color: #f8f9fa;
  /* Gray color for disabled button */
  color: #6c757d;
  /* Gray text color */
  cursor: not-allowed;
}

.accordion-body {
  background-color: #f8f9fa;
  /* Light background for accordion body */
}

.accordion-button h5 {
  margin-bottom: 0.25rem;
}

.accordion-button small {
  font-size: 0.875rem;
  color: #6c757d;
  /* Gray text color */
}

.list-group-item {
  cursor: pointer;
  border: none;
  background-color: #f8f9fa;
  transition: background-color 0.2s ease;
}

.list-group-item:hover {
  background-color: #e9ecef;
}

.active-module {
  background-color: white !important;
  font-weight: bold;
}

.custom-badge {
  font-size: 0.9rem;
  padding: 0.25rem 0.5rem;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
</style>