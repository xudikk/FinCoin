from contextlib import closing

from django.conf import settings
from django.db import connection
from methodism import custom_response, dictfetchone, dictfetchall
from methodism.sqlpaginator import SqlPaginator

from core.models import New


def home_page(request):
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
    news = "select id, img, title from core_new order by id desc limit 3"

    with closing(connection.cursor()) as cursor:
        cursor.execute(balance)
        balance = dictfetchone(cursor)

        cursor.execute(rating)
        rating = dictfetchall(cursor)

        cursor.execute(news)
        news = dictfetchall(cursor)

    return custom_response(True, data={
        "balance": balance['summ'],
        "rating": rating,
        "news": news
    })


def mentors(request):
    mentors = "select * from core_user where ut=2 order by id desc"
    with closing(connection.cursor()) as cursor:
        cursor.execute(mentors)
        mentors = dictfetchall(cursor)

    return custom_response(True, data=mentors)


def algorithm(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        page = 1
    offset = (page - 1) * settings.PAGINATE_BY
    # print(request.user.id)

    algos = f""" 
            SELECT al.*, us.first_name, us.last_name, us.username  from core_algorithm al
            inner join core_user us on al.creator_id = us.id
            LIMIT {settings.PAGINATE_BY} OFFSET {offset}
            """
    cnt = "SELECT COUNT(*) as cnt from core_algorithm"

    with closing(connection.cursor()) as cursor:
        cursor.execute(algos)
        algos = dictfetchall(cursor)
        cursor.execute(cnt)
        cnt = dictfetchone(cursor)

        if cnt:
            count_records = cnt['cnt']
        else:
            count_records = 0
        paginator = SqlPaginator(request, page=page, per_page=settings.PAGINATE_BY, count=count_records)
        pagging = paginator.get_paginated_response(per_page=settings.PAGINATE_BY, current_page=page)

    return custom_response(True, data={"algorithms": algos, "pagging": pagging})
