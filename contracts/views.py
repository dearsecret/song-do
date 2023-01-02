from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import ContractSerializer
from .models import Contract

# Create your views here.


class Contracts(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        contracts = Contract.objects.all()
        return Response(ContractSerializer(contracts, many=True).data)
