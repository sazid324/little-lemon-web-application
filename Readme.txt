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

TESTING:

Running Unit Tests:
1. Test Models:
   python manage.py test reastaurant.test_models

2. Test Views/API:
   python manage.py test reastaurant.test_views

3. Run All Tests:
   python manage.py test reastaurant

Running the Server:
   python manage.py runserver

Access the Application:
   - Homepage & API Tester: http://localhost:8000/
   - Django Admin: http://localhost:8000/admin/
   - Browsable API: http://localhost:8000/api/
