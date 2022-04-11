# Import default modules
from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Import Serializer from api.serializers
from .serializers import (UserSerializer, SignUpSerializer, SignInSerializer, SignOutSerializer)
# Import set_cookies from api.utils
from .utils import set_cookies, unset_cookies


# SignUpAPIView, used as_view for signup url,
class SignUpAPIView(generics.GenericAPIView):
    # SignUpSerializer class for serializering request
    serializer_class = SignUpSerializer

    # Post method,
    def post(self, request):
        # Serializer instance with data
        serializer = self.get_serializer(data=request.data)
        # Check validity of data, if it is not valid raise exceptions
        serializer.is_valid(raise_exception=True)

        # Save new user
        user = serializer.save()

        # Create response, message and user info
        return Response(
            {
                "message": "Successfully signed up.",
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


# SignInAPIView, used as_view for signin url,
class SignInAPIView(generics.GenericAPIView):
    # SignInSerializer class for serializering request
    serializer_class = SignInSerializer

    # POST method,
    def post(self, request):
        # Serializer instance with data
        serializer = self.get_serializer(data=request.data)
        # Check validity of data, if it is not valid raise exceptions
        serializer.is_valid(raise_exception=True)

        # User data (username, password)
        user = serializer.data
        # Authenticate User with username and password
        user = authenticate(
            request, username=user["username"], password=user["password"]
        )

        # If user is authenticated,
        if user:
            # Create refresh_token from user_id
            refresh_token = RefreshToken.for_user(user)

            # Create response, message and user info
            response = Response(
                {
                    "message": "Successfully signed-in.",
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                }
            )
            # Add tokens in cookies,
            set_cookies(response, refresh_token)
            return response

        # Return response with message "SignIn failed"
        return Response({"message": "SignIn failed!",})


# SignOutAPIView, used as_view for signout url,
class SignOutAPIView(generics.GenericAPIView):
    serializer_class = SignOutSerializer

    # Delete method,
    def delete(self, request):
        # Create response with message "Successfully signout."
        response = Response({"message":"Successfully signout."})
        # Remove cookies
        unset_cookies(response)
        return response
