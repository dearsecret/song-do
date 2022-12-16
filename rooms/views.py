from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import KindSerializer, FacilitySerializer
from .models import Kind, Facility

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound


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


class KindDetail(APIView):
    def get_object(self, pk):
        try:
            return Kind.objects.get(pk=pk)
        except Kind.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        kind = self.get_object(pk)
        serializer = KindSerializer(kind)
        return Response(serializer.data)

    def put(self, request, pk):
        serializer = KindSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            kind = serializer.save()
            return Response(KindSerializer(kind).data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        kind = self.get_object(pk)
        kind.delete()
        return Response(status=HTTP_204_NO_CONTENT)


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


class FacilityDetail(APIView):
    def get_object(self, pk):
        try:
            return Facility.objects.get(pk=pk)
        except Facility.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        facility = self.get_object(pk)
        return Response(FacilitySerializer(facility).data)

    def put(self, request, pk):
        serializer = FacilitySerializer(data=request.data, partial=True)
        if serializer.is_valid():
            facility = serializer.save()
            return Response(FacilitySerializer(facility).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        facility = self.get_object(pk)
        facility.delete()
        return Response(status=HTTP_204_NO_CONTENT)
