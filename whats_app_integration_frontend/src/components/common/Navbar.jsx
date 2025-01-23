import React from 'react';
import { Link } from 'react-router-dom'; // Import the Link component

function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark flex-column vh-100 p-3" style={{ width: '250px' }}>
      <Link to="/" className="navbar-brand mb-4 text-center"> {/* Link for the brand */}
        <h4>Admin Panel</h4>
      </Link>
      <ul className="navbar-nav flex-column">
        <li className="nav-item">
          <Link className="nav-link text-white" to="/dashboard"> {/* Link to Dashboard */}
            Dashboard
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/chats"> {/* Link to Chats */}
            Chats
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/notifications"> {/* Link to Notifications */}
            Notifications
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/tickets"> {/* Link to Tickets */}
            Tickets
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/statistics"> {/* Link to Statistics */}
            Statistics
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/settings"> {/* Link to Settings */}
            Settings
          </Link>
        </li>
        <li className="nav-item">
          <Link className="nav-link text-white" to="/help"> {/* Link to Help */}
            Help
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;