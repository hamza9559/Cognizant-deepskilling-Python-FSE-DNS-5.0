import React from 'react';
import { Link } from 'react-router-dom';

export default function HomePage() {
    return (
        <div className="page home-page">
            <section className="hero-landing">
                <h1>Welcome to Student Portal</h1>
                <p>Your integrated digital workspace for academic success. Access your profile, browse available courses, register for subjects, and keep track of your grades in real time.</p>
                <div className="hero-actions">
                    <Link to="/courses" className="btn-primary">Browse Courses</Link>
                    <Link to="/profile" className="btn-secondary">View Profile</Link>
                </div>
            </section>

            <section className="portal-features">
                <h2>Portal Features</h2>
                <div className="features-grid">
                    <div className="feature-card">
                        <h3>Interactive Course Search</h3>
                        <p>Search, filter, and sort courses to build your custom schedule for the upcoming semester.</p>
                    </div>
                    <div className="feature-card">
                        <h3>State Management</h3>
                        <p>Powered by Redux Toolkit for seamless data flow across different views and pages.</p>
                    </div>
                    <div className="feature-card">
                        <h3>Dynamic Navigation</h3>
                        <p>Fast, client-side routing using React Router v6 for a fluid application experience.</p>
                    </div>
                </div>
            </section>
        </div>
    );
}
