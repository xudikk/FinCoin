#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.urls import path, include
from core.dashboard.auto import gets, auto_form
from core.dashboard.monitoring import algaritm, admin_page, category
from core.dashboard.view import index
from core.dashboard.auth import sign_in, sign_out, clear
from core.dashboard.list import list_user


urlpatterns = [

    path("", index, name='home'),

    path("category/", category, name="category"),
    path("category/<status>/", category, name="category_add"),
    path("category/<status>/<int:pk>/", category, name="category_edit"),



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
    path('algaritm/<key>/<int:pk>/', algaritm, name='edit_algaritm'),

    #
    path('clear/', clear, name='card-clear'),

    # admin page
    path('admin-page/', admin_page, name='admin_page'),
    path('admin-page/<key>/', admin_page, name='create_admin'),


    # auto
    path("<key>/", gets, name="dashboard-auto-list"),
    path("<key>/<int:pk>/", gets, name="dashboard-auto-detail"),
    path("auto/<key>/add/", auto_form, name="dashboard-auto-add"),
    path("auto/<key>/edit/<int:pk>/", auto_form, name="dashboard-auto-edit"),

]
