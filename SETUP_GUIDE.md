SETUP AND INSTALLATION GUIDE

Prerequisites:
- Python 3.8 or higher
- MySQL Server running locally
- pip (Python package manager)

STEP 1: Create and Setup MySQL Database
1. Open MySQL Command Line Client or MySQL Workbench
2. Create a new database:
   CREATE DATABASE littlelemon;
3. Create a database user (optional but recommended):
   CREATE USER 'littlelemon_user'@'localhost' IDENTIFIED BY 'littlelemon_password';
   GRANT ALL PRIVILEGES ON littlelemon.* TO 'littlelemon_user'@'localhost';
   FLUSH PRIVILEGES;

STEP 2: Clone the Repository
git clone https://github.com/sazid324/little-lemon-web-application.git
cd little-lemon-web-application

STEP 3: Create and Activate Virtual Environment
# On Windows:
python -m venv env
env\Scripts\activate

# On macOS/Linux:
python3 -m venv env
source env/bin/activate

STEP 4: Install Required Packages
pip install -r requirements.txt

STEP 5: Update Database Configuration (if using different credentials)
Edit little_lemon/settings.py and update the DATABASES section:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'littlelemon',
        'USER': 'root',  # or 'littlelemon_user' if you created one
        'PASSWORD': 'password',  # or 'littlelemon_password' if you created one
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STEP 6: Run Migrations
python manage.py migrate

STEP 7: Create a Superuser (Admin Account)
python manage.py createsuperuser
# Follow the prompts to create an admin account

STEP 8: Run the Development Server
python manage.py runserver

The API will be available at: http://localhost:8000/api/
The Django Admin interface will be available at: http://localhost:8000/admin/

STEP 9: Run Tests
python manage.py test

TROUBLESHOOTING:

1. MySQL Connection Error:
   - Make sure MySQL Server is running
   - Check your database credentials in settings.py
   - Verify the database exists

2. Module Not Found Errors:
   - Make sure virtual environment is activated
   - Run: pip install -r requirements.txt

3. Migration Errors:
   - Delete any .pyc files in migrations folder
   - Run: python manage.py makemigrations
   - Run: python manage.py migrate

TESTING WITH INSOMNIA:

1. Start the server: python manage.py runserver
2. Open Insomnia REST Client
3. Create a POST request to: http://localhost:8000/api/auth/register/
4. Body (JSON):
   {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "first_name": "Test",
     "last_name": "User"
   }
5. Copy the token from the response
6. Use the token in future requests by adding this header:
   Authorization: Token {your_token_here}

7. Test other endpoints:
   - GET http://localhost:8000/api/menu/
   - GET http://localhost:8000/api/bookings/
   - POST http://localhost:8000/api/bookings/ (with booking data and token)
