import React, { useState } from 'react';
import Cookies from 'js-cookie';
import axios from 'axios';

function NewChatModal({ closeModal, refreshThreads }) {
  const [receiverNumber, setReceiverNumber] = useState('');
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState(''); // Declare success message state

  const handleReceiverNumberChange = (e) => setReceiverNumber(e.target.value);
  const handleMessageChange = (e) => setMessage(e.target.value);

  // Function to send the message
  const handleSendMessage = async () => {
    const token = Cookies.get('token');

    if (!receiverNumber.trim() || !message.trim()) {
      setErrorMessage('Both receiver number and message are required!');
      return;
    }

    setSending(true); // Set sending state to true
    setErrorMessage(''); // Clear any previous error message
    setSuccessMessage(''); // Clear any previous success message

    const baseURL = process.env.REACT_APP_API_BASE_URL;

    try {
      // Send POST request to API
      const response = await axios.post(
        `${baseURL}messages/`, 
        {
          receiver_number: receiverNumber,
          content: message,
          message_type: 'text',
        },
        {
          headers: {
            Authorization: `Bearer ${token}`, // Add token to request headers
          },
        }
      );

      // Handle the success response
      const responseData = response.data;
      console.log('Message sent successfully:', responseData);
      setSuccessMessage('Message sent successfully!');
      setSending(false);
      setReceiverNumber('');
      setMessage('');
      refreshThreads(); // Refresh the list of threads/messages
      closeModal(); // Close the modal after sending the message
    } catch (error) {
      setSending(false);
      setErrorMessage('Error sending message. Please try again later.');
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="modal show" tabIndex="-1" style={{ display: 'block', backgroundColor: 'rgba(0, 0, 0, 0.5)' }}>
      <div className="modal-dialog">
        <div className="modal-content">
          <div className="modal-header">
            <h5 className="modal-title">Start New Chat</h5>
            <button type="button" className="btn-close" onClick={closeModal}></button>
          </div>
          <div className="modal-body">
            <div className="mb-3">
              <label htmlFor="receiverNumber" className="form-label">
                Receiver's Number
              </label>
              <input
                type="text"
                id="receiverNumber"
                className="form-control"
                value={receiverNumber}
                onChange={handleReceiverNumberChange}
                placeholder="Enter receiver's number"
              />
            </div>
            <div className="mb-3">
              <label htmlFor="message" className="form-label">
                Message
              </label>
              <textarea
                id="message"
                className="form-control"
                value={message}
                onChange={handleMessageChange}
                placeholder="Enter your message"
              ></textarea>
            </div>

            {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
            {successMessage && <div className="alert alert-success">{successMessage}</div>} {/* Display success message */}
          </div>
          <div className="modal-footer">
            <button type="button" className="btn btn-secondary" onClick={closeModal}>
              Close
            </button>
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleSendMessage}
              disabled={sending || !receiverNumber.trim() || !message.trim()}
            >
              {sending ? 'Sending...' : 'Send Message'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default NewChatModal;
