<script setup>
import { RouterView } from 'vue-router';
import Header from './components/Header.vue';
</script>

<template>
  <div class="app-container">
    <Header siteName="Student Portal" />
    
    <main class="main-content">
      <RouterView />
    </main>

    <footer class="site-footer">
      <p>&copy; 2026 Student Portal. All rights reserved.</p>
    </footer>
  </div>
</template>

<style>
/* Global CSS for Vue App */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: #f8fafc;
  color: #0f172a;
  line-height: 1.6;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

.site-footer {
  background-color: #0f172a;
  color: #94a3b8;
  text-align: center;
  padding: 1.5rem;
  margin-top: auto;
  font-size: 0.85rem;
}
</style>
