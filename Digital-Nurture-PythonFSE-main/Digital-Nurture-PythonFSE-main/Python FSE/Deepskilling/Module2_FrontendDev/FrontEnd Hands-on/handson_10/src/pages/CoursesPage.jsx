import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import CourseCard from '../components/CourseCard';
import { 
    enroll, 
    selectCourses, 
    selectCoursesLoading, 
    selectCoursesError, 
    selectEnrolledCourses 
} from '../redux/enrollmentSlice';

export default function CoursesPage() {
    const [searchTerm, setSearchTerm] = useState('');
    const dispatch = useDispatch();
    const navigate = useNavigate();

    // 146. Use selectors instead of accessing store shape or receiving props directly
    const courses = useSelector(selectCourses);
    const loading = useSelector(selectCoursesLoading);
    const error = useSelector(selectCoursesError);
    const enrolledCourses = useSelector(selectEnrolledCourses);

    const handleEnroll = (course) => {
        dispatch(enroll(course));
        navigate('/profile');
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

            {loading && <div className="loading-state">Loading courses catalog...</div>}
            
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
