from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import KindSerializer, FacilitySerializer
from .models import Kind, Facility

from rest_framework.status import HTTP_400_BAD_REQUEST


class Kinds(APIView):
    # authentication_classes

    def get(self, request):
        all_kinds = Kind.objects.all()
        serializer = KindSerializer(all_kinds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = KindSerializer(data=request.data)
        if serializer.is_valid():
            kinds = serializer.save()
            return Response(KindSerializer(kinds).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Facilities(APIView):
    # authentication_classes

    def get(self, request):
        all_facilities = Facility.objects.all()
        serializer = FacilitySerializer(all_facilities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FacilitySerializer(data=request.data)
        if serializer.is_valid():
            new_facility = serializer.save()
            return Response(FacilitySerializer(new_facility).data)
        else:
            return Response(serializer.errors)
