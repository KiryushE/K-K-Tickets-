from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Concert

admin.site.register(Concert)
admin.site.register(User, UserAdmin)
