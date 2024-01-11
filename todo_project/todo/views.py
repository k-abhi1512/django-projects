from django.shortcuts import render, redirect
from .models import Task

# Create your views here.

def pending_task_list(request):
    pending_tasks = Task.objects.filter(completed=False)
    return render(request, 'pending-task.html', {'pending_tasks': pending_tasks})


def all_task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})


def mark_complete(request, task_id):
    task = Task.objects.get(pk=task_id)
    if task.completed != True:
        task.completed = True
    else:
        task.completed = False
    task.save()
    requested_url = request.META.get('HTTP_REFERER')
    requested_url = requested_url.split('/')
    if requested_url[-2] != 'pending-tasks':
        return redirect('all_task_list')
    else:
        return redirect('pending_task_list')
