from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()
    date_created = models.DateField(auto_now_add=True)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    date_updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
