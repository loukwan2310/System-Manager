from rest_framework import serializers

from apps.users.models import User


class LoginRequest(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=100)
    password = serializers.CharField(required=True, max_length=100)


class UserLoginInfo(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()


class LoginResponse(serializers.Serializer):
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')
    user = UserLoginInfo(required=True)


class FitbitVerifyCodeRequest(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=100)


class FitbitVerifyCodeResponse(serializers.Serializer):
    user_id = serializers.CharField()
    target_user = UserLoginInfo(required=True)


class RegisterRequest(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("The email has already exist")
        return data


class RegisterResponse(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()


class VerifyOTPCodeRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField(max_length=6, min_length=6)


class VerifyOTPCodeResponseSerializer(serializers.Serializer):
    user = UserLoginInfo(required=True)
    access_token = serializers.CharField()
    token_type = serializers.CharField(default='Bearer')


class SendGridEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class SendGridEmailRequestResponse(serializers.Serializer):
    email = serializers.EmailField()
