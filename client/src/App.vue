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

export default {
  name: 'App',
  computed: {
    isLessonsActive() {
      return this.$route.path.startsWith('/lessons');
    },
  },
};
</script>

<style>
@import './assets/css/fonts.css';

nav ul {
  list-style-type: none;
  padding: 0;
}

nav li {
  display: inline;
  margin-right: 10px;
}

.navbar-nav .nav-link.active {
  font-weight: bold;
}
</style>
