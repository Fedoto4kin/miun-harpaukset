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
      </div>
      <div class="col-9 mt-2" id="lesson-frame">
        <div class="sticky-lesson pt-5">  
          <LessonHeaderComponent :lesson="activeLesson" v-if="activeLesson" />
        </div>
        <div v-if="!isContentLoading" class="mt-5 mx-5">
          <ModuleContentComponent
            :moduleData="moduleData"
            :hasPreviousModule="hasPreviousModule"
            :hasNextModule="hasNextModule"
            :nextLesson="nextLesson"
            :previousLesson="previousLesson"
            @previous-module="goToPreviousModule"
            @next-module="goToNextModule"
            @next-lesson="goToNextLesson"
            @previous-lesson="goToPreviousLesson"
          />
        </div>
        <div v-else>
          <h3 class="text-center">
            <font-awesome-icon :icon="['fas', 'spinner']" spin />
          </h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { getLessons, getModulesByLesson, getModuleContent } from '../services/lessonsService.js';
import ModuleList from '@/components/ModuleListComponent.vue'; 
import ModuleContentComponent from '@/components/ModuleContentComponent.vue';
import LessonHeaderComponent from '@/components/LessonHeaderComponent.vue';

export default {
  name: 'LessonsComponent',
  components: {
    FontAwesomeIcon,
    ModuleList,
    ModuleContentComponent,
    LessonHeaderComponent,
  },
  data() {
    return {
      title: 'Urokat',
      loading: true,
      lessons: [],
      activeLesson: null,
      modules: [],
      isContentLoading: false,
      isModulesByLessonLoading: false,
      
      selectedModuleId: null,
      nextLesson: null,
      previousLesson: null,
      moduleData: {
        html_content: null,
        speech: null,
        exercises: null
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
  computed: {
    currentModuleIndex() {
      return this.modules.findIndex(module => module.id === this.selectedModuleId);
    },
    hasPreviousModule() {
      return this.currentModuleIndex > 0;
    },
    hasNextModule() {
      return this.currentModuleIndex < this.modules.length - 1;
    },
  },
  watch: {
    '$route.params.id': 'handleRoute',
  },
  methods: {
    isLessonActive(lesson) {
      return (this.activeLesson && this.activeLesson.id === lesson.id);
    },
    getLessonIndex() {
      return this.lessons.findIndex(lesson => lesson.id === this.activeLesson.id);
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
      const currentLessonIndex = this.getLessonIndex();
      this.nextLesson = this.checkLessonIsEnable(this.lessons[currentLessonIndex + 1]) ?
                        this.lessons[currentLessonIndex + 1] : 
                        null;
      this.$router.push({ path: `/lessons/${lesson.number}` });
    },
    handleRoute() {
      const lessonId = this.$route.params.id;
      const moduleId = this.$route.params.moduleId;
      if (!lessonId) {
        this.$router.replace({ path: '/lessons/1' });
      } else {
        const lesson = this.lessons.find((lesson) => lesson.number == lessonId);
        if (!lesson || !lesson.is_enabled) {
          this.$router.replace({ path: '/lessons/1' });
        } else {
            this.setActiveLesson(lesson);
            this.loadModules().then(() => {
              if (this.modules.length === 0) {
                this.isContentLoading = false;
                return;
              }
              const moduleExists = this.modules.some(module => module.id == moduleId);
              if (moduleId && moduleExists) {
                this.loadModuleContent(moduleId);
              } else  {
                this.loadModuleContent(this.modules[0].id);
              }
            }
          );
        } 
      }
    },
    async loadModules() {
      if (!this.activeLesson) return;
      this.isModulesByLessonLoading = true;
      this.isContentLoading = true;
      try {
        this.selectedModuleId = null;
        this.moduleData = {};
        this.modules = await getModulesByLesson(this.activeLesson.id);
      } catch (error) {
        console.error('Error loading modules:', error);
      } finally {
        this.isModulesByLessonLoading = false;
      }
    },
    async loadModuleContent(moduleId) {
      this.isContentLoading = true;
      try {
        this.selectedModuleId = Number(moduleId);
        this.$router.replace({path: `/lessons/${this.activeLesson.id}/${this.selectedModuleId}`});
        this.moduleData = {
          html_content: null,
          speech: null,
          exercises: null
        };
        const response = await getModuleContent(moduleId);
        this.moduleData = {
          html_content: response.html_content,
          speech: response.speech || null,
          exercises: response.exercises || null
        };
      } catch (error) {
        console.error('Error loading module content:', error);
        this.moduleData = {}
        this.selectedModuleId = null;
      } finally {
        this.isContentLoading = false;
      }

    },
    formatDescription(lesson) {
      return lesson.number + '. ' + lesson.description.replace(/\n/g, '<br>');
    },
    goToPreviousModule() {
      if (this.hasPreviousModule) {
        const previousModuleId = this.modules[this.currentModuleIndex - 1].id;
        this.loadModuleContent(previousModuleId);
      }
    },
    goToNextModule() {
      if (this.hasNextModule) {
        const nextModuleId = this.modules[this.currentModuleIndex + 1].id;
        this.loadModuleContent(nextModuleId);
      }
    },
    goToNextLesson() {
      const currentLessonIndex = this.getLessonIndex();
      const nextLesson = this.lessons[currentLessonIndex + 1];
      if (currentLessonIndex >= 0 && currentLessonIndex < this.lessons.length - 1) {        
        if (nextLesson.is_enabled) {
          this.setActiveLesson(nextLesson);
          this.loadModules();
        }
      }
    },
    goToPreviousLesson() {
      const currentLessonIndex = this.getLessonIndex();
      const previousLesson = this.lessons[currentLessonIndex - 1];
      if (currentLessonIndex > 0) {
        if (previousLesson.is_enabled) {
          this.setActiveLesson(previousLesson);
          this.loadModules();
        }
      }
    },
    checkLessonIsEnable(lesson) {
      if (lesson) {
        return lesson.is_enabled;
      }
      return false;
    },
    
  },
};
</script>

<style scoped>
.container {
  margin-top: 20px;
}

.sticky-lesson {
  z-index: 999;
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