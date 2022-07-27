from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.generics import get_object_or_404
from rest_framework import serializers

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

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


class UsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]
