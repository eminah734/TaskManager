from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Task
from .forms import NewTaskForm, SignUpForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"tasks": tasks})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')

def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tasks = Task.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_user = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user.follows.remove(profile)
                messages.success(request, "You have unfollowed this user!")
            else:
                current_user.follows.add(profile)
                messages.success(request, "You have followed this user!")
            current_user.save()
        return render(request, "profile.html", {"profile": profile, "tasks": tasks})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')

def addNewTask(request):
    if request.user.is_authenticated:
        form = NewTaskForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                messages.success(request, "You successfully added a new Task!")
                return redirect('home')
        return render(request, "newTask.html", {"form": form})
    else:
        messages.success(request, "You must be logged in to view this page!")
        return redirect('home')

def editTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        form = NewTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect('home')
    else:
        form = NewTaskForm(instance=task)
    return render(request, "editTask.html", {"form": form})

def deleteTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    messages.success(request, "Task deleted successfully!")
    return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "Invalid username or password!")
            return redirect('login')
    else:
        return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('home')

def register_user(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered!")
            return redirect('home')
    return render(request, "register.html", {'form': form})