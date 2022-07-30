from django.urls import path
from api.views import SignupView, GetAuthTokenView

app_name = 'api'


urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('token/', GetAuthTokenView.as_view()),
]
