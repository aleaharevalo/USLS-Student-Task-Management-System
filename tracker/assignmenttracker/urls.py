from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('add/', views.add_assignment, name='add_assignment'),
    path('create/', views.create_task, name='create_task'),
    path('undo/<int:task_id>/', views.undo_task, name='undo_task'),
    path('mark-done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/drop/<int:subject_id>/', views.drop_subject, name='drop_subject'),
    path('logout/', views.logout_view, name='logout'),
]

