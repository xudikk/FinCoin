import datetime
import uuid

from django.http import HttpResponse
from django.shortcuts import redirect, render

from base.helper import generate_number
from core.models import Card
from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request,  pk=None):
    try:
        update_user = User.objects.filter(id=pk).first()
        card = Card.objects.filter(user=update_user)
    except Exception as e:
        return render(request, 'base.html', {"error": 404})

    return render(request, 'pages/list.html',
                  {"update_user": update_user, "card_user": card, 'u_active': "active"})
