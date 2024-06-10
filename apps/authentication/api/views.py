from uuid import uuid4
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
# from fcm_django.models import FCMDevice
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.users.models import User
from common.exceptions import BadRequest, Unauthorized
from common.jwt_manager import JWTManager
from common.serializers import ErrorResponse
from common.fitbit_client import FitbitAPIException
from .serializers import LoginRequest, LoginResponse, FitbitVerifyCodeRequest, FitbitVerifyCodeResponse


@extend_schema(tags=['Authentication'])
class LoginAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def _create_token(user):
        expired = timezone.localtime(timezone.now()) + timedelta(hours=settings.JWT_TOKEN_EXPIRE_HOURS)
        payload = {
            'jti': uuid4().hex,
            'sub': str(user.id),
            'exp': expired
        }
        token = JWTManager.create_token(payload, secret_key=settings.SECRET_KEY)
        return token

    @extend_schema(auth=[], request=LoginRequest,
                   responses={200: LoginResponse, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        serializer = LoginRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(username=username).first()
        if not user or (user and not check_password(password, user.password)):
            raise Unauthorized(401004)

        access_token = self._create_token(user)
        response = LoginResponse({
            'access_token': access_token,
            'user': user
        })
        return Response(response.data)


@extend_schema(tags=['Authentication'])
class LogoutAPIView(APIView):

    @extend_schema(request=None, responses={204: None, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        user = request.user
        FCMDevice.objects.filter(user_id=user.id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Authentication'])
class FitbitVerifyCodeAPIView(APIView):

    @transaction.atomic()
    @extend_schema(request=FitbitVerifyCodeRequest,
                   responses={200: FitbitVerifyCodeResponse, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        serializer = FitbitVerifyCodeRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        fitbit_user_id = None
        user = request.user
        code = serializer.validated_data.get('code')
        try:
            fitbit_user_id = FitbitUser.verify_code(code=code, target_user=user)
        except FitbitAPIException as err:
            raise BadRequest(400008) from err

        FitbitUser.objects.filter(target_user_id=user.id) \
            .exclude(user_id=fitbit_user_id) \
            .delete()
        response = FitbitVerifyCodeResponse({
            'user_id': fitbit_user_id,
            'target_user': user
        })
        return Response(response.data)
