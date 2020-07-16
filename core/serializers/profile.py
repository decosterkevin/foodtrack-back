
from rest_framework import serializers
from core.models import ProductorProfile, UserProfile, MyImage
from core.serializers import AddressSerializer, ProductSerializer, CartSerializer
class MyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyImage
        fields = ("file", "name")


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    saved_products = ProductSerializer(many=True)
    current_cart = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ("id", "picture", "saved_products", "carts", "current_cart")

    def get_current_cart(self, obj):
        cart = obj.carts.filter(checked_out=False).first()
        serializer = CartSerializer(cart)
        return serializer.data

class ProductorProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    address = AddressSerializer()
    rating = serializers.FloatField(read_only=True)
    pictures = serializers.ListSerializer(child=MyImageSerializer(), required=False, allow_null=True)
    user_picture = serializers.FileField(source="user.user_profile.picture", read_only=True)
    products = ProductSerializer(many=True, required=False, allow_null=True)
    class Meta:
        model = ProductorProfile
        fields = ("id", "rating", "address", "pictures", "bio", "name", "user_picture", 'products')
        read_only_fields = ("id", "user_picture","rating")

class SimpleProductorProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    address = AddressSerializer()
    rating = serializers.FloatField(read_only=True)
    pictures = serializers.ListSerializer(child=MyImageSerializer())
    user_picture = serializers.FileField(source="user.user_profile.picture", read_only=True)
    class Meta:
        model = ProductorProfile
        fields = ("id", "rating", "address", "pictures", "bio", "name", "user_picture")
        read_only_fields = ("id", "user_picture","rating")
