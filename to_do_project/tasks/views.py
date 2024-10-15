from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Task
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# @login_required was added to the task_list, add_task delete_task to make sure that unauthorized users cannot manipulate tasks leading to data breaches or loss
@login_required
def task_list(request):
    tasks =Task.objects.all()
    return render(request,"task_list.html", {"tasks": tasks})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            Task.objects.create(title=title)
            return redirect("task_list")
        
    return render(request, "add_task.html")

@login_required
def delete_task (request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect("task_list")
