from django.urls import path
from . import views

urlpatterns = [    

    path('', views.home, name=''),

    #CRUD

    path('createtask', views.createTask, name='createtask'),

    path('viewtasks', views.viewTasks, name='viewtasks'),

    path('updatetask/<str:pk>/', views.updateTask, name='updatetask'),

    path('deletetask/<str:pk>/', views.deleteTask, name='deletetask'),

    #USERS

    path('register', views.register, name='register'),

    path('login', views.login, name='login'),

    path('logout', views.logout, name='logout'),

    path('dashboard', views.dashboard, name='dashboard'),

    path('profilemanager', views.profileManager, name='profilemanager'),

    #THREAD


    #path('readtasks', views.viewTasks),

] 