# todo/urls.py
from django.urls import path
from .views import (
    pending_task_list,
    all_task_list, 
    mark_complete,
    task_create,
    task_update,
    task_delete

)

urlpatterns = [
    path('', all_task_list, name='all_task_list'),
    path('pending-tasks/', pending_task_list, name='pending_task_list'),
    path('mark_complete/<int:task_id>/', mark_complete, name='mark_complete'),
    path('task-create', task_create, name='task_create'),
    path('task-update/<int:id>', task_update, name='task_update'),
    path('task-delete/<int:id>', task_delete, name='task_delete'),
]
