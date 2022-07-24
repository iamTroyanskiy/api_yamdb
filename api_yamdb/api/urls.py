from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import SignupView, GetAuthTokenView, UsersViewSet

app_name = 'api_auth'

router = SimpleRouter()
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('auth/signup/', SignupView.as_view()),
    path('auth/token/', GetAuthTokenView.as_view()),
    path('', include(router.urls))
]
