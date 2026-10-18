<template>
  <div ref="stickyRoot" :class="['sticky-lesson', { 'compact': isCompact }]">
    <div class="d-flex align-items-center justify-content-between border-bottom px-2 py-2">
      <h4 class="mb-0">
        {{ lesson.full_name }}
      </h4>
      <button class="btn my-1 btn-outline-secondary" @click="showPopup = true" :class="[{ 'btn-sm': isCompact }]"
        title='Löydiä šanan šanakniigašta'>
        <font-awesome-icon :icon="['fas', 'book']" />
      </button>
    </div>
    <div class="d-flex align-items-center justify-content-between px-2 py-2 gap-2 module-toolbar flex-wrap">
      <div class="d-flex align-items-center gap-2 flex-shrink-1 min-w-0">
        <h5 class="mb-0 module-num">
          <span class="badge rounded-pill badge-lg bg-primary">{{ number }}</span>
        </h5>
        <span v-if="tags" class="d-flex gap-1">
          <span v-for="tag in tags" :key="tag.id">
            <TagIcon :tagCode="tag.code" :hintFinnish="tag.hint_finnish" :hintRussian="tag.hint_russian"
              :tagName="tag.name" />
          </span>
        </span>
        <div v-if="speech && showCompactControls" class="compact-audio d-flex align-items-center gap-1">
          <button type="button" class="btn btn-outline-primary btn-sm audio-btn"
            :title="isPlaying ? 'Pysäytä' : 'Šoita'" @click="togglePlay">
            <font-awesome-icon :icon="['fas', isPlaying ? 'pause' : 'play']" />
          </button>
          <button type="button" class="btn btn-outline-secondary btn-sm audio-btn" title="Lopeta"
            :disabled="!isPlaying && currentTime === 0" @click="stopAudio">
            <font-awesome-icon :icon="['fas', 'stop']" />
          </button>
        </div>
      </div>
      <div class="d-flex gap-2 flex-shrink-0">
        <button class="btn btn-primary btn-sm btn-extra-small"
          :style="{ visibility: hasPreviousModule ? 'visible' : 'hidden' }" @click="goToPreviousModule">
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'arrow-left']" class="text-primary" />
          </span>
          <span class="d-none d-md-inline">&nbsp;Tagah</span>
        </button>
        <button class="btn btn-primary btn-sm btn-extra-small" v-if="hasNextModule" @click="goToNextModule">
          <span class="d-none d-md-inline">Edeh&nbsp;</span>
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'arrow-right']" class="text-primary" />
          </span>
        </button>
        <button class="btn btn-success btn-sm" v-if="!hasNextModule && nextLesson" @click="goToNextLesson">
          <span class="d-none d-md-inline">{{ nextLesson?.full_name }}&nbsp;</span>
          <span class="badge badge-light bg-light">
            <font-awesome-icon :icon="['fas', 'right-from-bracket']" class="text-success" />
          </span>
        </button>
      </div>
    </div>
  </div>
  <!-- Вне sticky: большой плеер просто уезжает при прокрутке -->
  <div v-if="speech" ref="fullAudioSlot" class="full-audio-block"
    :class="{ 'full-audio-block--visible': showFullPlayer }">
    <audio ref="audioEl" class="lesson-audio" :class="{ 'lesson-audio--full': showFullPlayer }"
      :controls="showFullPlayer" preload="metadata" :key="speech" @play="isPlaying = true"
      @pause="isPlaying = false" @ended="onEnded" @timeupdate="onTimeUpdate" @loadedmetadata="onLoadedMeta">
      <source :src="speech" type="audio/mpeg" />
    </audio>
  </div>
  <WordSearchPopupComponent :show="showPopup" @close="showPopup = false" />
</template>

<script>
import TagIcon from '@/components/ui/TagIcon.vue';
import WordSearchPopupComponent from './WordSearchPopupComponent.vue';

const WIDE_MQ = '(min-width: 768px)';

