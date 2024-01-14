from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from .models import (
    Tasks
)
# Create your views here.

def index_view(request):
    tasks = Tasks.objects.all()
    context = {
        'tasks' : tasks
    }
    return render(request, 'index.html', context=context)


def create_tasks(request):
    return HttpResponse(f"Please Create You Task")


def pending_task_list(request):
    pending_tasks = Tasks.objects.filter(completed=False)
    return render(request, 'pending-task.html', {'pending_tasks': pending_tasks})


def mark_complete(request, task_id):
    task = Tasks.objects.get(pk=task_id)
    if task.completed != True:
        task.completed = True
    else:
        task.completed = False
    task.save()
    requested_url = request.META.get('HTTP_REFERER')
    requested_url = requested_url.split('/')
    if requested_url[-2] != 'pending-tasks':
        return redirect('todo_index')
    else:
        return redirect('pending_task_list')





# views.py
from rest_framework import viewsets, generics
from .serializers import (
    TodoSerializer,
    TodoFormSerializer
)

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TodoSerializer


class TodoFormPageView(View):
    template_name = 'todo_form.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
