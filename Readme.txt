Little Lemon Restaurant API - Backend Capstone Project

This is a Django REST Framework API for managing table bookings and menu items for the Little Lemon restaurant.

FEATURES:
- User Registration and Authentication using Token-based authentication
- Menu API for browsing restaurant items
- Table Booking API for managing reservations
- User-specific booking management
- MySQL database integration

API ENDPOINTS:

User Registration and Authentication:
- POST /api/auth/register/ - Register a new user
  Required fields: username, email, password, first_name, last_name
  
- POST /api/auth/login/ - Login and get authentication token
  Required fields: username, password

Menu API:
- GET /api/menu/ - Get all menu items (no authentication required)
- GET /api/menu/{id}/ - Get a specific menu item (no authentication required)
- POST /api/menu/ - Create a new menu item (authentication required)
- PUT /api/menu/{id}/ - Update a menu item (authentication required)
- DELETE /api/menu/{id}/ - Delete a menu item (authentication required)

Booking API:
- GET /api/bookings/ - Get all bookings for the current user (authentication required)
- GET /api/bookings/{id}/ - Get a specific booking (authentication required)
- POST /api/bookings/ - Create a new booking (authentication required)
  Required fields: name, no_of_guests, booking_date, booking_time
  
- PUT /api/bookings/{id}/ - Update a booking (authentication required)
- DELETE /api/bookings/{id}/ - Delete a booking (authentication required)

TESTING WITH INSOMNIA:

1. First, register a new user:
   POST /api/auth/register/
   Body: {
     "username": "testuser",
     "email": "test@example.com",
     "password": "testpass123",
     "first_name": "Test",
     "last_name": "User"
   }

2. Copy the token from the response

3. Use the token for authenticated requests:
   Header: Authorization: Token {your_token_here}

4. Test menu endpoints:
   - GET /api/menu/ (no auth needed)

5. Test booking endpoints:
   - GET /api/bookings/ (with token)
   - POST /api/bookings/
     Body: {
       "name": "John Doe",
       "no_of_guests": 4,
       "booking_date": "2025-12-31",
       "booking_time": "19:30"
     }

RUNNING TESTS:
python manage.py test

DATABASE CONFIGURATION:
By default, the application is configured to use MySQL with the following settings:
- Database name: littlelemon
- User: root
- Password: password
- Host: localhost
- Port: 3306

Make sure MySQL is running before starting the application.

STARTING THE SERVER:
python manage.py runserver

The API will be available at http://localhost:8000/api/
