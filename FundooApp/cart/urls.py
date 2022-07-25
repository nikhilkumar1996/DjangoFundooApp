from django.urls import path, include
from . import views

urlpatterns = [
     path('cart/', views.CartOperations.as_view()),
     path('cart/<int:value>', views.CartOperations.as_view()),
     path('delete_cart/<int:id>', views.DeleteCart.as_view()),
]