import React from 'react';

function ConversationItem({ thread, onClick, isSelected }) {
  return (
    <li
      className={`list-group-item ${isSelected ? 'bg-light' : ''}`} // Apply 'bg-light' if selected
      onClick={onClick}
      style={{ cursor: 'pointer' }}
    >
      <div>
        <strong>Chat with: </strong>
        {thread.receiver_number}
      </div>
      <small>
        <strong>Created At: </strong>
        {new Date(thread.created_at).toLocaleString()}
      </small>
      <br />
      <small>
        <strong>Last Accessed At: </strong>
        {new Date(thread.last_accessed_at).toLocaleString()}
      </small>
      <br />
      <small>
        <strong>Read: </strong>
        {thread.read ? 'Yes' : 'No'}
      </small>
    </li>
  );
}

export default React.memo(ConversationItem);
