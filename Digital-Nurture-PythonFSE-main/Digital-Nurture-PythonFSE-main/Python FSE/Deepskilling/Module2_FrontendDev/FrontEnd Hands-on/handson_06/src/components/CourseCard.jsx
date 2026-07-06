import React from 'react';
import { Link } from 'react-router-dom';

export default function CourseCard({ id, name, code, credits, grade, onEnroll, isEnrolled }) {
    return (
        <article className="course-card">
            <div className="course-card-content">
                <Link to={`/courses/${id}`} className="course-title-link">
                    <h3>{name}</h3>
                </Link>
                <p>Gain advanced knowledge and core skills in this specialized subject area.</p>
                <div className="course-details">
                    <span className="course-code">{code}</span>
                    <span className="course-credits">Credits: {credits}</span>
                    <span className="course-grade">Grade Target: {grade}</span>
                </div>
            </div>
            <div className="course-card-actions">
                <Link to={`/courses/${id}`} className="view-details-link">View Details</Link>
                <button 
                    type="button" 
                    className={`enroll-btn-card ${isEnrolled ? 'enrolled' : ''}`}
                    onClick={() => !isEnrolled && onEnroll({ id, name, code, credits, grade })}
                    disabled={isEnrolled}
                >
                    {isEnrolled ? 'Enrolled' : 'Enroll'}
                </button>
            </div>
        </article>
    );
}
