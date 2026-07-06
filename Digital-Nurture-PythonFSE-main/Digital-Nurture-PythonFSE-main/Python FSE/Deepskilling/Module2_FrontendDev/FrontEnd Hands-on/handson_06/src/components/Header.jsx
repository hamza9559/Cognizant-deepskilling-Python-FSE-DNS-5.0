import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useSelector } from 'react-redux';

export default function Header({ siteName = "Student Portal" }) {
    const enrolledCourses = useSelector(state => state.enrollment.enrolledCourses);
    const location = useLocation();

    return (
        <header className="site-header">
            <div className="logo">
                <Link to="/" style={{ textDecoration: 'none', color: '#ffffff' }}>
                    <span>{siteName}</span>
                </Link>
            </div>
            <nav className="nav-menu">
                <ul>
                    <li>
                        <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Home</Link>
                    </li>
                    <li>
                        <Link to="/courses" className={location.pathname.startsWith('/courses') ? 'active' : ''}>Courses</Link>
                    </li>
                    <li>
                        <Link to="/profile" className={location.pathname === '/profile' ? 'active' : ''}>Profile</Link>
                    </li>
                </ul>
            </nav>
            <div className="enrollment-badge">
                Enrolled: <span className="badge-count">{enrolledCourses.length}</span>
            </div>
        </header>
    );
}
