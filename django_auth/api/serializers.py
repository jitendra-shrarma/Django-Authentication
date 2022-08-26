from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SignUpSerializer(serializers.ModelSerializer):
    USER_LEVELS = (
        ("Super-Admin", "Super-Admin"),
        ("Teacher", "Teacher"),
        ("Student", "Student"),
    )
    username = serializers.CharField(required=True, help_text='Username required')
    password = serializers.CharField(required=True, help_text='Password required')
    email = serializers.EmailField(required=True, help_text='Email required')
    user_level = serializers.ChoiceField(choices=USER_LEVELS, default="Student", help_text='User_Level required')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'user_level')
        extra_fields = {'password': {'write_only':True}}

    def validate_email(self, email):
        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError('Email address already in use.')
        return email

    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if user:
            raise serializers.ValidationError('Use another username.')
        return username

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def to_representation(self, obj):
        ret = super(ModelSerializer, self).to_representation(obj)
        ret.pop('user_level')

    def create(self, validated_data):
        group_name = validated_data['user_level']

        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )

        group, new_group = Group.objects.get_or_create(name=group_name)
        if new_group:
            if group_name == "Teacher":
                content_type = ContentType.objects.get_for_model(User)
                permission = Permission.objects.create(
                    codename = "view_student",
                    name = "Can view Student",
                    content_type = content_type,
                )
                group.permissions.add(permission)
            elif group_name == "Super-Admin":
                permission = Permission.objects.filter(codename="view_user").values()
                group.permissions.add(permission[0]['id'])

        group.user_set.add(user)
        return user
