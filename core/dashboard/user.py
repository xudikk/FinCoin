#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.shortcuts import render

from base.errors import MSG
from base.helper import lang_helper
from methodism.helper import custom_response, exception_data
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


def set_lang(request, lang):
    if not lang or lang not in ['uz', 'ru', 'en']:
        return render(request, "page", context=MSG['LangError'][request.user.lang])
    request.user.lang = lang
    request.user.save()
    return render(request, "page", context=MSG['SuccessLangChanged'][lang_helper(request)])


def user_info(request):
    return render(request, "page", context=request.user.personal())


def password(request, key):
    if key == "check_pass":
        if request.method == "POST":
            params = request.POST
            if 'password' not in params:
                return render(request, "page", context=MSG['ParamsNotFull'][lang_helper(request)])
            if not request.user.check_password(params['password']):
                return render(request, "page", context=MSG['PasswordError'])
            return render(request, "page", context={
                'access': True
            })
    elif key == "set_pass":
        if request.method == "POST":
            params = request.POST
            if 'password' not in params:
                return render(request, "page", context=MSG['ParamsNotFull'][lang_helper(request)])
            request.user.set_password(params['password'])
            request.user.save()
            return render(request, "page", context={
                'success': True
            })
    return render(request, "page")



# def user_edit(request, params):
#     try:
#         ser = UserSerializer(data=params, instance=request.user, partial=True)
#         ser.is_valid()
#         user = ser.save()
#         return custom_response(True, data=user.personal(), message=MSG['Success'][lang_helper(request)])

#     except Exception as e:
#         return custom_response(False, data=exception_data(e), message=MSG['UndefinedError'][lang_helper(request)])


