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

from core.models import Algorithm


def create_card(request):
    if request.user.ut not in [1, 2] or request.user.is_anonymous:
        return redirect("home")
    if request.method == "POST":
        user = request.user
        now = datetime.datetime.now()
        card = Card.objects.create(
            user=user,
            name=f"Fintech Coin Card",
            balance=10_000,
            number=generate_number(),
            token=uuid.uuid4(),
            expire=f"{now.month}/{f'{now.year + 1}'[2:]}",
            is_primary=False,
            card_registered_phone=user.phone
        )
    return render(request, "page", context=card.response())


def algaritm(request, key=None):
    all_algaritm = f""" select cor_al.id, cor_al.reward, cor_al.description, cor_al.bonus, user_c.first_name, user_c.last_name from core_algorithm cor_al
                    left join core_user user_c on cor_al.creator_id == user_c.id
                """
    user = f"""
            select c_user.id, c_user.first_name, c_user.last_name from core_user c_user
            """
    with closing(connection.cursor()) as cursor:
        cursor.execute(all_algaritm)
        algarithm = dictfetchall(cursor)

        cursor.execute(user)
        user = dictfetchall(cursor)

    if key == 'create':
        if request.method == 'POST':
            data = request.POST
            Algorithm.objects.create(
                reward=data['reward'],
                description=data['description'],
                bonus=data['bonus'],
                creator_id=data['created_by']
            )
            return redirect('all_algaritm')

    return render(request, 'pages/algaritm.html', {"all_algorithm": algarithm, 'key': key, 'user': user})
