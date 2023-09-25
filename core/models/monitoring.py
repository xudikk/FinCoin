#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.db import models

from base.helper import card_mask
from core.models import User


class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=128)
    balance = models.FloatField(max_length=128)  # default = 0
    mask = models.CharField(max_length=128, null=True)
    number = models.CharField(max_length=128, default=0)
    token = models.CharField(max_length=128, null=True)
    expire = models.CharField(max_length=10)  # goden do
    is_primary = models.BooleanField()
    card_registered_phone = models.CharField(max_length=50, null=True)
    blocked = models.IntegerField(null=True)  # ?
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "M. Cards"

    def save(self, *args, **kwargs):
        if not self.mask:
            self.mask = card_mask(self.number)
        return super(Card, self).save(*args, **kwargs)

    def response(self):
        return {
            'id': self.token,
            'user': self.user.full_name(),
            'name': self.name,
            'balance': self.balance,
            'mask': self.mask,
            'number': self.number,
            'token': self.token,
            'expire_date': self.expire,
            'is_primary': self.is_primary,
            'card_registered_phone': self.card_registered_phone,
            'blocked': self.blocked,
            'created_at': self.created.strftime("%d %b, %Y"),
            'updated_at': self.updated.strftime("%d %b, %Y"),
        }
