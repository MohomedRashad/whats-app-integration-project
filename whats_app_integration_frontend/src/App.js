import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Chats from './pages/Chats';
import NotificationsPage from './pages/Notifications';
import Tickets from './pages/Tickets';
import Statistics from './pages/Statistics';
import Settings from './pages/Settings';
import Help from './pages/Help';
import { AuthProvider, useAuth } from './services/AuthContext'; // Import AuthContext

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            {/* Route for the login page */}
            <Route
              path="/"
              element={<LoginRoute />}
            />
            {/* Other routes */}
            <Route
              path="/dashboard"
              element={<AuthWrapper><Dashboard /></AuthWrapper>}
            />
            <Route
              path="/chats"
              element={<AuthWrapper><Chats /></AuthWrapper>}
            />
            <Route path="/notifications" element={<NotificationsPage />} />
            <Route path="/tickets" element={<Tickets />} />
            <Route path="/statistics" element={<Statistics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/help" element={<Help />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

// Special route to handle login display
const LoginRoute = () => {
  const { token } = useAuth();
  
  // If user is logged in, redirect to dashboard
  if (token) {
    return <Navigate to="/dashboard" />;
  }

  // If user is not logged in, display login page
  return (
    <div className="container vh-100 d-flex justify-content-center align-items-center">
      <Login />
    </div>
  );
};

const AuthWrapper = ({ children }) => {
  const { token } = useAuth();
  return token ? children : <Navigate to="/" />;
};

export default App;
