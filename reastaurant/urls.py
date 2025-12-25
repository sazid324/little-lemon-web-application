from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BookingView, MenuView, UserRegistrationView

router = DefaultRouter()
router.register(r"menu", MenuView, basename="menu")
router.register(r"bookings", BookingView, basename="booking")
router.register(r"auth", UserRegistrationView, basename="auth")

urlpatterns = [
    path(r"", include(router.urls)),
]
