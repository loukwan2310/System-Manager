from string import punctuation

from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.users.models import User
from common.error_codes import HTTP_400_BAD_REQUEST


class UserTrainingLevelInfoResponse(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    value = serializers.IntegerField()
    level_down_point = serializers.IntegerField()
    level_up_point = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class UserHairStyleInfoResponse(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    url = serializers.URLField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class FitbitUserInfoResponse(serializers.Serializer):
    user_id = serializers.CharField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class MyProfileResponse(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    name = serializers.CharField()
    birthday = serializers.DateTimeField()
    gender = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class FitbitConfigInfoResponse(serializers.Serializer):
    client_id = serializers.CharField()
    response_type = serializers.CharField()
    code_challenge = serializers.CharField()
    code_challenge_method = serializers.CharField()
    scope = serializers.CharField()


class MyConfigResponse(serializers.Serializer):
    fitbit = FitbitConfigInfoResponse()


class UpdateMyProfileRequest(serializers.Serializer):
    name = serializers.CharField(max_length=24)
    birthday = serializers.DateTimeField()
    gender = serializers.IntegerField(min_value=1, max_value=3)

    def validate(self, attrs):
        name = attrs.get('name')
        birthday = attrs.get('birthday')
        current_time = timezone.localtime(timezone.now())

        if set(name).intersection(str(punctuation)):
            raise ValidationError(detail={
                'name': HTTP_400_BAD_REQUEST.get(400020)
            })

        if current_time.year - birthday.year > 130 or birthday > current_time:
            raise ValidationError(detail={
                'birthday': HTTP_400_BAD_REQUEST.get(400015)
            })
        return attrs


class UpdateMyProfileResponse(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    birthday = serializers.DateTimeField()
    gender = serializers.IntegerField()


class UserHairStyleListRequest(serializers.Serializer):
    limit = serializers.IntegerField(min_value=1, max_value=1000, required=False, default=10)
    offset = serializers.IntegerField(min_value=1, max_value=10000, required=False, default=1)


class UserHairStyleListResponse(serializers.Serializer):
    count = serializers.IntegerField()
    data = UserHairStyleInfoResponse(many=True)
