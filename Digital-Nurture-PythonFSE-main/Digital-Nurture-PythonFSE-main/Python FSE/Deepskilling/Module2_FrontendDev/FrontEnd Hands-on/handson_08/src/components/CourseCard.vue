<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  id: {
    type: Number,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  code: {
    type: String,
    required: true
  },
  credits: {
    type: Number,
    required: true
  },
  grade: {
    type: String,
    required: true
  }
});
</script>

<template>
  <article class="course-card">
    <div class="course-card-content">
      <RouterLink :to="'/courses/' + id" class="course-title-link">
        <h3>{{ name }}</h3>
      </RouterLink>
      <p>Gain advanced knowledge and core skills in this specialized subject area.</p>
      <div class="course-details">
        <span class="course-code">{{ code }}</span>
        <span class="course-credits">Credits: {{ credits }}</span>
        <span class="course-grade">Grade Target: {{ grade }}</span>
      </div>
    </div>
    <div class="course-card-actions">
      <RouterLink :to="'/courses/' + id" class="view-details-link">View Details</RouterLink>
    </div>
  </article>
</template>

<style scoped>
.course-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 200px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
  border-color: #bfdbfe;
}

.course-title-link {
  text-decoration: none;
  color: #1e3a8a;
}

.course-title-link:hover h3 {
  color: #3b82f6;
}

.course-card h3 {
  font-size: 1.15rem;
  margin-bottom: 0.5rem;
}

.course-card p {
  font-size: 0.9rem;
  color: #475569;
  margin-bottom: 1.25rem;
}

.course-details {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.course-code {
  background-color: #eff6ff;
  color: #1d4ed8;
  font-weight: 600;
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
}

.course-credits,
.course-grade {
  background-color: #f1f5f9;
  color: #475569;
  font-weight: 500;
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  border-radius: 0.25rem;
}

.course-card-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f1f5f9;
  padding-top: 1rem;
  margin-top: auto;
}

.view-details-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #3b82f6;
  text-decoration: none;
}

.view-details-link:hover {
  text-decoration: underline;
}
</style>
