from contextlib import closing

from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render
from methodism import dictfetchall

from base.custom import mentor_permission_checker, admin_permission_checker
from core.models import Course


@mentor_permission_checker
def user_instruction(request, student_id=None):
    if student_id:
        student = f"""                    
                select c_davomat.status, c_davomat.user_id, c_dars.topic, c_dars.startedTime, c_dars.endedTime, c_dars.is_end, c_user.username, c_course.name course_name from core_davomat c_davomat
                inner join core_dars c_dars on c_davomat.dars_id == c_dars.id inner join core_user c_user on c_davomat.user_id == c_user.id inner join core_group c_group on c_davomat.group_id == c_group.id inner join core_course c_course on c_group.course_id == c_course.id
                where c_davomat.user_id == {student_id}
            """
        with closing(connection.cursor()) as cursor:
            cursor.execute(student)
            _student = dictfetchall(cursor)
        ctx = {"student_id": _student}
        return render(request, 'pages/teacher/user_davomat.html', ctx)
    else:
        all_lesson = f"""
                select
                core_course.name as course_name, core_group.id as group_id, core_group.name as group_name,
                core_user.id as student_id,core_user.username as student_username,
                (COALESCE(core_user.first_name, '') || ' ' || COALESCE(core_user.last_name, '')) as student_full_name from
                core_course inner join core_group on core_course.id = core_group.course_id
                inner join core_groupstudent on core_group.id = core_groupstudent.group_id
                inner join core_user on core_groupstudent.student_id = core_user.id where core_course.mentor_id = {request.user.id}
                group by core_user.id;
                """

        with closing(connection.cursor()) as cursor:
            cursor.execute(all_lesson)
            all_dars = dictfetchall(cursor)

            paginator = Paginator(all_dars, 10)
            page_number = request.GET.get("page", 1)
            paginated = paginator.get_page(page_number)

        ctx = {"lessons": paginated}
        return render(request, 'pages/teacher/user_davomat.html', ctx)


@admin_permission_checker
def _instruction(request, user_id=None):
    all_lesson = f"""
            select c_davomat.status, c_dars.topic, c_dars.is_end, c_dars.startedTime, c_dars.endedTime, c_user.username, c_course.name course_name from core_davomat c_davomat
            inner join core_dars c_dars on c_davomat.dars_id == c_dars.id inner join core_user c_user on c_davomat.user_id == c_user.id inner join core_group c_group on c_davomat.group_id == c_group.id inner join core_course c_course on c_group.course_id == c_course.id
            where c_davomat.user_id == {user_id}
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(all_lesson)
        all_dars = dictfetchall(cursor)
    ctx = {"lessons": all_dars}
    return render(request, 'pages/owner/all_user_davomat.html', ctx)
