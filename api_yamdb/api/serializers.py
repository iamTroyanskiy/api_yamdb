from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

from rest_framework.generics import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.Serializer):

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        min_length=2,
    )
    email = serializers.EmailField(required=True)

    def create(self, validated_data):
        try:
            instance, created = User.objects.get_or_create(**validated_data)
            return instance
        except IntegrityError as integrity_error:
            error_field = str(integrity_error)[37:]
            raise ValidationError(
                f'Пользователь с таким {error_field} уже существует'
            )

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
