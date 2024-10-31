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

from . import views

urlpatterns = [
    path("task/create/",views.TaskListCreateAPIView.as_view()),
    path("task/edit/<int:pk>",views.TaskRetrieveUpdateDestroyAPIView.as_view()),
    path("case/create/", views.CaseListCreateAPIView.as_view()),
    path("case/edit/<int:pk>", views.CaseRetrieveUpdateDestroyAPIView.as_view()),
]
