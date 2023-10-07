#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import uuid
from contextlib import closing

from django.db import connection
from methodism import dictfetchall, dictfetchone

from base.helper import generate_number
from core.models import Card
from django.shortcuts import redirect, render


# def note():
#     sql = 'select id,name,phone from core_user where new=true and not user_type = 1 limit 3'
#     count = 'select count(*) as cnt from core_user where new = true and not user_type = 1'
#
#     with closing(connection.cursor()) as cursor:
#         cursor.execute(sql)
#         result = dictfetchall(cursor)
#
#     with closing(connection.cursor()) as cursor:
#         cursor.execute(count)
#         result_cnt = dictfetchone(cursor)
#     return {'note': result,
#             'count_not': result_cnt
#             }


def create_card(request):
    if request.user.ut not in [1, 2] or request.user.is_anonymous:
        return redirect("home")
    if request.method == "POST":
        user = request.user
        now = datetime.datetime.now()
        card = Card.objects.create(
            user=user,
            name=f"{user.full_name()}'s card",
            balance=10_000,
            number=generate_number(),
            token=uuid.uuid4(),
            expire=f"{now.month}/{f'{now.year + 1}'[2:]}",
            is_primary=False,
            card_registered_phone=user.phone
        )
    return render(request, "page", context=card.response())


def all_card(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, "page", context={
        x.response() for x in cards
    })
