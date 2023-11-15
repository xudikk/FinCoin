from django.urls import path

from core.education.dars import manage_group_mentor
from core.education.education import manage_group, manage_course, interested, manage_lesson, end_lesson, attends
from core.education.user_group import user_group_page

urlpatterns = [
    # group
    path("gr/", manage_group, name="admin-group"),
    path("gr/list/<int:status>/", manage_group, name="admin-group-list"),
    path("gr/edit/<int:status>/<int:group_id>/", manage_group, name="admin-group-edit"),
    path("gr/<int:group_id>/", manage_group, name="admin-group-one"),
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

    # dars va davomat
    path("dars/g-<int:group_id>/d-<int:pk>/", manage_lesson, name='education_dars'),
    path("dars/g-<int:group_id>/edit<int:pk>/s-<status>/", manage_lesson, name='education_dars_edit'),
    path("dars/g-<int:group_id>/add/s-<status>/", manage_lesson, name='education_dars_add'),
    path("end/lesson/<int:lesson_id>/", end_lesson, name="end_lesson"),
    path("attends/g<int:group_id>/lesson/d<int:dars_id>/s<int:student_id>/<status>/", attends, name="lesson_attends"),

    # mentor group
    path("gr/mentor_/", manage_group_mentor, name="mentor_admin-group"),
    path("gr/list/<int:status>/mentor_/", manage_group_mentor, name="mentor_admin-group-list"),
    path("gr/<int:group_id>/mentor_/", manage_group_mentor, name="mentor_admin-group-one"),

    # user group
    path('user_group/', user_group_page, name='user_group_page'),
    path('user_group/g-<int:group_id>/', user_group_page, name='user_group_dars'),
]
