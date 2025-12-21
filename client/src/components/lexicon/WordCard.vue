<template>
  <div class="card">
    <div class="card-body">
      <p class="card-title d-flex justify-content-between align-items-center">
        <span class="d-flex align-items-center flex-wrap">
          <!-- Основное слово -->
          <span class="word-main">
            {{ word.word ? word.word.replace('|', '') : '' }}
          </span>
          <span v-if="word.additional" class="word-main">
            &nbsp;<i>(</i>{{ word.additional }}<i>)</i>
          </span>
          <span v-if="word.variant" class="text-muted variant ms-2">
            {{ word.variant }}
          </span>

          <!-- Часть речи с тултипом -->
          <VTooltip class="d-inline ms-2">
            <span class="badge bg-secondary align-middle">
              {{ word.pos }}
            </span>
            <template #popper>
              <ul class="my-0 list-unstyled">
                <li>🇫🇮 {{ word.pos_name_fi }}</li>
                <li>🇷🇺 {{ word.pos_name_ru }}</li>
              </ul>
            </template>
          </VTooltip>
        </span>

        <!-- Кнопка воспроизведения звука -->
        <button @click="playSound(word.speech)" :disabled="isPlaying"
          class="btn btn-sm btn-outline-primary align-self-start">
          <font-awesome-icon icon="volume-up" />
        </button>
      </p>

      <!-- Определения -->
      <ul class="list-group list-group-flush">
        <li v-for="(def, lang) in definition(word.definition)" :key="lang" class="list-group-item">
          <div class="d-flex align-items-center">
            <img :src="'/img/' + lang + '-xs.png'" :alt="lang" class="me-2" />
            <div class="definition-content">
              <span v-if="def.length > 1">
                <ol class="mb-0" style="margin-left: -1rem;">
                  <li v-for="d in def" :key="d">{{ d }}</li>
                </ol>
              </span>
              <span v-else class="ms-3">{{ def[0] }}</span>
            </div>
          </div>
        </li>
      </ul>

      <!-- Синонимы -->
      <div v-if="word.alias_words.length" class="mt-2">
        <span class='text-muted'>Šama kuin </span>
        <span v-for="al in alias(word.alias_words)" :key="al" class="badge bg-info me-1">{{ al }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'WordCard',
  props: {
    word: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      isPlaying: false
    };
  },
  methods: {
    definition(definitions) {
      return definitions.reduce((r, a) => {
        r[a.lang] = r[a.lang] || [];
        r[a.lang].push(a.definition);
        return r;
      }, Object.create(null));
    },
    alias(aliases) {
      return aliases.map((d) => d.word.replace('|', ''));
    },
    playSound(file) {
      if (!file) return;

      const audio = new Audio(file);
      this.isPlaying = true;
      audio.play();
      audio.onended = () => {
        this.isPlaying = false;
      };
      audio.onerror = () => {
        this.isPlaying = false;
      };
    }
  }
};
</script>

<style scoped>
.card-body {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: larger;
  min-height: 2.5rem;
  /* Минимальная высота для выравнивания */
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  /* Выравниваем по верхнему краю */
}

.word-main {
  font-style: italic;
  font-weight: 500;
  font-size: 1.25rem;
}

.word-main i {
  color: #4f585f;
}

.variant {
  font-weight: 400;
  font-size: 0.9em;
}

/* Выравнивание кнопки звука */
.btn-outline-primary {
  margin-top: 0.125rem;
  /* Небольшой отступ для визуального баланса */
  flex-shrink: 0;
  /* Не сжимаем кнопку */
}

/* Для лучшего выравнивания badge с текстом */
.badge {
  line-height: 1.2;
  padding: 0.35em 0.65em;
  vertical-align: middle;
}

.definition-content {
  margin-left: 0.5rem;
}

/* Адаптивность для мобильных */
@media (max-width: 576px) {
  .card-title {
    flex-direction: column;
    align-items: flex-start;
  }

  .btn-outline-primary {
    margin-top: 0.5rem;
    align-self: flex-end;
  }
}
</style>