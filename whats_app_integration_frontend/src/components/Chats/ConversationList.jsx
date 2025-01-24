import React from 'react';
import ConversationItem from './ConversationItem';

function ConversationList({ threads, onThreadClick, selectedThreadId }) {
  return (
    <div className="conversation-list">
      {threads.map((thread) => (
        <ConversationItem
          key={thread.id}
          thread={thread}
          isSelected={thread.id === selectedThreadId} // Pass isSelected to style the selected thread
          onClick={() => onThreadClick(thread)}
        />
      ))}
    </div>
  );
}

export default ConversationList;
