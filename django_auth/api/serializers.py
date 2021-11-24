# Import default modules
from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import password_validation


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # fields to be serialized
    class Meta:
        model = User
        fields = ("id", "username", "email")


# SignUp Serializer
class SignUpSerializer(serializers.ModelSerializer):

    # A user_level field Choices
    USER_LEVELS = (
        ("Super-Admin", "Super-Admin"),
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )
    # Required fields for SignUp
    username = serializers.CharField(required=True, help_text="Username required")
    password = serializers.CharField(required=True, help_text="Password required")
    email = serializers.EmailField(required=True, help_text="Email required")
    # A user_level field only to assign user to respective group
    user_level = serializers.ChoiceField(
        choices=USER_LEVELS, default="Student", help_text="User_Level required"
    )

    # fields to be serialized
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "user_level")

    # Validate email for uniqueness
    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError("Email address already in use.")
        return email

    # Validate username for uniqueness
    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError("Use another username.")
        return username

    # Validate password by password_validation module
    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    # Remove user_level form Serializer's response
    def to_representation(self, obj):
        ret = super(ModelSerializer, self).to_representation(obj)
        ret.pop("user_level")

    # Create new user with validated_data
    def create(self, validated_data):
        # Get group_name from user_level, this group_name will be used
        # to identify user's group and respective permissions associated with group
        group_name = validated_data["user_level"]

        # Create user with fields( username, email, password)
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )

        # Get group, if group associated with group_name is exists
        # if not, then create a new group and assign new_group=True
        group, new_group = Group.objects.get_or_create(name=group_name)

        # If new_group=True, means a new group was created, assign respective permissions
        if new_group:
            # If new group is "Teacher"
            if group_name == "Teacher":
                # Create a new permission "view_student"
                content_type = ContentType.objects.get_for_model(User)
                permission = Permission.objects.create(
                    codename="view_student",
                    name="Can view Student",
                    content_type=content_type,
                )
                # Assign this new permission to "Teacher" group
                group.permissions.add(permission)

            # Else if new group is "Super-Admin"
            elif group_name == "Super-Admin":
                # Get permission "view_user", this will allow user to view all users
                permission = Permission.objects.filter(codename="view_user").values()
                # Assign this permission to "Super-Admin" group
                group.permissions.add(permission[0]["id"])

        # Add user to it's group
        group.user_set.add(user)
        return user


# SignIn Serializer
class SignInSerializer(serializers.ModelSerializer):

    # Required fields for SignUp
    username = serializers.CharField(required=True, help_text="Username required")
    password = serializers.CharField(required=True, help_text="Password required")

    # fields to be serialized
    class Meta:
        model = User
        fields = ("id", "username", "password")

    # Validate password by password_validation module
    def validate_password(self, password):
        password_validation.validate_password(password)
        return password


# Empty Serializer
class EmptySerializer(serializers.Serializer):
    pass
