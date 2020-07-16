from django.contrib import admin
from django.contrib.gis import admin as admin_gis
from .models.address import Address
from .models.product import Product  # add this
from .models.profile import  ProductorProfile, UserProfile
from .models.cart import Cart, CartItem
# from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
# Register your models here.
# class ProductorAdmin(admin.ModelAdmin, DynamicArrayMixin):
#     pass

admin.site.register(Product)
admin_gis.site.register(Address, admin_gis.OSMGeoAdmin)
admin.site.register(ProductorProfile)
admin.site.register(UserProfile)
admin.site.register(Cart)
admin.site.register(CartItem)

# Register your models here.
