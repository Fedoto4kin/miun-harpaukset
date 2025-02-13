<template>
  <div class="search-bar-container my-lg-3 my-sm-1 col-lg-6 col-md-12">
    <form @submit.prevent="handleSearchButtonClick">
      <div class="position-relative">
        <div class="input-group align-item-center">
          <span class="search-bar-switcher mx-2 d-md-block d-none">
            <SwitchButton :checked="reverse" offLabel="Karielan šana" onLabel="Kiännökšeššä" @change="toggleReverse" />
          </span>
          <input type="text" class="form-control search-bar-input" placeholder="" v-model="searchText" ref="searchInput"
            @input="fetchSuggestions" @keyup.enter="handleSearchButtonClick" autofocus />
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
          <li v-for="suggestion in suggestions" :key="suggestion" class="list-group-item"
            @click="handleSuggestionClick(suggestion)">
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
import { fetchSearchSuggestions } from '../services/searchService';
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

    const clearSearchText = () => {
      searchText.value = '';
      suggestions.value = [];
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
          const data = await fetchSearchSuggestions(searchText.value, reverse.value);
          suggestions.value = data.map(item => item.word);
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

    onMounted(() => {
      searchInput.value.focus();
    });

    const toggleReverse = (checked) => {
      reverse.value = checked;
    };

    const toggleMobileChars = () => {
      showMobileChars.value = !showMobileChars.value;
    };

    return {
      searchText,
      reverse,
      searchInput,
      suggestions,
      showMobileChars,
      clearSearchText,
      fetchSuggestions,
      handleSearchButtonClick,
      handleSuggestionClick,
      handleDiacrtButtonClick,
      toggleReverse,
      toggleMobileChars,
      faSearch
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

.list-group-item {
  cursor: pointer;
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
  /* Adjust according to your layout */
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
  /* Adjust to position the diacritic properly */
  left: 50%;
  transform: translateX(-140%);
  font-size: 32px;
  /* Increased size */
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
  /* Adjust to position the diacritic properly */
  left: 65%;
  font-size: 32px;
  /* Increased size */
}
</style>
