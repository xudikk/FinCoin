from django.urls import path

from core.education.dars import manage_group_mentor, manage_lesson_mentor, end_lesson_mentor, attends_mentor, \
    interested_mentor
from core.education.education import manage_group, manage_course, interested, manage_lesson, end_lesson, attends

urlpatterns = [
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
    path("gr/edit/<int:_id>/mentor_/", manage_group_mentor, name="mentor_admin-group-edit"),
    path("gr/<int:group_id>/student/<int:student_id>/mentor_/", manage_group_mentor, name="mentor_admin-group-del-student"),
    path("gr/<int:group_id>/gs/<int:status>/mentor_/", manage_group_mentor, name="mentor_admin-group-add-student"),

    # interesting
    path("ins/mentor_/", interested_mentor, name="mentor_admin-interested"),
    path("ins/<int:contac_id>/mentor_/", interested_mentor, name="mentor_admin-interested-contacted"),
    path("ins/detail/<int:pk>/mentor_/", interested_mentor, name="mentor_admin-inters-detail"),

    # dars va davomat
    path("dars/g-<int:group_id>/d-<int:pk>/mentor_/", manage_lesson_mentor, name='mentor_education_dars'),
    path("dars/g-<int:group_id>/edit<int:pk>/s-<status>/mentor_/", manage_lesson_mentor, name='mentor_education_dars_edit'),
    path("dars/g-<int:group_id>/add/s-<status>/mentor_/", manage_lesson_mentor, name='mentor_education_dars_add'),
    path("end/lesson/<int:lesson_id>/mentor_/", end_lesson_mentor, name="mentor_end_lesson"),
    path("attends/g<int:group_id>/lesson/d<int:dars_id>/s<int:student_id>/<status>/mentor_/", attends_mentor,
         name="mentor_lesson_attends"),

]
