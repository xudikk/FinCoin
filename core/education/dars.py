from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from base.custom import mentor_permission_checker
from base.helper import gcnt
from core.forms.education import GroupForm, GrStForm
from core.models import Group, GroupStudent, Dars, Interested, Davomat


@mentor_permission_checker
def manage_group_mentor(requests, group_id=None, status=None, student_id=None, _id=None):
    if status == 201:  # status -> HTTP RESPONSE statuses 201-add, 99-add student, 1,2,3-group statuses
        group = Group.objects.filter(id=group_id).first()
        form = GroupForm(requests.POST or None, instance=group)
        ctx = {"group": group, "form": form, "position": "add"}
        if form.is_valid():
            form.save()
            return redirect('admin-group-one', group_id=group_id)
        else:
            for i, j in form.errors.items():
                ctx['error'] = i
                break
        return render(requests, 'pages/education/groups.html', ctx)

    elif group_id:
        group = Group.objects.filter(id=group_id).first()
        if group:
            if student_id:
                gs = GroupStudent.objects.filter(group=group, student_id=student_id).first()
                None if not gs else gs.delete()
            elif status == 99:
                form = GrStForm(requests.POST or None, group=group)
                ctx = {"group": group, "form": form, "position": "gr"}
                if form.is_valid():
                    form.save()
                    return redirect('admin-group-one', group_id=group_id)
                else:
                    for i, j in form.errors.items():
                        ctx['error'] = i
                        break
                return render(requests, 'pages/education/groups.html', ctx)

        queryset = GroupStudent.objects.select_related('group').filter(group=group)
        members = [x.student for x in queryset]
        lessons = Dars.objects.filter(group_id=group_id).order_by('-pk')
        paginator = Paginator(lessons, 40)
        page_number = requests.GET.get("page", 1)
        lessons = paginator.get_page(page_number)
        ctx = {
            'group': group,
            "position": "one",
            'members': members,
            "lessons": lessons
        }
        return render(requests, 'pages/education/groups.html', ctx)

    elif status:
        groups = Group.objects.filter(status=status).order_by('-pk')
        ctx = {
            'groups': groups,
            'position': 'list',
        }
        return render(requests, 'pages/education/groups.html', ctx)
    ctx = {
        'position': 'main',
        'gcnt': gcnt(),
    }
    return render(requests, 'pages/education/groups.html', ctx)
