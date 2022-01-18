# Import default modules
from django.contrib.auth import authenticate
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Import Serializer from api.serializers
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    SignInSerializer,
    SignOutSerializer,
)

# Import set_cookies from api.utils
from .utils import set_cookies, unset_cookies, get_access_token_response


# SignUpAPIView, used as_view for signup url,
class SignUpAPIView(generics.GenericAPIView):
    # SignUpSerializer class for serializering request
    serializer_class = SignUpSerializer

    # Post method,
    def post(self, request):
        # Check for access_token and return response
        response = get_access_token_response(request)

        # If request have access_token or refresh_token, return response
        if response is not None:
            return response

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
            },
            status=status.HTTP_201_CREATED,
        )


# SignInAPIView, used as_view for signin url,
class SignInAPIView(generics.GenericAPIView):
    # SignInSerializer class for serializering request
    serializer_class = SignInSerializer

    # POST method,
    def post(self, request):
        # Check for access_token and return response
        response = get_access_token_response(request)

        # If request have access_token or refresh_token, return response
        if response is not None:
            return response

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
                },
                status=status.HTTP_200_OK,
            )
            # Add tokens in cookies,
            set_cookies(response, refresh_token)
            return response

        # Return response with message "SignIn failed"
        return Response(
            {"message": "SignIn failed!"}, status=status.HTTP_204_NO_CONTENT
        )


# SignOutAPIView, used as_view for signout url,
class SignOutAPIView(generics.GenericAPIView):
    serializer_class = SignOutSerializer

    # Delete method,
    def delete(self, request):
        # Check for access_token and return response
        response = get_access_token_response(request)

        # If request have no access_token or refresh_token, return response
        if response is None:
            return Response(
                {"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create response with message "Successfully signout."
        response = Response(
            {"message": "Successfully signout."}, status=status.HTTP_200_OK
        )
        # Remove tokens from cookies
        unset_cookies(response)
        return response
