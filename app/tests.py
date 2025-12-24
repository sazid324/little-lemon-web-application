from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Menu, Booking
from datetime import date, time


class MenuAPITestCase(TestCase):
    """Test cases for Menu API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        
        # Create test menu items
        self.menu1 = Menu.objects.create(
            title='Burger',
            price=9.99,
            inventory=50
        )
        self.menu2 = Menu.objects.create(
            title='Pizza',
            price=12.99,
            inventory=30
        )
    
    def test_get_menu_list(self):
        """Test retrieving menu items list"""
        response = self.client.get('/api/menu/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_get_menu_item_detail(self):
        """Test retrieving a single menu item"""
        response = self.client.get(f'/api/menu/{self.menu1.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Burger')
        self.assertEqual(response.data['price'], '9.99')
    
    def test_create_menu_item_authenticated(self):
        """Test creating a menu item with authentication"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'title': 'Pasta',
            'price': 11.99,
            'inventory': 20
        }
        response = self.client.post('/api/menu/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Pasta')
    
    def test_create_menu_item_unauthenticated(self):
        """Test creating a menu item without authentication"""
        data = {
            'title': 'Salad',
            'price': 8.99,
            'inventory': 40
        }
        response = self.client.post('/api/menu/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_menu_item(self):
        """Test updating a menu item"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'title': 'Burger Updated',
            'price': 10.99,
            'inventory': 45
        }
        response = self.client.put(f'/api/menu/{self.menu1.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Burger Updated')
    
    def test_delete_menu_item(self):
        """Test deleting a menu item"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(f'/api/menu/{self.menu1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Menu.objects.filter(id=self.menu1.id).exists())


class BookingAPITestCase(TestCase):
    """Test cases for Booking API"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='other@example.com'
        )
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        
        # Create test booking
        self.booking = Booking.objects.create(
            user=self.user,
            name='John Doe',
            no_of_guests=4,
            booking_date=date(2025, 12, 31),
            booking_time=time(19, 30)
        )
    
    def test_get_booking_list_authenticated(self):
        """Test retrieving user's bookings"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_booking_list_unauthenticated(self):
        """Test that unauthenticated users cannot access bookings"""
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_booking(self):
        """Test creating a booking"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'name': 'Jane Smith',
            'no_of_guests': 2,
            'booking_date': '2025-12-30',
            'booking_time': '18:30'
        }
        response = self.client.post('/api/bookings/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Jane Smith')
        self.assertEqual(response.data['user'], self.user.id)
    
    def test_user_can_only_see_own_bookings(self):
        """Test that users only see their own bookings"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.other_token.key}')
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_update_booking(self):
        """Test updating a booking"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        data = {
            'name': 'John Doe Updated',
            'no_of_guests': 6,
            'booking_date': '2025-12-31',
            'booking_time': '20:00'
        }
        response = self.client.put(f'/api/bookings/{self.booking.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'John Doe Updated')
    
    def test_delete_booking(self):
        """Test deleting a booking"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.delete(f'/api/bookings/{self.booking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())


class UserAuthenticationTestCase(TestCase):
    """Test cases for User Registration and Authentication"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password': 'newpass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_user_login(self):
        """Test user login"""
        # First create a user
        User.objects.create_user(
            username='loginuser',
            password='loginpass123',
            email='login@example.com'
        )
        
        # Then try to login
        data = {
            'username': 'loginuser',
            'password': 'loginpass123'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

