from contextlib import closing

from django.db import connection
from django.shortcuts import render
from methodism import dictfetchall

from base.helper import cusmot_dictfetchall
from core.models import Backed


def basket_page(request, status=None):
    if status == 1 or status == 0:
        all_s = f"""
                select cb.id backed_id, cb.quantity soni, cb.'order', cb.cost, cb.'view', cp.img,
                cp.name, cc.name category, cp.discount_percent, cb.quantity
	            from core_backed cb , core_product cp , core_category cc 
	            where cb.user_id == 2 and cb.product_id == cp.id and cb."order" = {status} and cp.category_id == cc.id
            """

        with closing(connection.cursor()) as cursor:
            cursor.execute(all_s)
            all_ = cusmot_dictfetchall(cursor)

            ctx = {
                f"order_{status}": all_,
                'status': status
            }

            return render(request, 'pages/notifications/basket.html', ctx)

    return render(request, 'pages/notifications/basket.html', {'status': status})
