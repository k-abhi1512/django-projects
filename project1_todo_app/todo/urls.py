from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet

from .views import (
    index_view,
    create_tasks,
    mark_complete,
    pending_task_list,
    TodoFormPageView
)

router = DefaultRouter()
router.register(r'todo', TodoViewSet, basename='todo')


urlpatterns = [
    path('tasks/', index_view, name='todo_index'),
    path('create_tasks/', create_tasks, name='create_task'),
    path('pending-tasks/', pending_task_list, name='pending_task_list'),
    path('mark_complete/<int:task_id>', mark_complete, name='mark_complete'),
    path('', include(router.urls)),
    path('form/', TodoFormPageView.as_view(), name='todo_form'),

]
