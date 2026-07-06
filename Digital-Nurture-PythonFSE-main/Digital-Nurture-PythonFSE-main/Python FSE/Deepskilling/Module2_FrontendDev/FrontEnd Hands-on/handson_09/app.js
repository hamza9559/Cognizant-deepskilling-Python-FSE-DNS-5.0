import { courses } from './data.js';

// Hamburger mobile navigation toggler with aria-expanded update (Step 131)
const hamburger = document.getElementById('hamburger-menu');
const navList = document.getElementById('nav-list');

if (hamburger && navList) {
    hamburger.addEventListener('click', () => {
        const isExpanded = hamburger.getAttribute('aria-expanded') === 'true';
        hamburger.setAttribute('aria-expanded', !isExpanded);
        navList.classList.toggle('nav-links-collapsed');
        navList.classList.toggle('nav-links-expanded');
    });
}

// Active navigation link handler
const navLinks = document.querySelectorAll('.nav-link');
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        navLinks.forEach(l => {
            l.classList.remove('active');
            l.removeAttribute('aria-current');
        });
        e.target.classList.add('active');
        e.target.setAttribute('aria-current', 'page');
    });
});

let currentCourses = [...courses];
const gridContainer = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-courses');
const selectedSection = document.getElementById('selected-course-section');
const selectedCardContent = document.getElementById('selected-course-card');

// Render Function with semantic fixing (headings H3 inside cards, grid container role status)
function renderCourses(coursesList) {
    gridContainer.innerHTML = '';
    const fragment = document.createDocumentFragment();
    
    coursesList.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.setAttribute('data-id', course.id);
        article.setAttribute('tabindex', '0'); // keyboard-focusable (Step 129)
        article.setAttribute('role', 'button'); // semantic button description
        article.setAttribute('aria-label', `Course details for ${course.name}. Code: ${course.code}, Credits: ${course.credits}`);
        
        // H3 headings inside cards follow H2 section header (Step 126)
        article.innerHTML = `
            <h3>${course.name}</h3>
            <p>Learn structural development, design patterns, and programming frameworks in this comprehensive program.</p>
            <div class="course-footer">
                <span class="course-code">${course.code}</span>
                <span class="course-credits">Credits: ${course.credits}</span>
            </div>
        `;
        fragment.appendChild(article);
    });
    
    gridContainer.appendChild(fragment);
    
    // Update total credits dynamically
    const sumCredits = coursesList.reduce((sum, c) => sum + c.credits, 0);
    
    // role="status" and aria-live="polite" are declared on totalCreditsEl in HTML.
    // Screen readers will announce this change. (Step 130)
    totalCreditsEl.textContent = `Total Credits Enrolled: ${sumCredits} (${coursesList.length} courses listed)`;
}

// Initial render
renderCourses(currentCourses);

// Search filtering (input event)
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const filtered = courses.filter(course => 
        course.name.toLowerCase().includes(query) || 
        course.code.toLowerCase().includes(query)
    );
    renderCourses(filtered);
});

// Sorting (click event)
sortButton.addEventListener('click', () => {
    currentCourses.sort((a, b) => b.credits - a.credits);
    renderCourses(currentCourses);
    sortButton.textContent = 'Sorted by Credits';
    sortButton.setAttribute('aria-label', 'Course list is sorted by credit count descending');
    sortButton.classList.add('active-btn');
});

// Shared Detail View Trigger
function triggerCourseSelection(courseId) {
    const selectedCourse = courses.find(c => c.id === courseId);
    if (!selectedCourse) return;
    
    selectedSection.classList.remove('hidden');
    selectedCardContent.innerHTML = `
        <div class="selected-details">
            <h4>${selectedCourse.name}</h4>
            <p><strong>Code:</strong> ${selectedCourse.code}</p>
            <p><strong>Credits:</strong> ${selectedCourse.credits}</p>
            <p><strong>Current Grade:</strong> ${selectedCourse.grade}</p>
            <button type="button" id="close-details-btn" aria-label="Close selected course details panel">Close Details</button>
        </div>
    `;
    
    selectedSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    const closeBtn = document.getElementById('close-details-btn');
    closeBtn.addEventListener('click', () => {
        selectedSection.classList.add('hidden');
        // Return focus to the clicked card for keyboard navigation flow
        const originalCard = document.querySelector(`.course-card[data-id="${courseId}"]`);
        if (originalCard) originalCard.focus();
    });
}

// Event Delegation for click events
gridContainer.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (!card) return;
    const courseId = parseInt(card.getAttribute('data-id'), 10);
    triggerCourseSelection(courseId);
});

// Keyboard Accessibility: Event Delegation for keydown event (Step 129)
gridContainer.addEventListener('keydown', (e) => {
    const card = e.target.closest('.course-card');
    if (!card) return;
    
    // Pressing Enter or Space triggers the selection
    if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault(); // prevent default browser scrolling for Space key
        const courseId = parseInt(card.getAttribute('data-id'), 10);
        triggerCourseSelection(courseId);
    }
});
