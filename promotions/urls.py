from django.urls import path
from .views import Promotions, PromotionDetail

urlpatterns = [
    path("", Promotions.as_view()),
    path("<int:pk>", PromotionDetail.as_view()),
]
