from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    LOCATION_CHOICES = [
        ('Kochi', 'Kochi'),
        ('Munnar', 'Munnar'),
        ('Trivandrum', 'Trivandrum'),
        ('Alleppey', 'Alleppey'),
        ('Calicut', 'Calicut'),
    ]
    location = models.CharField(max_length=100, choices=LOCATION_CHOICES, default='Kochi')
    description = models.TextField()
    amenities = models.CharField(max_length=200)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    ROOM_TYPE_CHOICES = [
        ('Single Room', 'Single Room'),
        ('Double Room', 'Double Room'),
        ('Deluxe Room', 'Deluxe Room'),
        ('Executive Suite', 'Executive Suite'),
        ('Honeymoon Room', 'Honeymoon Room'),
    ]
    room_type = models.CharField(max_length=50, choices=ROOM_TYPE_CHOICES, default='Deluxe Room') # e.g., Deluxe, Suite
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.room_type}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)