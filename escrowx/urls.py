"""
URL configuration for escrowx project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin  # type: ignore
from django.urls import path  # type: ignore

from item_control.views import initiate_item
from transaction_control.views import get_item_by_id, get_transaction_by_id, transaction
from user_control.views import login, register_user

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/register/", register_user, name="register"),
    path("auth/login/", login, name="login"),
    path("seller/item/", initiate_item, name="initiate_item"),
    path("transaction/", transaction, name="transaction"),
    path("get_transaction/", get_transaction_by_id, name="get_transaction"),
    path("get_item/<int:id>/", get_item_by_id, name="get_item"),
]
