import React, { Component } from 'react';

// --- Task 3: Global Error Handler ---
export default class ErrorBoundary extends Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error) {
        // Update state so the next render will show the fallback UI.
        return { hasError: true, error };
    }

    componentDidCatch(error, errorInfo) {
        // Log the error details to console
        console.error("[Global Error Boundary] Caught an unhandled exception:", error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            // Render beautiful error fallback screen
            return (
                <div className="error-boundary-container">
                    <div className="error-boundary-card">
                        <span className="error-icon">⚠️</span>
                        <h2>Application Error</h2>
                        <p>Something went wrong on our end. The global application error boundary captured an exception.</p>
                        <div className="error-trace-wrapper">
                            <pre className="error-trace">{this.state.error?.toString() || 'Unknown Javascript error'}</pre>
                        </div>
                        <button 
                            type="button" 
                            className="reload-btn"
                            onClick={() => window.location.reload()}
                        >
                            Reload Application
                        </button>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}
