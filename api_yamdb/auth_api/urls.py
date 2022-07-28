from django.urls import path
from auth_api.views import SignupView, GetAuthTokenView

app_name = 'auth_api'


urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('token/', GetAuthTokenView.as_view()),
]
