from django.urls import path
from . import views

urlpatterns = [
    path('', views.hotel_search, name='hotel_search'),
    path('book/<int:room_id>/', views.book_room, name='book_room'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('review/<int:hotel_id>/', views.add_review, name='add_review'),
    path('register/', views.register, name='register'),
]