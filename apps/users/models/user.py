import logging

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from common.models import BaseModel

logger = logging.getLogger(__file__)


class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        user = self.model(username=username, email=email)
        user.set_password(password)
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
