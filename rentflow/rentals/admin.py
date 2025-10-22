from django.contrib import admin
from .models import RentalListing, Booking


@admin.register(RentalListing)
class RentalListingAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'property_type',
        'price_per_night',
        'owner',
        'is_published'
    ]
    list_filter = ['property_type', 'is_published', 'created_at']
    search_fields = ['title', 'address']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'rental_listing',
        'guest',
        'check_in_date',
        'check_out_date',
        'status'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['rental_listing__title', 'guest__username']
