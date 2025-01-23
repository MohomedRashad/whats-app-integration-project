import React, { useState } from 'react';

function LoginForm({ onSubmit }) {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        onSubmit(username, password);
        setUsername('');
        setPassword('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="mb-3">
                <label htmlFor="username" className="form-label">
                    Username
                </label>
                <input
                    type="text"
                    id="username"
                    name="username"
                    className="form-control" // Bootstrap form control (Comment moved outside)
                    placeholder="Enter your username"
                    required
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>

            <div className="mb-3">
                <label htmlFor="password" className="form-label">
                    Password
                </label>
                <input
                    type="password"
                    id="password"
                    name="password"
                    className="form-control" // Bootstrap form control (Comment moved outside)
                    placeholder="Enter your password"
                    required
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>

            <div className="d-grid">
                <button type="submit" className="btn btn-primary">
                    Login
                </button>
            </div>
        </form>
    );
}

export default LoginForm;