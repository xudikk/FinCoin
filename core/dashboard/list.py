import datetime

from django.shortcuts import redirect, render
from core.models.monitoring import Card
from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request):
    users = User.objects.all()
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # for i in users:
    #     print(i.phone)
    return render(request, 'pages/list.html', {'roots': users, 'u_active': "active"})


def create_user(request):
    if request.method == 'POST':
        data = request.POST
        nott = "phone" if "phone" not in data else "name" if "name" not in data \
            else "surname" if "surname" not in data else "email" if "email" not in data \
            else "pass" if "pass" not in data else "pass_conf" if "pass_conf" not in data \
            else "username" if "username" not in data else "ut" if "ut" not in data else ""

        if nott:
            return render(request, "pages/create-user.html", {"error": f"{nott} datada bo'lishi kerak"})
        user1 = User.objects.filter(phone=data["phone"]).first()
        if user1:
            return render(request, "pages/create-user.html", {"error": "Phone Band"})
        if data["pass"] != data["pass_conf"]:
            return render(request, "pages/create-user.html", {"error": "Password not confirmed"})
        user = User.objects.create_user(
            phone=data["phone"], password=data["pass"],
            first_name=data["name"], last_name=data["surname"],
            email=data["email"], username=data["username"], ut=data["ut"]
        )
        user.save()
        card = Card.objects.create(
            user=user,
            name=f"{user.full_name}'s card",
            balance=0.0,
            expire=f"{datetime.datetime.now().month}/{datetime.datetime.now().year}",
            is_primary=True
        )
        card.save()
    return render(request, 'pages/create-user.html')
