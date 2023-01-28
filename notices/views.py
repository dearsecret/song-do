from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .serializers import NoticeListSerializer, NoticeDetailSerializer
from .models import Notice

# Create your views here.


class NoticeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notices = Notice.objects.all()
        serializer = NoticeListSerializer(notices, many=True)
        return Response(serializer.data)


class NoticeDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Notice.objects.get(pk=pk)
        except Notice.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        notice = self.get_object(pk)
        serializer = NoticeDetailSerializer(notice)
        return Response(serializer.data)
