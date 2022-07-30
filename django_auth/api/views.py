# Import default modules
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

# Import Serializer from api.serializers
from .serializers import UserSerializer, SignUpSerializer


# SignUpAPIView, used as_view for signup url,
class SignUpAPIView(generics.GenericAPIView):
    # SignUpSerializer class for serializering request
    serializer_class = SignUpSerializer

    # POST method handler, hald post method requests for this view
    def post(self, request, *args, **kwargs):
        # Serializer instance with data
        serializer = self.get_serializer(data=request.data)
        # Check validity of data, if it is not valid raise exceptions
        serializer.is_valid(raise_exception=True)

        # Save new user
        user = serializer.save()

        # Return User data, by serializing user info, with a new token
        ### afte completion of project, save this token in cookies HttpOnly
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "token": Token.objects.create(user=user).key,
            }
        )
