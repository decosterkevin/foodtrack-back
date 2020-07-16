from django.db import models
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db.models.signals import post_save
from core.utils import get_location_from_address

class Address(models.Model):
    street = models.TextField()
    street_cp = models.TextField(default="")
    city = models.TextField()
    province = models.TextField(default="")
    postal_code = models.TextField()
    country = models.TextField()
    point  = PointField(default=Point(2.349014, 48.864716))

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if not created:
            return
        address_str = f'{instance.street}, {instance.postal_code}, {instance.city}, {instance.country}'
        (lat, lon) = get_location_from_address(address_str)
        instance.point = Point(lon, lat)
        instance.save()

post_save.connect(Address.post_create, sender=Address)