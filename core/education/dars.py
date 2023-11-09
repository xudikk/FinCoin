from django.shortcuts import render, redirect

from core.models import Group, Dars


def dars(request, group_id=None, status=None):
    group = Dars.objects.filter(group_id=group_id)
    ctx = {"roots": group, 'status': status, "group_id": group_id}
    if status == 'posted':
        if request.method == 'POST':
            data = request.POST
            Dars.objects.create(
                group_id=group_id,
                topic=data['topic'],
                startedTime=data['start'],
                endedTime=data['end']
            )
            return redirect('dars', group_id)
        return render(request, 'pages/education/dars.html', ctx)
    return render(request, 'pages/education/dars.html', ctx)
