<template>
  <div :class="['sticky-lesson', { 'compact': isCompact }]">
    <!-- Верхний ряд: заголовок урока и кнопка поиска -->
    <div class="d-flex align-items-center justify-content-between border-bottom px-2 py-2">
      <h4 class="mb-0">
        {{ lesson.full_name }}
      </h4>
        <button class="btn my-1 btn-outline-secondary" 
                @click="showPopup = true" :class="[{'btn-sm' : isCompact }]"
                title='Löydiä šanan šanakniigašta'
        >
            <font-awesome-icon :icon="['fas', 'book']" />
        </button>
    </div>
    <div class="d-flex align-items-center justify-content-between px-2 py-2">
      <div class="d-flex align-items-center gap-2">
        <h5 class="mb-0">
          <span class="badge rounded-pill badge-lg bg-primary">{{ number }}</span>
        </h5>
        <span v-if="tags" class="d-flex gap-1">
          <span v-for="tag in tags" :key="tag.id">
            <TagIcon
              :tagCode="tag.code"
              :hintFinnish="tag.hint_finnish"
              :hintRussian="tag.hint_russian"
              :tagName="tag.name"
            />
          </span>
        </span>
      </div>
      <div class="d-flex gap-2">
        <button
          class="btn btn-primary btn-sm"
          :style="{ visibility: hasPreviousModule ? 'visible' : 'hidden' }"
          @click="goToPreviousModule"
        >
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'arrow-left']" class="text-primary" />
          </span>
          <span class="d-none d-md-inline">&nbsp;Tagah</span>
        </button>
        <button
          class="btn btn-primary btn-sm"
          :style="{ visibility: hasNextModule ? 'visible' : 'hidden' }"
          @click="goToNextModule"
        >
        <span class="d-none d-md-inline">Edeh&nbsp;</span>
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-primary" />
          </span>
        </button>
        <button
          class="btn btn-success btn-sm"
          v-if="!hasNextModule && nextLesson"
          @click="goToNextLesson"
        >
          {{ nextLesson?.full_name }}
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'right-from-bracket']" class="text-success" />
          </span>
        </button>
      </div>
    </div>
  </div>
  <SearchPopupComponent :show="showPopup" @close="showPopup = false" />
</template>

<script>
import SearchPopupComponent from './SearchPopupComponent.vue';
import TagIcon from './ui/TagIcon.vue';

export default {
  name: 'LessonHeaderComponent',
  components: {
    SearchPopupComponent,
    TagIcon,
  },
  props: {
    lesson: {
      type: Object,
      required: true,
    },
    number: Number,
    tags: Array,
    hasPreviousModule: Boolean,
    hasNextModule: Boolean,
    nextLesson: Object,
    previousLesson: Object,
  },
  data() {
    return {
      showPopup: false,
      isCompact: false,
    };
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
  },
  methods: {
    handleScroll() {
      const offset = window.pageYOffset;
      this.isCompact = offset > 150;
    },
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

.sticky-lesson {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  z-index: 55555;
  background: white;
  transition: all 0.3s ease;
}

.sticky-lesson.compact {
  padding: 0.5rem;
  font-size: 0.8rem;
}

.sticky-lesson.compact h4,
.sticky-lesson.compact h3 {
  font-size: 1rem;
}

.sticky-lesson.compact .audio-player {
  display: none;
}
</style>