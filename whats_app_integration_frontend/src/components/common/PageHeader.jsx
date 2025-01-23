import React from 'react';

function PageHeader({ title, onLogout }) {
  return (
    <div className="d-flex justify-content-between align-items-center mb-4">
      <h1 className="h4">{title}</h1>
      <button className="btn btn-primary" onClick={onLogout}>
        Logout
      </button>
    </div>
  );
}

export default PageHeader;