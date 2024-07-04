import logging
from datetime import timedelta
import pyotp
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from common.emails import SendGridEmailClient
from common.models import BaseModel

logger = logging.getLogger(__file__)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_inactive_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username=username, email=email, password=password)
        user.save()
        return user


class User(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=31, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=24, null=True)
    birthday = models.DateTimeField(null=True)
    gender = models.SmallIntegerField(null=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'users_users'

    def __str__(self):
        return self.username


class UserOTP(BaseModel):
    code = models.CharField()
    counter = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    expire_time = models.DateTimeField()
    target_user = models.ForeignKey("users.User", on_delete=models.CASCADE)

    @staticmethod
    def _generate_otp_code():
        totp = pyotp.TOTP(pyotp.random_base32())
        return totp.now()

    @classmethod
    def send_otp_to_email(cls, email, target_user_id):
        otp_code = cls._generate_otp_code()
        sendgrid = SendGridEmailClient()
        sendgrid.send_mail_verification_code(email, "Hello", otp_code)
        expire_time = timezone.now() + timedelta(minutes=1)
        payload = {
            "code": otp_code,
            "expire_time": expire_time,
            "target_user_id": target_user_id

        }
        if cls.objects.filter(target_user_id=target_user_id).exists():
            cls.objects.filter(target_user_id=target_user_id).update(**payload)
        else:
            cls.objects.create(**payload)
