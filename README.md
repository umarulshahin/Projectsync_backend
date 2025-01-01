Project Overview
This project is a Django-based backend API using Django Rest Framework (DRF), PostgreSQL, Simple JWT for authentication, and CORS management. 
It is divided into three primary apps: user, authentication, and admin. Each app has specific responsibilities based on its purpose:

Authentication App: Handles authentication purposes using Simple JWT.
User App: Manages project and task creation, management, and user permissions.
Admin App: Provides administrative functionalities, such as user management and access to user data from the user app.

Technologies Used:
  Python 3.x
  Django
  Django Rest Framework
  PostgreSQL
  Simple JWT for authentication
  CORS handling using django-cors-headers
  environ for environment variable management

Clone the project repository to your local machine:

Setp 1

git clone <repository-url>
cd <project-folder>


Step 2: Create and Activate Virtual Environment
Create a virtual environment for the project:

python -m venv venv

Activate the environment:

venv\Scripts\activate
For macOS/Linux:

Step 3: Install Requirements
Install the necessary dependencies from the requirements.txt file:

pip install -r requirements.txt

Step 4: Configure Environment Variables
Create a .env file in the root directory and configure it with the following values (adjust as necessary):

.env

SECRET_KEY=<your-secret-key>
DATABASE_URL=postgres://username:password@localhost:5432/dbname

Step 5: Apply Migrations
Run database migrations to set up the database schema:

python manage.py migrate

Step 6: Create Superuser (Optional)
If you'd like to create a superuser for the admin panel:

python manage.py createsuperuser

Step 7: Run the Development Server
Start the Django development server:

python manage.py runserver
The backend API should now be accessible at http://localhost:8000.
