from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from base.custom import mentor_permission_checker
from base.helper import gcnt
from core.forms.education import GroupForm, GrStForm
from core.models import Group, GroupStudent, Dars, Interested, Davomat, Course


@mentor_permission_checker
def manage_group_mentor(requests, group_id=None, status=None, _id=None):
    if group_id:
        group = Group.objects.filter(id=group_id).first()
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
        groups = Group.objects.filter(status=status, course__mentor=requests.user.id).order_by('-pk')

        ctx = {
            'groups': groups,
            "gr_active": "active",
            'position': 'list',
        }
        return render(requests, 'pages/education/groups.html', ctx)
    course = Course.objects.filter(mentor_id=requests.user.id).first() or None
    ctx = {
        'position': 'main',
        'gcnt': gcnt(course_id=None if not course else course.id),
        "gr_active": "active",
    }
    return render(requests, 'pages/education/groups.html', ctx)
