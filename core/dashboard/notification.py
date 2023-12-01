from contextlib import closing

from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect
from methodism import dictfetchall

from base.custom import admin_permission_checker, user_notification_sender
from core.models import Backed, Done, Card
from core.models.monitoring import UserNotification


@admin_permission_checker
def notification(request, status=None):
    ctx = {'status': status}
    if status == 'done_algorithm':
        all_done = f"""
                select cd.id done_id, cd.status, cu.first_name , cu.last_name, cu.username, cu.phone, cd.algorithm_id algorithm_id, cd.view
                from core_done cd, core_user cu
                where cd.user_id == cu.id
                order by cd.id desc                

            """

        with closing(connection.cursor()) as cursor:
            cursor.execute(all_done)
            _all_ = dictfetchall(cursor)

            paginator = Paginator(_all_, 10)
            page_number = request.GET.get("page", 1)
            paginated = paginator.get_page(page_number)

            ctx.update({
                'all_done': paginated
            })
        viewed = Done.objects.filter(view=False)
        if viewed:
            for _i_ in viewed:
                _i_.view = True
                _i_.save()
        return render(request, f'pages/notifications/all.html', ctx)
    elif status == 'backed':
        all_backed = f"""
        select COALESCE((select 1 from core_card WHERE cb.cost < card.balance), 0) as may_order,
               cb.id backed_id,
               cb.quantity soni,
               cb.'order',
               cb.cost,
               cu.first_name, 
               cu.last_name, 
               cu.username, 
               cu.phone,
               cb.'view', 
               cu.id as user_id, 
               cp.name product_name
        from core_backed cb, core_user cu, core_product cp 
        inner join core_card card on card.user_id = cu.id 
        where cb.user_id == cu.id and cb.product_id == cp.id
        order by cb.id desc
        """

        with closing(connection.cursor()) as cursor:

            cursor.execute(all_backed)
            all_ = dictfetchall(cursor)

            paginator = Paginator(all_, 10)
            page_number = request.GET.get("page", 1)
            paginated = paginator.get_page(page_number)

            ctx.update({
                'all_backed': paginated,
            })

        viewed = 'update core_backed set "view" = 1  WHERE "view" = 0'
        with closing(connection.cursor()) as cursor:
            cursor.execute(viewed)

        return render(request, f'pages/notifications/all.html', ctx)
    elif status == 'bonus':
        all_ = UserNotification.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(all_, 50)
        page_number = request.GET.get("page", 1)
        paginated = paginator.get_page(page_number)
        ctx.update({
            'bonuses': paginated,
        })
        all_.filter(viewed=False).update(viewed=True)

    return render(request, f'pages/notifications/all.html', ctx)


@admin_permission_checker
def done_action(request, status=None, action=None, pk=None):
    if status == 'done_algorithm':
        model = Done.objects.filter(id=pk).first()
        if not model:
            return redirect('notifications')

        if action == 1:
            model.status = "Muaffaqiyatli"
            card = Card.objects.filter(user=model.user).first()
            card.balance += model.algorithm.reward
            card.save()
            user_notification_sender(card.user_id, "Bajarilgan Algoritm uchun bonus", "Bonus", bonus= model.algorithm.reward)
            model.save()
            return redirect('notification_status', status='done_algorithm')
        else:
            model.status = model.status_choices.get(action, 'Bajarilmoqda')
            model.save()
            return redirect('notification_status', status='done_algorithm')
    else:
        return redirect('notifications')


@admin_permission_checker
def backed_action(request, status=None, pk=None):
    if status == 'backed':
        model = Backed.objects.filter(id=pk).first()
        if not model:
            return redirect('notifications')
        model.order = True
        model.save()

    return redirect('notification_status', status=status)
