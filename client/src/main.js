import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import { FontAwesomeIcon } from './font-awesome';
import router from './router';

import FloatingVue from 'floating-vue';
import 'floating-vue/dist/style.css'; 

const app = createApp(App);

app
  .component('font-awesome-icon', FontAwesomeIcon)
  .use(FloatingVue)
  .use(router)
  .mount('#app');
