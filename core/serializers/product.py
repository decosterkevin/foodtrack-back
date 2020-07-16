from rest_framework import serializers

from core.models import Product
# from core.serializers import ProductorProfileSerializer

# class ProductBasicSerializer(serializers.ModelSerializer):
#     # location = AddressSerializer(source='creator.address', read_only=True)
#     rating = serializers.FloatField(read_only=True)
#     quantity = serializers.IntegerField()
#     price = serializers.FloatField()
#     class Meta:
#         model = Product
#         fields = ("id", "name", "picture", 'description', 'rating', 'created_at',"category", "price", "quantity", "is_active", "is_deliverable", "delivery_time_days")

class ProductSerializer(serializers.ModelSerializer):
    # location = AddressSerializer(source='creator.address', read_only=True)
    # creator = ProductorProfileSerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    is_favorite = serializers.SerializerMethodField(read_only =True)
    class Meta:
        model = Product
        fields = ("id", "name", "picture", 'description','is_favorite', 'creator', 'rating', 'created_at', 'updated_at',"category", "price", "quantity", "is_active", "is_deliverable", "delivery_time_days")

    def get_is_favorite(self, obj):
        user =  self.context['request'].user
        if user:
            if user.user_profile.saved_products.filter(pk=obj.id).first():
                return True
        
        return False