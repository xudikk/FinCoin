#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from contextlib import closing

from django.db import connection
from django.shortcuts import redirect, render
from methodism import METHODISM, custom_response, MESSAGE, exception_data
from re import compile as re_compile

from rest_framework.response import Response

from base.helper import lang_helper


def method_params_checker(funk):
    def wrapper(self, req, *args, **kwargs):
        params = req.data.get('params')
        method = req.data.get("method")
        response = {
            not method: Response(
                custom_response(status=False, method=method, message=MESSAGE['MethodMust'][lang_helper(req)])),
            params is None: Response(
                custom_response(status=False, method=method, message=MESSAGE['ParamsMust'][lang_helper(req)]))
        }
        return response.get(True) or funk(self, req, *args, **kwargs)

    return wrapper


def method_checker(funk):
    def wrapper(self, req, *args, **kwargs):
        method = req.GET.get("method", None)
        response = {
            not method: Response(
                custom_response(status=False, method=method, message=MESSAGE['MethodMust'][lang_helper(req)])),
        }
        return response.get(True) or funk(self, req, *args, **kwargs)

    return wrapper


def permission_checker(funk):
    def wrapper(request, *args, **kwargs):
        response = {
            not request.user.is_active: redirect('login'),
            not request.user.is_staff: redirect('login'),
            request.user.is_anonymous: redirect('login'),
        }
        if True in response.keys():
            return response.get(True)

        if request.user.ut != 1:
            return render(request, 'base.html', {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


def admin_permission_checker(funk):
    def wrapper(request, *args, **kwargs):

        if request.user.is_anonymous:
            return redirect('login')
        if 'status' in kwargs and kwargs['status'] == 'bonus':
            return funk(request, *args, **kwargs)
        if request.user.ut != 1:
            return render(request, 'base.html', {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


def mentor_permission_checker(funk):
    def wrapper(request, *args, **kwargs):

        if request.user.is_anonymous:
            return redirect('login')

        if request.user.ut not in [1, 2]:
            return render(request, 'base.html', {'error': 404})

        return funk(request, *args, **kwargs)

    return wrapper


class CustomMETHODISM(METHODISM):

    @method_params_checker
    def post(self, requests, *args, **kwargs):
        method = requests.data.get("method")
        params = requests.data.get("params")
        headers = requests.headers
        if method not in self.not_auth_methods and "*" not in self.not_auth_methods:
            authorization = headers.get(self.auth_headers, '')
            pattern = re_compile(self.token_key + r" (.+)")

            if not pattern.match(authorization):
                return Response(custom_response(status=False, method=method,
                                                message=MESSAGE['NotAuthenticated'][lang_helper(requests)]))
            input_token = pattern.findall(authorization)[0]

            # Authorize
            token = self.token_class.objects.filter(key=input_token).first()
            if not token:
                return Response(
                    custom_response(status=False, method=method, message=MESSAGE['AuthToken'][lang_helper(requests)]))
            requests.user = token.user
        try:
            funk = getattr(self.file, method.replace('.', '_').replace('-', '_'))
        except AttributeError:
            return Response(
                custom_response(False, method=method, message=MESSAGE['MethodDoesNotExist'][lang_helper(requests)]))
        except Exception as e:
            return Response(
                custom_response(False, method=method, message=MESSAGE['UndefinedError'][lang_helper(requests)],
                                data=exception_data(e)))
        res = map(funk, [requests], [params])
        try:
            response = Response(list(res)[0])
            response.data.update({'method': method})
        except Exception as e:
            response = Response(
                custom_response(False, method=method, message=MESSAGE['UndefinedError'][lang_helper(requests)],
                                data=exception_data(e)))
        return response


def user_notification_sender(user_id, note, type, bonus=0, many=False):
    sql = f""" 
            insert into core_usernotification ("type", "desc", bonus, viewed ,user_id)
            {f"select '{type}','{note}','{bonus}',0,id from core_user WHERE ut=3" if many else  f"values ('{type}','{note}','{bonus}',0,'{user_id}')"}
         """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
    # UserNotification.objects.create(**{"user_id": user_id, "type": type, 'bonus': bonus, 'desc': note})
    return True

