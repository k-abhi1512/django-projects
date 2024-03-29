# todo/urls.py
from django.urls import path
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    )
from .views import (
    pending_task_list,
    all_task_list, 
    mark_complete,
    task_create,
    task_update,
    task_delete,
    profile,
    update_profile,
    CustomLogoutView

)

urlpatterns = [
    path('', all_task_list, name='all_task_list'),
    path('pending-tasks/', pending_task_list, name='pending_task_list'),
    path('mark_complete/<int:task_id>/', mark_complete, name='mark_complete'),
    path('task-create', task_create, name='task_create'),
    path('task-update/<int:id>', task_update, name='task_update'),
    path('task-delete/<int:id>', task_delete, name='task_delete'),
    path('user-profile/', profile, name='profile'),
    path('update-profile/', update_profile, name='update_profile'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
