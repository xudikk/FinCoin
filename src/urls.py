#  Created by Xudoyberdi Egamberdiyev
#
#  Please contact before making any changes
#
#  Tashkent, Uzbekistan

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from core.v1.views import FcMain

from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve

def page_not_found_view(request, exception):
    return render(request, 'pages/abs404.html', context={"error": 404}, status=404)


def error_500(request, *args, **kwargs):
    return render(request, 'pages/abs500.html', context={"error": 500}, status=500)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", FcMain.as_view()),
    path('edu/', include('core.education.urls')),
    path("", include("core.urls"))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]


handler404 = "src.urls.page_not_found_view"
handler500 = "src.urls.error_500"
