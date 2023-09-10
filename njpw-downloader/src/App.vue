<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import DownloadProgressToast from './components/DownloadProgressToast.vue'

const progress = ref(null)
</script>

<template>
  <header>
    <div class="wrapper">
      <nav>
        <RouterLink to="/associations">Associations</RouterLink>
        <RouterLink to="/njpwEpisodes">NJPW World Episodes</RouterLink>
        <RouterLink to="/tvdbEpisodes">TVDB Episodes</RouterLink>
        <a href="#" @click="progress.toggle()">Downloads</a>
      </nav>
    </div>
  </header>

  <main>
    <RouterView />
    <DownloadProgressToast ref="progress" />
  </main>
</template>

<style scoped>
header {
  line-height: 1.5;
  height: 100%;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: block;
  padding: 0 2rem;
  border-bottom: 1px solid var(--color-border);
}

@media (min-width: 1024px) {
  nav {
    text-align: left;
    font-size: 1rem;
    margin-top: 2rem;
  }
}
</style>
