import React, { createContext, useState } from 'react';

// Define context
export const EnrollmentContext = createContext();

// Provider component
export function EnrollmentProvider({ children }) {
    const [enrolledCourses, setEnrolledCourses] = useState([]);

    const enrollCourse = (course) => {
        if (!enrolledCourses.find(c => c.id === course.id)) {
            setEnrolledCourses(prev => [...prev, course]);
        }
    };

    const unenrollCourse = (courseId) => {
        setEnrolledCourses(prev => prev.filter(c => c.id !== courseId));
    };

    return (
        <EnrollmentContext.Provider value={{ enrolledCourses, enrollCourse, unenrollCourse }}>
            {children}
        </EnrollmentContext.Provider>
    );
}
