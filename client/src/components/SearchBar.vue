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
        <ul v-if="suggestions.length" class="list-group mt-2 suggestions">
          <li
            v-for="(suggestion, index) in suggestions"
            :key="suggestion"
            class="list-group-item"
            :class="{ 'list-group-item-hover': index === highlightedIndex }"
            @click="handleSuggestionClick(suggestion)"
          >
            {{ suggestion }}
          </li>
        </ul>
      </div>
      <div class="text-muted text-center">Zavodikkua kirjuttua täššä, štobi löydiä šanan šanakniigašta</div>
    </form>
  </div>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import SwitchButton from './SwitchButton.vue';
import { fetchSearchSuggestionsGrouped } from '../services/searchService';
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
    const highlightedIndex = ref(-1); // Индекс подсвеченного элемента
    let inputTimeout = null;

    const clearSearchText = () => {
      searchText.value = '';
      suggestions.value = [];
      highlightedIndex.value = -1;
    };

    watch(() => props.search, (newSearch) => {
      searchText.value = newSearch;
    });

    watch(() => props.reverseProp, (newReverse) => {
      reverse.value = newReverse;
      clearSearchText();
    });

    const fetchSuggestions = async () => {
      if (searchText.value.length >= 2) {
        try {
          const data = await fetchSearchSuggestionsGrouped(searchText.value, reverse.value);
          suggestions.value = data.map(item => item.word);
          highlightedIndex.value = -1; // Сброс подсветки при новом запросе
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
        emit('pushClear', 'A');
        return;
      }

      const params = { query: searchText.value };
      if (reverse.value) {
        params.reverse = reverse.value;
      }
      emit('pushSearchStr', params);
      suggestions.value = [];
      searchInput.value.focus();
    };

    const handleSuggestionClick = (suggestion) => {
      searchText.value = suggestion;
      suggestions.value = [];
      handleSearchButtonClick();
    };

    const handleDiacrtButtonClick = (e) => {
      const position = searchInput.value.selectionStart;
      const updatedText = [
        searchText.value.slice(0, position),
        e.target.dataset.char,
        searchText.value.slice(position)
      ].join('');
      searchText.value = updatedText;
      nextTick(() => {
        searchInput.value.focus();
        searchInput.value.selectionStart = searchInput.value.selectionEnd = position + 1;
        fetchSuggestions();
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
        event.preventDefault(); // Предотвращаем стандартное поведение формы
        handleSuggestionClick(suggestions.value[highlightedIndex.value]);
      } else {
        handleSearchButtonClick(); // Если нет подсвеченного предложения, выполняем поиск по текущему значению
      }
    };

    onMounted(() => {
      searchInput.value.focus();
    });

    const toggleReverse = (checked) => {
      reverse.value = checked;
    };

    const toggleMobileChars = () => {
      showMobileChars.value = !showMobileChars.value;
    };

    const handleInput = () => {
      if (inputTimeout) clearTimeout(inputTimeout);
      inputTimeout = setTimeout(() => {
        fetchSuggestions();
      }, 300); // 300ms delay to debounce input
    };

    return {
      searchText,
      reverse,
      searchInput,
      suggestions,
      showMobileChars,
      highlightedIndex,
      clearSearchText,
      fetchSuggestions,
      handleSearchButtonClick,
      handleSuggestionClick,
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