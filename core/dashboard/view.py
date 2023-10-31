#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from base.custom import admin_permission_checker
from core.forms.auto import AlgorithmForm
from core.models import Algorithm, User, Card, New


@login_required(login_url='login')
def index(request, pk=None):
    if request.user.ut == 3:
        if pk:
            root = New.objects.filter(pk=pk).first()
            ctx = {
                "pos": "one",
                'root': root,
            }
            if not root:
                ctx['error'] = 404
        else:
            pagination = New.objects.all().order_by('-pk')
            paginator = Paginator(pagination, settings.PAGINATE_BY)
            page_number = request.GET.get("page", 1)
            paginated = paginator.get_page(page_number)
            all_algo = Algorithm.objects.all()
            ctx = {
                "all_algo": all_algo,
                "all_news": paginated,
            }
            return render(request, 'pages/index.html', ctx)
    return render(request, 'pages/index.html', {'active': "active"})

