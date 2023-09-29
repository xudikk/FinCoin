#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import uuid
from base.helper import generate_number
from core.models import Card
from django.shortcuts import redirect, render


def create_card(request):
    if request.user.ut not in [1, 2] or request.user.is_anonymous:
        return redirect("home")
    if request.method == "POST":
        user = request.user
        now = datetime.datetime.now()
        card = Card.objects.create(
            user=user,
            name=f"{user.full_name()}'s card",
            balance=10_000,
            number=generate_number(),
            token=uuid.uuid4(),
            expire=f"{now.month}/{f'{now.year + 1}'[2:]}",
            is_primary=False,
            card_registered_phone=user.phone
        )
    return render(request, "page", context=card.response())


def all_card(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, "page", context={
        x.response() for x in cards
    })
