from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import (
    Task,
    UserProfile,
)
from .forms import (
    TaskForm, 
    UserProfileForm
)

# Create your views here.

def pending_task_list(request):
    pending_tasks = Task.objects.filter(completed=False)
    return render(request, 'pending-task.html', {'pending_tasks': pending_tasks})


def all_task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'task_list.html', context=context)


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
    

def task_create(request):  
    if request.method == "POST":  
        import pdb
        pdb.set_trace()
        task_form = TaskForm(request.POST, request.FILES)  
        if task_form.is_valid():  
            try:  
                task_form.save() 
                model = task_form.instance
                form_submitted = True
            except:  
                form_submitted = False
        else:
            form_submitted = False
    else:  
        task_form = TaskForm()
        form_submitted = False
    return render(request,'create-task.html',{'task_form':task_form, 'form_submitted':form_submitted}) 



def task_update(request, id):
    task = get_object_or_404(Task, pk=id)
    form_submitted = False

    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task_form.save()
            form_submitted = True
    else:
        task_form = TaskForm(instance=task)

    return render(request, 'update-task.html', {'task_form': task_form, 'form_submitted': form_submitted})


def task_delete(request, id):
    task = Task.objects.get(id=id)
    try:
        task.delete()
    except:
        pass
    return redirect('all_task_list')


def login(request):
    return HttpResponse("Please log in to app.")

@login_required(login_url='/login/')
def profile(request):
    user = request.user

    try:
        user_data = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return HttpResponse("UserProfile not found for the current user.")

    context = {
        'user_data': user_data
    }
    return render(request, 'profile.html', context=context)


@login_required
def update_profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    form_submitted = False
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if user_form.is_valid():
            user_form.save()
            form_submitted = True
    else:
        user_form = UserProfileForm(instance=user_profile)
        form_submitted = False

    context = {
            'user_form': user_form, 
            'user': user,
            'form_submitted': form_submitted
        }
    return render(request, 'update-profile.html', context=context)

