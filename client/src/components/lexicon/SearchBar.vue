<template>
  <div class="search-bar-container my-lg-3 my-sm-1 col-lg-6 col-md-12">
    <form @submit.prevent="handleSearchButtonClick">
      <div class="position-relative">
        <div class="input-group align-item-center">
          <span class="search-bar-switcher mx-2 d-md-block d-none">
            <SwitchButton :checked="reverse" 
            offLabel="Karielan šana" 
            onLabel="Kiännökšeššä" 
            @change="toggleReverse" />
          </span>
          <input
            type="text"
            class="form-control search-bar-input"
            placeholder=""
            v-model="searchText"
            ref="searchInput"
            @input="handleInput"
            @keydown.enter="handleEnter"
            @keydown.down="handleKeyDown"
            @keydown.up="handleKeyUp"
            autofocus
          />
          <div class="input-group-append d-md-none">
            <div class="btn-group">
              <button class="navbar-toggler diacritic-button" type="button" @click="toggleMobileChars">
                <span class="diacritic-top">ˇ</span>
                <span class="diacritic-middle muted">/</span>
                <span class="diacritic-bottom">¨</span>
              </button>
              <div v-if="showMobileChars" class="mobile-chars d-md-none">
                <SpecialCharsButtons :searchText="searchText" @diacrt-click="handleDiacrtButtonClick" :btn-class="[]" />
              </div>
              <button class="btn btn-light border-dark search-run" type="button" @click="handleSearchButtonClick"
                :disabled="!searchText.length">
                <font-awesome-icon :icon="faSearch" />
              </button>
            </div>
          </div>
          <div class="input-group-append d-none d-md-block krl-letters">
            <div class="btn-group">
              <SpecialCharsButtons :searchText="searchText" @diacrt-click="handleDiacrtButtonClick" />
              <button class="btn btn-light border-dark search-run" type="button" @click="handleSearchButtonClick"
                :disabled="!searchText.length">
                <font-awesome-icon :icon="faSearch" />
              </button>
            </div>
          </div>
        </div>
        <ul
          v-if="suggestions.length"
          class="list-group mt-2 suggestions"
          :class="{ 'suggestions-tall': suggestionsHaveForms }"
        >
          <li
            v-for="(suggestion, index) in suggestions"
            :key="suggestionKey(suggestion)"
            class="list-group-item"
            :class="{ 'list-group-item-hover': index === highlightedIndex }"
            @click="handleSuggestionClick(suggestion)"
          >
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
              <div>{{ suggestion.word }}</div>
              <div
                v-if="suggestion.sample_forms && suggestion.sample_forms.length"
                class="sample-forms"
              >
                <button
                  v-for="sf in suggestion.sample_forms"
                  :key="sf.form"
                  type="button"
                  class="sample-form-chip"
                  :title="sf.label_krl"
                  @click.stop="handleFormChipClick(sf.form)"
                >
                  <em>{{ sf.form }}</em>
                </button>
                <span
                  v-if="suggestion.sample_forms_more"
                  class="sample-forms-more text-muted"
                  title="On enämbi muutošformua"
                >…</span>
              </div>
            </template>
          </li>
        </ul>
      </div>
      <div class="mt-1 text-muted text-center small">Zavodikkua kirjuttua täššä, štobi löydiä šana šanakniigašta</div>
    </form>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, nextTick } from 'vue';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import SwitchButton from '@/components/lexicon/SwitchButton.vue';
import { fetchSearchSuggestionsGrouped } from '@/services/searchService';
import SpecialCharsButtons from '@/components/ui/SpecialCharsButtons.vue';

