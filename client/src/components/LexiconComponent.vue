<template>
  <div class="container">
    <div class="row my-4">
      <h1 class="mt-4 col-6">{{ title }}</h1>
      <SearchBar @pushSearchStr="getWordsBySearch" />
    </div>
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
    <div v-if="loading" class="text-center mt-4">
      <img src="/img/preloader.gif" alt="Loading..." />
    </div>
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
    };
  },
  methods: {
    getWordsByLetter(letter) {
      this.loading = true;
      this.letter = letter;
      axios.get(`v0/lexicon/search/${letter}/`)
        .then((response) => {
        console.log(response.data);
          this.words = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getWordsBySearch(params) {
      this.loading = true;
      const url = params.reverse ? `v0/lexicon/reverse/${params.search}/` : `v0/lexicon/search/${params.search}/`;
      axios.get(url, { params: params })
        .then((response) => {
          this.words = response.data;
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  created() {
    this.getWordsByLetter(this.letter);
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
