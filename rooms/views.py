from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    KindSerializer,
    FacilitySerializer,
    RoomSerializer,
    RoomDetailSerializer,
)
from medias.serializers import PhotoSerializer
from .models import Kind, Facility, Room

from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.exceptions import NotFound, PermissionDenied


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
    # authentication_classes
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
    # authentication_classes
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


class Rooms(APIView):
    # authentication_classes

    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room, context={"request", request})
        return Response(serializer.data)


class RoomPhotos(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        if request.user != room.host:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
