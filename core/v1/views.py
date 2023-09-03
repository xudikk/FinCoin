#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan
from django.conf import settings
from methodism import custom_response, MESSAGE, exception_data
from rest_framework.response import Response

from core import v1
from base.custom import CustomMETHODISM, method_checker
from base.helper import lang_helper
from core.models.token import Token
from core.v1 import rget
from re import compile as re_compile


class FcMain(CustomMETHODISM):
    file = v1
    token_key = "FcBearer"
    auth_headers = 'FintechCoin-Authorization'
    token_class = Token
    not_auth_methods = settings.METHODS
    get_methods = rget

    @method_checker
    def get(self, request, *args, **kwargs):
        method = request.GET.get("method")
        headers = request.headers
        if method not in self.not_auth_methods and "*" not in self.not_auth_methods:
            authorization = headers.get(self.auth_headers, '')
            pattern = re_compile(self.token_key + r" (.+)")

            if not pattern.match(authorization):
                return Response(custom_response(status=False, method=method,
                                                message=MESSAGE['NotAuthenticated'][lang_helper(request)]))
            input_token = pattern.findall(authorization)[0]

            # Authorize
            token = self.token_class.objects.filter(key=input_token).first()
            if not token:
                return Response(
                    custom_response(status=False, method=method, message=MESSAGE['AuthToken'][lang_helper(request)]))
            request.user = token.user
        try:
            funk = getattr(self.get_methods, method.replace('.', '_').replace('-', '_'))
        except AttributeError:
            return Response(
                custom_response(False, method=method, message=MESSAGE['MethodDoesNotExist'][lang_helper(request)]))
        except Exception as e:
            return Response(
                custom_response(False, method=method, message=MESSAGE['UndefinedError'][lang_helper(request)],
                                data=exception_data(e)))
        res = map(funk, [request])
        try:
            response = Response(list(res)[0])
            response.data.update({'method': method})
        except Exception as e:
            response = Response(
                custom_response(False, method=method, message=MESSAGE['UndefinedError'][lang_helper(request)],
                                data=exception_data(e)))
        return response
