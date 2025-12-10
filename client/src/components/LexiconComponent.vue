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
                @pushSearchStr="getWordsBySearch" @pushClear="getWordsByClear" />
    </div>
    <div class="d-flex bg-light rounded-pill p-2">
      <button class="btn btn-light border-secondary me-2 flex-shrink-0 align-self-start d-lg-none" type="button" data-bs-toggle="collapse" data-bs-target="#abc"
        aria-controls="abc" aria-expanded="false" aria-label="Toggle navigation">
        <span v-if="letter">{{ letter }}</span>
        <span v-else><font-awesome-icon icon="ellipsis" /></span>
      </button>
      <div class="collapse navbar-collapse flex-grow-1 d-lg-block" id="abc">
        <div class="d-flex flex-wrap justify-content-center gap-2">
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
  data() {
    return {
      selectedOption: 'Karielan šana',
      reverse: false,
      title: 'Šanakniiga',
      words: [],
      letter: 'A',
      abc: 'ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ',
      loading: false,
      message: '', // Message about the number of words found
      searching: false, // Flag to track search state
    };
  },
  computed: {
    // Class for Bootstrap Alert based on search results
    alertClass() {
      return this.words.length > 0 ? 'alert-success' : 'alert-warning';
    }
  },
  methods: {
    // Handle letter click
    async handleLetterClick(letter) {
      // 1. Сначала закрываем алфавитную панель (мгновенно, без анимации)
      this.collapseAlphabetWithoutAnimation();
      
      // 2. Затем загружаем данные
      await this.getWordsByLetter(letter);
      
      // 3. Очищаем поисковую строку
      this.$refs.searchBar.clearSearchText();
    },
    
    // Метод для сворачивания алфавитной панели на мобильных БЕЗ анимации
    collapseAlphabetWithoutAnimation() {
      if (window.innerWidth < 992) {
        const abcCollapse = document.getElementById('abc');
        if (abcCollapse && abcCollapse.classList.contains('show')) {
          // Сохраняем текущие стили transition
          const originalTransition = abcCollapse.style.transition;
          const originalWebkitTransition = abcCollapse.style.webkitTransition;
          
          // Временно отключаем анимацию
          abcCollapse.style.transition = 'none';
          abcCollapse.style.webkitTransition = 'none';
          
          // Убираем классы Bootstrap для закрытия
          abcCollapse.classList.remove('show');
          abcCollapse.classList.add('collapsing');
          
          // Небольшая задержка для обновления DOM
          setTimeout(() => {
            abcCollapse.classList.remove('collapsing');
            abcCollapse.classList.add('collapse');
            
            // Восстанавливаем transition
            abcCollapse.style.transition = originalTransition;
            abcCollapse.style.webkitTransition = originalWebkitTransition;
          }, 10);
          
          // Обновляем состояние кнопки toggle
          const toggleButton = document.querySelector('[data-bs-target="#abc"]');
          if (toggleButton) {
            toggleButton.setAttribute('aria-expanded', 'false');
          }
        }
      }
    },
    
    // Fetch words by letter
    async getWordsByLetter(letter) {
      this.loading = true;
      this.letter = letter;
      this.message = '';
      this.searching = false; // Reset search flag
      this.words = [];
      try {
        this.words = await fetchWordsByLetter(letter);
        this.updateMessage(this.words.length); // Update message
      } catch (error) {
        this.message = 'Failed to fetch words. Please try again later.';
      } finally {
        this.loading = false;
      }
    },
    
    // Fetch words by search query
    async getWordsBySearch(params) {
      this.loading = true;
      this.message = '';
      this.letter = null;
      this.searching = true; // Set search flag
      try {
        this.words = await fetchWordsBySearch(params);
        this.updateMessage(this.words.length); // Update message
      } catch (error) {
        this.message = 'Ei voi löydy. Kuottekua jälgeh';
      } finally {
        this.loading = false;
      }
    },
    
    // Handle clear search
    getWordsByClear() {
      // 1. Сначала закрываем алфавитную панель
      this.collapseAlphabetWithoutAnimation();
      
      // 2. Затем загружаем данные
      const currentLetter = this.letter || 'A';
      this.getWordsByLetter(currentLetter);
    },
    
    // Update the message based on the number of words found
    updateMessage(wordCount) {
      if (this.searching && wordCount) {
        this.message = 'Löydy ' + wordCount;
        this.message += (wordCount > 1) ? ' šanua' : ' šana';
      } else if (this.searching) {
        this.message = 'Ei nimidä löydyn';
      } else {
        this.message = ''; // Reset message if search is not active
      }
    },
    
    handleSelectChange() {
      this.reverse = this.selectedOption === 'Kiännökšeššä';
    }
  },
  created() {
    this.getWordsByLetter(this.letter);
  },
  mounted() {
    document.title = this.title;
  }
};
</script>


<style scoped>
.navbar {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.nav-item {
  cursor: pointer;
}

.nav-item.active {
  font-weight: bold;
}

.scroll-to-top-btn {
  position: fixed;
  bottom: 1%;
  right: 1%;
  padding: 10px 15px;
  z-index: 1000;
}

/* Новые стили для кнопки и контейнера */
.btn-abc {
  flex-shrink: 0; /* Запрещаем кнопке изменять размер */
  white-space: nowrap; /* Запрещаем перенос текста */
}

.collapse.navbar-collapse {
  flex-grow: 1; /* Алфавит занимает оставшееся пространство */
}

/* Центрирование букв алфавита и перенос на новую строку */
.d-flex.flex-wrap.justify-content-center {
  width: 100%;
  gap: 0.5rem; /* Отступ между кнопками */
}

/* Фикс для вертикального выравнивания кнопки */
.align-self-start {
  align-self: flex-start !important;
}

/* Стили для кнопок букв */
.btn-primary {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

@media (max-width: 991.98px) {
  #abc.fast-collapse.collapsing {
    transition: none !important;
    -webkit-transition: none !important;
  }
}

/* На мобильных уменьшаем кнопки */
@media (max-width: 768px) {
  .btn-primary {
    min-width: 35px;
    height: 35px;
    font-size: 0.9rem;
  }
  
  /* Класс для быстрого закрытия без анимации */
  #abc.fast-collapse.collapsing {
    transition: none !important;
    -webkit-transition: none !important;
  }
}
</style>