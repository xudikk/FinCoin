from contextlib import closing

from django.db import connection
from django.shortcuts import render
from methodism import dictfetchall


def user_group_page(request, group_id=None):
    all_group = f"""
            select cg.group_id, cg.start_date, cg2.name group_name, cg2.duration, cg2.status, cg2.course_id,
            cg2.start_date group_start_date 
            from core_groupstudent cg , core_group cg2 
            where cg.group_id == cg2.id and cg.student_id == {request.user.id}
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(all_group)
        all_ = dictfetchall(cursor)
    ctx = {"all_user_group": all_, 'gr_active': 'active'}
    if group_id:
        all_lesson = f"""
            SELECT dars.*, cg.start_date AS cursga_kirgan, davomat.status
            FROM core_dars AS dars
            LEFT JOIN core_groupstudent AS cg ON dars.group_id = cg.group_id AND cg.student_id = {request.user.id}
            LEFT JOIN core_davomat AS davomat ON dars.id = davomat.dars_id AND davomat.user_id = {request.user.id}
            WHERE dars.group_id = {group_id};
            """

        with closing(connection.cursor()) as cursor:
            cursor.execute(all_lesson)
            all_dars = dictfetchall(cursor)

            ctx.update({"all_lesson": all_dars, "group_id": group_id})
        return render(request, 'pages/education/user_group.html', ctx)

    return render(request, 'pages/education/user_group.html', ctx)
