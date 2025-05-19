from django.contrib import admin
from .models import CartModel,CartItemModel
# Register your models here.
@admin.register(CartModel)
class Cart_ModelAdmin(admin.ModelAdmin):
    list_display=["cart_id","user"]

@admin.register(CartItemModel)
class CartItem_ModelAdmin(admin.ModelAdmin):
    list_display=["cart_id","product_variant_id","quantity"]
