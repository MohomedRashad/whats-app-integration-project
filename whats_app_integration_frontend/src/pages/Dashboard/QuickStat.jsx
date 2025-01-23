import React from 'react';

function QuickStat({ title, value }) {
  return (
    <div className="card text-center shadow-sm p-3">
      <h4>{title}</h4>
      <p className="display-6">{value}</p>
    </div>
  );
}

export default QuickStat;