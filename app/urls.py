from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import MenuViewSet, BookingViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'bookings', BookingViewSet, basename='booking')
router.register(r'auth', UserRegistrationViewSet, basename='auth')

urlpatterns = [
    path(r"", include(router.urls)),
]
