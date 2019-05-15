from django.urls import path

from . import views
from .views import AdminOrderDetails
from .views import AdminOrders

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/<int:pk>', views.order_summary, name='order_summary'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
    path('clear_order/<int:pk>', views.clear_order, name='clear_order'),
    path('auth_order/<int:pk>/<slug:auth>/', views.AuthOrder.as_view()),
    path('orders/<slug:area>', AdminOrders.as_view()),
    path('order_details/<int:pk>', AdminOrderDetails.as_view()),
]
