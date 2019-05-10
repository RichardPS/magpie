from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('summary/<int:pk>', views.order_summary, name='order_summary')
]
