import datetime

from django.http import HttpResponse
from django.shortcuts import redirect, render

from base.helper import generate_number
from core.models import Card
from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request, key=None, pk=None):
    users = User.objects.all()
    try:
        update_user = User.objects.filter(id=pk).first()
        card = Card.objects.filter(user=update_user)
    except Exception as e:
        HttpResponse("Xatolik yuzaga keldi >", e)
    if key == 'create':
        if request.method == 'POST':
            data = request.POST
            user_type = data.get("ut")
            gender = data.get('gender')

            user1 = User.objects.filter(phone=data["phone"]).first()
            if user1:
                return redirect('user_list', {"error": "Bu raqam band qilingan"})

            user = User.objects.create_user(
                phone=data["phone"], password=data["pass"],
                first_name=data["name"], gender=gender,
                email=data["email"], ut=user_type
            )
            user.save()
            card = Card.objects.create(
                user=user,
                number=generate_number(),
                name=f"{user.full_name()}'s card",
                balance=0.0,
                expire=f"{datetime.datetime.now().month}/{str(datetime.datetime.now().year + 1)[2:]}",
                is_primary=False,
                card_registered_phone=user.phone
            )
            card.save()
            return redirect('user_list')
    if key == 'edit':
        if request.method == 'POST':
            data = request.POST
            user_type = data.get("ut")
            update_user.first_name = data["name"]
            update_user.email = data["email"]
            update_user.ut = user_type
            update_user.phone = data["phone"]

            update_user.save()
            return redirect('user_list')
    if key == '_info':
        pass
    return render(request, 'pages/list.html',
                  {'roots': users, "update_user": update_user, "card_user": card, "key": key, 'u_active': "active"})
