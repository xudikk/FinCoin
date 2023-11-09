from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from base.errors import MSG
from base.helper import lang_helper
from core.models import Product
from core.models.core import Backed


@login_required(login_url='login')
def savat(request):
    if request.method == "POST":
        params = request.POST
        product = Product.objects.filter(id=params['product_id']).first()
        if not product:
            return render(request, "pages/shop.html", context={"error": MSG['NotData'][lang_helper(request)]})
        print(request.POST)
        backed = Backed.objects.get_or_create(product=product, user=request.user, order=False)[0]
        backed.view = False
        backed.save()
        if "extra" in request.POST:
            backed.quantity = backed.quantity + int(params.get('quentity', backed.quantity))
        else:
            backed.quantity = params.get('quentity', backed.quantity)
        backed.save()
        request.session['ordered'] = True
    else:
        try:
            del request.session['ordered']
        except:
            pass

    product = Product.objects.all().order_by("-pk")
    ctx = {
        "root": product
    }
    return render(request, "pages/shop.html", ctx)
