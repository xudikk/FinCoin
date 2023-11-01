#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.urls import path, include
from core.dashboard.auto import gets, auto_form
from core.dashboard.home import algaritm, category
from core.dashboard.auth import create_user, change_password, grader, create_cart
from core.dashboard.monitoring import award
from core.dashboard.view import index
from core.dashboard.auth import sign_in, sign_out, clear
from core.dashboard.list import list_user, delCard, profile

urlpatterns = [

    path("", index, name='home'),

    path("category/", category, name="category"),
    path("category/form/", category, name="category_add"),
    path("category/form/<int:pk>/", category, name="category_edit"),


    # real users
    path("u/<int:type>/", create_user, name="user"),
    path("u/<int:type>/<status>/", create_user, name="user_add"),
    path("u/<int:type>/<status>/<int:pk>/", create_user, name="user_edit"),
    path("change/password/<int:user_id>/", change_password, name="change-password"),
    path("grader/<int:gr>/<int:pk>/", grader, name="grader"),

    # bonus actions
    path("cart/<user_id>/", create_cart, name="create-cart"),
    path("award/", award, name="award_for_all"),
    path("award/<int:pk>/", award, name="award_for_one"),


    # auth
    path("login/", sign_in, name='login'),
    path('logout/', sign_out, name='log-out'),


    # user actions
    path('user/info/<int:pk>/', list_user, name='get_user_info'),
    path('user-profile/', profile, name='user_profile'),

    # algaritm

    path('algaritm/', algaritm, name='all_algaritm'),
    path('algaritm/<key>/', algaritm, name='create_algaritm'),
    path('algaritm/<key>/<int:pk>/', algaritm, name='edit_algaritm'),

    #
    path('clear/', clear, name='card-clear'),


    # auto
    path("auto/<key>/", gets, name="dashboard-auto-list"),
    path("auto/<key>/<int:pk>/", gets, name="dashboard-auto-detail"),
    path("auto/<key>/add/", auto_form, name="dashboard-auto-add"),
    path("auto/<key>/edit/<int:pk>/", auto_form, name="dashboard-auto-edit"),

    #card
    path("del-card/<int:user>/<int:pk>/", delCard, name="del-card"),

]
