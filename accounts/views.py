from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from accounts.forms import SignUpForm
from django.contrib.auth.models import User
from datetime import datetime
import requests
import json
from django.utils import timezone
from .models import Profile,Repository
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            repo_info = requests.get('https://api.github.com/users/{}/repos'.format(username)).json()
            for repo in repo_info:
                Repository.objects.create(name=repo['name'],stars=repo['stargazers_count'],user=User.objects.get(username = username).profile)
            user_info = requests.get('https://api.github.com/users/{}'.format(username)).json()
            user = User.objects.get(username=username)
            user.profile.avatar = user_info['avatar_url']
            user.profile.time_inof = str(datetime.now().strftime("%m/%d/%Y, %H:%M"))
            user.save()
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
    args = {'form':form}
    return render(request,'registration/signup.html',args)

@login_required
def profile(request,username):
    uid = User.objects.get(username = username)
    user_info = requests.get('https://api.github.com/users/{}'.format(username)).json()
    uid.profile.followers = user_info['followers']
    repos = uid.profile.repository_set.all()
    repo_dict = {}
    for repo in repos:
        repo_dict[repo.name] = repo.stars
    repo_dict = {k: v for k, v in reversed(sorted(repo_dict.items(), key=lambda item: item[1]))}
    uid.save()
    args = {'username':uid,'repos':repo_dict}
    return render(request,'profile.html',args)

@login_required
def explore(request):
    all_users = User.objects.all()
    args = {'all_users':all_users}
    return render(request,'explore.html',args)

@login_required
def update(request):
    request.user.profile.repository_set.all().delete()
    repo_info = requests.get('https://api.github.com/users/{}/repos'.format(request.user.username)).json()
    for repo in repo_info:
        Repository.objects.create(name=repo['name'],stars=repo['stargazers_count'],user=request.user.profile)
    request.user.profile.time_inof = str(datetime.now().strftime("%m/%d/%Y, %H:%M"))
    repos = request.user.profile.repository_set.all()
    args = {'username':request.user,'repos':repos}
    user_info = requests.get('https://api.github.com/users/{}'.format(request.user.username)).json()
    request.user.profile.avatar = user_info['avatar_url']
    request.user.save()
    return redirect('profile',username=request.user.username)

    
        
