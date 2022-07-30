# Import path function
from django.urls import path

# Import SignUpAPIView
from .views import SignUpAPIView


# Create urlpatterns
urlpatterns = [
    # path for auth/signup, response for signup with SignUpAPIView
    path("auth/signup", SignUpAPIView.as_view(), name="signup"),
]
