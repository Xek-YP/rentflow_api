from rest_framework import serializers
from .models import RentalListing, Booking, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_dields = ('id',)


class RentalListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = RentalListing
        fields =(
            'id',
            'title',
            'description',
            'address',
            'property_type',
            'price_per_night',
            'max_guests',
            'bedrooms',
            'bathrooms',
            'amenities',
            'latitude',
            'longitude',
            'owner',
            'is_published',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('owner', 'created_at', 'updated_at')


class BookingSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    rental_listing = RentalListingSerializer(read_only=True)
    rental_listing_id = serializers.PrimaryKeyRelatedField(
        queryset=RentalListing.objects.all(),
        source='rental_listing',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = (
            'rental_listing_id',
            'rental_listing',
            'guest',
            'check_in_date',
            'check_out_date',
            'guest_count',
            'status',
            'total_price',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('guest', 'total_price', 'created_at', 'updated_at')
