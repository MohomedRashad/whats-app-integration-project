import React, { useState } from 'react';
import { sendMessage } from '../../services/send_message'; // Assuming sendMessage is implemented
import Cookies from 'js-cookie';

function ChatWindow({ thread, messages, setMessages }) {
    const [message, setMessage] = useState('');  // Local state to store the message
    const [sending, setSending] = useState(false);  // To show loading state

    const handleMessageChange = (e) => {
        setMessage(e.target.value);  // Update the message as user types
    };

    const handleSendMessage = () => {
        const token = Cookies.get('token');
        if (token && message.trim()) {
            setSending(true);  // Set sending state to true (show loading indicator)
            sendMessage(token, thread.receiver_number, message, 'text')
                .then((newMessage) => {
                    setSending(false);  // Reset sending state
                    setMessage('');  // Clear input field
                    setMessages((prevMessages) => [...prevMessages, newMessage]); // Add new message
                })
                .catch((error) => {
                    setSending(false);
                    console.error('Error sending message:', error);
                });
        }
    };

    return (
        <div className="chat-window">
            <div className="chat-header">
                <h5>Chat with {thread.name}</h5>
            </div>
            <div className="messages" style={{ overflowY: 'auto', height: 'calc(100vh - 250px)' }}>
                {messages.length === 0 ? (
                    <div>No messages to display</div>
                ) : (
                    messages.map((msg) => (
                        <div key={msg.message_id} className={`message ${msg.sender_number === thread.sender_number ? 'sent' : 'received'}`}>
                            <div className="message-content">{msg.content}</div>
                            <small>{new Date(msg.timestamp).toLocaleTimeString()}</small>
                        </div>
                    ))
                )}
            </div>

            <div className="message-input">
                <input
                    type="text"
                    value={message}
                    onChange={handleMessageChange}
                    placeholder="Type a message"
                    disabled={sending}
                    style={{ width: '80%', padding: '10px' }}
                />
                <button
                    onClick={handleSendMessage}
                    disabled={sending || !message.trim()}  // Disable button if no message or sending in progress
                    style={{ padding: '10px', marginLeft: '10px' }}
                >
                    {sending ? 'Sending...' : 'Send'}
                </button>
            </div>
        </div>
    );
}

export default ChatWindow;
