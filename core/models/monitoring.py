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
    balance = models.FloatField(max_length=128, default=10000)  # default = 0
    mask = models.CharField(max_length=128, null=True)
    number = models.CharField(max_length=128)
    token = models.CharField(max_length=128, null=True)
    expire = models.CharField(max_length=10)  # goden do
    is_primary = models.BooleanField()
    card_registered_phone = models.CharField(max_length=50, null=True)
    blocked = models.IntegerField(null=True)  # ? IntegerField or BooleanField
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = "M. Cards"

    def save(self, *args, **kwargs):
        if not self.mask:
            self.mask = card_mask(self.number)
        return super(Card, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}  ||  {self.balance}"

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


class Monitoring(models.Model):
    tr_id = models.CharField(max_length=512)
    sender = models.ForeignKey(Card, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='sender')
    sender_token = models.CharField(max_length=128, null=True, blank=True, editable=False)
    receiver = models.ForeignKey(Card, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='receiver')
    receiver_token = models.CharField(max_length=128, null=True, blank=True, editable=False)
    amount = models.IntegerField(default=0)
    status = models.SmallIntegerField(default=0)  # 0-created, 1-success, 2-canceled
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def response(self):
        return {
            "transaction_id": self.tr_id,
            "amount": self.amount,
            "sender": self.sender.mask,
            "receiver": self.sender.number,
            "status": {0: "Created", 1: "Success", 2: "Canceled"}[self.status]
        }
