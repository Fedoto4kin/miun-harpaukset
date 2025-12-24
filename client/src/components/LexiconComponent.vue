<template>
  <div class="container">
    <div class="row my-lg-4 my-sm-2">
      <h1 class="mt-lg-4 col-lg-6 col-sm-12 d-flex align-items-center mt-0">
        <span class="mx-2">{{ title }}</span>
        <select class="form-select ml-3 d-sm-block d-md-none" v-model="selectedOption" @change="handleSelectChange">
          <option value="Karielan šana">Karielan šana</option>
          <option value="Kiännökšeššä">Kiännökšeššä</option>
        </select>
      </h1>
      <SearchBar ref="searchBar" 
                :reverse-prop="reverse" 
                @pushSearchStr="handleSearchFromUI"
                @pushClear="getWordsByClear"
                @reverseChanged="handleReverseChange" />
    </div>
    <div class="d-flex p-2">
      <button class="btn btn-light border-secondary me-2 flex-shrink-0 align-self-start d-lg-none" type="button" data-bs-toggle="collapse" data-bs-target="#abc"
        aria-controls="abc" aria-expanded="false" aria-label="Toggle navigation">
        <span v-if="letter">{{ letter }}</span>
        <span v-else><font-awesome-icon icon="ellipsis" /></span>
      </button>
      <div class="collapse navbar-collapse flex-grow-1 d-lg-block" id="abc">
        <div class="d-flex flex-wrap justify-content-center gap-1">
          <span v-for="l in abc.split('')" :key="l" :class="['nav-item', 'my-1', { active: l == letter }]"
            @click="handleLetterClick(l)" class="btn btn-primary">
            {{ l }}
          </span>
        </div>
      </div>
    </div>

    <div v-if="message" class="row">
      <div class="col-12 mt-2">
        <div :class="['alert', alertClass]" role="alert">
          {{ message }}
        </div>
      </div>
    </div>
    <LoadingSpinner v-if="loading" />

    <ScrollToTopButton />

    <div class="row mt-2">
      <div v-for="word in words" class="col-md-6 col-lg-4 mb-4" :key="word.id">
        <WordCard :word="word" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import WordCard from './lexicon/WordCard.vue';
import SearchBar from './lexicon/SearchBar.vue';
import ScrollToTopButton from './ui/ScrollToTopButton.vue';
import LoadingSpinner from './ui/LoadingDots.vue';
import { fetchWordsByLetter, fetchWordsBySearch } from '../services/lexiconService';

