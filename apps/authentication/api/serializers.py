from rest_framework import serializers


class LoginRequest(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=100)
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
