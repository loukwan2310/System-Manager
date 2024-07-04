from django.db import models

from common.models import BaseModel


class BannedTokens(BaseModel):
    """ These AD tokens are banned from being used. """
    token = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
