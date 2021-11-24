# Import path function and django_rest_passwordreset module
import django_rest_passwordreset
from django.urls import path, include
# Import SignUpAPIView
from .views import SignUpAPIView, SignInAPIView, SignOutAPIView, UserViewAPIView


# Create urlpatterns
urlpatterns = [
    # path for auth/signup, response for signup with SignUpAPIView
    path("auth/signup", SignUpAPIView.as_view(), name="signup"),
    # path for auth/signin, response for signin with SignInAPIView
    path("auth/signin", SignInAPIView.as_view(), name="signin"),
    # path for auth/signout, response for signout with SignOutAPIView
    path("auth/signout", SignOutAPIView.as_view(), name="signout"),
    # path for password reset
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset'), name="password-reset"),
    # path for view users
    path("user/", UserViewAPIView.as_view(), name="view-user")
]