export default {
  name: 'SearchBar',
  components: {
    SwitchButton,
    SpecialCharsButtons,
  },
  props: {
    search: {
      type: String,
      default: ''
    },
    reverseProp: {
      type: Boolean,
      default: false
    }
  },
  setup(props, { emit }) {
    const searchText = ref(props.search);
    const reverse = ref(props.reverseProp);
    const searchInput = ref(null);
    const suggestions = ref([]);
    const showMobileChars = ref(false);
    const highlightedIndex = ref(-1);
    let inputTimeout = null;

    // Высокий дропдаун только если есть превью словоформ (чипы).
    const suggestionsHaveForms = computed(() =>
      suggestions.value.some(
        (s) => Array.isArray(s.sample_forms) && s.sample_forms.length > 0
      )
    );

    // Методы для работы с текстом
    const clearSearchText = () => {
      searchText.value = '';
      suggestions.value = [];
      highlightedIndex.value = -1;
    };

    const setSearchText = (text) => {
      searchText.value = text;
    };

    const getSearchText = () => {
      return searchText.value;
    };

    watch(() => props.search, (newSearch) => {
      searchText.value = newSearch;
    });

    watch(() => props.reverseProp, (newReverse) => {
      reverse.value = newReverse;
    });

    const suggestionKey = (s) =>
      s.matched_form ? `${s.matched_form}→${s.word}` : s.word;

    const suggestionLabels = (s) =>
      Array.isArray(s?.matched_form_labels_krl) ? s.matched_form_labels_krl : [];

    /** Строка для поиска: при форме — сама форма (карточка покажет метку). */
    const suggestionQuery = (s) => s.matched_form || s.word;

    const fetchSuggestions = async () => {
      if (searchText.value.length >= 2) {
        try {
          const data = await fetchSearchSuggestionsGrouped(searchText.value, reverse.value);
          suggestions.value = Array.isArray(data) ? data : [];
          highlightedIndex.value = -1;
        } catch (error) {
          console.error('Failed to fetch suggestions:', error);
          suggestions.value = [];
        }
      } else {
        suggestions.value = [];
      }
    };

    const handleSearchButtonClick = () => {
      if (!searchText.value.trim()) {
        emit('pushClear');
        return;
      }

      // Эмитим событие для родительского компонента
      emit('pushSearchStr', searchText.value.trim());
      suggestions.value = [];
      if (searchInput.value) {
        searchInput.value.blur();
      }
    };

    const runSearch = (q) => {
      searchText.value = q;
      suggestions.value = [];
      emit('pushSearchStr', q);
      if (searchInput.value) {
        searchInput.value.blur();
      }
    };

    const handleSuggestionClick = (suggestion) => {
      const q = typeof suggestion === 'string' ? suggestion : suggestionQuery(suggestion);
      runSearch(q);
    };

    const handleFormChipClick = (form) => {
      runSearch(form);
    };

    const handleDiacrtButtonClick = (e) => {
      if (!searchInput.value) return;
      
      const position = searchInput.value.selectionStart;
      const updatedText = [
        searchText.value.slice(0, position),
        e.target.dataset.char,
        searchText.value.slice(position)
      ].join('');
      searchText.value = updatedText;
      nextTick(() => {
        if (searchInput.value) {
          searchInput.value.focus();
          searchInput.value.selectionStart = searchInput.value.selectionEnd = position + 1;
          fetchSuggestions();
        }
      });
    };

    const handleKeyDown = (event) => {
      if (suggestions.value.length > 0) {
        event.preventDefault();
        highlightedIndex.value = Math.min(highlightedIndex.value + 1, suggestions.value.length - 1);
      }
    };

    const handleKeyUp = (event) => {
      if (suggestions.value.length > 0) {
        event.preventDefault();
        highlightedIndex.value = Math.max(highlightedIndex.value - 1, 0);
      }
    };

    const handleEnter = (event) => {
      if (highlightedIndex.value !== -1 && suggestions.value[highlightedIndex.value]) {
        event.preventDefault();
        handleSuggestionClick(suggestions.value[highlightedIndex.value]);
      } else {
        handleSearchButtonClick();
      }
      if (searchInput.value) {
        searchInput.value.blur();
      }
    };

    onMounted(() => {
      if (searchInput.value) {
        searchInput.value.focus();
      }
    });

    const toggleReverse = (checked) => {
      reverse.value = checked;
      searchText.value = '';
      emit('reverseChanged', checked);
    };

    const toggleMobileChars = () => {
      showMobileChars.value = !showMobileChars.value;
    };

    const handleInput = () => {
      if (inputTimeout) clearTimeout(inputTimeout);
      inputTimeout = setTimeout(() => {
        fetchSuggestions();
      }, 300);
    };

    // Экспортируем методы для родительского компонента
    return {
      searchText,
      reverse,
      searchInput,
      suggestions,
      suggestionsHaveForms,
      showMobileChars,
      highlightedIndex,
      suggestionKey,
      suggestionLabels,
      clearSearchText,
      setSearchText,
      getSearchText,
      fetchSuggestions,
      handleSearchButtonClick,
      handleSuggestionClick,
      handleFormChipClick,
      handleDiacrtButtonClick,
      toggleReverse,
      toggleMobileChars,
      faSearch,
      handleInput,
      handleKeyDown,
      handleKeyUp,
      handleEnter,
    };
  }
};
</script>

<style scoped>
.search-bar-switcher {
  margin-right: 10px;
}

.search-bar-input {
  max-width: 250px;
}

.list-group {
  max-height: 200px;
  overflow-y: auto;
  z-index: 1060;
}

.list-group.suggestions-tall {
  max-height: min(70vh, 480px);
}

.list-group-item {
  cursor: pointer;
}

.list-group-item:hover,
.list-group-item-hover {
  cursor: pointer;
  color: var(--bs-list-group-action-active-color);
  background-color: var(--bs-list-group-action-active-bg);
}

.suggestions {
  position: absolute;
  background-color: white;
  width: 100%;
  z-index: 1000;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.suggestions .list-group-item {
  margin-bottom: 0;
}

.suggestion-chain-head {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.1rem;
}

.suggestion-labels {
  margin-top: 0.2rem;
  padding-left: 0.15rem;
  font-size: 0.85rem;
  line-height: 1.35;
}

.suggestion-labels li {
  margin: 0;
}

.sample-forms {
  display: flex;
  flex-wrap: wrap;
  gap: 0.25rem 0.35rem;
  margin-top: 0.25rem;
}

.sample-form-chip {
  border: 1px solid #dee2e6;
  background: #f8f9fa;
  border-radius: 0.25rem;
  padding: 0.05rem 0.4rem;
  font-size: 0.85rem;
  line-height: 1.4;
  color: #495057;
  cursor: pointer;
}

.sample-form-chip:hover {
  background: #e9ecef;
  border-color: #adb5bd;
}

.sample-forms-more {
  padding: 0.05rem 0.2rem;
  font-size: 0.95rem;
  line-height: 1.4;
  user-select: none;
}

.mobile-chars {
  position: absolute;
  right: 3.5em;
  top: 2.5rem;
  z-index: 2000;
  background-color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  padding: 2px;
}

.diacritic-button {
  position: relative;
  display: inline-block;
  font-size: 24px;
  padding: 10px 20px;
  background-color: #f8f9fa;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.diacritic-top {
  position: absolute;
  top: 0.35em;
  left: 50%;
  transform: translateX(-140%);
  font-size: 32px;
}

.diacritic-middle {
  font-size: 0.8em;
  position: relative;
  color: #999;
  z-index: 1;
}

.diacritic-bottom {
  position: absolute;
  bottom: -0.35em;
  left: 65%;
  font-size: 32px;
}
</style>