import { createRouter, createWebHistory } from 'vue-router';
import HomeComponent from '../components/HomeComponent.vue';
import LexiconComponent from '../components/LexiconComponent.vue';
import LessonsComponent from '../components/LessonsComponent.vue';
import AuthorsComponent from '../components/AuthorsComponent.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeComponent
  },
  {
    path: '/lexicon',
    name: 'Lexicon',
    component: LexiconComponent
  },
  {
    path: '/lessons',
    name: 'Lessons',
    component: LessonsComponent
  },
  {
    path: '/authors',
    name: 'Authors',
    component: AuthorsComponent,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
