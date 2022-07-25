from django.db import models
from userlogin.models import User
from bookstore.models import Book


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    book = models.ForeignKey(Book, related_name='orders', on_delete=models.CASCADE, null=True, blank=True)
    address = models.TextField(max_length=500, null=False)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now=True)
    confirm_order = models.BooleanField(default=False)

    def __str__(self):
        return self.book.name
