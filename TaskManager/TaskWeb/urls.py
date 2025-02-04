from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('newTask/', views.addNewTask, name='task'),
    path('editTask/<int:task_id>', views.editTask, name='editTask'),
    path('deleteTask/<int:task_id>', views.deleteTask, name='deleteTask'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]