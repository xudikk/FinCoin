from contextlib import closing

from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from methodism import dictfetchone


def main(requests):
    return {
        "app_name": settings.APP_NAME
    }


def user_type(request):
    if not request.user.is_active:
        logout(request)

    try:
        types = {
            1: "pages/owner/main.html",
            2: "pages/teacher/main.html",
            3: "pages/default_user/main.html",

        }.get(request.user.ut, ["pages/default_user/main.html"])
    except:
        types = ["pages/client/main.html"]
    ctx = {
        "type": types,
        'app_name': settings.APP_NAME
    }
    if not request.user.is_anonymous:
        ctx.update({'user_type': request.user.ut})
    return ctx


def count(request):
    sql = """
            select (select COUNT(*) from core_user WHERE ut = 1) as count_admin,
            (select COUNT(*) from core_user WHERE ut = 2) as count_teacher,
            (select COUNT(*) from core_user WHERE ut = 3) as count_user,
            (select COUNT(*) from core_card) as count_card
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

    return {
        'count': result
    }
