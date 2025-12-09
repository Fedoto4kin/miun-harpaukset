<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-lg">
        <router-link class="navbar-brand" to="/">Miun harpaukšet karielan kieleh</router-link>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/lessons" :class="{ active: isLessonsActive }">Urokat</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/lexicon" exact-active-class="active">Šanakniiga</router-link>
            </li>
            
            <li class="nav-item dropdown" :class="{ show: grammarDropdownOpen }" @mouseenter="openGrammarDropdown" @mouseleave="closeGrammarDropdown">
              <a class="nav-link dropdown-toggle" href="#" id="grammarDropdown" role="button"
                :aria-expanded="grammarDropdownOpen" @click.prevent="toggleGrammarDropdown">
                Grammatikka
              </a>
              <ul class="dropdown-menu" :class="{ show: grammarDropdownOpen }" aria-labelledby="grammarDropdown">
                <li v-if="loadingGrammar">
                  <a class="dropdown-item disabled" href="#">
                    <span class="spinner-border spinner-border-sm" role="status"></span>
                  </a>
                </li>
                <template v-else>
                  <li v-for="table in grammarTables" :key="table.id">
                    <router-link 
                      class="dropdown-item" 
                      :to="`/grammar/${table.id}`"
                      @click="closeGrammarDropdown"
                      :class="{ active: $route.params.id === String(table.id) }"
                    >
                      {{ table.title }}
                    </router-link>
                  </li>
                </template>
              </ul>
            </li>
            
            <li class="nav-item">
              <router-link class="nav-link" to="/books" exact-active-class="active">Literatura</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/authors" exact-active-class="active">Luadijat</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <router-view></router-view>
  </div>
</template>

<script>
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { grammarService } from '@/services/grammarService';

export default {
  name: 'App',
  data() {
    return {
      grammarDropdownOpen: false,
      grammarTables: [],
      loadingGrammar: false,
      grammarError: null,
      dropdownTimer: null
    };
  },
  computed: {
    isLessonsActive() {
      return this.$route.path.startsWith('/lessons');
    },
  },
  created() {
    this.fetchGrammarTables();
  },
  methods: {
    async fetchGrammarTables() {
      this.loadingGrammar = true;
      this.grammarError = null;
      
      try {
        const response = await grammarService.getAll();
        this.grammarTables = response.data.slice(0, 10);
      } catch (error) {
        console.error('Error fetching grammar tables:', error);
        this.grammarError = 'Не удалось загрузить таблицы';
      } finally {
        this.loadingGrammar = false;
      }
    },
    
    toggleGrammarDropdown() {
      this.grammarDropdownOpen = !this.grammarDropdownOpen;
    },
    
    openGrammarDropdown() {
      clearTimeout(this.dropdownTimer);
      this.grammarDropdownOpen = true;
    },
    
    closeGrammarDropdown() {
      this.dropdownTimer = setTimeout(() => {
        this.grammarDropdownOpen = false;
      }, 200);
    },
    
    handleClickOutside(event) {
      const dropdown = this.$el.querySelector('.dropdown');
      if (dropdown && !dropdown.contains(event.target)) {
        this.grammarDropdownOpen = false;
      }
    }
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside);
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside);
    clearTimeout(this.dropdownTimer);
  },
};
</script>

<style>
@import './assets/css/fonts.css';

.navbar-nav .nav-link.active {
  font-weight: bold;
}

.dropdown-menu {
  max-height: 400px;
  overflow-y: auto;
  z-index: 666666;
}

.dropdown-item.active {
  background-color: #0d6efd;
  color: white;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
}

.dropdown-item.active:hover {
  background-color: #0b5ed7;
}

/* Для мобильных устройств */
@media (max-width: 992px) {
  .dropdown-menu {
    position: static !important;
    transform: none !important;
    border: none;
    box-shadow: none;
  }
  
  .nav-item.dropdown {
    position: static;
  }
}
</style>