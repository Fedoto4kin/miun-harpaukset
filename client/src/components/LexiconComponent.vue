<template>
  <div class="container">
    <div class="row my-4">
      <h1 class="mt-4 col-6">
        <font-awesome-icon icon="book" class="text-success" />
        {{ title }}
      </h1>
      <SearchBar @pushSearchStr="getWordsBySearch" @pushClear="getWordsByLetter"/>
    </div>

    <!-- Сообщение о количестве найденных слов -->
    <div v-if="message" class="row">
      <div class="col-12">
        <div :class="['alert', alertClass]" role="alert">
          {{ message }}
        </div>
      </div>
    </div>

    <!-- Ряд букв -->
    <div class="navbar">
      <span
        v-for="l in abc.split('')"
        :key="l"
        :class="['nav-item', 'my-1', { active: l == letter }]"
        @click="getWordsByLetter(l)"
        class="btn btn-primary mx-1"
      >
        {{ l }}
      </span>
    </div>

    <!-- Прелоадер -->
    <div v-if="loading" class="text-center mt-4">
      <img src="/img/preloader.gif" alt="Loading..." />
    </div>

    <!-- Список слов -->
    <div v-else class="row mt-4">
      <WordCard
        v-for="word in words"
        :key="word.id"
        :word="word"
      />
    </div>
  </div>
</template>

<script>
import axios from '../axios';
import WordCard from './WordCard.vue';
import SearchBar from './SearchBar.vue';

export default {
  name: 'LexiconComponent',
  components: {
    WordCard,
    SearchBar
  },
  data() {
    return {
      title: 'Šanakniiga',
      words: [],
      letter: 'A',
      abc: 'ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ',
      loading: false,
      message: '', // Сообщение о количестве найденных слов
      searching: false, // Флаг для отслеживания состояния поиска
    };
  },
  computed: {
    // Класс для Bootstrap Alert в зависимости от наличия результатов
    alertClass() {
      return this.words.length > 0 ? 'alert-success' : 'alert-warning';
    }
  },
  methods: {
    getWordsByLetter(letter) {
      this.loading = true;
      this.letter = letter;
      this.searching = false; // Сброс флага поиска
      axios.get(`v0/lexicon/search/`, { params: { query: letter } })
        .then((response) => {
          this.words = response.data;
          this.updateMessage(response.data.length); // Обновление сообщения
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getWordsBySearch(params) {
      this.loading = true;
      this.searching = true; // Установка флага поиска
      const url = params.reverse ? `v0/lexicon/reverse/` : `v0/lexicon/search/`;
      axios.get(url, { params: params })
        .then((response) => {
          this.words = response.data;
          this.updateMessage(response.data.length); // Обновление сообщения
        })
        .finally(() => {
          this.loading = false;
        });
    },
    updateMessage(wordCount) {
      if (this.searching && wordCount) {
        this.message = 'Löydy ' + wordCount;
        this.message += (wordCount > 1) ? ' šanua' : ' šana';
      } else if (this.searching) {
        this.message = 'Ei nimidä löydyn';
      } else {
        this.message = ''; // Сброс сообщения, если поиск не активен
      }
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
</style>