from rest_framework import serializers

from core.models import Cart, CartItem
from core.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = ("product","product_name", "quantity", "unit_price", "total_price", "id")
        # write_only_fields = ("cart",)
    def get_product_name(self, obj):
        return obj.product.name
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ( "items", "id", "items")
        