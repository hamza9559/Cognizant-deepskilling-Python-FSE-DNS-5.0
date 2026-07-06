import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getAllCourses } from '../api/courseApi';

// --- Task 2: Advanced Redux Toolkit — Async Thunks ---

// 143. Create Async Thunk to fetch courses from API using centralized layer
export const fetchAllCourses = createAsyncThunk(
    'courses/fetchAll',
    async (_, { rejectWithValue }) => {
        try {
            return await getAllCourses();
        } catch (err) {
            // rejectWithValue extracts standardized error message thrown by interceptor
            return rejectWithValue(err.message || 'Failed to fetch courses');
        }
    }
);

const initialState = {
    courses: [],
    enrolledCourses: [],
    loading: false,
    error: null
};

const enrollmentSlice = createSlice({
    name: 'enrollment',
    initialState,
    reducers: {
        enroll: (state, action) => {
            const course = action.payload;
            if (!state.enrolledCourses.find(c => c.id === course.id)) {
                state.enrolledCourses.push(course);
            }
        },
        unenroll: (state, action) => {
            const courseId = action.payload;
            state.enrolledCourses = state.enrolledCourses.filter(c => c.id !== courseId);
        }
    },
    // 144. Handle the three thunk lifecycle actions
    extraReducers: (builder) => {
        builder
            .addCase(fetchAllCourses.pending, (state) => {
                state.loading = true;
                state.error = null;
            })
            .addCase(fetchAllCourses.fulfilled, (state, action) => {
                state.courses = action.payload;
                state.loading = false;
            })
            .addCase(fetchAllCourses.rejected, (state, action) => {
                state.error = action.payload;
                state.loading = false;
            });
    }
});

// 146. Add Selectors (components should not access store shape directly)
export const selectCourses = (state) => state.enrollment.courses;
export const selectCoursesLoading = (state) => state.enrollment.loading;
export const selectCoursesError = (state) => state.enrollment.error;
export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses;

export const { enroll, unenroll } = enrollmentSlice.actions;
export default enrollmentSlice.reducer;
