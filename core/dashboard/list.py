import datetime
import uuid

from django.http import HttpResponse
from django.shortcuts import redirect, render

from base.helper import generate_number
from core.models import Card
from base.custom import permission_checker, admin_permission_checker
from core.models.auth import User


@admin_permission_checker
def list_user(request, pk=None):
    try:
        update_user = User.objects.filter(id=pk).first()
        card = Card.objects.filter(user=update_user)
        return render(request, 'pages/list.html',
                      {"update_user": update_user, "card_user": card, 'u_active': "active", "card_len": len(card)})
    except Exception as e:
        return render(request, 'pages/abs404.html')
    # return render(request, 'pages/list.html')


def profile(request):
    if request.user.is_anonymous:
        return redirect('login')

    card = Card.objects.filter(user=request.user)
    return render(request, 'sidebars/profile.html', {"card_user": card})


def delCard(request, pk, user):
    try:
        Card.objects.filter(pk=pk).first().delete()
        return redirect("get_user_info", pk=user)
    except Exception as e:
        return render(request, "pages/abs404.html")

    # return render(request, "pages/list.html")
