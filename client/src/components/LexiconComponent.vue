<template>
  <div class="container">
    <div class="row my-4">
      <h1 class="mt-4 col-6">
        <font-awesome-icon icon="book" class="text-success" />
        {{ title }}
      </h1>
      <SearchBar 
        ref="searchBar" 
        @pushSearchStr="getWordsBySearch" 
        @pushClear="getWordsByLetter"
        />
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
        @click="handleLetterClick(l)"
        class="btn btn-primary mx-1"
      >
        {{ l }}
      </span>
    </div>

    <!-- Прелоадер -->
    <div v-if="loading" class="text-center mt-4">
      <img src="/img/preloader.gif" alt="Loading..." />
    </div>
    
    <ScrollToTopButton />
    
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
import WordCard from './WordCard.vue';
import SearchBar from './SearchBar.vue';
import ScrollToTopButton from './ui/ScrollToTopButton.vue';
import { fetchWordsByLetter, fetchWordsBySearch } from '../services/lexiconService'; // Импортируем сервис

export default {
  name: 'LexiconComponent',
  components: {
    WordCard,
    SearchBar,
    ScrollToTopButton,
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
      await this.getWordsByLetter(letter); // Fetch words for the selected letter
      this.$refs.searchBar.clearSearchText(); // Clear the search bar
    },
    // Fetch words by letter
    async getWordsByLetter(letter) {
      this.loading = true;
      this.letter = letter;
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
      this.searching = true; // Set search flag
      try {
        this.words = await fetchWordsBySearch(params);
        this.updateMessage(this.words.length); // Update message
      } catch (error) {
        this.message = 'Failed to fetch words. Please try again later.';
      } finally {
        this.loading = false;
      }
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
</style>