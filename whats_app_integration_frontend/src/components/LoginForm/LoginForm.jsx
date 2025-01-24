import React, { useState } from 'react';
import { useAuth } from '../../services/AuthContext'; // Import the Auth context

function Login() {
  const { login, error, loading } = useAuth(); // Access login, error, and loading states from context
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login(username, password);
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={loading}>Login</button>
      </form>

      {/* Display error message if there's an error */}
      {error && <div className="error-message alert alert-danger">{error}</div>}

      {/* Optional: Show loading spinner or message */}
      {loading && <div>Loading...</div>}
    </div>
  );
}

export default Login;
