# Import default modules
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Import Serializer from api.serializers
from .serializers import (
    UserSerializer,
    SignUpSerializer,
    SignInSerializer,
    EmptySerializer,
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
        if response:
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
        if response:
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
    serializer_class = EmptySerializer

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


# UserViewAPIView, used to render users info based on current_user group
class UserViewAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        # Check for refresh token
        response = get_access_token_response(request)
        # If user have no access_token or refresh_token, return "Invalid request" response
        if response is None:
            return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)

        # Get user instance from refresh token
        refresh_token = request.COOKIES.get('refresh_token', None)
        user_id = RefreshToken(refresh_token).payload['user_id']
        current_user = User.objects.get(pk=user_id)

        # User group based on permissions
        # user_queryset is retrive user_set based on group
        # message associated with current_user_group_name
        # status_message associated with current_user_group_name
        if current_user.has_perm('auth.view_user'):
            current_user_group_name = "Super-Admin"
            user_queryset = User.objects.all()
            message = f"Your {current_user_group_name} group has permissions to view all users."
            status_message = status.HTTP_200_OK
        elif current_user.has_perm('auth.view_student'):
            current_user_group_name = "Teacher"
            user_queryset = User.objects.filter(groups__name="Student")
            message = f"Your {current_user_group_name} group has permissions to view all students."
            status_message = status.HTTP_200_OK
        else:
            current_user_group_name = "Student"
            user_queryset = None
            message = f"Your {current_user_group_name} group has no permissions to view users."
            status_message = status.HTTP_400_BAD_REQUEST

        # serialize data
        serializer = self.get_serializer(data=user_queryset, many=True)
        serializer.is_valid()

        # if user_group is "student", return empty list of users
        if current_user_group_name == "Student":
            users_list = []
        # else return users list based on current user_group
        else:
            users_list = serializer.data

        # return response with message and data
        response = Response({
            "message": message,
            "data": users_list,
        }, status=status_message)
        return response
