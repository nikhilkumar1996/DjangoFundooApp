from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path('register/', views.Register.as_view(), name='register'),
     path('login/', views.Login.as_view(), name='login'),
     path('getallusers/', views.GetAllUsers.as_view(), name='getallusers'),
     path('activate/<int:user_id>/', views.ActivateUser.as_view()),
     path('authuser/', views.AuthUserCheck.as_view())

]