from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.title


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateField()
    booking_time = models.TimeField()
    
    class Meta:
        ordering = ['booking_date', 'booking_time']
    
    def __str__(self):
        return f"{self.name} - {self.booking_date} at {self.booking_time}"
