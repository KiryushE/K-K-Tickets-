from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.concert_list, name='concert_list'),
    path('concert/<int:concert_id>/', views.concert_detail, name='concert_detail'),
    path('concert/<int:concert_id>/booking/', views.booking_view, name='booking'),
    path('profile/', views.profile_view, name='profile'),
]
