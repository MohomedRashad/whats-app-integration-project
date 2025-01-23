import React from 'react';

function WelcomeSection({ name }) {
  return (
    <div className="mb-4">
      <h2 className="h5">Hello, {name}!</h2>
      <p>Welcome back! Here’s what’s happening today:</p>
    </div>
  );
}

export default WelcomeSection;