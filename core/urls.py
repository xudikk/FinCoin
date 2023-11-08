#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.urls import path, include
from core.dashboard.auto import gets, auto_form
from core.dashboard.education import manage_group, manage_course, interested
from core.dashboard.home import algaritm, category,done_algoritms
from core.dashboard.auth import create_user, change_password, grader, create_cart
from core.dashboard.monitoring import award, p2p
from core.dashboard.notification import notification, done_action, backed_action
from core.dashboard.shop import savat
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

    #user payments
    path('transfer/', p2p, name='user_payments'),
    path('transfer/<status>/', p2p, name='p2p'),

    # algaritm

    path('algaritm/', algaritm, name='all_algaritm'),
    path('algaritm/<key>/', algaritm, name='create_algaritm'),
    path('algaritm/<key>/<int:pk>/', algaritm, name='edit_algaritm'),
    path("algaritms/done/", done_algoritms, name='done_algoritms'),
    path("algaritms/done/<int:pk>", done_algoritms, name='done_algoritms_pk'),

    #
    path('clear/', clear, name='card-clear'),

    # auto
    path("auto/<key>/", gets, name="dashboard-auto-list"),
    path("auto/<key>/<int:pk>/", gets, name="dashboard-auto-detail"),
    path("auto/<key>/add/", auto_form, name="dashboard-auto-add"),
    path("auto/<key>/edit/<int:pk>/", auto_form, name="dashboard-auto-edit"),

    # card
    path("del-card/<int:user>/<int:pk>/", delCard, name="del-card"),

    # group
    path("gr/", manage_group, name="admin-group"),
    path("gr/list/<int:status>/", manage_group, name="admin-group-list"),
    path("gr/<int:group_id>/", manage_group, name="admin-group-one"),
    path("gr/edit/<int:_id>/", manage_group, name="admin-group-edit"),
    path("gr/<int:group_id>/student/<int:student_id>/", manage_group, name="admin-group-del-student"),
    path("gr/<int:group_id>/gs/<int:status>", manage_group, name="admin-group-add-student"),

    # course
    path("course/", manage_course, name="admin-course"),
    path("course/one/<int:pk>/", manage_course, name="admin-course-one"),
    path("course/<int:edit_id>/", manage_course, name="admin-course-edit"),
    path("course/del/<int:del_id>/", manage_course, name="admin-course-delete"),

    # interesting
    path("ins/", interested, name="admin-interested"),
    path("ins/<int:contac_id>", interested, name="admin-interested-contacted"),
    path("ins/detail/<int:pk>/", interested, name="admin-inters-detail"),

    # shop
    path('mahsulotlar/', savat, name='shop'),

    # notification
    path('notifications/', notification, name='notifications'),
    path('notifications/<status>/', notification, name='notification_status'),
    path('notifications/<int:pk>/<status>/', backed_action, name='notification_backed'),
    path('notifications/<int:pk>/<status>/<int:action>/', done_action, name='notification_action'),

]
