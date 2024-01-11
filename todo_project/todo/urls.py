# todo/urls.py
from django.urls import path
from .views import (
    pending_task_list,
    all_task_list, 
    mark_complete,
)

urlpatterns = [
    path('', all_task_list, name='all_task_list'),
    path('pending-tasks/', pending_task_list, name='pending_task_list'),
    path('mark_complete/<int:task_id>/', mark_complete, name='mark_complete'),
]
