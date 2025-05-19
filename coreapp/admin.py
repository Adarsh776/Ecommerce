from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(CategoriesModel)
class Categories_ModelAdmin(admin.ModelAdmin):
    list_display=['name','category_image','parent_category']

@admin.register(ProductModel)
class Product_ModelAdmin(admin.ModelAdmin):
    list_diplay=['category_id','name','description','product_type','created_at']

@admin.register(ProductVariantModel)
class ProductVariant_ModelAdmin(admin.ModelAdmin):
    list_display=["product_id","attribute","value","color","image1","image2","image3","stock","extra_price","original_price","sale_price","discount_per","slug"]

@admin.register(ProductAttributeModel)
class ProductAttribute_ModelAdmin(admin.ModelAdmin):
    list_display=["variant_id","attribute","value"]

@admin.register(PaymentsModel)
class Payments_ModelAdmin(admin.ModelAdmin):
    list_display=["amount","status","created_at"]

@admin.register(ReviewsModel)
class Reviews_ModelAdmin(admin.ModelAdmin):
    list_display=["rating","review","created_at"]

@admin.register(DigitalProductModel)
class DigitalProduct_ModelAdmin(admin.ModelAdmin):
    list_display=["file_url"]

