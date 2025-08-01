import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from .forms import RegisterForm, LoginForm
from .models import Concert, Booking
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('concert_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('concert_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def concert_list(request):
    concerts = Concert.objects.order_by('date')
    for concert in concerts:
        print(f'{concert.title} — {concert.image_url}')
    return render(request, 'concert_list.html', {'concerts': concerts})


def concert_detail(request, concert_id):
    concert = get_object_or_404(Concert, pk=concert_id)
    return render(request, 'concert_detail.html', {'concert': concert})


@login_required
def booking_view(request, concert_id):
    concert = get_object_or_404(Concert, id=concert_id)
    user = request.user
    bookings = Booking.objects.filter(concert=concert)
    taken_seats = [f"{b.row}-{b.seat}" for b in bookings]
    user_seats = [f"{b.row}-{b.seat}" for b in bookings if b.user == user]

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        print("🔥 Отримані місця из формы (POST, без JS):", selected_seats)
        if not selected_seats:
            messages.error(request, "Оберіть хоча б одне місце!")
            return redirect('booking', concert_id=concert.id)
        for seat_id in selected_seats:
            try:
                row_str, seat_str = seat_id.split('-')
                row = int(row_str)
                seat_num = int(seat_str)
                print(f"👉 Опрацьовуємо місце: row={row}, seat={seat_num}")
            except (ValueError, IndexError):
                messages.error(request, f"Некорректний формат місця: {seat_id}")
                continue
            already_taken = Booking.objects.filter(concert=concert, row=row, seat=seat_num).exists()
            print(f"🔎 Чи зайнято {seat_id}? {'Так' if already_taken else 'Ні'}")

            if already_taken:
                messages.warning(request, f"Місце {row + 1}-{seat_num + 1} вже занято.")
            else:
                Booking.objects.create(user=user, concert=concert, row=row, seat=seat_num)
                print(f"✅ Заброньоване місце: {row}-{seat_num}")
                messages.success(request, f"Місце {row + 1}-{seat_num + 1} успішно заброньовано.")
        return redirect('booking', concert_id=concert.id)
    context = {
        'concert': concert,
        'rows': list(range(5)),
        'seats': list(range(10)),
        'taken_seats': taken_seats,
        'user_seats': user_seats,
    }

    return render(request, 'booking.html', context)


@login_required
def profile_view(request):
    user_bookings = Booking.objects.filter(user=request.user).select_related('concert').order_by('concert__date')
    bookings_by_concert = {}
    for booking in user_bookings:
        concert_id = booking.concert.id
        if concert_id not in bookings_by_concert:
            bookings_by_concert[concert_id] = {
                'concert': booking.concert,
                'seats': []
            }
        bookings_by_concert[concert_id]['seats'].append(f"Ряд {booking.row + 1}, місце {booking.seat + 1}")
    context = {
        'bookings_by_concert': bookings_by_concert.values()
    }
    return render(request, 'profile.html', context)