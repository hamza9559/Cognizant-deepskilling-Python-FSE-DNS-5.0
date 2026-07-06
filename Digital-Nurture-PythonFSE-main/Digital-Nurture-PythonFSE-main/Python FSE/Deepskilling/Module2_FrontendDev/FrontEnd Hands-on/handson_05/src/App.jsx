import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';
import CourseCard from './components/CourseCard';
import StudentProfile from './components/StudentProfile';
import './App.css';

export default function App() {
    const [courses, setCourses] = useState([]);
    const [enrolledCourses, setEnrolledCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    // --- Task 3: useEffect Hook & Lifecycle ---
    
    // Fetch courses from JSONPlaceholder API on mount
    useEffect(() => {
        const fetchCoursesData = async () => {
            try {
                setLoading(true);
                const response = await fetch('https://jsonplaceholder.typicode.com/posts');
                if (!response.ok) {
                    throw new Error(`Failed to fetch courses (HTTP ${response.status})`);
                }
                const data = await response.json();
                
                // Map the first 5 posts to course-like objects
                const mappedCourses = data.slice(0, 5).map(post => ({
                    id: post.id,
                    name: post.title.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
                    code: `CS${100 + post.id * 5}`,
                    credits: (post.id % 2) + 3, // alternating 3 and 4 credits
                    grade: post.id % 3 === 0 ? 'A' : (post.id % 3 === 1 ? 'A-' : 'B+')
                }));
                
                setCourses(mappedCourses);
                setError(null);
            } catch (err) {
                console.error("API error:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchCoursesData();
    }, []); // Empty array runs once on mount

    // Log whenever the courses state changes
    useEffect(() => {
        if (courses.length > 0) {
            console.log('Courses updated:', courses);
        }
        
        /*
          CRITICAL COMMENT: Why the dependency array [courses] matters:
          - If the array contains [courses], React will run this effect ONLY when the reference/value of `courses` changes.
          - If the array is empty [], it would only run once on component mount, capturing the initial empty state.
          - If we omit the dependency array entirely, this effect would execute on EVERY render cycle (e.g. when typing in
            the search input or clicking Enroll, which triggers state updates). This wastes resources and can cause
            infinite rendering loops if the effect itself updates any state.
        */
    }, [courses]);

    // Handle course enrollment
    const handleEnroll = (course) => {
        if (!enrolledCourses.find(c => c.id === course.id)) {
            setEnrolledCourses(prev => [...prev, course]);
        }
    };

    // Filter courses based on search term
    const filteredCourses = courses.filter(course => 
        course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        course.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="app-container">
            <Header siteName="Student Portal" enrolledCount={enrolledCourses.length} />
            
            <main className="main-content">
                <section id="hero">
                    <h1>Manage Your Academic Journey</h1>
                    <p>Select your favorite courses, enroll instantly, and track your student profile dynamically.</p>
                </section>

                <div className="content-layout">
                    {/* Course Section */}
                    <section className="courses-section">
                        <div className="section-header">
                            <h2>Featured Courses</h2>
                            <input 
                                type="text" 
                                className="search-bar"
                                placeholder="Search courses by name or code..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>

                        {loading && <div className="loading-state">Loading courses...</div>}
                        
                        {error && (
                            <div className="error-state">
                                <p>Error loading courses: {error}</p>
                            </div>
                        )}

                        {!loading && !error && (
                            <div className="courses-grid">
                                {filteredCourses.length > 0 ? (
                                    filteredCourses.map(course => (
                                        <CourseCard 
                                            key={course.id} 
                                            {...course} 
                                            onEnroll={handleEnroll}
                                            isEnrolled={!!enrolledCourses.find(c => c.id === course.id)}
                                        />
                                    ))
                                ) : (
                                    <div className="no-results">No courses found matching "{searchTerm}"</div>
                                )}
                            </div>
                        )}
                    </section>

                    {/* Profile Section */}
                    <aside className="sidebar-section">
                        <StudentProfile />
                        
                        {/* Enrolled Courses Summary List */}
                        <div className="enrolled-summary">
                            <h3>My Enrolled Courses</h3>
                            {enrolledCourses.length > 0 ? (
                                <ul className="enrolled-list">
                                    {enrolledCourses.map(course => (
                                        <li key={course.id} className="enrolled-item">
                                            <span className="enrolled-code">{course.code}</span>
                                            <span className="enrolled-name">{course.name}</span>
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <p className="no-enrollments">No courses enrolled yet.</p>
                            )}
                        </div>
                    </aside>
                </div>
            </main>

            <Footer />
        </div>
    );
}
