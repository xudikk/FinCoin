from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render
from methodism import dictfetchall

from base.helper import cusmot_dictfetchall, custom_dictfetchone
from core.models import Backed


@login_required(login_url='login')
def basket_page(request, status=None):
    if status == 1 or status == 0:
        all_s = f"""
                select cb.id backed_id, cb.quantity soni, cb.'order', cb.cost, cp.cost as price, cb.'view', cp.img,
                cp.name, cc.name category, cp.discount_percent, cp.discount_price as dp
	            from core_backed cb , core_product cp , core_category cc 
	            where cb.user_id == {request.user.id} and cb.product_id == cp.id and cb."order" = {status}
	             and cp.category_id == cc.id
            """
        total_cost = f"""
                SELECT SUM(cb.cost) AS total_cost FROM core_backed cb 
                WHERE user_id == {request.user.id} and cb."order" = {status}
            """

        with closing(connection.cursor()) as cursor:
            cursor.execute(all_s)
            all_ = cusmot_dictfetchall(cursor)


            cursor.execute(total_cost)
            total_cost_result = custom_dictfetchone(cursor)
            total_cost = total_cost_result.get('total_cost', 0)

            ctx = {
                f"order_{status}": all_,
                'total_cost': total_cost,
                'status': status

            }
            print(f'\n\n\n\n{ctx}\n\n\n\n')
            return render(request, 'pages/notifications/basket.html', ctx)

    return render(request, 'pages/notifications/basket.html', {'status': status})




