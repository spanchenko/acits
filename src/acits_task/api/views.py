from django.http import request
from .models import CustomUser, Flat, RentOrder, FlatRoom
from .serializers import CustomUserSerializer, FlatSerializer, RentOrderSerializer, FlatRoomSerializer, CreateCustomUserSerializer
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters


class RegisterView(views.APIView):
    parser_classes = [JSONParser]   

    def post(self, request):
        serializer = CreateCustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": CustomUserSerializer(user).data
        })


class UserViewSet(viewsets.ModelViewSet): 
    parser_classes = [JSONParser]   
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    serializer_class = CustomUserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    filter_fields = ('language', 'age')
    search_fields = ('email', 'phone', 'first_name', 'last_name')

    def get_queryset(self):
        if self.request.user.status == 'OWNER':
            return CustomUser.objects.filter(status='RENTER').order_by('first_name', 'last_name')
        else:
            return CustomUser.objects.filter(status='OWNER').order_by('first_name', 'last_name')



class FlatViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FlatSerializer
    parser_classes = [JSONParser]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    filter_fields = ('build', 'type', 'price', 'created_at')
    search_fields = ('price')

    def get_queryset(self):
        if self.request.method == 'GET':
            return Flat.objects.all().order_by('build__id', 'room_count', 'owner__id')
        else:
            return Flat.objects.filter(owner=self.request.user)


class RentOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RentOrderSerializer
    parser_classes = [JSONParser]
    def get_queryset(self):
            return RentOrder.objects.filter(renter=self.request.user).order_by('total_price')


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FlatRoomSerializer
    def get_queryset(self):
        if self.request.method == 'GET':
            return FlatRoom.objects.filter(flat=self.kwargs['flats_pk'])