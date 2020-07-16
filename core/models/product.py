from django.db import models
from core.utils import ChoiceEnum
from django.contrib.postgres.fields import ArrayField

class ProductCategory(ChoiceEnum):

    BAKERY = 'bakery'
    ALCOOL = 'alcool'
    MEAT = 'meat'
    VEGETABLE = 'vegetable'

class Product(models.Model):
    name = models.CharField(max_length=120)
    product_code = models.CharField(max_length=120, default="")
    
    picture = models.FileField()    
    creator = models.ForeignKey("core.ProductorProfile", on_delete=models.CASCADE, related_name="products")
    price = models.FloatField(default=0.0)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(default=6.0, decimal_places=2, max_digits=3)
    category = models.CharField(max_length=120, default=ProductCategory.MEAT.name, choices=ProductCategory.choices())
    is_active = models.BooleanField(default=True)
    description = models.TextField(default="")

    is_deliverable = models.BooleanField(default=True)
    delivery_time_days = models.IntegerField(default=7)
    def __str_(self):
        return self.name


