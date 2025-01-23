import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Chats from './pages/Chats';
import NotificationsPage from './pages/Notifications';
import Tickets from './pages/Tickets';
import Statistics from './pages/Statistics';
import Settings from './pages/Settings';
import Help from './pages/Help';
import { loginUser } from './services/authService';

function App() {
    const [token, setToken] = useState(localStorage.getItem('token') || null);

    const handleLogin = async (username, password) => {
        try {
            const data = await loginUser(username, password);
            setToken(data.access);
            localStorage.setItem('token', data.access);
        } catch (error) {
            alert(error.message);
            console.error('Login error:', error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
    };

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={token ? <Navigate to="/dashboard" /> : <div className="container vh-100 d-flex justify-content-center align-items-center"><Login onLogin={handleLogin} /></div>} />
          <Route path="/dashboard" element={token ? <Dashboard token={token} onLogout={handleLogout} /> : <Navigate to="/" />} />
          <Route path="/chats" element={<Chats />} />
          <Route path="/notifications" element={<NotificationsPage />} />
          <Route path="/tickets" element={<Tickets />} />
          <Route path="/statistics" element={<Statistics />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/help" element={<Help />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;