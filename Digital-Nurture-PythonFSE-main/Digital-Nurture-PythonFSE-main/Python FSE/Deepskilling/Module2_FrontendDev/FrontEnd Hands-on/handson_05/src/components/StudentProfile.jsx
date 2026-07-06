import React, { useState } from 'react';

export default function StudentProfile() {
    const [profile, setProfile] = useState({
        name: 'Jane Doe',
        email: 'jane.doe@university.edu',
        semester: '6'
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`Profile Saved Successfully:\nName: ${profile.name}\nEmail: ${profile.email}\nSemester: ${profile.semester}`);
    };

    return (
        <div className="profile-section">
            <h3>Student Profile</h3>
            <form onSubmit={handleSubmit} className="profile-form">
                <div className="form-group">
                    <label htmlFor="profile-name">Full Name</label>
                    <input 
                        type="text" 
                        id="profile-name" 
                        name="name" 
                        value={profile.name} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="profile-email">Email Address</label>
                    <input 
                        type="email" 
                        id="profile-email" 
                        name="email" 
                        value={profile.email} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="profile-semester">Current Semester</label>
                    <input 
                        type="number" 
                        id="profile-semester" 
                        name="semester" 
                        min="1" 
                        max="8" 
                        value={profile.semester} 
                        onChange={handleChange} 
                        required 
                    />
                </div>
                <button type="submit" className="save-btn">Update Profile</button>
            </form>

            <div className="profile-preview">
                <h4>Live Preview</h4>
                <p><strong>Name:</strong> {profile.name}</p>
                <p><strong>Email:</strong> {profile.email}</p>
                <p><strong>Semester:</strong> Semester {profile.semester}</p>
            </div>
        </div>
    );
}
