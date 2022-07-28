from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UsersViewSet

app_name = 'api_users'


router = SimpleRouter()
router.register(r'users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
