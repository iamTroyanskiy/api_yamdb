from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from api.filters import TitleFilter
from reviews.models import Category, Genre, Title, Review


from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAdminModeratorOwnerOrReadOnly
)
from .utils import send_email, get_confirmation_code
from .serializers import (
    CategorySerializers,
    GenreSerializers,
    TitlesReadSerializers,
    TitleWriteSerializers,
    CommentSerializer,
    ReviewSerializer,
    SignupSerializer,
    GetAuthTokenSerializer,
    UsersSerializer,
)


User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorOwnerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


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


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializers
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-id')
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesReadSerializers
        return TitleWriteSerializers
