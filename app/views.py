from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer, UserSerializer, UserRegistrationSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """
    API endpoint for menu items.
    Allows users to view and create menu items.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for table bookings.
    Only authenticated users can create and manage bookings.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own bookings
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Automatically assign the current user
        serializer.save(user=self.request.user)


class UserRegistrationViewSet(viewsets.ViewSet):
    """
    API endpoint for user registration.
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

