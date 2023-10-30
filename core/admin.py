#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.contrib import admin
from core.models import User, Token, Otp, Card, ExpiredToken, Algorithm, Done, Product, Category, New

# Register your models here.
admin.site.register(User)
admin.site.register(Otp)
admin.site.register(Token)
admin.site.register(Card)
admin.site.register(ExpiredToken)
admin.site.register(Algorithm)
admin.site.register(Done)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(New)