# WhatsApp Messaging Integration for Customer Support System
This repository demonstrates the integration of WhatsApp messaging into a customer support system. The application consists of two components:
-   **Backend:** A Django REST API handling messaging logic, data storage, and interactions with a simulated WhatsApp API.
-  **Frontend:** A React application providing an admin interface for customer support activities, including authentication and communication.
## Features
-   Simulates WhatsApp messaging using a mock API.
-   Exposes endpoints for sending and receiving messages.
- Implements a mock webhook to simulate WhatsApp events, including message status updates and incoming WhatsApp messages.
-   Handles user authentication and message persistence.
-   Implements models and serializers for managing users, messages, and conversations.
-   Provides an admin interface for customer support agents.
-   Allows authentication and role-based access control.
-   Enables sending messages to customers through the backend.
##  Project Setup
The first step, regardless of your chosen setup method, is to clone the repository and move to the project directory:
```bash
git clone https://github.com/MohomedRashad/whats-app-integration-project.git
cd whats-app-integration-project
```
After cloning, you can choose one of the following setup methods:
1.  Using Docker and Docker Compose (Recommended)
Docker Compose is the quickest and easiest way to get the project up and running. It manages the entire setup process, including building images, creating containers, and linking them together. This method is highly recommended as it handles dependencies and ensures a consistent environment.
2.  Manual Setup (For Advanced Users)
The manual setup provides more control over the environment and is useful for development or debugging. However, it requires manually installing dependencies and configuring the backend and frontend separately.

###  Setting up with docker and docker-compose
1. Before using Docker Compose, you'll need to have Docker installed on your system. You can download Docker from the official website: [https://www.docker.com/products/docker-desktop]  
In addition to Docker, you'll also need Docker Compose installed. You can find installation instructions for Docker Compose here: [https://docs.docker.com/compose/install/]  
2. Once you have Docker Compose set up and your environment configured, you can start the services by running the following command:
```bash
docker-compose up --build
```
This command will build the Docker images, create the containers, and start the services.  
3. Create a Superuser
After the services are up and running, you’ll need to manually create a superuser to access the admin interface. You have two options for how to access the backend container:
####  Option 1: Use a Separate Terminal Window
1. 
Open a new terminal window and run the following command to access the backend container:
```bash
docker-compose exec backend /bin/bash
```
2.  
Once inside the container, create the superuser by running:
```bash
python manage.py createsuperuser
```
You will be prompted to enter the username, and password for the superuser. Follow the prompts to create the superuser account.
####  Option 2: Run Docker Compose in Detached Mode
1. 
Alternatively, you can run Docker Compose in detached mode, which will allow you to keep the backend container running in the background while you continue to use the same terminal window:
~~~bash
docker-compose up -d
```
2. 
Once the container is running in detached mode, you can follow the above steps to get into the container and create the superuser by running:
```bash
docker-compose exec backend /bin/bash
python manage.py createsuperuser
```
Again, you will be prompted to enter the username and password for the superuser. Complete the prompts to create the superuser.
3.  Access the Admin Interface
Once the superuser is created, you can access the admin interface at http://localhost:3000.
- Username: Your superuser username (e.g., admin)
- Password: Your superuser password (the one you entered during creation)  
Note: Docker Compose automatically handles database migrations and creates a superuser (admin/admin) for the backend API.

###  Manual Setup
For the manual setup, you will need to configure and run both the backend (Django REST API) and frontend (React) independently. This requires using two separate terminal windows to handle both services simultaneously.

####  Backend Setup (Django REST API)
To set up the backend for the project manually, follow these steps:
1.  Navigate to the backend directory:
```bash
cd whats_app_integration_backend
```
2.  Create a Virtual Environment (Recommended):
It's recommended to create a virtual environment for managing dependencies. This isolates the project’s dependencies from your global Python environment. Create and activate the virtual environment following the instructions for Windows.
```bash
python -m venv venv
```
3.  Activating the Virtual Environment (Windows)
After creating the virtual environment, you need to activate it. On Windows, you can do this by running the following command in the same terminal window where the virtual environment was created:
```bash
.\env\Scripts\activate
```
Once activated, you should see the virtual environment name (e.g., (env)) at the beginning of the command prompt. This indicates that the virtual environment is active, and any Python packages you install will be contained within it.  
4.  Install Dependencies
Inside the virtual environment, install the necessary Python packages. These packages are listed in the requirements.txt file and include everything needed to run the Django application.
```bash
pip install -r requirements.txt
```
5. Migrate the Database
After installing the dependencies, you’ll need to set up the database. Since the project uses SQLite, running the database migrations will create the necessary tables in the SQLite database file.
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
7.  Run the Server:
Finally, start the backend development server using Django's management command.
```bash
python manage.py runserver
```
The Django API should now be running at `http://127.0.0.1:8000/`.

