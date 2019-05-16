# 3rd party
from django.urls import path
from django.contrib.auth import views as auth_views

# local
from . import views
from .views import AdminOrderDetails
from .views import AdminOrders
from .views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('raise_pos/', views.raise_pos, name='raise_pos'),
    path(
        'login/',
        auth_views.LoginView.as_view(),
        {'template_name': 'login.html'},
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('summary/<int:pk>', views.order_summary, name='order_summary'),
    path('cancel_order/<int:pk>', views.cancel_order, name='cancel_order'),
    path('clear_order/<int:pk>', views.clear_order, name='clear_order'),
    path('auth_order/<int:pk>/<slug:auth>/', views.AuthOrder.as_view()),
    path('orders/<slug:area>', AdminOrders.as_view()),
    path('order_details/<int:pk>', AdminOrderDetails.as_view()),
]
