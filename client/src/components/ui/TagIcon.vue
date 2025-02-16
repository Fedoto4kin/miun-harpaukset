<template>
  <VTooltip :distance="16" placement="bottom" :disabled="disabled" >
    <font-awesome-icon :icon="getTagIcon(tagCode)" class="custom-icon" />
    <template #popper>
      <span class="px-1 title">&bullet;&nbsp;{{ tagName }}</span>
      <ul class="my-0 list-unstyled">
        <li>
          <span><img :src="'/img/ru-xs.png'" alt="ru" class="me-2" />{{ hintRussian }}</span>
        </li>
        <li>
          <span><img :src="'/img/fi-xs.png'" alt="fi" class="me-2" />{{ hintFinnish }}</span>
        </li>
      </ul>
    </template>
  </VTooltip>
</template>

<script>
export default {
  name: 'TagIcon',
  props: {
    tagCode: {
      type: String,
      required: true,
    },
    hintFinnish: {
      type: String,
      required: true,
    },
    hintRussian: {
      type: String,
      required: true,
    },
    tagName: {
      type: String,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    getTagIcon(tagCode) {
      const tagIcons = {
        grammar: ['fas', 'exclamation-triangle'],
        tell: ['fas', 'comment'],
        vocabulary: ['fas', 'book'],
        dialogue: ['fas', 'comments'],
        remember: ['fas', 'brain'],
        proverbs: ['fas', 'book-open-reader'],
        task: ['fas', 'question-circle'],
        game: ['fas', 'face-grin-stars'],
        read: ['fas', 'book-open'],
        sing: ['fas', 'music'],
        write: ['fas', 'pencil-alt'],
        smile: ['fas', 'smile'],
        listen: ['fas', 'headphones'],
        test: ['fas', 'tasks'],
        key: ['fas', 'key'],
      };
      return tagIcons[tagCode] || ['fas', 'question-circle'];
    },
  },
};
</script>

<style scoped>
.custom-icon {
  font-size: 1.5em;
  margin-right: 0.5rem;
  color: #495057;

}

.title {
  font-size: large;
}

.v-popper {
  z-index: 99999999 !important;
}

</style>