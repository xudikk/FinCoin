#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.urls import path, include

from core.dashboard.home import news
from core.dashboard.monitoring import algaritm
from core.dashboard.view import index
from core.dashboard.auth import sign_in, sign_out
from core.dashboard.list import list_user

urlpatterns = [

    path("", index, name='home'),

    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),

    # list
    path('user/list/', list_user, name='user_list'),
    path('user/list/<key>/', list_user, name='create_user'),
    path('user/list/<key>/', list_user, name='teacher'),

    # user actions
    path('user/list/<key>/<int:pk>/', list_user, name='update_user'),
    path('user/list/<key>/<int:pk>/', list_user, name='get_user_info'),

    # algaritm
    path('algaritm/', algaritm, name='all_algaritm'),
    path('algaritm/<key>/', algaritm, name='create_algaritm'),

    # news
    path('news/', news, name='news'),
    path('news/<key>/<int:pk>/', news, name='news_view'),
]
