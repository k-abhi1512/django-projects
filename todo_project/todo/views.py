from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.views import LogoutView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.dispatch import receiver
from django.contrib import messages


from .models import (
    Task,
    UserProfile,
)
from .forms import (
    TaskForm, 
    UserProfileForm
)

from .signals import task_completed_signal


# Create your views here.
@login_required
def pending_task_list(request):
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
        pending_tasks = Task.objects.filter(completed=False)
        return render(request, 'pending-task.html', {'pending_tasks': pending_tasks})


@login_required
def all_task_list(request):
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
        tasks = Task.objects.all()

        # Add pagination
        page = request.GET.get('page', 1)
        paginator = Paginator(tasks, 5)  # Show 5 tasks per page
        try:
            tasks = paginator.page(page)
        except PageNotAnInteger:
            tasks = paginator.page(1)
        except EmptyPage:
            tasks = paginator.page(paginator.num_pages)

        context = {'tasks': tasks}
        return render(request, 'task_list.html', context=context)


@login_required
def mark_complete(request, task_id):
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
        task = get_object_or_404(Task, pk=task_id)
        
        # Toggle the completion status
        task.completed = not task.completed
        task.save()

        # Send the completion signal
        task_completed_signal.send(sender=Task, instance=task)
        try:
            if task.completed == True:
                messages.add_message(request, messages.SUCCESS, f'{task.title}: marked as completed!')
            else:
                messages.add_message(request, messages.INFO, f'{task.title}: Un-marked as completed!')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'{task.title}: Error {str(e)}')
        # Redirect based on the requested URL
        requested_url = request.META.get('HTTP_REFERER')

        if 'pending-tasks' in requested_url:
            return redirect('pending_task_list')
        else:
            return redirect('all_task_list')


# New receiver function to handle the signal
@receiver(task_completed_signal)
def task_completed_handler(sender, instance, **kwargs):
    # Perform actions when a task is marked as complete
    print(f'Task "{instance.title}" marked as completed!')
    # Add your custom logic here, such as sending notifications, etc.
    


@login_required
def task_create(request):  
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
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


@login_required
def task_update(request, id):
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
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

@login_required
def task_delete(request, id):
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
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
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
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
    if not request.user.is_authenticated:
        # Redirect to login or show an appropriate message
        return render(request, 'not_authenticated.html')
    else:
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


class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'logout.html')
        # else:
        #     # Use the default logout template
        #     return super().dispatch(request, *args, **kwargs)

