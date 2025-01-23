import React from 'react';

function RecentActivity() {
  return (
    <div className="card shadow-sm p-4 mb-4">
      <h4 className="h5">Recent Activity</h4>
      <ul className="list-group list-group-flush">
        <li className="list-group-item">Message sent to John Smith at 10:15 AM</li>
        <li className="list-group-item">New ticket created by Mary Johnson</li>
        <li className="list-group-item">Chat initiated with Alex Brown</li>
      </ul>
    </div>
  );
}

export default RecentActivity;