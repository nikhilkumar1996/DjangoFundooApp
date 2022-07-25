from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
     path('bookstore/', views.BookStore.as_view()),
     path('bookstore/<int:id>/<int:number>', views.BookStore.as_view()),
     path('bookstore/<int:id>', views.BookStore.as_view())
]