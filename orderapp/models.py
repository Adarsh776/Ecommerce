from django.db import models
from coreapp.models import ProductModel
from authentication.models import Custom_UserModel

class OrdersModel(models.Model):
    order_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Custom_UserModel,on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=100)
    created_at=models.DateField(auto_now=True)
    ordered=models.BooleanField(default=False)
    order_item=models.ForeignKey("OrderItemModel",on_delete=models.CASCADE,default=False)


class OrderItemModel(models.Model):
    order_item_id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    ordered=models.BooleanField(default=False)


class ShippingModel(models.Model):
    shipping_id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(OrdersModel,on_delete=models.CASCADE)
    address=models.TextField()
    tracking_id=models.CharField(max_length=100)
    status=models.CharField(max_length=100)

