from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

from .views import (
    index_view,
    create_tasks,
    mark_complete,
    pending_task_list,
    particular_item,
    update_task,
    delete_task,
    task_form
    # TodoFormPageView
)

router = DefaultRouter()
router.register(r'todo', TodoViewSet, basename='todo')


urlpatterns = [
    path('tasks/', index_view, name='todo_index'),
    path('create_tasks/', create_tasks, name='create_task'),
    path('pending-tasks/', pending_task_list, name='pending_task_list'),
    path('mark_complete/<int:task_id>', mark_complete, name='mark_complete'),
    path('particular_item/<int:task_id>', particular_item, name='particular_item'),
    path('update_task/<int:task_id>', update_task, name='update_task'),
    path('delete_task/<int:task_id>', delete_task, name='delete_task'),
    path('task_form/', task_form, name='task_form'),

    
    path('', include(router.urls))

]
