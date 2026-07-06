<script setup>
import { ref } from 'vue';
import { useEnrollmentStore } from '../stores/enrollment';

const store = useEnrollmentStore();

const profile = ref({
  name: 'Jane Doe',
  email: 'jane.doe@university.edu',
  semester: 6
});

function handleSave() {
  alert(`Profile Saved Successfully:\nName: ${profile.value.name}\nEmail: ${profile.value.email}\nSemester: ${profile.value.semester}`);
}
</script>

<template>
  <div class="profile-page">
    <div class="profile-layout">
      <!-- Profile Form -->
      <div class="profile-form-container">
        <div class="profile-section">
          <h3>Student Profile</h3>
          
          <form @submit.prevent="handleSave" class="profile-form">
            <div class="form-group">
              <label for="profile-name">Full Name</label>
              <input 
                type="text" 
                id="profile-name" 
                v-model="profile.name" 
                required 
              />
            </div>
            
            <div class="form-group">
              <label for="profile-email">Email Address</label>
              <input 
                type="email" 
                id="profile-email" 
                v-model="profile.email" 
                required 
              />
            </div>
            
            <div class="form-group">
              <label for="profile-semester">Current Semester</label>
              <input 
                type="number" 
                id="profile-semester" 
                v-model.number="profile.semester" 
                min="1" 
                max="8" 
                required 
              />
            </div>
            
            <button type="submit" class="save-btn">Update Profile</button>
          </form>

          <div class="profile-preview">
            <h4>Live Preview</h4>
            <p><strong>Name:</strong> {{ profile.name }}</p>
            <p><strong>Email:</strong> {{ profile.email }}</p>
            <p><strong>Semester:</strong> Semester {{ profile.semester }}</p>
          </div>
        </div>
      </div>

      <!-- Enrolled Courses -->
      <div class="profile-enrollments-container">
        <div class="enrolled-summary">
          <h3>My Enrolled Courses</h3>
          
          <div v-if="store.enrolledCourses.length > 0">
            <ul class="enrolled-list">
              <li 
                v-for="course in store.enrolledCourses" 
                :key="course.id" 
                class="enrolled-item-expanded"
              >
                <div class="item-meta">
                  <span class="enrolled-code">{{ course.code }}</span>
                  <span class="enrolled-name">{{ course.name }}</span>
                  <span class="enrolled-credits">({{ course.credits }} Credits)</span>
                </div>
                <button 
                  type="button" 
                  class="remove-course-btn" 
                  @click="store.unenroll(course.id)"
                >
                  Remove
                </button>
              </li>
            </ul>
            
            <div class="credits-total">
              Total Enrolled Credits: <strong>{{ store.totalCredits }}</strong>
            </div>
          </div>
          
          <p class="no-enrollments" v-else>
            No courses enrolled yet. Browse courses to add them.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  width: 100%;
}

.profile-layout {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.profile-form-container,
.profile-enrollments-container {
  flex: 1;
}

.profile-section,
.enrolled-summary {
  background-color: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.profile-section h3,
.enrolled-summary h3 {
  font-size: 1.2rem;
  color: #1e3a8a;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f1f5f9;
}

.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #475569;
}

.form-group input {
  padding: 0.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 0.375rem;
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}

.form-group input:focus {
  border-color: #3b82f6;
}

.save-btn {
  background-color: #1e3a8a;
  color: #ffffff;
  border: none;
  padding: 0.6rem;
  font-weight: 600;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-btn:hover {
  background-color: #1d4ed8;
}

.profile-preview {
  background-color: #f8fafc;
  border: 1px dashed #cbd5e1;
  border-radius: 0.5rem;
  padding: 1rem;
}

.profile-preview h4 {
  font-size: 0.9rem;
  color: #64748b;
  margin-bottom: 0.5rem;
}

.profile-preview p {
  font-size: 0.875rem;
  color: #334155;
  margin-bottom: 0.25rem;
}

.enrolled-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.enrolled-item-expanded {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.enrolled-code {
  font-size: 0.75rem;
  font-weight: 700;
  color: #10b981;
  background-color: #ecfdf5;
  padding: 0.15rem 0.4rem;
  border-radius: 0.25rem;
}

.enrolled-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #334155;
}

.enrolled-credits {
  font-size: 0.8rem;
  color: #64748b;
}

.remove-course-btn {
  background-color: #fef2f2;
  color: #ef4444;
  border: 1px solid #fca5a5;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  font-weight: 600;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-course-btn:hover {
  background-color: #ef4444;
  color: #ffffff;
  border-color: #ef4444;
}

.credits-total {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
  font-size: 1rem;
  text-align: right;
  color: #1e3a8a;
}

.no-enrollments {
  font-size: 0.875rem;
  color: #94a3b8;
  font-style: italic;
}

@media (min-width: 1024px) {
  .profile-layout {
    flex-direction: row;
    align-items: flex-start;
  }
}
</style>
