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
                @input="fetchSuggestions"
                @keydown.up.prevent="moveUp"
                @keydown.down.prevent="moveDown"
                @keydown.enter.prevent="selectCurrent"
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
                <span class="word-suggestion">
                  <template v-if="suggestion.matched_form">
                    <em>{{ suggestion.matched_form }}</em>
                    <span class="text-muted mx-1">→</span>
                    <em>{{ suggestion.word }}</em>
                  </template>
                  <template v-else>
                    {{ suggestion.word }}
                  </template>
                </span>
                <span v-if="suggestion.pos" class="badge bg-secondary">{{ suggestion.pos }}</span>
              </li>
            </ul>
          </div>
          <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedWord">
            <WordCard :word="selectedWord" :show-paradigm-btn="false" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { nextTick } from 'vue';
  import { fetchSearchSuggestionsGrouped, fetchWordCard } from '@/services/searchService';
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
    },
    data() {
      return {
        searchText: '',
        suggestions: [],
        selectedWord: null,
        hoveredIndex: -1,
        selectedIndex: -1,
      };
    },
    methods: {
      closePopup() {
        this.$emit('close');
        this.searchText = '';
        this.suggestions = [];
        this.selectedWord = null;
        this.hoveredIndex = -1;
        this.selectedIndex = -1;
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
      async selectSuggestion(suggestion) {
        if (!suggestion?.word_id) return;
        try {
          const wordCard = await fetchWordCard(suggestion.word_id);
          this.selectedWord = {
            ...wordCard,
            matched_form: suggestion.matched_form || null,
            matched_form_label_krl: suggestion.matched_form_label_krl || null,
          };
          this.suggestions = [];
          this.searchText = '';
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
      selectCurrent() {
        if (this.selectedIndex !== -1) {
          this.selectSuggestion(this.suggestions[this.selectedIndex]);
        }
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
          this.fetchSuggestions();
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
    display: inline-flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.1rem;
  }

  .list-group-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    min-height: 2.5rem;
  }
</style>
