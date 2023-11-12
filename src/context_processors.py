from contextlib import closing

from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from methodism import dictfetchone, dictfetchall


def user_type(request):
    if not request.user.is_active:
        logout(request)

    try:
        types = {
            1: ["pages/owner/main.html", "sidebars/admin.html"],
            2: ["pages/teacher/main.html", "sidebars/mentor.html"],
            3: ["pages/default_user/main.html", "sidebars/student.html"],

        }.get(request.user.ut, ["pages/default_user/main.html", "sidebars/student.html"])
    except:
        types = ["pages/default_user/main.html", "sidebars/student.html"]
    ctx = {
        "pages_html_type": types,
        'app_name': settings.APP_NAME
    }
    if not request.user.is_anonymous:
        ctx.update({'user_type': request.user.ut})
    return ctx


def notifications(request):
    result = {}
    if not request.user.is_anonymous and request.user.ut == 1:
        sql = """
                select 
                    (select COUNT(*) from core_backed cb where cb.'view' = 0) as count_backed,
                    (select COUNT(*) from core_done cd where cd.'view' = 0) as count_done_algorithm,
                    (SELECT COUNT(*) FROM core_backed cb WHERE cb.'view' = 0) + (SELECT COUNT(*) FROM core_done cd WHERE cd.'view' = 0) AS all_count
            """
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            result = {'notifications': dictfetchone(cursor)}
    return result


def basket(request):
    result = {}
    if not request.user.is_anonymous and request.user.ut == 3:
        basket = f"""
                select (SELECT COUNT(*) from core_backed cb where cb."order" = 0 and cb.user_id == {request.user.id}) as basket_count,
            	(SELECT COUNT(*) from core_backed cb where cb."order" == 1 and cb.user_id == {request.user.id}) as order_true
            """
        with closing(connection.cursor()) as cursor:
            cursor.execute(basket)
            result = {'basket': dictfetchone(cursor)}

    return result
