from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet
)
from .views import SignupView, GetAuthTokenView, UsersViewSet

app_name = 'api_auth'


router = SimpleRouter()
router.register(r'users', UsersViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', GetAuthTokenView.as_view()),
    path('', include(router.urls))
]
