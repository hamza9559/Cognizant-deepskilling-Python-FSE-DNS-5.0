import { courses } from './data.js';

// --- Task 1: ES6+ Syntax Practice ---

// 1. Destructure name and credits in a loop (using arrow function version of loop)
console.log("=== Course Destructuring Loop ===");
courses.forEach(({ name, credits }) => {
    console.log(`Course: ${name}, Credits: ${credits}`);
});

// 2. Use Array.map() to create formatted strings
const courseStrings = courses.map(({ code, name, credits }) => `${code} — ${name} (${credits} credits)`);
console.log("=== Formatted Course Strings (Map) ===");
console.log(courseStrings);

// 3. Use Array.filter() to get only courses with credits >= 4
const highCreditCourses = courses.filter(course => course.credits >= 4);
console.log("=== High Credit Courses (Filter) ===");
console.log(`Count of courses with >= 4 credits: ${highCreditCourses.length}`);
console.log(highCreditCourses);

// 4. Use Array.reduce() to calculate total credits
const totalCreditsValue = courses.reduce((sum, course) => sum + course.credits, 0);
console.log("=== Total Credits Enrolled (Reduce) ===");
console.log(`Total Credits: ${totalCreditsValue}`);


// --- Task 2 & 3: DOM Selection, Dynamic Rendering, & Interactivity ---

// State copy of courses array to allow sorting/filtering
let currentCourses = [...courses];
let isSortedAscending = false; // toggle sort state

const gridContainer = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-courses');
const selectedSection = document.getElementById('selected-course-section');
const selectedCardContent = document.getElementById('selected-course-card');

// Render Function
function renderCourses(coursesList) {
    // Clear container
    gridContainer.innerHTML = '';
    
    // Use DocumentFragment for performance batch insertion
    const fragment = document.createDocumentFragment();
    
    coursesList.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        // Set attribute for event delegation
        article.setAttribute('data-id', course.id);
        article.setAttribute('tabindex', '0'); // make keyboard-focusable
        
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
    
    // Update total credits count dynamically
    const sumCredits = coursesList.reduce((sum, c) => sum + c.credits, 0);
    totalCreditsEl.textContent = `Total Credits Enrolled: ${sumCredits}`;
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
    // Sort descending by credits
    currentCourses.sort((a, b) => b.credits - a.credits);
    renderCourses(currentCourses);
    sortButton.textContent = 'Sorted by Credits';
    sortButton.classList.add('active-btn');
});

// Event Delegation for clicking a course card
gridContainer.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (!card) return;
    
    const courseId = parseInt(card.getAttribute('data-id'), 10);
    const selectedCourse = courses.find(c => c.id === courseId);
    
    if (selectedCourse) {
        showSelectedCourse(selectedCourse);
    }
});

function showSelectedCourse(course) {
    selectedSection.classList.remove('hidden');
    selectedCardContent.innerHTML = `
        <div class="selected-details">
            <h4>${course.name}</h4>
            <p><strong>Code:</strong> ${course.code}</p>
            <p><strong>Credits:</strong> ${course.credits}</p>
            <p><strong>Current Grade:</strong> ${course.grade}</p>
            <button type="button" id="close-details-btn">Close Details</button>
        </div>
    `;
    
    // Smooth scroll to details
    selectedSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // Add close button event
    document.getElementById('close-details-btn').addEventListener('click', () => {
        selectedSection.classList.add('hidden');
    });
}
