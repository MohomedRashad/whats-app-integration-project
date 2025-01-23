const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const loginUser = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/users/token/`, { // Use template literals
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData?.detail || errorData?.non_field_errors || "Login Failed"
      throw new Error(errorMessage);
    }

    const data = await response.json();
    return data; // Return the token
  } catch (error) {
    console.error("Login Error:", error);
    throw error; // Re-throw the error for the component to handle
  }
};

export { loginUser };