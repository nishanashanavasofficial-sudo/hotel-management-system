from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm  
from django.contrib.auth import login
from .models import Hotel, Room, Booking, Review
from django.contrib.auth.decorators import login_required
from datetime import datetime

def hotel_search(request):
    location = request.GET.get('location', '')
    max_price = request.GET.get('max_price', '')
    room_type = request.GET.get('room_type', '')
    facility = request.GET.get('facility', '')

    hotels = Hotel.objects.all()

    if location:
        hotels = hotels.filter(location__icontains=location)
    if facility:
        hotels = hotels.filter(amenities__icontains=facility)
    if max_price:
        hotels = hotels.filter(rooms__price_per_night__lte=max_price)
    if room_type:
        hotels = hotels.filter(rooms__room_type__icontains=room_type)

    hotels = hotels.distinct()

    context = {
        'hotels': hotels,
        'selected_location': location,
        'selected_price': max_price,
        'selected_room_type': room_type,
        'selected_facility': facility,
    }
    return render(request, 'core/search.html', context)

@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')
        
        # Calculate number of nights and total price
        d1 = datetime.strptime(check_in_str, "%Y-%m-%d")
        d2 = datetime.strptime(check_out_str, "%Y-%m-%d")
        nights = max((d2 - d1).days, 1)
        total_price = nights * float(room.price_per_night)

        booking = Booking.objects.create(
            user=request.user,
            room=room,
            check_in=check_in_str,
            check_out=check_out_str,
            total_price=total_price,
            is_paid=False
        )
        return redirect('payment', booking_id=booking.id)

    return render(request, 'core/book.html', {'room': room})

@login_required
def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.is_paid = True
        booking.save()
        
        # Mark room as unavailable after payment
        room = booking.room
        room.is_available = False
        room.save()
        
        return redirect('my_bookings')
    return render(request, 'core/payment.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'core/my_bookings.html', {'bookings': bookings})

@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            user=request.user,
            hotel=hotel,
            rating=rating,
            comment=comment
        )
        return redirect('hotel_search')
    return render(request, 'core/add_review.html', {'hotel': hotel})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically logs in the user after signing up
            return redirect('hotel_search')
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})