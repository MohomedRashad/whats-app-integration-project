import React from 'react';
import { useNavigate } from 'react-router-dom';  // Import useNavigate hook
import { useAuth } from '../../services/AuthContext'; // Import useAuth hook

const PageHeader = ({ title }) => {
  const { logout } = useAuth(); // Get logout function from AuthContext
  const navigate = useNavigate(); // Initialize the navigate function

  const handleLogout = () => {
    console.log('Logout button clicked');
    logout(); // Call the logout function
    navigate('/'); // Redirect to the login page
  };

  return (
    <div className="page-header d-flex justify-content-between align-items-center">
      <h1>{title}</h1>
      <button onClick={handleLogout} className="btn btn-danger">Logout</button>
    </div>
  );
};

export default PageHeader;
