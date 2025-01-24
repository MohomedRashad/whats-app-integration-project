import axios from 'axios';

// Fetch all threads
export const fetchThreads = async (token) => {
    const baseURL = process.env.REACT_APP_API_BASE_URL;

    if (!token) {
        console.error('Token not found in the API call');
        throw new Error('Token not found');
    }

    try {
        const response = await axios.get(`${baseURL}threads/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        // Dump the entire error to the console
        console.error('Error fetching threads:', error.response || error);
        throw new Error('Could not fetch threads. Please try again later.');
    }
};

// Fetch messages for a specific thread
export const fetchMessages = async (token, thread) => {
    const baseURL = process.env.REACT_APP_API_BASE_URL;

    if (!token) {
        console.error('Token not found in the API call');
        throw new Error('Token not found');
    }

    try {
        const response = await axios.get(`${baseURL}threads/${thread.id}/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data.messages; // Return only the messages array
    } catch (error) {
        // Dump the entire error to the console
        console.error('Error fetching messages:', error.response || error);
        throw new Error('Could not fetch messages. Please try again later.');
    }
};
