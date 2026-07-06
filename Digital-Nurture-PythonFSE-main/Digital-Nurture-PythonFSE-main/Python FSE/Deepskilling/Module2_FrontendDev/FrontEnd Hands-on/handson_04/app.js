import { courses } from './data.js';

/* 
========================================================================
TASK 3: FETCH API VS AXIOS SIDE-BY-SIDE COMPARISON
========================================================================
Differences:
1. Request Setup & Data Parsing:
   - Fetch: Requires two steps. First call fetch(), then parse response (e.g. response.json()).
   - Axios: Automatically parses JSON. The resulting data is available directly in response.data.

2. Error Handling / Non-2xx Responses:
   - Fetch: Rejects only on network failure. A 404 or 500 error is considered a successful completion,
            requiring manual inspection of response.ok (or response.status) to throw an error.
   - Axios: Automatically throws an error for any status code outside the 2xx range (e.g. 404, 500),
            which can be caught directly in a try/catch block.

3. Features & Configuration:
   - Fetch: Bare-bones API built into browsers. Lacks advanced features out-of-the-box.
   - Axios: Feature-rich library providing Request/Response Interceptors, request timeouts (e.g. timeout: 5000),
            automatic CSRF protection, and upload/download progress events.
========================================================================
*/

// --- Task 1: Promises and async/await ---

// 45. Promise Chaining fetchUser
function fetchUser(id) {
    fetch(`https://jsonplaceholder.typicode.com/users/${id}`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(user => {
            console.log(`[Promise Chain] User ${id} Name:`, user.name);
        })
        .catch(err => console.error(`[Promise Chain] Error:`, err));
}

// 46. Async/Await with try/catch rewrite
async function fetchUserAsync(id) {
    try {
        const response = await fetch(`https://jsonplaceholder.typicode.com/users/${id}`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const user = await response.json();
        console.log(`[Async/Await] User ${id} Name:`, user.name);
        return user;
    } catch (err) {
        console.error(`[Async/Await] Error:`, err);
        throw err;
    }
}

// 47. Simulate 1-second network delay for courses
function fetchAllCourses() {
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(courses);
        }, 1000);
    });
}

// 49. Demonstrate Promise.all()
async function runPromiseAllDemo() {
    console.log("=== Starting Promise.all() Demo ===");
    try {
        const promise1 = fetch(`https://jsonplaceholder.typicode.com/users/1`).then(r => r.json());
        const promise2 = fetch(`https://jsonplaceholder.typicode.com/users/2`).then(r => r.json());
        
        const [user1, user2] = await Promise.all([promise1, promise2]);
        console.log(`[Promise.all] User 1: ${user1.name}, User 2: ${user2.name}`);
        console.log("=== Promise.all() Completed ===");
    } catch (err) {
        console.error("Promise.all() error:", err);
    }
}

// Execute Promise.all demo and test functions on load
fetchUser(1);
fetchUserAsync(2);
runPromiseAllDemo();


// --- Task 2: Fetch API with Error Handling & UI Rendering ---

const gridContainer = document.querySelector('.course-grid');
const totalCreditsEl = document.getElementById('total-credits');
const coursesLoader = document.getElementById('courses-loader');
const searchInput = document.getElementById('search-courses');
const sortButton = document.getElementById('sort-courses');
const selectedSection = document.getElementById('selected-course-section');
const selectedCardContent = document.getElementById('selected-course-card');

let currentCourses = [];

// Render Course Grid
function renderCourses(coursesList) {
    gridContainer.innerHTML = '';
    const fragment = document.createDocumentFragment();
    
    coursesList.forEach(course => {
        const article = document.createElement('article');
        article.className = 'course-card';
        article.setAttribute('data-id', course.id);
        article.setAttribute('tabindex', '0');
        
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
    
    const sumCredits = coursesList.reduce((sum, c) => sum + c.credits, 0);
    totalCreditsEl.textContent = `Total Credits Enrolled: ${sumCredits}`;
}

// 48. Call fetchAllCourses and render after delay
async function loadAndInitCourses() {
    try {
        coursesLoader.style.display = 'block';
        gridContainer.innerHTML = '';
        
        const data = await fetchAllCourses();
        currentCourses = [...data];
        
        coursesLoader.style.display = 'none';
        renderCourses(currentCourses);
    } catch (err) {
        coursesLoader.textContent = 'Failed to load courses.';
        console.error(err);
    }
}

loadAndInitCourses();

// Controls
searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const filtered = currentCourses.filter(course => 
        course.name.toLowerCase().includes(query) || 
        course.code.toLowerCase().includes(query)
    );
    renderCourses(filtered);
});

