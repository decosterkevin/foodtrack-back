from rest_framework import serializers

from core.models import Exploitation, Address
from drf_extra_fields.geo_fields import PointField

class AddressSerializer(serializers.ModelSerializer):
    # lat = PointSerializer(source='point.y', read_only=True)
    lat = PointField(source='point.y', read_only=True)
    lng = PointField(source='point.x', read_only=True)
    class Meta:
        model = Address
        fields = ("street", "street_cp", "city", "province", "postal_code", "country", "lat", "lng")


class ExploitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exploitation
        fields = ("address", "pictures", "creator")

