from contextlib import closing

from django.db import connection
from django.shortcuts import render

from base.helper import cusmot_dictfetchall,custom_dictfetchone
from core.models import Message


def chat(request, user_id=None):
    ctx = {}
    # message = Message.objects.all()
    if user_id:
        sql1 = f"""
        SELECT cm.chat_id, cm.message, cm.media, cm.created, cc.user_id, cu.first_name, cu.last_name, count(cm.id) as 'messege_len' from core_message cm 
        inner join core_chatuser cc 
        on cc.user_id == {user_id}
        INNER join core_user cu 
        on cc.user_id == cu.id 
        """
        with closing(connection.cursor()) as cursor:
            cursor.execute(sql1)
            all1 = cusmot_dictfetchall(cursor)
        ctx = {'messages': all1}
        # return render(request, 'pages/chat/index.html', )

    sql = f"""
            SELECT ccu.user_id, cu.first_name, cu.last_login, cu.last_name, cu.avatar  FROM core_chat cc 
            inner join core_chatuser ccu
            on ccu.user_id == {request.user.id}
            inner join core_user cu 
            on ccu.user_id == cu.id
        """
    chat_data = """
            SELECT cu.first_name, cu.last_name, count(cm.id) as 'messege_len' from core_message cm 
            left join core_chatuser cc  
            on cc.user_id == 9
            INNER join core_user cu 
            on cc.user_id == cu.id 
                """
    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        all = cusmot_dictfetchall(cursor)

        cursor.execute(chat_data)
        data = custom_dictfetchone(cursor)

    ctx["users"] = all
    ctx["chat_data"] = data
    return render(request, 'pages/chat/index.html', ctx)


def chatSearch(request):
    data = request.GET.get('id', 0)
    sql = f"SELECT * FROM core_user cu WHERE LOWER(cu.id) like LOWER('%{data}%') or LOWER(cu.phone) LIKE  lower('%{data}%')"

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        users = cusmot_dictfetchall(cursor)

    return render(request, 'pages/chat/index.html', {"users": users, "key": "search"})