sortButton.addEventListener('click', () => {
    currentCourses.sort((a, b) => b.credits - a.credits);
    renderCourses(currentCourses);
    sortButton.textContent = 'Sorted by Credits';
    sortButton.classList.add('active-btn');
});

gridContainer.addEventListener('click', (e) => {
    const card = e.target.closest('.course-card');
    if (!card) return;
    const courseId = parseInt(card.getAttribute('data-id'), 10);
    const selectedCourse = currentCourses.find(c => c.id === courseId);
    if (selectedCourse) {
        selectedSection.classList.remove('hidden');
        selectedCardContent.innerHTML = `
            <div class="selected-details">
                <h4>${selectedCourse.name}</h4>
                <p><strong>Code:</strong> ${selectedCourse.code}</p>
                <p><strong>Credits:</strong> ${selectedCourse.credits}</p>
                <p><strong>Current Grade:</strong> ${selectedCourse.grade}</p>
                <button type="button" id="close-details-btn">Close Details</button>
            </div>
        `;
        document.getElementById('close-details-btn').addEventListener('click', () => {
            selectedSection.classList.add('hidden');
        });
    }
});


// --- Task 2: Fetch API with Error Handling (Notifications Section) ---
const notificationsContainer = document.getElementById('notifications');
const notificationsLoader = document.getElementById('notifications-loader');
const notificationsErrorContainer = document.getElementById('notifications-error');
const errorMessageEl = document.getElementById('error-message');
const retryBtn = document.getElementById('retry-btn');
const triggerErrorBtn = document.getElementById('trigger-error-btn');
const fetchUserPostsBtn = document.getElementById('fetch-user-posts-btn');

let lastFetchUrl = 'https://jsonplaceholder.typicode.com/posts?_limit=4';

// 50. Reusable apiFetch function (Fetch-based)
async function apiFetch(url) {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error(`HTTP Error! Status: ${response.status} (${response.statusText})`);
    }
    return await response.json();
}

// 56. Axios Rewrite of apiFetch
// 58. Axios Request Interceptor
axios.interceptors.request.use(config => {
    console.log(`[Axios Interceptor] API call started: ${config.url}`);
    return config;
}, error => {
    return Promise.reject(error);
});

async function apiFetchAxios(url, params = {}) {
    // Axios automatically parses JSON and throws on non-2xx responses
    const response = await axios.get(url, { params });
    return response.data;
}

// Rendering notifications in the UI
function renderNotifications(posts) {
    notificationsContainer.innerHTML = '';
    
    posts.forEach(post => {
        const card = document.createElement('div');
        card.className = 'notification-card';
        card.innerHTML = `
            <div class="notification-header">
                <span class="notification-badge">Alert</span>
                <span class="notification-id">ID: #${post.id}</span>
            </div>
            <h4>${post.title}</h4>
            <p>${post.body.slice(0, 120)}...</p>
        `;
        notificationsContainer.appendChild(card);
    });
}

// Main fetch logic
async function loadNotifications(url, useAxios = false, params = {}) {
    // Show spinner, hide grid/errors
    notificationsLoader.classList.remove('hidden');
    notificationsContainer.innerHTML = '';
    notificationsErrorContainer.classList.add('hidden');
    
    try {
        let posts;
        if (useAxios) {
            posts = await apiFetchAxios(url, params);
        } else {
            posts = await apiFetch(url);
        }
        
        // Render
        renderNotifications(posts.slice(0, 4)); // limit to 4 posts for UI neatness
    } catch (err) {
        // Show error UI with Retry button
        notificationsErrorContainer.classList.remove('hidden');
        errorMessageEl.textContent = `Error loading notifications: ${err.message}`;
        console.error("UI Error caught:", err);
    } finally {
        notificationsLoader.classList.add('hidden');
    }
}

// Initialize Notifications (using Fetch API by default)
loadNotifications(lastFetchUrl, false);

// 54. Retry Button
retryBtn.addEventListener('click', () => {
    loadNotifications(lastFetchUrl, lastFetchUrl.includes('axios') || lastFetchUrl.includes('userId'));
});

// 53. Simulate 404 error
triggerErrorBtn.addEventListener('click', () => {
    lastFetchUrl = 'https://jsonplaceholder.typicode.com/nonexistent';
    loadNotifications(lastFetchUrl, false);
});

// 57. Use axios.get with a params object to fetch posts of user 1
fetchUserPostsBtn.addEventListener('click', () => {
    lastFetchUrl = 'https://jsonplaceholder.typicode.com/posts';
    loadNotifications(lastFetchUrl, true, { userId: 1 });
});
