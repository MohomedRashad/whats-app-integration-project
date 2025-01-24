import React, { createContext, useContext, useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { loginUser } from './authService'; // Import the loginUser function from your service

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(Cookies.get('token') || null);
  const [loading, setLoading] = useState(false); // Loading state for login
  const [error, setError] = useState(null); // Error state for login

  // Sync token from cookie on component mount
  useEffect(() => {
    const cookieToken = Cookies.get('token');
    if (cookieToken) {
      setToken(cookieToken);
      console.log("Token synchronized from cookie:", cookieToken);
    }
  }, []);

  const login = async (username, password) => {
    setLoading(true);
    try {
      const data = await loginUser(username, password);
      setToken(data.access);
      Cookies.set('token', data.access, { expires: 1 });
      console.log("Token set in cookie during login:", data.access);
      setError(null); // Clear any previous errors
    } catch (err) {
      setError(err.message || "Login failed. Please try again.");
      console.error("Login Error:", err); // Log the error in the console for debugging
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    setToken(null);
    Cookies.remove('token');
  };

  return (
    <AuthContext.Provider value={{ token, login, logout, loading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
