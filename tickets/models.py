from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.templatetags.static import static


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError("У користувача повинен бути email")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email=email, name=name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Concert(models.Model):
    title = models.CharField(max_length=200)
    performer = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    image = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.title} — {self.date.strftime('%d.%m.%Y')}"

    @property
    def image_url(self):
        return static(f'img/{self.image}')


class Seat(models.Model):
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE, related_name='seats')
    row = models.IntegerField()
    seat_number = models.IntegerField()
    user = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return f"Ряд {self.row}, місце {self.seat_number} — {'Зайнято' if self.booked else 'Вільно'}"

