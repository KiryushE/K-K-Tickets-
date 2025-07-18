from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.templatetags.static import static

from .forms import RegisterForm, LoginForm
from .models import Concert


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


