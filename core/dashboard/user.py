#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
import datetime
import random

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django import forms
from django.shortcuts import redirect, render
from methodism import code_decoder

from base.custom import permission_checker
from base.helper import generate_number
from core.models import User, Otp, Card
from methodism import generate_key
import uuid


def sign_in(requests):
    if not requests.user.is_anonymous:
        return redirect("home")

    if requests.POST:
        data = requests.POST
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return render(requests, 'pages/auth/login.html', {"error": "Username xato"})

        if not user.check_password(data['pass']):
            return render(requests, 'pages/auth/login.html', {"error": "Parol xato"})

        if not user.is_active:
            return render(requests, 'pages/auth/login.html', {"error": "Profil active emas "})
        login(requests, user)
        return redirect('home')
    return render(requests, 'pages/auth/login.html')


@login_required(login_url='login')
def sign_out(request):
    logout(request)
    return redirect("login")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'


@permission_checker
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
        'u_active': "active",
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
                root.save()

            return redirect('user', type=type)

        ctx["form"] = form
        ctx['suggest_status'] = "form"
        if root:
            ctx.update({'editing': True})

    return render(request, f'pages/user.html', ctx)


@permission_checker
def change_password(request, user_id):
    if request.POST and request.user.ut == 1:
        root = User.objects.filter(pk=user_id).first()
        if root and root.ut != 1:
            root.set_password(request.POST.get("password"))
            root.save()
        if root == request.user:
            request.user.set_password(request.POST.get("password"))
            request.user.save()

    return redirect('user')


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

