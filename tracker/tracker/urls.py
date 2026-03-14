from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('assignmenttracker.urls')),
    path('', include('theme.urls')), 
]

if settings.DEBUG:
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ] 
