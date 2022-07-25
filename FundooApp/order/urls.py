from django.urls import path, include
from . import views

urlpatterns = [
     path('order/', views.OrderViewSet.as_view())
]