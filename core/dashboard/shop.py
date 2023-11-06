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

        backed = Backed.objects.create(product=product, user=request.user)
        backed.quantity = params.get('quentity', backed.quantity)
        backed.save()
        return redirect('shop')
    product = Product.objects.all()

    ctx = {
        "root": product
    }
    # print(f"\n\n\n\n{ctx}\n\n\n\n")
    return render(request, "pages/shop.html", ctx)
