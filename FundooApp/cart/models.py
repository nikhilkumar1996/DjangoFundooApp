from django.db import models
from userlogin.models import User
from bookstore.models import Book


class Cart(models.Model):
    user = models.ForeignKey(User, related_name='cart', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='cart', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def __str__(self):
        return self.book.name
