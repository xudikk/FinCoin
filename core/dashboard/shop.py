from contextlib import closing
from django.db import connection
from django.shortcuts import render
from methodism import dictfetchall
from base.errors import MSG
from base.helper import lang_helper
from core.models import Product
from core.models.core import Backed


def savat(request):
    if request.method == "POST":
        params = request.POST
        if "product_id" not in params:
            return render(request, "page", context=MSG['product_id_not_in_params'][lang_helper(request)])
        product = Product.objects.filter(id=params['product_id']).first()
        if not product:
            return render(request, "page", context=MSG['NotData'][lang_helper(request)])

        backed = Backed.objects.get_or_create(product=product, user=request.user)[0]
        backed.quantity = params.get('quantity', backed.quantity)
        backed.save()
        return render(request, "page", context=MSG['Success'][lang_helper(request)])

    if request.method == "GET":
        sql = f"""
                select bc.*, pr.name as product_name, pr.img as product_img  from core_backed bc
                inner join core_product pr on pr.id = bc.product_id 
                where bc.user_id={request.user.id}
            """
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
            mentors = dictfetchall(cursor)

        return render(request, "page", context=mentors)
    return render(request, "page")
