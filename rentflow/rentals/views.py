from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import viewsets, permissions

from .models import RentalListing, Booking
from .serializers import RentalListingSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly, IsBookingParticipant

class RentalListingViewSet(viewsets.ModelViewSet):
    queryset = RentalListing.objects.filter(is_published=True)
    serializer_class = RentalListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['property_type', 'price_per_night', 'max_guests']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsBookingParticipant]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['status',]

    def get_queryset(self):
        return Booking.objects.filter(
            Q(guest=self.request.user) |
            Q(rental_listing__owner=self.request.user)
        ).distinct()
    
    def perform_create(self, serializer):
        serializer.save(guest=self.request.user)