import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark flex-column vh-100 p-3" style={{ width: '250px' }}>
      <Link to="/" className="navbar-brand mb-4 text-center">
        <h4>Admin Panel</h4>
      </Link>
      <ul className="navbar-nav flex-column">
        <li className="nav-item">
          <Link className="nav-link text-white" to="/dashboard">Dashboard</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/chats">Chats</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/notifications">Notifications</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/tickets">Tickets</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/statistics">Statistics</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/settings">Settings</Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/help">Help</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
