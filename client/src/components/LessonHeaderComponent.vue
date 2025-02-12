<template>
  <div class="sticky-lesson">
    <div>
      <div class="d-flex align-items-center justify-content-between border-bottom px-2 mb-3">
        <h4 class="">
          {{ lesson.full_name }}
        </h4>
        <div v-if="lesson.speech" class="audio-container">
          <audio controls class="audio-player" :key="lesson.id">
            <source :src="lesson.speech" type="audio/mpeg" />
          </audio>
        </div>
      </div>
      <div class="d-flex align-items-center justify-content-between">
        <h3 class="px-3">
          {{ lesson.slogan }}
        </h3>
        <button class="btn mt-n1 btn-outline-secondary" @click="showPopup = true">
          <font-awesome-icon :icon="['fas', 'book']" />
        </button>
      </div>
      <SearchPopupComponent :show="showPopup" @close="showPopup = false" />
    </div>
    <div class="d-md-none d-block">
      <div class="px-3 mt-1 d-flex align-items-center justify-content-start gap-2">
          <h5><span class="badge rounded-pill badge-lg bg-primary"> {{ number }}</span></h5>
          <span>&nbsp;</span>
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
    </div>
  </div>
</template>

<script>
import SearchPopupComponent from './SearchPopupComponent.vue';
import TagIcon from './ui/TagIcon.vue';

export default {
  name: 'LessonHeaderComponent',
  components: {
    SearchPopupComponent,
    TagIcon
  },
  props: {
    lesson: {
      type: Object,
      required: true,
    },
    number: Number,
    tags: Array,
  },
  data() {
    return {
      showPopup: false,
    };
  },
};
</script>

<style scoped>
.audio-container {
  right: 0;
  top: -0.5rem;
  width: 22em;
  z-index: 1000;
}

.audio-player {
  width: 100%;
  transform: scale(0.75);
  transform-origin: top right;
}
</style>
