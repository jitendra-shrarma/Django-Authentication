from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, help_text='Username required')
    email = serializers.EmailField(required=True, help_text='Email required')
    password = serializers.CharField(required=True, help_text='Password required')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
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
        return email

    def validate_password(self, password):
        password_validation.validate_password(password)
        return password

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
