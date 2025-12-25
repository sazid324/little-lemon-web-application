from datetime import date, time

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .models import Booking, Menu


class MenuViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)
        self.menu_item = Menu.objects.create(
            title="Pasta Carbonara", price=12.99, inventory=50
        )

    def test_menu_list_unauthenticated(self):
        response = self.client.get("/api/menu/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_menu_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/menu/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_menu_retrieve(self):
        response = self.client.get(f"/api/menu/{self.menu_item.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Pasta Carbonara")
        self.assertEqual(float(response.data["price"]), 12.99)

    def test_menu_create_unauthenticated(self):
        data = {"title": "Risotto", "price": 15.99, "inventory": 30}
        response = self.client.post("/api/menu/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_menu_create_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"title": "Risotto", "price": 15.99, "inventory": 30}
        response = self.client.post("/api/menu/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 2)

    def test_menu_update_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {"title": "Updated Pasta", "price": 14.99, "inventory": 40}
        response = self.client.put(
            f"/api/menu/{self.menu_item.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.menu_item.refresh_from_db()
        self.assertEqual(self.menu_item.title, "Updated Pasta")

    def test_menu_delete_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(f"/api/menu/{self.menu_item.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 0)


class BookingViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)
        self.booking = Booking.objects.create(
            user=self.user,
            name="John Doe",
            no_of_guests=4,
            booking_date=date(2025, 12, 26),
            booking_time=time(19, 00),
        )

    def test_booking_list_unauthenticated(self):
        response = self.client.get("/api/bookings/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_booking_list_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/bookings/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_booking_list_shows_only_user_bookings(self):
        other_booking = Booking.objects.create(
            user=self.other_user,
            name="Jane Doe",
            no_of_guests=2,
            booking_date=date(2025, 12, 27),
            booking_time=time(20, 00),
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get("/api/bookings/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = (
            response.data.get("results", response.data)
            if isinstance(response.data, dict)
            else response.data
        )
        booking_ids = [b["id"] for b in data]
        self.assertNotIn(other_booking.id, booking_ids)
        self.assertGreater(len(booking_ids), 0)

    def test_booking_retrieve(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.get(f"/api/bookings/{self.booking.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "John Doe")

    def test_booking_create_authenticated(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "name": "Jane Smith",
            "no_of_guests": 2,
            "booking_date": "2025-12-27",
            "booking_time": "20:00",
        }
        response = self.client.post("/api/bookings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 2)
        new_booking = Booking.objects.get(name="Jane Smith")
        self.assertEqual(new_booking.user, self.user)

    def test_booking_create_unauthenticated(self):
        data = {
            "name": "Jane Smith",
            "no_of_guests": 2,
            "booking_date": "2025-12-27",
            "booking_time": "20:00",
        }
        response = self.client.post("/api/bookings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_booking_update(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        data = {
            "name": "John Updated",
            "no_of_guests": 6,
            "booking_date": "2025-12-26",
            "booking_time": "19:00",
        }
        response = self.client.put(
            f"/api/bookings/{self.booking.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.no_of_guests, 6)

    def test_booking_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        response = self.client.delete(
            f"/api/bookings/{self.booking.id}/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_user_isolation(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.other_token.key)
        response = self.client.get(f"/api/bookings/{self.booking.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserRegistrationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_register(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "newuser@example.com",
        }
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_register_duplicate_username(self):
        User.objects.create_user(username="testuser", password="testpass123")
        data = {
            "username": "testuser",
            "password": "newpass123",
            "email": "different@example.com",
        }
        response = self.client.post("/api/auth/register/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        User.objects.create_user(username="testuser", password="testpass123")
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], "testuser")

    def test_user_login_invalid_credentials(self):
        User.objects.create_user(username="testuser", password="testpass123")
        data = {"username": "testuser", "password": "wrongpass"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login_nonexistent_user(self):
        data = {"username": "nonexistent", "password": "password"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_creation_on_register(self):
        data = {
            "username": "newuser",
            "password": "newpass123",
            "email": "newuser@example.com",
        }
        self.client.post("/api/auth/register/", data, format="json")
        user = User.objects.get(username="newuser")
        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_token_retrieval_on_login(self):
        user = User.objects.create_user(username="testuser", password="testpass123")
        Token.objects.create(user=user)
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post("/api/auth/login/", data, format="json")
        self.assertIn("token", response.data)
        self.assertEqual(response.data["token"], user.auth_token.key)
