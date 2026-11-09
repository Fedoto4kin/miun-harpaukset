<template>
  <div v-if="show" class="modal" tabindex="-1" @click.self="closePopup">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <div class="position-relative flex-grow-1 me-2">
            <div class="input-group">
              <input
                type="text"
                class="form-control"
                placeholder="Löydiä šana šanakniigašta..."
                v-model="searchText"
                ref="searchInput"
                @input="onInput"
                @keydown.up.prevent="moveUp"
                @keydown.down.prevent="moveDown"
                @keydown.enter.prevent="onEnter"
              />
              <div class="input-group-append krl-letters">
                <div class="btn-group">
                  <SpecialCharsButtons @diacrt-click="handleDiacrtButtonClick" />
                </div>
              </div>
            </div>
            <ul class="list-group position-absolute w-100 mt-1" v-if="suggestions.length">
              <li
                v-for="(suggestion, index) in suggestions"
                :key="suggestion.word_id || suggestion.word"
                class="list-group-item list-item d-flex justify-content-between align-items-center"
                @click="selectSuggestion(suggestion)"
                @mouseover="hoveredIndex = index"
                @mouseout="hoveredIndex = -1"
                :class="{ 'list-item-hover': hoveredIndex === index || selectedIndex === index }"
              >
                <div class="word-suggestion flex-grow-1">
                  <template v-if="suggestion.matched_form">
                    <div class="suggestion-chain-head">
                      <em>{{ suggestion.matched_form }}</em>
                      <span class="text-muted mx-1">→</span>
                      <em>{{ suggestion.word }}</em>
                    </div>
                    <ul
                      v-if="suggestionLabels(suggestion).length"
                      class="suggestion-labels list-unstyled text-muted mb-0"
                    >
                      <li v-for="(lab, i) in suggestionLabels(suggestion)" :key="i">
                        {{ lab }}
                      </li>
                    </ul>
                  </template>
                  <template v-else>
                    {{ suggestion.word }}
                  </template>
                </div>
                <span v-if="suggestion.pos" class="badge bg-secondary align-self-start">{{ suggestion.pos }}</span>
              </li>
            </ul>
          </div>
          <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="loading" class="text-muted text-center py-3">…</div>
          <div v-else-if="notFound" class="alert alert-warning mb-0">
            Šanua «{{ notFoundQuery }}» ei löydyny šanakniigašta.
          </div>
          <div v-else-if="selectedWords.length" class="d-flex flex-column gap-3">
            <WordCard
              v-for="w in selectedWords"
              :key="w.id"
              :word="w"
              :show-paradigm-btn="false"
              :show-lexicon-link="true"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { nextTick } from 'vue';
  import { fetchSearchSuggestionsGrouped, fetchWordCard } from '@/services/searchService';
  import { fetchWordsBySearch } from '@/services/lexiconService';
  import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
  import WordCard from '@/components/lexicon/WordCard.vue';

  export default {
    name: 'WordSearchPopupComponent',
    components: {
      WordCard,
      SpecialCharsButtons,
    },
    props: {
      show: {
        type: Boolean,
        required: true,
      },
      /** Слово из выделения / внешней команды — сразу ищем */
      query: {
        type: String,
        default: '',
      },
    },
    data() {
      return {
        searchText: '',
        suggestions: [],
        selectedWords: [],
        loading: false,
        notFound: false,
        notFoundQuery: '',
        hoveredIndex: -1,
        selectedIndex: -1,
      };
    },
    watch: {
      show(val) {
        if (val) {
          this.resetResults();
          const q = (this.query || '').trim();
          if (q) {
            this.searchText = q;
            this.runExactSearch(q);
          } else {
            this.searchText = '';
            nextTick(() => this.$refs.searchInput?.focus());
          }
        }
      },
      query(val) {
        if (!this.show) return;
        const q = (val || '').trim();
        if (!q) return;
        this.searchText = q;
        this.runExactSearch(q);
      },
    },
    methods: {
      suggestionLabels(s) {
        return Array.isArray(s?.matched_form_labels_krl)
          ? s.matched_form_labels_krl
          : [];
      },
      resetResults() {
        this.suggestions = [];
        this.selectedWords = [];
        this.loading = false;
        this.notFound = false;
        this.notFoundQuery = '';
        this.hoveredIndex = -1;
        this.selectedIndex = -1;
      },
      closePopup() {
        this.$emit('close');
        this.searchText = '';
        this.resetResults();
      },
      onInput() {
        this.notFound = false;
        this.selectedWords = [];
        this.fetchSuggestions();
      },
      async fetchSuggestions() {
        if (this.searchText.length >= 2) {
          try {
            const data = await fetchSearchSuggestionsGrouped(this.searchText);
            this.suggestions = Array.isArray(data) ? data : [];
            this.selectedIndex = -1;
          } catch (error) {
            console.error('Failed to fetch suggestions:', error);
            this.suggestions = [];
          }
        } else {
          this.suggestions = [];
        }
      },
      async runExactSearch(raw) {
        const q = (raw || '').trim();
        if (!q) return;
        this.loading = true;
        this.notFound = false;
        this.notFoundQuery = q;
        this.selectedWords = [];
        this.suggestions = [];
        try {
          const results = await fetchWordsBySearch({ query: q });
          const list = Array.isArray(results) ? results : [];
          if (!list.length) {
            this.notFound = true;
            return;
          }
          this.selectedWords = list;
        } catch (error) {
          console.error('Failed to search word:', error);
          this.notFound = true;
        } finally {
          this.loading = false;
        }
      },
      async selectSuggestion(suggestion) {
        if (!suggestion?.word_id) return;
        try {
          const wordCard = await fetchWordCard(suggestion.word_id);
          this.selectedWords = [
            {
              ...wordCard,
              matched_form: suggestion.matched_form || null,
              matched_form_labels_krl: this.suggestionLabels(suggestion),
            },
          ];
          this.suggestions = [];
          this.notFound = false;
          this.searchText = suggestion.matched_form || suggestion.word || this.searchText;
        } catch (error) {
          console.error('Failed to fetch word card:', error);
        }
      },
      moveUp() {
        if (this.selectedIndex > 0) {
          this.selectedIndex--;
        }
      },
      moveDown() {
        if (this.selectedIndex < this.suggestions.length - 1) {
          this.selectedIndex++;
        }
      },
      onEnter() {
        if (this.selectedIndex !== -1 && this.suggestions[this.selectedIndex]) {
          this.selectSuggestion(this.suggestions[this.selectedIndex]);
          return;
        }
        this.runExactSearch(this.searchText);
      },
      handleDiacrtButtonClick(e) {
        const position = this.$refs.searchInput.selectionStart;
        const updatedText = [
          this.searchText.slice(0, position),
          e.target.dataset.char,
          this.searchText.slice(position)
        ].join('');
        this.searchText = updatedText;
        nextTick(() => {
          this.$refs.searchInput.focus();
          this.$refs.searchInput.selectionStart = this.$refs.searchInput.selectionEnd = position + 1;
          this.onInput();
        });
      },
    },
  };
</script>

<style scoped>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 99999;
  }

  .modal-dialog {
    min-height: 500px;
    margin: auto;
  }

  .modal-dialog input::placeholder {
    font-size: 0.7em;
  }

  .modal-content {
    background: #fff;
    border-radius: 0.5rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    position: relative;
    min-height: 100px;
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
  }

  .modal-body {
    padding: 1rem;
  }

  .list-group {
    overflow-y: auto;
    z-index: 999;
    max-height: 300px;
  }

  .list-item {
    cursor: pointer;
    padding: 0.5rem 1rem;
  }

  .list-item:hover,
  .list-item-hover {
    cursor: pointer;
    color: var(--bs-list-group-action-active-color);
    background-color: var(--bs-list-group-action-active-bg);
  }

  .word-suggestion {
    font-weight: 500;
    min-width: 0;
  }

  .suggestion-chain-head {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.1rem;
  }

  .suggestion-labels {
    margin-top: 0.2rem;
    font-size: 0.85rem;
    line-height: 1.35;
    font-weight: 400;
  }

  .suggestion-labels li {
    margin: 0;
  }

  .list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 2.5rem;
  }
</style>
