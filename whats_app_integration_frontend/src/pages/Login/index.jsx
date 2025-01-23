import React from 'react';
import LoginForm from '../../components/LoginForm/LoginForm';

function Login({ onLogin }) {
    const handleLoginSubmit = (username, password) => {
        onLogin(username, password);
    };

    return (
        <div className="container vh-100 d-flex justify-content-center align-items-center">
            <div className="card shadow-sm border-0">
                <div className="card-body p-4">
                    <div className="text-center mb-4">
                        <h4 className="text-primary">Admin Login</h4>
                    </div>
                    <LoginForm onSubmit={handleLoginSubmit} />
                    <div className="text-center mt-3">
                        <a href="#" className="text-decoration-none">
                            Forgot Password?
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Login;