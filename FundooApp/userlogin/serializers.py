from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