export default {
  name: 'LexiconComponent',
  components: {
    WordCard,
    SearchBar,
    ScrollToTopButton,
    LoadingSpinner,
  },
  setup() {
    const route = useRoute();
    const router = useRouter();
    
    const searchBar = ref(null);
    const selectedOption = ref('Karielan šana');
    const reverse = ref(false);
    const title = ref('Šanakniiga');
    const words = ref([]);
    const letter = ref('A');
    const abc = ref('ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ');
    const loading = ref(false);
    const message = ref('');
    const searching = ref(false);
    
    const alertClass = computed(() => {
      return words.value.length > 0 ? 'alert-success' : 'alert-warning';
    });

    // Инициализация на основе текущего URL
    const initializeFromURL = async () => {
      const { name, params } = route;
      
      if (name === 'LexiconLetter' && params.letter) {
        // Буквенный поиск: /lexicon/A
        await handleLetterFromURL(params.letter);
      } else if (name === 'LexiconSearch' && params.query) {
        // Прямой поиск: /lexicon/search/kala
        reverse.value = false;
        selectedOption.value = 'Karielan šana';
        await handleSearchFromURL(params.query, false);
      } else if (name === 'LexiconTranslate' && params.query) {
        // Обратный перевод: /lexicon/translate/рыба
        reverse.value = true;
        selectedOption.value = 'Kiännökšeššä';
        await handleSearchFromURL(params.query, true);
      }
      // Маршрут /lexicon теперь автоматически перенаправляется на /lexicon/A
    };

    // Обработка буквенного поиска из URL
    const handleLetterFromURL = async (letterParam) => {
      loading.value = true;
      searching.value = false;
      letter.value = letterParam.toUpperCase();
      message.value = '';
      words.value = [];
      
      try {
        words.value = await fetchWordsByLetter(letter.value);
        updateMessage(words.value.length);
        
        // Очищаем поисковую строку
        if (searchBar.value) {
          searchBar.value.clearSearchText();
        }
      } catch (error) {
        message.value = 'Failed to fetch words. Please try again later.';
      } finally {
        loading.value = false;
      }
    };

    // Обработка текстового поиска из URL
    const handleSearchFromURL = async (query, isReverse) => {
      loading.value = true;
      searching.value = true;
      letter.value = null;
      message.value = '';
      words.value = [];
      
      try {
        const params = {
          query: query,
          reverse: isReverse
        };
        words.value = await fetchWordsBySearch(params);
        updateMessage(words.value.length);
        
        // Устанавливаем текст в поисковой строке
        if (searchBar.value) {
          searchBar.value.setSearchText(query);
        }
      } catch (error) {
        message.value = 'Ei voi löydy. Kuottekua jälgeh';
      } finally {
        loading.value = false;
      }
    };

    // Обновление URL для буквенного поиска
    const updateURLForLetter = (letterParam) => {
      router.push({
        name: 'LexiconLetter',
        params: { letter: letterParam.toUpperCase() }
      }).catch(() => {});
    };

    // Обновление URL для текстового поиска
    const updateURLForSearch = (query, isReverse) => {
      if (!query.trim()) {
        const currentLetter = letter.value || 'A';
        return updateURLForLetter(currentLetter);
      }
      
      const routeName = isReverse ? 'LexiconTranslate' : 'LexiconSearch';
      
      router.push({
        name: routeName,
        params: { query: query.trim() }
      }).catch(() => {});
    };

    // Клик по букве
    const handleLetterClick = async (letterParam) => {
      collapseAlphabetWithoutAnimation();
      updateURLForLetter(letterParam);
    };

    // Поиск из UI (от SearchBar)
    const handleSearchFromUI = (searchText) => {
      updateURLForSearch(searchText, reverse.value);
    };

    // Очистка поиска
    const getWordsByClear = () => {
      collapseAlphabetWithoutAnimation();
      const currentLetter = letter.value || 'A';
      updateURLForLetter(currentLetter);
    };

    // Изменение направления поиска
    const handleReverseChange = (isReverse) => {
      reverse.value = isReverse;
      selectedOption.value = isReverse ? 'Kiännökšeššä' : 'Karielan šana';
      
      // Если есть активный поиск, обновляем URL
      if (searching.value && searchBar.value) {
        const currentSearch = searchBar.value.getSearchText();
        if (currentSearch && currentSearch.trim()) {
          updateURLForSearch(currentSearch.trim(), isReverse);
        }
      }
    };

    // Изменение опции на мобильных
    const handleSelectChange = () => {
      const newReverse = selectedOption.value === 'Kiännökšeššä';
      handleReverseChange(newReverse);
    };

    const updateMessage = (wordCount) => {
      if (searching.value && wordCount) {
        message.value = 'Löydy ' + wordCount;
        message.value += (wordCount > 1) ? ' šanua' : ' šana';
      } else if (searching.value) {
        message.value = 'Ei nimidä löydyn';
      } else {
        message.value = '';
      }
    };

    // Сворачивание алфавитной панели без анимации
    const collapseAlphabetWithoutAnimation = () => {
      if (window.innerWidth < 992) {
        const abcCollapse = document.getElementById('abc');
        if (abcCollapse && abcCollapse.classList.contains('show')) {
          const originalTransition = abcCollapse.style.transition;
          const originalWebkitTransition = abcCollapse.style.webkitTransition;
          
          abcCollapse.style.transition = 'none';
          abcCollapse.style.webkitTransition = 'none';
          
          abcCollapse.classList.remove('show');
          abcCollapse.classList.add('collapsing');
          
          setTimeout(() => {
            abcCollapse.classList.remove('collapsing');
            abcCollapse.classList.add('collapse');
            
            abcCollapse.style.transition = originalTransition;
            abcCollapse.style.webkitTransition = originalWebkitTransition;
          }, 10);
          
          const toggleButton = document.querySelector('[data-bs-target="#abc"]');
          if (toggleButton) {
            toggleButton.setAttribute('aria-expanded', 'false');
          }
        }
      }
    };

    // Отслеживаем изменения маршрута
    watch(() => route.fullPath, () => {
      initializeFromURL();
    }, { immediate: true });

    onMounted(() => {
      document.title = title.value;
    });

    return {
      searchBar,
      selectedOption,
      reverse,
      title,
      words,
      letter,
      abc,
      loading,
      message,
      searching,
      alertClass,
      handleLetterClick,
      handleSearchFromUI,
      getWordsByClear,
      handleReverseChange,
      handleSelectChange,
      collapseAlphabetWithoutAnimation
    };
  }
};
</script>