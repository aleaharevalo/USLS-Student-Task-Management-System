from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_assignment, name='add_assignment'),
    path('undo/<int:task_id>/', views.undo_task, name='undo_task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('task/update-note/<int:task_id>/', views.update_task_note, name='update_task_note'),
    path('subjects/drop/<int:subject_id>/', views.drop_subject, name='drop_subject'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('logout/', views.logout_view, name='logout'),
]

