from django.urls import path
from . import views

urlpatterns = [
    path("me", views.Me.as_view()),
    path("login", views.LogIn.as_view()),
    path("logout", views.LogOut.as_view()),
    path("change", views.ChangePassword.as_view()),
    path("new", views.NewUser.as_view()),
]
