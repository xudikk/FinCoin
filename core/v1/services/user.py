#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from base.errors import MSG
from base.helper import lang_helper
from methodism.helper import custom_response, exception_data
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


def set_lang(request, params):
    if not params.get('lang', False) or params.get("lang") not in ['uz', 'ru', 'en']:
        return custom_response(False, message=MSG['Lang'][request.user.lang])
    request.user.lang = params['lang']
    request.user.save()
    return custom_response(True, data=MSG['SuccessLangChanged'][lang_helper(request)],
                           message=MSG['Success'][lang_helper(request)])


def user_info(request):
    return custom_response(True, data=request.user.personal(), message=MSG['Success'][lang_helper(request)])


def check_pass(request, params):
    if 'password' not in params or 'uuid' not in params:
        return custom_response(False, message=MSG['ParamsNotFull'][lang_helper(request)])

    if not request.user.check_password(params['password']):
        return custom_response(False, message=MSG['PasswordError'][lang_helper(request)])

    return custom_response(True, data={'access': True}, message=MSG['Success'][lang_helper(request)])


def change_pass(request, params):
    if 'password' not in params: return custom_response(False, message=MSG['ParamsNotFull'][lang_helper(request)])
    request.user.set_password(params['password'])
    request.user.save()
    return custom_response(True, data={'success': True}, message=MSG['Success'][lang_helper(request)])


def user_edit(request, params):
    try:
        ser = UserSerializer(data=params, instance=request.user, partial=True)
        ser.is_valid()
        user = ser.save()
        return custom_response(True, data=user.personal(), message=MSG['Success'][lang_helper(request)])
    except Exception as e:
        return custom_response(False, data=exception_data(e), message=MSG['UndefinedError'][lang_helper(request)])
