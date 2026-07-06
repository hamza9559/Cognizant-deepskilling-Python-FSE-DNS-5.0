<script setup>
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="home-page">
    <section class="hero-landing">
      <h1>Welcome to Student Portal</h1>
      <p>Your integrated digital workspace for academic success. Access your profile, browse available courses, register for subjects, and keep track of your grades in real time.</p>
      <div class="hero-actions">
        <RouterLink to="/courses" class="btn-primary">Browse Courses</RouterLink>
        <RouterLink to="/profile" class="btn-secondary">View Profile</RouterLink>
      </div>
    </section>

    <section class="portal-features">
      <h2>Portal Features</h2>
      <div class="features-grid">
        <div class="feature-card">
          <h3>Composition API</h3>
          <p>Built with Vue 3's reactive reference and script setup syntax for clean and performant logic.</p>
        </div>
        <div class="feature-card">
          <h3>Pinia State</h3>
          <p>Powered by Pinia for global state management of enrolled courses and computed totals.</p>
        </div>
        <div class="feature-card">
          <h3>Vue Router</h3>
          <p>Multi-page routing with path parameter detail views and automated navigation guards.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home-page {
  width: 100%;
}

.hero-landing {
  text-align: center;
  background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
  color: #ffffff;
  padding: 5rem 2rem;
  border-radius: 1rem;
  margin-bottom: 3rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.hero-landing h1 {
  font-size: clamp(2.25rem, 5vw, 3.5rem);
  font-weight: 800;
  margin-bottom: 1.5rem;
}

.hero-landing p {
  font-size: 1.15rem;
  color: #e2e8f0;
  max-width: 800px;
  margin: 0 auto 2.5rem auto;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.btn-primary {
  background-color: #ffffff;
  color: #1e3a8a;
  padding: 0.75rem 1.75rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background-color: #eff6ff;
}

.btn-secondary {
  background-color: transparent;
  color: #ffffff;
  padding: 0.75rem 1.75rem;
  border: 2px solid #ffffff;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.portal-features h2 {
  font-size: 1.875rem;
  color: #1e3a8a;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.feature-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.feature-card h3 {
  color: #1e3a8a;
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  color: #475569;
  font-size: 0.95rem;
}

@media (min-width: 768px) {
  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .features-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
