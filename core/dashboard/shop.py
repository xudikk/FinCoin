from contextlib import closing
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchall, dictfetchone

from base.custom import permission_checker, admin_permission_checker
from base.errors import MSG
from base.helper import lang_helper, cusmot_dictfetchall
from core.models import Product
from core.models.core import Backed


def savat(request):
    if request.user.is_anonymous:
        return redirect('login')
    if request.method == "POST":
        params = request.POST
        # print(params)
        product = Product.objects.filter(id=params['product_id']).first()
        if not product:
            return render(request, "page", context=MSG['NotData'][lang_helper(request)])

        backed = Backed.objects.get_or_create(product=product, user=request.user)[0]
        backed.quantity = params.get('quantity', backed.quantity)
        backed.save()
        # return render(request, "pages/shop.html", context={"error": MSG['Success'][lang_helper(request)]})

    product = Product.objects.all()

    ctx = {
        "root": product
    }
    # print(f"\n\n\n\n{ctx}\n\n\n\n")
    return render(request, "pages/shop.html", ctx)
