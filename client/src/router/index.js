import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import LexiconComponent from '../components/LexiconComponent.vue';
import LessonsComponent from '../components/LessonsComponent.vue';
import AuthorsComponent from '../components/AuthorsComponent.vue';
import BooksComponent from '../components/BooksComponent.vue';
import GrammarTableDetail from '@/components/grammar/GrammarTableDetail.vue';
import NotFoundComponent from '@/components/NotFoundComponent.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeComponent,
  },
  {
    path: '/lexicon',
    name: 'Lexicon',
    component: LexiconComponent,
    props: (route) => ({
      // Обратная совместимость
      query: route.query.q,
      mode: route.query.reverse === 'true' ? 'translate' : 'search',
      letter: route.query.letter
    }),
    // Добавляем переадресацию
    beforeEnter: (to, from, next) => {
      // Если есть параметры поиска, оставляем как есть
      if (to.query.q || to.query.letter) {
        next();
      } else {
        // Иначе перенаправляем на /lexicon/A
        next('/lexicon/A');
      }
    }
  },
  {
    // Новый формат для поиска
    path: '/lexicon/search/:query',
    name: 'LexiconSearch',
    component: LexiconComponent,
    props: (route) => ({
      query: route.params.query,
      mode: 'search'
    }),
  },
  {
    // Новый формат для обратного перевода
    path: '/lexicon/translate/:query',
    name: 'LexiconTranslate',
    component: LexiconComponent,
    props: (route) => ({
      query: route.params.query,
      mode: 'translate'
    }),
  },
  {
    // Новый формат для букв (один символ - это всегда буква)
    path: '/lexicon/:letter',
    name: 'LexiconLetter',
    component: LexiconComponent,
    props: (route) => ({
      letter: route.params.letter
    }),
    // Валидация параметра буквы
    beforeEnter: (to, from, next) => {
      const letter = to.params.letter;
      const validLetters = 'ABCČDEFGHIJKLMNOPRSŠZŽTUVYÄÖ';
      
      // Проверяем, что буква валидная (одна и входит в алфавит)
      if (letter && letter.length === 1 && validLetters.includes(letter.toUpperCase())) {
        next();
      } else {
        // Если буква невалидная, перенаправляем на A
        next('/lexicon/A');
      }
    }
  },
  {
    path: '/lessons/:id?/:moduleId?',
    name: 'Lessons',
    component: LessonsComponent,
  },
  {
    path: '/authors',
    name: 'Authors',
    component: AuthorsComponent,
  },
  {
    path: '/books',
    name: 'Books',
    component: BooksComponent,
  },
  {
    path: '/grammar/:id',
    name: 'GrammarTableDetail',
    component: GrammarTableDetail,
    props: true,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundComponent,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;