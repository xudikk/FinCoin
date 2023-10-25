from contextlib import closing

from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from methodism import dictfetchone, dictfetchall

from base.helper import cusmot_dictfetchall


def main(requests):
    return {
        "app_name": settings.APP_NAME
    }


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


def count(request):
    sql = """
            select (select COUNT(*) from core_user WHERE ut = 1) as count_admin,
            (select COUNT(*) from core_user WHERE ut = 2) as count_teacher,
            (select COUNT(*) from core_user WHERE ut = 3) as count_user,
            (select COUNT(*) from core_algorithm) as count_algorithm
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        result = dictfetchone(cursor)

    return {
        'count': result
    }


def balance_rating_news(request):
    if not request.user.is_anonymous:
        balance = f"""
            select SUM(balance) as summ from core_card  
            where user_id = {request.user.id}
        """
        rating = f"""
                SELECT cast(COALESCE(SUM(card.balance), 0) as int) as balance, uu.id, COALESCE(uu.username, 'not set yet') as username,
             uu.phone, (COALESCE(uu.first_name, '') || ' ' || COALESCE(uu.last_name, '')) as full_name, uu.avatar, uu.level
            from core_user uu
            left join core_card card on card.user_id = uu.id
            group by uu.id, uu.username, uu.phone, uu.first_name, uu.last_name, uu.avatar
            order by balance desc 
            limit 5
        """
        balances = """
            SELECT cast(COALESCE(SUM(card.balance), 0) as int) as balance
            from core_user uu
            left join core_card card on card.user_id = uu.id
            group by uu.id, uu.username, uu.phone, uu.first_name, uu.last_name, uu.avatar
            order by balance desc 
            limit 5
        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(balance)
            balance = dictfetchone(cursor)

            cursor.execute(rating)
            rating = dictfetchall(cursor)

            cursor.execute(balances)
            balances = cursor.fetchall()
        return {
            "balance": balance['summ'],
            "rating": rating,
            "balances": [x[0] for x in balances]

        }
    return {}
