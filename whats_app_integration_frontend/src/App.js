import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Chats from './pages/Chats';
import NotificationsPage from './pages/Notifications';
import Tickets from './pages/Tickets';
import Statistics from './pages/Statistics';
import Settings from './pages/Settings';
import Help from './pages/Help';
import { loginUser } from './services/authService';
import Cookies from 'js-cookie';

function App() {
    // Read the token from cookies on initial load
    const [token, setToken] = useState(Cookies.get('token') || null);

    const handleLogin = async (username, password) => {
        try {
            const data = await loginUser(username, password);
            const token = data.access;
            setToken(token);
            // Store the token in an HttpOnly cookie
            Cookies.set('token', token, { expires: 1, secure: process.env.NODE_ENV === 'production' });
        } catch (error) {
            alert(error.message);
            console.log(error.message);
            console.error('Login error:', error);
        }
    };

    const handleLogout = () => {
        Cookies.remove('token'); // Remove the token from the cookies
        setToken(null);
    };

    // Check if token exists when rendering the routes
    useEffect(() => {
    }, [token]);

    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route
                        path="/"
                        element={
                            token ? (
                                <Navigate to="/dashboard" />
                            ) : (
                                <div className="container vh-100 d-flex justify-content-center align-items-center">
                                    <Login onLogin={handleLogin} />
                                </div>
                            )
                        }
                    />
                    <Route
                        path="/dashboard"
                        element={token ? <Dashboard token={token} onLogout={handleLogout} /> : <Navigate to="/" />}
                    />
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
