from contextlib import closing

from django.conf import settings
from django.db import connection
from methodism import custom_response, dictfetchone, dictfetchall

from core.models import New


def home_page(request):
    balance = f"""
        select SUM(balance) as summ from core_card  
        where user_id = {request.user.id}
    """
    rating = f"""
    select  SUM(card.balance) as balance, uu.id, uu.username, uu.phone, uu.first_name, uu.last_name, uu.avatar
    from core_user uu
    left join core_card card ON card.user_id = uu.id 
    GROUP by card.user_id 
    order by balance DESC 
    limit {settings.PAGINATE_BY}
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