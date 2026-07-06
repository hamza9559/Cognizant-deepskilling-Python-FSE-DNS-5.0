<script setup>
import { ref, computed, onMounted } from 'vue';
import CourseCard from '../components/CourseCard.vue';

const courses = ref([]);
const searchTerm = ref('');

onMounted(() => {
  // Initialize with 5 courses inside onMounted lifecycle hook
  courses.value = [
    { id: 1, name: "Introduction to Computer Science", code: "CS101", credits: 4, grade: "A" },
    { id: 2, name: "Database Management Systems", code: "CS202", credits: 4, grade: "A-" },
    { id: 3, name: "Web Application Development", code: "CS301", credits: 3, grade: "B+" },
    { id: 4, name: "Software Engineering", code: "CS302", credits: 3, grade: "A" },
    { id: 5, name: "Data Structures & Algorithms", code: "CS201", credits: 4, grade: "A" }
  ];
});

// Computed property filteredCourses cached automatically
const filteredCourses = computed(() => {
  const query = searchTerm.value.toLowerCase().trim();
  if (!query) return courses.value;
  
  return courses.value.filter(course => 
    course.name.toLowerCase().includes(query) || 
    course.code.toLowerCase().includes(query)
  );
});
</script>

<template>
  <div class="courses-page">
    <div class="section-header">
      <h2>Explore Courses</h2>
      <div class="controls">
        <input 
          type="text" 
          class="search-bar" 
          placeholder="Search courses by name or code..." 
          v-model="searchTerm"
        />
      </div>
    </div>

    <!-- Course Cards Grid using v-for -->
    <div class="courses-grid">
      <CourseCard 
        v-for="course in filteredCourses" 
        :key="course.id"
        :id="course.id"
        :name="course.name"
        :code="course.code"
        :credits="course.credits"
        :grade="course.grade"
      />
    </div>

    <!-- Empty State -->
    <div class="no-results" v-if="filteredCourses.length === 0">
      No courses found matching "{{ searchTerm }}"
    </div>
  </div>
</template>

<style scoped>
.courses-page {
  width: 100%;
}

.section-header {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #1e3a8a;
  position: relative;
  padding-bottom: 0.5rem;
}

.section-header h2::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 50px;
  height: 4px;
  background-color: #3b82f6;
  border-radius: 2px;
}

.search-bar {
  padding: 0.75rem 1rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  font-size: 0.95rem;
  outline: none;
  transition: all 0.2s;
  width: 100%;
}

.search-bar:focus {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.courses-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}

.no-results {
  text-align: center;
  padding: 4rem 2rem;
  font-weight: 600;
  color: #64748b;
}

@media (min-width: 768px) {
  .section-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .search-bar {
    width: 320px;
  }

  .courses-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .courses-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
