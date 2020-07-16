from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
User = get_user_model()
from .utils import *
from core.serializers import ProductorProfileSerializer, UserProfileSerializer
from core.models import Address, ProductorProfile
class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    # productor_profile = ProductorProfileSerializer(default=None)
    
    def update(self, instance, data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.username = data.get('username', instance.username)
        # instance.first_name = data.get('first_name', instance.first_name)
        # instance.last_name = data.get('last_name', instance.last_name)
        instance.email = data.get('email', instance.email)
        instance.is_deliverer = data.get('is_deliverer', instance.is_deliverer)
        instance.is_productor = data.get('is_productor', instance.is_productor)
        instance.created_at = data.get('created_at', instance.created_at)
        instance.birth_date =  data.get('birth_date', instance.birth_date)
        # instance.user_profile =  data.get('user_profile', instance.user_profile)
        # instance.productor_profile =  data.get('productor_profile', instance.productor_profile)
        # instance.is_staff = data.get('is_staff', instance.is_staff)
        # instance.is_superuser = data.get('is_superuser', instance.is_staff)
        # instance.set_password(data.get('password'))
        instance.save()
        return instance 
        
    class Meta:
        model = User
        fields= ("id","username","email","is_deliverer","is_productor", "birth_date", "created_at", "user_profile", "productor_profile")


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # # The client should not be able to send a token along with a registration
    # # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)
    productor_profile = ProductorProfileSerializer(default=None)
    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ('email', 'username', 'password', 'token', 'is_productor', 'birth_date', 'productor_profile')

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        productor_profile_data = validated_data.pop('productor_profile', None)
        user = User.objects.create_user(**validated_data)
        if productor_profile_data:
            address_data = productor_profile_data.pop('address', None)
            if address_data:
                address = Address.objects.create(**address_data)
                productor_profile_data['address'] = address
            productor_profile = ProductorProfile.objects.create(user=user, **productor_profile_data)
            user.productor_profile = productor_profile
            user.save()
        return user

class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """
    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )

