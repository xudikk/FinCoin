#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.contrib import admin
from core.models import User, Token, Otp, Card, ExpiredToken
# Register your models here.
admin.site.register(User)
admin.site.register(Otp)

