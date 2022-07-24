from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ErrorDetail
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .exceptions import AlreadyExistException, AlreadyExistUserException
from .permissions import IsAdmin
from .serializers import SignupSerializer, GetAuthTokenSerializer, UsersSerializer
from .utils import send_email, get_confirmation_code

User = get_user_model()


class SignupView(APIView):

    permission_classes = [AllowAny, ]

    @staticmethod
    def is_existing_user(serializer):
        len_serializer_data = len(serializer.data)
        errors = serializer.errors
        codes = [error[0].code for error in errors.values()]
        return all(
            [code == 'unique' for code in codes]
        ) and len(codes) == len_serializer_data

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid()
        confirmation_code = get_confirmation_code()
        if serializer.errors:
            if self.is_existing_user(serializer):
                username = request.data['username']
                email = request.data['email']
                send_email(username, email, confirmation_code)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        serializer.save(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
        send_email(username, email, confirmation_code)
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


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = PageNumberPagination
    lookup_field = 'username'

    @action(
        methods=['get', 'patch', ],
        detail=False,
        url_path='me',
        permission_classes=[IsAuthenticated, ]
    )
    def user_get_his_account_data(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        data = request.data.copy()
        data.pop('role', None)
        serializer = self.get_serializer(
            user,
            data=data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

