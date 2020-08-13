# Django-Authentication

Django-Authentication is a set of REST APIs based on Django that provides user authentication functionalities, including signup, signin, signout, and reset password. It also includes an API to list users based on the current user's group.

## Requirements

The following dependencies are required to run the Django-Authentication project:

- asgiref==3.2.10
- Django==3.1
- django-environ==0.4.5
- django-rest-framework==0.1.0
- django-rest-passwordreset==1.1.0
- djangorestframework==3.11.1
- djangorestframework-simplejwt==4.4.0
- psycopg2==2.8.5
- PyJWT==1.7.1
- pytz==2020.1
- sqlparse==0.3.1

## How to Run on Your System

Follow the steps below to run the Django-Authentication project on your system:

1. Create a virtual environment:

   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:

   - For Windows:

     ```
     .venv\Scripts\activate
     ```

   - For Linux/Mac:

     ```
     source .venv/bin/activate
     ```

3. Upgrade the pip tool:

   ```
   python -m pip install --upgrade pip
   ```

4. Install the project dependencies in the current virtual environment:

   ```
   pip install -r requirements.txt
   ```

5. Start the Django project:

   ```
   django-admin startproject django_auth
   ```

6. Create an app within the Django project:

   ```
   python manage.py startapp api
   ```

7. Apply the database migrations:

   ```
   python manage.py migrate
   ```

8. Run the Django development server:

   ```
   python manage.py runserver
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

## Endpoints

The following endpoints are available in the Django-Authentication project:

- `POST /api/signup`: Register a new user with the provided credentials. Required fields: `username` and `password`.

- `POST /api/signin`: Authenticate a user and obtain an access token. Required fields: `username` and `password`.

- `POST /api/signout`: Sign out the current user and invalidate the access token. Required fields: `refresh_token`.

- `POST /api/reset-password`: Reset the user's password by sending a password reset email. Required field: `email`.

- `GET /api/users`: List all users based on the current user's group. Requires authentication.

## Authentication

The Django-Authentication project uses JSON Web Tokens (JWT) for authentication. When a user signs in, an access token is generated and returned. This token should be included in the `Authorization` header of subsequent requests with the format: `Bearer <access_token>`.

## Contributing

Contributions to the Django-Authentication project are welcome! If you would like to contribute, please follow the guidelines outlined in the CONTRIBUTING.md file.

---

Feel free to modify and customize this README file based on your project's specific details and requirements.