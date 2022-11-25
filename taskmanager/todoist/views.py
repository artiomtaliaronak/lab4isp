from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import CreateUserForm, LoginForm, CreateTaskForm, UpdateUserForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from .models import Task

from .models import *

import logging

from threading import Thread

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs.txt", level=logging.INFO)


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

# Create your views here.

def home(request):
    logger.info('homepage opened')
    return render(request, 'index.html')

#CRUD-CREATE
@start_new_thread
@login_required(login_url='login')
def createTask(request):
    
    form = CreateTaskForm()

    if request.method == 'POST':

        form = CreateTaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()
            logger.info('task created by {}' .format(request.user.username))
            return redirect('viewtasks')

    context = {'form':form}

    return render(request, 'profile/createtask.html', context=context)

#CRUD-READ
@login_required(login_url='login')
def viewTasks(request):
    
    current_user = request.user.id

    task = Task.objects.all().filter(user=current_user)

    context= {'task':task}
    logger.info('tasks viewed by {}' .format(request.user.username))
    return render(request, 'profile/viewtasks.html', context=context)

#CRUD-UPDATE
@start_new_thread
@login_required(login_url='login')
def updateTask(request, pk):

    task = Task.objects.get(id=pk)

    form = CreateTaskForm(instance=task)

    if request.method == 'POST':

        form = CreateTaskForm(request.POST, instance=task)

        if form.is_valid():

            task = form.save(commit=False)

            task.user = request.user

            task.save()
            logger.info('task updated by {}' .format(request.user.username))
            return redirect('viewtasks')

    context = {'form':form}

    return render(request, 'profile/updatetask.html', context=context)


#CRUD-DELETE
@start_new_thread
@login_required(login_url='login')
def deleteTask(request, pk):
    
    task = Task.objects.get(id=pk)

    if request.method == 'POST':
        
        task.delete()

        return redirect('viewtasks')
    logger.info('task deleted by {}' .format(request.user.username))
    return render(request, 'profile\deletetask.html')


#USER-CREATE
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':
        
        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    context = {'form':form}

    return render(request, 'register.html', context=context)

#USER-LOGIN
def login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                
                auth.login(request, user)

                return redirect('dashboard')

    context = {'form':form}
    logger.info('{} logged in' .format(request.user.username))
    return render(request, 'login.html', context=context)

#USER-LOGOUT
def logout(request):

    auth.logout(request)
    logger.info('{} logged out' .format(request.user.username))
    return redirect('')

#DASHBOARD
@login_required(login_url='login')
def dashboard(request):
    logger.info('{} opened dashboard' .format(request.user.username))
    return render(request, 'profile/dashboard.html')

@start_new_thread
@login_required(login_url='login')
def profileManager(request):
    
    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=request.user)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

    form = UpdateUserForm(instance=request.user)        

    context = {'form':form}
    logger.info('{} updated profile' .format(request.user.username))
    return render(request, 'profile\profilemanager.html', context=context)












