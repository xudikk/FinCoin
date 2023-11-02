from contextlib import closing

from django.conf import settings
from django.contrib.auth import logout
from django.db import connection
from methodism import dictfetchone, dictfetchall


def user_type(request):
    if not request.user.is_active:
        logout(request)

    try:
        types = {
            1: ["pages/owner/main.html", "sidebars/admin.html"],
            2: ["pages/teacher/main.html", "sidebars/mentor.html"],
            3: ["pages/default_user/main.html", "sidebars/student.html"],

        }.get(request.user.ut, ["pages/default_user/main.html", "sidebars/student.html"])
    except:
        types = ["pages/default_user/main.html", "sidebars/student.html"]
    ctx = {
        "pages_html_type": types,
        'app_name': settings.APP_NAME
    }
    if not request.user.is_anonymous:
        ctx.update({'user_type': request.user.ut})
    return ctx


