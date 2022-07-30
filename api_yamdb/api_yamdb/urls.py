from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
    path('api/v1/auth/', include('api.urls', namespace='api')),
    path('api/v1/', include('reviews.urls', namespace='api_reviews')),
    path('api/v1/', include('users.urls', namespace='api_users')),
]
