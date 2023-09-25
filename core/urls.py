#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.urls import path, include
from core.dashboard.view import index
from core.dashboard.auth import sign_in, sign_out
from core.dashboard.list import list_user, create_user

urlpatterns = [

    path("", index, name='home'),

    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),

    # list
    path('user/list/', list_user, name='user_list'),
    path('user/create/', create_user, name='create_user'),
]
