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
          <div class="accordion" id="lessonsAccordion">
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
                    <h5 class="mb-2">{{ lesson.full_name }}</h5>
                    <small class="text-muted" v-html="formatDescription(lesson.description)"></small>
                  </div>
                </button>
              </h2>
              <div
                :id="'collapse' + lesson.id"
                class="accordion-collapse collapse"
                :class="{ show: isLessonActive(lesson) }"
                :aria-labelledby="'heading' + lesson.id"
              >
                <div class="accordion-body" v-if="lesson.is_enabled">
                  <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                  </ul>
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
                Your browser does not support the audio tag.
              </audio>
            </div>
            <h4 class="border-bottom pb-2 shift-left">
              {{ activeLesson.full_name }}
            </h4>
            <h3 class="shift-left">
              {{ activeLesson.slogan }}
            </h3>
          </div>
          <div v-else>
            <h1>...tulošša piäh</h1>
          </div>
        </div>
        <div class="lesson-content">
            Here we are
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { getLessons } from '../services/lessonsService.js';

export default {
  name: 'LessonsComponent',
  components: {
    FontAwesomeIcon,
  },
  data() {
    return {
      title: 'Urokat',
      loading: true,
      lessons: [],
      activeLesson: null, // Store the active lesson as an object
    };
  },
  async mounted() {
    document.title = 'Urokat';
    try {
      this.lessons = await getLessons(); // Fetch lessons asynchronously
      this.handleRoute(); // Handle route after lessons are loaded
    } catch (error) {
      console.error('Error loading lessons:', error);
    } finally {
      this.loading = false; // Finish loading
    }
  },
  watch: {
    // Watch for changes in the route
    '$route.params.id': 'handleRoute',
  },
  methods: {
    // Check if the lesson is active
    isLessonActive(lesson) {
      return this.activeLesson && this.activeLesson.id === lesson.id;
    },
    // Toggle lesson (open/close)
    toggleLesson(lesson) {
      if (this.isLessonActive(lesson)) {
        // If the lesson is already active, do nothing (prevent collapsing)
        return;
      }
      this.setActiveLesson(lesson);
    },
    // Set the active lesson
    setActiveLesson(lesson) {
      // Остановить текущее аудио, если оно воспроизводится
      const audioElement = document.querySelector('.audio-player');
      if (audioElement) {
        audioElement.pause();
        audioElement.currentTime = 0; // Сбросить время воспроизведения
      }

      this.activeLesson = lesson;
      this.$router.push({ path: `/lessons/${lesson.num}` });
    },
    // Handle route changes
    handleRoute() {
      const lessonId = this.$route.params.id;
      if (!lessonId) {
        // Redirect to the first lesson if no ID is provided
        this.$router.replace({ path: '/lessons/1' });
      } else {
        const lesson = this.lessons.find((lesson) => lesson.num == lessonId);
        if (!lesson || !lesson.is_enabled) {
          // Redirect to the first lesson if the lesson doesn't exist or is disabled
          this.$router.replace({ path: '/lessons/1' });
        } else {
          this.activeLesson = lesson; // Set the active lesson
        }
      }
    },
    // Format description to replace newlines with <br>
    formatDescription(description) {
      return description.replace(/\n/g, '<br>');
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
  right: 0; /* Размещаем слева */
  top: -0.5rem;
  width: 18em; /* Ширина аудиоплеера */
  z-index: 1000;
}

.audio-player {
  width: 100%;
  transform: scale(0.75); /* Уменьшаем размер в 1.5 раза */
  transform-origin: top left; /* Масштабируем от верхнего левого угла */
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
</style>