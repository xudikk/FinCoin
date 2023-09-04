from django.shortcuts import redirect, render

from base.custom import permission_checker
from core.models.auth import User


@permission_checker
def list_user(request):
    users = User.objects.all()
    return render(request, 'pages/list.html', {'roots': users, 'u_active': "active"})
