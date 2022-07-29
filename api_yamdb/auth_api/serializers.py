from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework.generics import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Пользователь с таким email уже существует'
            )
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                'Пользователь с таким username уже существует'
            )
        instance, created = User.objects.get_or_create(
            username=username,
            email=email
        )
        return instance

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError(
                "Имя пользователя 'me' запрещено, используйте другое."
            )
        return username


class GetAuthTokenSerializer(serializers.Serializer):

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data):
        username = data.get('username')
        user = get_object_or_404(User, username=username)
        input_confirmation_code = data.get('confirmation_code')
        if input_confirmation_code != user.confirmation_code:
            raise serializers.ValidationError(
                'Введите корректный код подтверждения.'
            )
        return data
