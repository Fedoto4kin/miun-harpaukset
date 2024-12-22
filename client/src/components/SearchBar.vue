<template>
  <div class="search-bar-container my-3 col-6">
    <form @submit.prevent="handleSearchButtonClick">
      <div class="form-group mb-1">
        <div class="input-group">
          <span class="search-bar-switcher mx-2">
            <SwitchButton
              :checked="reverse"
              offLabel="Karielan šana"
              onLabel="Kiännökšeššä"
              @change="toggleReverse"
            />
          </span>
          <input
            type="text"
            class="form-control search-bar-input"
            placeholder=""
            v-model="searchText"
            ref="searchInput"
            @keyup.enter="handleSearchButtonClick"
            autofocus
          />
          <div class="input-group-append krl-letters">
            <div class="btn-group">
              <span
                v-for="char in specialChars"
                :key="char"
                :data-char="char"
                class="btn btn-secondary"
                @click="handleDiacrtButtonClick"
              >
                {{ char }}
              </span>
              <button class="btn btn-light border-dark search-run" type="button" @click="handleSearchButtonClick">
                <font-awesome-icon :icon="faSearch" />
              </button>
            </div>
          </div>
        </div>
      </div>
      <div class="text-muted text-center small">Zavodikkua kirjuttua täššä, štobi löydiä šanan šanakniigašta</div>
    </form>
  </div>
</template>

<script>
import { ref, watch, onMounted, nextTick } from 'vue';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import SwitchButton from './SwitchButton.vue';

export default {
  name: 'SearchBar',
  components: {
    FontAwesomeIcon,
    SwitchButton
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

    const specialChars = ['č', 'š', 'ž', 'ä', 'ö'];

    watch(() => props.search, (newSearch) => {
      searchText.value = newSearch;
    });

    watch(() => props.reverseProp, (newReverse) => {
      reverse.value = newReverse;
    });

    const handleSearchButtonClick = () => {
      const params = { search: searchText.value };
      if (reverse.value) {
        params.reverse = reverse.value;
      }
      emit('pushSearchStr', params);
      searchInput.value.focus();
    };

    const handleDiacrtButtonClick = (e) => {
      const position = searchInput.value.selectionStart;
      const updatedText = [
        searchText.value.slice(0, position),
        e.target.dataset.char,
        searchText.value.slice(position)
      ].join('');
      searchText.value = updatedText;
      // Устанавливаем фокус и позицию курсора
      nextTick(() => {
        searchInput.value.focus();
        searchInput.value.selectionStart = searchInput.value.selectionEnd = position + 1;
      });
    };

    onMounted(() => {
      searchInput.value.focus();
    });

    const toggleReverse = (checked) => {
      reverse.value = checked;
    };

    return {
      searchText,
      reverse,
      searchInput,
      specialChars,
      handleSearchButtonClick,
      handleDiacrtButtonClick,
      toggleReverse,
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
</style>
