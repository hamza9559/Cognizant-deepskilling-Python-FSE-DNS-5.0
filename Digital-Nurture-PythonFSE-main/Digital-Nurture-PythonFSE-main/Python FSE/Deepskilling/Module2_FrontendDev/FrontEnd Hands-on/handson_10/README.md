# Hands-On 10: API Integration & Advanced State Management

This folder contains the final framework solution demonstrating **Centralized API Service Layers**, **Redux Async Thunks**, and **Global Error Boundaries** in React. It also serves as a comparative analysis of state management across React, Angular, and Vue.js.

---

## State Management Framework Comparison

| Metric / Aspect | React + Redux Toolkit (RTK) | Angular + NgRx | Vue.js 3 + Pinia |
| :--- | :--- | :--- | :--- |
| **Architectural Pattern** | Redux (Actions, Reducers, Store, Selectors, Middleware/Thunks). | Redux / Elm Architecture (Actions, Reducers, Effects, Selectors, Store). | Composition API / Reactive Store (Refs are State, Computeds are Getters, Functions are Actions). |
| **Boilerplate Code** | **Medium**: RTK greatly reduces standard Redux boilerplate via `createSlice` and `createAsyncThunk`, but slices and selectors are still required. | **High**: Strongly typed actions, reducers, selectors, and side-effect modules (Effects) require writing multiple files and extensive setup. | **Low**: Almost zero boilerplate. Defining a store is identical to writing a standard Vue Composition component. |
| **Reactivity Mechanism** | Virtual DOM diffing. Components trigger selector hooks (`useSelector`) and re-render when selected sub-state changes reference. | RxJS Observables. Push-based reactivity where templates subscribe to state changes (using the `async` pipe). | Vue Reactivity System. Tracked dynamically via JavaScript Proxies. State changes automatically trigger reactive updates in components. |
| **Learning Curve** | **Moderate**: Requires understanding immutable state patterns, action dispatching, and asynchronous middleware (thunks). | **Steep**: Requires a strong grasp of RxJS streams, operators, reactive dependency injection, and NgRx module setup. | **Gentle**: Extremely intuitive if you understand Vue 3's reactive primitives like `ref()` and `computed()`. |
| **Built-in / Dev Tools** | Excellent Redux DevTools extension for time-travel debugging, dispatch logging, and state inspection. | Excellent integration with Redux DevTools via NgRx DevTools Instrumentation. | Premium integration with the official Vue DevTools, providing Pinia timelines, state modifications, and action logs. |

### Key Architectural Differences

1. **Boilerplate and Structure**:
   - **React + Redux Toolkit** streamlines the setup by uniting actions and reducers in "Slices". Asynchronous calls are wrapped in Thunks.
   - **Angular + NgRx** isolates side-effects entirely into `Effects` classes which process actions and emit new actions using complex RxJS streams.
   - **Vue + Pinia** drops the concept of separate "mutations" or "actions" dispatchers; you mutate state directly in action functions and read them as simple values.

2. **Async Operations**:
   - **RTK** uses Thunks that resolve promises and dispatch actions at lifecycle points (pending, fulfilled, rejected).
   - **NgRx** relies on RxJS Observables to handle HTTP calls asynchronously using effects.
   - **Pinia** actions are standard async/await Javascript functions that mutate refs directly, without mapping wrappers.

---

## Technical Features Implemented in this Project

1. **Centralized API Service Layer (`src/api/`)**:
   - `apiClient.js` configures a reusable Axios instance with a `baseURL`, default headers, and a request timeout.
   - A request interceptor attaches a mock token (`Authorization: Bearer mock-token-xyz123`) to every request.
   - A response interceptor extracts response data directly (`response.data`) and catches non-2xx statuses, mapping them to a standardized Javascript `Error` object containing the `statusCode`.
   - `courseApi.js` exports semantic service functions (`getAllCourses`, `getCourseById`, `enrollStudent`).

2. **Async Redux Thunks (`src/redux/enrollmentSlice.js`)**:
   - `fetchAllCourses` thunk dispatches and manages lifecycle states (`pending`, `fulfilled`, and `rejected`).
   - Store selectors (`selectCourses`, `selectCoursesLoading`, `selectCoursesError`) isolate the state shape from UI components.

3. **Global Error Boundary (`src/components/ErrorBoundary.jsx`)**:
   - Wraps the application root to catch runtime JavaScript crashes in components, displaying an elegant fallback dashboard with error traces.

---

## Verification & Execution

### Run Locally
To verify this React SPA:
1. Make sure you have installed packages (`npm install`).
2. Run the production build command:
   ```bash
   npm run build
   ```
3. Run the Vite development server:
   ```bash
   npm run dev
   ```
