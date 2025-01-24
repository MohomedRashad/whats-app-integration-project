import React, { useState, useEffect } from 'react';
import Cookies from 'js-cookie';
import { fetchThreads, fetchMessages } from '../../services/messages';
import ConversationList from '../../components/Chats/ConversationList';
import ChatWindow from '../../components/Chats/ChatWindow';
import Navbar from '../../components/common/Navbar';
import PageHeader from '../../components/common/PageHeader';
import Footer from '../../components/common/Footer';
import NewChatModal from '../../components/Chats/NewChatModal';

function Chats({ token, onLogout }) {
  const [threads, setThreads] = useState([]);
  const [selectedThread, setSelectedThread] = useState(null);
  const [error, setError] = useState(null);
  const [messages, setMessages] = useState([]);
  const [showModal, setShowModal] = useState(false); // State to control modal visibility

  useEffect(() => {
    const token = Cookies.get('token');
    if (token) {
      fetchThreads(token)
        .then((data) => {
          setThreads(data);
        })
        .catch((err) => setError(err.message));
    } else {
      setError('Token not found');
    }
  }, []);

  const handleThreadClick = (thread) => {
    setSelectedThread(thread);
    const token = Cookies.get('token');
    if (token) {
      fetchMessages(token, thread)
        .then((fetchedMessages) => {
          setMessages(fetchedMessages);
        })
        .catch((err) => setError(err.message));
    }
  };

  const handleNewChatClick = () => {
    setShowModal(true); // Show the modal when the button is clicked
  };

  // Function to refresh threads after sending a message
  const refreshThreads = () => {
    const token = Cookies.get('token');
    if (token) {
      fetchThreads(token)
        .then((data) => {
          setThreads(data);
          setSelectedThread(null); // Close the chat window by resetting the selected thread
        })
        .catch((err) => setError(err.message));
    } else {
      setError('Token not found');
    }
  };

  return (
    <div className="d-flex bg-light">
      <Navbar />
      <div className="container-fluid d-flex">
        <div className="flex-grow-2 p-4">
          <PageHeader title="Chat" onLogout={onLogout} />
        </div>

        <div
          className="bg-white border-end conversation-list"
          style={{ width: '30%', overflowY: 'auto', height: 'calc(100vh - 140px)' }}
        >
<div className="p-3 border-bottom">
                <button
                  className="btn btn-primary"
                  onClick={handleNewChatClick}
                >
                  Start New Chat
                </button>
                </div>
          {error ? (
            <div className="alert alert-danger" role="alert">
              {error}
            </div>
          ) : threads.length === 0 ? (
            <div className="d-flex align-items-center justify-content-center h-100">
              <div className="text-center">
                <h5>No chats available.</h5>
                <p>Click the new chat button to start a new chat.</p>
              </div>
            </div>
          ) : (
            <ConversationList
              threads={threads}
              onThreadClick={handleThreadClick}
            />
          )}
        </div>

        <div
          className="chat-window bg-light flex-grow-1"
          style={{ height: 'calc(100vh - 140px)', overflowY: 'auto' }}
        >
          {selectedThread ? (
            <ChatWindow thread={selectedThread} messages={messages} setMessages={setMessages} />
          ) : (
            <div className="d-flex align-items-center justify-content-center h-100">
              <h5>Select a conversation to view messages</h5>
            </div>
          )}
        </div>
      </div>
      <Footer />

      {/* Modal for new chat */}
      {showModal && (
        <NewChatModal
          closeModal={() => setShowModal(false)} // Close the modal
          refreshThreads={refreshThreads} // Pass refreshThreads function to modal
        />
      )}
    </div>
  );
}

export default Chats;
