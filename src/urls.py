#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.contrib import admin
from django.urls import path, include
from core.v1.views import FcMain

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", FcMain.as_view()),
    path("", include("core.urls"))

]
