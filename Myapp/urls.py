"""
URL configuration for ToDo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from setuptools.extern import names

from . import views

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tasks/", views.TaskListCreateAPIView.as_view(), name="tasks_list_create"),
    path(
        "task/<int:pk>/",
        views.TaskRetrieveUpdateDestroyAPIView.as_view(),
        name="task_retrieve_update_destroy",
    ),
    path("cases/", views.CaseListCreateAPIView.as_view(), name="cases_list_create"),
    path(
        "case/<int:pk>/",
        views.CaseRetrieveUpdateDestroyAPIView.as_view(),
        name="case_retrieve_update_destroy",
    ),
]
