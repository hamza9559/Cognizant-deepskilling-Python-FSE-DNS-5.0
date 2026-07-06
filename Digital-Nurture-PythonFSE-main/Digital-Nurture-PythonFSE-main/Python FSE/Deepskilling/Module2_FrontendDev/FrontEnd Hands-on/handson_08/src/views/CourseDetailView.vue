<script setup>
import { computed } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import { useEnrollmentStore } from '../stores/enrollment';

const route = useRoute();
const router = useRouter();
const store = useEnrollmentStore();

const courses = [
  { id: 1, name: "Introduction to Computer Science", code: "CS101", credits: 4, grade: "A" },
  { id: 2, name: "Database Management Systems", code: "CS202", credits: 4, grade: "A-" },
  { id: 3, name: "Web Application Development", code: "CS301", credits: 3, grade: "B+" },
  { id: 4, name: "Software Engineering", code: "CS302", credits: 3, grade: "A" },
  { id: 5, name: "Data Structures & Algorithms", code: "CS201", credits: 4, grade: "A" }
];

const course = computed(() => {
  const courseId = parseInt(route.params.id, 10);
  return courses.find(c => c.id === courseId);
});

const isEnrolled = computed(() => {
  if (!course.value) return false;
  return !!store.enrolledCourses.find(c => c.id === course.value.id);
});

function handleEnroll() {
  if (course.value) {
    store.enroll(course.value);
    // Programmatic routing to profile
    router.push('/profile');
  }
}
</script>

<template>
  <div class="course-detail-page">
    <div class="detail-card" v-if="course">
      <div class="detail-header">
        <span class="detail-code">{{ course.code }}</span>
        <h2>{{ course.name }}</h2>
      </div>
      
      <div class="detail-body">
        <p class="detail-description">
          This is a comprehensive, hands-on course designed to build deep technical foundations and skilling.
          Over the course of the semester, you will work on projects, coding exercises, and exams aligned with
          modern industry standards.
        </p>
        
        <div class="detail-stats">
          <div class="detail-stat">
            <span class="stat-label">Credits</span>
            <span class="stat-value">{{ course.credits }}</span>
          </div>
          <div class="detail-stat">
            <span class="stat-label">Grade Target</span>
            <span class="stat-value">{{ course.grade }}</span>
          </div>
          <div class="detail-stat">
            <span class="stat-label">Format</span>
            <span class="stat-value">Interactive</span>
          </div>
        </div>
      </div>

      <div class="detail-actions">
        <RouterLink to="/courses" class="btn-secondary">Back to Courses</RouterLink>
        <button 
          type="button" 
          class="enroll-btn-detail"
          :class="{ enrolled: isEnrolled }"
          @click="handleEnroll"
          :disabled="isEnrolled"
        >
          {{ isEnrolled ? 'Already Enrolled' : 'Enroll in Course' }}
        </button>
      </div>
    </div>
    
    <div class="error-card" v-else>
      <h2>Course Not Found</h2>
      <p>The course ID you requested does not exist or has been removed.</p>
      <RouterLink to="/courses" class="btn-primary">Back to Courses</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.course-detail-page {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
  width: 100%;
}

.detail-card, .error-card {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 1rem;
  padding: 2.5rem;
  max-width: 700px;
  width: 100%;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.error-card {
  text-align: center;
}

.error-card h2 {
  color: #ef4444;
  margin-bottom: 1rem;
}

.error-card p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

.detail-header {
  margin-bottom: 1.5rem;
}

.detail-code {
  display: inline-block;
  background-color: #eff6ff;
  color: #1d4ed8;
  font-weight: 700;
  font-size: 0.875rem;
  padding: 0.25rem 0.75rem;
  border-radius: 0.5rem;
  margin-bottom: 0.75rem;
}

.detail-header h2 {
  font-size: 2rem;
  color: #1e3a8a;
}

.detail-body {
  margin-bottom: 2rem;
}

.detail-description {
  color: #475569;
  font-size: 1.05rem;
  margin-bottom: 2rem;
}

.detail-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  background-color: #f8fafc;
  padding: 1.25rem;
  border-radius: 0.75rem;
  border: 1px solid #f1f5f9;
}

.detail-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.detail-stat:not(:last-child) {
  border-right: 1px solid #e2e8f0;
}

.detail-stat .stat-label {
  font-size: 0.75rem;
  color: #64748b;
  text-transform: uppercase;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.detail-stat .stat-value {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e3a8a;
}

.detail-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #f1f5f9;
  padding-top: 1.5rem;
}

.btn-secondary {
  color: #1e3a8a;
  border: 1px solid #cbd5e1;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  background-color: transparent;
  transition: all 0.2s;
}

.btn-secondary:hover {
  background-color: #f1f5f9;
}

.btn-primary {
  background-color: #1e3a8a;
  color: #ffffff;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-primary:hover {
  background-color: #1d4ed8;
}

.enroll-btn-detail {
  background-color: #1e3a8a;
  color: #ffffff;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.enroll-btn-detail:hover {
  background-color: #1d4ed8;
}

.enroll-btn-detail.enrolled {
  background-color: #10b981;
  cursor: not-allowed;
}
</style>
