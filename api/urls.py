from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.users_api),
    path('orders/', views.orders_api),
    path('orders/<int:order_id>', views.order_api),   
    path('users/<int:user_id>', views.user_api),
]