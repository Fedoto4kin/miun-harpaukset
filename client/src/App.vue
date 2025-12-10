<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-lg">
        <router-link class="navbar-brand" to="/" @click="closeMobileMenu">
          Miun harpaukšet karielan kieleh
        </router-link>

        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
          aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            <li class="nav-item">
              <router-link class="nav-link" to="/lessons" @click="closeMobileMenu"
                :class="{ active: isLessonsActive }">Urokat</router-link>
            </li>
            
            <!-- Кастомный dropdown для Grammatikka -->
            <li class="nav-item dropdown-custom" :class="{
              'show': grammarDropdownOpen,
              'active-dropdown': isGrammarActive
            }">
              <a class="nav-link dropdown-toggle-custom" href="#" 
                :class="{ active: isGrammarActive }"
                @click.prevent="toggleGrammarDropdown"
                @mouseenter="!isMobile && openGrammarDropdown()"
                @mouseleave="!isMobile && closeGrammarDropdownWithDelay()">
                Grammatikka
                <span class="dropdown-arrow" :class="{ 'rotated': grammarDropdownOpen }">▼</span>
              </a>

              <transition name="dropdown">
                <ul v-if="grammarDropdownOpen" class="dropdown-menu-custom" 
                    @mouseenter="!isMobile && cancelCloseDropdown()"
                    @mouseleave="!isMobile && closeGrammarDropdownWithDelay()"
                    @click.stop="handleDropdownClick">
                  
                  <!-- Если данные еще загружаются -->
                  <li v-if="loadingGrammar" class="dropdown-loading">
                    <span class="spinner-border spinner-border-sm" role="status"></span>
                    <span class="loading-text">Загрузка...</span>
                  </li>
                  
                  <!-- Если загрузка завершена и есть данные -->
                  <template v-else-if="grammarTables.length > 0">
                    <li v-for="table in grammarTables" :key="table.id">
                      <router-link class="dropdown-item-custom" 
                        :to="`/grammar/${table.id}`"
                        :class="{ active: $route.params.id === String(table.id) }"
                        @click="handleGrammarItemClick">
                        {{ table.title }}
                      </router-link>
                    </li>
                  </template>
                  
                  <!-- Если загрузка завершена, но данных нет -->
                  <li v-else class="dropdown-empty">
                    <span class="empty-text">---</span>
                  </li>
                </ul>
              </transition>
            </li>

            <li class="nav-item">
              <router-link class="nav-link" to="/lexicon" @click="closeMobileMenu"
                exact-active-class="active">Šanakniiga</router-link>
            </li>

            <li class="nav-item">
              <router-link class="nav-link" to="/books" @click="closeMobileMenu"
                exact-active-class="active">Literatura</router-link>
            </li>
          </ul>

          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/authors" @click="closeMobileMenu"
                exact-active-class="active">Luadijat</router-link>
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
      grammarTables: [], // Изначально пустой массив
      loadingGrammar: true, // Начинаем с состояния загрузки
      dropdownTimer: null,
      closeDropdownTimer: null,
      windowWidth: window.innerWidth,
    };
  },
  computed: {
    isLessonsActive() {
      return this.$route.path.startsWith('/lessons');
    },
    isGrammarActive() {
      return this.$route.path.startsWith('/grammar');
    },
    isMobile() {
      return this.windowWidth <= 992;
    }
  },
  watch: {
    isGrammarActive(newVal) {
      if (this.isMobile && newVal) {
        setTimeout(() => {
          const navbar = document.getElementById('navbarNav');
          if (navbar && navbar.classList.contains('show')) {
            this.grammarDropdownOpen = true;
          }
        }, 100);
      }
    },
    windowWidth() {
      if (!this.isMobile) {
        this.grammarDropdownOpen = false;
      }
    }
  },
  // Загружаем данные как можно раньше
  async created() {
    // Запускаем загрузку данных немедленно
    await this.loadGrammarData();
  },
  mounted() {
    // Настраиваем обработчики событий после загрузки данных
    this.setupEventListeners();
  },
  methods: {
    async loadGrammarData() {
      try {
        const response = await grammarService.getAll();
        this.grammarTables = response.data.slice(0, 10);
      } catch (error) {
        console.error('Error fetching grammar tables:', error);
        this.grammarTables = [];
      } finally {
        this.loadingGrammar = false;
      }
    },
    
    setupEventListeners() {
      document.addEventListener('click', this.handleDocumentClick);
      window.addEventListener('resize', this.handleResize);
      
      const navbar = document.getElementById('navbarNav');
      if (navbar) {
        navbar.addEventListener('show.bs.collapse', this.handleNavbarShow);
        navbar.addEventListener('hide.bs.collapse', this.handleNavbarHide);
      }
    },

    handleResize() {
      this.windowWidth = window.innerWidth;
    },

    handleNavbarShow() {
      if (this.isMobile && this.isGrammarActive) {
        setTimeout(() => {
          this.grammarDropdownOpen = true;
        }, 150);
      }
    },

    handleNavbarHide() {
      if (this.isMobile) {
        this.grammarDropdownOpen = false;
      }
    },

    toggleGrammarDropdown(event) {
      event.preventDefault();
      event.stopPropagation();
      
      if (this.isMobile) {
        this.grammarDropdownOpen = !this.grammarDropdownOpen;
      } else {
        this.grammarDropdownOpen = !this.grammarDropdownOpen;
      }
    },

    openGrammarDropdown() {
      clearTimeout(this.dropdownTimer);
      clearTimeout(this.closeDropdownTimer);
      this.grammarDropdownOpen = true;
    },

    closeGrammarDropdownWithDelay() {
      if (!this.isMobile) {
        this.closeDropdownTimer = setTimeout(() => {
          this.grammarDropdownOpen = false;
        }, 200);
      }
    },

    cancelCloseDropdown() {
      clearTimeout(this.closeDropdownTimer);
    },

    handleGrammarItemClick() {
      this.grammarDropdownOpen = false;
      this.closeMobileMenu();
    },

    handleDropdownClick(event) {
      event.stopPropagation();
    },

    closeMobileMenu() {
      if (this.isMobile) {
        this.closeNavbarWithoutAnimation();
      }
    },

    closeNavbarWithoutAnimation() {
      const navbarCollapse = document.getElementById('navbarNav');
      const toggler = document.querySelector('.navbar-toggler');

      if (!navbarCollapse || !navbarCollapse.classList.contains('show')) {
        return;
      }

      const originalTransition = navbarCollapse.style.transition;
      const originalWebkitTransition = navbarCollapse.style.webkitTransition;

      navbarCollapse.style.transition = 'none';
      navbarCollapse.style.webkitTransition = 'none';

      if (toggler) {
        toggler.click();
      }

      setTimeout(() => {
        if (navbarCollapse) {
          navbarCollapse.style.transition = originalTransition;
          navbarCollapse.style.webkitTransition = originalWebkitTransition;
        }
      }, 10);
    },

    handleDocumentClick(event) {
      const dropdownElement = this.$el.querySelector('.dropdown-custom');
      if (dropdownElement && !dropdownElement.contains(event.target)) {
        this.grammarDropdownOpen = false;
      }
    }
  },
  beforeUnmount() {
    this.grammarDropdownOpen = false;
    clearTimeout(this.dropdownTimer);
    clearTimeout(this.closeDropdownTimer);

    document.removeEventListener('click', this.handleDocumentClick);
    window.removeEventListener('resize', this.handleResize);
    
    const navbar = document.getElementById('navbarNav');
    if (navbar) {
      navbar.removeEventListener('show.bs.collapse', this.handleNavbarShow);
      navbar.removeEventListener('hide.bs.collapse', this.handleNavbarHide);
    }
  },
};
</script>

