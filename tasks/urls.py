
from django.urls import path
from .views import task_view, certificate_view

urlpatterns = [
    path("", task_view, name="task"),
    path("certificate/", certificate_view, name="certificate"),
]

