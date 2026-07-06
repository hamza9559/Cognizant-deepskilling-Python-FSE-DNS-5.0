import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import StudentProfile from '../components/StudentProfile';
import { unenroll } from '../redux/enrollmentSlice';

export default function ProfilePage() {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
    const dispatch = useDispatch();

    const handleRemove = (courseId) => {
        dispatch(unenroll(courseId));
    };

    return (
        <div className="page profile-page">
            <div className="profile-layout">
                <div className="profile-form-container">
                    <StudentProfile />
                </div>
                
                <div className="profile-enrollments-container">
                    <div className="enrolled-summary">
                        <h3>My Enrolled Courses</h3>
                        {enrolledCourses.length > 0 ? (
                            <ul className="enrolled-list">
                                {enrolledCourses.map(course => (
                                    <li key={course.id} className="enrolled-item-expanded">
                                        <div className="item-meta">
                                            <span className="enrolled-code">{course.code}</span>
                                            <span className="enrolled-name">{course.name}</span>
                                            <span className="enrolled-credits">({course.credits} Credits)</span>
                                        </div>
                                        <button 
                                            type="button" 
                                            className="remove-course-btn"
                                            onClick={() => handleRemove(course.id)}
                                        >
                                            Remove
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p className="no-enrollments">No courses enrolled yet. Browse courses to add them.</p>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}
