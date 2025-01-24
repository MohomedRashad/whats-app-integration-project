const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const loginUser = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}users/token/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    // Log the status code and the response body if it's OK
    if (!response.ok) {
      const errorData = await response.json();
      console.error("Error Data:", errorData);  // Log the error data
      const errorMessage = errorData?.detail || errorData?.non_field_errors || "Login Failed";
      throw new Error(errorMessage);
    }

    // Log the successful response JSON
    const data = await response.json();
    console.log("Response Data:", data);  // Log the successful response
    return data; // Return the token
  } catch (error) {
    console.error("Login Error:", error);
    throw error; // Re-throw the error for the component to handle
  }
};

export { loginUser };
