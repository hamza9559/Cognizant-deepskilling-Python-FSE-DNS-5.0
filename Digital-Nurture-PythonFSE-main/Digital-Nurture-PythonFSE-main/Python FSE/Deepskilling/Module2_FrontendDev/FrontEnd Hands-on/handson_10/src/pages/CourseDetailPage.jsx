import React from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useSelector, useDispatch } from 'react-redux';
import { enroll, selectCourses, selectEnrolledCourses } from '../redux/enrollmentSlice';

export default function CourseDetailPage() {
    const { courseId } = useParams();
    const navigate = useNavigate();
    const dispatch = useDispatch();

    // Consume state from selectors
    const courses = useSelector(selectCourses);
    const enrolledCourses = useSelector(selectEnrolledCourses);

    const course = courses.find(c => c.id === parseInt(courseId, 10));
    
    if (!course) {
        return (
            <div className="page error-page">
                <h2>Course Not Found</h2>
                <p>The course ID you requested does not exist or has been removed from the catalog.</p>
                <Link to="/courses" className="btn-primary">Back to Courses</Link>
            </div>
        );
    }

    const isEnrolled = !!enrolledCourses.find(c => c.id === course.id);

    const handleEnroll = () => {
        dispatch(enroll(course));
        navigate('/profile');
    };

    return (
        <div className="page course-detail-page">
            <div className="detail-card">
                <div className="detail-header">
                    <span class="detail-code">{course.code}</span>
                    <h2>{course.name}</h2>
                </div>
                
                <div className="detail-body">
                    <p className="detail-description">
                        This is a comprehensive, hands-on course designed to build deep technical foundations and skilling.
                        Over the course of the semester, you will work on projects, coding exercises, and exams aligned with
                        modern industry standards.
                    </p>
                    
                    <div className="detail-stats">
                        <div className="detail-stat">
                            <span className="stat-label">Credits</span>
                            <span className="stat-value">{course.credits}</span>
                        </div>
                        <div className="detail-stat">
                            <span className="stat-label">Grade Target</span>
                            <span className="stat-value">{course.grade}</span>
                        </div>
                        <div className="detail-stat">
                            <span className="stat-label">Format</span>
                            <span className="stat-value">Interactive</span>
                        </div>
                    </div>
                </div>

                <div className="detail-actions">
                    <Link to="/courses" className="btn-secondary">Back to Courses</Link>
                    <button 
                        type="button" 
                        className={`enroll-btn-detail ${isEnrolled ? 'enrolled' : ''}`}
                        onClick={handleEnroll}
                        disabled={isEnrolled}
                    >
                        {isEnrolled ? 'Already Enrolled' : 'Enroll in Course'}
                    </button>
                </div>
            </div>
        </div>
    );
}
