<<<<<<< HEAD
from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet
from .views import SignupView, GetAuthTokenView, UsersViewSet

app_name = 'api_auth'

router = SimpleRouter()
router.register(r'users', UsersViewSet)
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', GetAuthTokenView.as_view()),
    path('', include(router.urls))
]
=======
from django.urls import path, include
from rest_framework import routers

from .views import (
    CommentViewSet,
    ReviewViewSet,

)

router_v1 = routers.DefaultRouter()
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews',
)
>>>>>>> b22e124 (Comment, Review)
