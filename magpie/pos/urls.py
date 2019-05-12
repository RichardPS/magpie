from django.urls import path

from . import views
from .views import AdminOrderDetails
from .views import AdminOrders

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/<int:pk>', views.order_summary, name='order_summary'),
    path('orders/<slug:area>', AdminOrders.as_view()),
    path('order_details/<int:pk>', AdminOrderDetails.as_view()),
]
