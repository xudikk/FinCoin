#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan


# Bu faylda Faqatgina Cartalar bilan bog'liq bo'lgan o'tqazma va bonuslar uchun codelar yoziladi. Asosan o'tqazmalar
from contextlib import closing

from django.db import connection
from django.shortcuts import redirect

from base.custom import permission_checker


@permission_checker
def award(request, pk=None):
    if request.POST:
        sql = f"""
            UPDATE core_card 
            set balance = balance + {request.POST.get('reward', 0)}
            {f'where user_id = {pk} ' if pk else ""}
        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)
    if pk:
        return redirect("get_user_info", pk=pk)
    else:
        return redirect("home")
