from geopy.geocoders import OpenCage
from django.conf import settings
from enum import Enum

def get_location_from_address(address):
    geolocator = OpenCage(api_key=settings.OPENCAGE_API_KEY)
    location = geolocator.geocode(address)

    if location.latitude and location.longitude:
        return (location.latitude, location.longitude)
    else:
        return None

class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]