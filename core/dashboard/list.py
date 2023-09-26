import datetime

from django.shortcuts import redirect, render

from base.helper import generate_number
from core.models.monitoring import Card
from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request):
    users = User.objects.all()
    
    return render(request, 'pages/list.html', {'roots': users, 'u_active': "active"})


def create_user(request):
    if request.method == 'POST':
        data = request.POST

        nott = "name" if "name" not in data else "surname" if "surname" not in data \
            else "username" if "username" not in data else "email" if "email" not in data \
            else "phone" if "phone" not in data else "pass" if "pass" not in data \
            else "pass_conf" if "pass_conf" not in data else ""
        user_type = data.get("ut")
        gender = data.get('gender')

        if nott:
            return render(request, "pages/create-user.html", {"error": f"{nott} datada bo'lishi kerak"})

        user1 = User.objects.filter(phone=data["phone"]).first()
        if user1:
            return render(request, "pages/create-user.html", {"error": "Phone Band"})
        if data["pass"] != data["pass_conf"]:
            return render(request, "pages/create-user.html", {"error": "Password not confirmed"})
        user = User.objects.create_user(
            phone=data["phone"], password=data["pass"],
            first_name=data["name"], last_name=data["surname"], gender=gender,
            email=data["email"], username=data["username"], ut=user_type
        )
        user.save()
        # print("1")
        card = Card.objects.create(
            user=user,
            number=generate_number(),
            name=f"{user.full_name()}'s card",
            balance=0.0,
            expire=f"{datetime.datetime.now().month}/{str(datetime.datetime.now().year+1)[2:]}",
            is_primary=False,
            card_registered_phone=user.phone
        )
        card.save()
        # print(card.user.first_name, ">>>>>>>>>", card.number)
        # print("here")
        return redirect('user_list')
    return render(request, 'pages/create-user.html')

