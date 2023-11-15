#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import random
from contextlib import closing

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import redirect, render
from methodism import code_decoder, dictfetchall

from base.custom import permission_checker, admin_permission_checker
from base.helper import generate_number
from core.models import User, Otp, Card
from methodism import generate_key
import uuid


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect("home")

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(phone=data['phone']).first()
        if not user:
            return render(requests, 'pages/auth/login.html', {"error": "Phone xato"})

        if not user.check_password(data['pass']):
            return render(requests, 'pages/auth/login.html', {"error": "Parol xato"})

        if not user.is_active:
            return render(requests, 'pages/auth/login.html', {"error": "Profil active emas "})
        login(requests, user)
        return redirect('home')
    return render(requests, 'pages/auth/login.html')


# def otp(request):
#     if not request.session.get("otp_token"):
#         return redirect("login")
#
#     if request.POST:
#         otp = Otp.objects.filter(key=request.session["otp_token"]).first()
#         code = request.POST['code']
#
#         if not code.isdigit():
#             return render(request, "pages/auth/otp.html", {"error": "Harflar kiritmang!!!"})
#
#         if otp.is_expired:
#             otp.step = "failed"
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Token eskirgan!!!"})
#
#         if (datetime.datetime.now() - otp.created).total_seconds() >= 120:
#             otp.is_expired = True
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Vaqt tugadi!!!"})
#         unhashed = code_decoder(otp.key, decode=True, l=settings.RANGE)
#         unhash_code = eval(settings.UNHASH)
#         if int(unhash_code) != int(code):
#             otp.tries += 1
#             otp.save()
#             return render(request, "pages/auth/otp.html", {"error": "Cod hato!!!"})
#
#         user = User.objects.get(phone=request.session["phone"])
#         otp.step = "logged"
#         login(request, user)
#         otp.save()
#
#         del request.session["user_id"]
#         del request.session["code"]
#         del request.session["phone"]
#         del request.session["otp_token"]
#
#         return redirect("home")
#
#     return render(request, "pages/auth/otp.html")
#
#
# def resent_otp(request):
#     if not request.session.get("otp_token"):
#         return redirect("login")
#
#     old = Otp.objects.filter(key=request.session["otp_token"]).first()
#     old.step = 'failed'
#     old.is_expired = True
#     old.save()
#
#     otp = random.randint(int(f'1{"0" * (settings.RANGE - 1)}'), int('9' * settings.RANGE))
#     # shu yerda sms chiqib ketadi
#     code = eval(settings.CUSTOM_HASHING)
#     hash = code_decoder(code, l=settings.RANGE)
#     token = Otp.objects.create(key=hash, mobile=old.mobile, step='login', extra={"via": "template"})
#
#     request.session['otp_token'] = token.key
#     request.session['code'] = otp
#     request.session['phone'] = token.mobile
#
#     return redirect("otp")
#

@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect("login")


@admin_permission_checker
def clear(request):
    sql = "select number from core_card"
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        cards = cursor.fetchall()
        with open("base/numbers.txt", "w") as file:
            result = ""
            for i in cards:
                result += i[0] + ",\n"
            file.write(result)
    return redirect('home')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


@admin_permission_checker
def create_user(request, status=None, pk=None, type=0):
    if type:
        pagination = User.objects.filter(ut=type)
    else:
        pagination = User.objects.all()
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = request.GET.get("page", 1)
    paginated = paginator.get_page(page_number)
    ctx = {
        "roots": paginated,
        "pos": "list",
        "type": type
    }
    if status == 'form':
        root = User.objects.filter(pk=pk).first()
        form = UserForm(instance=root or None)
        if request.method == "POST":
            if not root:
                data = {
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'phone': request.POST.get('phone'),
                    'gender': request.POST.get('gender'),
                    'level': request.POST.get('level'),
                    "specialty": request.POST.get('specialty'),
                    "username": request.POST.get('username'),
                    "password": request.POST.get('password'),
                    "email": request.POST.get('email'),
                    "ut": type or 3
                }
                user = User.objects.create_user(**data)
                card = Card.objects.create(
                    user=user,
                    number=generate_number(),
                    name=f"Fintech Coin Card",
                    expire=f"{datetime.datetime.now().month}/{str(datetime.datetime.now().year + 1)[2:]}",
                    is_primary=False,
                    card_registered_phone=user.phone,
                    token=uuid.uuid4()
                )
                card.save()
            else:
                root.first_name = request.POST.get('first_name')
                root.last_name = request.POST.get('last_name')
                root.phone = request.POST.get('phone')
                root.gender = request.POST.get('gender')
                root.level = request.POST.get('level')
                root.specialty = request.POST.get('specialty')
                root.username = request.POST.get('username')
                root.email = request.POST.get('email')
                root.save()

            return redirect('user', type=type)

        ctx["form"] = form
        ctx['suggest_status'] = "form"
        if root:
            ctx.update({'editing': True})

    ctx.update({"open_menu_fc": "menu-open"})

    return render(request, f'pages/user.html', ctx)


def change_password(request, user_id):
    if request.user.is_anonymous:
        return redirect('login')
    root = 0
    if request.POST and request.user.ut == 1 or request.user.ut == 3:
        root = User.objects.filter(pk=user_id).first()
        if root and root.ut != 1:
            root.set_password(request.POST.get("password"))
            root.save()
        if root == request.user:
            request.user.set_password(request.POST.get("password"))
            request.user.save()

    return redirect('user', type=3 if not root else root.ut)


@permission_checker
def grader(request, gr, pk):
    root = User.objects.filter(pk=pk).first()
    if not root or request.user.ut != 1:
        return render(request, "base.html", {"error": 404})
    if request.user.ut == 1:
        root.ut = gr
        root.save()
    return redirect('get_user_info', pk=root.id)


@permission_checker
def create_cart(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    if not user:
        return redirect('home')
    card = Card.objects.filter(user=user).first()
    if card:
        return redirect('home')
    card = Card.objects.create(
        user=user,
        number=generate_number(),
        name=f"Fintech Coin Card",
        expire=f"{datetime.datetime.now().month}/{str(datetime.datetime.now().year + 1)[2:]}",
        is_primary=False,
        card_registered_phone=user.phone,
        token=uuid.uuid4()
    )
    card.save()
    return redirect('get_user_info', pk=user_id)
