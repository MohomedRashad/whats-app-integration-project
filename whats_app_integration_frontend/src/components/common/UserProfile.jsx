import React from 'react';

function UserProfile() {
  return (
    <div className="card shadow-sm p-4 mb-4">
      <div className="d-flex align-items-center">
        <img src="https://via.placeholder.com/50" alt="Profile" className="rounded-circle me-3" />
        <div>
          <h5 className="mb-0">John Doe</h5>
          <p className="text-muted">Admin</p>
        </div>
      </div>
    </div>
  );
}

export default UserProfile;