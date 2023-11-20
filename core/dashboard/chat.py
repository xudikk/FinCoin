from contextlib import closing

from django.contrib.auth.decorators import login_required
from django.db import connection
from django.shortcuts import render

from base.helper import cusmot_dictfetchall, custom_dictfetchone
from core.models import Message


@login_required(login_url="login")
def chat(request, user_id=None):
    ctx = {}
    # message = Message.objects.all()
    if user_id:
        sql1 = f"""
                SELECT * FROM core_message cm 
                inner join core_chatuser ccu 
                on ccu.user_id == {request.user.id}         
                inner join core_chat cc 
                on cc.id == ccu.chat_id 
                GROUP by cm.id 
            """

        # chat_data = f"""
        #         SELECT cu.first_name, cu.last_name, LENGTH(cm.id) as 'messege_len', cu.* from core_message cm
        #         left join core_chatuser cc
        #         on cc.user_id == {request.user.id}
        #         INNER join core_user cu
        #         on cc.user_id == cu.id
        #         """

        with closing(connection.cursor()) as cursor:
            cursor.execute(sql1)
            all1 = cusmot_dictfetchall(cursor)

            # cursor.execute(chat_data)
            # data = custom_dictfetchone(cursor)
        print(all1)
        print(request.user.id)
        ctx = {'messages': all1, "chat_data": all1[0]}

        # print(all1)
        # return render(request, 'pages/chat/index.html', )

    sql = f"""
            SELECT cu.*, chat.id as chat_id, cu.id as user_id FROM core_chatuser cc 
            inner join core_chat chat
            on cc.chat_id == chat.id and cc.user_id == {request.user.id}
            INNER join core_chatuser cc2 
            on chat.id == cc2.chat_id 
            INNER join core_user cu 
            on cc2.user_id == cu.id
            WHERE cu.id != {request.user.id}
            group by cu.id
        """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        all = cusmot_dictfetchall(cursor)
    print(all)
    ctx["users"] = all
    return render(request, 'pages/chat/index.html', ctx)


def chatSearch(request):
    data = request.GET.get('id', 0)
    sql = f"SELECT *, cu.id as user_id FROM core_user cu WHERE LOWER(cu.id) like LOWER('%{data}%') or LOWER(cu.phone) LIKE  lower('%{data}%')"

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        users = cusmot_dictfetchall(cursor)

    return render(request, 'pages/chat/index.html', {"users": users, "key": "search"})
