import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CoursesPage from './pages/CoursesPage';
import ProfilePage from './pages/ProfilePage';
import CourseDetailPage from './pages/CourseDetailPage';
import './App.css';

export default function App() {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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
    }, []);

    return (
        <div className="app-container">
            <Header siteName="Student Portal" />
            
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route 
                        path="/courses" 
                        element={
                            <CoursesPage 
                                courses={courses} 
                                loading={loading} 
                                error={error} 
                            />
                        } 
                    />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route 
                        path="/courses/:courseId" 
                        element={<CourseDetailPage courses={courses} />} 
                    />
                </Routes>
            </main>

            <Footer />
        </div>
    );
}
