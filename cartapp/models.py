from django.db import models
from coreapp.models import  ProductVariantModel
from authentication.models import Custom_UserModel

# Create your models here.
class CartModel(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Custom_UserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Cart {self.cart_id} - {self.user.username}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_original_price(self):
        return sum(item.quantity * item.product_variant_id.original_price for item in self.items.all())

    @property
    def total_discount(self):
        return self.total_original_price - self.total_price

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def delivery_charge(self):
        # Customize: Free delivery above ₹5000
        return 0 if self.total_price > 5000 else 100

    @property
    def packaging_fee(self):
        return 218  # Can be made dynamic later if needed

    @property
    def total_payable(self):
        return self.total_price + self.delivery_charge + self.packaging_fee
    


class CartItemModel(models.Model):
    cart_id=models.ForeignKey(CartModel, on_delete=models.CASCADE,related_name='items')
    product_variant_id=models.ForeignKey(ProductVariantModel, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    selected_attribute_value = models.CharField(max_length=100, null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant_id.product_id.name} - {self.cart_id.cart_id}"

    @property
    def total_price(self):
        return self.quantity * self.product_variant_id.sale_price
        

