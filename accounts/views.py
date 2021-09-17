from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from accounts.forms import SignUpForm
from django.contrib.auth.models import User
from datetime import datetime
import requests
import json
from django.utils import timezone


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login')
    else:
        form = SignUpForm()
    args = {'form':form}
    return render(request,'registration/signup.html',args)

def profile(request,username):
    uid = User.objects.get(username = username)
    user_info = requests.get('https://api.github.com/users/{}'.format(username)).json()
    uid.profile.followers = user_info['followers']
    repo_info = requests.get('https://api.github.com/users/{}/repos'.format(username)).json()
    repo_json = json.loads('{}')
    repo_dict = {}
    for repo in repo_info:
        repo_dict[repo['name']] = repo['stargazers_count']
    repo_dict = {k: v for k, v in reversed(sorted(repo_dict.items(), key=lambda item: item[1]))}
    for k,v in repo_dict.items():
        repo_json.update({k:v})
    uid.profile.repo_info = repo_json
    uid.save()
    now = timezone.now()
    args = {'username':uid,'time':now}
    return render(request,'profile.html',args)

def explore(request):
    all_users = User.objects.values()
    args = {'all_users':all_users}
    return render(request,'explore.html',args)
    
        
