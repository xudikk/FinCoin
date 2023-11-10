from django.urls import path

from core.education.education import manage_group, manage_course, interested, manage_lesson

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

]

