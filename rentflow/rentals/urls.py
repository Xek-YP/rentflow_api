from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RentalListingViewSet, BookingViewSet

router_v1 = DefaultRouter()
router_v1.register(r'listings', RentalListingViewSet)
router_v1.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]