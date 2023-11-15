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
        backed = Backed.objects.get_or_create(product=product, user=request.user, order=False)
        print(backed)
        backed[0].view = False
        backed[0].save()
        if "extra" in request.POST and not backed[1]:
            backed[0].quantity = backed[0].quantity + int(params.get('quentity'))
        else:
            backed[0].quantity = params.get('quentity', backed[0].quantity)
        backed[0].save()
        request.session['ordered'] = True
    else:
        try:
            del request.session['ordered']
        except:
            pass

    product = Product.objects.all().order_by("-pk")
    ctx = {
        "root": product,
        'shop_active': 'active'
    }
    return render(request, "pages/shop.html", ctx)
