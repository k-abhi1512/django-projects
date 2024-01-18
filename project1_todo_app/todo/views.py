from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views import View

from .models import (
    Tasks
)
from .forms import TaskForm
# Create your views here.

def task_form(request):
    tasks_form = TaskForm()
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()

    context = {
        'task_form': tasks_form
    }
    return render(request, 'task_form.html', context=context)


def index_view(request):
    tasks = Tasks.objects.all()
    context = {
        'tasks' : tasks
    }
    return render(request, 'index.html', context=context)


def particular_item(request, task_id):
    tasks = Tasks.objects.filter(id=task_id)

    return HttpResponse(f"the task is: {tasks.first()}")


def update_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    task.title = 'Updated task'
    task.save()
    return redirect('todo_index')


def delete_task(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    task.delete()
    return redirect('todo_index')


def create_tasks(request):
    if request.method == 'POST':
        print(request.POST)
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
        # try:
        #     title = request.POST.get('title')
        #     completed = request.POST.get('completed')
        #     if completed is not None and (completed == 'on'):
        #         completed = True
        #     else:
        #         completed = False
        #     new_task = Tasks(title=title, completed=completed)
        #     new_task.save()
        # except Exception as e:
        #     print("Exception Occured : ", str(e))

    task_form = TaskForm()
    context = {
        'task_form':task_form
    }

    return render(request, 'create-tasks.html', context=context)


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
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import (
    TodoSerializer,
    TodoFormSerializer
)
from rest_framework.decorators import action

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TodoSerializer

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        try:
            if task.completed != True:
                task.completed = True
            else:
                task.completed = False
            task.save()
            serialised_item = self.get_serializer(task)

            return Response(serialised_item.data, status=status.HTTP_200_OK)
        except Exception as KeyError:
            return Response({'details':'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            return Response({'details':'Error'}, status=status.HTTP_404_NOT_FOUND)



# class TodoFormPageView(View):
#     template_name = 'todo_form.html'

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)
