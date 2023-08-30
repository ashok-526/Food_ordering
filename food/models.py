from django.db import models
from django.contrib.auth.models import User

import uuid

class Basemodel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  # Use auto_now instead of auto_now_add

    class Meta:
        abstract = True

class Categories(Basemodel):  
    category_name = models.CharField(max_length=100)

class Pizza(Basemodel):  
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='food')
    pizza_name = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to='media')

class Cart(Basemodel):  #
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='carts')
    is_paid = models.BooleanField(default=False)
    esewa = models.CharField(max_length=1000)
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart with no user"


class CartItem(Basemodel):  
    cart_reference = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='food_items')  
    pizza_reference = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Add this field to represent the quantity

    