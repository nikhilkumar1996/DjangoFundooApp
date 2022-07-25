from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from datetime import date


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=254, unique=True)
    phone_no = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    password = models.TextField()
    is_active = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_no', 'password']

    def __str__(self):
        return "{}".format(self.email)

# class User(models.Model):
#     username = models.CharField(max_length=20, unique=True, blank=False)
#     firstname = models.TextField()
#     lastname = models.TextField()
#     email = models.EmailField()
#     phone_no = models.BigIntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
#     password = models.TextField()
#     is_active = models.BooleanField(default=False)
#
#     def __str__(self):
#         return self.username
