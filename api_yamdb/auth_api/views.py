from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.utils import send_email, get_confirmation_code
from .serializers import (
    SignupSerializer,
    GetAuthTokenSerializer,
)

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = get_confirmation_code()
        user = serializer.save()
        send_email(user.username, user.email, confirmation_code)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class GetAuthTokenView(APIView):

    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = GetAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        jwt_token = RefreshToken.for_user(user).access_token
        return Response(
            {'token': str(jwt_token)},
            status=status.HTTP_200_OK
        )
