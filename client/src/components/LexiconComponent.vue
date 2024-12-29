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
    
    <!-- Кнопка "Наверх" -->
    <button 
      v-if="showScrollButton" 
      @click="scrollToTop" 
      class="scroll-to-top-btn btn btn-primary"
    >
      <font-awesome-icon icon="arrow-up" />
    </button>
    
    <!-- Список слов -->
    <div class="row mt-4">
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
      message: '', // Message about the number of words found
      searching: false, // Flag to track search state
      showScrollButton: false, // Flag to show/hide the scroll-to-top button
    };
  },
  computed: {
    // Class for Bootstrap Alert based on search results
    alertClass() {
      return this.words.length > 0 ? 'alert-success' : 'alert-warning';
    }
  },
  methods: {
    // Fetch words by letter
    getWordsByLetter(letter) {
      this.loading = true;
      this.letter = letter;
      this.searching = false; // Reset search flag
      axios.get(`v0/lexicon/search/`, { params: { query: letter } })
        .then((response) => {
          this.words = response.data;
          this.updateMessage(response.data.length); // Update message
        })
        .finally(() => {
          this.loading = false;
        });
    },
    // Fetch words by search query
    getWordsBySearch(params) {
      this.loading = true;
      this.searching = true; // Set search flag
      const url = params.reverse ? `v0/lexicon/reverse/` : `v0/lexicon/search/`;
      axios.get(url, { params: params })
        .then((response) => {
          this.words = response.data;
          this.updateMessage(response.data.length); // Update message
        })
        .finally(() => {
          this.loading = false;
        });
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
    // Scroll to the top of the page
    scrollToTop() {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    },
    // Handle scroll event to show/hide the scroll-to-top button
    handleScroll() {
      this.showScrollButton = window.scrollY > 100; // Show button if scrolled more than 100px
    }
  },
  created() {
    this.getWordsByLetter(this.letter);
  },
  mounted() {
    document.title = this.title;
    window.addEventListener('scroll', this.handleScroll); // Add scroll event listener
  },
  beforeUnmount() {
    window.removeEventListener('scroll', this.handleScroll); // Remove scroll event listener
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
</style>