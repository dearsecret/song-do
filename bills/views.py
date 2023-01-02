from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
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
        # 권한 수정 요망
        invoice = Invoice.objects.all()
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
        return Response(serializer.data)
