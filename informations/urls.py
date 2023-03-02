from django.urls import path
from . import views

urlpatterns = [
    path("customer", views.CustNumList.as_view()),
    path("check", views.Check.as_view()),
    path("weather", views.Weather.as_view()),
]
