# WhatsApp Messaging Integration for Customer Support
This repository demonstrates the integration of WhatsApp messaging into a customer support system. The application consists of:
*   **Backend:** A Django REST API handling messaging logic, data storage, and interactions with a simulated WhatsApp API.
*   **Frontend:** A React application providing an admin interface for customer support activities, including authentication and communication.
## Features
*   Simulates WhatsApp messaging using a mock API.
*   Exposes endpoints for sending and receiving messages.
*   Handles user authentication and message persistence.
*   Implements models and serializers for managing users, messages, and conversations.
*   Provides an admin interface for customer support agents.
*   Allows authentication and role-based access control.
*   Enables sending messages to customers through the backend.

## Project Setup
The first step, regardless of your chosen setup method, is to clone the repository:
```bash
git clone [https://github.com/MohomedRashad/whats-app-integration-project.git](https://github.com/MohomedRashad/whats-app-integration-project.git)
cd whats-app-integration-project
```
After cloning, you can choose one of the following setup methods:
1. Using Docker and Docker Compose (Recommended)
Docker Compose is the quickest and easiest way to get the project up and running. It manages the entire setup process, including building images, creating containers, and linking them together. This method is highly recommended as it handles dependencies and ensures a consistent environment.
2. Manual Setup (For Advanced Users)
The manual setup provides more control over the environment and is useful for development or debugging. However, it requires manually installing dependencies and configuring the backend and frontend separately.

### Setting up with docker and docker-compose
Before using Docker Compose, you'll need to have Docker installed on your system. You can download Docker from the official website: [https://www.docker.com/products/docker-desktop]
In addition to Docker, you'll also need Docker Compose installed. You can find installation instructions for Docker Compose here: [https://docs.docker.com/compose/install/]
Start the Services:
```bash
docker-compose up
```
This command builds the Docker images, creates and starts the containers, and configures them.
Access the Admin Interface
After starting the services, access the frontend at http://localhost:3000. You can log in with the default credentials:
• Username: admin
• Password: admin
Note: Docker Compose automatically handles database migrations and creates a superuser (admin/admin) for the backend API.

### Backend Setup (Django REST API)
To set up the backend for the project manually, follow these steps:
1.  **Navigate to the backend directory:
After cloning the repository, navigate to the backend directory where the Django project is located.
```bash
cd whats_app_integration_backend
```
2.  Create a Virtual Environment (Recommended):
It's recommended to create a virtual environment for managing dependencies. This isolates the project’s dependencies from your global Python environment. Create and activate the virtual environment following your system's instructions.
```bash
python -m venv venv
```
3. 
Activate the Virtual Environment:
The process for activating the virtual environment varies based on your operating system:
4.  **Install Dependencies
Inside the virtual environment, install the necessary Python packages. These packages are listed in the requirements.txt file and include everything needed to run the Django application.
```bash
pip install -r requirements.txt
```
5. Migrate the Database
After installing the dependencies, you’ll need to set up the database. This involves running database migrations, which will create the necessary tables and apply any schema changes.
```bash
python manage.py migrate
```
6. Admin Access:
Since user registration is not supported from the frontend at the moment, creating a superuser account manually will grant you access to the system.
```bash
python manage.py createsuperuser
```
This command will prompt you to enter the required information, such as the username, and password for the superuser account. Ensure that the credentials you choose are secure and memorable, as these will be used to access the admin interface.
Once the superuser is created, you can log in to the admin interface of the frontend using the credentials you provided during the superuser creation process. The frontend will be accessible at http://localhost:3000.
7.  **Run the Server:** Finally, start the backend development server using Django's management command.
The Django API should now be running at `http://127.0.0.1:8000/`.

### Frontend Setup (React Application)
Follow these steps to manually set up the React frontend for the project:
1.  Navigate to the Frontend Directory:
After cloning the repository, navigate to the frontend directory where the React project is located.
```bash
cd whats_app_integration_frontend
```
2.  Install Node.js and npm (If Not Installed):
If you don't have Node.js and npm (Node Package Manager) installed on your system, you'll need to install them. Visit the Node.js website and download the latest stable version for your operating system.
3.  Install Dependencies:
Inside the frontend directory, run the command to install all the necessary dependencies. This will download and install the packages listed in the package.json file, which are required for the React application to run.
```bash
npm install
```
4.  Configure API Endpoints (Optional):
If needed, configure the API endpoints in the frontend to point to the correct backend URL. This step may be necessary if you're using a custom backend URL or if the default configuration needs adjustments.
5.  Run the React Development Server:
After installing the dependencies, start the React development server. This will launch the frontend application, and it will be accessible at http://localhost:3000 in your browser.
```bash
npm start
```
6.  Access the Admin Interface:
Once the frontend is running, you can log in using the superuser credentials you created earlier. The admin interface should be available for you to interact with.
