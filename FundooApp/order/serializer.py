from userlogin.serializers import UserSerializer
from bookstore.serializers import BookSerializer
from .models import Order
from bookstore.models import Book
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        return order
