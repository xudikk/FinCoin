from contextlib import closing

from django.db import connection
from django.shortcuts import render, redirect

from base.errors import MSG
from base.helper import lang_helper
from core.models import Product
from core.models.core import Backed


def savat(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        params = request.POST
        print(params)
        product = Product.objects.filter(id=params['product_id']).first()

        if not product:
            return render(request, "pages/shop.html", context={"error": MSG['NotData'][lang_helper(request)]})

        backed = Backed.objects.get_or_create(product=product, user=request.user)[0]
        backed.quantity = params.get('quentity', backed.quantity)
        backed.save()
        return redirect('shop')

    total = f""" SELECT SUM(cost) AS total_cost, SUM(quantity) AS total_quantity, user_id  FROM core_backed cb GROUP BY user_id
                             """

    with closing(connection.cursor()) as cursor:
        cursor.execute(total)
        results = cursor.fetchall()

    user_data = None

    current_user_id = request.user.id
    for result in results:
        total_cost = result[0]
        total_quantity = result[1]
        user_id = result[2]

        if user_id == current_user_id:
            user_data = {
                'total_cost': total_cost,
                'total_quant': total_quantity
            }
            break
    product = Product.objects.all()

    ctx = {
        'user_data': user_data,
        "root": product
    }

    return render(request, "pages/shop.html", ctx)
