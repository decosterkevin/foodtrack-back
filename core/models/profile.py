from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Cart
User = get_user_model()

class MyImage(models.Model):
    file = models.FileField(blank=True)
    name = models.CharField(max_length=120,default="")

class DeliveryMode(models.Model):
    title = models.CharField(max_length=120)
    modality = models.TextField(default="")
    delay = models.IntegerField(default=2)
    address = models.ForeignKey("core.Address", on_delete=models.CASCADE,blank=True,
        null=True)
    creator = models.ForeignKey("core.ProductorProfile", on_delete=models.CASCADE, related_name="custom_delivery_modes")

class ProductorProfile(models.Model):
    user = models.OneToOneField("authentication.User",  on_delete=models.CASCADE , related_name='productor_profile', null=True, blank=True)
    rating = models.DecimalField(default=6.0,blank=True, decimal_places=2, max_digits=3)
    name = models.CharField(max_length=120, default="")
    bio = models.TextField(blank=True)
    address = models.ForeignKey("core.Address", on_delete=models.CASCADE,blank=True,
        null=True)
    pictures = models.ManyToManyField(MyImage, blank=True)
    def __str__(self):
        return self.user.username

class UserProfile(models.Model):
    user = models.OneToOneField("authentication.User",   on_delete=models.CASCADE ,related_name='user_profile')
    picture = models.FileField(blank=True)
    saved_products = models.ManyToManyField("core.Product", blank=True, related_name="fans")
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    instance.user_profile.save()

@receiver(post_save, sender=UserProfile)
def create_or_update_cart(sender, instance, created, **kwargs):
    if created:
        cart = Cart(creator=instance)
        cart.save()
        instance.carts.add(cart)