#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
from contextlib import closing

from django.conf import settings
from random import randint

from django.db import connection
from methodism import dictfetchone, dictfetchall


def unique_card():
    number = "8800 " + " ".join([str(randint(1000, 9999)) for x in range(3)])
    with open("base/numbers.txt", "r") as file:
        if number not in file.read().replace('\n', '').split(","):
            file = open("base/numbers.txt", "a")
            file.write(number + ",\n")
            return number
        else:
            return unique_card()


def lang_helper(request):
    if not request.user.is_anonymous:
        return request.user.lang
    return settings.DEFAULT_LANG


def card_mask(number):
    return number[0:4] + ' **** ****' + number[14:]


def generate_number():
    return unique_card()


def cusmot_dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = []
    for i in cursor.description:
        columns.append(i[0])
    a = cursor.fetchall()
    img = None
    if "img" in columns:
        img = columns.index("img")
    natija = []
    for i in a:
        i = list(i)
        if img:
            i[img] = f"{settings.HOST_URL}/media/" + i[img]
        b = dict(zip(columns, i))
        natija.append(b)
    return natija


def custom_dictfetchone(cursor):
    columns = [i[0] for i in cursor.description]
    row = cursor.fetchone()
    if row is not None:
        img = None
        if "img" in columns:
            img = columns.index("img")
        row = list(row)
        if img is not None:
            row[img] = f"{settings.HOST_URL}/media/" + row[img]
        return dict(zip(columns, row))
    else:
        return None


def look_at_params(params: dict, requires: list):
    return set(requires) - set(params.keys())


def make_transfer(sender, receiver, amount: int):
    try:
        sender.balance = sender.balance - amount
        receiver.balance = receiver.balance + amount
    except:
        return False
    sender.save(), receiver.save()
    return True


def gcnt():
    sql = """
            SELECT  
            (SELECT COUNT(*) FROM core_group where status == 1) AS start, 
            (SELECT COUNT(*) FROM   core_group where status == 2) AS act,
            (SELECT COUNT(*) FROM   core_group where status == 3 ) AS end,
            (SELECT COUNT(*) FROM   core_interested WHERE contacted is FALSE or "view" is FALSE) AS icnt
            FROM core_group
            limit 1
        """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        res = dictfetchone(cursor)

    return res


def count():
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
