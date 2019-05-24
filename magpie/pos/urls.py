# 3rd party
from django.urls import path
from django.contrib.auth import views as auth_views

# local
from . import views
from .views import AddUser
from .views import AdminOrderDetails
from .views import AdminOrders
from .views import EditUser
from .views import Index
from .views import OrderSummary
from .views import UserManagement

from .views import RaisePos

urlpatterns = [
    path("", Index.as_view(), name="index"),
    # path("raise_order/", RaisePos.as_view(), name="raise_order"),
    path("raise_pos/", views.raise_pos, name="raise_pos"),
    path("summary/<int:pk>", OrderSummary.as_view(), name="order_summary"),
    path("cancel_order/<int:pk>", views.cancel_order, name="cancel_order"),
    path("clear_order/<int:pk>", views.clear_order, name="clear_order"),
    path("auth_order/<int:pk>/<slug:auth>/", views.AuthOrder.as_view()),
    path("orders/<slug:area>", AdminOrders.as_view()),
    path("order_details/<int:pk>", AdminOrderDetails.as_view()),
    path("user_management", UserManagement.as_view(), name="user_management"),
    path("edit_user/<int:pk>", EditUser.as_view()),
    path("add_user/", AddUser.as_view()),
    path(
        "login/",
        auth_views.LoginView.as_view(),
        {"template_name": "login.html"},
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(),
        {"template_name": "password_reset_form.html"},
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        {"template_name": "password_reset_done.html"},
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        {"template_name": "password_reset_confirm.html"},
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        {"template_name": "password_reset_complete.html"},
        name="password_reset_complete",
    ),
]
