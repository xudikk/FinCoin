#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from methodism import models as abs_models
from django.db import models

from core.models import User


class Token(abs_models.Token):
    pass

    class Meta:
        verbose_name_plural = "T. Auth Token"


class Otp(abs_models.Otp):
    mobile = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    by = models.SmallIntegerField(choices=[
        (1, "login"),
        (2, "dashboard"),
        (3, "p2p")
    ], default=1)

    class Meta:
        verbose_name_plural = "T. One Time Password"


class ExpiredToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expired_access_token")
    key = models.CharField(max_length=128)
    created = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name_plural = "T. Expired Token"

    def __str__(self):
        return self.key