from django.urls import path
from . import views

urlpatterns = [
    path("", views.Rooms.as_view()),
    path("<int:pk>", views.RoomDetail.as_view()),
    path("<int:pk>/photos", views.RoomPhotos.as_view()),
    path("kind", views.Kinds.as_view()),
    path("kind/<int:pk>", views.KindDetail.as_view()),
    path("facility", views.Facilities.as_view()),
    path("facility/<int:pk>", views.FacilityDetail.as_view()),
]
