from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_assignment, name='add_assignment'),
    path('create/', views.create_task, name='create_task'),
    path('undo/<int:task_id>/', views.undo_task, name='undo_task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark_done'),
]