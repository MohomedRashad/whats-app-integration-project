import axios from 'axios';

export const sendMessage = async (token, receiverNumber, content, messageType) => {
    const baseURL = process.env.REACT_APP_API_BASE_URL;
    console.log('Receiver Number:', receiverNumber);
    console.log('Message Content:', content);
    console.log('Message Type:', messageType);

    try {
        // Send POST request to API
        const response = await axios.post(`${baseURL}messages/`, 
        {
            receiver_number: receiverNumber,
            content: content,
            message_type: messageType,
        }, 
        {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        // Log the response data (new message or success status)
        console.log('Message sent:', JSON.stringify(response.data));
        return response.data; // Return the response or the new message object
    } catch (error) {
        // Dump the entire error to the console
        console.error('Error sending message:', error.response || error);
        throw new Error('Could not send message. Please try again later.');
    }
};
