#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from contextlib import closing

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import redirect, render
from methodism import dictfetchall

from base.custom import admin_permission_checker
from base.helper import count, balance_rating_news, gcnt
from core.forms.auto import AlgorithmForm
from core.models import Algorithm, User, Card, New


@login_required(login_url='login')
def index(request, pk=None):
    if request.user.ut == 3:
        pagination = New.objects.all().order_by('-pk')
        all_algaritm = f""" select cor_al.id, cor_al.reward, cor_al.description, cor_al.bonus, user_c.first_name, user_c.last_name from core_algorithm cor_al
                            left join core_user user_c on cor_al.creator_id == user_c.id order by -(cor_al.id ) limit 4
                        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(all_algaritm)
            algarithm = dictfetchall(cursor)

        ctx = {
            "all_algo": algarithm,
            "all_news": pagination[:4],
        }
        ctx.update(balance_rating_news(request))
        return render(request, 'pages/index.html', ctx)
    if request.user.ut == 2:
        ctx = {
            'position': 'main',
            'gcnt': gcnt(),
        }

        return render(request, 'pages/index.html', ctx)
    ctx = {'active': "active"}
    ctx.update(count())
    ctx.update(balance_rating_news(request))
    ctx.update({"open_menu_fc": "menu-open"})

    return render(request, 'pages/index.html', ctx)
