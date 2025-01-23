import React from 'react';

function QuickAction({ title, type = "primary", onClick }) {
    const buttonClassName = `btn btn-${type} w-100`;
  return (
    <div className="col-md-4">
      <button className={buttonClassName} onClick={onClick}>{title}</button>
    </div>
  );
}

export default QuickAction;