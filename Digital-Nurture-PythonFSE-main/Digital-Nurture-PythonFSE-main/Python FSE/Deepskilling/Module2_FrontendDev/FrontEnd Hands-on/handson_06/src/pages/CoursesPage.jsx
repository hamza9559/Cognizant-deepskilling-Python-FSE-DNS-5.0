import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import { enroll } from '../redux/enrollmentSlice';

export default function CoursesPage({ courses, loading, error }) {
    const [searchTerm, setSearchTerm] = useState('');
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleEnroll = (course) => {
        dispatch(enroll(course));
        navigate('/profile'); // Automatically navigate to profile page after enrolling
    };

    const filteredCourses = courses.filter(course => 
        course.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        course.code.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="page courses-page">
            <div className="section-header">
                <h2>Explore Courses</h2>
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
        </div>
    );
}
