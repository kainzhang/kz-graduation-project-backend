from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff']
        extra_kwargs = {
            'username': {
                'min_length': 6,
                'max_length': 16
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20
            }
        }
