from django.urls import path
from . import views


urlpatterns = [
    path("bills", views.BillList.as_view()),
    path("bills/<int:pk>", views.BillDetail.as_view()),
    path("pages/", views.InvoiceList.as_view()),
    path("<int:pk>", views.InvoiceDetail.as_view()),
]
