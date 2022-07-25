from rest_framework import serializers
from .models import Cart
from userlogin.serializers import UserSerializer
from bookstore.models import Book


class CartSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), many=False)

    class Meta:
        model = Cart
        fields = ('id', 'book', 'quantity')



