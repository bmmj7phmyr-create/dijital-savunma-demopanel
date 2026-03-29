from rest_framework import serializers
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    ad = serializers.CharField(source="full_name")
    telefon = serializers.CharField(source="phone")
    rol = serializers.CharField(source="role")

    class Meta:
        model = User
        fields = ["id", "username", "email", "ad", "telefon", "rol"]