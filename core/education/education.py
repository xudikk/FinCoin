from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from base.helper import gcnt, get_davomat, check_attendance_makeable
from base.custom import admin_permission_checker, mentor_permission_checker
from core.forms.education import GrStForm, GroupForm, CourseForm, DarsForm
from core.models import GroupStudent, Group, User
from core.models.education import Interested, Course, Dars, Davomat


@admin_permission_checker
def manage_group(requests, group_id=None, status=None, student_id=None, _id=None):
    if status == 201:  # status -> HTTP RESPONSE statuses 201-add, 99-add student, 1,2,3-group statuses
        group = Group.objects.filter(id=group_id).first()
        form = GroupForm(requests.POST or None, instance=group)
        ctx = {"group": group, "form": form, "position": "add", "gr_active": "active"}
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
                ctx = {"group": group, "form": form, "position": "gr", "gr_active": "active"}
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
            "lessons": lessons,
            "gr_active": "active"
        }
        return render(requests, 'pages/education/groups.html', ctx)

    elif status:
        groups = Group.objects.filter(status=status).order_by('-pk')
        ctx = {
            'groups': groups,
            'position': 'list',
            "gr_active": "active"
        }
        return render(requests, 'pages/education/groups.html', ctx)
    ctx = {
        'position': 'main',
        'gcnt': gcnt(),
        "gr_active": "active"
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
            "ints_active": "active"
        }
        return render(requests, 'pages/instres.html', ctx)

    elif contac_id:
        ins = Interested.objects.filter(id=contac_id).first()
        inst = Interested.objects.all().order_by('-pk')
        if not ins:
            ctx = {
                'intres': inst,
                'error': True,
                "ints_active": "active"
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
            "ints_active": "active"
        }

        return render(requests, 'pages/education/instres.html', ctx)


@admin_permission_checker
def manage_course(requests, pk=None, edit_id=None, del_id=None):
    ctx = {"course_active": "active"}
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


@mentor_permission_checker
def manage_lesson(request, group_id, pk=None, status=None):
    root = Dars.objects.filter(pk=pk).first() or None
    group = Group.objects.filter(pk=group_id).first() or None
    if (not root and status is None) or not group:
        return render(request, 'base.html', {'error': 404})

    if not status and root.group != group:
        return render(request, 'base.html', {'error': 404})

    form = DarsForm(request.POST or None, request.FILES or None, instance=root, group=group)
    if form.is_valid():
        root = form.save()
        redirect('education_dars', group_id=group_id, pk=root.id)

    ctx = {
        "form": form,
        "root": root,
        "group_id": group_id,
        "gr_active": "active"
    }
    if root:
        ctx.update({'members': get_davomat(group_id, root.id)})
    if status:
        ctx.update({"status": "form", "group_id": group_id})
    return render(request, "pages/education/dars.html", ctx)


@mentor_permission_checker
def end_lesson(request, lesson_id):  # attends -> davomat
    root = Dars.objects.filter(pk=lesson_id).first()
    if not root:
        return render(request, 'base.html', {'error': 404})
    root.is_end = True
    root.save()
    return redirect('education_dars', group_id=root.group_id, pk=root.id)


@mentor_permission_checker
def attends(request, group_id, dars_id, student_id, status):
    check = check_attendance_makeable(group_id, dars_id, student_id)
    if not check:
        return render(request, 'base.html', {'error': 404})
    if status == "Kemad":
        "Shu yerda userning ota onasiga sms chiqarib yuboriladi."
    Davomat.objects.create(dars_id=dars_id, group_id=group_id, user_id=student_id, status=status)
    return redirect('education_dars', group_id=group_id, pk=dars_id)
