<template>
  <div class="card">
    <div class="card-body">
      <div v-if="word.matched_form" class="matched-form text-muted mb-1">
        <em class="matched-form-orth">{{ word.matched_form }}</em>
        <ul
          v-if="matchedLabels.length"
          class="matched-form-labels list-unstyled mb-0"
        >
          <li v-for="(lab, i) in matchedLabels" :key="i">{{ lab }}</li>
        </ul>
      </div>

      <p class="card-title d-flex justify-content-between align-items-center">
        <span class="d-flex align-items-center flex-wrap">
          <span class="word-main">
            {{ word.word ? word.word.replace('|', '') : '' }}
          </span>
          <span v-if="word.additional" class="word-main">
            &nbsp;<i>(</i>{{ word.additional }}<i>)</i>
          </span>
          <span v-if="word.variant" class="text-muted variant ms-2">
            {{ word.variant }}
          </span>

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

        <span class="d-flex gap-1 align-self-start">
          <button
            v-if="showParadigmBtn && word.has_paradigm"
            @click="openParadigm"
            class="btn btn-sm btn-outline-secondary"
            title="Muutokšet"
            type="button"
          >
            <font-awesome-icon icon="table" />
          </button>
          <a
            v-if="showLexiconLink"
            :href="lexiconSearchUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-sm btn-outline-secondary"
            title="Šanakniigašta"
          >
            <font-awesome-icon :icon="['fas', 'arrow-up-right-from-square']" />
          </a>
          <button @click="playSound(word.speech)" :disabled="isPlaying"
            class="btn btn-sm btn-outline-primary" type="button">
            <font-awesome-icon icon="volume-up" />
          </button>
        </span>
      </p>

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

      <div v-if="word.alias_words && word.alias_words.length" class="mt-2">
        <span class='text-muted'>Šama kuin </span>
        <span v-for="al in alias(word.alias_words)" :key="al" class="badge bg-info me-1">{{ al }}</span>
      </div>
    </div>

    <ParadigmPopup
      :show="showParadigm"
      :lemma="word.word ? word.word.replace('|', '') : ''"
      :pos="paradigmPos || word.pos || ''"
      :highlight-form="word.matched_form || ''"
      :forms="paradigmForms"
      :loading="paradigmLoading"
      :error="paradigmError"
      @close="showParadigm = false"
    />
  </div>
</template>

<script>
import ParadigmPopup from './ParadigmPopup.vue';
import { fetchWordParadigm } from '../../services/lexiconService';

export default {
  name: 'WordCard',
  components: { ParadigmPopup },
  props: {
    word: {
      type: Object,
      required: true
    },
    showParadigmBtn: {
      type: Boolean,
      default: true,
    },
    showLexiconLink: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      isPlaying: false,
      showParadigm: false,
      paradigmForms: [],
      paradigmPos: '',
      paradigmLoading: false,
      paradigmError: '',
    };
  },
  computed: {
    matchedLabels() {
      const labels = this.word?.matched_form_labels_krl;
      return Array.isArray(labels) ? labels : [];
    },
    lexiconSearchUrl() {
      const q =
        this.word?.matched_form ||
        (this.word?.word ? this.word.word.replace('|', '') : '');
      if (!q) return '/lexicon/A';
      return `/lexicon/search/${encodeURIComponent(q)}`;
    },
  },
  methods: {
    definition(definitions) {
      return (definitions || []).reduce((r, a) => {
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
    },
    async openParadigm() {
      this.showParadigm = true;
      this.paradigmError = '';
      this.paradigmLoading = true;
      try {
        const data = await fetchWordParadigm(this.word.id);
        this.paradigmForms = data.forms || [];
        this.paradigmPos = data.pos || '';
      } catch (e) {
        this.paradigmError = 'Ei voitu lataa muutokšie';
        this.paradigmForms = [];
        this.paradigmPos = '';
      } finally {
        this.paradigmLoading = false;
      }
    },
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
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.matched-form {
  font-size: 1.05rem;
  line-height: 1.35;
  margin-bottom: 0.35rem;
}

.matched-form-orth {
  display: inline-block;
  margin-bottom: 0.1rem;
}

.matched-form-labels {
  margin: 0.15rem 0 0;
  padding-left: 0.1rem;
  font-size: 0.9rem;
}

.matched-form-labels li {
  margin: 0;
}

.badge {
  line-height: 1.2;
  padding: 0.35em 0.65em;
  vertical-align: middle;
}

.definition-content {
  margin-left: 0.5rem;
}

@media (max-width: 576px) {
  .card-title {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
