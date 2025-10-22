from django.db import models
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import RentalListing, Booking
from .serializers import RentalListingSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly

class RentalListingViewSet(viewsets.ModelViewSet):
    queryset = RentalListing.objects.filter(is_published=True)
    serializer_class = RentalListingSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'bedrooms', 'bathrooms', 'max_guests']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Получить все бронирования для данного объявления"""
        rental_listing = self.get_object()
        bookings = Booking.objects.filter(rental_listing=rental_listing)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(
            models.Q(guest=user) | 
            models.Q(rental_listing__owner=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)