export default {
  name: 'LessonHeaderComponent',
  components: {
    WordSearchPopupComponent,
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
    speech: String,
  },
  data() {
    return {
      showPopup: false,
      isCompact: false,
      isWide: false,
      isPlaying: false,
      currentTime: 0,
      duration: 0,
      mediaQuery: null,
    };
  },
  computed: {
    // Desktop at top of page: full native player
    showFullPlayer() {
      return !!this.speech && this.isWide && !this.isCompact;
    },
    // Mobile always, or desktop while sticky-scrolled
    showCompactControls() {
      return !!this.speech && (!this.isWide || this.isCompact);
    },
  },
  watch: {
    speech() {
      this.isPlaying = false;
      this.currentTime = 0;
      this.duration = 0;
    },
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll, { passive: true });
    this.mediaQuery = window.matchMedia(WIDE_MQ);
    this.isWide = this.mediaQuery.matches;
    if (this.mediaQuery.addEventListener) {
      this.mediaQuery.addEventListener('change', this.onViewportChange);
    } else {
      this.mediaQuery.addListener(this.onViewportChange);
    }
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll);
    if (this.mediaQuery) {
      if (this.mediaQuery.removeEventListener) {
        this.mediaQuery.removeEventListener('change', this.onViewportChange);
      } else {
        this.mediaQuery.removeListener(this.onViewportChange);
      }
    }
    this.stopAudio();
  },
  methods: {
    onViewportChange(event) {
      this.isWide = event.matches;
    },
    handleScroll() {
      const offset = window.pageYOffset || document.documentElement.scrollTop || 0;
      if (!this.isCompact && offset > 120) {
        this.setCompact(true);
      } else if (this.isCompact && offset < 40) {
        this.setCompact(false);
      }
    },
    setCompact(next) {
      if (this.isCompact === next) return;
      const slot = this.$refs.fullAudioSlot;
      const before = slot?.offsetHeight || 0;
      this.isCompact = next;
      this.$nextTick(() => {
        if (!this.isWide) return;
        const after = slot?.offsetHeight || 0;
        const delta = before - after;
        if (delta) {
          window.scrollBy(0, delta);
        }
      });
    },
    togglePlay() {
      const audio = this.$refs.audioEl;
      if (!audio) return;
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
    },
    stopAudio() {
      const audio = this.$refs.audioEl;
      if (!audio) return;
      audio.pause();
      audio.currentTime = 0;
      this.isPlaying = false;
      this.currentTime = 0;
    },
    onEnded() {
      this.isPlaying = false;
      this.currentTime = 0;
    },
    onTimeUpdate(event) {
      this.currentTime = event.target.currentTime || 0;
    },
    onLoadedMeta(event) {
      this.duration = event.target.duration || 0;
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
}

.sticky-lesson.compact {
  font-size: 0.8rem;
}

.sticky-lesson.compact .btn-extra-small {
  padding: 0.1rem 0.3rem;
  font-size: 0.75rem;
}

.sticky-lesson.compact h4,
.sticky-lesson.compact h3,
.sticky-lesson.compact h5 {
  font-size: 1rem;
}

.module-toolbar {
  min-height: 2.5rem;
}

.full-audio-block {
  display: none;
  justify-content: center;
  padding: 0.35rem 0.5rem 0.5rem;
  background: white;
}

.full-audio-block--visible {
  display: flex;
}

.lesson-audio {
  display: none;
}

.lesson-audio--full {
  display: block;
  width: min(100%, 28rem);
}

.audio-btn {
  width: 2rem;
  height: 2rem;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  line-height: 1;
}

.sticky-lesson.compact .audio-btn {
  width: 1.75rem;
  height: 1.75rem;
  font-size: 0.75rem;
}

@media (min-width: 992px) {
  .full-audio-block--visible .lesson-audio--full {
    transform: scale(0.9);
    transform-origin: center top;
  }
}

@media (max-width: 575.98px) {
  .audio-btn {
    width: 2.25rem;
    height: 2.25rem;
  }
}
</style>
