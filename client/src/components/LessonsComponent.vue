<template>
  <div class="container-lg pb-5">
    <div class="row">
      <LessonListComponent :title="title" :loading="loading" :lessons="lessons" :isLessonActive="isLessonActive"
        :toggleLesson="toggleLesson" :formatDescription="formatDescription"
        :isModulesByLessonLoading="isModulesByLessonLoading" :modules="modules" :selectedModuleId="selectedModuleId"
        @module-clicked="loadModuleContent" />
      <div class="col-lg-9 col-sm-12 mt-2" id="lesson-frame">
        <LessonHeaderComponent :lesson="activeLesson" 
                                v-bind="filterModuleData(['number', 'tags'])"
                                v-if="activeLesson"
                                :hasPreviousModule="hasPreviousModule" 
                                :hasNextModule="hasNextModule" 
                                :nextLesson="nextLesson"
                                :previousLesson="previousLesson" 
                                @previous-module="goToPreviousModule" 
                                @next-module="goToNextModule"
                                @next-lesson="goToNextLesson" 
                                @previous-lesson="goToPreviousLesson"
                                 />
        <div v-if="activeLesson && !isContentLoading && moduleData.html_content" class="mt-md-5 mx-md-5">
          <ModuleContentComponent v-bind="filterModuleData(['html_content', 'exercises', 'speech'])" />
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
import { createApp, h } from 'vue';
import { getLessons, getModulesByLesson, getModuleContent } from '../services/lessonsService.js';
import ModuleContentComponent from '@/components/ModuleContentComponent.vue';
import LessonHeaderComponent from '@/components/LessonHeaderComponent.vue';
import LessonListComponent from '@/components/LessonListComponent.vue';
import LessonCoverContent from '@/components/LessonCoverContentComponent.vue';

export default {
  name: 'LessonsComponent',
  components: {
    ModuleContentComponent,
    LessonHeaderComponent,
    LessonListComponent,
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
        exercises: null,
        tags: [],
        number: null,
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
            } else {
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
        this.$router.replace({ path: `/lessons/${this.activeLesson.id}/${this.selectedModuleId}` });
        this.moduleData = {
          number: null,
          html_content: null,
          speech: null,
          exercises: null,
          tags: []
        };
        const response = await getModuleContent(moduleId);
        this.moduleData = this.buildModuleData(response);
      } catch (error) {
        console.error('Error loading module content:', error);
        this.moduleData = {}
        this.selectedModuleId = null;
      } finally {
        this.isContentLoading = false;
      }
    },

    buildModuleData(response) {
      if (response.html_content.includes('[[widget:lesson_cover]]')) {
        const tempContainer = document.createElement('div');
        const app = createApp({
          render: () => h(LessonCoverContent, { lesson: this.activeLesson }),
        });
        app.mount(tempContainer);
        const htmlContent = tempContainer.innerHTML;
        app.unmount();

        return {
          html_content: htmlContent,
          speech: this.activeLesson.speech,
          exercises: null,
          tags: [],
          number: response.number || null,
        };
      }

      return {
        html_content: response.html_content,
        speech: response.speech || null,
        exercises: response.exercises || null,
        tags: response.tags || [],
        number: response.number || null,
      };
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
    filterModuleData(keys) {
      if (this.moduleData === null) {
        return null;
      }
      const filteredData = {};
      keys.forEach(key => {
        if (key in this.moduleData) {
          filteredData[key] = this.moduleData[key];
        }
      });
      return filteredData;
    }

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

.sticky-lesson {
  position: sticky;
  top: 0;
  overflow-y: auto;
  background-color: #fff;
}
</style>
