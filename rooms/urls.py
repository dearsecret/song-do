from django.urls import path
from . import views

urlpatterns = [
    path("kind", views.Kinds.as_view()),
    path("facility", views.Facilities.as_view()),
]
