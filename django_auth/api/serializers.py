from rest_framework import serializers
from django.contrib.auth.models import User, Group
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
        is_superuser = False
        is_staff = False

        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password'],
        )

        group, group_status = Group.objects.get_or_create(name=group_name)
        group.user_set.add(user)
        return user
