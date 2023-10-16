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

from base.custom import permission_checker
from base.helper import generate_number
from core.models import Card, User
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


def algaritm(request, key=None, pk=None):
    all_algaritm = f""" select cor_al.id, cor_al.reward, cor_al.description, cor_al.bonus, user_c.first_name, user_c.last_name from core_algorithm cor_al
                    left join core_user user_c on cor_al.creator_id == user_c.id
                """
    user = f"""
            select c_user.id, c_user.first_name, c_user.last_name from core_user c_user
            """
    bonuses = "select bonus from core_algorithm"

    with closing(connection.cursor()) as cursor:
        cursor.execute(all_algaritm)
        algarithm = dictfetchall(cursor)

        cursor.execute(user)
        user = dictfetchall(cursor)

        cursor.execute(bonuses)
        bonuses = cursor.fetchall()

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
    if key == 'edit':

        edit_ = Algorithm.objects.filter(id=pk).first()
        if not edit_:
            return redirect('all_algaritm')
        if request.method == 'POST':
            data = request.POST
            edit_.reward = data['reward']
            edit_.bonus = data['bonus']
            edit_.creator_id = data['created_by']
            edit_.description = data['desc']

            edit_.save()
            return redirect('all_algaritm')
        return render(request, 'pages/algaritm.html',
                      {"all_algorithm": algarithm, 'key': key, 'user': user, "edited": edit_})
    return render(request, 'pages/algaritm.html',
                  {"all_algorithm": algarithm, 'key': key, 'user': user, "bonuses": [x[0] for x in bonuses]})


@permission_checker
def admin_page(request, key=None):
    admin_ = f"""select * from core_user c_us WHERE c_us.ut = 1"""
    with closing(connection.cursor()) as cursor:
        cursor.execute(admin_)
        admin_user = dictfetchall(cursor)
    if key == 'create_admin':
        if request.method == 'POST':
            data = request.POST
            user_type = data.get("ut")
            gender = data.get('gender')

            user1 = User.objects.filter(phone=data["phone"]).first()
            if user1:
                return redirect('user_list', {"error": "Bu raqam band qilingan"})

            user = User.objects.create_user(
                phone=data["phone"], password=data["pass"],
                first_name=data["name"], gender=gender,
                last_name=data['last_name'],
                email=data["email"], ut=1
            )
            user.save()
            card = Card.objects.create(
                user=user,
                number=generate_number(),
                name=f"Fintech Coin Card",
                expire=f"{datetime.datetime.now().month}/{str(datetime.datetime.now().year + 1)[2:]}",
                is_primary=False,
                card_registered_phone=user.phone
            )
            card.save()
            return redirect('admin_page')

    return render(request, 'pages/admin_page.html', {"admin_": admin_user, 'key': key})
