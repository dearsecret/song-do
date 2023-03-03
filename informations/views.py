from django.conf import settings
import requests
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import CustSerializer, BillingSerializer, WeatherSerializer
from .models import Customer, Billing
from realtimes.models import WeatherFcst


class CustNumList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        cust = Customer.objects.all()
        serializer = CustSerializer(cust, many=True)
        return Response(serializer.data)


class Check(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            custNo = request.query_params.get("custNo")
            bill_ym = request.query_params.get("bill_ym")
            bill_ym = int(bill_ym)
            if not len(bill_ym) == 6:
                return Response({"error": "날짜형식을 확인해주세요."})
            cust = Customer.objects.get(custNum=custNo)
        except Customer.DoesNotExist:
            return Response({"error": "고객번호를 확인해주세요"})
        if Billing.objects.filter(custNo=cust, bill_ym=bill_ym).exists():
            billing = Billing.objects.filter(custNo=cust, bill_ym=bill_ym)
            serializer = BillingSerializer(billing)
            return Response(serializer.data)
        res = requests.get(
            f"https://opm.kepco.co.kr:11080/OpenAPI/getCustBillData.do?custNo={custNo}&dataMonth={bill_ym}&serviceKey={settings.BILLING_KEY}&returnType=02"
        )
        data = res.json()
        data = data.get("custBillDataInfoList")
        serializer = BillingSerializer(data=data)
        if serializer.is_valid():
            serializer.save(custNo=cust)
            return Response(data)
        else:
            return Response(serializer.errors)


class Weather(APIView):
    def get(self, request):
        weathers = WeatherFcst.objects.all().order_by("pk")[0]
        serializer = WeatherSerializer(weathers)
        return Response(serializer.data)
