from django.contrib import admin
from django.urls import include, path
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('assignmenttracker.urls')),
    path('', include('theme.urls')), 
]


if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ] 
