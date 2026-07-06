import React from 'react';

export default function Header({ siteName, enrolledCount }) {
    return (
        <header className="site-header">
            <div className="logo">
                <span>{siteName}</span>
            </div>
            <nav className="nav-menu">
                <ul>
                    <li><a href="#courses" className="active">Courses</a></li>
                    <li><a href="#profile">Profile</a></li>
                </ul>
            </nav>
            <div className="enrollment-badge">
                Enrolled Courses: <span className="badge-count">{enrolledCount}</span>
            </div>
        </header>
    );
}