<style>
@import './assets/css/fonts.css';

.navbar-nav .nav-link.active {
  font-weight: bold;
}

.nav-item.dropdown-custom {
  position: relative;
}

.nav-item.dropdown-custom.active-dropdown > .dropdown-toggle-custom {
  font-weight: bold;
}

.navbar-nav li.nav-item {
  padding-left: 1em;
}

/* Стили для кастомного dropdown */
.dropdown-toggle-custom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  position: relative;
  padding-right: 25px !important;
}

.dropdown-arrow {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  transition: transform 0.3s ease;
}

.dropdown-arrow.rotated {
  transform: translateY(-50%) rotate(180deg);
}

.dropdown-menu-custom {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  min-width: 200px;
  padding: 0.5rem 0;
  margin: 0.125rem 0 0;
  font-size: 1rem;
  color: #212529;
  text-align: left;
  list-style: none;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0,0,0,.15);
  border-radius: 0.25rem;
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,.175);
  z-index: 66666;
}

.dropdown-item-custom {
  display: block;
  width: 100%;
  padding: 0.25rem 1.5rem;
  clear: both;
  font-weight: 400;
  color: #212529;
  text-align: inherit;
  text-decoration: none;
  white-space: nowrap;
  background-color: transparent;
  border: 0;
  cursor: pointer;
}

.dropdown-item-custom:hover,
.dropdown-item-custom:focus {
  color: #16181b;
  text-decoration: none;
  background-color: #f8f9fa;
}

.dropdown-item-custom.active {
  color: #fff;
  text-decoration: none;
  background-color: #0d6efd;
}

.dropdown-item-custom.active:hover {
  background-color: #0b5ed7;
}

.dropdown-item-custom.disabled {
  color: #6c757d;
  pointer-events: none;
  background-color: transparent;
}

/* Анимации для dropdown */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px);
  max-height: 0;
}

.dropdown-enter-to,
.dropdown-leave-from {
  opacity: 1;
  transform: translateY(0);
  max-height: 400px;
}

/* Для мобильных устройств */
@media (max-width: 992px) {
  .dropdown-menu-custom {
    position: static !important;
    transform: none !important;
    border: none;
    box-shadow: none;
    width: 100%;
    max-height: 300px;
    overflow-y: auto;
  }

  .dropdown-toggle-custom {
    padding-right: 15px !important;
  }
  
  .dropdown-arrow {
    right: 5px;
  }
  
  /* Класс для быстрого закрытия без анимации */
  .navbar-collapse.fast-collapse {
    transition: none !important;
  }
}
</style>