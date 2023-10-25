from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from core.models import Product, New
from core.forms.auto import ProductForm, NewForm


@login_required(login_url='sign-in')
def gets(requests, key, pk=None):
    try:
        Model = {
            "news": New,
            "product": Product
        }[key]
    except:
        return render(requests, 'base.html', {"error": 404})
    if pk:
        root = Model.objects.filter(pk=pk).first()
        ctx = {
            "pos": "one",
            'root': root,
        }
        if not root:
            ctx['error'] = 404
    else:
        pagination = Model.objects.all().order_by('-pk')
        paginator = Paginator(pagination, settings.PAGINATE_BY)
        page_number = requests.GET.get("page", 1)
        paginated = paginator.get_page(page_number)

        ctx = {
            "roots": paginated,
            "pos": "list"
        }
    ctx.update({f"{key}_active": "active"})

    return render(requests, f'pages/{key}.html', ctx)


@login_required(login_url='sign-in')
def auto_form(requests, key, pk=None):
    try:
        Model = {
            "news": "New",
            "product": "Product"
        }[key]
    except:
        return render(requests, 'base.html', {"error": 404})
    root = None
    if pk:
        root = eval(Model).objects.filter(pk=pk).first()
        if not root:
            ctx = {"error": 404}
            return render(requests, f'pages/{key}.html', ctx)

    form = eval(f"{Model}Form")(requests.POST or None, requests.FILES or None, instance=root)
    if form.is_valid():
        form.save()
        return redirect('dashboard-auto-list', key=key)

    ctx = {
        "form": form,
        "pos": 'form'
    }
    return render(requests, f'pages/{key}.html', ctx)

