from django.shortcuts import redirect, render

from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request):
    users = User.objects.all()
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>")
    # for i in users:
    #     print(i.phone)
    return render(request, 'pages/list.html', {'roots': users, 'u_active': "active"})
