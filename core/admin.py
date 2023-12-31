#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.contrib import admin
from core.models import User, Token, Otp, Card, ExpiredToken, Algorithm, Done, Product, Category, New, Group, \
    GroupStudent, Course, Backed, Interested, Dars, Davomat, Monitoring, Chat, ChatUser, Message, ViewMessages, Reply_Message

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
admin.site.register(Group)
admin.site.register(GroupStudent)
admin.site.register(Course)
admin.site.register(Backed)
admin.site.register(Interested)
admin.site.register(Dars)
admin.site.register(Davomat)
admin.site.register(Monitoring)
admin.site.register(Chat)
admin.site.register(ChatUser)
admin.site.register(Message)
admin.site.register(ViewMessages)
admin.site.register(Reply_Message)
