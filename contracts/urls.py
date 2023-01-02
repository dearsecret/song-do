from django.urls import path
from . import views

urlpatterns = [
    path("", views.Contracts.as_view()),
]
