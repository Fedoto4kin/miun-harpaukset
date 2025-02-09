<template>
  <div v-if="show" class="modal" tabindex="-1" @click.self="closePopup">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <div class="position-relative">
            <div class="input-group">
              <input 
                type="text" 
                class="form-control" 
                placeholder="Löydiä šanan šanakniigašta..." 
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
                :key="suggestion.word_id" 
                class="list-group-item list-item"
                @click="selectWord(suggestion.word_id)"
                @mouseover="hoveredIndex = index"
                @mouseout="hoveredIndex = -1"
                :class="{ 'list-item-hover': hoveredIndex === index, 'list-item-hover': selectedIndex === index }"
              >
                {{ suggestion.word }}
              </li>
            </ul>
          </div>
          <button type="button" class="btn-close" @click="closePopup" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <div v-if="selectedWord" class="mt-3">
            <WordCard :word="selectedWord" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import { nextTick } from 'vue';
  import { fetchSearchSuggestions, fetchWordCard } from '@/services/searchService';
  import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';
  import WordCard from './WordCard.vue';
  
  export default {
    name: 'SearchPopupComponent',
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
            const data = await fetchSearchSuggestions(this.searchText);
            this.suggestions = data;
            this.selectedIndex = -1;
          } catch (error) {
            console.error('Failed to fetch suggestions:', error);
            this.suggestions = [];
          }
        } else {
          this.suggestions = [];
        }
      },
      async selectWord(wordId) {
        try {
          const wordCard = await fetchWordCard(wordId);
          this.selectedWord = wordCard;
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
          this.selectWord(this.suggestions[this.selectedIndex].word_id);
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
    z-index: 1050;
  }
  
  .modal-dialog {
    max-width: 500px;
    min-height: 500px;
    margin: auto;
  }
  
  .modal-content {
    background: #fff;
    border-radius: 0.5rem;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    position: relative;
    min-height: 100px;
    width: 500px;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
  }
  
  .modal-title {
    margin: 0;
    font-size: 1.25rem;
  }
  
  .modal-body {
    padding: 1rem;
  }

  .list-group {
    max-height: 200px;
    overflow-y: auto;
    z-index: 1060;
  }
  
  .list-item {
    cursor: pointer;
  }

  .list-item:hover {
    cursor: pointer;
    color: var(--bs-list-group-action-active-color);
    background-color: var(--bs-list-group-action-active-bg);
  }
  
  .list-item-hover {
    color: var(--bs-list-group-action-active-color);
    background-color: var(--bs-list-group-action-active-bg);
  }
</style>
