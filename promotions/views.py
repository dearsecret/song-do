from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .serializers import PromotionDetialSerializer, PromotionListSerializer
from .models import Promotion


class Promotions(APIView):
    def get(self, request):
        promotions = Promotion.objects.all().order_by("-pk")[:2]
        serializer = PromotionListSerializer(promotions, many=True)
        return Response(serializer.data)


class PromotionDetail(APIView):
    def get_object(self, pk):
        try:
            return Promotion.objects.get(pk=pk)
        except Promotion.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        promoiton = self.get_object(pk)
        serializer = PromotionDetialSerializer(promoiton)
        return Response(serializer.data)
