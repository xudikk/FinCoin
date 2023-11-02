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
from base.helper import count, balance_rating_news
from core.forms.auto import AlgorithmForm
from core.models import Algorithm, User, Card, New


@login_required(login_url='login')
def index(request, pk=None):
    if request.user.ut == 3:
        pagination = New.objects.all().order_by('-pk')
        paginator = Paginator(pagination[:4], settings.PAGINATE_BY)
        page_number = request.GET.get("page", 1)
        paginated = paginator.get_page(page_number)

        all_algaritm = f""" select cor_al.id, cor_al.reward, cor_al.description, cor_al.bonus, user_c.first_name, user_c.last_name from core_algorithm cor_al
                            left join core_user user_c on cor_al.creator_id == user_c.id order by -(cor_al.id ) limit 4
                        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(all_algaritm)
            algarithm = dictfetchall(cursor)

        ctx = {
            "all_algo": algarithm[:4],
            "all_news": paginated,
        }
        ctx.update(balance_rating_news(request))
        return render(request, 'pages/index.html', ctx)
    ctx = {'active': "active"}
    ctx.update(count())
    ctx.update(balance_rating_news(request))
    return render(request, 'pages/index.html', ctx)

