from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
import requests
from .serializers import (
    BillListSerializer,
    BillDetailSerializer,
    InvoiceListSerializer,
    InvoiceDetailSerializer,
)
from .models import Invoice, Bill


class BillList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bills = Bill.objects.all()
        serializer = BillListSerializer(bills, many=True)
        return Response(serializer.data)


class BillDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Bill.objects.get(pk=pk)
        except:
            raise NotFound

    def get(self, request, pk):
        bill = self.get_object(pk)
        return Response(BillDetailSerializer(bill).data)


class InvoiceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # try:
        #     page = request.data.get("page", 1)
        #     page = int(page)
        # except ValueError:
        #     page = 1
        # page_size = 10
        # start = (page - 1) * page_size
        # end = start + page_size

        # if request.user.is_staff:[start:end]
        invoice = Invoice.objects.all()
        # else:
        #     invoice = Invoice.objects.filter(contract__customer=request.user)[start:end]
        serializer = InvoiceListSerializer(invoice, many=True)
        return Response(serializer.data)


class InvoiceDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        # 권한 수정 요망
        invoice = self.get_object(pk)
        serializer = InvoiceDetailSerializer(invoice)
        if not request.user.is_host:
            if request.user != invoice.contract.customer:
                raise PermissionDenied()
        return Response(serializer.data)
