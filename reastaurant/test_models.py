from datetime import date, time
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Booking, Menu


class MenuModelTest(TestCase):
    def setUp(self):
        self.menu_item = Menu.objects.create(
            title="Pasta Carbonara", price=12.99, inventory=50
        )

    def test_menu_creation(self):
        self.assertEqual(self.menu_item.title, "Pasta Carbonara")
        self.assertEqual(self.menu_item.price, 12.99)
        self.assertEqual(self.menu_item.inventory, 50)

    def test_menu_str_representation(self):
        self.assertEqual(str(self.menu_item), "Pasta Carbonara")

    def test_menu_price_decimal_places(self):
        menu = Menu.objects.create(title="Grilled Fish", price=19.75, inventory=30)
        self.assertEqual(menu.price, 19.75)

    def test_menu_inventory_default(self):
        menu = Menu.objects.create(title="Salad", price=8.50)
        self.assertEqual(menu.inventory, 0)

    def test_menu_ordering(self):
        menu1 = Menu.objects.create(title="Item 1", price=10.00)
        menu2 = Menu.objects.create(title="Item 2", price=20.00)
        menus = list(Menu.objects.filter(id__in=[menu1.id, menu2.id]))
        self.assertEqual(menus[0].id, menu1.id)
        self.assertEqual(menus[1].id, menu2.id)

    def test_menu_update(self):
        self.menu_item.price = 14.99
        self.menu_item.save()
        updated_menu = Menu.objects.get(id=self.menu_item.id)
        self.assertEqual(updated_menu.price, Decimal("14.99"))

    def test_menu_delete(self):
        menu_id = self.menu_item.id
        self.menu_item.delete()
        self.assertFalse(Menu.objects.filter(id=menu_id).exists())


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.booking = Booking.objects.create(
            user=self.user,
            name="John Doe",
            no_of_guests=4,
            booking_date=date(2025, 12, 26),
            booking_time=time(19, 00),
        )

    def test_booking_creation(self):
        self.assertEqual(self.booking.name, "John Doe")
        self.assertEqual(self.booking.no_of_guests, 4)
        self.assertEqual(self.booking.user, self.user)

    def test_booking_str_representation(self):
        expected = "John Doe - 2025-12-26 at 19:00:00"
        self.assertEqual(str(self.booking), expected)

    def test_booking_user_relationship(self):
        self.assertEqual(self.booking.user.username, "testuser")

    def test_booking_cascade_delete(self):
        booking_id = self.booking.id
        self.user.delete()
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())

    def test_booking_date_and_time(self):
        self.assertEqual(self.booking.booking_date, date(2025, 12, 26))
        self.assertEqual(self.booking.booking_time, time(19, 00))

    def test_multiple_bookings_same_user(self):
        Booking.objects.create(
            user=self.user,
            name="Jane Doe",
            no_of_guests=2,
            booking_date=date(2025, 12, 27),
            booking_time=time(20, 00),
        )
        user_bookings = Booking.objects.filter(user=self.user)
        self.assertEqual(user_bookings.count(), 2)

    def test_booking_ordering(self):
        Booking.objects.create(
            user=self.user,
            name="Early Booking",
            no_of_guests=2,
            booking_date=date(2025, 12, 26),
            booking_time=time(18, 00),
        )
        Booking.objects.create(
            user=self.user,
            name="Late Booking",
            no_of_guests=2,
            booking_date=date(2025, 12, 26),
            booking_time=time(20, 00),
        )
        bookings = list(Booking.objects.all())
        # First should be the earliest
        self.assertEqual(bookings[0].booking_time, time(18, 00))

    def test_booking_update(self):
        self.booking.no_of_guests = 6
        self.booking.save()
        updated_booking = Booking.objects.get(id=self.booking.id)
        self.assertEqual(updated_booking.no_of_guests, 6)

    def test_booking_delete(self):
        booking_id = self.booking.id
        self.booking.delete()
        self.assertFalse(Booking.objects.filter(id=booking_id).exists())
