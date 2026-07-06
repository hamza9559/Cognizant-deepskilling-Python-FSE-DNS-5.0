import apiClient from './apiClient';

export const getAllCourses = async () => {
    const posts = await apiClient.get('/posts');
    
    // Map the first 5 posts to course-like objects
    return posts.slice(0, 5).map(post => ({
        id: post.id,
        name: post.title.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
        code: `CS${100 + post.id * 5}`,
        credits: (post.id % 2) + 3, // alternating 3 and 4 credits
        grade: post.id % 3 === 0 ? 'A' : (post.id % 3 === 1 ? 'A-' : 'B+')
    }));
};

export const getCourseById = async (id) => {
    const post = await apiClient.get(`/posts/${id}`);
    
    return {
        id: post.id,
        name: post.title.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' '),
        code: `CS${100 + post.id * 5}`,
        credits: (post.id % 2) + 3,
        grade: post.id % 3 === 0 ? 'A' : (post.id % 3 === 1 ? 'A-' : 'B+')
    };
};

export const enrollStudent = async (studentId, courseId) => {
    // Mock student registration by making a post call
    return await apiClient.post('/posts', {
        studentId,
        courseId,
        enrolledAt: new Date().toISOString()
    });
};
