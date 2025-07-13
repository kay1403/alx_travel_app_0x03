from rest_framework import serializers
from .models import Listing


class ListingSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    location = serializers.CharField(max_length=100)
    price_per_night = serializers.DecimalField(max_digits=8, decimal_places=2)
    available = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)


class BookingSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    check_in = serializers.DateField()
    check_out = serializers.DateField()
    created_at = serializers.DateTimeField(read_only=True)
