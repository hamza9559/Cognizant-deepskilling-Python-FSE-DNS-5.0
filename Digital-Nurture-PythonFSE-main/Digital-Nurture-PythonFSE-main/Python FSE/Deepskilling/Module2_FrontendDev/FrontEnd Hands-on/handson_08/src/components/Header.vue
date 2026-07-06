<script setup>
import { RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

defineProps({
  siteName: {
    type: String,
    default: 'Student Portal'
  }
});

const store = useEnrollmentStore();
</script>

<template>
  <header class="site-header">
    <div class="logo">
      <RouterLink to="/" style="text-decoration: none; color: white;">
        <span>{{ siteName }}</span>
      </RouterLink>
    </div>
    <nav class="nav-menu">
      <ul>
        <li><RouterLink to="/" active-class="active">Home</RouterLink></li>
        <li><RouterLink to="/courses" active-class="active">Courses</RouterLink></li>
        <li><RouterLink to="/profile" active-class="active">Profile</RouterLink></li>
      </ul>
    </nav>
    <div class="enrollment-badge">
      Enrolled: <span class="badge-count">{{ store.enrolledCourses.length }}</span>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  background-color: #1e3a8a;
  color: #ffffff;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.logo span {
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-menu ul {
  list-style: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.nav-menu ul li a {
  color: #cbd5e1;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-menu ul li a:hover,
.nav-menu ul li a.active {
  color: #ffffff;
}

.enrollment-badge {
  background-color: rgba(255, 255, 255, 0.15);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.badge-count {
  background-color: #10b981;
  color: #ffffff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
}
</style>
