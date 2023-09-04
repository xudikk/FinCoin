#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required(login_url='login')
def index(request):
    return render(request, 'pages/index.html', {'active': "active"})
