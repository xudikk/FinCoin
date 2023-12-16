from contextlib import closing
from django.conf import settings
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect
from methodism import custom_response, dictfetchone, dictfetchall
from methodism.sqlpaginator import SqlPaginator
from base.custom import permission_checker, admin_permission_checker, mentor_permission_checker
from core.forms.auto import AlgorithmForm, CategoryForm
from core.models import New, Algorithm, Category, Done


@admin_permission_checker
def category(request, pk=None):
    pagination = Category.objects.all().order_by('-pk')
    paginator = Paginator(pagination, settings.PAGINATE_BY)
    page_number = request.GET.get("page", 1)
    paginated = paginator.get_page(page_number)
    ctx = {
        "roots": paginated,
        "pos": "list",
    }

    root = Category.objects.filter(pk=pk).first()
    form = CategoryForm(request.POST or None, instance=root or None)
    if form.is_valid():
        form.save()
        return redirect('category')
    ctx["form"] = form
    ctx['suggest_status'] = "form"

    return render(request, f'pages/ctg.html', ctx)


@mentor_permission_checker
def algaritm(request, key=None, pk=None):
    if key == 'form':
        root = Algorithm.objects.filter(pk=pk).first()
        kwar = {
            'instance': root or None,
            'creator': request.user
        }
        form = AlgorithmForm(request.POST or None, **kwar)
        if form.is_valid():
            form.save()
            return redirect('all_algaritm')
        else:
            print(form.errors)
        return render(request, 'pages/algorithms/algaritm.html',
                      {'key': key, "form": form, })

    all_algaritm = f""" select cor_al.id, cor_al.reward, cor_al.description, cor_al.bonus, (COALESCE(user_c.first_name, '') || ' ' || COALESCE(user_c.last_name, '')) as full_name
                from core_algorithm cor_al
                    left join core_user user_c on cor_al.creator_id == user_c.id
                """
    user = f"""
            select c_user.id, c_user.first_name, c_user.last_name from core_user c_user
            """
    bonuses = "select bonus from core_algorithm"

    with closing(connection.cursor()) as cursor:
        cursor.execute(all_algaritm)
        algarithm = dictfetchall(cursor)

        cursor.execute(user)
        user = dictfetchall(cursor)

        cursor.execute(bonuses)
        bonuses = cursor.fetchall()

    return render(request, 'pages/algorithms/algaritm.html',
                  {"all_algorithm": algarithm, 'key': key, 'user': user,
                   "bonuses": [x[0] for x in bonuses]})


def done_algoritms(request, pk=None):
    if pk:
        Done.objects.create(status="Tekshirilmoqda", user=request.user, algorithm_id=pk)
        return redirect("done_algoritms")
    sql = f"""
        SELECT a.*
        FROM core_algorithm a
        WHERE NOT EXISTS (
          SELECT 1
          FROM core_done d
          WHERE d.algorithm_id = a.id
            AND d.user_id = {request.user.id} and d.status != 'Xato'
        )
    """

    with closing(connection.cursor()) as cursor:
        cursor.execute(sql)
        algorithm = dictfetchall(cursor)

    return render(request, 'pages/algorithms/done_algoritm.html', {"roots": algorithm, })


def mentor_algorithm(request):
    all_mentor_algorithm = f"""
            SELECT ca.id, ca.reward, ca.description, ca.bonus, cu.id user_id, cu.first_name, cu.last_name
            FROM core_algorithm ca
            JOIN core_user cu ON ca.creator_id = cu.id
            WHERE ca.creator_id = {request.user.id} AND cu.ut = 2
        """
    print("Raw Query:", all_mentor_algorithm)
    with closing(connection.cursor()) as cursor:
        cursor.execute(all_mentor_algorithm)
        all_ = dictfetchall(cursor)
        print("Raw Results:", all_)
        ctx = {'all_algorithm': all_}

    return render(request, 'pages/algorithms/mentor_algorithm.html', ctx)
