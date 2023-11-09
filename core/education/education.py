from django.shortcuts import render, redirect

from base.custom import admin_permission_checker, permission_checker_by_ut
from base.helper import gcnt
from core.forms.education import GrStForm, GroupForm, CourseForm
from core.models import GroupStudent, Group
from core.models.education import Interested, Course


@permission_checker_by_ut
def manage_group(requests, group_id=None, status=None, student_id=None, _id=None):
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
        ctx = {
            'group': group,
            "position": "one",
            'members': members
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


@admin_permission_checker
def interested(requests, pk=None, contac_id=None):
    if pk:
        ins = Interested.objects.filter(id=pk).first()
        inst = Interested.objects.all().order_by('-pk')
        if not ins:
            ctx = {
                'intres': inst,
                'error': True,
            }
            return render(requests, 'pages/education/instres.html', ctx)
        ins.view = True
        ins.save()
        ctx = {
            'inst': ins,
            'position': "one",
        }
        return render(requests, 'pages/instres.html', ctx)

    elif contac_id:
        ins = Interested.objects.filter(id=contac_id).first()
        inst = Interested.objects.all().order_by('-pk')
        if not ins:
            ctx = {
                'intres': inst,
                'error': True,
            }
            return render(requests, 'pages/instres.html', ctx)
        ins.contacted = True
        ins.who_contacted = requests.user
        ins.save()
        return redirect('admin-interested')

    else:
        inst = Interested.objects.all().order_by('-pk')
        ctx = {
            'intres': inst,
        }

        return render(requests, 'pages/instres.html', ctx)


@admin_permission_checker
def manage_course(requests, pk=None, edit_id=None, del_id=None):
    ctx = {}
    if del_id:
        course = Course.objects.filter(id=del_id).first()
        if not course:
            return redirect('admin-course')
        course.delete()
        return redirect('admin-course')

    if edit_id or edit_id == 0:
        course = Course.objects.filter(id=edit_id).first()
        form = CourseForm(requests.POST or None, instance=course)
        if form.is_valid():
            form.save()
            return redirect('admin-course')

        return render(requests, 'pages/education/course.html', {"form": form, "position": 'edit'})
    if pk:
        course = Course.objects.filter(pk=pk).first()
        if not course:
            return redirect('admin-course')
        groups = Group.objects.filter(course=course)
        ctx.update({
            'position': 'one',
            'root': course,
            "groups": groups
        })

    else:
        ctx['position'] = 'list'
        ctx['courses'] = Course.objects.all()

    return render(requests, 'pages/education/course.html', ctx)
