<template>
  <div class="container pb-5">
    <div class="row">
      <div class="col-3" id="lesson-list">
        <h1 class="mt-2 mb-4">
          <font-awesome-icon :icon="['fas', 'star']" class="text-success" />
          {{ title }}
        </h1>
        <div v-if="loading">
          <h3>
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
                  <div v-if="modulesLoading">
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
      </div>
      <div class="col-9 mt-2" id="lesson-frame">
        <div class="sticky-lesson pt-3">  
          <div v-if="activeLesson" class="text-center position-relative">
            <div v-if="activeLesson.speech" class="audio-container">
              <audio controls class="audio-player" :key="activeLesson.id">
                <source :src="activeLesson.speech" type="audio/mpeg" />
              </audio>
            </div>
            <h4 class="border-bottom pb-2 shift-left">
              {{ activeLesson.full_name }}
            </h4>
            <h3 class="shift-left">
              {{ activeLesson.slogan }}
            </h3>
          </div>
        </div>
        <div v-if="!modulesLoading" class="mt-5 mx-5">
          <div class="lesson-content" 
               v-if="moduleData.html_content" 
               v-html="moduleData.html_content">
          </div>
          <div class="lesson-content" v-else>
          ...tulošša piäh
          </div>
          <div v-if="moduleData && moduleData.speech" class="mt-4">
          <div class="mb-3">
            <audio controls class="audio-player" :key="moduleData.speech">
              <source :src="moduleData.speech" type="audio/mpeg" />
            </audio>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { getLessons, getModulesByLesson, getModuleContent } from '../services/lessonsService.js';
import ModuleList from '@/components/ModuleListComponent.vue'; 

export default {
  name: 'LessonsComponent',
  components: {
    FontAwesomeIcon,
    ModuleList,
  },
  data() {
    return {
      title: 'Urokat',
      loading: true,
      lessons: [],
      activeLesson: null,
      modules: [],
      modulesLoading: false,
      selectedModuleId: null,
      moduleData: {
        html_content: null,
        speech: null,
      }, 
    };
  },
  async mounted() {
    document.title = 'Urokat';
    try {
      this.lessons = await getLessons();
      this.handleRoute();
    } catch (error) {
      console.error('Error loading lessons:', error);
    } finally {
      this.loading = false;
    }
  },
  watch: {
    '$route.params.id': 'handleRoute',
  },
  methods: {
    isLessonActive(lesson) {
      return this.activeLesson && this.activeLesson.id === lesson.id;
    },
    toggleLesson(lesson) {
      if (this.isLessonActive(lesson)) {
        return;
      }
      this.setActiveLesson(lesson);
    },
    setActiveLesson(lesson) {
      const audioElement = document.querySelector('.audio-player');
      if (audioElement) {
        audioElement.pause();
        audioElement.currentTime = 0;
      }

      this.activeLesson = lesson;
      this.$router.push({ path: `/lessons/${lesson.number}` });
    },
    handleRoute() {
      const lessonId = this.$route.params.id;
      if (!lessonId) {
        this.$router.replace({ path: '/lessons/1' });
      } else {
        const lesson = this.lessons.find((lesson) => lesson.number == lessonId);
        if (!lesson || !lesson.is_enabled) {
          this.$router.replace({ path: '/lessons/1' });
        } else {
          this.activeLesson = lesson;
          this.loadModules();
        }
      }
    },
    async loadModules() {
      if (!this.activeLesson) return;

      this.modulesLoading = true;
      try {
        this.modules = await getModulesByLesson(this.activeLesson.id);

        if (this.modules.length > 0) {
          await this.loadModuleContent(this.modules[0].id);
        } else {
          this.selectedModuleId = null;
          this.moduleData = {};
        }
      } catch (error) {
        console.error('Error loading modules:', error);
      } finally {
        this.modulesLoading = false;
      }
    },
    async loadModuleContent(moduleId) {
      try {
        const response = await getModuleContent(moduleId);
        this.moduleData = {
          html_content: response.html_content,
          speech: response.speech || null,
        };
        this.selectedModuleId = moduleId;
      } catch (error) {
        console.error('Error loading module content:', error);
        this.moduleData = {}
        this.selectedModuleId = null;
      }
    },
    formatDescription(lesson) {
      return lesson.number + '. ' + lesson.description.replace(/\n/g, '<br>');
    },
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.fa-spinner {
  margin-right: 16px;
}

.accordion-button {
  font-weight: bold;
  background-color: #d4edda; /* Green color for accordion button */
  color: #155724; /* Dark green text color */
  display: flex;
  align-items: flex-start;
  padding: 1rem;
}

.accordion-button:not(.collapsed) {
  background-color: #fff3cd; /* Yellow color for active button */
  color: #856404; /* Dark yellow text color */
}

.accordion-button.disabled {
  background-color: #f8f9fa; /* Gray color for disabled button */
  color: #6c757d; /* Gray text color */
  cursor: not-allowed;
}

.accordion-body {
  background-color: #f8f9fa; /* Light background for accordion body */
}

.accordion-button h5 {
  margin-bottom: 0.25rem;
}

.accordion-button small {
  font-size: 0.875rem;
  color: #6c757d; /* Gray text color */
}

.audio-container {
  position: absolute;
  right: 0;
  top: -0.5rem;
  width: 22em; 
  z-index: 1000;
}

.audio-player {
  width: 100%;
  transform: scale(0.75); 
  transform-origin: top left; 
}

.sticky-lesson {
  position: sticky;
  top: 0;
  overflow-y: auto;
  background-color: #fff;
}

#lesson-list {
  height: calc(100vh); 
  overflow-y: auto;
}

.lesson-content {
  margin-top: 0.5rem;
  padding-left: 1.5rem;
}
.shift-left {
  transform: translateX(-12%);
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
  background-color: white !important; /* Белый фон для активного элемента */
  font-weight: bold; /* Жирный шрифт для активного элемента */
}

.custom-badge {
  font-size: 0.9rem; /* Уменьшаем размер шрифта в 2 раза */
  padding: 0.25rem 0.5rem; /* Уменьшаем отступы в 2 раза */
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075); /* Тень для badge */
}
</style>