from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile, Tweet
from .forms import TweetForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    tweets = Tweet.objects.all().order_by("-created_at")
    
    return render(request, 'home.html', {"tweets":tweets})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        if request.method == "POST":
            current_user = request.user.profile
            akcja = request.POST['follow']

            if akcja == "unfollow":
                current_user.follows.remove(profile)
                messages.success(request, ("You have unfollowed this user!"))
            else:
                current_user.follows.add(profile)
                messages.success(request, ("You have followed this user!"))
            current_user.save()
        return render(request, "profile.html", {"profile":profile , "tweets":tweets})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')
    

def tweet(request):
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("You successfully tweeted!"))
                return redirect('tweet')
        return render(request, "tweet.html", {"form":form})
    else:
        messages.success(request, ("You must be logged in to view this page!"))
        return redirect('home')
    


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("Invalid username or password!"))
            return redirect('login')
    else:
        return render(request, "login.html")


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm(request.POST)
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username = username, password=password)
            login(request,user)

            messages.success(request, ("You have successfully registered!"))

            return redirect('home')
        
    return render(request, "register.html", {'form':form})