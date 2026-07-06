import axios from 'axios';

// Create a single Axios instance
const apiClient = axios.create({
    baseURL: 'https://jsonplaceholder.typicode.com',
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Request Interceptor: Attach mock auth token (Step 141)
apiClient.interceptors.request.use(
    (config) => {
        const mockToken = 'Bearer mock-token-xyz123';
        config.headers['Authorization'] = mockToken;
        console.log(`[Axios Request Interceptor] Attaching token to: ${config.url}`);
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response Interceptor: Standardize outputs and errors (Step 140)
apiClient.interceptors.use(
    (response) => {
        // (a) Return response.data directly so callers do not see the Axios envelope wrapper
        return response.data;
    },
    (error) => {
        // (b) Catch errors and throw standardized Error object with message and statusCode
        const message = error.response?.data?.message || error.message || 'An error occurred during the API call';
        const statusCode = error.response?.status || 500;
        
        const standardError = new Error(message);
        standardError.statusCode = statusCode;
        
        console.error(`[Axios Response Interceptor] Standardized Error: ${statusCode} - ${message}`);
        return Promise.reject(standardError);
    }
);

export default apiClient;
