from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Cart(models.Model):
    creator = models.ForeignKey("core.UserProfile", on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checked_out = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return  self.creator.user.username
class CartItem(models.Model):
    product = models.ForeignKey("core.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    cart = models.ForeignKey('core.Cart', on_delete=models.CASCADE, related_name="items")
    
    def __str__(self):
        return  str(self.product.id)
    def total_price(self):
        return self.quantity * self.unit_price
    
    