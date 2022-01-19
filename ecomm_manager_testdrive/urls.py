from django.contrib import admin
from django.urls import path, include

from .views import store_logs

urlpatterns = [
    path('store_logs/', store_logs)
]