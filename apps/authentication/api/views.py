from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from pyotp.utils import strings_equal
from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.authentication.api.serializers import (LoginRequest, LoginResponse, RegisterRequest, RegisterResponse,
                                                 VerifyOTPCodeRequestSerializer, VerifyOTPCodeResponseSerializer,
                                                 SendGridEmailRequestSerializer, SendGridEmailRequestResponse,
                                                 GetOTPCodeResponseSerializer)
from apps.authentication.models import BannedTokens
from apps.users.models import User
from apps.users.models.user import UserOTP
from common.exceptions import BadRequest, Unauthorized
from common.jwt_manager import JWTManager
from common.serializers import ErrorResponse


class TokenAuthentication:

    @staticmethod
    def create_token(user):
        expired = timezone.localtime(timezone.now()) + timedelta(hours=settings.JWT_TOKEN_EXPIRE_HOURS)
        payload = {
            'jti': uuid4().hex,
            'sub': str(user.id),
            'exp': expired
        }
        token = JWTManager.create_token(payload, secret_key=settings.SECRET_KEY)
        return token


@extend_schema(tags=['Authentication'])
class LoginAPIView(APIView, TokenAuthentication):
    permission_classes = []
    authentication_classes = []

    @extend_schema(auth=[], request=LoginRequest,
                   responses={200: LoginResponse, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        access_token = None
        serializer = LoginRequest(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(400000, error_detail=serializer.errors)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=email).first()
        if not user or (user and not check_password(password, user.password)):
            raise Unauthorized(401004)
        if user.is_active:
            access_token = self.create_token(user)
        response = LoginResponse({
            'access_token': access_token,
            'user': user
        })
        return Response(response.data)


@extend_schema(tags=['Authentication'])
class LogoutAPIView(APIView):

    def _ban_token(self, request):
        # Remove old, expired tokens
        time_threshold = timezone.localtime(timezone.now() - timedelta(hours=5))
        BannedTokens.objects.filter(created__lt=time_threshold).delete()
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if isinstance(authorization_header, str):
            authorization_header = authorization_header.encode(HTTP_HEADER_ENCODING)
        token = authorization_header.split()[1]
        if token:
            baned_token = BannedTokens(token=token)
            baned_token.save()

    @transaction.atomic
    @extend_schema(request=None, responses={204: None, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        self._ban_token(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Authentication'])
class RegisterAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(auth=[], request=RegisterRequest,
                   responses={200: LoginResponse, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        serializer = RegisterRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        username = email.split("@")[0]
        user = User.objects.create_inactive_user(username=username, email=email, password=password)
        response = RegisterResponse(user)
        return Response(response.data)


@extend_schema(tags=['Authentication'])
class OTPCodeAPIView(APIView, TokenAuthentication):
    authentication_classes = []
    permission_classes = []

    @transaction.atomic()
    @extend_schema(auth=[], responses={200: VerifyOTPCodeResponseSerializer, 400: ErrorResponse, 500: ErrorResponse})
    def get(self, request):
        all_otp = UserOTP.objects.all()
        response = GetOTPCodeResponseSerializer(all_otp, many=True)
        return Response(response.data)

    @transaction.atomic()
    @extend_schema(auth=[], request=VerifyOTPCodeRequestSerializer,
                   responses={200: VerifyOTPCodeResponseSerializer, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        serializer = VerifyOTPCodeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request_otp = serializer.validated_data.get("otp_code")
        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        if user.is_active:
            raise BadRequest(400029)
        user_otp = UserOTP.objects.filter(target_user_id=user.id).first()
        if not user_otp:
            raise BadRequest(400026)
        if not user:
            raise BadRequest(400026)
        otp_verified = strings_equal(user_otp.code, request_otp)
        if not otp_verified:
            raise BadRequest(400027)
        if timezone.localtime(timezone.now()) > user_otp.expire_time:
            raise BadRequest(400028)
        user.is_active = True
        user.save()
        access_token = self.create_token(user)
        response = VerifyOTPCodeResponseSerializer({
            'access_token': access_token,
            'user': user
        })
        return Response(response.data)


@extend_schema(tags=['Authentication'])
class SendgridEmailAPIView(APIView):
    permission_classes = []
    authentication_classes = []

    @extend_schema(auth=[], request=SendGridEmailRequestSerializer,
                   responses={200: LoginResponse, 400: ErrorResponse, 500: ErrorResponse})
    def post(self, request):
        serializer = SendGridEmailRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise BadRequest(400026)
        if user.is_active:
            raise BadRequest(400029)
        UserOTP.send_otp_to_email(email, user.id)
        response = SendGridEmailRequestResponse(user)
        return Response(response.data)
