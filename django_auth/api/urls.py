# Import path function
from django.urls import path

# Import SignUpAPIView
from .views import SignUpAPIView, SignInAPIView


# Create urlpatterns
urlpatterns = [
    # path for auth/signup, response for signup with SignUpAPIView
    path("auth/signup", SignUpAPIView.as_view(), name="signup"),
    # path for auth/signin, response for signin with SignInAPIView
    path("auth/signin", SignInAPIView.as_view(), name="signin"),
]
