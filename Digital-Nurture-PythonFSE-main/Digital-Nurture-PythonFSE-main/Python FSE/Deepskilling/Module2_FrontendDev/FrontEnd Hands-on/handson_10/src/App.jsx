import React, { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import Header from './components/Header';
import Footer from './components/Footer';
import HomePage from './pages/HomePage';
import CoursesPage from './pages/CoursesPage';
import ProfilePage from './pages/ProfilePage';
import CourseDetailPage from './pages/CourseDetailPage';
import { fetchAllCourses } from './redux/enrollmentSlice';
import './App.css';

export default function App() {
    const dispatch = useDispatch();

    // 145. Dispatch the thunk in useEffect on mount.
    // This loads the courses into global state once and keeps components decoupled from fetch commands.
    useEffect(() => {
        dispatch(fetchAllCourses());
    }, [dispatch]);

    return (
        <div className="app-container">
            <Header siteName="Student Portal" />
            
            <main className="main-content">
                <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/courses" element={<CoursesPage />} />
                    <Route path="/profile" element={<ProfilePage />} />
                    <Route path="/courses/:courseId" element={<CourseDetailPage />} />
                </Routes>
            </main>

            <Footer />
        </div>
    );
}
