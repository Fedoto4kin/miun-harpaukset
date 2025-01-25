<template>
    <VTooltip>
        <font-awesome-icon :icon="getTagIcon(tagCode)" class="custom-icon" />
        <template #popper>
            <ul class="my-0 list-unstyled">
                <li>
                    <span><img :src="'/img/ru-xs.png'" :alt="lang" class="me-2" />{{ hintRussian }}</span>
                </li>
                <li>
                    <span><img :src="'/img/fi-xs.png'" :alt="lang" class="me-2" />{{ hintFinnish }}</span>
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
  </style>