from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(OrdersModel)
class Orders_ModelAdmin(admin.ModelAdmin):
    list_display=['total','status','created_at']

@admin.register(OrderItemModel)
class OrderItem_ModelAdmin(admin.ModelAdmin):
    list_display=['quatity','price']

@admin.register(ShippingModel)
class Shipping_ModelAdmin(admin.ModelAdmin):
    list_display=['address','tracking_id','status']