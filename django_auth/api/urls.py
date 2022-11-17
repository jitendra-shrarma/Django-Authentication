from django.urls import path

from .views import SignUpAPIView


urlpatterns = [
    path('auth/signup', SignUpAPIView.as_view(), name='signup'),
]
