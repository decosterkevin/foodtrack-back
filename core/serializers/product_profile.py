from rest_framework import serializers

from core.models import Product
from core.serializers import SimpleProductorProfileSerializer, ProductSerializer

class FullProductSerializer(ProductSerializer):
    # location = AddressSerializer(source='creator.address', read_only=True)
    creator = SimpleProductorProfileSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    class Meta:
        model = Product
        fields = ("id", "name", "picture", 'is_favorite', 'description', 'creator', 'rating', 'created_at', 'updated_at',"category", "price", "quantity", "is_active", "is_deliverable", "delivery_time_days")