#### Frontend Setup (React Application)
Follow these steps to manually set up the React frontend for the project:
1.  Navigate to the Frontend Directory:
After cloning the repository, navigate to the frontend directory where the React project is located. This should be run from the root directory of the cloned project:
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
The base URL of the Django server API endpoint has been hardcoded in the .env file located in the frontend directory. If you need to modify the backend URL, you can do so in one place by updating the .env file. This step is only necessary if you're using a custom backend URL or if the default configuration requires adjustments.
5.  Run the React Development Server:
After installing the dependencies, start the React development server. This will launch the frontend application, and it will be accessible at http://localhost:3000 in your browser.
```bash
npm start
```
6.  Access the Admin Interface:
Make sure the Django API server is running. Once the frontend is up and running, you can log in using the superuser credentials you created earlier. The admin interface should now be available for you to interact with.

##  Design Decisions
The design decisions in this technical assessment were made to focus on evaluating the integration of WhatsApp messaging within a customer support system. Due to the scope of the assessment, the backend was prioritized, while the frontend was simplified. The main objective was to simulate a WhatsApp messaging system using a mock API, as access to the real WhatsApp Cloud API wasn't feasible. The system was designed with scalability in mind, ensuring that future improvements and additional features could be added without major changes to the current setup.
###  Business Assumptions
This application is a Software-as-a-Service (SaaS) platform designed to integrate WhatsApp messaging for customer support systems. The following business assumptions were made to simplify the implementation:
- Single WhatsApp Business Number: For simplicity, the frontend is associated with a single WhatsApp Business number, which is hardcoded. This setup can be extended in future versions to support multiple numbers.
- Account Creation: The application does not support user registration. Instead, the super admin creates an account, sets the credentials, and associates it with a WhatsApp Business number. The super admin can then grant access to support agents who manage customer conversations and tickets.
- Mock WhatsApp API: A mock WhatsApp API is used because integrating the real WhatsApp Cloud API is not feasible for this demonstration. This mock API simulates the behavior of the real WhatsApp API, enabling realistic testing and illustration of message sending and receiving.
###  Technical Assumptions:
The following technical assumptions were made during the project to streamline the development process:
- Backend Focus: Heavy emphasis was placed on the backend development, specifically integrating and simulating the WhatsApp API. The main focus was to implement the vacant system.
- Mock Webhooks and API Documentation: Mock WhatsApp API webhooks and API documentation have been included to enhance the development process and provide a clear understanding of the system. The Postman collection, which contains all API endpoints and related information, has been exported and saved in the root folder of this repo for easy use. Importing the collection through the Postman app would be the fastest way to get the full idea about the API.
- Frontend Limitations: Although several backend features were implemented, not all frontend functionalities have been fully implemented due to time constraints and the focus on backend development. As a result, there are some issues in the frontend, and the code quality isn't as clean compared to the backend API implementation. The frontend was not prioritized in this phase, so it remains simplified for now.
- API Testing with Postman: The provided Postman collection allows you to test the API endpoints, with sample data included for easier testing and understanding of the system.
- Authentication and Authorization: The API has been integrated with proper authentication and authorization mechanisms for illustration purposes, utilizing the Django REST Simple JWT library. All endpoints are protected to ensure that only authenticated users can perform actions.
- Scalability and Future Improvements: The project structure has been designed with scalability in mind, allowing for future improvements both in the backend and frontend. The backend has been modularized to facilitate easy integration of additional features, while the frontend can be expanded and improved based on the needs of the application.
- Environment Configuration: Environmental variables have been configured to ensure that different deployment environments (e.g., development, staging, production) can be easily handled. These variables should be customized to fit specific deployment configurations.

##  Future Improvements
The Future Improvements section highlights potential features that could enhance the platform. These improvements focus on increasing flexibility, expanding functionalities, and providing better scalability. The goal is to allow the system to grow with user needs and integrate new capabilities. Some of these improvements include:
1. Customizable Admin Dashboard: Allow users to personalize the admin dashboard for their specific customer support needs, including custom reporting and workflow tools.
2. Multi-Agent Support: Enable multiple agents to handle messages from the same WhatsApp Business number, with features like agent routing and ticket priority assignment.
3. Platform Scalability: Integrate additional messaging services (e.g., SMS, Facebook Messenger, Telegram) to manage inquiries from multiple channels.
4. Automated Ticket Routing and AI Support: Use AI to automatically route tickets based on customer queries and agent expertise, with chatbots to handle FAQs.
5. Audit Trails and Compliance Features: Add audit trails for tracking agent activities to help meet compliance standards (e.g., GDPR, HIPAA).
6. Localization and Multilingual Support: Support multiple languages for businesses in different regions, including localized front-end interfaces and multi-language automated messages.
7. Pricing and Subscription Tiers: Implement a subscription model with multiple pricing tiers, offering advanced features for higher tiers and a free tier for smaller businesses.
8. Security and Data Privacy: Enhance security with data encryption, two-factor authentication, and compliance certifications like SOC 2.
9. Integrations with Customer Support Platforms: Integrate with platforms like Zendesk, Freshdesk, and ServiceNow to manage WhatsApp messages along with other channels.
10. Analytics and Reporting: Add advanced analytics and reporting tools to track KPIs like response times, customer satisfaction, and agent performance.